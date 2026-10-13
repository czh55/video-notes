#!/usr/bin/env node
/**
 * b62o：生成 lazy-voice-two-fixes 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'lazy-voice-two-fixes-理性分析.svg');

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
  title: '说话声音懒散，没精神，两件事帮助改善',
  duration: '1分13秒',
  url: 'https://xhslink.cn/o/53Yg0UDxRtr',
  tags: ['职场表达', '咬字', '声音送远', '精气神', '演讲'],
  perspective: '理性分析 · 职场表达',
  summary:
    '核心命题：说话「懒散没精气神」时，优先练什么？作者给出可执行的双轨：咬字加力（双唇舌头、字边清晰、略斩钉截铁）+ 声音送远（拖音/抛物线/珠子隐喻）。证据层级为口播教学与字幕演示，属表达习惯建议，非医学或嗓音病理结论。',
  timeline: [
    ['00:00', '问题：声音懒洋洋、没精气神'],
    ['00:05', '框架：咬字 + 声音两个维度'],
    ['00:10', '咬字：力度、字边、双唇舌头'],
    ['00:28', '咬字目标感：斩钉截铁'],
    ['00:31', '送远：避免一说就结束'],
    ['00:45', '拖音 + 抛物线/珠子隐喻'],
    ['01:04', '结果：优雅感 → 精气神与形象感'],
  ],
  map: [
    ['问题', '懒散没精神'],
    ['维度A', '咬字加力'],
    ['维度B', '声音送远'],
    ['体感', '优雅/精气神'],
  ],
  corrections: [
    '误解：没精神=嗓子不够亮。纠偏：作者把问题拆成咬字松垮与声音「落地即灭」，先练口腔边界与送远路径。',
    '误解：送远=大声喊。纠偏：片中强调的是方向与延续（拖音、抛物线），不是音量竞赛。',
    '误解：斩钉截铁=凶或硬。纠偏：语境是咬字有力度、字边清楚，服务清晰度与精气神，不是情绪攻击。',
    '立场分层：操作隐喻（珠子/抛物线）可练习；「形象感一定改善」属作者观点，个体差异未验证。',
  ],
  cards: [
    {
      title: '在讲什么：用两个维度替代空练嗓',
      body: '关键理解：懒散是听感标签，真正可练的是咬字力度与声音运行方式。用法：自检时先问「字咬实了吗」「声音有没有送出去」，再决定练什么。',
      quote: '那你可以从两个维度去提升——一个是你的咬字，一个是你的声音',
      relation: '问题标签 → 可操作维度，避免「多练嗓」空转。',
      tone: 'card',
    },
    {
      title: '在讲什么：咬字加力与字边清晰',
      body: '关键理解：松松垮垮会让每个字边缘糊掉；双唇与舌头的力量感是咬清的物理抓手。用法：朗读时刻意加强唇舌阻力，追求一点点斩钉截铁，而不是含糊滑过。',
      quote: '让咬字有一点点斩钉截铁的感觉',
      relation: '口腔力量 × 字边清晰 = 听感上的「有精神」。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：声音送远与抛物线隐喻',
      body: '关键理解：反面是声音马上结束、掉到地面；正面是适度拖音、像抛物线把珠子扔远。用法：每句收尾前想象声音还在往前走，而不是落地灭火。',
      quote: '把自己的声音当做一个一个的珠子从自己的口腔扔出去',
      relation: '送远感 → 优雅感 → 精气神/形象感（作者因果链）。',
      tone: 'card-purple',
    },
    {
      title: '风险边界：这不是嗓音医疗建议',
      body: '关键理解：短片给的是表达与演讲习惯训练。若有声带不适、疼痛或病理问题，应就医，不要用「加力」「送远」硬扛。',
      quote: '整个人的精气神和这种形象感也就会因此得到一定的改善',
      relation: '教学观点 ≠ 疗效承诺；「一定改善」需降级为「可能改善」。',
      tone: 'card-orange',
    },
  ],
  compare: [
    ['维度', '练什么', '反面状态', '目标听感'],
    ['咬字', '双唇舌头力度、字边', '松松垮垮、字不清', '清晰、斩钉截铁'],
    ['声音', '送远、拖音、抛物线', '一说就结束、掉地', '优雅、有精气神'],
  ],
  actions: [
    '选一段日常自我介绍，慢读一遍，只检查「每个字边缘是否咬清」。',
    '第二遍只练送远：句尾留一点点拖音，想象声音沿抛物线出去。',
    '录音对比：是否从「落地灭」变成「还在往前」。',
    '开会发言前做 10 秒唇舌加力热身（轻声弹舌/夸张口型即可）。',
    '若练后喉咙痛，立刻减量并区分「口腔用力」与「喉部硬挤」。',
  ],
  pitfalls: [
    '把送远练成喊叫，喉部代偿，越练越累。',
    '只追求斩钉截铁却咬得过硬，听感生硬、不自然。',
    '忽略字边清晰，只加音量，懒散感依旧。',
    '把作者的「形象感改善」当成保证，忽视场景与个体差异。',
  ],
  shifts: [
    ['以前：觉得没精神就多喝水/清嗓', '现在：先查咬字松不松、声音送不送'],
    ['以前：把懒散归因于天生嗓音', '现在：拆成可练的口腔力度与送远路径'],
    ['以前：句尾急收像灭火', '现在：用抛物线/珠子隐喻把声音送远'],
  ],
};

const timelineHtml = d.timeline
  .map(
    ([t, text]) =>
      `<div class="timeline-item"><div class="timeline-time">${esc(t)}</div><div class="timeline-text">${esc(text)}</div></div>`,
  )
  .join('');

const mapHtml = d.map
  .map((node, i) => {
    const cls = i === 0 ? 'node' : i === d.map.length - 1 ? 'node-green' : i === 1 ? 'node-orange' : 'node-purple';
    const [a, b] = node;
    return `${i ? '<div class="arrow">→</div>' : ''}<div class="${cls}"><div>${esc(a)}</div><div style="font-size:12px;font-weight:600;margin-top:4px">${esc(b)}</div></div>`;
  })
  .join('');

const cardsHtml = d.cards
  .map(
    (c) => `<div class="card ${c.tone}">
  <h3>${esc(c.title)}</h3>
  <p>${esc(c.body)}</p>
  <div class="quote">${esc(c.quote)}</div>
  <div class="relation">${esc(c.relation)}</div>
</div>`,
  )
  .join('\n');

const tableHtml = `<table><tr>${d.compare[0].map((h) => `<th>${esc(h)}</th>`).join('')}</tr>${d.compare
  .slice(1)
  .map((row) => `<tr>${row.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`)
  .join('')}</table>`;

const body = `<div class="root-wrap"><div class="container">
  <h1>${esc(d.title)}</h1>
  <div class="meta">
    ${d.tags.map((t) => `<span class="tag tag-blue">${esc(t)}</span>`).join('')}
    <span class="tag tag-gray">${esc(d.duration)}</span>
    <span class="tag tag-purple">${esc(d.perspective)}</span>
  </div>
  <a class="source-link" href="${esc(d.url)}">原视频（小红书短链）</a>
  <div class="summary-line">${esc(d.summary)}</div>

  <div class="timeline"><h3>关键证据时间轴</h3>${timelineHtml}</div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">${mapHtml}</div>
  </div>

  <div class="correction">
    <h3>常见误解与认知纠偏</h3>
    ${d.corrections.map((x) => `<p>${esc(x)}</p>`).join('')}
  </div>

  <div class="section">
    <h2 class="sec-title">观点卡片</h2>
    ${cardsHtml}
  </div>

  <div class="card">
    <h3>横向对比：咬字 vs 送远</h3>
    ${tableHtml}
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <ul>
      <li>懒散没精神 → 先拆成咬字与声音两个维度。</li>
      <li>咬字：双唇舌头加力，字边清楚，略斩钉截铁。</li>
      <li>声音：送远、可带拖音，抛物线/珠子隐喻防「落地即灭」。</li>
    </ul>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>避坑</h3>
    <ul>${d.pitfalls.map((p) => `<li>${esc(p)}</li>`).join('')}</ul>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>
  <div class="footer">双轨产物 · 理性分析 · 证据来自 Whisper 转录与片内字幕</div>
</div></div>`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'lazy-voice-two-fixes-svg-height.txt'),
  String(height),
  'utf8',
);
