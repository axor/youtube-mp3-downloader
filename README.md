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

---

## Uso ✅

Descarga rápida desde la línea de comandos:

```bash
python -m src.downloader "https://www.youtube.com/xyz"
```

Opciones principales:

- **Posicional** `url`: URL del video de YouTube.
- `-o, --output-dir`: Directorio de salida (por defecto: `downloads`).
- `-n, --name`: Nombre del archivo de salida (sin extensión).
- `-q, --quality [medium|high]`: Calidad de salida para MP3. **`medium` = 128 kbps**, **`high` = 192 kbps**. El valor por defecto es **`high`**.
- `--best`: Descarga el mejor audio disponible **y evita re-encoding**, manteniendo la extensión y el códec original cuando sea posible (ej. `.m4a`, `.webm`).

Ejemplos:

```bash
# Default (high, convierte a MP3 a 192 kbps)
python -m src.downloader https://youtu.be/xyz

# Forzar calidad media (128 kbps)
python -m src.downloader -q medium -o downloads -n myfile https://youtu.be/xyz

# Mantener formato original y evitar re-encoding
python -m src.downloader --best -o downloads -n myfile https://youtu.be/xyz
```

### Uso programático 💡

Puedes usar la función desde Python sin ejecutar la CLI (útil en pruebas o scripts):

```python
from src.downloader import download_audio_mp3

# Descarga y convierte a MP3 (default quality = 'high')
path = download_audio_mp3(
    "https://youtu.be/xyz",
    output_dir="downloads",
    filename="myfile",
    quality="high",
)

# Descarga el mejor audio disponible, manteniendo el formato original
path_best = download_audio_mp3(
    "https://youtu.be/xyz",
    output_dir="downloads",
    filename="myfile",
    best=True,
)
```

### Tests 🧪

Las pruebas usan `pytest` y no requieren conexión de red (se usan mocks):

```bash
pip install -r requirements.txt  # incluye pytest
pytest -q
```

---

> **Nota:** `--best` puede producir salidas con extensiones distintas a `.mp3` según el origen; si prefieres siempre MP3, omite `--best` y utiliza `-q` para elegir bitrate.
