# -*- coding: utf-8 -*-
"""Standalone Windows launcher for the WeChat 4.x archive assistant."""
from __future__ import annotations

import ctypes
import json
import multiprocessing
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication


def _resource_path(relative: str) -> str:
    root = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, relative)


def main() -> int:
    multiprocessing.freeze_support()
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "WeChatArchive.Assistant")
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

    if "--self-test" in sys.argv:
        from Cryptodome.Cipher import AES  # noqa: F401
        from wx4 import pdf
        from wx4.gui import WEBENGINE_AVAILABLE

        root = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(root, "models", "sensevoice")
        pdf_ok, pdf_detail = pdf.weasyprint_available()
        try:
            import sherpa_onnx  # noqa: F401
            sherpa_ok = True
        except Exception:
            sherpa_ok = False
        report = {
            "webengine": bool(WEBENGINE_AVAILABLE),
            "pdf": bool(pdf_ok),
            "pdf_detail": pdf_detail,
            "sensevoice_model": os.path.isfile(os.path.join(model_dir, "model.int8.onnx")),
            "sensevoice_tokens": os.path.isfile(os.path.join(model_dir, "tokens.txt")),
            "sherpa_onnx": sherpa_ok,
        }
        index = sys.argv.index("--self-test")
        if len(sys.argv) > index + 1:
            with open(sys.argv[index + 1], "w", encoding="utf-8") as stream:
                json.dump(report, stream, ensure_ascii=False, indent=2)
        return 0 if all(report[key] for key in (
            "webengine", "pdf", "sensevoice_model", "sensevoice_tokens", "sherpa_onnx")) else 2

    app = QApplication(sys.argv)
    app.setApplicationName("微信聊天记录归档助手")
    app.setOrganizationName("WeChatArchive")
    app.setFont(QFont("Microsoft YaHei UI", 11))
    icon_path = _resource_path(os.path.join("app", "data", "icon.png"))
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Import WebEngine-dependent UI only after AA_ShareOpenGLContexts is set.
    from wx4.gui import Wx4ExportWindow

    window = Wx4ExportWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
