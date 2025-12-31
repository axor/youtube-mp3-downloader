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

    def fake_download_audio_mp3(url, output_dir, filename, quality="medium", best=False):
        called['args'] = (url, output_dir, filename, quality, best)
        p = tmp_path / "audio.mp3"
        p.write_text("dummy")
        return p

    monkeypatch.setattr(downloader, "download_audio_mp3", fake_download_audio_mp3)

    rc = downloader.main(["https://youtu.be/xyz", "-o", str(tmp_path), "-n", "myfile", "-q", "high"])
    captured = capsys.readouterr()

    assert rc == 0
    assert "Archivo descargado en" in captured.out
    assert called['args'] == ("https://youtu.be/xyz", str(tmp_path), "myfile", "high", False)


def test_main_with_best_flag(monkeypatch, tmp_path, capsys):
    downloader = load_module()

    called = {}

    def fake_download_audio_mp3(url, output_dir, filename, quality="high", best=False):
        called['args'] = (url, output_dir, filename, quality, best)
        p = tmp_path / "audio.m4a"
        p.write_text('dummy')
        return p

    monkeypatch.setattr(downloader, "download_audio_mp3", fake_download_audio_mp3)

    rc = downloader.main(["https://youtu.be/xyz", "-o", str(tmp_path), "-n", "myfile", "--best"])
    captured = capsys.readouterr()

    assert rc == 0
    assert called['args'][4] is True


def test_download_audio_sets_quality_in_ydl_opts(monkeypatch, tmp_path):
    downloader = load_module()

    instances = []

    class FakeYDL:
        def __init__(self, opts):
            self.opts = opts
            instances.append(self)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download):
            return {"title": "audio"}

    monkeypatch.setattr(downloader, "YoutubeDL", FakeYDL)

    p = downloader.download_audio_mp3("https://youtu.be/xyz", output_dir=str(tmp_path), filename="f", quality="high")

    assert instances, "YoutubeDL was not instantiated"
    opts = instances[0].opts
    assert opts["postprocessors"][0]["preferredquality"] == "192"

    # medium quality
    instances.clear()
    p2 = downloader.download_audio_mp3("https://youtu.be/xyz", output_dir=str(tmp_path), filename="f2", quality="medium")
    opts2 = instances[0].opts
    assert opts2["postprocessors"][0]["preferredquality"] == "128"


def test_download_audio_best_avoids_postprocessor(monkeypatch, tmp_path):
    downloader = load_module()

    instances = []

    class FakeYDL:
        def __init__(self, opts):
            self.opts = opts
            instances.append(self)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download):
            return {"title": "audio", "ext": "m4a"}

    monkeypatch.setattr(downloader, "YoutubeDL", FakeYDL)

    p = downloader.download_audio_mp3("https://youtu.be/xyz", output_dir=str(tmp_path), filename="f", best=True)

    assert instances, "YoutubeDL was not instantiated"
    opts = instances[0].opts
    assert "postprocessors" not in opts
    assert p.suffix == ".m4a"

def test_main_defaults_to_high(monkeypatch, tmp_path, capsys):
    downloader = load_module()

    called = {}

    def fake_download_audio_mp3(url, output_dir, filename, quality='medium'):
        called['args'] = (url, output_dir, filename, quality)
        p = tmp_path / "audio.mp3"
        p.write_text('dummy')
        return p

    monkeypatch.setattr(downloader, "download_audio_mp3", fake_download_audio_mp3)

    rc = downloader.main(["https://youtu.be/xyz", "-o", str(tmp_path), "-n", "myfile"])
    captured = capsys.readouterr()

    assert rc == 0
    assert called['args'][3] == 'high'
