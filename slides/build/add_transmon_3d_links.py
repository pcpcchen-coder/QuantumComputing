# -*- coding: utf-8 -*-
"""替 slides/transmon.pptx 補上 3D 動畫（animations/transmon-3d.html）的連結與介紹頁。

做的事：
1. 既有頁面右上角加「▶ 3D 第 N 章」按鈕（點擊開啟對應章節），講者備註補上動畫網址。
2. 在「一句話總結」之前新增第 04 段「用 3D 動畫走一遍」：
   八章導覽、操控與讀取、案例（頻率配置）、振幅長條（糾纏／Grover／Deutsch）、Shor。
3. 總結頁的「animations/transmon-3d.html」改成可點的超連結。

可重複執行：一律從 slides/build/transmon_base.pptx（原始 17 頁）出發，輸出覆寫 slides/transmon.pptx。
要改原始內容請改 transmon_base.pptx 後再執行本腳本。
用法（在 repo 根目錄）：
    node slides/capture_3d_transmon.js          # 需要時重新擷取截圖
    python3 slides/build/add_transmon_3d_links.py
"""
import copy
import os

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PPTX = os.path.join(ROOT, "slides", "transmon.pptx")
BASE = os.path.join(ROOT, "slides", "build", "transmon_base.pptx")   # 原始 17 頁（未加動畫連結）
FIG = os.path.join(ROOT, "slides", "figures", "3d_transmon")
ANIM = "https://pcpcchen-coder.github.io/QuantumComputing/animations/transmon-3d.html"   # GitHub Pages 網址

FONT = "Microsoft JhengHei"
INK = RGBColor(0x16, 0x18, 0x1D)
INK2 = RGBColor(0x3A, 0x3F, 0x4A)
CARD = RGBColor(0xEE, 0xF1, 0xF3)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
TEAL = RGBColor(0x17, 0x87, 0x7F)
GRAY = RGBColor(0x7D, 0x87, 0x96)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

TAG_LINK = "anim-link"          # 按鈕 shape 名稱前綴
TAG_SLIDE = "anim-3d-slide"     # 新增投影片的標記 shape 名稱
NOTE_MARK = "【3D 動畫】"

CHAPTERS = {
    "chip": (1, "晶片"), "junction": (2, "約瑟夫森結"), "potential": (3, "位能井"),
    "control": (4, "操控"), "readout": (5, "讀取"), "case": (6, "案例"),
    "grover": (7, "振幅長條"), "shor": (8, "Shor"),
    "bv": (9, "BV 密碼"), "surface": (10, "表面碼"), "surgery": (11, "邏輯閘"), "stack": (12, "軟體堆疊"),
    "deutsch": (7, "Deutsch"), "deutsch-lab": (7, "自由實驗"),
}


def url(hash_):
    return f"{ANIM}#{hash_}"


def pill_label(hash_):
    n, short = CHAPTERS[hash_]
    return f"▶ 3D 第 {n} 章：{short}"


# --------------------------------------------------------------------------- 基本元件
def style_run(run, size, color, bold=False, italic=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    f.name = FONT
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rpr.find(f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}{tag[2:]}")
        if el is None:
            el = etree.SubElement(rpr, f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}{tag[2:]}")
        el.set("typeface", FONT)


def textbox(slide, x, y, w, h, paras, size=12, color=INK2, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, name=None, space=4):
    """paras: list of str 或 list of [(text, {bold, color, size, link})]"""
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if i:
            p.space_before = Pt(space)
        runs = [(para, {})] if isinstance(para, str) else para
        for text, o in runs:
            r = p.add_run()
            r.text = text
            style_run(r, o.get("size", size), o.get("color", color), o.get("bold", False), o.get("italic", False))
            if o.get("link"):
                r.hyperlink.address = o["link"]
    return tb


def pill(slide, x, y, w, h, hash_, label=None, size=10):
    """可點的圓角按鈕：shape 與文字都帶超連結。"""
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    sh.name = f"{TAG_LINK}_{hash_}"
    sh.adjustments[0] = 0.5
    sh.fill.solid()
    sh.fill.fore_color.rgb = TEAL
    sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Emu(45720)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label or pill_label(hash_)
    style_run(r, size, WHITE, bold=True)
    r.hyperlink.address = url(hash_)
    sh.click_action.hyperlink.address = url(hash_)
    # 文字超連結顏色跟隨文字（PowerPoint 2019+），避免變成藍底線
    hl = r._r.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}hlinkClick")
    if hl is not None:
        ext = etree.SubElement(hl, "{http://schemas.openxmlformats.org/drawingml/2006/main}extLst")
        e = etree.SubElement(ext, "{http://schemas.openxmlformats.org/drawingml/2006/main}ext",
                             uri="{A12FA001-AC4F-418D-AE19-62706E023703}")
        c = etree.SubElement(e, "{http://schemas.microsoft.com/office/drawing/2018/hyperlinkcolor}hlinkClr",
                             nsmap={"ahyp": "http://schemas.microsoft.com/office/drawing/2018/hyperlinkcolor"})
        c.set("val", "tx")
    return sh


