#!/usr/bin/env python3
"""b66b ins-photo-color-grade-keep-good-frames 双轨"""
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ins-photo-color-grade-keep-good-frames"
URL = "https://xhslink.cn/o/5md9r1wKVXs"
TITLE = "ins风摄影·调色：不要放弃构图不错但没调色的片子"
DATE = "2026-10-31"

PAGES = [
    ("松鼠逆光剪影 Yes vs 提亮细节 But", "同一树干松鼠：上为轮廓光剪影，下为提亮后见毛色条纹——构图在，调色决定戏剧还是说明", "Same squirrel on a log: silhouette rim light above vs lifted detail below—composition holds; grade picks drama or documentation"),
    ("大象水岸金线 Yes vs 头顶留白过多 But", "象在水岸金线中：上幅主体贴光带更稳，下幅天空负空间过大冲淡张力", "Elephant on a golden waterline: tighter to the light band above; excess sky below weakens tension"),
    ("哈欠虎雾林 Yes vs 欠曝灰雾 But", "打哈欠的虎：上为蓝雾聚光对比，下为欠曝灰绿——底片别扔，对比度与分区曝光可救", "Yawning tiger: blue-mist spotlight above vs underexposed mud below—don't trash flats; contrast and selective light can recover"),
    ("羚羊日落剪影 Yes vs 扁平暖金 But", "双羚剪影对日：上幅焦糖深橙高反差，下幅提亮发灰——剪影要靠压暗天空成立", "Two antelope vs sun: deep burnt-orange silhouette above vs washed gold below—silhouettes need a darker sky"),
    ("瀑布崖壁 Yes vs 雾霾平灰 But", "多级瀑布：上幅深绿高反差电影感，下幅灰雾扁平——同一构图，对比度即风格", "Cascades: deep green contrast above vs hazy flat below—same frame, contrast is the style"),
    ("雄狮草地 Yes vs 环境均亮 But", "趴卧雄狮：上幅压暗草地聚焦脸鬃，下幅环境均匀明亮——主体隔离靠减背景", "Lying lion: darkened grass spotlights face above vs evenly bright field below—isolate subject by killing the background"),
    ("雾林鹿 Yes vs 灰片无层次 But", "雾中鹿剪影：上幅冷蓝 vignette，下幅灰糊——情绪光比先于器材", "Deer in fog: cool blue vignette above vs grey mush below—mood contrast beats gear"),
    ("灰冠鹤 Yes vs 低饱和灰底 But", "双鹤侧脸：上幅青绿底+冠羽跳色，下幅灰蓝低饱和——背景色相决定贵气", "Crowned cranes: cyan field and crest pop above vs dull grey-blue below—background hue sells luxury"),
    ("双虎互动 Yes vs 雾霾 Raw But", "互嗅双虎：上幅高对比橙黑，下幅灰雾 Raw——野生题材更依赖后期对比", "Two tigers nuzzling: punchy orange-black above vs hazy raw below—wildlife leans on post contrast"),
    ("豹脸特写 Yes vs 过暖草绿 But", "正视豹：上幅偏冷电影绿，下幅过暖黄绿——色温选择即情绪选择", "Leopard stare: cooler cinematic green above vs warmer yellow-green below—white balance is mood"),
]

CSS = """*{box-sizing:border-box}body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}.c{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}h1{font-size:28px;font-weight:800;margin-bottom:8px}.meta{color:#78716c;font-size:14px;margin-bottom:24px}.intro{font-size:17px;color:#44403c;margin-bottom:32px}img{max-width:100%;display:block}figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.08)}figcaption{padding:14px 18px;color:#57534e}h2{font-size:22px;margin:32px 0 16px}h3{font-size:18px;margin:24px 0 12px}.tb{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}.sl{color:#3b82f6;font-size:14px;text-decoration:none}"""

