#!/usr/bin/env python3
"""b62n：生成 espresso-crema-thickness-myth 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "espresso-crema-thickness-myth"
KEY = "b62n"


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
    n = 0
    for seg in whisper.get("segments", []):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        n += 1
        rows.append(
            f'<li class="transcript-row" id="transcript-{n}">'
            f'<time datetime="PT{int(seg["start"])}S">{fmt(seg["start"])}</time>'
            f"<p>{esc(text)}</p></li>"
        )
    return "\n".join(rows), n


def main() -> None:
    shots = json.loads((ROOT / f"shots-{SLUG}.json").read_text(encoding="utf-8"))["shots"]
    by_num = {int(s["file"].replace("shot-", "").replace(".jpg", "")): s for s in shots}
    transcript, n_seg = build_transcript()

    title = "浓缩的油脂越厚，就越好喝吗？"
    url = "https://xhslink.cn/o/3ia9NIz5I2O"
    duration = "2分24秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」用一杯「金黄油脂厚得像奶盖、喝起来却又苦又糙」的浓缩开场，"
        "追问杯面那一层到底是咖啡精华还是泡沫。"
        "视频把口语里的「油脂」正名为 crema（咖啡泡沫）：体积主要由气泡撑起，气体多来自烘焙残留的二氧化碳；"
        "泡沫厚首先说明能起泡，不能换算成萃出了更多精华。"
        "同一包豆排气后泡沫变薄、罗布斯塔往往比阿拉比卡更易起泡、双层增压粉碗也会改观感——"
        "最后建议先轻轻搅匀再尝整杯，把泡沫当观察线索。下列实录按时间线展开；观点均标注为作者口播与画面。"
    )
    summary_rows = [
        ("00:00→00:15", "开场反差", "厚得像奶盖却苦又糙；先问清这一层是精华还是泡沫。"),
        ("00:15→00:56", "正名与机制", "所谓油脂=crema；气泡来自豆内二氧化碳，流出粉碗后减压冒泡。"),
        ("00:56→01:20", "厚度边界", "泡沫多=比较能起泡≠更多精华；排气变薄≠变难喝。"),
        ("01:20→01:47", "豆种与粉碗", "罗布斯塔泡沫更多但脂肪未必更高；增压粉碗会「造」泡沫观感。"),
        ("01:47→02:24", "怎么喝", "泡沫有用但非越多越好；搅匀后看酸苦、杂味与余味。"),
    ]
    takeaway = (
        "别用 crema 厚度给浓缩打分。"
        "把它当气体与起泡能力的线索，先搅匀再以整杯味道判断；薄了也不必急着追更厚。"
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

    chapters_html = f"""