def picture(slide, name, x, y, w, link=None):
    pic = slide.shapes.add_picture(os.path.join(FIG, name + ".jpg"), Emu(x), Emu(y), width=Emu(w))
    pic.name = f"{TAG_LINK}_img_{name}"
    if link:
        pic.click_action.hyperlink.address = url(link)
    pic.line.color.rgb = RGBColor(0xD5, 0xDA, 0xE0)
    pic.line.width = Pt(0.75)
    return pic


def picture_fit(slide, name, x, y, w, h, link=None):
    """等比例縮放後置中放進 w × h 的框（截圖比例不一時用），框底填深色。"""
    from PIL import Image
    iw, ih = Image.open(os.path.join(FIG, name + ".jpg")).size
    if abs(iw / ih - w / h) < 0.02:
        return picture(slide, name, x, y, w, link=link)
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(x), Emu(y), Emu(w), Emu(h))
    frame.name = f"{TAG_LINK}_frame_{name}"
    frame.fill.solid(); frame.fill.fore_color.rgb = RGBColor(0x0A, 0x0C, 0x11)
    frame.line.color.rgb = RGBColor(0xD5, 0xDA, 0xE0); frame.line.width = Pt(0.75); frame.shadow.inherit = False
    scale = min(w / iw, h / ih)
    pw, ph = int(iw * scale), int(ih * scale)
    pic = slide.shapes.add_picture(os.path.join(FIG, name + ".jpg"), Emu(x + (w - pw) // 2), Emu(y + (h - ph) // 2),
                                   width=Emu(pw), height=Emu(ph))
    pic.name = f"{TAG_LINK}_img_{name}"
    if link:
        pic.click_action.hyperlink.address = url(link)
    return pic


def set_title(slide, text):
    from pptx.enum.shapes import PP_PLACEHOLDER
    t = next(ph for ph in slide.placeholders if ph.placeholder_format.type == PP_PLACEHOLDER.TITLE)
    t.text = text
    for r in t.text_frame.paragraphs[0].runs:
        style_run(r, 26, INK, bold=True)
    # 頁碼：沿用既有頁面的 Slide Number placeholder
    if _SLDNUM is not None:
        slide.shapes._spTree.append(copy.deepcopy(_SLDNUM))


_SLDNUM = None


def add_notes(slide, text):
    tf = slide.notes_slide.notes_text_frame
    old = tf.text.strip()
    tf.text = (old + "\n\n" if old else "") + text


def marker(slide):
    m = slide.shapes.add_textbox(0, 0, Emu(10), Emu(10))
    m.name = TAG_SLIDE


# --------------------------------------------------------------------------- 既有頁面加按鈕
SW, SH = 9144000, 5143500
PILL_H = Inches(0.27)
PILL_Y = Inches(0.07)

EXISTING = {   # 投影片頁碼（1 起算）→ 章節
    1: ["chip"],
    4: ["junction"],
    5: ["junction"],
    6: ["potential"],
    7: ["potential"],
    8: ["potential"],
    10: ["chip"],
    11: ["chip"],
    12: ["potential"],
    14: ["potential"],
    15: ["potential"],
    16: ["control", "readout", "case"],
}


def add_existing_buttons(prs):
    slides = list(prs.slides)
    for no, hashes in EXISTING.items():
        s = slides[no - 1]
        if no == 1:   # 封面：放在標題區下方
            pill(s, Inches(0.55), Inches(4.55), Inches(2.3), Inches(0.34), "chip",
                 label="▶ 開啟 3D 互動動畫（8 章）", size=11)
        else:
            w = Inches(1.75)
            gap = Inches(0.08)
            x = SW - Inches(0.25) - len(hashes) * w - (len(hashes) - 1) * gap
            for k, h in enumerate(hashes):
                pill(s, x + k * (w + gap), PILL_Y, w, PILL_H, h, size=9)
        lines = [f"{pill_label(h)[2:]}　{url(h)}" for h in hashes]
        add_notes(s, NOTE_MARK + "\n" + "\n".join(lines))


def link_summary(prs):
    s = list(prs.slides)[-1]
    for sh in s.shapes:
        if sh.has_text_frame and "animations/transmon-3d.html" in sh.text_frame.text:
            tf = sh.text_frame
            p = tf.paragraphs[0]
            for r in list(p.runs):
                r._r.getparent().remove(r._r)
            for text, link in (("配套：", None), ("notes/transmon-josephson-inductance.md", "../notes/transmon-josephson-inductance.md"),
                               (" ・ ", None), ("animations/transmon-3d.html（點此開啟 3D 動畫）", url("chip"))):
                r = p.add_run()
                r.text = text
                style_run(r, 11, RGBColor(0xA3, 0xAA, 0xB5))
                if link:
                    r.hyperlink.address = link


# --------------------------------------------------------------------------- 新增投影片
def layout(prs, name):
    return next(l for l in prs.slide_layouts if l.name == name)


def new_section(prs):
    s = prs.slides.add_slide(layout(prs, "SECTION"))
    ph = list(s.placeholders)
    texts = ["04", "用 3D 動畫走一遍", "transmon-3d.html 十二章：晶片 → 約瑟夫森結 → 位能井 → 操控 → 讀取 → 案例 → 振幅長條 → Shor → BV 密碼 → 表面碼 → 邏輯閘 → 軟體堆疊"]
    for p, t in zip(ph, texts):
        p.text = t
    marker(s)
    pill(s, Inches(0.6), Inches(4.35), Inches(2.4), Inches(0.36), "chip", label="▶ 開啟 3D 互動動畫", size=12)
    add_notes(s, "接下來不講新公式，而是打開 3D 動畫，把前面三段講的東西實際動起來看一次，"
                 "再往前走：多顆位元的頻率配置、兩位元的振幅運算、Shor 與 BV 演算法，"
                 "最後看錯誤更正（表面碼、lattice surgery 與魔術態）和把程式變成微波的軟體堆疊。\n\n"
                 + NOTE_MARK + "\n" + url("chip"))
    return s


def new_tour(prs):
    s = prs.slides.add_slide(layout(prs, "CONTENT"))
    set_title(s, "3D 動畫導覽：十二章一覽")
    marker(s)
    rows = [
        ("chip", "一顆 transmon 的俯視圖", "十字電容、SQUID、XY／Z 線、讀取共振腔；π 脈衝與 T₁", "p10、11"),
        ("junction", "約瑟夫森結：非線性電感", "拖動相位差 φ：I = I_c sin φ、L_J = L_J0 / cos φ", "p4、5"),
        ("potential", "cos 位能井：能階不再等距", "cos 井 vs 拋物線、能階越往上越密、量子單擺", "p6–8、14、15"),
        ("control", "用微波轉動布洛赫球", "X／Y 軸 π、π/2 脈衝，Rabi 振盪與 P(|1⟩)", "p16、19"),
        ("readout", "色散讀取：從頻移讀出狀態", "±χ 頻移、IQ 點群、讀取鏈與重設", "p16、19"),
        ("case", "案例：三顆可調 transmon", "SQUID 調頻、頻率碰撞、XY 串擾、CZ 閘", "p16、20"),
        ("grover", "振幅長條：糾纏、Grover、Deutsch", "CZ 產生糾纏、Oracle＋擴散、一次查詢", "p21"),
        ("shor", "Shor：用 QFT 找週期，分解 15", "模指數、量子傅立葉轉換、連分數與 gcd", "p22"),
        ("bv", "BV：3 顆位元一次猜中密碼", "H → 黑盒子 → H → 量測；在 transmon 上的時間與誤差", "p23"),
        ("surface", "量子錯誤更正：表面碼", "穩定子、亮點配對解碼、邏輯錯誤、碼距與閾值", "p24"),
        ("surgery", "Lattice surgery 與魔術態蒸餾", "縫合補丁做邏輯 CNOT、T 閘傳送、15-to-1 蒸餾", "p25"),
        ("stack", "編譯與控制軟體堆疊", "分解、映射、路由、最佳化、排程脈衝、回饋、校準", "p26"),
    ]
    x0, y0 = Inches(0.4), Inches(0.98)
    cw, rh, gap = Inches(4.55), Inches(0.62), Inches(0.1)
    for k, (h, title, desc, pages) in enumerate(rows):
        col, row = divmod(k, 6)
        x, y = x0 + col * (cw + gap), y0 + row * rh
        bg = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y + Inches(0.03), cw, rh - Inches(0.06))
        bg.adjustments[0] = 0.12
        bg.fill.solid(); bg.fill.fore_color.rgb = CARD; bg.line.fill.background(); bg.shadow.inherit = False
        bg.name = "row-bg"
        pill(s, x + Inches(0.08), y + Inches(0.1), Inches(1.45), Inches(0.24), h, size=8)
        textbox(s, x + Inches(0.08), y + Inches(0.37), Inches(1.45), Inches(0.2), [pages], size=8, color=GRAY,
                align=PP_ALIGN.CENTER)
        textbox(s, x + Inches(1.62), y + Inches(0.08), cw - Inches(1.7), Inches(0.5),
                [[(title, {"bold": True, "color": INK, "size": 10.5, "link": url(h)})], desc], size=8.5, space=1)
    textbox(s, x0, Inches(4.75), Inches(9.2), Inches(0.3),
            ["點按鈕或標題即開啟線上動畫（GitHub Pages：" + ANIM + "#章節）；離線時可改開 repo 內的 animations/transmon-3d.html。"
             " 捷徑：#deutsch 直接進第 7 章 Deutsch 步驟、#deutsch-lab 進自由實驗。"], size=7.5, color=GRAY)
    add_notes(s, "這張是 3D 動畫的目錄。每一格左邊的按鈕可以直接跳到該章，按鈕下方是本簡報對應的頁碼。"
                 "前三章對應第一、二段的觀念，第四、五章對應控制與讀取，第六到九章從一顆位元走到多顆位元和演算法，"
                 "第十、十一章是量子錯誤更正，第十二章是把程式變成微波的軟體堆疊。\n\n"
                 + NOTE_MARK + "\n" + "\n".join(f"第 {CHAPTERS[r[0]][0]} 章　{url(r[0])}" for r in rows))
    return s


