#!/usr/bin/env node
/**
 * b62m：生成 espresso-machine-dial-in-beginner 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'espresso-machine-dial-in-beginner-理性分析.svg');

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
  title: '咖啡机调试教程｜新手必看',
  duration: '4分39秒',
  url: 'https://xhslink.cn/o/8oHA2m5BWWP',
  tags: ['意式调试', '研磨粗细', '磨豆时间', '自动定量', '新手起点'],
  perspective: '理性分析 · 咖啡手作 · 设备调参顺序',
  summary:
    '核心命题：新买咖啡机与磨豆机，第一次调参应先动哪一台？作者给出可复用顺序——先用流速定研磨粗细，再固定研磨用磨时定粉量，最后才设咖啡机自动定量。18–19克粉 / 36克液 / 25–30秒是稳定起点，不是所有豆的死答案；参数只是起点，好喝才是结果。',
  timeline: [
    ['00:00', '三问：先动哪台 / 外冲怪谁 / 时间怎么算'],
    ['00:13', '总顺序：粗细 → 磨时 → 自动定量'],
    ['00:18', '预热与纪律：91–93℃，暂不改压力预浸'],
    ['00:58', '按键计时，到36克停；不到25秒调细，超过30秒调粗'],
    ['01:28', '认标识；调完排约10克残粉'],
    ['02:09', '固定研磨，用磨豆时间锁18–19克'],
    ['02:45', '计时定量 vs 流量计定量，设完秤复测'],
    ['03:55', '三步复盘：先流速、再粉量、后自动化'],
    ['04:08', '边界：数字是起点，先稳机再品鉴'],
  ],
  map: [
    ['问题', '先动哪台？'],
    ['步骤1', '流速定研磨'],
    ['步骤2', '磨时定粉量'],
    ['步骤3', '自动定量'],
    ['边界', '数字=起点'],
  ],
  corrections: [
    '误解：一上来就设咖啡机自动定量。纠偏：作者顺序是研磨粗细 → 磨豆时间 → 最后自动定量。',
    '误解：时间从第一滴咖啡出来才开始算。纠偏：口播明确「不是等咖啡流出来再算」，按键同时计时。',
    '误解：粉看起来像细盐就说明研磨合适。纠偏：细盐只作起点，最终看液重和时间。',
    '误解：调完研磨立刻下一杯测试。纠偏：先排约10克残粉，避免混档。',
    '误解：把18–19克/36克/25–30秒当所有豆的标准答案。纠偏：作者称其为新手稳定起点，进阶靠味道。',
    '立场分层：三步顺序与计时规则属作者教学观点；91–93℃、粉液时间区间为作者建议起点，视频未提供独立实验数据；「以说明书为准」标明机型差异边界。',
  ],
  cards: [
    {
      title: '在讲什么：调参顺序比「数字几」更重要',
      body: '关键理解：新设备真正要记住的是流程——先调流速、再定粉量、最后做自动化；不是背某台磨豆机刻度。用法：任何机型先问「现在改的是哪一步」，避免同时拧多旋钮。',
      quote: '不是某一台磨豆机到底调到数字几，而是三个步骤',
      relation: '顺序约束 ← 单变量调试；同时改粉量/研磨/自动量会让结果不可解释。',
      tone: 'card',
    },
    {
      title: '在讲什么：用液重+时间反推研磨',
      body: '关键理解：固定18–19克粉，目标36克液；不到25秒到36克→调细，超过30秒→调粗，落在25–30秒即进入起始范围。用法：疯狂外冲且粉量未变时，先查研磨是否太粗。',
      quote: '不到25秒已经到36克，流速太快，研磨调细',
      relation: '流速信号 → 研磨方向；粉量与操作保持不变是前提。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：磨时定量与复称触发条件',
      body: '关键理解：定量磨豆机常用秒数控制出粉；锁研磨后调磨时到18–19克，三次稳定可保存。用法：日常可免每杯称粉，但开机第一杯、换豆、调过研磨或流速明显变化时必须复称。',
      quote: '三次都比较稳定，就可以保存这个磨豆时间',
      relation: '磨时 ← 粉量稳定；研磨变更会使旧磨时失效。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：两种自动定量与验收标准',
      body: '关键理解：计时定量记秒数不知杯中克数；流量计按水量控制通常更稳。用法：按稳定萃到36克的秒数/长按记忆设置，再用秤复测；连续2–3杯接近36克才算调好。不同机型操作以说明书为准。',
      quote: '这个自动萃取键才算真正调好',
      relation: '设置完成 ≠ 验收完成；复测杯数是硬门槛。',
      tone: 'card-orange',
    },
  ],
  table: [
    ['环节', '主要动作', '验收信号', '常见误操作'],
    ['研磨粗细', '只改研磨；按键计时到36克', '25–30秒较稳定', '同时改粉量或自动定量'],
    ['磨豆时间', '研磨固定后调磨时', '出粉连续三次18–19克', '未排残粉就测'],
    ['计时定量', '按稳定秒数设自动时长', '秤复测液重≈36克', '只设秒数不复测'],
    ['流量计定量', '长按记忆到36克松开', '连续2–3杯接近36克', '忽略机型保存步骤'],
    ['进阶', '机器稳定后品鉴调味', '酸甜苦涩/浓度/风味', '把起点数字死守不换豆'],
  ],
  actions: [
    '预热充分；温度先放作者建议的91–93℃区间，压力/预浸/自动量先别动。',
    '每杯称18–19克粉，按键同时计时，到36克停并记秒数；按不到25秒调细、超过30秒调粗规则只改研磨。',
    '每次调研磨后排约10克残粉再测；大幅调细分段进行。',
    '研磨稳定后调磨豆时间锁18–19克，三次稳定再保存；换豆或调磨后复称。',
    '最后设自动定量并用秤复测2–3杯；通过后再用味道做进阶微调。',
  ],
  pitfalls: [
    '一上来就拧自动定量或同时改多个参数。',
    '等第一滴出来才开始计时。',
    '用眼睛「像细盐」判定研磨完成。',
    '调完研磨不排残粉，导致混档测不准。',
    '把18–19/36/25–30当成所有豆的永久标准答案。',
  ],
  shifts: [
    ['以前：先找「正确数字几」', '现在：先走三步顺序'],
    ['以前：靠粉外观判断研磨', '现在：用液重+时间反推'],
    ['以前：设完自动键就结束', '现在：连续复测2–3杯才验收'],
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
        <div class="node ${i === d.map.length - 1 ? 'node-green' : i === 1 ? 'node-orange' : i === 3 ? 'node-purple' : ''}">
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
    <h3>横向对照：三步与两种自动定量</h3>
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
    <p>新手调设备先走顺序：流速定研磨 → 磨时定粉量 → 自动定量验收。配方数字是稳定起点，不是风味终点。</p>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>

  <div class="footer">双轨产物 · 理性分析 SVG · 与图文实录共享同一转录证据 · 独立于 espresso-grinder-dial-in-guide（另一短链）</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'b62m-svg-height.txt'),
  String(height),
  'utf8',
);
