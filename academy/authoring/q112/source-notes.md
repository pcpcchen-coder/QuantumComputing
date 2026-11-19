# Q112 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接讀取原始 wikitext（Transmon 經 MediaWiki API 取得 revision id；Learning by teaching 經 action=raw 讀取，未取得 revision id，記錄讀取日）。學程內部文件與動畫程式由製作代理讀取。程式由製作代理實際執行；動畫面板數值由製作代理以 Playwright 開啟頁面讀取（單張截圖，非正式錄影、非 QV2_DRY）。

## Transmon（Wikipedia，oldid=1377984572）

- 「a '''transmon''' is a type of [[Superconductivity|superconducting]] [[charge qubit]] designed to have reduced sensitivity to charge noise.」
- 「one which consists of a [[Cooper-pair box]] "where the two superconductors are also [capacitively] shunted in order to decrease the sensitivity to charge noise, while maintaining a sufficient anharmonicity for selective qubit control".」
- 「The transmon achieves its reduced sensitivity to charge noise by significantly increasing the ratio of the [[Josephson energy]] to the charging energy. This is accomplished through the use of a large shunting capacitor.」
- 「The disadvantage is the reduced anharmonicity … Reduced anharmonicity complicates the device operation as a two level system, e.g. exciting the device from the ground state to the first excited state by a resonant pulse also populates the higher excited state.」

## Learning by teaching（Wikipedia，2026-11-18 以 action=raw 讀取）

- 「In the field of [[pedagogy]], '''learning by teaching''' is a method of [[teaching]] in which students are made to learn material and prepare [[lesson]]s to teach it to the other students. There is a strong emphasis on acquisition of [[life skills]] along with the subject matter.」

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md

- 開頭：「對話內容依主題重新編排成 3 篇、13 課」「每一課都附上可以直接開啟的 3D 互動動畫（animations/transmon-3d.html，共 12 章）」
- 使用方式：「**上課** | 每課約 30–50 分鐘：先播放對應動畫的導覽步驟，再用對話引導討論，最後讓學生操作「自由實驗」」；「**出題** | 「學生的理解 → 老師的修正」段落可以直接改成是非題或改錯題（見附錄 D）」
- 「**每一課的固定結構：** 1. 🎯 學習目標 2. 💬 師生對話（依原始討論整理，保留學生的原始問法） 3. 📌 重點整理 4. 🎬 動畫演示（直接點連結開啟；需連網載入 three.js） 5. ✏️ 課後練習」
- 範例參數：「十字電容 C_Σ | 約 77.5 fF」「位元頻率 f₀₁ | 5.21 GHz」「T₁ | 約 100 μs」
- 目錄：第一篇 硬體 第 1–6 課；第二篇 演算法 第 7–10 課；第三篇 容錯與系統 第 11–13 課。
- 課程地圖表：「3 | 迷思修正 | … | 第 6 章 案例」「4 | 頻率配置 | … | 第 6 章 案例」「6 | 讀取與重設 | … | 第 5 章 讀取」「7 | 疊加與 BV | … | 第 9 章 BV 密碼」「8 | 糾纏與 Grover | … | 第 7 章 振幅長條」「9 | Deutsch | … | 第 7 章（#deutsch）」「11 | 表面碼 | … | 第 10 章 表面碼」
- 第 2 課學生提問：「再延伸問一下，那 transmon 是怎麼寫入狀態的？SQUID 作用是？你用這張圖解釋清楚（之前你做的模型）。」
- 第 2 課零件表：十字電容板 C_Σ、SQUID（兩個 JJ 圍成迴路）、XY 驅動線「**寫入**：送 f₀₁ 的微波脈衝」、Z 磁通線「**調頻率**」、讀取共振腔（約 7 GHz）＋饋線；「重點：**SQUID 不負責寫入，XY 線才負責寫入。**」
- 第 2 課脈衝參數表：「振幅 × 時間（面積） | 旋轉**角度** | π 脈衝：|0⟩→|1⟩；π/2：|0⟩→(|0⟩+|1⟩)/√2」「微波**相位** | 繞**哪一軸**」「**頻率** | 選**哪一對能階** | 5.21 GHz 只驅動 0↔1」
- 第 2 課：「**SQUID 的兩個身分** 1. **非線性電感** … 2. **頻率旋鈕**」
- 第 2 課課後練習：「1. 要把 |0⟩ 寫成 (|0⟩+|1⟩)/√2，要調整脈衝的哪個參數？」答「脈衝面積（振幅 × 時間）做成 π/2」；「2. XY 線和 Z 線分別用電場還是磁場耦合到位元？」答「XY：電容耦合（電場）；Z：電感耦合（磁場，磁通穿過 SQUID 迴路）」
- 動畫內文（transmon-3d.html 第 1 章 B 分頁；「擺錘」比喻只在動畫，不在師生對話紀錄）：「**讓 transmon「變重」**：E_C = e²/2C_Σ 被壓低，背景電荷雜訊造成的頻率漂移隨 √(8E_J/E_C) 指數下降。就像單擺的擺錘越重，越不怕被推。」「電容太大，α 太小，脈衝容易漏到 |2⟩。」
- 附錄 D：「可以直接改成是非題或改錯題」，表列 12 條（# 1–12）。

