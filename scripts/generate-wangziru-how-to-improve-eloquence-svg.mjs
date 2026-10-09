#!/usr/bin/env node
/** 单篇：王自如聊口才如何变好 → 理性分析 SVG */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'wangziru-how-to-improve-eloquence-理性分析.svg');

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}
.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}
.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:160px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}
.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}
.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
tr:nth-child(even) td{background:#fafbfc}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

const d = {
  title: '王自如聊口才如何变好',
  duration: '1分29秒',
  url: 'https://xhslink.cn/o/4HOOivj1BL9',
  tags: ['口才', '表达', '思维方式', '写稿', 'storytelling'],
  perspective: '理性分析 · 职场沟通',
  summary:
    '核心判断：表达能力的瓶颈很少是「口才技巧」，而是思维高度、逻辑训练与写作推敲；演讲课的总分总只提供形式外壳，内涵与关联才决定说话是否失败。',
  timeline: [
    ['00:04', '重点放错了：别只练口才'],
    ['00:12', '不是口齿，是思维与思想'],
    ['00:16', '慢说话亦可穿透'],
    ['00:26', '总分总一二三四的形式逻辑'],
    ['00:40', '无内涵无关联=失败表达'],
    ['00:50', 'ZEALER 写稿改思维'],
    ['01:12', 'Storytelling 与节奏感'],
    ['01:24', '15字/25字与声调推敲'],
  ],
  map: [
    ['问题', '口才如何变好'],
    ['证据', '思维＞口齿；写稿＞套路'],
    ['判断', '形式逻辑≠好表达'],
    ['行动', '写通想法再开口'],
  ],
  corrections: [
    '误解：表达强=口才好。纠偏：文字力与感染力来自思维方式与思想高度。',
    '误解：上演讲课学会总分总就有条理。纠偏：无思维训练的一二三四只剩外壳，细听无内涵。',
    '误解：练语速、口齿最重要。纠偏：慢说话也可有穿透力，关键是思想高度。',
    'ASR：ZILLER→ZEALER（王自如科技媒体品牌）。',
  ],
  cards: [
    {
      title: '在讲什么：训练对象换轨',
      body: '把「练口才」改成「练思维」。写得好不好、说得有没有感染力，是思想问题不是口齿问题。',
      quote: '一个人的表达不是口才问题……不是口齿的问题。',
      relation: '理解：技巧课解决外壳，内容课解决内核。',
      tone: 'card-purple',
    },
    {
      title: '关键理解：形式逻辑的失败判据',
      body: '总分总、一二三四听起来有逻辑，但内容无内涵、无关联，反而是失败说话。',
      quote: '仔细听了把内容里边是毫无内涵毫无关联性可言的。',
      relation: '判据：听完能否复述「为什么」而不只是「第几点」。',
      tone: 'card-blue',
    },
    {
      title: '怎么用：写稿→Storytelling 推敲',
      body: '用写作逼思维落地；脑子想通却写不清=表达垃圾。进阶练讲故事节奏：句尾留白的字数与声调都要推敲。',
      quote: '到底是用15个字还是25个字，最后一个词是应该用第几声结束。',
      relation: '行动：每周把一个想法写成可进片的短段落。',
      tone: 'card-green',
    },
    {
      title: '边界：经验叙事非万能课纲',
      body: '观点来自王自如个人内容创业路径（ZEALER、《科技相对论》），强调写稿与叙事工匠，不否定必要的表达技巧课，也不等于学术传播学结论。',
      quote: '说话可能是一个被训练的过程。',
      relation: '适用：内容创作者、汇报表达；弱适用：即兴辩论口齿专项。',
      tone: 'card-orange',
    },
  ],
  table: {
    title: '练口才 vs 练表达内核',
    head: ['维度', '口才课倾向', '王自如强调'],
    rows: [
      ['训练对象', '语速、条理外壳、总分总', '思维方式、思想高度、写作'],
      ['成功表象', '一二三四听起来有逻辑', '有内涵、有关联、可进片'],
      ['失败信号', '不会套模板', '想通却写不清/说不清'],
      ['进阶手艺', '更多演讲套路', 'Storytelling 节奏与句尾推敲'],
    ],
  },
  boundary: [
    '短片经验分享，非系统沟通课程。',
    '「写稿改思维」对内容创作者更直接，职场口头汇报仍需场景练习。',
    '不否定基础表达技巧，只反对把技巧当全部。',
  ],
  pitfalls: [
    '只背总分总结构，不检查内容是否有因果与证据。',
    '把慢说当成缺点，忽视思想密度。',
    '脑子有感觉但不落笔，长期无法进片子/作文。',
  ],
  conclusion: {
    key: [
      '表达瓶颈多在思维，不在口齿。',
      '形式条理≠有内涵的好表达。',
      '写稿与叙事推敲是可复用训练路径。',
    ],
    actions: [
      '下周选一个工作观点，写成 200 字可口播稿再念。',
      '听别人演讲时只记：内涵一句 + 关联一句，忽略点数。',
      '关键句尾试写 15 字版与 25 字版，对比留白效果。',
    ],
    shift: '从「我要练口才」转向「我要把想通的事写清楚、讲成故事」。',
  },
};

function buildBody(data) {
  const tags = (data.tags || [])
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`)
    .join('');
  const timeline = (data.timeline || [])
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const mapNodes = (data.map || [])
    .map(([label, x], i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node'][i % 4];
      const arrow = i < data.map.length - 1 ? '<span class="arrow">→</span>' : '';
      return `<div class="${cls}">${esc(label)}<br/>${esc(x)}</div>${arrow}`;
    })
    .join('');
  const corrections = (data.corrections || []).map((c) => `<p>${esc(c)}</p>`).join('');
  const cards = (data.cards || [])
    .map(
      (c) => `<div class="card ${c.tone || ''}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p>${
        c.quote ? `<div class="quote">${esc(c.quote)}</div>` : ''
      }${c.relation ? `<div class="relation">${esc(c.relation)}</div>` : ''}</div>`
    )
    .join('');
  const thead = `<tr>${data.table.head.map((h) => `<th>${esc(h)}</th>`).join('')}</tr>`;
  const tbody = data.table.rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
  const boundary = data.boundary.map((b) => `<li>${esc(b)}</li>`).join('');
  const pitfalls = data.pitfalls.map((p) => `<div class="pitfall">${esc(p)}</div>`).join('');
  const key = data.conclusion.key.map((k) => `<li>${esc(k)}</li>`).join('');
  const actions = data.conclusion.actions.map((a) => `<li>${esc(a)}</li>`).join('');

  return `<div class="container root-wrap">
  <h1>${esc(data.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(data.duration)}</span><span class="tag tag-gray">${esc(data.perspective)}</span></div>
  <a class="source-link" href="${esc(data.url)}">原视频</a>
  <div class="summary-line">${esc(data.summary)}</div>
  <div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>
  <div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">${esc(data.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul>${pitfalls}</div></div>
  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${key}</ul><h3>行动清单</h3><ol>${actions}</ol><h3>关键认知转变</h3><p>${esc(data.conclusion.shift)}</p></div>
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自同一 Whisper 转录 · ${esc(data.duration)}</div>
</div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: buildBody(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.writeFileSync(path.join(DIR, '..', '_wangziru_svg_height.txt'), String(height), 'utf8');
