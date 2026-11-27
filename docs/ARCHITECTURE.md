# 架構

```text
瀏覽器 (static/js) ──fetch──> Flask routes ──> pet.py (邏輯)
                                    └──────> storage.py ──> SQLite
```

## 模組職責
| 檔案 | 職責 |
|---|---|
| pet.py | Pet dataclass、apply_action()、decay(elapsed_seconds) |
| storage.py | init_db()、load_pet()、save_pet() |
| routes.py | Flask Blueprint，兩支 API 與首頁 |
| static/js/main.js | 呼叫 API、更新畫面、按鈕事件 |

## 資料表 pet
id INTEGER PK (固定 1), name TEXT, hunger INT, mood INT,
energy INT, cleanliness INT, stage TEXT, updated_at REAL

## 離線補算
讀取時：elapsed = min(now - updated_at, 86400) → decay() → 存回。

## 擴充（MVP 之後）
動畫、進化階段、商店、音效、多寵物。