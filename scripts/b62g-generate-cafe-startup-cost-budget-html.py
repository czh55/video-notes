#!/usr/bin/env python3
"""b62g：生成 cafe-startup-cost-budget 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "cafe-startup-cost-budget"
KEY = "b62g"


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

    title = "开一家咖啡店，到底要准备多少钱？"
    url = "https://xhslink.cn/o/3sv78FfB0sR"
    duration = "4分07秒"
    intro = (
        "小红书账号「甄茶笔记&大喜」直接回答「到底要准备多少钱」："
        "手里只有五万元就先别开；正常准备建议保底十万元。"
        "真正要算的不是能不能把门打开，而是开门以后有没有养店钱撑过销量爬坡。"
        "视频把预算拆成开门钱与养店钱，用小店模型示意开业前六到七万、缓冲三到四万；"
        "再列出开业前一次性投入清单、开业后持续支出、降标准恶性循环，以及开店前三张表与四件事。"
        "下列实录按时间线展开；金额均为作者经营建议与画面示意，非某一城市或门店报价。"
    )
    summary_rows = [
        ("00:00→00:32", "五万 vs 十万", "五万不是启动线；勉强开门≠具备经营条件。作者建议保底十万元再启动。"),
        ("00:32→01:15", "开业清单与持续支出", "押金转让装修设备原料等花完可能开门，但房租水电原料包装平台活动维护从第一天继续发生。"),
        ("01:15→02:00", "爬坡与恶性循环", "五万的硬伤是开业后没钱陪流量爬坡；被迫降设备/水电/原料标准后，复购更难、现金更紧。"),
        ("02:00→02:50", "两个账户", "同时准备开门钱与养店钱；小店示意六到七万开业前、三到四万缓冲；用现金覆盖月数算调整时间。"),
        ("02:50→03:35", "有效投入与四件事", "有钱也不全花开业前；贵设备/复杂装修要能提高效率、营业额、复购或降低停机风险。算清店型、一次性投入、月净流出、调整时间。"),
        ("03:35→04:07", "三张表与收束", "一次性投入表、月度收支表、保守销量现金余额表；五万不是低成本方案。下期预告保本杯量。"),
    ]
    takeaway = (
        "开店预算要同时准备「开门钱」和「养店钱」。"
        "作者观点：五万连开门都勉强、开业后更难维持；保底十万再启动，才有机会在开业后继续调整，而不是一开门就全面降标准。"
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
  <h2><span class="time-marker">00:00–00:32</span>五万元先别开：开门不等于具备经营条件</h2>
  <p>标题卡先把问题钉死：开一家咖啡店，到底要准备多少钱？作者几乎立刻给出态度——如果你手里只有五万元，建议先不要开；画面大字写的是「五万元不是开店的启动线」，不是一句轻松的励志鼓励。</p>
  <p>即便房租极低、没有高额转让费、装修和设备都压到极限，老板自己守店，也最多勉强开出十平方米以内的小微社区店。但「把门打开」和「具备经营条件」不是一回事：画面把开门的小店，和空钱包、账单堆叠的「没有养店钱」并置。真正要解决的，不是能不能开门，而是开门以后还能不能继续经营。作者给出自己的保底建议：手里有十万元再启动。</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:32–01:15</span>只算开业第一天：清单花完能开门，开业却是持续花钱的开始</h2>
  <p>很多人算预算，只算到开业第一天。画面逐项展开：房租和押金、可能存在的转让费、装修和水电改造、门头、操作台、洗消和冷藏设施、咖啡设备、首批原料、包装、桌椅、收银和各种小工具。这些钱花完，店「可能」开起来——但作者立刻改口：开业不是花钱的终点，而是持续花钱的开始。</p>
  <p>顾客不会在开业第一天就稳定进来，外卖销量和复购也不会立刻形成。与此同时，房租、水电、原料、包装、平台活动和设备维护，从第一天起就会继续发生；就算打算一个人顶，高峰或长营业时间也可能要请兼职或全职，收入还没稳，人力成本却已经按月开始付。（本段 Whisper 几乎空白，清单与句子以画面大字/烧录字幕重建。）</p>
  {figs(3)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">01:15–02:00</span>五万的真正风险：爬坡期没钱，最后变成经营恶性循环</h2>
  <p>作者把五万元的问题说得更狠：不只是开业时紧，而是开业后账户可能没有钱陪店走过流量爬坡。现金一紧，往往不是只砍一笔开支——机器买得勉强，水电和排水能省就省，原料和包装只看最低价；人手不够时，推广、维护和测新品也会被搁置。</p>
  <p>这些标准一起掉，结果是出品不稳、效率变低、体验变差，周转和复购更难抬升，现金于是更紧。画面用「现金收紧→恶性循环→小咖啡店」收束：一次预算不足，最后会变成整家店的经营恶性循环——这也是作者不建议用五万元开店的真正原因。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">02:00–02:50</span>两个账户：开门钱与养店钱；小店示意六到七万 / 三到四万</h2>
  <p>为什么正常建议保底十万元？因为开店预算必须同时准备两个账户：一个负责把店开起来（开门钱），一个负责把店养下去（养店钱）。以小店模型为例，画面给出一组示意拆分：开业前控制在六到七万元，剩下三到四万元作为经营缓冲——作者强调这不是全国统一标准，但至少保证开业当天账户里还有钱应对收入尚未稳定的阶段。</p>
  <p>「这三到四万元能撑多久，不能靠感觉。」做法是保守估算每月收入，再减掉房租、人工、水电、平台、原料和其他支出；如果每个月仍然净流出，剩余现金能覆盖几个月，才是你真正拥有的调整时间。（「六到七万 / 三到四万」来自画面大字，勿当作某一城市报价。）</p>
  {figs(5)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">02:50–03:35</span>有钱也不全花开业前；有效投入；先算清四件事</h2>
  <p>手里有十万元，也不代表可以把十万元全部花在开业前；更不能因为有二十万、三十万，就一定要把店做大、把机器买贵。更贵的设备、更复杂的装修，只有在确实提高出杯效率、营业额、复购，或者降低停机风险时，才可能是一笔有效投入——否则只是把以后需要收回的钱变多。</p>
  <p>示意对照很直观：同样每个月赚一万元，前期投入八万元的店，和投入三十万元的店，回收难度完全不同。口播随即把「孤立总预算」拆成四件事：你要开什么店型、开业前一次性花多少、保守销量下每月还会净流出多少、开业后剩余的钱能留下多少调整时间。</p>
</section>

<section class="story-section" id="ch6">
  <h2><span class="time-marker">03:35–04:07</span>开店前三张表；五万不是低成本方案；下期算保本杯量</h2>
  <p>行动落点是三张表：一张列开业前一次性投入，一张列每月固定和变动支出，一张用保守销量测算开业后的现金余额；再把「必须现在买」和「以后赚钱了再加」的项目分开。</p>
  <p>回到开头：五万元不是值得尝试的低成本方案，而是连开店都很勉强、开业后更难维持的预算。正常准备咖啡店，手里保底有十万元再启动，才有机会把店开起来以后继续调整，而不是一开业就被现金逼着全面降标准。片尾留下互动：你更想看外卖档口，还是有座位的社区店，具体要卖多少杯才能养活自己？并预告下一期算小店每月要卖多少杯才能跨过保本线——本期没有给出具体保本杯量数字。</p>
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
            ("ch1", "五万先别开：开门≠经营条件"),
            ("ch2", "开业清单与持续支出"),
            ("ch3", "爬坡期没钱与恶性循环"),
            ("ch4", "开门钱/养店钱与十万拆分"),
            ("ch5", "有效投入与四件事"),
            ("ch6", "三张表与保底十万收束"),
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
    <span class="meta-tag tag-topic">咖啡经营 · 开店预算 · 现金流</span>
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
    <div class="warn">Whisper 仅约 17 段且前半大量空洞，正文已结合画面字幕重建；五万元/十万元/六到七万/三到四万/八万与三十万等数字均来自画面或后半口播，未臆造未出现金额。文中金额为作者经营建议与示意拆分，不是某一城市或门店的实测报价。本期未给出保本杯量。</div>
  </div>
  {chapters_html}
  <section class="transcript-section" id="transcript">
    <details class="transcript-collapsible">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div class="transcript-body">
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差与空洞；正文已按画面与语境校正（如「店型」「再加的项目」），转录区保持原样以便核对。</p>
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
