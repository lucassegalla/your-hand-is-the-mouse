import math
import time

import pyautogui

from config import (
    CURSOR_DEADZONE_PX,
    DRAG_HOLD_SECONDS,
    FILTER_BETA,
    FILTER_D_CUTOFF,
    FILTER_MIN_CUTOFF,
    ROI_X_MAX,
    ROI_X_MIN,
    ROI_Y_MAX,
    ROI_Y_MIN,
    SCROLL_DEADZONE,
    SCROLL_SENSITIVITY,
)
from gesture_detector import (
    NEUTRO,
    PALMA_ABERTA,
    PINCA,
    PINCA_MEDIA,
    PUNHO,
    SCROLL,
    centro_palma,
)

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False


def _clamp(valor, minimo=0.0, maximo=1.0):
    return max(minimo, min(maximo, valor))


class LowPassFilter:
    def __init__(self):
        self.valor = None

    def filtrar(self, valor, alpha):
        if self.valor is None:
            self.valor = valor
        else:
            self.valor = alpha * valor + (1 - alpha) * self.valor
        return self.valor


class OneEuroFilter:
    """Filtro adaptativo: suave parado, responsivo quando a mao acelera."""

    def __init__(self, min_cutoff, beta, d_cutoff):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_filter = LowPassFilter()
        self.dx_filter = LowPassFilter()
        self.ultimo_tempo = None
        self.ultimo_x = None

    @staticmethod
    def _alpha(cutoff, dt):
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def filtrar(self, x, agora):
        if self.ultimo_tempo is None:
            self.ultimo_tempo = agora
            self.ultimo_x = x
            self.x_filter.valor = x
            self.dx_filter.valor = 0.0
            return x

        dt = max(agora - self.ultimo_tempo, 1e-4)
        dx = (x - self.ultimo_x) / dt

        alpha_d = self._alpha(self.d_cutoff, dt)
        dx_filtrado = self.dx_filter.filtrar(dx, alpha_d)

        cutoff = self.min_cutoff + self.beta * abs(dx_filtrado)
        alpha = self._alpha(cutoff, dt)
        x_filtrado = self.x_filter.filtrar(x, alpha)

        self.ultimo_tempo = agora
        self.ultimo_x = x
        return x_filtrado

    def reset(self):
        self.x_filter = LowPassFilter()
        self.dx_filter = LowPassFilter()
        self.ultimo_tempo = None
        self.ultimo_x = None


class MouseController:
    def __init__(self):
        self.largura_tela, self.altura_tela = pyautogui.size()

        self.filtro_x = OneEuroFilter(
            FILTER_MIN_CUTOFF, FILTER_BETA, FILTER_D_CUTOFF
        )
        self.filtro_y = OneEuroFilter(
            FILTER_MIN_CUTOFF, FILTER_BETA, FILTER_D_CUTOFF
        )

        posicao = pyautogui.position()
        self.ultimo_x = posicao.x
        self.ultimo_y = posicao.y

        self.gesto_anterior = NEUTRO
        self.inicio_pinca = None
        self.arrastando = False
        self.scroll_y_anterior = None
        self.ultimo_right_click = 0.0

    def _mapear_palma_para_tela(self, mao, agora):
        x, y = centro_palma(mao)

        x = (x - ROI_X_MIN) / (ROI_X_MAX - ROI_X_MIN)
        y = (y - ROI_Y_MIN) / (ROI_Y_MAX - ROI_Y_MIN)

        x = _clamp(x)
        y = _clamp(y)

        x = self.filtro_x.filtrar(x, agora)
        y = self.filtro_y.filtrar(y, agora)

        destino_x = int(x * (self.largura_tela - 1))
        destino_y = int(y * (self.altura_tela - 1))

        return destino_x, destino_y

    def _mover(self, mao, agora):
        x, y = self._mapear_palma_para_tela(mao, agora)

        distancia = math.hypot(x - self.ultimo_x, y - self.ultimo_y)
        if distancia < CURSOR_DEADZONE_PX:
            return

        pyautogui.moveTo(x, y, duration=0)
        self.ultimo_x = x
        self.ultimo_y = y

    def _finalizar_pinca(self):
        if self.inicio_pinca is None:
            return

        if self.arrastando:
            pyautogui.mouseUp(button="left")
        else:
            pyautogui.click(button="left")

        self.inicio_pinca = None
        self.arrastando = False

    def _processar_pinca(self, mao, agora):
        # Cursor continua acompanhando a palma durante a pinca/arrasto.
        self._mover(mao, agora)

        if self.gesto_anterior != PINCA:
            self.inicio_pinca = agora
            self.arrastando = False
            return

        if (
            self.inicio_pinca is not None
            and not self.arrastando
            and agora - self.inicio_pinca >= DRAG_HOLD_SECONDS
        ):
            pyautogui.mouseDown(button="left")
            self.arrastando = True

    def _processar_scroll(self, mao):
        _, y = centro_palma(mao)

        if self.gesto_anterior != SCROLL or self.scroll_y_anterior is None:
            self.scroll_y_anterior = y
            return

        delta = self.scroll_y_anterior - y

        if abs(delta) >= SCROLL_DEADZONE:
            passos = int(delta * SCROLL_SENSITIVITY)
            if passos != 0:
                pyautogui.scroll(passos)
                self.scroll_y_anterior = y

    def atualizar(self, gesto, mao):
        agora = time.perf_counter()

        # Se a mao sumir, nunca deixe um arrasto preso nem gere clique fantasma.
        if mao is None:
            if self.arrastando:
                pyautogui.mouseUp(button="left")
            self.arrastando = False
            self.inicio_pinca = None
            self.scroll_y_anterior = None
            self.gesto_anterior = NEUTRO
            self.filtro_x.reset()
            self.filtro_y.reset()
            return

        # Sair da pinca conclui clique curto ou solta um arrasto.
        if self.gesto_anterior == PINCA and gesto != PINCA:
            self._finalizar_pinca()

        if gesto == PALMA_ABERTA:
            self._mover(mao, agora)

        elif gesto == PINCA:
            self._processar_pinca(mao, agora)

        elif gesto == PINCA_MEDIA:
            # Um clique por entrada no gesto.
            if self.gesto_anterior != PINCA_MEDIA:
                pyautogui.rightClick()
                self.ultimo_right_click = agora

        elif gesto == SCROLL:
            self._processar_scroll(mao)

        elif gesto == PUNHO:
            # PUNHO funciona como estado neutro/pausa.
            pass

        if gesto != SCROLL:
            self.scroll_y_anterior = None

        if gesto not in (PALMA_ABERTA, PINCA):
            # Ao reentrar no movimento, o filtro se adapta rapidamente a nova posicao.
            if self.gesto_anterior in (PALMA_ABERTA, PINCA):
                self.filtro_x.reset()
                self.filtro_y.reset()

        self.gesto_anterior = gesto

    def encerrar(self):
        if self.arrastando:
            pyautogui.mouseUp(button="left")
        self.arrastando = False
        self.inicio_pinca = None