def two_image_slide(prs, title, imgs, caps, hashes, bullets, notes, pill_labels=None):
    s = prs.slides.add_slide(layout(prs, "CONTENT"))
    set_title(s, title)
    marker(s)
    iw = Inches(3.05)
    ih = int(iw * 840 / 1160)
    xs = [Inches(0.45), Inches(0.45) + iw + Inches(0.12)]
    y = Inches(1.0)
    for k, (img, cap) in enumerate(zip(imgs, caps)):
        picture_fit(s, img, xs[k], y, iw, ih, link=hashes[min(k, len(hashes) - 1)])
        textbox(s, xs[k], y + ih + Inches(0.05), iw, Inches(0.25), [cap], size=9, color=GRAY, align=PP_ALIGN.CENTER)
    # 下方按鈕列
    bw = Inches(1.95)
    for k, h in enumerate(hashes):
        lab = pill_labels[k] if pill_labels else None
        pill(s, Inches(0.45) + k * (bw + Inches(0.12)), Inches(3.62), bw, Inches(0.3), h, label=lab, size=9)
    # 右側說明
    bx = Inches(6.85)
    paras = []
    for b in bullets:
        if isinstance(b, tuple):
            head, body = b
            paras.append([(head, {"bold": True, "color": TEAL, "size": 11}), ("　" + body, {})])
        else:
            paras.append(b)
    textbox(s, bx, Inches(1.0), SW - bx - Inches(0.35), Inches(3.75), paras, size=10, space=6)
    textbox(s, Inches(0.45), Inches(4.05), Inches(6.2), Inches(0.75),
            ["動畫網址：" + "\n".join(f"{ANIM}#{h}" for h in hashes)], size=8, color=GRAY)
    add_notes(s, notes + "\n\n" + NOTE_MARK + "\n" + "\n".join(f"{pill_label(h)[2:]}　{url(h)}" for h in hashes))
    return s


