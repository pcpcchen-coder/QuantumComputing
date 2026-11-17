# -*- coding: utf-8 -*-
"""把所有 .pptx 裡指向 animations/ 的相對路徑連結，改成 GitHub Pages 網址。

  ../animations/index.html#bloch
  ../../animations/transmon-3d.html#deutsch
→ https://pcpcchen-coder.github.io/QuantumComputing/animations/index.html#bloch

只改超連結目標（.rels 的 Target）與投影片／備忘稿文字裡出現的相對路徑，其餘內容原封不動。
可重複執行。各簡報的產生器也已改用同一個網址，重新產生簡報時結果一致。

用法（在 repo 根目錄）：python3 slides/build/use_pages_links.py [檔案.pptx ...]
不給檔名時處理 slides/ 與 academy/ 下所有 .pptx（略過 slides/build/）。
"""
import glob
import os
import re
import shutil
import sys
import tempfile
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PAGES_ANIM = "https://pcpcchen-coder.github.io/QuantumComputing/animations/"
REL = re.compile(r"(?:\.\./)+animations/")


def convert(path):
    changed = 0
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx", dir=os.path.dirname(path))
    tmp.close()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            name = item.filename
            if name.endswith(".rels") or (name.startswith(("ppt/slides/", "ppt/notesSlides/")) and name.endswith(".xml")):
                text = data.decode("utf-8")
                new, n = REL.subn(PAGES_ANIM, text)
                if name.endswith(".rels") and n:
                    # 網址一定是外部連結
                    new = re.sub(r'(<Relationship\b[^>]*Target="' + re.escape(PAGES_ANIM) + r'[^"]*")(?![^>]*TargetMode=)',
                                 r'\1 TargetMode="External"', new)
                if n:
                    changed += n
                    data = new.encode("utf-8")
            zout.writestr(item, data)
    if changed:
        shutil.move(tmp.name, path)
    else:
        os.unlink(tmp.name)
    return changed


def main():
    files = sys.argv[1:] or sorted(
        p for p in glob.glob(os.path.join(ROOT, "**", "*.pptx"), recursive=True)
        if "/node_modules/" not in p and "/slides/build/" not in p and "/.git/" not in p)
    for f in files:
        n = convert(f)
        print(f"{n:4d}  {os.path.relpath(f, ROOT)}")


if __name__ == "__main__":
    main()
