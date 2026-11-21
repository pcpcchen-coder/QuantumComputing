# 量子電腦學程 v2（動畫展示版）逐課製作手冊

給接手製作 Q011 起課次的 Claude 雲端對話。Q001–Q010 已用這套流程做完，可直接當範例。
全程用**繁體中文**和使用者互動、寫報告。

## 0. 不可違反的規則

- 金鑰、權杖絕不出現在對話、檔案或指令裡。Azure 語音金鑰（`eastasia.tts.speech.microsoft.com`）與 Google Drive 權杖（`www.googleapis.com`）都由環境的網路代理注入；收到 401／403 時，用 `request_credential` 重新要，不要請使用者貼上。
- 不 commit 到 XiNewVideoGPT（`pcpcchen-coder/xinewvideogpt`）；它只當製作工具，`specials/` 下的檔案留在容器裡。
- YouTube 由使用者自己上傳；不登入、不上傳 YouTube。
- MP4、錄影原檔 webm、純旁白 MP3 不進 Git，只把檔名、大小和 SHA-256 記在 `delivery.json`。
- 背景作業一次最多 2 小時。用 `tools/chain.sh`，它有 110 分鐘預算；時間到就再跑一輪，從快取接續，不必重新問使用者。
- 一次只錄一課，錄影期間不要跑交付（重新壓縮預覽版會搶 CPU，讓動畫錄影變慢、時間點錯開）。
- 不可把機器檢查寫成真人聽審；`manual-review.md` 要寫清楚誰看、怎麼看、限制在哪。
- 每課做完、驗收、記錄後就 commit 並 push，再做下一課。

## 1. 容器準備（每個新對話一次）

```bash
# 1) 加入製作工具 repo（用 add_repo 工具：owner=pcpcchen-coder repo=xinewvideogpt），再 clone 到 /home/user/xinewvideogpt
# 2) 安裝可攜環境與語音辨識（約 5–10 分鐘）
/home/user/QuantumComputing/academy/authoring/v2/tools/setup_env.sh
```

環境變數（有預設值，通常不用設）：`XINEW_ACADEMY=/home/user/xinewvideogpt/academy`、`QWORK=/home/user/qwork`（ASR 模型、日誌、完成標記）。
`/home/user/xinewvideogpt/academy` 下文中記為 `$XINEW`。

## 2. 每課流程

以 Q011 為例；slug 自己取，用英文小寫加連字號，例如 `q011-xxx`。

### 2.1 內容稿：v1 的 12 頁加 36 句旁白，再加教材

依序讀以下檔案：
- `academy/lessons/Q011/brief.md`、`lesson.json`
- 範例 `academy/authoring/q004/` … `q010/`
- `academy/authoring/qbuild.py`
- `academy/docs/PRODUCTION_GUIDE.md`

寫出 `academy/authoring/q011/` 下這些檔案：
- `prepare_content.py`：模仿 q004–q010。檔頭要有一行 `LESSON, SLUG, CHECKED = 'Q011', 'q011-xxx', '日期'`，`build_v2.py` 靠這行自動登記課次，不要改 `build_v2.py` 的 LESSONS。
- `classroom.py`：4 頁列印包與課堂教材。
- `fact-check.md`、`source-notes.md`、`plan.md`、`delivery-summary.md`。

旁白規則：
- 12 頁，每頁 3 句，共 36 句，句子不可重複。
- 第一句的格式是「歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第Ｎ堂，…」，而且要包含「依課綱製作的課前教學版」和「並非實際上課錄音」。
- 最後一句預告下一課，並以「我是陳犀牛，保持好奇，我們下次見！」結尾。
- 念出來的字避免英文字母和縮寫，例如說「哈達瑪閘」「零態」。
- 避免破音字「長」。
- 量子閘一律用：翻轉閘、哈達瑪閘、相位翻轉閘、受控反閘。

簡報上的可見文字要和 L001 模板的欄位數、換行數完全一致。照範例逐欄複製結構。時間表標籤固定為 `'00–25','25–65','65–75','75–105','105–115','115–120','休息十分鐘'`。

事實要有來源：本 repo 的 `slides/`、動畫原始碼、維基百科等。不確定的不要寫。

