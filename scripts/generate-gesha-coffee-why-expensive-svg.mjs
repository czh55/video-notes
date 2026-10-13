#!/usr/bin/env node
/**
 * b62i：生成 gesha-coffee-why-expensive 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'gesha-coffee-why-expensive-理性分析.svg');

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
  title: '瑰夏咖啡，为什么能卖这么贵？',
  duration: '3分17秒',
  url: 'https://xhslink.cn/o/3KvyJWICIkc',
  tags: ['瑰夏', 'Gesha', '微批次', '拍卖', '选豆'],
  perspective: '理性分析 · 咖啡手作 · 价格与批次',
  summary:
    '核心命题：同名「瑰夏」为什么价格可以差一个数量级？作者判断——品种潜力只是入场门票；真正拉开差距的是地块/处理/微批次筛选带来的稀缺，以及拍卖竞价形成的极端成交价。拍卖价是市场结果，不能倒推普通生产成本；买豆应问清批次信息，并先匹配口味。',
  timeline: [
    ['00:00', '提问：瑰夏为什么这么贵？抛出冠军批次拍卖锚点'],
    ['00:15', '普通批次 vs 冠军小批次；产量低只说对一部分'],
    ['00:25', '三层：品种潜力 / 具体批次 / 市场竞价'],
    ['00:30', 'WCR：高海拔品质潜力极高、产量潜力低'],
    ['00:54', '同名不一定同源；T2722 也需条件'],
    ['01:17', '2004 翡翠庄园分区独立批次；杯测与纪录叙事'],
    ['01:40', '筛选越细量越少；售价≠成本；拍卖价不能倒推成本'],
    ['02:30', '别贴智商税标签；问清批次；口味先于品种名'],
  ],
  map: [
    ['问题', '为何同名不同价'],
    ['门票', '品种潜力'],
    ['筛选', '微批次稀缺'],
    ['市场', '拍卖竞价'],
    ['边界', '价≠普通成本'],
    ['行动', '问批次+口味'],
  ],
  corrections: [
    '误解：瑰夏贵=树难种、产量低。纠偏：这只说对一部分；还要看具体批次信息与市场竞价。',
    '误解：看见「瑰夏」就等于顶级。纠偏：多个遗传背景曾共用此名；名字本身不等于顶级。',
    '误解：随便种瑰夏都能卖高价。纠偏：海拔、成熟采摘、管理与地块/处理批次都会改变结果。',
    '误解：极端拍卖价≈普通生产成本。纠偏：拍卖价是成交结果，不能倒推普通成本；售价高也不等于成本就这么高。',
    '误解：贵=智商税 / 便宜=不值。纠偏：先问批次是否清楚、风味是否匹配自己，再谈值不值。',
    '立场分层：拍卖数字、20kg/总成交等为视频画面信息（未独立核验）；三层价格结构与买豆清单为作者观点；「同名不同源」引用 WCR 提醒属作者转述。',
  ],
  cards: [
    {
      title: '在讲什么：价格是三层叠加，不是一个品种标签',
      body: '关键理解：品种潜力、微批次稀缺、拍卖竞价分别回答「能不能进入高端」「为什么量少」「谁在抬价」。用法：看到天价时先拆层，不要用「瑰夏」一词解释全部溢价。',
      quote: '品种潜力、具体批次，还有市场竞价',
      relation: '潜力给门票 → 筛选压数量 → 竞价推高顶尖一小部分。',
      tone: 'card',
    },
    {
      title: '在讲什么：同名不一定同源',
      body: '关键理解：Geisha/Gesha 曾被用于多个遗传背景；巴拿马出名的 T2722 后代仍需合适条件。用法：把「品种名」降级为线索，把地块、处理、批次升为主信息。',
      quote: '瑰夏这个名字本身不等于顶级瑰夏',
      relation: '名字 ≠ 遗传背景 ≠ 杯中表现；同庄园不同批次也可完全不同。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：拍卖价是结果，不是成本说明书',
      body: '关键理解：极端成交价发生在极少量冠军批次与全球买家争夺的场景，不是普通批发市场。用法：不要用拍卖纪录去衡量咖啡馆一杯「瑰夏」的合理进货成本。',
      quote: '拍卖价是成交结果，不能倒推普通成本',
      relation: '售价高 ≠ 生产成本同等高；稀缺与竞价解释溢价尖端。',
      tone: 'card-orange',
    },
    {
      title: '在讲什么：值不值先看批次与口味',
      body: '关键理解：决策问题从「它贵不贵」换成「这是哪一批、合不合我口」。用法：问清国家/庄园/地块/处理/批次；深烘坚果巧克力偏好者未必适合花香茶感浅烘。',
      quote: '真正贵的不是瑰夏这两个字，而是……具体批次',
      relation: '信息清楚 + 数量很少 + 潜力被做出来 → 才谈得上「这杯为什么贵」。',
      tone: 'card-green',
    },
  ],
  table: [
    ['层级', '大致含义', '价格含义（作者视角）'],
    ['普通商用批次', '同名品种、规模化供应', '可贵，但通常不是拍卖尖端'],
    ['高海拔微批次', '地块/处理更细，数量更少', '溢价常来自筛选与信息密度'],
    ['获奖 / 年度冠军', '竞赛与杯测背书的极小量', '可能进入竞价与纪录叙事'],
    ['拍卖成交价', '全球买家争夺的市场结果', '不能倒推普通生产成本'],
  ],
  actions: [
    '看到「瑰夏」先问：国家、庄园、地块、处理法、批次号/名称是否清楚。',
    '把极端拍卖新闻当市场故事，不当日常进货成本参照。',
    '对照口味：花香茶感浅烘 vs 坚果巧克力厚重深烘，先选风格再选品种名。',
    '比较两杯「瑰夏」时，优先比批次信息与烘焙表达，而不是比标签字数。',
    '同样预算做选择题：为辨识度花香买单，还是为稳定厚重与性价比买单。',
  ],
  pitfalls: [
    '只凭品种名下单，把「瑰夏」当成品质保证书。',
    '用冠军拍卖价论证咖啡馆一杯必定值或不值。',
    '把产量低当成唯一解释，忽略批次筛选与竞价。',
    '口味不匹配仍硬喝「名品种」，再反向骂智商税。',
    '把未核验的画面数字当权威行情长期引用而不标注来源。',
  ],
  shifts: [
    ['以前：瑰夏=贵=好', '现在：瑰夏=线索，批次与口味=决策'],
    ['以前：贵因产量低', '现在：潜力+筛选稀缺+竞价三层'],
    ['以前：拍卖价≈成本', '现在：拍卖价是成交结果，不能倒推'],
  ],
};

const body = `
<div class="container">
  <h1>${esc(d.title)}</h1>
  <div class="meta">
    ${d.tags.map((t) => `<span class="tag tag-blue">${esc(t)}</span>`).join('')}
    <span class="tag tag-gray">${esc(d.duration)}</span>
    <span class="tag tag-purple">${esc(d.perspective)}</span>
  </div>
  <a class="source-link" href="${esc(d.url)}" target="_blank" rel="noopener">原视频（小红书短链）</a>
  <div class="summary-line">${esc(d.summary)}</div>

  <div class="timeline">
    <h3>关键证据时间轴</h3>
    ${d.timeline.map(([t, text]) => `
      <div class="timeline-item">
        <div class="timeline-time">${esc(t)}</div>
        <div class="timeline-text">${esc(text)}</div>
      </div>`).join('')}
  </div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">
      ${d.map.map((n, i) => `
        <div class="node ${i === d.map.length - 1 ? 'node-green' : i === 3 ? 'node-orange' : i === 4 ? 'node-purple' : ''}">
          <div style="font-size:12px;opacity:.75;margin-bottom:4px">${esc(n[0])}</div>
          ${esc(n[1])}
        </div>
        ${i < d.map.length - 1 ? '<div class="arrow">→</div>' : ''}
      `).join('')}
    </div>
  </div>

  <div class="correction">
    <h3>常见误解与认知纠偏</h3>
    ${d.corrections.map((c) => `<p>${esc(c)}</p>`).join('')}
  </div>

  <h2 class="sec-title">观点卡片</h2>
  ${d.cards.map((c) => `
    <div class="card ${c.tone}">
      <h3>${esc(c.title)}</h3>
      <p>${esc(c.body)}</p>
      <div class="quote">「${esc(c.quote)}」</div>
      <div class="relation">${esc(c.relation)}</div>
    </div>
  `).join('')}

  <div class="card">
    <h3>横向对照：批次层级与价格含义</h3>
    <table>
      <thead><tr>${d.table[0].map((h) => `<th>${esc(h)}</th>`).join('')}</tr></thead>
      <tbody>
        ${d.table.slice(1).map((row) => `<tr>${row.map((cell) => `<td>${esc(cell)}</td>`).join('')}</tr>`).join('')}
      </tbody>
    </table>
  </div>

  <div class="card card-orange">
    <h3>避坑总结</h3>
    <ul>${d.pitfalls.map((p) => `<li>${esc(p)}</li>`).join('')}</ul>
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <p>同名瑰夏可以完全不是一个价格带。品种潜力只负责开门；微批次筛选制造稀缺；拍卖竞价制造尖端成交。真正要买的是信息清楚的具体批次，以及适合自己的风味，而不是两个汉字。</p>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>

  <div class="footer">双轨产物 · 理性分析 SVG · 与图文实录共享同一转录与画面证据 · 画面拍卖数字未独立核验</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'b62i-svg-height.txt'),
  String(height),
  'utf8',
);
