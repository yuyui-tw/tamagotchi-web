# Copilot 專案指示

## 專案
離線電子雞網頁遊戲。Python 3.12 + Flask + SQLite（標準庫 sqlite3）+ 原生 JS。

## 規則
- 遊戲邏輯只放在 `app/pet.py`，必須是純函式或純資料類別，不可 import Flask 或操作資料庫。
- 資料存取只放在 `app/storage.py`；HTTP 路由只放在 `app/routes.py`。
- 前端用原生 JS（ES modules），不要引入 npm、打包工具或前端框架。
- 不使用任何需要網路的服務、CDN 或外部 API；資源皆放在 `app/static/`。
- 所有數值限制在 0–100，使用 `clamp()`。
- 時間補算以 `time.time()` 的秒數差計算，上限 24 小時。
- 新增邏輯必須附 pytest 測試於 `tests/`。
- 型別標註必須完整；格式化用 ruff。
- 程式碼註解與 commit 訊息使用繁體中文；變數與函式名用英文 snake_case。
- 不要提交 `.venv/`、`data/`、`*.db`、`__pycache__/`。

## 常用指令
- 安裝：`pip install -r requirements-dev.txt`
- 執行：`python run.py`
- 測試：`pytest`
- 檢查：`ruff check . && ruff format --check .`

## API 約定
- GET  /api/pet → 回傳目前寵物狀態（已補算）
- POST /api/pet/action，body: {"action": "feed|play|sleep|clean"}
- 回應一律 JSON：{"name","hunger","mood","energy","cleanliness","stage","updated_at"}