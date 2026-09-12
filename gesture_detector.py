import math

from config import (
    PINCH_RELEASE_RATIO,
    PINCH_START_RATIO,
    RIGHT_PINCH_RELEASE_RATIO,
    RIGHT_PINCH_START_RATIO,
)

PALMA_ABERTA = "PALMA_ABERTA"
PINCA = "PINCA"
PINCA_MEDIA = "PINCA_MEDIA"
SCROLL = "SCROLL"
PUNHO = "PUNHO"
NEUTRO = "NEUTRO"


def _distancia(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def centro_palma(mao):
    """Centro estavel calculado pela base dos dedos e pelo pulso."""
    indices = (0, 5, 9, 13, 17)
    pontos = [mao.landmark[i] for i in indices]
    x = sum(p.x for p in pontos) / len(pontos)
    y = sum(p.y for p in pontos) / len(pontos)
    return x, y


def tamanho_palma(mao):
    """Escala aproximada da mao para tornar gestos independentes da distancia da camera."""
    largura = _distancia(mao.landmark[5], mao.landmark[17])
    altura = _distancia(mao.landmark[0], mao.landmark[9])
    return max((largura + altura) / 2, 1e-6)


def _angulo(a, b, c):
    """Angulo ABC em graus. Dedos estendidos ficam proximos de 180 graus."""
    ba_x, ba_y = a.x - b.x, a.y - b.y
    bc_x, bc_y = c.x - b.x, c.y - b.y

    produto = ba_x * bc_x + ba_y * bc_y
    norma_ba = math.hypot(ba_x, ba_y)
    norma_bc = math.hypot(bc_x, bc_y)

    if norma_ba == 0 or norma_bc == 0:
        return 0.0

    cos_angulo = max(-1.0, min(1.0, produto / (norma_ba * norma_bc)))
    return math.degrees(math.acos(cos_angulo))


def dedo_levantado(mao, ponta, articulacao):
    # Para os quatro dedos principais: MCP = ponta - 3, PIP = ponta - 2.
    # O angulo torna a deteccao menos dependente da rotacao da mao na imagem.
    mcp = mao.landmark[ponta - 3]
    pip = mao.landmark[articulacao]
    tip = mao.landmark[ponta]
    return _angulo(mcp, pip, tip) > 155


def indicador_levantado(mao):
    return dedo_levantado(mao, 8, 6)


def medio_levantado(mao):
    return dedo_levantado(mao, 12, 10)


def anelar_levantado(mao):
    return dedo_levantado(mao, 16, 14)


def mindinho_levantado(mao):
    return dedo_levantado(mao, 20, 18)


def polegar_levantado(mao, lado_mao):
    ponta = mao.landmark[4]
    articulacao = mao.landmark[3]

    if lado_mao == "Right":
        return ponta.x < articulacao.x
    return ponta.x > articulacao.x


def distancia_pinca_indicador(mao):
    return _distancia(mao.landmark[4], mao.landmark[8]) / tamanho_palma(mao)


def distancia_pinca_medio(mao):
    return _distancia(mao.landmark[4], mao.landmark[12]) / tamanho_palma(mao)


class GestureDetector:
    """Reconhece gestos com histerese para evitar troca de estado por ruido."""

    def __init__(self):
        self._pinch_index_ativo = False
        self._pinch_medio_ativo = False

    def detectar(self, mao, lado_mao):
        if mao is None:
            self._pinch_index_ativo = False
            self._pinch_medio_ativo = False
            return NEUTRO

        pinch_index = distancia_pinca_indicador(mao)
        pinch_medio = distancia_pinca_medio(mao)

        # Histerese: um limite para entrar no gesto e outro para sair.
        if self._pinch_index_ativo:
            self._pinch_index_ativo = pinch_index < PINCH_RELEASE_RATIO
        else:
            self._pinch_index_ativo = pinch_index < PINCH_START_RATIO

        if self._pinch_medio_ativo:
            self._pinch_medio_ativo = pinch_medio < RIGHT_PINCH_RELEASE_RATIO
        else:
            self._pinch_medio_ativo = pinch_medio < RIGHT_PINCH_START_RATIO

        # A pinca do indicador tem prioridade sobre qualquer outro gesto.
        if self._pinch_index_ativo:
            return PINCA

        if self._pinch_medio_ativo:
            return PINCA_MEDIA

        indicador = indicador_levantado(mao)
        medio = medio_levantado(mao)
        anelar = anelar_levantado(mao)
        mindinho = mindinho_levantado(mao)

        dedos_principais = (indicador, medio, anelar, mindinho)

        # Ignoramos o polegar na palma aberta para deixar o controle mais tolerante.
        if all(dedos_principais):
            return PALMA_ABERTA

        if indicador and medio and not anelar and not mindinho:
            return SCROLL

        if not any(dedos_principais):
            return PUNHO

        return NEUTRO


# Funcoes de compatibilidade com a versao anterior.
def gesto_clique(mao):
    return distancia_pinca_indicador(mao) < PINCH_START_RATIO


def detectar_gesto(mao, lado_mao):
    # Mantido apenas para scripts antigos. No main novo use GestureDetector().
    detector = GestureDetector()
    return detector.detectar(mao, lado_mao)
