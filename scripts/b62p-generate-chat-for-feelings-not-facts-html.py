#!/usr/bin/env python3
"""b62p：生成 chat-for-feelings-not-facts 图文实录 HTML（可复跑）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SLUG = "chat-for-feelings-not-facts"
KEY = "b62p"


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

    title = "聊天不要聊事实，要聊点让人爽的"
    url = "https://xhslink.cn/o/8hOsu422nrh"
    duration = "9分46秒"
    intro = (
        "小红书账号「叶子认知思维」用近十分钟给出一套「十天闲聊训练」："
        "聊天别只陈述事实，要聊情绪、感受与共鸣，每天一个小动作，把「聊天机器」练成会制造情绪价值的人。"
        "从事实回应与感受回应的对照起步，依次练感受词、事实翻译法、适度夸张、隐藏情绪、共同体验、情绪反馈与追问感受，"
        "第九天串成四步流程并推荐书《学会闲聊》，第十天用一个月每日三次感受回应固化习惯。"
        "下列实录按时间线展开；技巧与效果均为作者口播观点，非普遍社交定律。"
    )
    summary_rows = [
        ("00:00→00:39", "问题与承诺", "同一件事有人说得舒服、有人说对却接不上话；十天每天一小步，学会闲聊。"),
        ("00:39→01:26", "第一天诊断", "翻三段聊天记录：事实回应=证明在听；感受回应=让人觉得懂他。"),
        ("01:26→03:10", "第二–三天", "感受词开头；事实翻译法=说出对方情绪+认同。"),
        ("03:10→04:50", "第四–五天", "适度夸张并配语气词；听出分享背后的认可期待。"),
        ("04:50→06:37", "第六–七天", "共同体验法连经历；情绪反馈结成「情绪共同体」。"),
        ("06:37→08:49", "第八–九天", "追问感受挖深话题；四步流程实战+闲聊核心是读情绪。"),
        ("08:49→09:46", "第十天固化", "聊情绪感受共鸣；一个月每天至少三次感受回应法。"),
    ]
    takeaway = (
        "闲聊的核心不是找话题，而是读懂言语背后的情绪并持续提供情绪价值。"
        "先把事实译成感受，再用夸张、共情联结与追问把话题往下挖；效果因人因场景而异，需按关系边界把握分寸。"
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
  <h2><span class="time-marker">00:00–00:39</span>开场：别只聊事实，十天练会情绪价值</h2>
  <p>视频一上来就把对立面摆清：聊天不要聊事实，要聊点让人爽的。作者问观众有没有发现——有些人说话特别招人喜欢，明明聊的是同一件事，从他嘴里说出来就是舒服；另一些人说的都对，却让人不想接话。</p>
  <p>今天的承诺很具体：用十天时间专门练会这个技能，从一个只会陈述事实的「聊天机器」，变成会制造情绪价值的社交高手；每天只需要一个小动作。互动环节要求观众现在就为自己打出四个字——「学会闲聊」。</p>
  {figs(1, 2)}
</section>

<section class="story-section" id="ch2">
  <h2><span class="time-marker">00:39–01:26</span>第一天：先认清你在回事实还是回感受</h2>
  <p>第一天不练别的，先观察自己平时怎么跟人聊天。作业是找出三段最近的聊天记录，数一数：多少句在陈述事实，多少句在表达感受。</p>
  <p>什么叫事实回应？朋友说今晚加班到十点，你回「辛苦了，早点休息」——信息正确，但停在礼貌层。什么叫表达感受？同样情况你可以说「天呐，十点才下班，你们老板也太黑了吧」——这是在共情对方的处境。作者收束得很干脆：事实只是让人知道你在听，感受会让人觉得你懂他。</p>
  {figs(3)}
</section>

<section class="story-section" id="ch3">
  <h2><span class="time-marker">01:26–02:19</span>第二天：回复前先在心里加一个感受词</h2>
  <p>从今天起，每次回复别人之前，先在心里加一个感受词——能表达情绪的词，比如太棒了、好羡慕、心疼你、真不容易、太爽了、好气啊。</p>
  <p>练习极简单：找五个朋友的朋友圈，每次回复都用感受词开头。晒美食别光说好看，要说「哇，这也太诱人了吧，隔着屏幕我都馋了」；吐槽堵车别只说注意安全，要说「这也太让人崩溃了，我最烦堵车了」。目标是让感受词成为口头禅，张口就来。</p>
  {figs(4)}
</section>

<section class="story-section" id="ch4">
  <h2><span class="time-marker">02:19–03:10</span>第三天：事实翻译法——把事实译成背后的感受</h2>
  <p>核心技能叫事实翻译法：把对方说的事实，翻译成他背后的感受。对方说今天跑了五公里，事实回应是「不错，坚持锻炼」；感受翻译是「五公里啊，跑完肯定特别爽吧，那种出汗的感觉太解压了」。</p>
  <p>同事晒新包，事实回应「挺好看的」；感受翻译则是「这个包太适合你了，背上特别有气质，你眼光可真好」。作业：找十个对话场景，每个都练习把事实译成感受。公式记一句——说出对方的情绪，再加上你的认同。</p>
  {figs(5)}
</section>

<section class="story-section" id="ch5">
  <h2><span class="time-marker">03:10–04:08</span>第四天：适度夸张，并一定要配语气词</h2>
  <p>会聊天的人懂一个秘密：适度夸张。不是瞎吹，而是把感受放大一点点，让对方感到你真的很在意。朋友说吃了顿好吃的，别说「不错」，要说「天呐，你也太幸福了吧，我现在就想冲过去蹭一口」；朋友说加班很累，别只说「辛苦了」，要说「哇，这强度也太恐怖了吧，你真的是太能扛了」。</p>
  <p>今天练五个场景，每个都用夸张词回应。夸张词包括：太、超级、简直、绝了、爆了、疯了。但作者特别提醒——夸张词一定要配合语气词，比如「天呐」「我的妈呀」，这样才不会显得很假。</p>
  {figs(6)}
</section>

<section class="story-section" id="ch6">
  <h2><span class="time-marker">04:08–04:50</span>第五天：挖掘隐藏情绪，说话是为了共鸣</h2>
  <p>第五天进入进阶：学会听出对方话里的隐藏情绪。很多人说话时，表面和真正想要的并不一样。对方说「我最近在学画画」，表面上是在分享，实际上可能在期待你的认可——你可以回「哇，你还会画画呀，太厉害了吧，改天给我画一张呗」。</p>
  <p>作业是找出三段对话，每段分析对方的隐藏情绪，再用感受去回应。作者钉下一句立场鲜明的话：说话的目的不是传递信息，而是寻求共鸣。（此为作者观点，职场正式沟通仍需以信息准确为先。）</p>
  {figs(7)}
</section>

<section class="story-section" id="ch7">
  <h2><span class="time-marker">04:50–05:47</span>第六天：共同体验法，把经历连起来</h2>
  <p>第六天学「共同体验法」：把对方的经历和你的经历连接起来，瞬间拉近距离。对方说周末去爬山了，别只说「哎呀真好」；要说爬山真的太爽了，上次爬完那种浑身酸爽的感觉现在想起来都很怀念，你是不是也有这种感觉？</p>
  <p>对方说最近在追剧，可以说「哎我懂我懂，追剧那种停不下来的感觉呀，恨不得一口气看完；你现在是不是也在纠结要不要熬夜把它看完？」作业：五个场景，每个都用「我也」「我懂」「我上次也这样」开头，让对方觉得你不是在敷衍，而是真的理解他。</p>
  {figs(8)}
</section>

<section class="story-section" id="ch8">
  <h2><span class="time-marker">05:47–06:37</span>第七天：情绪反馈，结成情绪共同体</h2>
  <p>第七天练「情绪反馈」：你不仅要表达自己的感受，还要告诉对方——他的感受给你带来了什么样的情绪。对方分享好消息，可以说「听到这个消息，我都替你开心，感觉自己也跟着沾光了」；对方吐槽烦心事，可以说「听你这么说，我都跟着生气了，真的是太气人了」。</p>
  <p>技巧的核心是让对方知道：他的情绪影响到了你，你们是情绪共同体。作业：找出三个场景，每个加上「我听了 / 我看到 / 知道后」这样的开头，再说出你的情绪反应。</p>
</section>

<section class="story-section" id="ch9">
  <h2><span class="time-marker">06:37–07:34</span>第八天：追问感受，别让话题停在事实层</h2>
  <p>第八天要练的是：不要让话题停在事实层面，要往感受层面追问。对方说今天开会被领导表扬了，别只说「哎呀恭喜」——要追问「那你当时是什么感受啊？是不是觉得特别爽？有没有那种被看见的感觉？」</p>
  <p>对方说周末在家躺了两天，别说「真好」，要问「躺了两天是不是感觉特别放松？有没有那种终于能喘口气的感觉？」作业：五个对话，每个在对方说完事实后追问一句感受。公式是：你当时是什么感觉 / 是不是特别…… / 有没有那种感觉——话题就能从表面深入到情绪。</p>
  {figs(9)}
</section>

<section class="story-section" id="ch10">
  <h2><span class="time-marker">07:34–08:49</span>第九天：四步流程实战，闲聊核心是读情绪</h2>
  <p>第九天要把前面所学全部用上：找三个真实场景（评论区或面对面），按流程走——先用感受词开头，再翻译对方的情绪，接着联结你的体验，最后追问对方的感受。示范：朋友说今天被领导批评了，可以回「哎呀那太难受了吧，被批评那种感觉真的让人很憋屈；我以前也遇到过，当时整个人都不好了；你现在还好吗？有没有感觉特别的委屈？」目标是让这套流程变成本能反应。</p>
  <p>若想熟练掌握这套沟通逻辑，作者建议去读一读《学会闲聊》（作者推荐书名，具体版本未在视频中核验）。很多人误以为闲聊是寻找话题，真正的核心是读懂言语背后的情绪，持续提供情绪价值；书里大量生活化案例帮你更快打通聊天思维。</p>
  {figs(10)}
</section>

<section class="story-section" id="ch11">
  <h2><span class="time-marker">08:49–09:46</span>第十天：总结固化——一个月每天三次感受回应</h2>
  <p>最后一天总结：聊天不聊事实，聊的是情绪、感受和共鸣。回顾这十天，看哪个环节最顺手、哪个还要加强；然后给自己定一个小目标——接下来一个月，每天至少用三次感受回应法，让它彻底成为聊天习惯。</p>
  <p>作者说：当你开始关注情绪而不是事实，身边的人就会越来越愿意跟你聊天，因为跟你聊天很舒服，聊完之后心情好——这就是社交中的核心竞争力。片尾自我介绍：「我是叶子，一个50岁从低谷爬起来的自己。」末句 Whisper 识别严重断裂，正文不采信；完整口播以转录区原文为准。</p>
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
            ("ch1", "开场：十天情绪价值"),
            ("ch2", "第一天：事实vs感受"),
            ("ch3", "第二天：感受词"),
            ("ch4", "第三天：事实翻译"),
            ("ch5", "第四天：适度夸张"),
            ("ch6", "第五天：隐藏情绪"),
            ("ch7", "第六天：共同体验"),
            ("ch8", "第七天：情绪反馈"),
            ("ch9", "第八天：追问感受"),
            ("ch10", "第九天：四步实战"),
            ("ch11", "第十天：固化习惯"),
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
    <span class="meta-tag tag-topic">职场社交 · 情绪价值 · 闲聊</span>
  </div>
  <p style="color:#57534e;font-size:14px;margin:0 0 12px">作者 叶子认知思维 · 2026-10-13</p>
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
        <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差；正文已按语境校正（如「进阶」「沾光」「联结」），转录区保持原样以便核对。末句识别严重断裂，未采信进正文。</p>
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
