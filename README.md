# 建兴智能-无线传输-(QRCode 后端)
## 前言
为了防止黑客或其他人为导致重要数据被篡改或窃取，公司致力研究一款产品能与机房物理隔绝，还能数据交互。
于是这么一款读取二维码数据无线传输的产品就出来了。
该Program是后端，主要接收外部转接请求，生成二维码发给前端，接收识别端的识别数据，拼接request 回复。

![AppVeyor](https://img.shields.io/static/v1?label=MoJeffrey&message=OCR-QR-Code-Backend&color=<COLOR>)

## 软件要求
[![Python - < 9.8](https://img.shields.io/badge/python-v9.8-2ea44f?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## 文件結構
```
.
│   .gitignore
│   requirements.txt
│   db.sqlite3
│   manage.py
│
├─── generators --生成二维码和展示二维码数据传输
├─── javaTools --jar 包
├─── logs --日志目录
├─── ocr_django --Django 项目配置
├─── recognizer --接收识别端回复
├─── static --静态文档（QRcode 生成的图片）
├─── Tools --工具类
├─── transponder --转发API请求
│
└─── UnitTest --測試代碼
```