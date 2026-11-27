# 電子雞網頁遊戲 (tamagotchi-web)

以瀏覽器遊玩的離線電子雞。後端 Python (Flask)，本機 SQLite 存檔，前端原生 HTML/CSS/JS。

## 需求
- Python 3.12+
- Git
- VS Code（建議安裝 .vscode/extensions.json 內的擴充套件）

## 快速開始
```bash
git clone https://github.com/<GitHub帳號>/tamagotchi-web.git
cd tamagotchi-web
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
python run.py
```
開啟 http://127.0.0.1:5000

## 測試
```bash
pytest
```

## 功能範圍 (MVP)
- 一隻寵物，飽食度、心情、體力與清潔度皆為 0–100
- 操作：餵食、玩耍、睡覺、清潔；主要數值到 100 時操作仍可呼叫，但不產生效果
- 預設衰減間隔 `DECAY_INTERVAL_SECONDS=30`，每個間隔依序減少飽食度 5、心情 2、體力 1、清潔度 3
- 離線補算最多 24 個衰減間隔；正式版可將間隔設為 3600 秒，即最多補算 24 小時
- API 操作回應包含 `status`、各數值 `delta`、`effective` 與文字 `message`
- 存檔於本機 SQLite（data/pet.db，不進版控）
- `DECAY_INTERVAL_SECONDS` 可由 Flask app 設定覆寫，測試可使用 30 秒
- 完全離線，不呼叫任何外部 API

## 文件
- 架構：docs/ARCHITECTURE.md
- 協作規範：CONTRIBUTING.md

## GitHub 協作
- 首次備份與 GitHub 倉庫設定請參考 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 修改請透過 Pull Request 合併；GitHub Actions 會執行測試與 Ruff 檢查。
- 本倉庫設定為公開，請勿提交密碼、金鑰或個人資料。