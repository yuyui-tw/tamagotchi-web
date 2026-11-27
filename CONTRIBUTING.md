# 協作規範

## 首次建立 GitHub 備份
1. 在 GitHub 建立名為 `tamagotchi-web` 的公開 repository，不要勾選自動建立 README、`.gitignore` 或 License。
2. 在專案資料夾初始化 Git，建立第一次提交並推送：

   ```powershell
   git init
   git add .
   git commit -m "chore: 建立電子雞專案骨架"
   git branch -M main
   git remote add origin https://github.com/<GitHub帳號>/tamagotchi-web.git
   git push -u origin main
   ```

   將 `<GitHub帳號>` 替換為實際 GitHub 帳號。Git for Windows 與 GitHub 登入可使用 Git Credential Manager；不要將存取權杖寫入檔案或提交到 repository。

## 分支與共編
- `main`：穩定版；完成首次推送後，建議在 GitHub 設定 Branch protection，禁止直接推送並要求 CI 通過。
- 功能分支：`feature/<簡述>`；修正：`fix/<簡述>`。
- 共編者可 fork 公開 repository、建立分支並送出 Pull Request；若要直接在本 repository 建分支，請由擁有者到 Settings → Collaborators 邀請對方。
- Pull Request 至少應說明變更內容與測試結果。若有其他共編者，請安排至少一位審核；單人開發時不要設定無人可滿足的必須審核規則。

## 日常流程
1. 從最新的 `main` 建立功能或修正分支。
2. 小步提交，訊息格式：`feat: 新增餵食功能`（feat/fix/docs/test/refactor/chore）。
3. 本機通過 `pytest` 與 `ruff` 後推送分支。
4. 開 Pull Request，等待 GitHub Actions 檢查通過與適當審核，再合併。

## GitHub 設定建議
- Branch protection 對 `main` 要求 Pull Request 與 CI 通過；審核人數依共編情況設定。
- 使用 Issues 追蹤工作，必要時再用 Projects 看板分工。