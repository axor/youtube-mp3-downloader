import os
from pathlib import Path
from typing import Optional

from yt_dlp import YoutubeDL


def download_audio_mp3(
    url: str,
    output_dir: str = "downloads",
    filename: Optional[str] = None,
    quality: str = "high",
    best: bool = False,
) -> Path:
    """
    Descarga el audio de un video de YouTube.

    :param url: URL del video de YouTube.
    :param output_dir: Directorio donde se guardarán los archivos.
    :param filename: Nombre base opcional del archivo (sin extensión).
    :param quality: Calidad deseada, 'medium' (128kbps) o 'high' (192kbps). Ignorado si best=True.
    :param best: Si es True, descarga el mejor audio disponible y evita re-encoding (mantiene formato original cuando sea posible).
    :return: Ruta al archivo descargado (extensión dependerá del modo).
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Plantilla de nombre
    # %(title)s = título del vídeo si no pasas filename
    if filename:
        outtmpl = os.path.join(output_dir, f"{filename}.%(ext)s")
    else:
        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    # Map requested quality to ffmpeg preferredquality (kbps)
    quality_map = {"medium": "128", "high": "192"}

    if best:
        # Don't add audio extraction postprocessor: keep the original audio file
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "quiet": False,
        }
    else:
        if quality not in quality_map:
            raise ValueError("quality must be 'medium' or 'high'")
        ydl_opts = {
            # Keep best audio from source
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality_map[quality],
                }
            ],
            # Evita mostrar demasiada basura en consola, opcional:
            "quiet": False,
        }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = filename if filename else info.get("title", "audio")

        if best:
            # Keep the original extension reported by yt-dlp (e.g., m4a, webm)
            ext = info.get("ext", "m4a")
            out_path = Path(output_dir) / f"{title}.{ext}"
        else:
            out_path = Path(output_dir) / f"{title}.mp3"

        return out_path


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
    parser.add_argument(
        "-q",
        "--quality",
        choices=["medium", "high"],
        default="high",
        help="Calidad deseada: 'medium' (128kbps) o 'high' (192kbps).",
    )
    parser.add_argument(
        "--best",
        action="store_true",
        help="Descargar el mejor audio disponible y evitar re-encoding (mantener formato original cuando sea posible).",
    )

    args = parser.parse_args(argv)

    if not args.url:
        parser.print_help()
        return 2

    quality = args.quality
    best = args.best

    mp3_path = download_audio_mp3(
        url=args.url,
        output_dir=args.output_dir,
        filename=args.name,
        quality=quality,
        best=best,
    )
    print(f"Archivo descargado en: {mp3_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
