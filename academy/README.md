# 父子科技學院｜量子電腦學程（Q001–Q144）

把本 repo 既有的 4 場技術分享、transmon 筆記、影片報告簡報與 47 個 3D 場景，改編成父子科技學院格式的課程（2026-11-07 規劃 96 堂，2026-11-18 第二次擴充到 144 堂）：
每堂 120 分鐘、一支課前教學影片、一份 12 頁可編輯簡報、一包課堂教材。

| 要做的事 | 入口 |
|---|---|
| 看規劃與決策 | [課程擴充規劃](../docs/量子電腦學院_課程擴充規劃.md) |
| 看 144 堂主題與目標 | [課表索引](CURRICULUM_INDEX.md) |
| 看每堂教案 | `lessons/Qxxx/brief.md`、`lessons/Qxxx/lesson.json` |
| 看製作進度 | [製作狀態](PRODUCTION_STATUS.md) |
| 製作一集 | [製作指南](docs/PRODUCTION_GUIDE.md) |
| 製作 v2 動畫展示版（在投影片之間插入 3D 動畫實際操作錄影） | `authoring/v2/`（`demos.py` 寫段落與操作，`build_v2.py` 錄影、簡報、組裝，`qc_v2.py` 驗收，`deliver_v2.py` 交付） |
| 改課綱 | 改 `curriculum/lessons_data.py`，再跑 `python3 academy/curriculum/build_curriculum.py` |

## 已定案的決策（2026-11-07）

1. **對象**：由淺到深。QM01 親子共學（難度 1–2），QM02–QM03 高中以上，QM04–QM06 高中理組、大學與工程同仁。
2. **課號與位置**：獨立的 Q 系列，放在本 repo 的 `academy/`。
3. **影片**：沿用父子科技學院的陳犀牛片頭 v2、`zh-TW-YunJheNeural` 合成旁白、L001 簡報版型；YouTube 由使用者自己上傳。
4. **程式環境**：只用本機模擬器（Qiskit Aer 等），不需要雲端帳號。
5. **規模**：96 堂（6 模組 × 16 堂）；2026-11-18 依 repo 新增內容延伸為 144 堂（9 模組），見[規劃第 7 節](../docs/量子電腦學院_課程擴充規劃.md)。

## 模組

| 模組 | 課次 | 主題 | 對象 |
|---|---|---|---|
| QM01 | Q001–Q016 | 量子直覺：不用公式看懂量子 | 親子共學 |
| QM02 | Q017–Q032 | 超導量子位元：從超導到 transmon | 高中以上 |
| QM03 | Q033–Q048 | 讀取量子位元與周邊系統 | 高中以上 |
| QM04 | Q049–Q064 | 操作量子電腦與演算法 | 高中理組／大學／工程同仁 |
| QM05 | Q065–Q080 | 各種量子電腦平台 | 高中理組／大學／工程同仁 |
| QM06 | Q081–Q096 | 錯誤更正、應用與未來 | 高中理組／大學／工程同仁 |
| QM07 | Q097–Q112 | 超導量子電腦深入：師生對話十三課 | 高中理組／大學／工程同仁 |
| QM08 | Q113–Q128 | 動手寫量子電路：從八個範例到自己的線路 | 國中以上（修完 QM01 即可） |
| QM09 | Q129–Q144 | 量子電腦的供電與機房工程 | 工程同仁、電力電子背景 |

## 資料夾

```
academy/
  curriculum/lessons_data.py       課綱唯一來源
  curriculum/build_curriculum.py   產生下面所有課綱檔案
  curriculum/catalog.json          144 堂完整欄位（欄位名稱同父子科技學院 V2 課表）
  curriculum/production-status.json
  lessons/Qxxx/                    每堂 brief.md 與 lesson.json
  authoring/qxxx/                  每集的內容稿、教材產生器、查核紀錄
  episodes/qxxx-<slug>/            每集製作來源、教材、QC 與 delivery.json（大型成品不進 Git）
  docs/PRODUCTION_GUIDE.md         製作指南
```
