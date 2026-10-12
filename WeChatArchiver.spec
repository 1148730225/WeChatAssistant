# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller onedir build for the Windows WeChat 4.x archive assistant."""
from __future__ import annotations

import glob
import os
import sys

from PyInstaller.utils.hooks import collect_all


project = os.path.abspath(SPECPATH)
conda_bin = os.path.join(sys.prefix, "Library", "bin")
if os.path.isdir(conda_bin):
    os.environ["PATH"] = conda_bin + os.pathsep + os.environ.get("PATH", "")
datas = [
    (os.path.join(project, "wx4", "assets"), "wx4/assets"),
    (os.path.join(project, "app", "data", "icon.png"), "app/data"),
]
binaries = []
hiddenimports = ["zstandard", "pilk"]

for package in ("weasyprint", "sherpa_onnx"):
    package_datas, package_bins, package_hidden = collect_all(package)
    datas += package_datas
    binaries += package_bins
    hiddenimports += package_hidden

sensevoice = os.path.join(project, "models", "sensevoice")
if os.path.isdir(sensevoice):
    datas.append((sensevoice, "models/sensevoice"))

# WeasyPrint on Conda/Windows needs the Pango, Cairo and transitive DLL set.
if os.path.isdir(conda_bin):
    binaries += [(path, "Library/bin") for path in glob.glob(os.path.join(conda_bin, "*.dll"))]

a = Analysis(
    [os.path.join(project, "wechat_archiver.py")],
    pathex=[project],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["faster_whisper", "ctranslate2", "torch", "tensorflow"],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="WeChatArchiveAssistant",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project, "app", "data", "wechat-archive.ico"),
    version=os.path.join(project, "packaging", "version_info.txt"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="WeChatArchiveAssistant",
)
