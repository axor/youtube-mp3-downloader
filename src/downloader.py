import os
from pathlib import Path
from typing import Optional

from yt_dlp import YoutubeDL


def download_audio_mp3(
    url: str,
    output_dir: str = "downloads",
    filename: Optional[str] = None
) -> Path:
    """
    Descarga el audio de un video de YouTube como archivo MP3.

    :param url: URL del video de YouTube.
    :param output_dir: Directorio donde se guardarán los MP3.
    :param filename: Nombre base opcional del archivo (sin extensión).
    :return: Ruta al archivo MP3 descargado.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Plantilla de nombre
    # %(title)s = título del vídeo si no pasas filename
    if filename:
        outtmpl = os.path.join(output_dir, f"{filename}.%(ext)s")
    else:
        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        # Evita mostrar demasiada basura en consola, opcional:
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # yt-dlp asigna la extensión final tras la conversión
        title = filename if filename else info.get("title", "audio")
        mp3_path = Path(output_dir) / f"{title}.mp3"
        return mp3_path


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Descargar audio MP3 desde un video de YouTube."
    )
    parser.add_argument("url", nargs="?", help="URL del video de YouTube")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help="Directorio de salida (por defecto: downloads)",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Nombre de archivo opcional (sin extensión)",
    )

    args = parser.parse_args(argv)

    if not args.url:
        parser.print_help()
        return 2

    mp3_path = download_audio_mp3(
        url=args.url,
        output_dir=args.output_dir,
        filename=args.name,
    )
    print(f"Archivo descargado en: {mp3_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
