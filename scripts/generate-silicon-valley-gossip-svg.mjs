#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'silicon-valley-gossip-理性分析.svg');
const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:28px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:22px;font-weight:700;color:#1e40af;margin:22px 0 12px;padding-bottom:6px;border-bottom:2px solid #e2e8f0}
h3{font-size:16px;font-weight:700;color:#334155;margin-bottom:8px}
p,li{font-size:14px;line-height:1.7;color:#475569;margin-bottom:5px}
ul,ol{padding-left:20px}
.tag{display:inline-block;padding:3px 10px;border-radius:16px;font-size:12px;font-weight:600;margin-right:6px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:8px 0 12px}
.summary-line{font-size:16px;line-height:1.65;padding:16px 18px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:14px;color:#334155;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:14px;padding:16px;margin-bottom:14px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline-item{display:flex;gap:10px;padding:5px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:12px;font-weight:700;color:#3b82f6;min-width:58px}
.timeline-text{font-size:13px;color:#475569}
.map{background:#fff;border-radius:16px;padding:22px;margin-bottom:14px;box-shadow:0 4px 20px rgba(0,0,0,.05)}
.map h2{margin:0;border:none;padding:0}
.diagram{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;padding:12px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:12px;padding:12px 16px;text-align:center;min-width:118px;font-weight:700;font-size:13px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:20px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:14px 16px;border-radius:10px;margin-bottom:12px}
.correction h3,.correction p{color:#92400e}
.sec-title{font-size:18px;font-weight:700;color:#1e40af;margin:6px 0 10px;padding-left:10px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:12px;padding:16px;margin-bottom:10px;border-left:5px solid #3b82f6;box-shadow:0 3px 16px rgba(0,0,0,.04)}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:15px;color:#1e40af}
.card .quote{background:#f8fafc;padding:8px 10px;border-radius:8px;margin:6px 0;font-size:12px;color:#64748b;border-left:3px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:8px 10px;border-radius:8px;font-size:12px;color:#166534}
.card .pitfall{background:#fef2f2;padding:8px 10px;border-radius:8px;margin:6px 0;font-size:12px;color:#991b1b;border-left:3px solid #ef4444}
table{width:100%;border-collapse:collapse;font-size:12px}
th{background:#f1f5f9;padding:8px;text-align:left;color:#1e40af}
td{padding:8px;border-bottom:1px solid #e2e8f0;vertical-align:top;color:#475569}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:16px;padding:22px;margin-top:16px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}
.conclusion h3{color:rgba(255,255,255,.9);margin:10px 0 6px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9)}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:16px 0}
.source-link{color:#3b82f6;font-size:13px;text-decoration:none;display:inline-block;margin-bottom:10px}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

const esc = (s) => String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');

const d = {
  title: '硅谷八卦｜地标、热潮与技术理想主义',
  duration: '16分30秒',
  url: 'https://b23.tv/b7mTZUi',
  tags: ['硅谷', 'AI', "Buck's", 'AGI', '风投'],
  perspective: '理性分析 · 产业现场',
  summary: '核心判断：片子用早餐桌与办公室地标重建「叙事可信度」，再用投资人框架解释本轮 AI——更快（Utility 扩散）、更通用（蒸汽机/电力级）、仍夹杂 2000 式估值狂欢；真正可带走的是「为什么不是我」的工程师理想主义土壤。',
  timeline: [
    ['02:30', "Buck's 创业桌"],
    ['03:20', '培根开场提问'],
    ['05:00', 'Apple I 文物'],
    ['07:10', 'FB 第一办公室'],
    ['07:50', 'PayPal 幸运办公室'],
    ['08:50', '斯坦福果园史'],
    ['10:50', 'AI 更快因 Utility'],
    ['12:40', 'AGI≈蒸汽/电力'],
    ['14:40', '图片搜索故事'],
    ['15:50', 'AGA House'],
  ],
  map: [
    ['问题', '矽谷 AI 到底怎样'],
    ['证据', '地标+口述+访谈'],
    ['判断', 'Utility 热潮更快'],
    ['行动', '看通用生产力扩散'],
  ],
  corrections: [
    '误解：标题八卦=小道消息拼盘。纠偏：主体是探访纪录片+一档对照访谈。',
    '误解：AI=又一次互联网。纠偏：口播强调类比缩小了议题，更接近通用生产力。',
    '误解：元数据时长约 2 小时。纠偏：可下载成片约 16 分 30 秒（B 站时长字段异常）。',
  ],
  cards: [
    { title: '地标叙事：桌子证明神话', body: "Buck's、FB/PayPal 办公室把抽象创业史钉在可走访坐标上；天价租金是筛选信号。", quote: '最幸运的办公室', relation: '现场感降低「听说」成本。', tone: 'card-purple' },
    { title: '扩散机制：网络效应 vs Utility', body: '移动互联网要凑齐好友才粘；AI 自己用上就能受益，故速度更快。', quote: '它是一个基础设施叫 Utility', relation: '解释估值与采用曲线为何更陡。', tone: 'card-blue' },
    { title: '历史定位：通用生产力', body: 'AGI 的 G=General；专用模型像单菜系厨师，大模型像开天眼的总厨带来涌现。', quote: '类似于蒸汽机、类似于电力', relation: '判断层从「App 浪潮」升到「能源级基础设施」。', tone: 'card-green' },
    { title: '文化燃料：为什么不是我', body: '图片搜索周末项目被谷歌看中上线；周围成功样本激励下一次尝试。', quote: '哎 为什么不是我', relation: '理想主义与资本狂欢并存是矽谷常态。', tone: 'card-orange' },
  ],
  table: {
    title: '本集信息层',
    head: ['层', '内容', '用途'],
    rows: [
      ['场景', "Buck's / 办公室 / AGA House", '建立现场可信度'],
      ['史纲', '果园→军工半导体→VC→互联网', '解释土壤'],
      ['框架', 'Utility 速度 + AGI 通用', '对照移动互联网'],
      ['文化', '工程师改命运故事', '理解动机结构'],
    ],
  },
  boundary: ['探访口播含传说成分（创业桌版本因人口述而异）。', '开场英文电视 ASR 不可作论据。', '邀请制活动仅下午片段，非完整议程。'],
  pitfalls: ['把餐厅传说当公司史一手档案。', '只用「又是泡沫」概括而忽略 Utility 扩散差异。', '忽略理想主义样本在人才吸引中的作用。'],
  conclusion: {
    key: ['地标让叙事可走访。', '本轮更快因 Utility。', '通用生产力叙事>App 浪潮叙事。'],
    actions: ['用 Utility vs 网络效应检查下一个 AI 产品是否需要冷启动。', '把 AGI 讨论从「会不会取代搜索」升到「像电一样渗透哪些流程」。', '留意邀请制社交如何再生产行业共识。'],
    shift: '从「矽谷又在炒什么」转向「扩散机制与文化燃料如何叠加热潮」。',
  },
};

function body(data) {
  const tags = data.tags.map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`).join('');
  const timeline = data.timeline.map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`).join('');
  const map = data.map.map(([a, b], i) => {
    const cls = ['node', 'node-green', 'node-orange', 'node'][i % 4];
    const ar = i < data.map.length - 1 ? '<span class="arrow">→</span>' : '';
    return `<div class="${cls}">${esc(a)}<br/>${esc(b)}</div>${ar}`;
  }).join('');
  const corr = data.corrections.map((c) => `<p>${esc(c)}</p>`).join('');
  const cards = data.cards.map((c) => `<div class="card ${c.tone}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p><div class="quote">${esc(c.quote)}</div><div class="relation">${esc(c.relation)}</div></div>`).join('');
  const thead = `<tr>${data.table.head.map((h) => `<th>${esc(h)}</th>`).join('')}</tr>`;
  const tbody = data.table.rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
  const bound = data.boundary.map((b) => `<li>${esc(b)}</li>`).join('');
  const pits = data.pitfalls.map((p) => `<div class="pitfall">${esc(p)}</div>`).join('');
  const key = data.conclusion.key.map((k) => `<li>${esc(k)}</li>`).join('');
  const act = data.conclusion.actions.map((a) => `<li>${esc(a)}</li>`).join('');
  return `<div class="container root-wrap"><h1>${esc(data.title)}</h1><div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(data.duration)}</span><span class="tag tag-gray">${esc(data.perspective)}</span></div><a class="source-link" href="${esc(data.url)}">原视频</a><div class="summary-line">${esc(data.summary)}</div><div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div><div class="map"><h2>核心脉络</h2><div class="diagram">${map}</div></div><div class="correction"><h3>常见误解与认知纠偏</h3>${corr}</div><div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div><div class="section"><h2 class="sec-title">${esc(data.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div><div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${bound}</ul>${pits}</div></div><div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${key}</ul><h3>行动清单</h3><ol>${act}</ol><h3>关键认知转变</h3><p>${esc(data.conclusion.shift)}</p></div><div class="footer">双轨产物之二 · 理性分析 · ${esc(data.duration)}</div></div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: body(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated', OUT, height);
fs.mkdirSync(path.join(DIR, '..', '_work/b61'), { recursive: true });
fs.writeFileSync(path.join(DIR, '..', '_work/b61/gossip-height.txt'), String(height));
