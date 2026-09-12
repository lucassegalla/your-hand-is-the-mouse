import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.65,
        )

    def processar(self, frame):
        """Detecta uma mao e retorna frame, landmarks e lado da mao."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = self.hands.process(frame_rgb)

        if not resultado.multi_hand_landmarks:
            return frame, None, None

        mao = resultado.multi_hand_landmarks[0]
        lado_mao = resultado.multi_handedness[0].classification[0].label

        mp_drawing.draw_landmarks(
            frame,
            mao,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style(),
        )

        return frame, mao, lado_mao

    def fechar(self):
        self.hands.close()


# Mantem compatibilidade com o formato usado nas etapas anteriores do projeto.
_tracker_padrao = HandTracker()


def detectar_mao(frame):
    return _tracker_padrao.processar(frame)
