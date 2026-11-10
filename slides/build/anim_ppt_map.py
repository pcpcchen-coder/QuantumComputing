# -*- coding: utf-8 -*-
"""產生「3D 動畫場景 ↔ PPT 投影片」對照表，並檢查每個場景是否都有簡報介紹。

掃描 animations/*.html 的所有場景（含 transmon-3d.html 的 8 章與 #deutsch 捷徑），
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
ANIM_DIR = os.path.join(ROOT, "animations")

PAGES = [  # (html, 場景 JS 目錄 or None, 說明)
    ("index.html", "js/scenes", "JJ 元件與微波讀取"),
    ("peripherals.html", "js/peripherals", "量子電腦周邊系統"),
    ("operation.html", "js/operation", "如何操作量子電腦"),
    ("atoms.html", "js/atoms", "離子阱與中性原子"),
    ("transmon-3d.html", None, "Transmon 3D（8 章）"),
]
DECK_NAMES = {
    "slides/JJ_Microwave_Readout_Talk.pptx": "JJ 與微波讀取",
    "slides/QC_Peripheral_Systems_Talk.pptx": "周邊系統",
    "slides/QC_Operation_Talk.pptx": "量子電腦操作",
    "slides/Ion_NeutralAtom_Talk.pptx": "離子阱與中性原子",
    "slides/transmon.pptx": "Transmon",
    "slides/output/qfish008-deutsch-algorithm.pptx": "量子金魚 008 Deutsch",
}


def scenes_of(html, js_dir):
    """回傳 [(id, 標題)]，依動畫中的順序。"""
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
                if u.scheme not in ("", "file") or "animations/" not in u.path:
                    continue
                html = os.path.basename(u.path)
                scene = u.fragment or "（首頁）"
                refs[(html, scene)].append((rel, no, slide_title(slide)))

    lines = ["# 3D 動畫 ↔ PPT 簡報對照表", "",
             "> 由 `python3 slides/build/anim_ppt_map.py` 自動產生（掃描 `animations/` 的場景與所有 `.pptx` 的超連結）。",
             "> 簡報裡的動畫連結都是相對路徑（例如 `../animations/index.html#bloch`），請保持 `slides/` 與 `animations/` 的相對位置；"
             "下表的「動畫網址」欄也用相對於 repo 根目錄的路徑，點下去就是對應場景。", ""]
    summary, missing, body = [], [], []
    for html, js_dir, desc in PAGES:
        sc = scenes_of(html, js_dir)
        covered = sum(1 for sid, _ in sc if refs.get((html, sid)))
        summary.append(f"| [`{html}`](../animations/{html}) | {desc} | {len(sc)} | {covered} | "
                       f"{'✅ 全部有' if covered == len(sc) else '⚠️ 缺 ' + str(len(sc) - covered)} |")
        body += [f"## `animations/{html}`：{desc}", "",
                 "| # | 場景 | 動畫網址 | 對應投影片（簡報 第 N 頁：標題） |", "|---|---|---|---|"]
        for k, (sid, title) in enumerate(sc, 1):
            r = refs.get((html, sid), [])
            if not r:
                missing.append(f"{html}#{sid}")
            by_deck = defaultdict(list)
            for deck, no, t in r:
                by_deck[deck].append(f"p{no} {t}")
            cell = "<br>".join(f"**{DECK_NAMES.get(d, d)}**（[`{os.path.basename(d)}`](../{d})）：" + "；".join(v)
                               for d, v in by_deck.items()) or "⚠️ 無"
            body.append(f"| {k} | {title} | [`#{sid}`](../animations/{html}#{sid}) | {cell} |")
        body.append("")
    lines += ["## 總覽", "", "| 動畫 | 主題 | 場景數 | 有簡報介紹 | 狀態 |", "|---|---|---|---|---|"] + summary + [""]
    lines += body
    if missing:
        lines += ["## 缺口", ""] + [f"- `{m}`" for m in missing] + [""]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print("wrote", os.path.relpath(OUT, ROOT))
    if missing:
        print("缺少簡報介紹的場景：", ", ".join(missing))
        sys.exit(1)
    print("所有場景都有對應投影片。")


if __name__ == "__main__":
    main()
