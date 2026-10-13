#!/usr/bin/env python3
"""b62h：生成 cafe-price-war-follow-or-not 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "cafe-price-war-follow-or-not"
KEY = "b62h"


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

    title = "咖啡店价格战能不能跟？"
    url = "https://xhslink.cn/o/Axsh7cqF0dz"
    duration = "3分25秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」用「隔壁美式降到九块九」开场，"
        "不直接回答跟不跟价，而是把问题改写成：降价以后要多卖多少杯，"
        "才能留下原来一样的钱。视频用十五元售价、五元变动成本的示意算例，"
        "算出九块九时约需二百零四杯才持平，再提醒平台到手价、人力产能与差评损耗都会让真实门槛更高；"
        "随后区分「完全不回应」与「有边界测试」，强调订单≠新客、小店不能照抄连锁，"
        "最后给出入口款、范围限定与停止条件。下列实录按时间线展开；数字均为作者示意，非某一门店实测。"
    )
    summary_rows = [
        ("00:00→00:20", "改写问题", "别盯对手卖多少；算降价后要多卖多少杯才能留下原来的钱。真正要防的是订单涨了利润没了。"),
        ("00:20→00:58", "单杯贡献", "留下≠净利润；15元−5元成本=每杯留10元。降到9.9后每杯4.9，持平约需204杯，且到手未必是9.9。"),
        ("00:58→01:25", "产能与结算", "翻倍后要加兼职、出杯排队、退款差评；先看单杯贡献、实际结算、高峰产能。"),
        ("01:25→01:54", "让利换什么", "同质商圈完全不回应可能丢单；关键是这次让利要换守单、获客还是填闲时。"),
        ("01:54→02:29", "订单≠新客", "多100杯活动单可能含60杯本会原价买；连锁能扛多久不能证明你也能。"),
        ("02:29→03:25", "有边界测试", "入口款+限定范围；写清停止条件；不能只跟价格，先算留下多少再确认换回什么。"),
    ]
    takeaway = (
        "可以跟，但不能只跟标价。"
        "先算单杯贡献与实际结算，再确认高峰产能接得住，最后用小范围测试核对让利是否换来新客、连带与复购；"
        "算不清就不要全店降价。"
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
  <h2><span class="time-marker">00:00–00:20</span>开场：别只看对手卖多少，先算要多卖多少杯</h2>
  <p>视频标题卡直接抛出场景：隔壁美式降到九块九，你到底要不要跟？作者没有先给「跟」或「不跟」的口号，而是改写判断标准——答案不是看他卖多少钱，而是看你降价以后要多卖多少杯，才能留下原来一样的钱。</p>
  <p>示意很干脆：一杯原来能留下十元，降价后只剩四块九，销量就要接近翻倍。作者把小店价格战的真正风险说得很反直觉：要防的不是订单下降，而是订单涨了、利润反而没了。于是口播转入「先把这笔账算完整」。</p>
  {figs(1)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:20–00:58</span>单杯贡献：十五元到九块九，纸面大约二百零四杯</h2>
  <p>「留下」在这里被明确定义：不是门店最后的净利润，而是售价扣掉原料、包装和其他随订单变化的成本以后，每卖一杯还能留下多少钱。示意算例是一杯原价十五元、这些成本一共五元，每杯留下十元；一天卖一百杯，一共留下一千元。</p>
  <p>售价降到九块九、成本仍按五元计，每杯只剩四块九；想继续留下一千元，就要卖到大约二百零四杯。作者立刻补刀：二百零四杯只是纸面答案——活动页写九块九，不等于商家实际到手九块九；平台补贴多少、门店承担多少、每单还有哪些费用，都要回到后台结算核对。</p>
  {figs(2, 3)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">00:58–01:25</span>订单翻倍后，成本和产能也可能一起动</h2>
  <p>纸面持平之外，真实经营还会抬高门槛：一个人坐得过来，可能变成要加兼职；原来的备料、制冰和咖啡机产能，可能变成出杯排队；等待时间一长，退款、差评和损耗也会跟着增加。（Whisper 原词「初杯排队」，据语境校正为「出杯排队」。）</p>
  <p>因此跟价之前，先别看对手的标价，先看自己的单杯贡献、实际结算和高峰产能。只要其中一个扛不住，订单越多，门店可能越忙，也越难留下钱。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">01:25–01:54</span>不是完全不能跟：先问这次让利换回什么</h2>
  <p>作者随即纠偏：这不是说小店完全不能跟价。同一个商圈里，如果几家店的产品、评分和配送时间都差不多，价格确实会影响顾客选择；你完全不回应，订单可能会被分走。</p>
  <p>但此时要判断的已经不是「九块九值不值得跟」，而是「这次让掉利润准备换回什么」——守住订单、让新顾客第一次下单，还是填补下午空闲时段。目标不同，降价的产品、时间和范围就不同；目标定下来以后，还要分清增加的是订单还是顾客。</p>
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">01:54–02:29</span>多出来的活动单，不等于多出来的新客</h2>
  <p>画面用一百杯阵列解释蚕食：其中六十杯本来就会按正常价格购买，只是现在改买了便宜款。看起来多了一百杯活动订单，真正新增的顾客却没有一百个；你还主动让掉了原本能留下的钱。（约 01:54 前后有短口播缺口，完整「多卖一百杯」设定由画面字幕补全。）</p>
  <p>真正被低价带来的顾客，也不能只看第一次下单——有没有顺带购买其他产品、活动结束后会不会按正常价格回来，才决定这次让利有没有买回后续价值。这也是小店不能直接照抄连锁九块九的原因：前台标价一样，背后的采购成本、品牌流量、会员体系、排班效率和库存能力可能完全不同；别人能承受多久，不能替你证明自己也能承受。</p>
  {figs(5)}
</section>

<section class="story-section" id="ch6">
  <h2><span class="time-marker">02:29–03:25</span>把跟价做成边界清楚的测试，并写好停止条件</h2>
  <p>对小店更稳妥的做法不是全店一起降，而是把价格竞争做成一次边界清楚的测试：选一款结构简单、出杯稳定的产品作为价格入口，再限定新客、时段、数量或活动周期；主力产品和真正承担利润的产品，不要一起被拖下去。促销价、原价和试用条件也要写清楚，不能靠虚构原价制造便宜感。</p>
  <p>测试开始前就把停止条件写下来：单杯贡献低于底线、出杯速度明显下降、退款和差评上升，或者低价订单增加了却没有带来新客、连带购买和正常价复购——就应该缩小范围、换产品或停止活动。收束句很干净：你不是不能跟，而是不能只跟价格；先算每杯能留下多少，再看门店能不能接住新增订单，最后确认这次让利到底换回了什么。如果这些问题没有答案，就不要直接全店降价。片尾留下互动：如果是你的店，你会先用一款产品小范围测试，还是暂时不跟？</p>
  {figs(6, 7)}
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
            ("ch1", "改写问题：多卖多少杯才持平"),
            ("ch2", "单杯贡献与204杯纸面账"),
            ("ch3", "产能、结算与三项自检"),
            ("ch4", "让利要换回什么"),
            ("ch5", "订单≠新客，勿抄连锁"),
            ("ch6", "有边界测试与停止条件"),
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
    <span class="meta-tag tag-topic">咖啡经营 · 价格战 · 单杯贡献</span>
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
    <div class="warn">文中十五元/五元/二百零四杯等数字均为作者口播示意算例，用来说明贡献与销量关系，不是某一门店或平台的实测财报。约 01:54 有短口播缺口，已用画面字幕补全「多卖一百杯」设定。</div>
  </div>
  {chapters_html}
  <section class="transcript-section" id="transcript">
    <details class="transcript-collapsible">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div class="transcript-body">
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按画面与语境校正（如「出杯排队」），转录区保持原样以便核对。</p>
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
