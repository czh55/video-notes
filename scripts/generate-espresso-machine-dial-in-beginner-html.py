#!/usr/bin/env python3
"""b62m：生成 espresso-machine-dial-in-beginner 图文实录 HTML（未增强 figcaption）。"""
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
SLUG = "espresso-machine-dial-in-beginner"
KEY = "b62m"
URL = "https://xhslink.cn/o/8oHA2m5BWWP"


def to_simplified(s: str) -> str:
    return _T2S.convert(s) if _T2S else s


def fmt(t: float) -> str:
    t = max(0, int(t))
    return f"{t // 60:02d}:{t % 60:02d}"


def escape(s: str) -> str:
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
            f'<li class="tr" id="transcript-{i}">'
            f'<time datetime="PT{int(seg["start"])}S">{fmt(seg["start"])}</time>'
            f"<p>{escape(text)}</p></li>"
        )
    return "\n".join(rows), len(rows)


def main() -> None:
    shots = json.loads((ROOT / f"shots-{SLUG}.json").read_text(encoding="utf-8"))["shots"]
    by_num = {
        int(s["file"].replace("shot-", "").replace(".jpg", "")): s for s in shots
    }

    def fig(num: int) -> str:
        s = by_num[num]
        cap = s["caption"]
        return (
            f'<figure><img src="assets/{SLUG}/{s["file"]}" alt="{escape(s.get("alt") or cap)}" loading="lazy">'
            f"<figcaption>[{s['time']}] {escape(cap)}</figcaption></figure>"
        )

    transcript, n_seg = build_transcript()
    desc = (
        "甄茶笔记&大喜给新手定调参总顺序：先调研磨粗细看流速，再调磨豆时间稳粉量，"
        "最后设咖啡机自动定量；18–19克粉、36克液、25–30秒是起点不是死答案。"
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escape(desc)}">
  <title>咖啡机调试教程｜新手必看｜图文实录</title>
  <style>
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}}
.c{{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}}
h1{{font-size:28px;font-weight:800;color:#1c1917;margin:0 0 8px;line-height:1.3}}
.meta{{color:#78716c;font-size:14px;margin-bottom:16px}}
.intro{{font-size:17px;color:#44403c;line-height:1.9;margin-bottom:24px}}
.sl{{display:inline-block;color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:28px}}
.sl:hover{{text-decoration:underline}}
h2{{font-size:22px;font-weight:700;color:#1c1917;margin:32px 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
h3{{font-size:18px;font-weight:700;color:#1c1917;margin:28px 0 12px}}
.sr{{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}}
.sr .tm{{flex-shrink:0;font-size:13px;font-weight:700;color:#b45309;min-width:110px;font-variant-numeric:tabular-nums}}
.sr strong{{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}}
.sr p{{color:#57534e;margin:0;font-size:15px}}
.tb{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}}
.tb strong{{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}}
.tb p{{color:#1e40af;margin:0;font-size:15px}}
.ss p{{color:#44403c;margin:0 0 14px}}
.trng{{font-size:13px;color:#b45309;font-weight:600;margin-bottom:10px}}
.quote{{background:#f8fafc;border-left:4px solid #cbd5e1;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:15px;color:#57534e;font-style:italic}}
.note-box{{background:#fff7ed;border-left:4px solid #f59e0b;border-radius:10px;padding:12px 16px;margin:16px 0;font-size:14px;color:#92400e}}
img{{display:block;max-width:100%;height:auto}}
figure{{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}}
figcaption{{padding:14px 18px;color:#57534e;font-size:14px}}
.tsl{{list-style:none;padding:0;margin:0}}
.tr{{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}}
.tr time{{color:#b45309;font-weight:700;font-variant-numeric:tabular-nums}}
.tr p{{margin:0}}
.tc{{border:none;padding:0;margin:0}}
.tc summary{{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;font-size:24px;font-weight:700;color:#1c1917;padding-bottom:8px;border-bottom:2px solid #e7e5e4}}
.tc summary::-webkit-details-marker,.tc summary::marker{{display:none}}
.tc summary::before{{content:"▶";font-size:12px;color:#b45309;transition:transform .2s}}
.tc[open] summary::before{{transform:rotate(90deg)}}
.tc[open] summary{{margin-bottom:16px}}
.note{{font-size:14px;color:#78716c}}
@media(max-width:640px){{.c{{padding:28px 18px 56px}}h1{{font-size:24px}}.tr{{grid-template-columns:56px 1fr;gap:10px}}.sr{{flex-direction:column}}}}
  </style>
</head>
<body>
<main class="c">
  <header>
    <h1>咖啡机调试教程｜新手必看</h1>
    <div class="meta">时长 4 分 39 秒 · 作者 甄茶笔记&amp;大喜 · 咖啡 · 小红书 · 2026-10-13</div>
    <p class="intro">小红书账号「甄茶笔记&amp;大喜」面向刚买咖啡机和磨豆机的新手，回答「第一次调参到底先动哪一台」。视频不背某台磨豆机的数字几，而是给出可复用的三步顺序：先用粉量、液重和时间把研磨粗细调稳，再固定研磨去调磨豆时间稳住出粉，最后才设置咖啡机自动定量。下列实录按时间线展开；温度区间与配方数字均为作者建议起点。</p>
    <a class="sl" href="{URL}" target="_blank" rel="noopener">→ 查看原视频（小红书）</a>
  </header>

  <article>
    <h2>内容要点</h2>
    <p>这是一则约四分半的设备调试教程：从「疯狂往外冲」「时间从哪开始算」等新手痛点切入，落到「先调流速 → 再定粉量 → 最后做自动化」。</p>
    <h3>知识结构</h3>
    <div class="sr"><span class="tm">[00:00→00:18]</span><div><strong>开场三问与总顺序</strong><p>先调哪一台、疯狂外冲怪谁、时间从按键还是第一滴算——作者给出顺序：研磨粗细 → 磨豆时间 → 自动定量。</p></div></div>
    <div class="sr"><span class="tm">[00:18→00:52]</span><div><strong>准备与称重纪律</strong><p>充分预热、温度先放在91–93℃，压力预浸自动量先别改；调试阶段每杯称粉也称液；粉接近细盐只作起点。</p></div></div>
    <div class="sr"><span class="tm">[00:52→01:26]</span><div><strong>第一步：用流速定研磨</strong><p>按键同时计时，到36克马上停；&lt;25秒调细，&gt;30秒调粗；落在25–30秒即进入合适起始范围。</p></div></div>
    <div class="sr"><span class="tm">[01:26→02:07]</span><div><strong>调研磨的避坑动作</strong><p>先认机身标识；每次调完排约10克残粉；大幅调细要分段；本阶段只改研磨度直至稳定。</p></div></div>
    <div class="sr"><span class="tm">[02:07→02:41]</span><div><strong>第二步：磨豆时间定粉量</strong><p>固定研磨后用磨时控制出粉；落在18–19克并连续三次稳定再保存；换豆或调磨后仍要复称。</p></div></div>
    <div class="sr"><span class="tm">[02:41→03:33]</span><div><strong>第三步：自动定量</strong><p>计时定量记秒数、流量计记水量；设完用秤复测，连续2–3杯接近36克才算调好。</p></div></div>
    <div class="sr"><span class="tm">[03:33→04:37]</span><div><strong>边界：数字是起点</strong><p>18–19克 / 36克 / 25–30秒不是死答案；先把机器调稳，再用味道判断，好喝才是结果。</p></div></div>
    <div class="tb"><strong>总结</strong><p>新设备调试真正要记住的不是某台磨豆机调到数字几，而是三步：先调流速，再定粉量，最后做自动化。</p></div>

    <section class="ss">
      <h2>图文实录</h2>
      <div class="note-box">说明：正文对 ASR 同音误识（如「细颜→细盐」「液中→液重」）已按画面与语境校正；页末转录仍保留 Whisper 原文作证据。本条与另一短链「磨豆机参数调试」主题可能相近，但 url/slug 独立，按本片口播单独成文。</div>

      <h3>第一次调参，先动哪一台</h3>
      <div class="trng">00:00 – 00:18</div>
      <p>视频一上来就抛出新手最慌的三件事：新买咖啡机和磨豆机，第一次调参数到底先调哪一个；18克粉一开机就疯狂往外冲，到底是粉量不对还是研磨太粗；萃取时间从按键开始算，还是第一滴出来以后才算。</p>
      <p>作者没有立刻甩一串机型数字，而是先钉死顺序：</p>
      <div class="quote">「记住一个顺序就够了：先调研磨粗细，再调磨豆时间，最后设置咖啡机自动定量。」</div>
      {fig(1)}

      <h3>先让机器稳定，再谈参数</h3>
      <div class="trng">00:18 – 00:52</div>
      <p>正式动手前，作者要求充分预热，温度先保持在91–93度；压力、预浸和自动萃取量暂时都不要改——调试阶段一次只动一个关键变量。准备同一款豆、双份粉碗、电子秤、浓缩杯和计时器；调试时每杯既要称粉，也要称最后的浓缩液。</p>
      <p>磨豆机可从默认研磨度开局，粉看起来接近细盐可以当视觉起点，但最终是否合适「不靠眼睛判断，要看液重和时间」。粉量目标落在18–19克，不要低于18克，且每轮尽量一致；装粉后新手建议先铺平，再水平压粉，手柄上机后电子秤和浓缩杯摆好。</p>
      {fig(2)}

      <h3>按键计时到36克：用流速定研磨</h3>
      <div class="trng">00:52 – 01:26</div>
      <p>口播在约52秒后有一小段空白，画面转入按键与萃取演示。规则很硬：不是等咖啡流出来再算；电子秤到36克马上停止萃取并记录时间。</p>
      <p>判断也很简单：不到25秒已经到36克，流速太快，研磨调细；超过30秒还没到36克，流速太慢，研磨调粗。若18–19克粉萃出36克液能落在25–30秒，研磨度就进入比较合适的起始范围。回扣开场：粉量和其他操作没变时，疯狂往外冲首先检查研磨是不是太粗。</p>
      {fig(3)}

      <h3>认标识、排残粉，只改研磨度</h3>
      <div class="trng">01:26 – 02:07</div>
      <p>多数磨豆机数字越小越细、越大越粗，但不同型号可能相反——调整前先看机器上的粗细标识。更关键的动作是：每次调整研磨度以后，先排掉大约10克咖啡粉，因为通道里还残留上一档位的粉；不排掉，下一杯会混入两种粗细，测试就不准。</p>
      <p>需要大幅调细时，也不要一次拧到底：调一点、抹一点、再继续调，避免豆子卡住刀盘、让调节机构受力过大。排完残粉后重新称18–19克，布粉压粉归零，按键同时计时到36克停止。这个阶段每一轮只改研磨度，其他条件尽量不变，重复直到36克能比较稳定地落在25–30秒——做到这里，研磨粗细先固定，不要再动。</p>
      {fig(4)}

      <h3>固定研磨后，用磨豆时间稳住粉量</h3>
      <div class="trng">02:07 – 02:41</div>
      <p>第二步开始调磨豆时间。许多定量磨豆机其实是通过「磨几秒」控制出粉量。作者建议先把磨豆时间设成3秒，磨完称重：低于18克就增加时间，超过19克就减少时间，直到每次出粉都在18–19克之间。</p>
      <p>然后连续测试三次，三次都比较稳定就可以保存这个磨豆时间——以后正常出杯就不用每杯重新称粉。但开机第一杯、换豆、调整过研磨度，或发现萃取速度明显变化时，还是要重新复称。</p>
      {fig(5)}

      <h3>最后才设咖啡机自动定量</h3>
      <div class="trng">02:41 – 03:33</div>
      <p>研磨度和粉量都稳定以后，才进入最后一步：设置咖啡机自动萃取量。作者对比两种常见方式。</p>
      <p>第一种是计时定量：机器只记住运行多少秒，并不知道杯子里实际有多少克咖啡液。所以根据前面稳定萃取到36克所需要的时间设置自动萃取时长，设完再放上电子秤复测，确认实际液重接近36克。</p>
      <p>第二种是流量计定量：机器根据流过系统的水量控制，一般会比单纯计时定量更稳定一些。常见做法是长按自定义萃取键开始萃取，电子秤到36克时松开，让机器记住这次萃取量；但不同咖啡机设置方式可能不同，有些需要再次按键停止和保存，具体以说明书为准。</p>
      <p>自动定量设置完成以后，再连续制作2到3杯，每杯都能比较稳定地接近36克，这个自动萃取键才算真正调好。</p>
      {fig(6)}

      <h3>三步复盘：数字是起点，好喝才是结果</h3>
      <div class="trng">03:33 – 04:37</div>
      <p>作者把整条顺序再走一遍：第一步用18–19克粉、目标36克液、25–30秒参考区间把研磨粗细调稳定；第二步研磨度不再改变，通过磨豆时间让自动出粉稳在18–19克；第三步最后设置咖啡机自动萃取到接近36克。</p>
      <div class="quote">「新设备调试真正需要记住的，不是某一台磨豆机到底调到数字几，而是三个步骤：先调流速，再定粉量，最后做自动化。」</div>
      <p>最后提醒：18–19克粉、36克液重、25–30秒并不是所有咖啡豆都必须死守的标准答案，更像是新手第一次调设备时一个比较稳定的起点。先按照这套参数把机器调稳定，再开始用味道判断；换了咖啡豆、烘焙度或饮用方式以后，合适的粉液比和时间都可能变化。进阶调试不是把数字卡得越来越死，而是根据酸甜苦涩、浓度和风味继续调整——参数只是起点，好喝才是结果。</p>
      {fig(7)}
    </section>
  </article>

  <section id="transcript">
    <details class="tc">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div>
        <p class="note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差（如细颜、液中、部分压粉等）；正文已按画面与语境校正。</p>
        <ol class="tsl">
{transcript}
        </ol>
      </div>
    </details>
  </section>
</main>
<script>(function(){{var d=document.querySelector(".tc");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body>
</html>
"""
    out = DOCS / f"{SLUG}-图文实录.html"
    out.write_text(to_simplified(html), encoding="utf-8")
    print(f"Generated: {out} segments: {n_seg}")


if __name__ == "__main__":
    main()
