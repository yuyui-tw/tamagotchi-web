# 架構

```text
瀏覽器文字對話 (static/js) ──fetch──> Flask routes ──> pet.py (邏輯)
                                    └──────> storage.py ──> SQLite
```

## 模組職責
| 檔案 | 職責 |
|---|---|
| pet.py | Pet dataclass、apply_action()、decay()、get_status()，維護四項 0–100 數值 |
| storage.py | init_db()、load_pet()、save_pet()，依衰減間隔補算並持久化 |
| routes.py | Flask Blueprint，文字操作 API、delta 計算與狀態回應 |
| static/js/main.js | 解析文字指令、顯示對話與輪詢寵物狀態 |

## 資料表 pet
id INTEGER PK (固定 1), name TEXT, hunger INT, mood INT,
energy INT, cleanliness INT, stage TEXT, updated_at REAL, stats_version INT

## 離線補算
`DECAY_INTERVAL_SECONDS` 預設為 30（測試用；正式版改為 3600），每個間隔執行一步，
最多補算 24 步。`updated_at` 只前進完整步數，因此未滿一個間隔的餘數會保留；
超過上限時，套用 24 步後將 `updated_at` 設為目前時間，捨棄額外離線時間。

每步飽食度減 5、心情減 2、體力減 1、清潔度減 3，並以 `clamp()` 限制在 0–100。
操作的主要數值已滿 100 時回傳原寵物、不保存狀態；有效操作回傳四項數值的
`delta`、`status`、`effective` 與文字 `message`。

## 狀態判斷
依序判斷：任一數值為 0 → `critical`；飽食度低於 30 → `hungry`；
體力低於 30 → `sleepy`；清潔度低於 30 → `dirty`；心情低於 30 → `sad`；
四項皆至少 70 → `happy`；其他情況為 `normal`。

## 擴充（MVP 之後）
動畫、進化階段、商店、音效、多寵物。