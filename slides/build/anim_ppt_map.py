# -*- coding: utf-8 -*-
"""產生「3D 動畫場景 ↔ PPT 投影片」對照表，並檢查每個場景是否都有簡報介紹。

掃描 animations/*.html 的所有場景（含 transmon-3d.html 的 12 章與 #deutsch 捷徑），
再掃描 repo 內所有 .pptx 的超連結，輸出 docs/動畫與簡報對照表.md。
有場景沒有任何投影片連到時，程式以結束碼 1 結束並列出缺口。

用法（在 repo 根目錄）：python3 slides/build/anim_ppt_map.py
"""
import glob
import os
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse

from pptx import Presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "docs", "動畫與簡報對照表.md")
README = os.path.join(ROOT, "README.md")
README_BEGIN, README_END = "<!-- anim-map:begin -->", "<!-- anim-map:end -->"   # README 裡自動更新的區塊
ANIM_DIR = os.path.join(ROOT, "animations")
PAGES_ANIM = "https://pcpcchen-coder.github.io/QuantumComputing/animations/"   # GitHub Pages

PAGES = [  # (html, 場景 JS 目錄 or None, 說明)
    ("index.html", "js/scenes", "JJ 元件與微波讀取"),
    ("peripherals.html", "js/peripherals", "量子電腦周邊系統"),
    ("operation.html", "js/operation", "如何操作量子電腦"),
    ("atoms.html", "js/atoms", "離子阱與中性原子"),
    ("transmon-3d.html", None, "Transmon 3D（12 章）"),
    ("power1000.html", "inline", "1,000 位元供電設計"),
    ("lc-vs-jj.html", "sections", "LC 與約瑟夫森接面（2D 圖解）"),
    ("basic-circuits.html", "engine", "八個基礎量子電路（2D 互動）"),
]
DECK_NAMES = {
    "slides/JJ_Microwave_Readout_Talk.pptx": "JJ 與微波讀取",
    "slides/QC_Peripheral_Systems_Talk.pptx": "周邊系統",
    "slides/QC_Operation_Talk.pptx": "量子電腦操作",
    "slides/Ion_NeutralAtom_Talk.pptx": "離子阱與中性原子",
    "slides/transmon.pptx": "Transmon",
    "slides/output/qfish008-deutsch-algorithm.pptx": "量子金魚 008 Deutsch",
    "slides/output/qc-power-supply.pptx": "量子電腦供電設計",
    "slides/output/basic-circuits.pptx": "八個基礎量子電路",
}
DECK_SHORT = {   # README 精簡表用的簡稱
    "slides/JJ_Microwave_Readout_Talk.pptx": "JJ", "slides/QC_Peripheral_Systems_Talk.pptx": "周邊",
    "slides/QC_Operation_Talk.pptx": "操作", "slides/Ion_NeutralAtom_Talk.pptx": "離子阱",
    "slides/transmon.pptx": "transmon", "slides/output/qfish008-deutsch-algorithm.pptx": "qfish008",
    "slides/output/qc-power-supply.pptx": "供電", "slides/output/basic-circuits.pptx": "基礎電路",
}


def page_list(nums):
    """[6, 7, 8, 14] → 'p6–8、14'"""
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else "、".join(str(n) for n in nums[i:j + 1]))
        i = j + 1
    return "p" + "、".join(out)


