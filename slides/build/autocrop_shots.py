# -*- coding: utf-8 -*-
"""把 3D 截圖四周的空白深色背景裁掉（第 9–12 章整頁擷取後使用）。

擷取後執行一次即可（重複執行會再裁一次）：
    node slides/capture_3d_transmon.js 9-12
    python3 slides/build/autocrop_shots.py slides/figures/3d_transmon/ch9_*.jpg slides/figures/3d_transmon/ch1[0-2]_*.jpg
"""
import sys

from PIL import Image, ImageChops

PAD = 24          # 內容外保留的邊距（px）
TOP_KEEP = 0      # 左上角字幕也保留
# 自動裁切後再依比例裁一次（左, 上, 右, 下）：第 11 章同一畫面裡有兩組場景，只留主角
EXTRA = {"ch11_merge": (0, 0, 0.56, 1), "ch11_distill": (0.07, 0, 1, 1)}


def autocrop(path):
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((im.width - 2, im.height // 2)))
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 28 else 0)
    box = diff.getbbox()
    if not box:
        return
    l, t, r, b = box
    l, t = max(0, l - PAD), max(TOP_KEEP, t - PAD)
    r, b = min(im.width, r + PAD), min(im.height, b + PAD)
    im = im.crop((l, t, r, b))
    key = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    if key in EXTRA:
        fl, ft, fr, fb = EXTRA[key]
        w, h = im.size
        im = im.crop((int(w * fl), int(h * ft), int(w * fr), int(h * fb)))
    im.save(path, quality=88)
    print(f"{path}: {im.size} -> {(r - l, b - t)}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        autocrop(p)
