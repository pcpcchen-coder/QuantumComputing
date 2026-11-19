這是依課綱製作的課前教學版，不是實際上課錄音。

父子科技學院量子電腦學程第一百一十八堂（八個量子電路範例的範例 5）：用一對糾纏位元加 2 個古典位元，把 q0 的狀態 ψ 搬到遠方 Bob 的 q2；四種 ψ 各傳一次，用 Bloch 球確認 Bob 收到的狀態。

這一集會學到
・範例 5 的四步：準備 ψ（q0）→ H + CNOT 讓 q1、q2 成為 Bell 態 → Alice 做 CNOT、H，量出 2 個位元 → Bob 照結果修正（q1 = 1 做 X、q0 = 1 做 Z）
・Alice 的四種結果各 ¼，Bob 手上分別是 ψ、Zψ、Xψ、XZψ，修完都是 ψ
・收到 2 個位元之前，Bob 的 q2 完全隨機：沒有古典通訊就完成不了，所以不能超光速
・延遲量測版：動畫用受控閘代替「量測後再修正」，結果相同；真的傳遠還是要先量
・四種 ψ（√¾|0⟩+½|1⟩、|1⟩、|+⟩、|−⟩）：|+⟩、|−⟩ 量起來一樣，要看 Bloch 球；傳完 q0 不再保有 ψ，是搬家不是複製
・拿掉修正：四種都縮在球心；只修 X 時 |+⟩ 量起來還是一半一半，其實傳錯

主要來源：維基百科 Quantum teleportation、Deferred measurement principle、No-cloning theorem、No-communication theorem；本學程「量子電路入門：八個範例」簡報第 15–17 頁與 basic-circuits.html、operation.html 互動動畫；本機 teleport_lab.py 與 Qiskit 2.6.2 實跑紀錄。

教材用法（classroom.zip）
先讀「00_爸爸先讀」，照「01_操作步驟」開 basic-circuits.html#teleport，四種 ψ 各逐步傳一次、量測 1,000 次；列印包有傳送流程表、三人傳送角色卡與修正表、拿掉修正的改造單、最後一關檢核表。課堂 120 分鐘另計。
