#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'language-shapes-thinking-理性分析.svg');

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
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
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:140px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

const esc = (s) => String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');

const d = {
  title: '全英｜语言决定了你的思维',
  duration: '3分25秒',
  url: 'https://b23.tv/VzNHL8C',
  tags: ['语言', '外语效应', '情绪粒度', '内耗', '维特根斯坦'],
  perspective: '理性分析 · 认知与沟通',
  summary: '核心判断：内耗与冲动反应常被「粗粒度标签语言」放大；外语效应与更细的情绪描述，是两套可切换的认知距离调节器。',
  timeline: [
    ['00:08', '说英语像换了一个人'],
    ['00:21', '外语效应：母语情绪更重'],
    ['00:45', 'Perry Link：英汉名词化差异'],
    ['01:10', '名词句式拉开情绪距离'],
    ['01:48', '算法偏爱极端标签'],
    ['02:20', '具体感受 vs 贴标签'],
    ['02:45', '情绪粒度与身心健康'],
    ['03:18', '语言边界=世界边界'],
  ],
  map: [
    ['问题', '内耗从哪来'],
    ['证据', '外语效应+标签机制'],
    ['判断', '语言粒度决定反应'],
    ['行动', '换词=换模板'],
  ],
  corrections: [
    '误解：学语言只为考试。纠偏：口播强调无意识地改变情绪处理模板。',
    '误解：贴标签能精准确认感受。纠偏：单字标签服务算法，压缩人类体验。',
    'ASR：neha→内耗；Lisa→Lisa Feldman Barrett；Wiggenstein→Wittgenstein。',
  ],
  cards: [
    { title: '在讲什么：两套距离机制', body: '外语效应用二语拉开情绪；名词化/细描述用句法拉开情绪。共同点是「不沉浸在母语情绪编码里」。', quote: 'The limits of my language means the limits of my world.', relation: '理解：语言是情绪操作系统，不是装饰。', tone: 'card-purple' },
    { title: '关键理解：粒度对抗极化', body: '算法奖励极端关键词；情绪粒度研究显示更细描述→更少冲动、更好身心。', quote: "people who can describe emotions with more specification are less likely to react impulsively", relation: '判据：你能否不用一个词讲清此刻身体与念头。', tone: 'card-blue' },
    { title: '怎么用：替换标签句', body: '把「我好内耗」改成「我不同意X，脑子乱，体温升」。英语练习时可刻意用二语复盘冲突。', quote: 'I notice my body temperature going up.', relation: '行动：冲突后写三句具体感受再贴标签。', tone: 'card-green' },
    { title: '边界：科普短片非临床', body: '外语效应与情绪粒度为研究线索的口播科普，不构成心理治疗；英汉对比取 Perry Link 一书视角，非全面语言学结论。', quote: 'learning language is not all about taking exams', relation: '适用：自我观察与表达训练。', tone: 'card-orange' },
  ],
  table: {
    title: '粗标签 vs 细描述',
    head: ['维度', '粗标签', '细描述'],
    rows: [
      ['例子', '内耗 / 愤怒 / 内卷', '不同意、脑子乱、体温升'],
      ['算法友好', '高（可索引）', '低'],
      ['情绪距离', '易被点燃', '更易观察'],
      ['健康相关', '口播指向更差冲动控制', '更高情绪粒度'],
    ],
  },
  boundary: ['英文口播的研究转述，非系统综述。', '「学语言变更好的人」是修辞结论，需个人验证。'],
  pitfalls: ['用二语压抑情绪当唯一策略。', '为了细描述而过度分析拖延行动。', '把算法标签原样搬进自我对话。'],
  conclusion: {
    key: ['语言调节情绪距离。', '标签服务算法，粒度服务健康。', '语言窄则世界窄。'],
    actions: ['冲突后先写三句具体感受。', '本周用英语复盘一次情绪事件。', '发帖前删掉唯一极端标签词再写正文。'],
    shift: '从「我是什么标签」转向「此刻身体与念头具体发生了什么」。',
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
console.log('Generated', OUT, 'height', height);
fs.writeFileSync(path.join(DIR,'..','_work/b61/language-shapes-height.txt'), String(height));
