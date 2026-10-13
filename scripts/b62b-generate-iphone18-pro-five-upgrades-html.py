#!/usr/bin/env python3
"""b62b：生成 iphone18-pro-five-upgrades 图文实录 HTML（一次性/可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "iphone18-pro-five-upgrades"
KEY = "b62b"


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

    title = "为了这5个升级，还是换了iPhone 18 Pro"
    url = "https://xhslink.cn/o/6GrB9slekhu"
    duration = "3分59秒"
    intro = (
        "小红书 UP 主 Winnie龟龟仔（口播自称龟龟）用原相机直出样片开场，"
        "声称今年 iPhone 18 Pro「有意思的东西几乎都集中在影像上」，"
        "并整理五个她最近高频使用的升级：星芒、调色盘胶片感、双击追踪、电影效果，以及 Pro 相机控制慢门；"
        "片尾再附一套她每次换机都会检查的原相机系统设置。下列实录按时间线展开，观点均标注为作者体验。"
    )
    summary_rows = [
        ("00:00→00:21", "开场立场", "今年好玩点几乎都在影像；若日常用得到，升级 Pro「真的不亏」（作者观点）。"),
        ("00:21→00:56", "星芒操作", "可变光圈收至约 f/4 出舞台星芒；仅 1×/2× 可用，4×/8× 自动取消。"),
        ("00:56→01:32", "胶片调色", "摄影风格新增纹理、颗粒与柔化皮肤；「反差色+胶片」适合演唱会出片。"),
        ("01:32→02:06", "双击追踪", "对比 17 Pro Max 雨天失焦痛点；双击屏幕稳定追主体，也可拍宠物。"),
        ("02:06→02:47", "电影效果", "一倍/二倍视频可后期调虚化；声音侧电影效果滑杆压环境噪声。"),
        ("02:47→03:16", "慢门控制", "原相机分控快门/光圈/白平衡，低快门加转动手机出拖影。"),
        ("03:16→03:58", "设置清单", "关相机调整、4K60、空间音频、高效、HEIF 48MP——换机例行检查。"),
    ]
    takeaway = (
        "这条视频的决策逻辑不是「参数全面碾压」，而是五个可复用的影像玩法是否命中你的拍摄场景；"
        "命中则作者认为换机划算，同时用系统设置把画质与后期弹性兜住。"
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
<section class="story-section" id="ch-intro">
  <h2><span class="time-marker">00:00–00:21</span>开场：今年好玩的点几乎都在影像</h2>
  <p>视频一上来先甩一组演唱会现场照，字幕写明「都是我用 iPhone 18 Pro 原相机直出的照片」。作者接着判断：今年有意思的升级几乎都集中在影像，而且「比我想的还更好玩一些」。她把今天的内容框成五个最近用得很频繁的升级，并给出立场——如果你平时会用得到，升级 Pro「真的不亏」。这是体验向推荐，不是参数评测。</p>
  {figs(1)}
</section>

<section class="story-section" id="ch-starburst">
  <h2><span class="time-marker">00:21–00:56</span>第一个升级：可变光圈星芒，演唱会「想不出片都难」</h2>
  <p>第一个被点名的是星芒效果。作者把它归因于本代可变光圈：舞台上发光的大排灯会变成小星星特效，画面立刻华丽起来。操作路径很具体——打开拍摄界面右下角「镜头光圈」，选到 4（画面可见滑到 <strong>f 4.0</strong>），就能拍出这种梦幻星芒。</p>
  <p>边界也写得很清楚：星芒目前只能在 <strong>1 倍和 2 倍</strong>焦段使用；切到 4 倍、8 倍会自动取消。因此现场策略是先拍出星芒，再调整构图。</p>
  {figs(2, 3)}
</section>

<section class="story-section" id="ch-palette">
  <h2><span class="time-marker">00:56–01:32</span>第二个升级：调色盘摄影风格，原相机直出胶片感</h2>
  <p>第二部分标题直接打出「Part 02. 调色盘」。作者说今年摄影风格新增了纹理和颗粒，还可以柔化皮肤，所以用原相机就能拍出胶片感。她实测推荐「反差色 + 胶片」组合拍演唱会舞台，称更出片、更有氛围；并提到前几天看邓紫棋演唱会时用这套组合出了不少「神图」。</p>
  <p>画面给出原图与叠加风格后的对照，再叠加纹理和颗粒后，她形容质感「非常绝」，「有一种拿着 4S 拍照的感觉」——这是主观比喻，用来强调复古味，而非声称参数复刻。</p>
  {figs(4, 5)}
</section>

<section class="story-section" id="ch-tracking">
  <h2><span class="time-marker">01:32–02:06</span>第三个升级：双击追踪，雨天演唱会对焦不再抓狂</h2>
  <p>「双击追踪」一开始她没 get 到使用场景，看完演唱会后「彻底悟了」。对比体验是：用 17 Pro Max 时好不容易在雨天对上舞台上的姐姐，对方一转身又失焦；换成 18 Pro 后双击屏幕就能追踪，跟得很稳，不必全程手动找人对焦。她强调看到好画面却对不上焦、或干等对焦的过程很抓狂，所以给这个功能「大拇哥」。生活场景也可用来拍小狗，画面更不易失焦。本段以口播对比为主，未提供同机位对照素材。</p>
</section>

<section class="story-section" id="ch-cinematic">
  <h2><span class="time-marker">02:06–02:47</span>第四个升级：电影效果——后期虚化与环境降噪</h2>
  <p>电影效果被她形容为「挺神奇」：用主摄一倍和二倍焦段拍的视频，可以在后期调整虚化，效果和拍照的可变光圈类似。画面用上下分屏展示浅景深与标 <strong>f/16</strong> 的更深景深对照。</p>
  <p>声音侧也可以选电影效果：滑杆越往右，环境噪音越小。她站在路边做现场对比——背后车流、旁边大喇叭；开启后称噪音一下子弱很多，基本上只听到自己的声音。据此推论：以后用后置拍 Vlog，就不用太担心环境杂音干扰。</p>
  {figs(6)}
</section>

<section class="story-section" id="ch-pro">
  <h2><span class="time-marker">02:47–03:16</span>第五个升级：Pro 相机控制，原相机玩王家卫式慢门</h2>
  <p>第五点是 Pro 相机控制：作者称 iPhone 终于能用原生相机拍出「王家卫同款」慢门照片。今年原相机可以单独控制快门速度、光圈和白平衡——把快门调低，再旋转手机，就能拍出梦幻、有动态感的照片；白天也能拍电影感拖影。</p>
  <p>她回忆上学时常拿相机和三脚架去天桥拍车流光轨，现在用原相机就能玩同类效果。画面给出夜景车流拖影样片作为结果示意。</p>
  {figs(7)}
</section>

<section class="story-section" id="ch-settings">
  <h2><span class="time-marker">03:16–03:58</span>附赠：让画质更清晰的原相机参数设置</h2>
  <p>片尾不是第六个「升级卖点」，而是一套她每次换新 iPhone 都会检查的设置：打开设置 → 相机控制，把「相机调整」关闭，避免拍摄时误触相机控制键；录制选 <strong>4K 60 帧</strong>，声音选<strong>空间音频</strong>，以便事后在相册里继续调录音室、电影效果等混音选项；格式选<strong>高效</strong>省空间；图片格式选 <strong>HEIF、48MP</strong>，兼顾体积与清晰度。调完就可以「放心开始拍一拍」。结尾署名龟龟，下期再见。</p>
  {figs(8)}
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
            ("ch-intro", "开场：影像升级总览"),
            ("ch-starburst", "星芒与可变光圈"),
            ("ch-palette", "调色盘胶片感"),
            ("ch-tracking", "双击追踪"),
            ("ch-cinematic", "电影效果"),
            ("ch-pro", "Pro 慢门控制"),
            ("ch-settings", "原相机设置清单"),
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
.quote{{background:#f8fafc;border-left:4px solid #cbd5e1;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:15px;color:#57534e;font-style:italic}}
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
    <span class="meta-tag tag-topic">iPhone影像 · 原相机</span>
  </div>
  <p style="color:#57534e;font-size:14px;margin:0 0 12px">作者 Winnie龟龟仔 · 2026-10-13</p>
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
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按画面与语境校正专有名词，转录区保持原样以便核对。</p>
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
