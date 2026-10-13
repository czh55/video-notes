#!/usr/bin/env python3
"""b62f：生成 cafe-100-cups-still-loss 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "cafe-100-cups-still-loss"
KEY = "b62f"


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

    title = "一天卖100杯，为什么还在亏钱？"
    url = "https://xhslink.cn/o/5PtNH1qUAEN"
    duration = "3分48秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」用「一天卖一百杯」开场，却不急着庆祝忙碌，"
        "而是把问题改写成：减掉变动成本以后，每杯还能留下多少钱去覆盖房租和基础人工。"
        "示意账用每月固定成本两万五千元、每杯贡献十元，算出月保本两千五百杯、日均至少八十四杯；"
        "贡献掉到八元时日均门槛约一百零五杯。随后提醒产品结构要加权、产能跨台阶会让保本线失效，"
        "并分清「保本不是赚钱」。开店前别抄别人的百杯答案，而要拆清成本、对照商圈需求与门店产能。"
        "下列实录按时间线展开；数字均为作者示意，非某一门店实测。"
    )
    summary_rows = [
        ("00:00→00:30", "忙碌≠赚钱", "一百杯只是销量标签；画面用保本线区分「看起来很忙」与真正进入利润区。"),
        ("00:30→00:57", "单杯贡献", "贡献=实际收入−变动成本；少卖一杯钱会不会跟着少，是区分变动/固定的快测。"),
        ("00:57→01:15", "人工水电要拆", "基础工资相对固定，加班临时工会跨量跳升；分不清就拆成「不开单也付」与「多一单才增」。"),
        ("01:15→01:45", "示意保本账", "25000÷10=2500杯/月≈日均84杯；贡献8元→约105杯；少留2元≈多21杯/日。"),
        ("01:45→02:15", "加权产品结构", "不能拿一杯高毛利代表全店；高贡献卖得少、低贡献外卖多，平均贡献掉、保本杯量升。"),
        ("02:15→02:50", "产能台阶", "80杯一人能做、120杯要加兼职或设备时，固定成本已跨台阶；还要问需求与高峰接单。"),
        ("02:50→03:48", "保本≠赚钱", "平衡点上营业利润约零；要利润就要抬杯量；别抄「一天一百杯」，拆成本并对照需求产能。"),
    ]
    takeaway = (
        "一天一百杯也可能亏钱。"
        "先算加权后的单杯贡献能否覆盖固定成本，再核对商圈需求与产能台阶；"
        "保本只是利润为零，不是开始赚钱。算不清就不要把希望压在开业后再卖更多。"
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
  <h2><span class="time-marker">00:00–00:30</span>开场：一天一百杯，先看保本线而不是看起来忙</h2>
  <p>视频标题卡直接抛出场景：你的咖啡店一天卖一百杯——然后立刻把「赚钱」和「亏钱」两套画面并置。作者没有用百杯销量当成功证明，而是把判断标准推到保本线：示意画面写出每月两千五百杯、折算日均大约八十四杯；并强调这条线决定的不是店里看起来有多忙，跨过它之后才真正进入利润区。</p>
  <p>这一段口播几乎没有进入 Whisper（约 00:01–00:30 为视觉讲解），但画面字幕把「销量标签≠利润」钉得很清楚。随后口播从「减掉变动成本」接上，开始定义单杯贡献。</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:30–00:57</span>单杯贡献：减掉变动成本，才谈得上覆盖房租人工</h2>
  <p>作者把「留下」说成：减掉这杯订单带来的变动成本以后，还能拿去覆盖房租、基础人工等固定支出的钱。最简单的判断方法是——如果今天少卖这一杯，这笔钱会不会跟着少。</p>
  <p>跟着少的通常进变动成本：咖啡豆、牛奶、糖浆、杯盖、纸袋，以及按订单发生的平台费用和优惠。房租、基础排班、软件和设备折旧，在当前经营规模内通常不会因为少卖一杯立刻消失，可以先放进固定成本。（Whisper 原词「电动成本」，据画面校正为「变动成本」。）</p>
  {figs(3, 4)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">00:57–01:15</span>人工和水电不能永远只贴一个标签</h2>
  <p>分完大类之后，作者立刻补刀：人工和水电不能永远只贴一个标签。基础工资可能相对固定，但加班和临时工会在订单跨过某个量以后突然增加；水电也可能同时有基础部分和随营业量变化的部分。</p>
  <p>分不清时，至少先拆成「不开单也要付」和「多一单才增加」两部分，不要把整笔费用随手塞到一边——否则后面的保本杯量会从一开始就算歪。</p>
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">01:15–01:45</span>示意账：两万五除以十元，日均至少八十四杯</h2>
  <p>回到例子：每月固定成本两万五千元，每杯平均贡献十元，两万五除以十就是每月两千五百杯；开三十天日均约八十三点三杯，实际计算至少要按八十四杯看。</p>
  <p>如果一杯实际只能留下八元，保本量变成三千一百二十五杯，日均约一百零四点二杯，至少按一百零五杯看。每杯只少留下两元，日均保本线就大约多二十一杯——价格少两元看起来不大，落到一个月可能是完全不同的客流要求。文中数字均为作者示意算例。</p>
  {figs(5, 6)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">01:45–02:15</span>产品结构一变，盈亏平衡点就要重算</h2>
  <p>咖啡店很少只卖一种产品：美式、拿铁、特调、甜点、自提和外卖，每一种订单的实际收入和变动成本都可能不同。此时不能拿菜单上某一杯的高毛利来代表全店，也不能把所有杯子都当成一样值钱。（Whisper「权电」据画面校正为「全店」。）</p>
  <p>更稳妥的做法是按真实或保守预计的销售结构，算加权后的平均贡献。高贡献产品卖得少、低贡献外卖单卖得多，整体平均贡献下降，保本杯量也会被抬高；产品结构一变，盈亏平衡点就要重算。</p>
  {figs(7)}
</section>

<section class="story-section" id="ch6">
  <h2><span class="time-marker">02:15–02:50</span>纸面答案的前提：产能跨台阶，旧保本线会失效</h2>
  <p>算出的杯数还只是纸面答案。本量利分析有一个前提：售价、单杯变动成本和固定成本，要在当前经营区间里大致稳定。如果八十杯时一个人能做，一百二十杯时必须加兼职、延长工时或者增加设备，固定成本就已经跨台阶；这时还拿原来的保本线判断，数字会偏得很远。</p>
  <p>所以算完以后还要问两个现实问题：这个位置有没有足够需求支撑这条保本线；人员、设备和出品速度能不能在高峰期接住这些订单。如果答案是否定的，先改店型、成本或产品结构，而不是把希望全部压在开业以后再想办法卖更多。（「改电行」据画面校正为「改店型」。）</p>
  {figs(8)}
</section>

<section class="story-section" id="ch7">
  <h2><span class="time-marker">02:50–03:48</span>保本不是赚钱；别抄别人的「一天一百杯」</h2>
  <p>最后还要分清：保本不是赚钱。画面写明盈亏平衡点只表示在这套假设下营业利润约为零——固定成本刚被贡献盖住。若还希望每月获得一万元经营利润，目标就不是两千五百杯；示意画面给出约三千五百杯量级（按两万五加一万再除以每杯十元理解，仍属作者算例）。</p>
  <p>Whisper 在约 02:52 后几乎失效（末段仅识别出残片「A S」），但画面字幕继续收束：开店前真正要做的不是抄别人「一天卖一百杯」的答案，而是拆清固定与变动成本，换成日均杯量，再和商圈需求及门店产能对照。片尾留下互动：你的日均保本杯量是多少？</p>
  {figs(9, 10, 11)}
</section>
"""

    summary_html = "\n".join(
        f'<div class="summary-row"><span class="time-marker">[{tr}]</span>'
        f"<div><strong>{esc(label)}</strong><p>{esc(txt)}</p></div></div>"
        for tr, label, txt in summary_rows
    )

    toc = "".join(
        f'<a href="#{cid}">{t}</a>'
        for cid, t in [
            ("ch1", "忙碌≠赚钱：先看保本线"),
            ("ch2", "单杯贡献与变动成本"),
            ("ch3", "人工水电要拆标签"),
            ("ch4", "两万五÷十元的示意账"),
            ("ch5", "加权产品结构"),
            ("ch6", "产能台阶与两个现实问题"),
            ("ch7", "保本≠赚钱，别抄百杯答案"),
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
.warn{{background:#fff7ed;border-left:4px solid #f59e0b;padding:12px 16px;border-radius:8px;margin:16px 0;font-size:14px;color:#9a3412}}
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
    <span class="meta-tag tag-topic">咖啡经营 · 保本杯量 · 单杯贡献</span>
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
    <div class="warn">文中两万五/十元/八十四杯/一百零五杯/三千五百杯等数字均为作者口播或画面示意算例，用来说明贡献与保本关系，不是某一门店实测财报。00:01–00:30 与约 02:52 后口播进 Whisper 不完整，已用画面字幕补全并在正文标明。</div>
  </div>
  {chapters_html}
  <section class="transcript-section" id="transcript">
    <details class="transcript-collapsible">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div class="transcript-body">
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差与繁体字形；正文已按画面与语境校正（如「变动成本」「全店」「改店型」），转录区保持原样以便核对。末段残片「A S」为识别失败。</p>
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