<section class="story-section" id="ch1">
  <h2><span class="time-marker">00:00–00:15</span>开场：厚得像奶盖，却又苦又糙</h2>
  <p>视频先摆出感官冲突：这杯浓缩金黄的「油脂」厚得像奶盖，喝起来却又苦又糙。大字把观众直觉压成一个问题——你追求的这一层，到底是咖啡精华还是泡沫？</p>
  <p>镜头立刻补上动态证据：刚接出来的浓缩表面会冒出细小泡泡；放一会儿，这层东西又慢慢变薄。反差与变化一起，把「厚度=好喝」的默认等式先拆开。</p>
  {figs(1)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:15–00:56</span>正名：油脂实际是 crema；体积靠气泡</h2>
  <p>作者纠名：习惯叫的油脂，实际是一层咖啡泡沫，叫 crema。里面有咖啡液、油脂和其他咖啡成分，但撑起这一层体积的是许多细小气泡。气泡主要来自咖啡豆里的二氧化碳——烘焙时产生、一部分留在豆子内部。</p>
  <p>萃取时，热水在压力下穿过咖啡粉，把这些气体带进咖啡液；液体流出粉碗后压力降低，溶在里面的气体冒出来形成细小泡泡，有点像汽水开瓶。咖啡中的一些成分又能帮气泡维持一阵，于是杯面留下金棕色一层；气泡逐渐破裂，泡沫也就慢慢变薄。</p>
  {figs(2, 3)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">00:56–01:20</span>泡沫多≠精华多；排气会让同一包豆变薄</h2>
  <p>机制讲完后，作者收紧结论：「泡沫多，首先说明这杯比较能起泡，不能直接换算成萃出了更多精华。」顺着同一条气体逻辑再看日常现象：为什么同一包豆前几天泡沫很厚，后来却薄了？</p>
  <p>豆子放着会慢慢排气。其他条件接近时，留下的气体少了，萃取时能冒出来的泡泡也可能变少。因此泡沫变薄，不能就此断定咖啡变难喝；反过来，刚烘好时泡沫很多，也不代表此时最适合喝。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">01:20–01:47</span>豆种与粉碗：厚度和含油量不是一回事</h2>
  <p>作者接着问：换一种含油更多的豆，泡沫会不会就更厚？画面给出研究对照叙事——阿拉比卡与罗布斯塔相比，罗布斯塔做出的泡沫更多，但阿拉比卡的脂肪含量反而更高。这说明这层「油脂」的厚度，和真正含了多少油并不是一回事。</p>
  <p>就算同一包豆，粉碗结构也可能让泡沫看起来不同。有些家用机的双层增压粉碗会利用出口结构增加阻力，让咖啡更容易形成泡沫。泡沫好看，豆子的风味和萃取结果还是得另外判断。</p>
  {figs(5, 6)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">01:47–02:24</span>有用但非越多越好：搅匀后再给整杯下结论</h2>
  <p>那这层泡沫对喝咖啡有没有用？作者答：有，它会影响香气释放和入口感受，但作用不是越多越好。作者转述：研究里把泡沫做得更多，并没有让好闻的香气继续增加（视频未给出具体文献名，作观点/转述理解）。</p>
  <p>在家判断时，可以先轻轻搅匀再尝，让上面的泡沫和下面的咖啡液混在一起；看入口酸苦是否协调、有没有明显杂味、咽下去以后余味舒不舒服。别只尝到最上面一口就给整杯下结论。收束句很干脆：泡沫厚，不会把一杯难喝的浓缩变成好咖啡；泡沫薄，也不用急着追求更厚——把它当观察线索，最后用整杯的味道判断。片尾互动：「你有没有喝过泡沫特别漂亮、入口却让你失望的浓缩？」</p>
</section>
"""

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    toc = "".join(
        f'<a href="#{cid}">{title}</a>'
        for cid, title in [
            ("ch1", "开场反差：厚≠好喝"),
            ("ch2", "正名：油脂=crema"),
            ("ch3", "泡沫多≠精华多"),
            ("ch4", "豆种与增压粉碗"),
            ("ch5", "搅匀再判断"),
            ("transcript", "完整转录"),
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{esc(intro[:140])}">
<title>{esc(title)}｜图文实录</title>
<style>
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.container{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}
header h1{{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}}
.meta-row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.meta-tag{{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
.tag-platform{{background:#ff2442;color:#fff}}.tag-duration{{background:#f1f5f9;color:#64748b}}.tag-topic{{background:#dbeafe;color:#1e40af}}
.source-link{{color:#3b82f6;font-size:14px;text-decoration:none}}.source-link:hover{{text-decoration:underline}}
.toc{{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.toc h3{{font-size:16px;color:#1e40af;margin:0 0 12px}}
.toc a{{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}}
.toc a:hover{{color:#3b82f6}}
.documentary{{font-size:17px}}.story-section{{margin:48px 0}}
.story-section h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.story-section p{{margin:0 0 14px;color:#44403c}}
.time-marker{{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}}
img{{display:block;max-width:100%;height:auto}}
figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}
.transcript-section{{margin-top:48px}}
.transcript-note{{font-size:14px;color:#78716c;margin-bottom:24px}}
.transcript-list{{list-style:none;padding:0;margin:0}}
.transcript-row{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.transcript-row time{{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}}
.transcript-row p{{margin:0}}
.transcript-collapsible{{border:none;margin:0;padding:0}}
.transcript-collapsible summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{{display:none}}
.transcript-collapsible summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}}
.transcript-collapsible[open] summary::before{{transform:rotate(90deg)}}
.transcript-collapsible[open] summary{{margin-bottom:16px}}
.summary-row{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.summary-row .time-marker{{flex-shrink:0;margin-top:2px}}
.summary-row strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.summary-row p{{color:#57534e;margin:0;font-size:15px}}
.takeaway-box{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.takeaway-box strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.takeaway-box p{{color:#3b82f6;margin:0;font-size:15px}}
.content-points h2{{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.content-points h3{{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}}
@media(max-width:640px){{.container{{padding:28px 18px 56px}}header h1{{font-size:24px}}.transcript-row{{grid-template-columns:56px 1fr;gap:10px}}}}
</style>
</head>
<body>
<main class="container">
<header>
  <h1>{esc(title)}</h1>
  <div class="meta-row">
    <span class="meta-tag tag-platform">小红书</span>
    <span class="meta-tag tag-duration">{duration}</span>
    <span class="meta-tag tag-topic">意式浓缩 · Crema · 泡沫厚度</span>
  </div>
  <p style="color:#57534e;font-size:14px;margin:0 0 12px">作者 甄茶笔记&amp;大喜 · 2026-10-13</p>
  <a class="source-link" href="{url}" target="_blank" rel="noopener">→ 原视频链接</a>
</header>
<nav class="toc"><h3>内容导航</h3>{toc}</nav>
<article class="documentary">
  <div class="content-points">
    <h2>内容要点</h2>
    <p>{esc(intro)}</p>
    <h3>知识结构</h3>
    {summary_html}
    <div class="takeaway-box"><strong>总结</strong><p>{esc(takeaway)}</p></div>
  </div>
  {chapters_html}
  <section class="transcript-section" id="transcript">
    <details class="transcript-collapsible">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div class="transcript-body">
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按画面与语境校正（如「含油更多的豆」、crema 正名），转录区保持原样以便核对。</p>
        <ol class="transcript-list">
{transcript}
        </ol>
      </div>
    </details>
  </section>
</article>
</main>
<script>(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body>
</html>
"""
    out = DOCS / f"{SLUG}-图文实录.html"
    out.write_text(html, encoding="utf-8")
    print(f"Generated: {out} segments={n_seg}")


if __name__ == "__main__":
    main()
