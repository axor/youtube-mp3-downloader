import importlib.util
from pathlib import Path

import pytest


def load_module():
    spec = importlib.util.spec_from_file_location(
        "downloader",
        Path(__file__).resolve().parents[1] / "src" / "downloader.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_main_no_args_returns_2():
    downloader = load_module()
    assert downloader.main([]) == 2


def test_main_with_args_calls_download(monkeypatch, tmp_path, capsys):
    downloader = load_module()

    called = {}

    def fake_download_audio_mp3(url, output_dir, filename):
        called['args'] = (url, output_dir, filename)
        p = tmp_path / "audio.mp3"
        p.write_text("dummy")
        return p

    monkeypatch.setattr(downloader, "download_audio_mp3", fake_download_audio_mp3)

    rc = downloader.main(["https://youtu.be/xyz", "-o", str(tmp_path), "-n", "myfile"])
    captured = capsys.readouterr()

    assert rc == 0
    assert "Archivo descargado en" in captured.out
    assert called['args'] == ("https://youtu.be/xyz", str(tmp_path), "myfile")