SVG_CSS = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}.container{max-width:1200px;margin:0 auto}h1{font-size:34px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}h2{font-size:24px;color:#1e40af;margin:28px 0 14px}.summary-line{font-size:18px;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin:16px 0}.card{background:#fff;border-radius:16px;padding:28px;margin:16px 0;border-left:5px solid #3b82f6;box-shadow:0 4px 24px rgba(0,0,0,.06)}.card h3{color:#1e40af;margin-bottom:10px}.action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:10px 0;border-left:4px solid #3b82f6}.pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:10px 0;border-left:4px solid #ef4444;color:#991b1b}ul{padding-left:22px}li{margin:6px 0;color:#475569}.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:32px;margin-top:28px}.conclusion h2{color:#fff}.footer{text-align:center;color:#94a3b8;font-size:13px;padding:28px 0}"""


def main():
    figs = []
    for i, (title, cap, en) in enumerate(PAGES, 1):
        figs.append(f"""
      <h3>{i}/10 {title}</h3>
      <figure>
        <img src="assets/{SLUG}/shot-{i:02d}.jpg" alt="{title}" loading="lazy">
        <figcaption>[{i}/10] {cap}</figcaption>
      </figure>""")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="十组 Yes/But：构图已成立的野生题材，靠对比度、分区曝光与色温把 Raw 收成可发布的电影感。">
<title>{TITLE}｜图文实录</title><style>{CSS}</style></head><body><main class="c">
<header><h1>{TITLE}</h1>
<div class="meta">纯图文 · 10 页 · Lee的审美积累 · 小红书 · {DATE}</div>
<p class="intro">标题提醒：不要因为「看起来灰、暗、平」就删掉<strong>构图已经成立</strong>的片子。十组 Yes/But 对照同一取景——上幅用压暗背景、提对比、改色温做出情绪；下幅接近 Raw 或错误曝光。松鼠剪影、象与金线、虎与雾、日落羚羊、瀑布、狮、雾鹿、冠鹤、双虎、豹脸，全部说明：后期不是作弊，是完成构图承诺。</p>
<a class="sl" href="{URL}" target="_blank" rel="noopener">→ 查看原笔记（小红书）</a></header>
<article><h2>内容要点</h2>
<p>保留标准：主体位置与光位正确即可入库；放弃标准不该是「颜色还没出来」。调色优先做三件事：压背景、拉主体光比、选定冷暖情绪。</p>
<div class="tb"><strong>总结</strong><p>构图决定「能不能留」；调色决定「值不值得发」。Yes 不是另一种拍摄，是同一张底片的完成态。</p></div>
<section>{''.join(figs)}</section></article></main></body></html>"""
    (ROOT / "docs" / f"{SLUG}-图文实录.html").write_text(html, encoding="utf-8")

    rows = "".join(f"<li>{t}</li>" for t, _, __ in PAGES)
    body = f"""<div class="container">
<h1>构图留底，调色交货</h1>
<p class="summary-line">十组 Yes/But：野生题材同一构图，用对比度、分区曝光与色温把灰雾 Raw 收成可发布画面——不要删掉「构图不错但还没调色」的片子。</p>
<div class="card"><h3>核心命题</h3><p>删除键不该惩罚未完成的后期；该惩罚的是无主体、无光位的废片。</p></div>
<div class="card"><h3>十组对照</h3><ul>{rows}</ul></div>
<div class="card"><h3>行动清单</h3>
<div class="action">入库标准：主体清晰 + 光位成立 → 再谈调色；调色顺序：遮罩压背景 → 曲线对比 → 色温情绪。</div>
<div class="pitfall">忌：因欠曝/灰雾直接删除；忌：全局提亮抹掉剪影；忌：只加饱和不加对比。</div></div>
<div class="conclusion"><h2>结论</h2><p>Yes 是承诺兑现，But 是半成品。ins 风野生片的关键产能，藏在「敢留灰片」的工作流里。</p></div>
<p class="footer">小红书 · Lee的审美积累</p></div>"""
    script = ROOT / "_work/b66/build-b66b-svg.mjs"
    script.write_text(
        f"import {{writeFileSync}} from 'fs';\nimport {{buildSvg}} from '../../svg-auto-height.mjs';\n"
        f"const css={json.dumps(SVG_CSS)};\nconst body={json.dumps(body)};\n"
        f"const {{svg,height}}=await buildSvg({{css,body}});\n"
        f"writeFileSync({json.dumps(str(ROOT/'docs'/f'{SLUG}-理性分析.svg'))},svg);\nconsole.log('svg_height',height);\n",
        encoding="utf-8",
    )
    subprocess.check_call(["node", str(script)], cwd=str(ROOT))

    part = {}
    for i, (_, cap, en) in enumerate(PAGES, 1):
        part[cap] = en
        part[f"[{i}/10] {cap}"] = en
    (ROOT / "_work/b66/translations-partial").mkdir(parents=True, exist_ok=True)
    (ROOT / "_work/b66/translations-partial" / f"{SLUG}.json").write_text(
        json.dumps(part, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    tr = json.loads((ROOT / "translations.json").read_text(encoding="utf-8"))
    tr.update(part)
    (ROOT / "translations.json").write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # read height from last run via file? re-parse
    import re
    svg = (ROOT / "docs" / f"{SLUG}-理性分析.svg").read_text(encoding="utf-8")
    h = int(re.search(r'height="(\d+)"', svg).group(1))
    entry = {
        "date": DATE,
        "title": "ins风摄影·调色 不要放弃那些构图不错，但没有调色的",
        "summary": "十组 Yes/But：松鼠、象、虎、羚羊、瀑布、狮、鹿、冠鹤、双虎、豹——构图已成立的底片用对比度与色温完成，不要因灰雾删除。",
        "primary": "photography",
        "skills": [],
        "tags": ["调色", "构图", "ins风", "野生动物"],
        "platform": "xiaohongshu",
        "url": URL,
        "duration": "",
        "outputs": {"html": f"{SLUG}-图文实录.html", "svg": f"{SLUG}-理性分析.svg"},
        "screenshot_count": 10,
        "transcript_segments": 0,
        "svg_height": h,
        "slug": SLUG,
    }
    (ROOT / "_work/b66/index-entries").mkdir(parents=True, exist_ok=True)
    (ROOT / "_work/b66/index-entries" / f"{SLUG}.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("done", SLUG, "h", h)


if __name__ == "__main__":
    main()