驗證（在 `$XINEW` 執行）：
```bash
EP=specials/q011-xxx
./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q011/prepare_content.py
./portable-runtime.sh python pipeline/academy.py run validate --episode $EP
./portable-runtime.sh python pipeline/academy.py run deck --episode $EP
./portable-runtime.sh python pipeline/qa/review_sheets.py --episode $EP --out /home/user/qwork/review-q011   # 用 Read 看每張 PNG，修溢字、截斷、怪換行
XINEW_CHROME=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/*/chrome-headless-shell | head -1) ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q011/classroom.py   # 列印包要 4 頁
```

### 2.2 動畫展示段：`academy/authoring/v2/demos_extra/q011.py`

- 格式照 `demos_extra/q004.py`。要定義 `LESSON = 'Q011'` 和 `DEMOS`，可以是清單，也可以是 `{'Q011': [...]}`。
- 每課通常 3 段。每段包含：
  - `key`
  - `after`：插在第幾頁之後，選內容頁，不選封面、時間表、結尾
  - `page`、`hash`、`scene`
  - `title`：寫成「動畫展示：…」
  - `sub`：寫成「三維動畫：…」
  - `sentences`：3–4 句新旁白，不和那 36 句重複
  - `actions`
  - `points`：3 組
  - `shot`
- 可用頁面見 `demos.py` 的 `PAGES`：
  - `op`：operation.html，場景用 hash 選，原始碼在 `animations/js/operation/`
  - `tr`：transmon-3d
  - `bc`：basic-circuits，用 `('sel', css)` 或 `('js', code)`
  - `jj`：index.html，JJ 與微波讀取
  - `lc`：lc-vs-jj
  - `pe`：peripherals
  - `at`：atoms
  - `pw`：power1000
- 按鈕文字、滑桿標籤、hash 一定要讀動畫原始碼確認。控制項不存在，錄影就會失敗。
- 每句約「字數 ÷ 4.5」秒。動作要落在它那一句裡，而且要在旁白說到時發生。
- **旁白只能描述畫面真的會出現的東西**（Q006 曾把只爬升一次的曲線說成「亮暗亮暗」，查核後只好重錄）。
- 試錄，不合成聲音：
  ```bash
  cd $XINEW && QV2_DRY=1 .venv/bin/python …/v2/build_v2.py Q011 audio && QV2_DRY=1 .venv/bin/python …/v2/build_v2.py Q011 record
  ```
  看 `specials/q011-xxx-v2/` 裡的截圖 PNG，確認場景和效果都對。確認後刪掉 `specials/q011-xxx-v2`。

### 2.3 製作：TTS、錄影、組裝、技術檢查、語音辨識

```bash
/home/user/QuantumComputing/academy/authoring/v2/tools/chain.sh Q011 Q012 Q013 > /home/user/qwork/chain.log 2>&1   # 用 Bash 的 run_in_background
```

- `produce.sh` 依序做：Azure 補 TTS 快取 → v1 tts（產生 timing）→ v2 audio、record、deck、assemble → `qc_v2.py`（13 項）→ ASR。
- 完成標記是 `/home/user/qwork/produced-Q011`；日誌是 `produce-Q011.log` 和 `asr-Q011.log`。
- 要重做某課，先刪掉它的完成標記。
- 背景作業結束會通知你，不要用 sleep 輪詢。

### 2.4 驗收與查核

1. `specials/q011-xxx-v2/qc/verify-v2.json` 必須 13/13 通過。
2. 看抽格總表 `specials/q011-xxx-v2/qc/video-frames/cues_*.jpg`。動畫段那幾張一定要親自看。
3. 看 ASR 結果 `qc/asr-review.json`：
   - 字面相似度低於 0.8 的條目，逐條說明原因，例如同音字或數字寫法。
   - 拼音相似度低於 0.9 的條目，標成「需要真人留意」。
4. 寫動畫段事實查核 `academy/authoring/v2/fact_check_v2_q011_q040.md`。檔名用你負責的範圍，格式照 `fact_check_v2_q004_q010.md`，每課一節 `## Q011`。
   - 逐句對照動畫原始碼、物理計算、畫格。
   - 查到不符就**改旁白、重做該課**，不要帶著「不符」交付。
   - 建議交給子代理做，它看不到你的結論，比較客觀。
