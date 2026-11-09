# 量子電腦學程｜製作指南

每集用父子科技學院的可攜製片流程（`pcpcchen-coder/XiNewVideoGPT` 的 `academy/`）產生影片、簡報與教材，
內容稿與成品來源則保存在本 repo。Q001 是第一集，以下流程與注意事項都是做 Q001 時實際走過的。

## 1. 準備環境（每台機器一次）

需要 Linux 或 macOS、Python 3.11+、ffmpeg、LibreOffice、poppler、Chromium。

```bash
git clone https://github.com/pcpcchen-coder/XiNewVideoGPT.git ~/xinewvideogpt
```

```bash
cd ~/xinewvideogpt/academy && ./setup-portable.sh
```

`setup-portable.sh` 會建立 `.venv`、安裝套件（含 `edge-tts==7.3.1`）、還原陳犀牛片頭並跑 preflight，最後印出 `"ready": true` 才算好。

```bash
export XINEW_ACADEMY=~/xinewvideogpt/academy
export XINEW_CHROME=/path/to/chrome-headless-shell   # 列印包用；完整版 Chrome 在某些容器會卡住
```

## 2. 每集的檔案

量子電腦學程不在父子學院的 192 堂課表裡，所以走它的「特別篇」路線（`authoring/special_builder.py`），
製作中的集數資料夾在 `$XINEW_ACADEMY/specials/qxxx-<slug>/`。

| 本 repo 的檔案 | 內容 |
|---|---|
| `academy/authoring/qxxx/prepare_content.py` | 12 幕 × 3 句旁白、12 頁版型文字、分鏡、來源；呼叫 `special_builder.build()` |
| `academy/authoring/qxxx/classroom.py` | 課堂教材與列印包 |
| `academy/authoring/qxxx/fact-check.md`、`source-notes.md`、`plan.md`、`delivery-summary.md` | 查核紀錄、逐字引文、120 分鐘安排、公開說明 |
| `academy/episodes/qxxx-<slug>/` | 製作完成後從 XiNewVideoGPT 複製回來的來源、教材、QC、音訊與 `delivery.json` |

內容規則（沿用父子學院）：

- 12 頁沿用 L001 版型，每頁文字格數與換行數必須和版型一致（`special_builder` 會檢查）。
- 第一句要揭露「依課綱製作的課前教學版，並非實際上課錄音」；最後一句以「我是陳犀牛，保持好奇，我們下次見！」結尾。
- 36 句不能和父子學院任何一集重複。
- 旁白避免英文縮寫與人名直接夾在中文裡（Edge TTS 會念得很短或念錯）：Shor 寫「秀爾」、Grover 寫「格羅弗」、Bloch 寫「布洛赫」。
- 投影片與字幕同一個詞要用同一個寫法。
- 每個事實都要有來源；能讀原文就讀原文，子代理回報的引文要在 `fact-check.md` 註明。

## 3. 逐階段命令

以下都在 `$XINEW_ACADEMY` 執行，`EP=specials/qxxx-<slug>`。

```bash
./portable-runtime.sh python ~/QuantumComputing/academy/authoring/qxxx/prepare_content.py
```

```bash
./portable-runtime.sh python pipeline/academy.py run validate --episode $EP
```

```bash
./portable-runtime.sh python pipeline/academy.py run deck --episode $EP
```

```bash
./portable-runtime.sh python pipeline/qa/review_sheets.py --episode $EP --out /tmp/review
```

逐頁看 `/tmp/review/*-slides-*.jpg`，有溢字就精簡文字後重跑 deck。

```bash
./portable-runtime.sh python ~/QuantumComputing/academy/authoring/qxxx/classroom.py
```

```bash
./portable-runtime.sh python pipeline/academy.py run tts --episode $EP
```

```bash
./portable-runtime.sh python pipeline/academy.py run media-check --episode $EP
```

```bash
./portable-runtime.sh python pipeline/academy.py run assemble --episode $EP
```

```bash
./portable-runtime.sh python pipeline/delivery.py --episode $EP
```

寫 `$EP/qc/manual-review.md`（檢視方法、發現、限制）後：

```bash
./portable-runtime.sh python pipeline/academy.py run verify --episode $EP
```

```bash
./portable-runtime.sh python pipeline/academy.py package --episode $EP --output delivery/Qxxx-v1
```

## 4. 收尾

1. 把集數資料夾複製回本 repo，再刪掉大型 MP4 與純旁白 MP3（`.gitignore` 也擋住了）：

   ```bash
   cp -a $XINEW_ACADEMY/specials/qxxx-<slug> ~/QuantumComputing/academy/episodes/ && cd ~/QuantumComputing/academy/episodes/qxxx-<slug> && rm -f output/*.mp4 output/narration-only.mp3 && rm -rf qc/clips qc/frames qc/subtitle-precheck
   ```

2. 在 `academy/episodes/qxxx-<slug>/delivery.json` 記錄 MP4 與交付 ZIP 的檔名、大小、SHA-256 與取得方式。
3. 改 `academy/curriculum/production-status.json` 該課為 `verified`、`publication: awaiting_user_upload`，再跑 `python3 academy/curriculum/build_curriculum.py`。
4. commit 本 repo；XiNewVideoGPT 那邊的 `specials/qxxx-*` 只是工作區，不 commit。

## 5. 做 Q001 時遇到的事

- **Edge TTS 間歇性不給音訊**：2026-11-07 下午連續回 `NoAudioReceived`，連父子學院念過的句子也失敗，短句時好時壞。
  正式管線每句最多試 7 次就整輪停下，三輪只過了 5 句。改用 `academy/authoring/fill_tts_cache.py`：它呼叫同一個合成函式（同樣的完整性檢查），
  失敗就等 90 秒再試，逐句存進 `.build-tts-cache/`；36 句花了約一個半小時。之後正式管線一次跑完、全部從快取取回。不要換聲線。
- **交付**：完整交付包約 152 MB，用 `pipeline/split_delivery.py` 切成 28 MiB 分段當對話附件；另用
  `ffmpeg -crf 31 -tune stillimage` 壓一支 1080p 預覽版（約 24 MB）方便直接看，預覽版不是上傳用的檔案。
- **列印包卡住**：完整版 Chromium 在容器裡 `--print-to-pdf` 會一直不結束；改用 Playwright 附的 `chrome-headless-shell` 立刻完成。
- **列印原稿位置**：`classroom_pack.build()` 要求 `authoring_dir` 在 XiNewVideoGPT 的 academy 底下，所以 Q001 先寫到
  `$XINEW_ACADEMY/authoring/q001/print/`，再複製一份回本 repo 的 `academy/authoring/q001/print/`。
- **特別篇路線的字樣**：`special_builder` 預設副標是「番外篇」；`prepare_content.py` 在建置後把 manifest 的
  `subtitle`、`seriesHeader` 改成量子電腦學程的字樣。
