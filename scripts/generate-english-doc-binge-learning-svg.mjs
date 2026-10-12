#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'english-doc-binge-learning-理性分析.svg');
const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:34px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p,li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
ul,ol{padding-left:24px;margin:8px 0}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:18px 24px;text-align:center;min-width:140px;font-weight:700;font-size:15px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:28px;margin-bottom:16px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:18px;font-weight:700;color:#1e40af;margin-bottom:10px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:10px 0;font-size:14px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:10px 0;font-size:14px;color:#991b1b;border-left:4px solid #ef4444}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
th{background:#f1f5f9;padding:12px 14px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 14px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:28px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}
.conclusion h3{color:rgba(255,255,255,.9);margin:16px 0 8px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9)}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:28px 0 12px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:20px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

const esc = (s) => String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');

const d = {
  title: '超下饭英文纪录片｜边看边学英语',
  duration: '3分25秒',
  url: 'https://b23.tv/sQSCjkh',
  tags: ['英语学习', '纪录片', 'Explained', 'F1', 'OJ'],
  perspective: '理性分析 · 语言输入',
  summary: '核心判断：英语进步来自「用英语学感兴趣的事」，不是刷题；三部纪录片分别训练短知识拼图、产业叙事+口音包容、长篇社会反思。',
  timeline: [
    ['00:05', '用英语学感兴趣内容'],
    ['00:24', 'Explained：20分钟/集'],
    ['00:41', '话题覆盖电竞到股市'],
    ['01:19', 'Drive to Survive'],
    ['02:10', '口音不重要，说清想法'],
    ['02:20', 'OJ Made in America'],
    ['03:08', '把自己放进语言里'],
  ],
  map: [
    ['问题', '英语怎么真进步'],
    ['证据', '三部片三种输入'],
    ['判断', '兴趣>题海'],
    ['行动', '选一部追完'],
  ],
  corrections: [
    '误解：学英语=刷教材剧。纠偏：用英语学世界运作更有效。',
    '误解：口音标准才算会说。纠偏：F1 访谈证明说清想法优先。',
    '误解：英文纪录片优于中文。纠偏：口播明确「那不是重点」。',
  ],
  cards: [
    { title: '在讲什么：兴趣驱动输入', body: '把英语当获取历史/经济/娱乐知识的介质；纪录片比剧更适合「学东西」。', quote: 'use English to learn something that you are generally interested in', relation: '先选兴趣，再选材料。', tone: 'card-purple' },
    { title: '三部片分工', body: 'Explained=短平快世界观拼图；F1=产业叙事+多口音；OJ=长篇社会与名人文化。', quote: 'accent is not important. What matters most is whether you can get your ideas across', relation: '按目标选片：词汇面 / 听力口音 / 深度议题。', tone: 'card-blue' },
    { title: '怎么用：一周追一季短片', body: '学生/职场都可从 Explained 开始；做笔记用英语写「本集三个事实+一个观点」。', quote: 'you need to put yourself inside that language from the very beginning', relation: '输出挂钩：用片中话题练一段 60 秒口述。', tone: 'card-green' },
    { title: '边界：个人片单非权威榜', body: '三部为 UP 主观最爱；版权与地区可用性因平台而异；犯罪纪录片含敏感内容需自辨。', quote: 'That is not the point.', relation: '可替换同结构片单，方法可迁移。', tone: 'card-orange' },
  ],
  table: {
    title: '三部纪录片对照',
    head: ['片', '时长形态', '英语训练点', '知识收益'],
    rows: [
      ['Explained', '约20分钟/集', '清晰发音、话题词汇', '跨领域世界观拼图'],
      ['Drive to Survive', '多季叙事', '多口音听力、产业用语', '理解陌生高 tip 产业'],
      ['OJ Made in America', '约1小时/集', '长听力与反思停顿', '美国社会与名人文化'],
    ],
  },
  boundary: ['推荐基于个人口味。', '不替代系统语法课程，作大量可理解输入。'],
  pitfalls: ['只收藏不追完。', '为「练发音」回避非母语口音材料。', '把纪录片当刷剧不记任何输出。'],
  conclusion: {
    key: ['兴趣是输入引擎。', '三部片覆盖短/中/长叙事。', '把自己放进语言里。'],
    actions: ['本周看完 3 集 Explained 并英语记三条事实。', '选一季 F1 听口音不暂停纠音。', 'OJ 每集后写一句社会观察（中或英）。'],
    shift: '从「学英语」转向「用英语学世界」。',
  },
};

function body(data) {
  const tags = data.tags.map((t,i)=>`<span class="tag ${['tag-blue','tag-green','tag-orange','tag-purple','tag-red'][i%5]}">${esc(t)}</span>`).join('');
  const timeline = data.timeline.map(([t,x])=>`<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`).join('');
  const map = data.map.map(([a,b],i)=>{const cls=['node','node-green','node-orange','node'][i%4];const ar=i<data.map.length-1?'<span class="arrow">→</span>':'';return `<div class="${cls}">${esc(a)}<br/>${esc(b)}</div>${ar}`;}).join('');
  const corr = data.corrections.map(c=>`<p>${esc(c)}</p>`).join('');
  const cards = data.cards.map(c=>`<div class="card ${c.tone}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p><div class="quote">${esc(c.quote)}</div><div class="relation">${esc(c.relation)}</div></div>`).join('');
  const thead=`<tr>${data.table.head.map(h=>`<th>${esc(h)}</th>`).join('')}</tr>`;
  const tbody=data.table.rows.map(r=>`<tr>${r.map(c=>`<td>${esc(c)}</td>`).join('')}</tr>`).join('');
  const bound=data.boundary.map(b=>`<li>${esc(b)}</li>`).join('');
  const pits=data.pitfalls.map(p=>`<div class="pitfall">${esc(p)}</div>`).join('');
  const key=data.conclusion.key.map(k=>`<li>${esc(k)}</li>`).join('');
  const act=data.conclusion.actions.map(a=>`<li>${esc(a)}</li>`).join('');
  return `<div class="container root-wrap"><h1>${esc(data.title)}</h1><div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(data.duration)}</span><span class="tag tag-gray">${esc(data.perspective)}</span></div><a class="source-link" href="${esc(data.url)}">原视频</a><div class="summary-line">${esc(data.summary)}</div><div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div><div class="map"><h2>核心脉络</h2><div class="diagram">${map}</div></div><div class="correction"><h3>常见误解与认知纠偏</h3>${corr}</div><div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div><div class="section"><h2 class="sec-title">${esc(data.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div><div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${bound}</ul>${pits}</div></div><div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${key}</ul><h3>行动清单</h3><ol>${act}</ol><h3>关键认知转变</h3><p>${esc(data.conclusion.shift)}</p></div><div class="footer">双轨产物之二 · 理性分析 · ${esc(data.duration)}</div></div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: body(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated', OUT, height);
fs.writeFileSync(path.join(DIR, '..', '_work/b61/english-doc-height.txt'), String(height));
