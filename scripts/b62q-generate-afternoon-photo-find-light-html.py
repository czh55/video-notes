#!/usr/bin/env python3
"""b62q：生成 afternoon-photo-find-light 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

try:
    import opencc

    _T2S = opencc.OpenCC("t2s")
except ImportError:
    _T2S = None

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "afternoon-photo-find-light"
KEY = "b62q"


def to_simplified(s: str) -> str:
    if _T2S:
        return _T2S.convert(s)
    return s


def fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_transcript() -> tuple[str, int]:
    whisper = json.loads((ROOT / f"{KEY}.json").read_text(encoding="utf-8"))
    rows = []
    for i, seg in enumerate(whisper.get("segments", []), 1):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        text = to_simplified(text)
        rows.append(
            f'<li class="transcript-row" id="transcript-{i}">'
            f'<time datetime="PT{int(seg["start"])}S">{fmt(seg["start"])}</time>'
            f"<p>{esc(text)}</p></li>"
        )
    return "\n".join(rows), len(rows)


def main() -> None:
    shots = json.loads((ROOT / f"shots-{SLUG}.json").read_text(encoding="utf-8"))["shots"]
    by_num = {int(s["file"].replace("shot-", "").replace(".jpg", "")): s for s in shots}
    transcript, n_seg = build_transcript()

    title = "下午拍照怎么找光线"
    url = "https://xhslink.cn/o/8itigYhyWET"
    duration = "1分27秒"
    intro = (
        "「跟着冬玖学摄影」用街边红砖墙人像演示：下午直射侧光容易把脸切成一半亮一半暗、"
        "留下三角光斑，甚至让模特眯眼——这是要避开的硬光。"
        "相对好看的光是议题，但把太阳拍进画面的完全逆光同样不推荐；"
        "对策是挡光源，或贴墙进入建筑阴影主动找光。"
        "Whisper 仅捕获两句碎片口播，下列叙述以画面字幕与操作演示为主。"
    )
    summary_rows = [
        ("00:00→00:30", "避坑演示", "硬侧光：半边脸亮、三角光斑、模特睁不开眼——标为要避免的光线。"),
        ("00:30→01:00", "判断标准", "看明暗「硬边缘」；相对好看的光 vs 完全逆光（太阳入画）也不推荐。"),
        ("01:00→01:27", "找光动作", "先挡太阳光源；挡不住就贴墙进阴影，等于避开直射。"),
    ]
    takeaway = (
        "下午拍照先判光质：硬侧光与完全逆光都易毁人像；"
        "用手挡或进墙影，把「找光」变成可执行的站位选择。"
    )

    def figs(*nums: int) -> str:
        out = []
        for num in nums:
            m = by_num[num]
            cap = m.get("caption") or m.get("scene") or ""
            alt = m.get("alt") or cap
            out.append(
                f'<figure><img src="assets/{SLUG}/{m["file"]}" alt="{esc(alt)}" loading="lazy">'
                f"<figcaption>[{m['time']}] {esc(cap)}</figcaption></figure>"
            )
        return "\n".join(out)

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    chapters_html = f"""
<section class="story-section" id="ch-hard">
  <h2><span class="time-marker">00:00–00:30</span>硬侧光：半边脸亮、三角光斑与眯眼</h2>
  <p>开场字幕直接提醒「拍照的时候切记哈」。模特靠在红砖墙前，下午太阳从侧面打过来：一边脸高光刺眼，另一边沉进阴影——字幕写「他一半脸亮」，并点明这是「要避免的一个光线」。</p>
  <p>接着演示更糟的结果：模特被直射光逼得「都睁不开眼睛」。讲解者用手指点向脸颊，字幕强调「这边脸上有一个三角形的光斑」——硬侧光不仅对比大，还会在脸上留下形状怪异的高光块。口播碎片里也说到「这种光线不要拍」，与画面一致。</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch-edge">
  <h2><span class="time-marker">00:30–01:00</span>硬光边缘、相对好看的光与完全逆光</h2>
  <p>中段继续盯着明暗交界：手指比出「你看它这个边缘」。Whisper 只听清「比较硬的一个一个」，结合画面可理解为在说光「硬」、过渡不柔。作者抛出问题「我们什么光线是最好的呢」，并给出相对表述——「光线是相对来讲最好看的」——视频未展开参数公式，重点仍是对照坏光。</p>
  <p>机位拉开到街景后，太阳落到模特脑后：轮廓发亮、脸部偏暗、眩光明显。字幕明确：「像这种完全的逆光也不推荐」「因为如果你把太阳拍进去了」。也就是说，下午找光不等于追逆光剪影；把太阳本身拍进画面，往往让人像更难成立。</p>
  {figs(3)}
