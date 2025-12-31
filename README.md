# YouTube MP3 Downloader (Python)

Script en Python para descargar el audio de videos de YouTube en formato MP3 utilizando [yt-dlp](https://github.com/yt-dlp/yt-dlp).

> ⚠️ Úsalo únicamente con contenido para el que tengas derechos o permiso. Respeta siempre los Términos de servicio de YouTube y las leyes de tu país.

## Requisitos

- Python 3.9 o superior
- `ffmpeg` instalado en tu sistema (requerido por yt-dlp para convertir a MP3)
- Paquetes Python listados en `requirements.txt`

## Instalación

```bash
git clone https://github.com/TU_USUARIO/youtube-mp3-downloader.git
cd youtube-mp3-downloader

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt
