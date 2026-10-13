#!/usr/bin/env python3
"""b62e：生成 coffee-channeling-effect 图文实录 HTML（未增强 figcaption，供后续音频/增强脚本处理）。"""
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
SLUG = "coffee-channeling-effect"
KEY = "b62e"
URL = "https://xhslink.cn/o/3ncye3zBuDz"


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
            f'<figure><img src="assets/{SLUG}/{s["file"]}" alt="{escape(cap)}" loading="lazy">'
            f"<figcaption>[{s['time']}] {escape(cap)}</figcaption></figure>"
        )

    transcript, n_seg = build_transcript()

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="粉量时间都正常却又酸又苦？甄茶笔记&大喜用通道效应解释：水在粉饼里走捷径，先布粉压粉萃匀再微调研磨。">
  <title>咖啡萃取之通道效应｜图文实录</title>
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
    <h1>咖啡萃取之通道效应</h1>
    <div class="meta">时长 2 分 29 秒 · 作者 甄茶笔记&amp;大喜 · 咖啡 · 小红书 · 2026-10-13</div>
    <p class="intro">甄茶笔记&amp;大喜用约两分半把一个常见挫败讲透：粉量、时间都在参考范围里，浓缩却又酸又苦——先别急着来回拧研磨度。视频用粉饼孔洞和剖面示意说明「通道效应」：水在粉床里走捷径，松处过萃、紧处欠萃，最后混进同一杯。应对顺序是先把布粉、压粉做匀，再微调研磨找味道。</p>
    <a class="sl" href="{URL}" target="_blank" rel="noopener">→ 查看原视频（小红书）</a>
  </header>

  <article>
    <h2>内容要点</h2>
    <p>这是一则意式萃取排错短片：从「犒劳自己却难喝」切入，先演示错误归因（只调粗研磨），再落到通道效应的机理与布粉压粉动作。</p>
    <h3>知识结构</h3>
    <div class="sr"><span class="tm">[00:00→00:25]</span><div><strong>难喝开场</strong><p>想做杯咖啡犒劳自己，结果酸、苦、涩全占齐；作者态度是「自己做的怎么也得把它调好」。</p></div></div>
    <div class="sr"><span class="tm">[00:25→00:55]</span><div><strong>误判过萃只拧磨</strong><p>先怀疑磨太细萃过头就调粗：涩轻了，但水流飞快，味道在酸、淡、涩之间来回晃。</p></div></div>
    <div class="sr"><span class="tm">[00:55→01:25]</span><div><strong>参数正常≠粉床均匀</strong><p>记录里时间、克重都在范围内；真正要看的是水在粉饼里怎么走——逮着松软处一路钻过去，就是通道效应。</p></div></div>
    <div class="sr"><span class="tm">[01:25→02:05]</span><div><strong>松紧从布粉压粉来</strong><p>粉堆偏、结团、表面压平但内部未分匀，都会造成松紧不均；可用细布粉针打散，再水平垂直压粉。</p></div></div>
    <div class="sr"><span class="tm">[02:05→02:29]</span><div><strong>先萃匀再调味</strong><p>哪一步没做好先改哪一步，再微调研磨；别把所有问题都怪在压粉上。作者收束：先萃匀，再调味，强过心疼豆子来回拧刻度。</p></div></div>
    <div class="tb"><strong>总结</strong><p>通道效应让一杯里同时出现欠萃与过萃；粉量时间「看起来正常」仍可能难喝。优先把粉床做匀，再谈研磨微调。</p></div>

    <section class="ss">
      <h2>图文实录</h2>
      <div class="note-box">说明：本片 Whisper 自动转录几乎失效（仅 3 段且后两段残缺）。以下章节按画面烧录字幕与笔记文案重建；页末「详细文字转录」仍完整保留原始 Whisper 分段作证据。</div>

      <h3>想犒劳自己，却喝到酸苦涩</h3>
      <div class="trng">00:00 – 00:25</div>
      <p>画面里作者站在银色家用意式机前持手柄出杯，字幕先把场景钉死：心血来潮想做杯咖啡犒劳自己。下一秒他端起白杯皱眉——字幕直白写出结果：「酸苦涩全占齐了」。旁置一只外卖杯，把「外面买」和「自己做」并置，语气落到「自己做的怎么也得把它调好」。</p>
      {fig(1)}
      {fig(2)}

      <h3>先怪磨细过萃，越拧越不对</h3>
      <div class="trng">00:25 – 00:55</div>
      <p>排错第一步很常见：琢磨是不是磨太细、萃过头了，于是拧磨豆机「调粗一点」。画面切到双嘴手柄两股液流飞快入杯，字幕承认涩轻了，但「水却跑得飞快」。折腾一通后，味道在酸、淡、涩之间摇摆——说明只动研磨度并没有打中真正的瓶颈。</p>
      {fig(3)}

      <h3>参数在范围里，问题在粉饼通道</h3>
      <div class="trng">00:55 – 01:25</div>
      <p>作者翻出记录：时间、克重都在参考范围里。转折出现在「看着手里的粉饼」——萃取后的湿粉饼表面能看到多个圆形孔洞。字幕点破此前的盲区：一直盯着整杯用了多少秒、出了多少克，却没管水在粉里面怎么走。</p>
      <div class="quote">「而是逮着几个好走的地方就一路钻过去了呢？」</div>
      <p>剖面动画把「通道效应」画成捷径：水优先从松软缝隙钻穿，通道处过萃、未过水处欠萃，最后却混进同一杯。笔记文案把症状概括为：粉量、时间都正常，咖啡却又酸又苦——可能是水走了捷径。</p>
      {fig(4)}
      {fig(5)}
      {fig(6)}

      <h3>松紧从哪来：布粉与压粉</h3>
      <div class="trng">01:25 – 02:05</div>
      <p>机理之后落到成因：粉没分匀就会有的地方紧、有的地方松；粉堆偏在一边、接粉结团，都会埋下通道。关键纠偏句是——表面压平了，可不代表里面也分匀了。操作演示：结团时用细布粉针轻轻打散；分匀后手柄放稳，压粉器保持水平，垂直下压。</p>
      {fig(7)}
      {fig(8)}

      <h3>先改步骤，再微调研磨</h3>
      <div class="trng">02:05 – 02:29</div>
      <p>收束顺序很明确：发现哪一步没做好就先改哪一步，再微调研磨找喜欢的味道；同时提醒「别把所有问题都怪在压粉上」。结尾字幕把策略钉成一句可执行原则：</p>
      <div class="quote">「先萃匀，再调味，总比心疼着豆子还在来回拧刻度强。」</div>
      <p>立场上，这是作者基于演示与示意的教学观点：优先均匀萃取，再谈风味微调；具体研磨刻度与配方数字需按自家豆子与设备验证。</p>
    </section>
  </article>

  <section id="transcript">
    <details class="tc">
      <summary>详细文字转录（{n_seg}段）</summary>
      <div>
        <p class="note">以下内容按 Whisper 原始分段完整呈现。本片 ASR 质量极差（后两段高无语音概率、文本残缺），正文已按画面字幕重建；请勿把下方残缺句当作完整口播。</p>
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
    out.write_text(html, encoding="utf-8")
    print(f"Generated: {out} segments: {n_seg}")


if __name__ == "__main__":
    main()
