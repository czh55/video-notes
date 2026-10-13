#!/usr/bin/env node
/**
 * b62q：生成 afternoon-photo-find-light 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'afternoon-photo-find-light-理性分析.svg');

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:32px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:24px;font-weight:700;color:#1e40af;margin:28px 0 14px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:18px;font-weight:700;color:#334155;margin-bottom:10px}
p,li{font-size:15px;line-height:1.75;color:#475569;margin-bottom:6px}
ul,ol{padding-left:22px}
.tag{display:inline-block;padding:4px 12px;border-radius:18px;font-size:12px;font-weight:600;margin-right:6px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:10px 0 16px}
.summary-line{font-size:17px;line-height:1.7;padding:18px 22px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:18px;color:#334155;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:14px;padding:20px 24px;margin-bottom:18px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline-item{display:flex;gap:12px;padding:6px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:13px;font-weight:700;color:#3b82f6;min-width:64px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:14px;color:#475569}
.map{background:#fff;border-radius:18px;padding:28px;margin-bottom:20px;box-shadow:0 4px 20px rgba(0,0,0,.05)}
.map h2{margin-top:0;border:none;padding:0}
.diagram{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;align-items:center;padding:16px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:14px;padding:14px 18px;text-align:center;min-width:140px;font-weight:700;font-size:14px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.node-purple{background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-color:#c4b5fd;color:#5b21b6}
.arrow{font-size:22px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:16px 20px;border-radius:12px;margin-bottom:18px}
.correction h3,.correction p{color:#92400e}
.sec-title{font-size:20px;font-weight:700;color:#1e40af;margin:8px 0 14px;padding-left:12px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:14px;padding:22px;margin-bottom:14px;border-left:5px solid #3b82f6;box-shadow:0 3px 16px rgba(0,0,0,.04)}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:16px;color:#1e40af;margin-bottom:8px}
.card .quote{background:#f8fafc;padding:10px 12px;border-radius:8px;margin:8px 0;font-size:13px;color:#64748b;border-left:3px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 12px;border-radius:8px;font-size:13px;color:#166534;margin:6px 0}
.card .pitfall{background:#fef2f2;padding:10px 12px;border-radius:8px;margin:8px 0;font-size:13px;color:#991b1b;border-left:3px solid #ef4444}
.card .action{background:#eff6ff;padding:10px 12px;border-radius:8px;margin:8px 0;font-size:13px;color:#1e40af;border-left:3px solid #3b82f6}
table{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}
th{background:#f1f5f9;padding:10px 12px;text-align:left;color:#1e40af}
td{padding:10px 12px;border-bottom:1px solid #e2e8f0;vertical-align:top;color:#475569}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:18px;padding:28px;margin-top:20px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}
.conclusion h3{color:rgba(255,255,255,.92);margin:14px 0 8px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.92)}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:20px 0 8px}
.source-link{color:#3b82f6;font-size:13px;text-decoration:none;display:inline-block;margin-bottom:12px}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

const esc = (s) => String(s ?? '')
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;');

const d = {
  title: '下午拍照怎么找光线',
  duration: '1分27秒',
  url: 'https://xhslink.cn/o/8itigYhyWET',
  tags: ['摄影', '用光', '下午光', '人像', '硬光', '逆光'],
  perspective: '理性分析 · 摄影用光',
  summary:
    '核心命题：下午街拍人像，关键不是「有没有太阳」，而是光质是否过硬、太阳是否入画。硬侧光（半边脸亮、三角光斑、眯眼）与完全逆光都应避开；可执行动作是挡光源，或贴墙进入阴影主动找相对好看的光。证据以画面字幕与站位演示为主，Whisper 口播极短。',
  timeline: [
    ['00:00', '提醒：这种光线不要拍'],
    ['00:03', '半边脸亮 / 要避免的硬侧光'],
    ['00:15', '模特眯眼；脸颊三角光斑'],
    ['00:30', '看硬边缘；讨论相对好看的光'],
    ['00:51', '完全逆光（太阳入画）也不推荐'],
    ['01:00', '用手挡住太阳光源'],
    ['01:12', '贴墙进阴影 = 避开直射'],
    ['01:24', '收束：应该去找合适的光'],
  ],
};

const timelineHtml = d.timeline
  .map(
    ([t, text]) =>
      `<div class="timeline-item"><div class="timeline-time">${esc(t)}</div><div class="timeline-text">${esc(text)}</div></div>`
  )
  .join('');

const tagsHtml = d.tags
  .map((t, i) => {
    const cls = ['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red', 'tag-gray'][i % 6];
    return `<span class="tag ${cls}">${esc(t)}</span>`;
  })
  .join('');

const body = `
<div class="container root-wrap">
  <h1>${esc(d.title)}</h1>
  <div class="meta">${tagsHtml}
    <span class="tag tag-gray">${esc(d.duration)}</span>
    <span class="tag tag-blue">${esc(d.perspective)}</span>
  </div>
  <a class="source-link" href="${esc(d.url)}">原视频链接</a>
  <div class="summary-line">${esc(d.summary)}</div>

  <div class="timeline">
    <h3>关键证据时间轴</h3>
    ${timelineHtml}
  </div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">
      <div class="node">下午有太阳？</div>
      <div class="arrow">→</div>
      <div class="node node-orange">光质硬 / 太阳入画？</div>
      <div class="arrow">→</div>
      <div class="node node-purple">避开或挡光</div>
      <div class="arrow">→</div>
      <div class="node node-green">进阴影找相对好看的光</div>
    </div>
  </div>

  <div class="correction">
    <h3>避坑总结 · 常见误解纠偏</h3>
    <p>「下午阳光好 = 适合拍人像」不成立：直射侧光会半边脸过曝、三角光斑、模特眯眼；「逆光一定高级」也不成立——把太阳拍进画面的完全逆光，作者明确不推荐。</p>
  </div>

  <div class="section">
    <h2 class="sec-title">观点卡片</h2>

    <div class="card card-red">
      <h3>硬侧光是要避开的光线</h3>
      <p><strong>在讲什么：</strong>下午侧向直射把脸切成明暗两半，并留下三角光斑。</p>
      <p><strong>关键理解：</strong>问题不在「有光」，而在光太硬、过渡太陡，破坏面部可读性与表情。</p>
      <p><strong>怎么用：</strong>开拍前先看半边脸是否过亮、模特是否眯眼、脸颊是否出现怪异高光块。</p>
      <div class="quote">原文依据（字幕/口播）：「要避免的一个光线」「他一半脸亮」「三角形的光斑」「这种光线不要拍」</div>
      <div class="relation">立场：作者教学观点 + 可核验画面现象</div>
    </div>

    <div class="card card-orange">
      <h3>完全逆光（太阳入画）同样不推荐</h3>
      <p><strong>在讲什么：</strong>太阳落在模特脑后时，脸暗、眩光重。</p>
      <p><strong>关键理解：</strong>「找光」不等于追剪影；把光源本身拍进画面会抬高失败率。</p>
      <p><strong>怎么用：</strong>构图时检查太阳是否进入画面；若入画，优先改站位或挡光。</p>
      <div class="quote">原文依据（字幕）：「像这种完全的逆光也不推荐」「因为如果你把太阳拍进去了」</div>
      <div class="pitfall">边界：艺术向剪影/炫光创作不在本片讨论范围；结论针对常规人像出片。</div>
    </div>

    <div class="card card-green">
      <h3>挡不住太阳就贴墙进阴影</h3>
      <p><strong>在讲什么：</strong>用手挡光源；或站进建筑阴影避开直射。</p>
      <p><strong>关键理解：</strong>找光 = 控制主体与光源的相对位置，而不是等待「完美时段」。</p>
      <p><strong>怎么用：</strong>优先挡；不行就贴墙、进阴影，让街面强光留在背景。</p>
      <div class="quote">原文依据（字幕）：「太阳这个光源给挡住」「这不就把这个光源给避开了吗」「我们应该去找」</div>
      <div class="action">立刻可做：让模特退半步进墙影，对比直射下的眯眼与半脸高光。</div>
    </div>
  </div>

  <div class="card">
    <h3>横向对比：三种下午光位</h3>
    <table>
      <thead><tr><th>光位</th><th>画面特征</th><th>作者态度</th><th>适用边界</th></tr></thead>
      <tbody>
        <tr><td>硬侧光</td><td>半边脸亮、三角光斑、易眯眼</td><td>避免</td><td>本片人像教学场景</td></tr>
        <tr><td>完全逆光（太阳入画）</td><td>脸暗、轮廓炫、眩光</td><td>不推荐</td><td>非剪影创作意图时</td></tr>
        <tr><td>墙影/挡光后</td><td>主体离开直射，光相对柔</td><td>相对好看</td><td>有遮挡或建筑阴影可用时</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card card-purple">
    <h3>方法边界与证据层级</h3>
    <ul>
      <li><strong>可验证事实：</strong>直射侧光造成半脸高光与三角光斑；太阳入画形成完全逆光眩光；站入墙影可避开直射。</li>
      <li><strong>作者观点：</strong>上述两种光「不要拍/不推荐」；墙影结果「也比较好看」。</li>
      <li><strong>推断：</strong>「相对最好看」未给参数定义，宜理解为相对坏光的对照，而非黄金公式。</li>
      <li><strong>证据缺口：</strong>Whisper 仅 2 段非空碎片；细节依赖画面简体字幕。</li>
    </ul>
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <ul>
      <li>先判光质：硬侧光与太阳入画的完全逆光都是高风险。</li>
      <li>找光是站位问题：挡光源或进阴影，比死等黄金时段更可执行。</li>
    </ul>
    <h3>行动清单</h3>
    <ol>
      <li>开拍前看模特是否眯眼、脸是否一半过亮。</li>
      <li>取景时检查太阳是否进入画面；入画则改角度或挡光。</li>
      <li>用手/帽子/身体挡一下太阳，对比挡前后脸部层次。</li>
      <li>有墙或建筑时，让主体退入阴影，把强光留给背景。</li>
      <li>把「应该去找」落实为：每到一处先扫阴影与遮挡，再摆姿势。</li>
    </ol>
    <h3>关键认知转变</h3>
    <ul>
      <li>以前：下午阳光足就拍 → 现在：先问光硬不硬、太阳在不在画里。</li>
      <li>以前：逆光 = 高级感 → 现在：太阳入画的完全逆光，常规人像要慎用。</li>
      <li>以前：等完美光线 → 现在：挡一下、贴墙进阴影，主动制造可用光。</li>
    </ul>
  </div>

  <div class="footer">双轨分析 · 基于本地转录与画面字幕 · 不替代原视频</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
