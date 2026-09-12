import cv2

from config import CAMERA_FPS, CAMERA_HEIGHT, CAMERA_INDEX, CAMERA_WIDTH


def abrir_camera(indice=CAMERA_INDEX):
    """Abre a webcam configurada usando DirectShow no Windows."""
    camera = cv2.VideoCapture(indice, cv2.CAP_DSHOW)

    if not camera.isOpened():
        raise RuntimeError(
            f"Nao foi possivel abrir a camera de indice {indice}. "
            "Altere CAMERA_INDEX em config.py."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

    return camera
