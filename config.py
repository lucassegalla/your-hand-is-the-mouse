# Configuracoes centrais do projeto.
# Ajuste estes valores para calibrar o comportamento sem alterar a logica.

CAMERA_INDEX = 1
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30

# Regiao da imagem usada para controlar 100% da tela.
# Quanto menor esta regiao, menor o movimento fisico necessario com a mao.
ROI_X_MIN = 0.36
ROI_X_MAX = 0.64
ROI_Y_MIN = 0.28
ROI_Y_MAX = 0.62

# Filtro One Euro: suaviza quando a mao esta parada e responde mais rapido em movimento.
FILTER_MIN_CUTOFF = 1.2
FILTER_BETA = 1.5
FILTER_D_CUTOFF = 1.0
CURSOR_DEADZONE_PX = 2

# Gestos de pinca normalizados pelo tamanho da palma.
PINCH_START_RATIO = 0.32
PINCH_RELEASE_RATIO = 0.42
RIGHT_PINCH_START_RATIO = 0.30
RIGHT_PINCH_RELEASE_RATIO = 0.40

# Segurar a pinca por este tempo inicia arrastar.
DRAG_HOLD_SECONDS = 0.38

# Scroll: movimento vertical da palma com indicador + medio levantados.
SCROLL_SENSITIVITY = 115
SCROLL_DEADZONE = 0.006
