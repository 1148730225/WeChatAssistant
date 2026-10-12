# Windows 构建说明

推荐使用 Python 3.10 x64。先安装 `requirements.txt` 和 PyInstaller，然后运行：

```powershell
$env:WECHAT_ARCHIVER_PYTHON = "C:\path\to\python.exe" # 可选，默认使用 python
powershell -ExecutionPolicy Bypass -File .\packaging\build_windows.ps1
```

输出目录为 `dist\WeChatArchiveAssistant`。这是适合 Qt WebEngine 的 onedir
发行结构，必须完整分发该目录，不能只复制其中的 EXE。

SenseVoice 模型不会提交到 GitHub。构建带离线语音识别的发行版前，将
`model.int8.onnx` 和 `tokens.txt` 放入 `models\sensevoice`，构建脚本会将其打包。

如需生成安装包，请安装 Inno Setup 7，然后在项目根目录执行：

```powershell
& "C:\Program Files (x86)\Inno Setup 7\ISCC.exe" .\packaging\installer.iss
```

程序数据默认写入 `D:\WeChatArchive`；没有 D 盘时写入
`%LOCALAPPDATA%\WeChatArchive`，不会写入安装目录。
