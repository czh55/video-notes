#!/usr/bin/env python3
"""b62r：生成 google-maps-predict-traffic 图文实录 HTML（可复跑）。"""
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
SLUG = "google-maps-predict-traffic"
KEY = "b62r"

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
    n = 0
    for i, seg in enumerate(whisper.get("segments", [])):
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        n += 1
        text = to_simplified(text)
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

    title = "Google地图为什么能提前知道前面堵车？"
    url = "https://xhslink.cn/o/4IB76GeYLwk"
    duration = "2分39秒"
    intro = (
        "「摩摩」用低多边形公路动画讲解 Google 地图路况：开场英文点明地图能提前看见前方堵车，"
        "关键不是路边传感器，而是手机匿名上报位置与速度。"
        "成百上千部手机的数据汇总后估计路段速度；相对常态从约 65 mph 掉到 15 mph，就是强烈拥堵信号。"
        "系统并不只信原始 GPS——高楼、高架、路口会让定位散乱，还要用方向、速度与道路形状对齐。"
        "最后用多设备聚合、对照时段常态，并把通行时间写成路网边权：更短的公里数也可能更慢。"
        "Whisper 在 57 秒后为空，后半段以画面英文字幕与 UI 数字为准。"
    )
    summary_rows = [
        ("00:00→00:30", "传感原理", "手机即路况传感器；画面标「no road sensor」，15 mph 对比 usual 65。"),
        ("00:30→00:52", "众包估速", "百多台手机位置更新汇总到路段；常态 65mph 突降至 15mph = 强信号。"),
        ("00:52→01:25", "GPS 对齐", "不只信 GPS；raw fixes 会偏，需 position / direction / speed / road shape。"),
        ("01:25→02:39", "时间边权", "多机聚合优于单机；对照 usual for this hour；最短 5.4km·9min vs 最快 7.3km·8min。"),
    ]
    takeaway = (
        "路况来自手机众包速度相对历史常态的偏离；"
        "原始 GPS 必须先对齐道路，再用时间边权选「最快」而非「最短」。"
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
<section class="story-section" id="ch-sensor">
  <h2><span class="time-marker">00:00–00:30</span>手机即路况传感器：不用路侧设备也能看见前方拥堵</h2>
  <p>开场英文口播直接抛出命题：<span class="quote">「Google maps can see a traffic jam miles ahead of you」</span>——地图能在你前方数英里外就看见堵车。动画里拥堵车道上方密布蓝色定位点，速度条写着 <strong>15 mph</strong>，旁边灰色小字是 <strong>usual 65</strong>；路缘用绿/橙/红标出通畅与拥堵段落。</p>
  <p>画面随即点破常见误解：桥架上没有路边感应器，标注写着「no road sensor」。真正在报数的，是车里开着定位服务的手机——哪怕只是「One phone slowing down」，系统也开始把实时速度与常态对照。视频未交代具体隐私协议细节，只演示「手机 = 匿名路况传感器」这一机制。</p>
  {figs(1)}
</section>

<section class="story-section" id="ch-crowd">
  <h2><span class="time-marker">00:30–00:52</span>众包估速：常态 65mph 突然掉到 15mph 就是强烈信号</h2>
  <p>镜头拉到车流更密的弯道，字幕接「But now, imagine hundreds」。口播（繁体转简）说：想象有百多台手机在同一条路上行动；Google 可以把这些位置更新的数据集中到某条路的部分，并估计每一条路段的速度。</p>
  <p>判断拥堵靠的是对比，不是绝对数字：如果车辆通常以约 65 mph 通过，却突然有大量设备以约 15 mph 移动——口播称「那是很强烈的信号，因为车速慢了」。Whisper 把「手机/设备」听成「机器」，结合蓝色定位球与英文字幕 large cluster，正文按设备集群理解。笔记文案里也有类似例子（高速从约 100 km/h 掉到 20 km/h），与动画用的 mph 演示同属「相对常态的骤降」。</p>
  {figs(2, 3)}
</section>

<section class="story-section" id="ch-gps">
  <h2><span class="time-marker">00:52–01:25</span>不只信原始 GPS：先对齐道路，再谈速度可信</h2>
  <p>口播强调：Google 并不只相信 GPS 数据。俯视图上标出「raw GPS fixes」——蓝圈散落在车道各处，并不整齐地落在你真正行驶的那条线上。随后画面列出误差场景：高楼旁边、高架桥下、复杂路口（beside tall buildings / under the overpass / at the junction）。</p>
  <p>要对齐道路，系统会同时看 <strong>position、direction、speed、road shape</strong>：位置点、行驶方向、瞬时速度，以及道路几何形状。Whisper 末句「GPS 的位置可以变得更快」语义残缺，疑为误听；本段不以该句作定量结论，而以画面标签与笔记文案「GPS 不准，要先找对路」为准。</p>
  {figs(4, 5)}
</section>

<section class="story-section" id="ch-route">
  <h2><span class="time-marker">01:25–02:39</span>多设备聚合、对照历史、给边加权：最短路不一定最快</h2>
  <p>本段 Whisper 为空，叙述完全依据画面 UI。先对比单机与集群：一辆车单独报 30 mph，31 部手机聚合后显示约 63 mph live——「from many devices, instead」。再把 live 速度和「usual for this hour」对照；时钟停在 17:30 一类高峰示意，说明系统会问：现在慢，是相对这个时段的常态慢，还是真异常。</p>
  <p>估速之后进入路网：边（edge）按通行时间加权，而不是只按公里数。示意图给出 <strong>shortest 5.4 km · 9 min</strong> 与 <strong>fastest 7.3 km · 8 min</strong>——更短那条反而更慢；另一帧用「9 min city streets / 10 min highway」和标红的 3 分钟贵价路段，解释为什么地图会绕开看起来近、实际堵的边。收束回到拥堵可视化：提前知道堵车，是为了用时间边权重算「最快到达」。</p>
  {figs(6)}
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
.story-section .quote{{color:#57534e;font-style:italic}}
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
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span><span class="meta-tag tag-duration">{duration}</span><span class="meta-tag tag-topic">地图 路况 众包 GPS 导航</span></div>
<a class="source-link" href="{url}" target="_blank" rel="noopener">→ 原视频链接</a></header>
<nav class="toc"><h3>内容导航</h3>
<a href="#ch-sensor">手机即路况传感器：不用路侧设备也能看见前方拥堵</a>
<a href="#ch-crowd">众包估速：常态 65mph 突然掉到 15mph 就是强烈信号</a>
<a href="#ch-gps">不只信原始 GPS：先对齐道路，再谈速度可信</a>
<a href="#ch-route">多设备聚合、对照历史、给边加权：最短路不一定最快</a>
<a href="#transcript">完整转录</a></nav>
<article class="documentary"><div class="content-points"><h2>内容要点</h2><p>{esc(intro)}</p><h3>知识结构</h3>
{summary_html}
<div class="takeaway-box"><strong>总结</strong><p>{esc(takeaway)}</p></div></div>
{chapters_html}
<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>完整转录（{n_seg}段）</summary>
<div class="transcript-body"><p class="transcript-note">以下文本由 Whisper medium 模型自动转录（已转简体）。00:03–00:30 与 00:57 之后口播识别为空，章节叙述主要依据画面英文 UI/字幕；「机器」等词可能为识别误差，详见章节说明。</p>
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