## 互動動畫 animations/transmon-3d.html

- 第 1 章：kicker「第 1 章 / 12」、標題「一顆 transmon 的俯視圖」；分頁「晶片總覽」「大十字電容的作用」；按鈕「送出 π 脈衝」、勾選框「顯示標籤」；說明「送出脈衝後，十字板發出金光代表位元被激發到 |1⟩，之後依 T₁ 慢慢衰減回 |0⟩。」；面板「實際尺寸 數百 μm（示意，未按比例）」「電容 C_Σ ≈ 77.5 fF」。
- 標籤：「十字電容板 C_Σ」「SQUID：兩個約瑟夫森結」「讀取共振腔 ~7 GHz」「饋線」「XY 驅動線」「Z 磁通線」「接地面（Al）」「基板（矽 / 藍寶石）」。
- 程式：`xyPulses = makePulses(6, COL.teal)`；`if (xyT * 1.4 > 1) { excite = xyDe ? 0 : 1; }`；`excite *= Math.exp(-dt / 6);`
- 大十字電容分頁：`<input type="range" id="c1C" min="5" max="200" step="0.5" value="77.5">`；`EC_PER_FF = 19.37`；判斷 `ratio < 20 ? "電荷雜訊主導（接近 Cooper pair box）" : ratio <= 120 ? "transmon 區間" : "非諧性偏小，閘需放慢"`；`sGoal = Math.min(1.8, Math.max(0.3, capC / 77.5))`（十字板粗細）。
- 頁面實讀（Playwright）：77.5 fF「250 MHz | 60.0 | 5.21 GHz | −283 MHz | 1.9 kHz | transmon 區間」；20 fF「969 MHz | 15.5 | 9.69 GHz | −1.33 GHz | 53.1 MHz | 電荷雜訊主導（接近 Cooper pair box）」；200 fF「96.8 MHz | 154.9 | 3.31 GHz | −104 MHz | < 0.1 Hz | 非諧性偏小，閘需放慢」。
- 章節列：`b.id = "chap-" + c.id`；點 chap-readout →「色散讀取：從頻移讀出狀態」、chap-bv →「基本操作案例：3 顆位元一次猜中密碼（BV）」、chap-surface →「量子錯誤更正：表面碼」、chap-chip →「一顆 transmon 的俯視圖」；`capEl.hidden = i < 4`（第 5 章起顯示左上字幕）。

## 課綱：academy/lessons/Q112/lesson.json

- 「學習目標」：孩子當老師，用師生對話形式講一課，並用 3D 動畫示範；「動手任務」：挑十三課其中一課，改寫成自己的師生對話並錄音；「孩子獨立改造」：替這課加三題課後練習與解答；「好玩機制」：角色交換；「作品／交付」：自編師生對話一課；「生活技能支線」：教學相長；「常見誤解與安全提醒」：引用動畫畫面時註明出處；「錄音重點」：1. 在解決什麼？2. 我怎麼做？3. 哪裡容易錯？4. 生活中或真實的量子電腦哪裡會用到？；「需新增素材」：◆ 自編對話模板。

## teach_helper.py 實跑（Python 3.13.18，無外部套件）

見 classroom.py 的 RUN_OUTPUT；建置時會再跑一次並逐字比對。