5. 產生人工檢視紀錄，再讀一遍補充：
   ```bash
   cd $XINEW && .venv/bin/python …/v2/tools/write_review.py Q011 '<親自看過的總表與段名>' '<字面低分原因>'
   ```

### 2.5 交付、提交、上傳

```bash
cd $XINEW && .venv/bin/python /home/user/QuantumComputing/academy/authoring/v2/deliver_v2.py Q011 <短名> <日期> /home/user/qwork/Q011交付
cd /home/user/QuantumComputing && python3 academy/curriculum/build_curriculum.py
cp $XINEW/specials/q011-xxx-v2/qc/asr-review.json academy/episodes/q011-xxx-v2/qc/   # 若 deliver 沒帶到
git add -A academy && git commit -m "Q011 v2 動畫展示版：製作、驗收、交付紀錄" && git push -u origin <你的分支>
```

`deliver_v2.py` 會：
- 檢查 13/13 通過，以及 `manual-review.md` 存在。
- 產生章節、說明、教材 zip（v1 教材加上動畫導覽）、分段 ZIP、30 MB 以下的預覽版。
- 把 episode 複製回 `academy/episodes/q011-xxx-v2`，寫入 `delivery.json`，並更新狀態表。

Google Drive 上傳：
- 上傳到你負責範圍的資料夾，資料夾 id 由派工訊息給。
- 每課上傳 3 個檔案，檔名格式和 Q001–Q003 相同：
  - `Q011 <短名>：<完整課名>（動畫展示版）.mp4`，用 `specials/<slug>-v2/output/<slug>-v2-zh-TW.mp4`，字幕已燒入
  - `Q011 <短名>（動畫展示版）簡報.pptx`
  - `Q011 <短名> 教材.zip`，用 `specials/<slug>-v2/output/classroom.zip`

```bash
T=/home/user/QuantumComputing/academy/authoring/v2/tools
$T/drive_upload.sh put <資料夾id> <本機檔> '<雲端檔名>'   # 會比對 md5，印出 id 和連結
```

- 回 401 表示權杖過期：用 `request_credential`（host `www.googleapis.com`、bearer）請使用者在表單更新，然後重試。
- 上傳後把 Drive 檔案 id 和連結記在 `academy/episodes/<slug>-v2/delivery.json` 的 `drive` 欄位，再 commit。

## 3. Git

- 只在派工訊息指定的分支工作。每課 commit 一次，push 時用 `git push -u origin <分支>`。
- 第一次 push 後，對 `main` 開 PR（ready for review），並訂閱 PR 動態。
- 只改你負責範圍的檔案，加上 `academy/curriculum/` 自動產生的檔案與 `production-status.json`。共用程式（`build_v2.py`、`demos.py`、`deliver_v2.py` 等）若一定要改，在 PR 描述說明原因。
- 不 force push，不改別人的分支。

## 4. 中斷與接續

- 額度或工具中斷時，寫 `academy/authoring/qxxx/HANDOFF.md`，記錄做到哪、下一步是什麼，然後 commit。
- 對話若被重啟，先看 `/home/user/qwork/` 的完成標記和日誌，再看 git log，從斷點繼續。容器若被回收，`qwork` 會消失：重跑 `setup_env.sh`，再從最後一個已 commit 的課接續（`specials/` 需要重建：重跑 `prepare_content.py`，TTS 快取也要重新合成）。

## 5. 已知問題與經驗

- Edge TTS 免費端點會被限流（NoAudioReceived），所以一律用 Azure（`fill_tts_azure.py`）。快取鍵相同，聲音和格式也相同。
- `record_demo.js` 的計時器可能早醒，已改成最後一定補拍截圖。
- `~` 在這個環境展開成 `/root`，路徑一律寫絕對路徑 `/home/user/...`。
- 用 `pgrep -f` 等其他工作時，會比對到自己的命令列；改用完成標記檔。
- 機器負載高時動畫會變慢。所以一次只錄一課，也不要同時跑兩個 chain。
