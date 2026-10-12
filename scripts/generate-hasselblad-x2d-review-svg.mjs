#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'hasselblad-x2d-review-理性分析.svg');
const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:32px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:24px;font-weight:700;color:#1e40af;margin:28px 0 14px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:18px;font-weight:700;color:#334155;margin-bottom:10px}
p,li{font-size:15px;line-height:1.75;color:#475569;margin-bottom:6px}
ul,ol{padding-left:22px}
.tag{display:inline-block;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;margin-right:6px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:10px 0 16px}
.summary-line{font-size:17px;line-height:1.7;padding:18px 22px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:18px;box-shadow:0 2px 12px rgba(0,0,0,.04);color:#334155}
.timeline{background:#fff;border-radius:16px;padding:22px;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#1e40af;margin-bottom:10px}
.timeline-item{display:flex;gap:12px;padding:7px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:13px;font-weight:700;color:#3b82f6;min-width:64px}
.timeline-text{font-size:14px;color:#475569}
.map{background:#fff;border-radius:18px;padding:28px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{margin-top:0;border:none;padding:0}
.diagram{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;align-items:center;padding:14px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:14px;padding:16px 20px;text-align:center;min-width:130px;font-weight:700;font-size:14px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:22px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:18px 22px;border-radius:12px;margin-bottom:18px}
.correction h3,.correction p{color:#92400e}
.sec-title{font-size:20px;font-weight:700;color:#1e40af;margin:8px 0 12px;padding-left:12px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:14px;padding:22px;margin-bottom:12px;box-shadow:0 4px 20px rgba(0,0,0,.05);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:17px;color:#1e40af;margin-bottom:8px}
.card .quote{background:#f8fafc;padding:10px 12px;border-radius:8px;margin:8px 0;font-size:13px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:8px 12px;border-radius:8px;font-size:13px;color:#166534}
.card .pitfall{background:#fef2f2;padding:10px 12px;border-radius:8px;margin:8px 0;font-size:13px;color:#991b1b;border-left:4px solid #ef4444}
table{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0}
th{background:#f1f5f9;padding:10px;text-align:left;color:#1e40af}
td{padding:10px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:18px;padding:28px;margin-top:22px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}
.conclusion h3{color:rgba(255,255,255,.9);margin:12px 0 6px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9)}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:22px 0 8px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;display:inline-block;margin-bottom:14px}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;
const esc = (s) => String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');

const d = {
  title: '哈苏 X2D：5万多贵在哪、坑在哪',
  duration: '12分20秒',
  url: 'https://b23.tv/FQUJVwg',
  tags: ['哈苏', 'X2D', '中画幅', '动态范围', '色彩'],
  perspective: '理性分析 · 器材选购',
  summary: '核心判断：X2D 用动态范围、色彩纯度、像素灵活性与拍照仪式感证明高价；用 AF/连拍/视频短板划清边界——多数人该买过剩全画幅，极少数静物画质党才「懂贵」。',
  timeline: [
    ['00:40', '动态范围第一惊艳'],
    ['02:00', '16bit 与欠曝肤色'],
    ['03:40', '自然色彩少后期'],
    ['05:30', '1亿像素裁切/防抖'],
    ['07:00', '影棚细节'],
    ['08:40', '屏幕菜单1TB软件'],
    ['09:10', 'AF/连拍/无视频'],
    ['11:20', '多数人不值/画质党可值'],
  ],
  map: [
    ['问题', '值不值5万+'],
    ['证据', '画质体验 vs 动态短板'],
    ['判断', '纯度机非全能机'],
    ['行动', '按场景否决'],
  ],
  corrections: [
    '误解：贵=全面更强。纠偏：体育/视频场景明确不值。',
    '误解：中画幅对焦越贵越好。纠偏：够用婚礼人像，不及同价顶级全画幅速度。',
    'ASR：风光/欠曝/佳能/XPan 等已按语境校正。',
  ],
  cards: [
    { title: '在讲什么：定价拆成两笔账', body: '一笔买宽容度+色彩+像素余量+触感软件；一笔「故意不买」视频与极速 AF。', quote: '哈苏明显把所有精力都放在了拍照体验上', relation: '先确认你是否需要那笔「不买」。', tone: 'card-purple' },
    { title: '值：文件与色彩', body: 'RAW 容错、自然色、后期减负、裁切自由、影棚微观质感。', quote: '这可能是我用过的最贴近人眼真实所见的相机了', relation: '对色彩挑剔者，单点即可支撑溢价叙事。', tone: 'card-blue' },
    { title: '不值：动态与视频', body: '3fps、无强 AI 追焦、连机关连续 AF、视频几乎不可用。', quote: '对大部分人来说，可能真的不值', relation: '否决清单比参数表更重要。', tone: 'card-orange' },
    { title: '怎么选', body: '人像/风光/影棚静物且不拍视频→可进入候选；体育/旅拍视频→直接排除，用 R5 级全画幅。', quote: '选相机适合自己的需求才是最划算的', relation: '用自己主力机对比片中样片再决定价差。', tone: 'card-green' },
  ],
  table: {
    title: '配得上 vs 配不上高价',
    head: ['维度', '配得上', '配不上'],
    rows: [
      ['画质', 'DR/16bit/色彩/1亿像素', '—'],
      ['体验', '握持 OLED 菜单 1TB 软件', '连机拍摄关连续 AF'],
      ['动态', '人像婚礼够用', '体育/高速/40fps 级'],
      ['视频', '专注拍照的取舍', '几乎无可用视频'],
    ],
  },
  boundary: ['个人俩月体验+样片对比，非实验室评测。', '镜头 35-100 贡献需计入系统价。'],
  pitfalls: ['为品牌仪式感忽略视频刚需。', '用体育场景标准否定其人像定位。', '不看原图只看片中压缩样张就下单。'],
  conclusion: {
    key: ['高价买的是拍照纯度。', '多数人全画幅已过剩。', '场景否决优先于参数崇拜。'],
    actions: ['列出自己是否拍视频/体育。', '用现有机拍同场景对比宽容度。', '试机重点：菜单、回放屏、连机 AF。'],
    shift: '从「值不值这个价」转向「我是否需要它故意不做的那些事」。',
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
fs.writeFileSync(path.join(DIR,'..','_work/b61/hasselblad-height.txt'), String(height));
