# Your Hand Is The Mouse

Aplicação desenvolvida em Python com foco no estudo de processamento de imagens, visão computacional e reconhecimento de gestos, permitindo controlar o computador através dos movimentos da mão capturados por uma webcam.

## Sumário

* [Objetivo](#objetivo)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Arquitetura](#arquitetura)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Funcionalidades](#funcionalidades)
* [Como executar](#como-executar)
* [Roadmap](#roadmap)
* [Autor](#autor)

## Objetivo

O projeto foi desenvolvido como trabalho acadêmico para estudar processamento de imagens e reconhecimento de gestos em vídeo.

A aplicação utiliza visão computacional para identificar a mão, rastrear seus movimentos e transformar diferentes gestos em comandos do computador, utilizando a palma como referência para movimentação do cursor.

## Tecnologias utilizadas

* **Python** - Linguagem utilizada na aplicação
* **OpenCV** - Captura e processamento do vídeo da webcam
* **MediaPipe** - Detecção da mão e rastreamento dos 21 landmarks
* **PyAutoGUI** - Controle do mouse e execução de comandos no sistema

## Arquitetura

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe
   ↓
Detecção da mão
   ↓
21 Landmarks
   ↓
Reconhecimento de gestos
   ↓
Controle do computador
```

A posição da palma é utilizada para movimentar o cursor, enquanto os landmarks dos dedos são analisados para identificar diferentes gestos.

## Estrutura do projeto

```text
.
├── camera.py             # Configuração da webcam
├── config.py             # Parâmetros da aplicação
├── controller.py         # Controle do mouse
├── gesture_detector.py   # Reconhecimento dos gestos
├── hand_tracker.py       # Detecção e rastreamento da mão
├── main.py               # Execução principal
├── requirements.txt
└── README.md
```

## Funcionalidades

* Detecção da mão em tempo real
* Rastreamento de 21 landmarks
* Identificação de mão esquerda e direita
* Controle do cursor pela palma da mão
* Suavização do movimento do cursor
* Clique esquerdo através de gesto de pinça
* Clique e arrastar
* Clique direito
* Scroll vertical
* Pausa do controle através de gesto

## Como executar

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Executar

```bash
python main.py
```

Para encerrar a aplicação utilize `Q` ou `ESC`.

## Roadmap

### Concluído

* [x] Captura de vídeo em tempo real
* [x] Detecção e rastreamento da mão
* [x] Identificação dos dedos
* [x] Reconhecimento de gestos
* [x] Controle do cursor pela palma
* [x] Clique, arrastar, clique direito e scroll
* [x] Suavização do movimento

### Próximos passos

* [ ] Melhorar a precisão e estabilidade dos gestos
* [ ] Criar calibração automática
* [ ] Adicionar novos gestos
* [ ] Permitir personalização dos comandos
* [ ] Estudar reconhecimento de gestos utilizando Machine Learning

## Autor

Desenvolvido por **Lucas Wallace Segalla**

* GitHub: https://github.com/lucassegalla
* LinkedIn: https://linkedin.com/in/lucassegalla