def readme_block(refs):
    """README 的總覽與「場景 → 投影片頁碼」精簡表。"""
    head = ["### 總覽", "",
            "> 這一段由 `python3 slides/build/anim_ppt_map.py` 自動更新，請不要手動修改。", "",
            "| 動畫（線上版） | 場景數 | 對應簡報 | 狀態 |", "|---|---|---|---|"]
    rows = ["", "### 場景 → 投影片頁碼", "",
            "主要簡報的頁碼不加前綴；其他簡報以簡稱標示（JJ、周邊、操作、離子阱、transmon、qfish008、供電、基礎電路）。", "",
            "| 動畫 | 主要簡報 | 場景代號 → 頁碼 |", "|---|---|---|"]
    for html, js_dir, desc in PAGES:
        sc = scenes_of(html, js_dir)
        decks = defaultdict(int)
        for sid, _ in sc:
            for d, _, _ in refs.get((html, sid), []):
                decks[d] += 1
        main_deck = max(decks, key=decks.get) if decks else None
        covered = sum(1 for sid, _ in sc if refs.get((html, sid)))
        deck_cell = "；".join(f"[`{os.path.basename(d)}`]({d})" for d in sorted(decks, key=lambda d: -decks[d]))
        status = "✅ 全部有" if covered == len(sc) else f"⚠️ 缺 {len(sc) - covered}"
        head.append(f"| [`{html}`]({PAGES_ANIM}{html})：{desc} | {len(sc)} | {deck_cell or '—'} | {status} |")
        cells = []
        for sid, _ in sc:
            by = defaultdict(list)
            for d, no, _ in refs.get((html, sid), []):
                by[d].append(no)
            if not by:
                cells.append(f"{sid} ⚠️ 無")
                continue
            parts = [page_list(by[main_deck])] if main_deck in by else []
            parts += [f"{DECK_SHORT.get(d, d)} {page_list(v)}" for d, v in by.items() if d != main_deck]
            cells.append(f"{sid} " + "、".join(parts[:1]) + (f"（另 {'；'.join(parts[1:])}）" if len(parts) > 1 else ""))
        rows.append(f"| **{html}** | {DECK_SHORT.get(main_deck, '—')} | {'；'.join(cells)} |")
    listed = {h for h, _, _ in PAGES}
    extra = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ANIM_DIR, "*.html"))
                   if os.path.basename(p) not in listed)
    for html in extra:
        linked = [k for k in refs if k[0] == html]
        head.append(f"| [`{html}`]({PAGES_ANIM}{html}) | —（沒有場景代號） | "
                    f"{'有連結' if linked else '目前沒有簡報連結'} | {'✅' if linked else '—'} |")
    return "\n".join(head + rows)


def update_readme(refs):
    text = open(README, encoding="utf-8").read()
    if README_BEGIN not in text or README_END not in text:
        print("README 沒有 anim-map 標記，略過")
        return
    a = text.index(README_BEGIN) + len(README_BEGIN)
    b = text.index(README_END)
    new = text[:a] + "\n" + readme_block(refs) + "\n" + text[b:]
    if new != text:
        open(README, "w", encoding="utf-8").write(new)
        print("updated README.md")


def scenes_of(html, js_dir):
    """回傳 [(id, 標題)]，依動畫中的順序。"""
    if js_dir == "engine":  # basic-circuits.html：SCENES 陣列裡的 { id: "…", short: "…", title: "…" }
        s = open(os.path.join(ANIM_DIR, html), encoding="utf-8").read()
        return re.findall(r'id: "([\w-]+)", short: "[^"]*", title: "([^"]+)"', s)
    if js_dir == "sections":  # 單頁圖解：<section class="step" id="…"> 後面的 <h2>
        s = open(os.path.join(ANIM_DIR, html), encoding="utf-8").read()
        return [(sid, re.sub(r"<[^>]+>", "", t).strip())
                for sid, t in re.findall(r'<section class="step" id="([\w-]+)".*?<h2[^>]*>(.*?)</h2>', s, re.S)]
    if js_dir == "inline":  # 場景直接寫在 HTML 裡：S({ id: '…', title: '…'
        s = open(os.path.join(ANIM_DIR, html), encoding="utf-8").read()
        return re.findall(r"S\(\{ id: '([\w-]+)', title: '([^']+)'", s)
    if js_dir:
        out = []
        for f in sorted(glob.glob(os.path.join(ANIM_DIR, js_dir, "[0-9]*.js"))):
            s = open(f, encoding="utf-8").read()
            sid = re.search(r"id:\s*['\"]([\w-]+)['\"]", s).group(1)
            title = re.search(r"title:\s*['\"]([^'\"]+)['\"]", s).group(1)
            out.append((sid, title))
        return out
    s = open(os.path.join(ANIM_DIR, html), encoding="utf-8").read()
    out = re.findall(r'\{ id: "([\w-]+)", short: "[^"]*", kicker: "[^"]*", title: "([^"]+)"', s)
    alias = re.search(r"HASH_ALIAS = \{([^}]*)\}", s)
    if alias:
        for name in re.findall(r'"?([\w-]+)"?:\s*\[', alias.group(1)):
            out.append((name, f"（捷徑）第 7 章 {'Deutsch 步驟' if name == 'deutsch' else 'Deutsch 自由實驗'}"))
    return out


