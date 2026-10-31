#!/usr/bin/env python3
"""生成 b66a ins-photo-composition-seen-vs-shot 双轨（纯图文）。"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ins-photo-composition-seen-vs-shot"
URL = "https://xhslink.cn/o/4rtXR1bE8MY"
TITLE = "ins风摄影构图·我看到的和我拍到的"
DATE = "2026-10-31"

# 每页：alt, 图注中文（页码徽章）, 英文翻译, 章节叙述要点
PAGES = [
    {
        "alt": "喷泉广角俯拍标注 what i see，黄框框住池角光斑与花瓣为 what i take",
        "cap": "广角看见整座喷泉与池面；黄框只取砖沿、绿瓦与一束阳光下的花瓣",
        "en": "Wide view of the whole fountain; the yellow frame keeps only the brick edge, green tiles, and sunlit petals",
        "claim": "看见的是场景，拍到的是光斑与局部秩序",
    },
    {
        "alt": "裁切后的喷泉池角：砖弧线、绿瓦、阳光束与水中花瓣硬币",
        "cap": "成片：对角线砖沿 + 光束切水 + 花瓣/硬币点缀，胶片颗粒与暖调压暗其余",
        "en": "Final frame: diagonal brick edge, a light beam on water, petals and coins as accents, film grain and warm grade",
        "claim": "裁切与调色把「杂乱池面」收成一条光的故事线",
    },
    {
        "alt": "街角广角标注 what i see，黄框框住门口红花麻袋盆栽为 what i take",
        "cap": "整条街道与门店入口一览无余；黄框只取柱角红花麻袋与绿植",
        "en": "Full street and shop entrance; the yellow frame isolates the red-flower sack and plants at the pillar corner",
        "claim": "行人与空街是干扰，角落静物才是构图核",
    },
    {
        "alt": "门口麻袋红花与石墙：侧光打亮袋面，背景绿植沉入阴影",
        "cap": "成片：低照度侧光勾勒麻袋质感，红花跳色，暗部吞掉杂乱背景",
        "en": "Final: sidelight sculpts the burlap, red blooms pop, shadows swallow the busy background",
        "claim": "曝光与暗部比「拍全门口」更能出情绪",
    },
    {
        "alt": "樱花树广角标注 what i see，黄框框住右中一团花簇为 what i take",
        "cap": "整树与步道行人尽入镜；黄框只截取被光打亮的一团重瓣花",
        "en": "Whole tree and path walkers; the yellow frame crops one sunlit cluster of double blossoms",
        "claim": "满树等于没重点，一团花才有主体",
    },
    {
        "alt": "暗背景中被侧光照亮的粉樱花簇特写",
        "cap": "成片：深影衬托粉樱，高光晕染花瓣，背景几乎消隐",
        "en": "Final: deep shadow behind pink sakura, soft highlight bloom on petals, background nearly gone",
        "claim": "用暗部做底板，让花成为唯一光源叙事",
    },
    {
        "alt": "室内廊道广角标注 what i see，黄框框住窗影几何光斑为 what i take",
        "cap": "窗景、栏杆、棋盘地砖全景；黄框只取斜切地面的窗框投影",
        "en": "Full hallway with window view and railing; the yellow frame keeps only the geometric window shadows on the floor",
        "claim": "地中海窗光的「形状」比窗外风景更可拍",
    },
    {
        "alt": "窗光斜影铺满瓷砖地面，窗外湖山与小船，胶片暖调",
        "cap": "成片：金色斜影铺地，窗外湖山作辅，颗粒与暖调统一情绪",
        "en": "Final: golden slanted shadows on tiles, lake and hills as secondary, grain and warm grade unify the mood",
        "claim": "光影几何是主，窗外风景降为陪衬",
    },
]

CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}.c{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}h1{font-size:28px;font-weight:800;color:#1c1917;margin-bottom:8px}.meta{color:#78716c;font-size:14px;margin-bottom:24px}.intro{font-size:17px;color:#44403c;line-height:1.9;margin-bottom:32px}img{display:block;max-width:100%;height:auto}figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}figcaption{padding:14px 18px;color:#57534e}h2{font-size:22px;font-weight:700;color:#1c1917;margin:32px 0 16px}h3{font-size:18px;font-weight:700;color:#1c1917;margin:28px 0 14px}.ss p{color:#44403c;margin-bottom:12px}.tb{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}.tb strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}.tb p{color:#1e40af;margin:0;font-size:15px}.sl{display:inline-block;color:#3b82f6;font-size:14px;text-decoration:none;margin-top:8px}.pair{background:#fff7ed;border-left:4px solid #f59e0b;border-radius:12px;padding:12px 16px;margin:16px 0;font-size:15px;color:#9a3412}@media(max-width:640px){.c{padding:28px 18px 56px}}"""

