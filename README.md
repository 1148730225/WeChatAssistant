# 微信 4.x 聊天记录归档助手

面向 Windows 微信 4.x 的本地聊天记录归档工具。程序可以自动检测账号、提取当前
账号的数据库与媒体密钥、解密数据库，并将指定会话导出为微信风格的 HTML 或 PDF。

## 功能

- 自动检测 Windows 微信 4.x 安装目录、数据目录和账号
- 按账号隔离保存密钥、解密数据库和导出结果
- 会话搜索、群聊/私聊筛选、聊天预览和批量导出
- 恢复本地图片、表情、GIF、语音、视频与文件
- 可选联网补全仍有效的微信 CDN 图片和表情
- HTML 离线归档与 WeasyPrint PDF 导出
- 可选 SenseVoice 离线语音转文字

所有聊天数据都在本机处理。请勿提交 `D:\WeChatArchive`、数据库、密钥文件、日志或
个人导出内容。

## 源码运行

建议使用 Python 3.10 x64：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python wechat_archiver.py
```

首次准备账号时，需要启动并登录电脑版微信。密钥与数据库缓存完成后，可以离线加载
已有数据。程序优先将数据写入 `D:\WeChatArchive`；没有 D 盘时使用
`%LOCALAPPDATA%\WeChatArchive`。

## 离线语音识别

将 SenseVoiceSmall 的 `model.int8.onnx` 和 `tokens.txt` 放入
`models\sensevoice`。模型文件较大，不包含在源码仓库中。

## Windows 打包

参见 [BUILD.md](BUILD.md)。正式发行采用 PyInstaller onedir 结构，Qt WebEngine
程序不能只复制主 EXE，必须保留完整输出目录或使用安装包。

## 使用范围

本工具用于备份和整理用户本人有权访问的本地微信数据。微信更新可能改变数据库结构或
密钥保存方式，发布前应在目标微信版本上重新验证。