def slide_title(slide):
    if slide.shapes.title is not None and slide.shapes.title.text.strip():
        return slide.shapes.title.text.strip().split("\n")[0]
    for sh in slide.placeholders:
        if sh.placeholder_format.type is not None and "TITLE" in str(sh.placeholder_format.type) and sh.text.strip():
            return sh.text.strip().split("\n")[0]
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            return sh.text_frame.text.strip().split("\n")[0]
    return ""


def links_of(slide):
    found = set()
    for sh in slide.shapes:
        try:
            a = sh.click_action.hyperlink.address
            if a:
                found.add(a)
        except Exception:
            pass
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.hyperlink.address:
                        found.add(r.hyperlink.address)
    return found


def main():
    refs = defaultdict(list)   # (html, id) -> [(deck, page, title)]
    decks = sorted(p for p in glob.glob(os.path.join(ROOT, "**", "*.pptx"), recursive=True)
                   if "/node_modules/" not in p and "/build/" not in p)
    for path in decks:
        rel = os.path.relpath(path, ROOT)
        prs = Presentation(path)
        for no, slide in enumerate(prs.slides, 1):
            for a in links_of(slide):
                u = urlparse(a)
                if u.scheme not in ("", "file", "http", "https") or "animations/" not in u.path:
                    continue
                html = os.path.basename(u.path)
                scene = u.fragment or "（首頁）"
                refs[(html, scene)].append((rel, no, slide_title(slide)))

    lines = ["# 3D 動畫 ↔ PPT 簡報對照表", "",
             "> 由 `python3 slides/build/anim_ppt_map.py` 自動產生（掃描 `animations/` 的場景與所有 `.pptx` 的超連結）。",
             "> 簡報裡的動畫連結都是 GitHub Pages 網址（例如 " + PAGES_ANIM + "index.html#bloch），在任何地方點都能開啟；"
             "下表的「動畫網址」欄也是同一個網址，點下去就是對應場景。離線時可改開 repo 內的 `animations/<頁面>.html#<場景>`。", ""]
    summary, missing, body = [], [], []
    for html, js_dir, desc in PAGES:
        sc = scenes_of(html, js_dir)
        covered = sum(1 for sid, _ in sc if refs.get((html, sid)))
        summary.append(f"| [`{html}`]({PAGES_ANIM}{html}) | {desc} | {len(sc)} | {covered} | "
                       f"{'✅ 全部有' if covered == len(sc) else '⚠️ 缺 ' + str(len(sc) - covered)} |")
        body += [f"## `animations/{html}`：{desc}", "",
                 "| # | 場景 | 動畫網址 | 對應投影片（簡報 第 N 頁：標題） |", "|---|---|---|---|"]
        for k, (sid, title) in enumerate(sc, 1):
            r = refs.get((html, sid), [])
            if not r:
                missing.append(f"{html}#{sid}")
            by_deck = defaultdict(list)
            for deck, no, t in r:
                by_deck[deck].append(f"p{no} {t}".replace("|", "\\|"))
            cell = "<br>".join(f"**{DECK_NAMES.get(d, d)}**（[`{os.path.basename(d)}`](../{d})）：" + "；".join(v)
                               for d, v in by_deck.items()) or "⚠️ 無"
            esc = lambda t: t.replace("|", "\\|")   # 標題裡的 |0⟩ 會打斷 Markdown 表格
            body.append(f"| {k} | {esc(title)} | [`#{sid}`]({PAGES_ANIM}{html}#{sid}) | {cell} |")
        body.append("")
    lines += ["## 總覽", "", "| 動畫 | 主題 | 場景數 | 有簡報介紹 | 狀態 |", "|---|---|---|---|---|"] + summary + [""]
    lines += body
    if missing:
        lines += ["## 缺口", ""] + [f"- `{m}`" for m in missing] + [""]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print("wrote", os.path.relpath(OUT, ROOT))
    update_readme(refs)
    if missing:
        print("缺少簡報介紹的場景：", ", ".join(missing))
        sys.exit(1)
    print("所有場景都有對應投影片。")


if __name__ == "__main__":
    main()