def build_new(prs):
    out = [new_section(prs), new_tour(prs)]
    out.append(two_image_slide(
        prs, "3D：微波操控與色散讀取",
        ["ch4_control", "ch5_readout"],
        ["第 4 章：X 軸 π/2 脈衝把 |0⟩ 轉到赤道", "第 5 章：量測 20 次，IQ 平面分成兩群"],
        ["control", "readout"],
        [("操控", "以 f₀₁ = 5.21 GHz 微波驅動，狀態在布洛赫球上繞 X 或 Y 軸旋轉；|1⟩→|2⟩ 低 283 MHz，不會被同一道微波推上去。"),
         ("讀取", "位元與 7 GHz 共振腔失諧約 1.8 GHz，共振腔頻率依狀態偏移 χ/2π ≈ ±0.77 MHz。"),
         ("IQ 點群", "在兩個頻率中間送探測微波，反射相位因狀態不同而分成兩群；結果依第 4 章的機率隨機出現。"),
         ("動手試", "先按「準備疊加態」再「量測 20 次」，統計會接近 P(|1⟩) = 0.5。")],
        "這一頁把第 16 頁的 XY 旋轉與色散讀取放進 3D。第 4 章可以按 X 軸 π、π/2、Y 軸 π/2，"
        "看布洛赫球上的箭頭怎麼轉；第 5 章把同一個疊加態量測 20 次，可以看到 IQ 平面上的兩個點群，"
        "以及每次量測結果都是隨機的 0 或 1。"))
    out.append(two_image_slide(
        prs, "案例：三顆可調 transmon 的頻率配置",
        ["ch6_case_plan", "ch6_case_cz"],
        ["步驟 ③：用 Z 線把 Q1、Q3 調到各自的頻率地址", "步驟 ⑤：CZ 閘刻意短暫拜訪 |11⟩↔|20⟩ 碰撞點"],
        ["case"],
        [("① 製程誤差", "JJ 氧化層差幾個原子，E_J 就差好幾 %，三顆頻率散亂、互相碰撞。"),
         ("② SQUID 調頻", "E_J(Φ) = E_J,max |cos(πΦ/Φ₀)|，用 Z 線磁通把頻率往下調。"),
         ("③ 頻率配置", "Q2 留在 sweet spot（5.10 GHz），避開同頻、0→1 撞 1→2（±283 MHz）、雙光子（±141 MHz）禁區。"),
         ("④ XY 寫入", "頻率錯開，對準 f₀₁ 的脈衝才不會串擾到鄰居。"),
         ("⑤ CZ 閘", "把 Q3 推到 f_Q2 − α，|11⟩ 繞一圈多一個 −1 相位。"),
         ("⑥ 自由實驗", "自己拖三條 Z 線，製造或消除碰撞。")],
        "這是第 6 章的案例，把前面五章串起來：三顆可調 transmon 排成一列。剛做好時頻率散亂，"
        "用 SQUID 加 Z 線磁通把頻率調開，給每顆位元一個地址；XY 寫入時頻率錯開才不會串擾；"
        "最後 CZ 閘反而是刻意、短暫地拜訪碰撞點，這就是第 16 頁說的「用到 |2⟩ 能階」。"))
    out.append(two_image_slide(
        prs, "振幅長條：糾纏、Grover 與 Deutsch",
        ["ch7_bell", "ch7_grover"],
        ["步驟 ①：兩顆都做 H，四個振幅都是 +½", "步驟 ④：擴散後答案 10 的振幅放大到 1"],
        ["grover", "deutsch", "deutsch-lab"],
        [("① 糾纏", "CZ 只把 |11⟩ 翻成負號，a₀₀·a₁₁ ≠ a₀₁·a₁₀，就拆不回兩顆各自的狀態。"),
         ("②–⑤ Grover", "Oracle 把答案的振幅翻負，擴散「對平均值翻轉」，四選一只查詢一次就找到 10。"),
         ("⑥ 轉過頭", "多做一次 Oracle＋擴散，振幅又回到各 25%。"),
         ("⑦ Deutsch", "黑盒子只問一次，就判斷 f 是常數還是平衡。"),
         ("⑧ 自由實驗", "自己送閘，或抽一個隱藏黑盒子來猜。")],
        "第 7 章用長條的高度表示振幅，負的是紅色。先看 CZ 怎麼只靠一個負號產生糾纏，"
        "再看兩位元 Grover：Oracle 標記答案、擴散對平均值翻轉，一次就把答案的機率推到 100%。"
        "最後是 Deutsch 演算法；量子金魚 008 簡報有更完整的 Deutsch 案例。",
        pill_labels=["▶ 3D 第 7 章：振幅長條", "▶ 直接看 Deutsch", "▶ Deutsch 自由實驗"]))
    out.append(two_image_slide(
        prs, "Shor 演算法：用 QFT 找週期，分解 15",
        ["ch8_comb", "ch8_qft"],
        ["步驟 ④：量測工作暫存器後只剩一把「梳子」", "步驟 ⑤：QFT 把梳子變成間隔 4 的尖峰"],
        ["shor"],
        [("① 古典歸約", "分解 N = 15 → 找 f(x) = 7ˣ mod 15 的週期 r。"),
         ("② 均勻疊加", "4 顆計數位元，16 個 x 同時存在。"),
         ("③ 模指數", "一次算出所有 f(x)，兩組暫存器產生糾纏。"),
         ("④ 梳子", "f(x) = 4 時只剩 x = 2、6、10、14。"),
         ("⑤ QFT", "間隔 r 的梳子 → 間隔 Q/r = 4 的尖峰。"),
         ("⑥–⑦ 量測與後處理", "量到 0、4、8、12；連分數找 r = 4，gcd(7² ± 1, 15) = 3、5。"),
         ("⑧ 自由實驗", "換 N（15、21）、a 與計數位元數。")],
        "第 8 章走完 Shor 演算法：量子電腦只負責找週期，前後都是古典計算。"
        "重點畫面是第 4、5 步：糾纏讓計數暫存器只剩一把間隔 r 的梳子，QFT 再把它變成間隔 Q/r 的尖峰，"
        "量測後用連分數就能求出 r，進而用 gcd 分解 15。"))
    out.append(two_image_slide(
        prs, "BV：3 顆位元一次猜中密碼",
        ["ch9_bv_query", "ch9_bv_measure"],
        ["步驟 ③：查詢一次，s·x 為奇數的項翻成負號", "步驟 ⑤：再做 H 後干涉，量到的就是 s = 101"],
        ["bv"],
        [("① 題目", "黑盒子藏 3 位元密碼 s，只回答 s·x 的奇偶；古典要問 3 次（n 位元問 n 次）。"),
         ("② 均勻疊加", "三顆都做 H，8 個 x 同時存在。"),
         ("③ 查詢一次", "|x⟩ → (−1)^(s·x)|x⟩，答案寫進正負號。"),
         ("④ 干涉", "再做一次 H，除了 |s⟩ 以外全部抵消。"),
         ("⑤ 量測", "一次查詢就拿到完整密碼。"),
         ("⑥ 真實硬體", "6 個 H（20–50 ns）＋虛擬 Z，約 100 ns，遠短於 T₁；讀取約 1 μs 後主動重設。"),
         ("⑦–⑧", "教科書版用輔助位元與 phase kickback；自由實驗可換密碼、和古典比賽。")],
        "第 9 章是一個完整的基本操作案例：用 3 顆位元跑 Bernstein–Vazirani 演算法。"
        "會用到前面所有的操作：XY 線的 H 閘、虛擬 Z、色散讀取與重設。重點是第 3、4 步："
        "黑盒子只查詢一次，就把密碼寫進每一項的正負號，再用 H 讓正負號干涉，只剩 |s⟩ 這一項。"))
    out.append(two_image_slide(
        prs, "量子錯誤更正：表面碼",
        ["ch10_surface_layout", "ch10_surface_error"],
        ["步驟 ①：d = 3，9 顆資料位元＋8 顆量測位元", "步驟 ③：D5 的 X 錯誤讓兩個 Z 穩定子亮起"],
        ["surface"],
        [("① 結構", "17 顆實體位元存 1 顆邏輯位元：資訊分散在糾纏態裡，不是複製。"),
         ("② 一個週期", "約 1 μs：量測位元與鄰居做 CZ，再讀出穩定子的奇偶。"),
         ("③–④ 抓錯", "Z 穩定子抓 X 錯誤、X 穩定子抓 Z 錯誤；Y 錯誤兩種都亮。"),
         ("⑤ 邊界", "落單的亮點配到邊界上。"),
         ("⑥ 邏輯錯誤", "d = 3 只能修 1 個錯；兩個錯誤可能騙過解碼器。"),
         ("⑦ 碼距與閾值", "d = 5、7 需 49、97 顆（2d² − 1）；實體錯誤率低於約 1% 時，碼距越大越可靠。"),
         ("⑧ 自由實驗", "點位元注入錯誤、解碼、跑統計。")],
        "第 10 章是量子錯誤更正。表面碼不直接量資料位元，而是量相鄰位元的奇偶（穩定子），"
        "所以不會破壞疊加。錯誤會讓附近的穩定子亮起來，解碼器把亮點兩兩配對，推回錯誤的位置。"
        "碼距越大能修的錯越多，但前提是實體錯誤率要低於閾值。"))
    out.append(two_image_slide(
        prs, "Lattice surgery 與魔術態蒸餾",
        ["ch11_merge", "ch11_distill"],
        ["步驟 ②：打開接縫，量出 X_A ⊗ X_B", "步驟 ⑥：15 顆髒魔術態蒸餾出 1 顆乾淨的"],
        ["surgery"],
        [("① 為什麼", "表面碼負責「存」；Eastin–Knill 定理說不能所有邏輯閘都靠橫向閘完成。"),
         ("②–③ 合併與拆開", "不移動位元，只改量哪些穩定子：縫合兩塊補丁量出聯合奇偶，再拆開。"),
         ("④ 邏輯 CNOT", "一塊輔助補丁＋三次聯合量測。"),
         ("⑤ T 閘", "消耗一顆魔術態，用閘傳送做出 T。"),
         ("⑥–⑦ 蒸餾", "15-to-1：錯誤率 p → 35p³；10⁻³ 兩輪後約 10⁻²¹，足夠跑 Shor。"),
         ("⑧ 自由實驗", "自己縫合、拆開、蒸餾。")],
        "第 11 章接著第 10 章：表面碼只負責把資訊存好，要計算還得做邏輯閘。"
        "Clifford 閘用 lattice surgery——把兩塊補丁縫在一起量出聯合奇偶、再拆開；"
        "真正帶來量子優勢的 T 閘，則要消耗事先蒸餾好的魔術態。蒸餾的錯誤率是三次方下降，一到兩輪就夠。"))
    out.append(two_image_slide(
        prs, "編譯與控制軟體堆疊",
        ["ch12_route", "ch12_pulse"],
        ["步驟 ④：直線晶片上不相鄰就插 SWAP", "步驟 ⑥：排程後每條線的奈秒時間軸"],
        ["stack"],
        [("① 全貌", "七層：從一行演算法，一路翻成某條同軸線上、某個奈秒的微波波形。"),
         ("② 分解", "H、CNOT 換成原生閘：Rz、√X、CZ。"),
         ("③ 映射", "依今天的校準資料，挑相鄰、錯誤率最低的實體位元。"),
         ("④ 路由", "不相鄰就插 SWAP（每個 SWAP = 3 個 CZ）。"),
         ("⑤ 最佳化", "H·H 抵消、合併 Rz、虛擬 Z（0 ns）。"),
         ("⑥ 排程與脈衝", "ASAP 並行，但相鄰 CZ 不能同時做（頻率碰撞）。"),
         ("⑦–⑧ 回饋與校準", "FPGA 幾百 ns 內完成量測回饋；參數會漂移，要依依賴圖定期重新校準。")],
        "最後一章跟著一個電路走完整條軟體堆疊。動畫裡的編譯器是真的在跑："
        "分解成原生閘、依校準資料映射到實體位元、插 SWAP 路由、最佳化、排程成脈衝，再模擬出結果。"
        "這也是第 16 頁「控制與讀取」在系統層級的樣子。"))
    return out


def move_before_last(prs, new_slides):
    ids = prs.slides._sldIdLst
    items = list(ids)
    n_new = len(new_slides)
    added = items[-n_new:]
    last_old = items[-n_new - 1]
    for el in added:
        ids.remove(el)
    pos = list(ids).index(last_old)
    for k, el in enumerate(added):
        ids.insert(pos + k, el)


def main():
    global _SLDNUM
    prs = Presentation(BASE)
    for sh in list(prs.slides)[1].shapes:
        if sh.name.startswith("Slide Number"):
            _SLDNUM = sh._element
    add_existing_buttons(prs)
    link_summary(prs)
    new = build_new(prs)
    move_before_last(prs, new)
    prs.save(PPTX)
    print("saved", PPTX, "slides:", len(prs.slides))


if __name__ == "__main__":
    main()