SVG_CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
p,li{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul{padding-left:24px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px;background:#dbeafe;color:#1e40af}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin:20px 0;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.card{background:#fff;border-radius:16px;padding:28px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);padding-bottom:8px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.92)}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}"""


def build_html() -> str:
    sections = []
    pairs = [
        (1, 2, "喷泉池角：整景 vs 光束局部"),
        (3, 4, "街角门口：空街 vs 红花麻袋"),
        (5, 6, "樱花树：满树 vs 一簇高光"),
        (7, 8, "廊道窗光：全景 vs 地面几何影"),
    ]
    for a, b, title in pairs:
        pa, pb = PAGES[a - 1], PAGES[b - 1]
        sections.append(f"""
      <h3>{title}</h3>
      <div class="pair">对照逻辑：{pa['claim']} → {pb['claim']}</div>
      <p>第 {a} 页用黄框标出「我拍到的」区域；第 {b} 页是裁切并调色后的成片——光比、颗粒与暗部共同完成从「看见」到「拍到」的转换。</p>
      <figure>
        <img src="assets/{SLUG}/shot-{a:02d}.jpg" alt="{pa['alt']}" loading="lazy">
        <figcaption>[{a}/8] {pa['cap']}</figcaption>
      </figure>
      <figure>
        <img src="assets/{SLUG}/shot-{b:02d}.jpg" alt="{pb['alt']}" loading="lazy">
        <figcaption>[{b}/8] {pb['cap']}</figcaption>
      </figure>""")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="四组 what I see / what I take：喷泉光斑、街角红花、樱花高光簇、廊道窗影——用裁切与调色把平凡场景收成可发布的构图。">
  <title>{TITLE}｜图文实录</title>
  <style>{CSS}</style>
</head>
<body>
<main class="c">
  <header>
    <h1>{TITLE}</h1>
    <div class="meta">纯图文 · 8 页 · 作者 Lee的审美积累 · 转载自 ins:jamtuna · 小红书 · {DATE}</div>
    <p class="intro">笔记用四组对照回答同一问题：眼睛扫到的是整片场景，相机该留下的往往是<strong>光、局部秩序与跳色</strong>。黄框标出「what i take」，下一张则是裁切 + 胶片感调色后的成片——喷泉池角的光束花瓣、门口麻袋红花、樱花树中的一簇高光、廊道地面的窗框斜影。</p>
    <a class="sl" href="{URL}" target="_blank" rel="noopener">→ 查看原笔记（小红书）</a>
  </header>
  <article>
    <h2>内容要点</h2>
    <p>方法可复用：先广角确认「看见了什么」，再框出唯一主体；曝光偏向侧光与暗部，让背景退场；调色用暖调与颗粒统一情绪，而不是把整景提亮。</p>
    <div class="tb"><strong>总结</strong><p>构图不是把看到的全装进画面，而是决定「只留下哪一块光」；调色服务于这个决定，把其余压暗。</p></div>
    <section class="ss">
      <h2>图文实录</h2>
      {''.join(sections)}
    </section>
  </article>
</main>
</body>
</html>
"""


def build_svg_body() -> str:
    rows = "".join(
        f"<tr><td>{i}/8</td><td>{p['claim']}</td></tr>" for i, p in enumerate(PAGES, 1)
    )
    return f"""
<div class="container">
  <h1>看见整景，拍下光的局部</h1>
  <div><span class="tag">构图</span><span class="tag">调色</span><span class="tag">ins 风</span></div>
  <p class="summary-line">四组 what I see → what I take：用黄框训练「取景眼」，再用侧光、暗部与胶片调色把局部做成可发布画面。</p>
  <div class="card">
    <h3>核心命题</h3>
    <p>摄影师与路人的差别，不在设备，而在是否敢于<strong>丢掉整景</strong>，只保留一条光影关系与一个跳色点。</p>
  </div>
  <div class="card">
    <h3>四组对照</h3>
    <table><tr><th>页</th><th>主张</th></tr>{rows}</table>
  </div>
  <div class="card">
    <h3>行动清单</h3>
    <div class="action">1. 广角先扫场 → 2. 黄框（或手指）框唯一主体 → 3. 等侧光/光束 → 4. 压暗背景再调色</div>
    <div class="pitfall">忌：把整条街、整棵树、整座喷泉「拍全」当完成；忌：全局提亮抹掉光比</div>
  </div>
  <div class="conclusion">
    <h2>结论</h2>
    <p>「我看到的」负责发现；「我拍到的」负责取舍。ins 风成立的条件是：主体清晰、光比戏剧、杂讯被暗部吞掉。</p>
  </div>
  <p class="footer">来源：小红书 · Lee的审美积累 · 转载 jamtuna</p>
</div>"""


def main() -> None:
    html_path = ROOT / "docs" / f"{SLUG}-图文实录.html"
    html_path.write_text(build_html(), encoding="utf-8")
    print("wrote", html_path)

    body = build_svg_body()
    tmp = ROOT / "_work" / "b66" / "b66a-svg-body.html"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(f"<style>{SVG_CSS}</style>{body}", encoding="utf-8")
    # node build
    script = ROOT / "_work" / "b66" / "build-b66a-svg.mjs"
    script.write_text(
        f"""
import {{ writeFileSync }} from 'fs';
import {{ buildSvg }} from '../../svg-auto-height.mjs';
const css = {json.dumps(SVG_CSS)};
const body = {json.dumps(body)};
const {{ svg, height }} = await buildSvg({{ css, body }});
writeFileSync({json.dumps(str(ROOT / "docs" / f"{SLUG}-理性分析.svg"))}, svg);
console.log('svg_height', height);
""",
        encoding="utf-8",
    )
    subprocess.check_call(["node", str(script)], cwd=str(ROOT))

    # translations partial
    part = {p["cap"]: p["en"] for p in PAGES}
    # keys in translations are without page badge - enhance strips [n/n]?
    # Check: TIME_RE only matches time. Page badges like [1/8] may stay in key.
    # Looking at enhance - it uses strip and TIME_RE. Page format [1/8] might not strip.
    # Sample image notes use [1/6] in cap-zh. translations keys are usually without badge.
    # extract strips time badge. For page badges, include full caption with badge as key OR without.
    # Safer: put both forms; enhance looks up chinese after removing time badge only.
    part2 = {}
    for i, p in enumerate(PAGES, 1):
        part2[f"[{i}/8] {p['cap']}"] = p["en"]
        part2[p["cap"]] = p["en"]
    (ROOT / "_work" / "b66" / "translations-partial").mkdir(parents=True, exist_ok=True)
    (ROOT / "_work" / "b66" / "translations-partial" / f"{SLUG}.json").write_text(
        json.dumps(part2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    tr_path = ROOT / "translations.json"
    tr = json.loads(tr_path.read_text(encoding="utf-8"))
    tr.update(part2)
    tr_path.write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("translations merged", len(part2))


if __name__ == "__main__":
    main()
