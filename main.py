import cv2

from camera import abrir_camera
from config import ROI_X_MAX, ROI_X_MIN, ROI_Y_MAX, ROI_Y_MIN
from controller import MouseController
from gesture_detector import GestureDetector, NEUTRO, centro_palma
from hand_tracker import HandTracker


def desenhar_interface(frame, mao, gesto):
    altura, largura = frame.shape[:2]

    x1 = int(ROI_X_MIN * largura)
    x2 = int(ROI_X_MAX * largura)
    y1 = int(ROI_Y_MIN * altura)
    y2 = int(ROI_Y_MAX * altura)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

    if mao is not None:
        x, y = centro_palma(mao)
        cx = int(x * largura)
        cy = int(y * altura)
        cv2.circle(frame, (cx, cy), 10, (255, 255, 255), -1)

    cv2.putText(
        frame,
        f"Gesto: {gesto}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    instrucoes = [
        "Palma aberta: mover",
        "Pinca indicador: clique | segurar: arrastar",
        "Pinca dedo medio: clique direito",
        "Indicador + medio: scroll",
        "Punho: pausa | Q/ESC: sair",
    ]

    y_texto = 70
    for texto in instrucoes:
        cv2.putText(
            frame,
            texto,
            (20, y_texto),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
        )
        y_texto += 23

    return frame


def main():
    camera = abrir_camera()
    tracker = HandTracker()
    detector = GestureDetector()
    mouse = MouseController()

    print("Sistema iniciado. Pressione Q ou ESC na janela da webcam para sair.")

    try:
        while True:
            sucesso, frame = camera.read()

            if not sucesso:
                print("Falha ao capturar frame da camera.")
                break

            # Espelhamento deixa o controle intuitivo: mao direita -> cursor direita.
            frame = cv2.flip(frame, 1)

            frame, mao, lado_mao = tracker.processar(frame)

            gesto = NEUTRO
            if mao is not None:
                gesto = detector.detectar(mao, lado_mao)

            # Tambem atualizamos sem mao para liberar qualquer arrasto com seguranca.
            mouse.atualizar(gesto, mao)

            frame = desenhar_interface(frame, mao, gesto)
            cv2.imshow("Your Hand Is The Mouse", frame)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla in (ord("q"), 27):
                break

    finally:
        mouse.encerrar()
        tracker.fechar()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