</section>

<section class="story-section" id="ch-fix">
  <h2><span class="time-marker">01:00–01:27</span>挡光源，或贴墙进阴影避开直射</h2>
  <p>对策先给「挡」：用手或其他遮挡把「太阳这个光源给挡住」。若现场没法挡，字幕追问「如果你没法挡光源怎么办呢」——随即让模特贴着红砖墙，站进建筑投下的阴影里：街面仍是强光，人物却离开了直射区。字幕收束：「这不就把这个光源给避开了吗」「也是比较好看的」。</p>
  <p>片尾字幕只剩半句「我们应该去找」——结合整条视频，意思是主动去找合适的光位（阴影、遮挡后的柔光），而不是站在最刺眼的直射里硬拍。本段 Whisper 为空，步骤完全来自字幕与站位变化。</p>
  {figs(4)}
</section>
"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{esc(intro)}">
<title>{esc(title)}｜图文实录</title>
<style>*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.container{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}header{{margin-bottom:40px}}
header h1{{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}}
.meta-row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.meta-tag{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
.tag-platform{{background:#ff2442;color:#fff}}.tag-duration{{background:#f1f5f9;color:#64748b}}.tag-topic{{background:#dbeafe;color:#1e40af}}
.source-link{{color:#3b82f6;font-size:14px;text-decoration:none}}.source-link:hover{{text-decoration:underline}}
.toc{{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.toc h3{{font-size:16px;color:#1e40af;margin:0 0 12px}}.toc a{{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}}.toc a:hover{{color:#3b82f6}}
.documentary{{font-size:17px}}.story-section{{margin:48px 0}}
.story-section h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.story-section p{{margin:0 0 14px;color:#44403c}}
.time-marker{{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}}
img{{display:block;max-width:100%;height:auto}}figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}
.transcript-section{{margin-top:48px}}.transcript-section h2{{font-size:24px;font-weight:700;color:#1c1917}}
.transcript-note{{font-size:14px;color:#78716c;margin-bottom:24px}}.transcript-list{{list-style:none;padding:0}}
.transcript-row{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.transcript-row time{{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}}.transcript-row p{{margin:0}}
@media(max-width:640px){{.container{{padding:28px 18px 56px}}header h1{{font-size:24px}}.transcript-row{{grid-template-columns:56px 1fr;gap:10px}}}}
.transcript-collapsible{{border:none;margin:0;padding:0}}.transcript-collapsible summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{{display:none}}
.transcript-collapsible summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}}
.transcript-collapsible[open] summary::before{{transform:rotate(90deg)}}.transcript-collapsible[open] summary{{margin-bottom:16px}}.transcript-collapsible .transcript-body{{margin-top:0}}
.summary-row{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.summary-row .time-marker{{flex-shrink:0;margin-top:2px}}
.summary-row strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.summary-row p{{color:#57534e;margin:0;font-size:15px}}
.takeaway-box{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.takeaway-box strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.takeaway-box p{{color:#3b82f6;margin:0;font-size:15px}}
.content-points h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.content-points h3{{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}}
</style>
</head>
<body><main class="container">
<header><h1>{esc(title)}</h1>
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span><span class="meta-tag tag-duration">{duration}</span><span class="meta-tag tag-topic">摄影 用光 下午光 人像 硬光</span></div>
<a class="source-link" href="{url}" target="_blank" rel="noopener">→ 原视频链接</a></header>
<nav class="toc"><h3>内容导航</h3>
<a href="#ch-hard">硬侧光：半边脸亮、三角光斑与眯眼</a>
<a href="#ch-edge">硬光边缘、相对好看的光与完全逆光</a>
<a href="#ch-find">挡光源，或贴墙进阴影避开直射</a>
<a href="#transcript">完整转录</a></nav>
<article class="documentary"><div class="content-points"><h2>内容要点</h2><p>{esc(intro)}</p><h3>知识结构</h3>
{summary_html}
<div class="takeaway-box"><strong>总结</strong><p>{esc(takeaway)}</p></div></div>
{chapters_html}
<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>完整转录（{n_seg}段）</summary>
<div class="transcript-body"><p class="transcript-note">以下文本由 Whisper medium 模型自动转录（已转简体），本片口播识别极短；章节叙述主要依据画面简体字幕与站位演示，可能与口播细节有出入。</p>
<ol class="transcript-list">
{transcript}
</ol></div></details></section>
</article>
</main>
<script>(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body></html>
"""

    out = DOCS / f"{SLUG}-图文实录.html"
    out.write_text(html, encoding="utf-8")
    print(f"Generated: {out} segments: {n_seg}")


if __name__ == "__main__":
    main()
