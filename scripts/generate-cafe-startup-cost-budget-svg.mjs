#!/usr/bin/env node
/**
 * b62g：生成 cafe-startup-cost-budget 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'cafe-startup-cost-budget-理性分析.svg');

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
.node-red{background:linear-gradient(135deg,#fef2f2,#fee2e2);border-color:#fca5a5;color:#991b1b}
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
  title: '开一家咖啡店，到底要准备多少钱？',
  duration: '4分07秒',
  url: 'https://xhslink.cn/o/3sv78FfB0sR',
  tags: ['咖啡店', '开店预算', '现金流', '养店钱', '创业准备'],
  perspective: '理性分析 · 咖啡经营 · 启动资金',
  summary:
    '核心命题：开一家小咖啡店到底要准备多少钱？作者结论是「五万先别开、保底十万再启动」——预算必须同时准备开门钱与养店钱；小店模型示意开业前六到七万、缓冲三到四万。真正要防的不是开不了门，而是开门后没有现金撑过销量爬坡，被迫全面降标准进入恶性循环。文中金额为作者建议与示意，非某城报价。',
  timeline: [
    ['00:00', '提问：到底要准备多少钱'],
    ['00:05', '五万不是启动线：先不要开'],
    ['00:20', '开门 ≠ 具备经营条件（缺养店钱）'],
    ['00:24', '建议：保底十万元再启动'],
    ['00:40', '只算开业第一天的投入清单'],
    ['01:00', '开业是持续花钱的开始'],
    ['01:30', '五万硬伤：爬坡期没钱→降标准'],
    ['01:55', '一次预算不足→经营恶性循环'],
    ['02:05', '两个账户：开门钱 + 养店钱'],
    ['02:12', '小店示意：6–7万 / 3–4万'],
    ['02:35', '用现金覆盖月数定义调整时间'],
    ['02:50', '有钱也不全花开业前；有效投入条件'],
    ['03:00', '8万店 vs 30万店：同赚1万回收难度不同'],
    ['03:10', '四件事：店型/一次性/月净流出/调整时间'],
    ['03:20', '开店前三张表'],
    ['03:40', '收束：保底十万再启动'],
    ['03:50', '互动与下期：保本杯量（本期未给数字）'],
  ],
  map: [
    ['问题', '准备多少钱'],
    ['否决', '五万不够'],
    ['结构', '开门+养店'],
    ['校验', '覆盖月数'],
    ['行动', '三张表'],
  ],
  corrections: [
    '误解：预算=把店开起来的一次性总价。纠偏：还要准备把店养下去的经营缓冲。',
    '误解：五万是值得尝试的低成本方案。纠偏：作者认为连开门都勉强，开业后更难维持。',
    '误解：有十万就可以全花在装修和设备上。纠偏：开业当天账户里还要留缓冲；有二十/三十万也不必盲目做大买贵。',
    '误解：贵设备/复杂装修天然更专业。纠偏：只有确实提高出杯效率、营业额、复购或降低停机风险，才可能是有效投入。',
    '误解：总预算一个数字就算完。纠偏：要算店型、一次性投入、保守销量下月净流出、剩余现金能留多少调整时间。',
    '立场分层：五万/十万阈值与 6–7万/3–4万拆分为作者经营建议与小店示意；非行业强制标准或某城市实测报价。本期未给出保本杯量。',
  ],
  cards: [
    {
      title: '在讲什么：把「总预算」改写成「还能经营多久」',
      body: '关键理解：决策变量不是开门那天花了多少，而是开门后账户还能不能撑过销量尚未稳定的阶段。用法：任何启动金额都拆成开门钱与养店钱两本账。',
      quote: '不是能不能开门，而是开门以后还能不能继续经营',
      relation: '只算开业第一天 → 开门后持续支出无着落 → 被迫降标准。',
      tone: 'card',
    },
    {
      title: '在讲什么：五万为什么被否决',
      body: '关键理解：在房租极低、无高转让费、装修设备压到极限且老板守店时，五万最多勉强开十平内小店，却很难留下爬坡现金。用法：别把「能开门」当成「能经营」。',
      quote: '五万元不是值得尝试的低成本方案',
      relation: '现金紧 → 机器/水电/原料全面压价 → 出品与体验变差 → 复购更难 → 更紧。',
      tone: 'card-red',
    },
    {
      title: '在讲什么：十万如何拆成两个账户',
      body: '关键理解：小店模型示意开业前六到七万、缓冲三到四万，合起来对应保底十万。用法：先固定缓冲，再倒逼开业清单砍到「必须现在买」；用保守销量下的月净流出估算现金覆盖月数=调整时间。',
      quote: '这三到四万元能撑多久，不能靠感觉',
      relation: '缓冲不是闲钱装饰，是收入未稳阶段的生存时间。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：有效投入 vs 把回本做难',
      body: '关键理解：同样月赚一万，前期投入八万与三十万的回收难度完全不同。用法：贵设备/复杂装修要能证明效率、营业额、复购或停机风险改善；否则只是抬高以后要收回的金额。',
      quote: '否则只是把以后需要收回的钱变多',
      relation: '资本开支上涨 → 保本压力上升；与「看起来更高级」不是同一回事。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：开店前三张表 + 四件事',
      body: '关键理解：一次性投入表、每月固定与变动支出表、保守销量现金余额表；并把现在必须买与以后再加分开。用法：先定店型（外卖档口/社区店等），再填四件事，而不是先拍一个总金额。',
      quote: '真正该计算的不是一个孤立的总预算而是四件事',
      relation: '表做完才知道缓冲够不够；不够就不要用五万硬开。',
      tone: 'card-orange',
    },
  ],
  table: [
    ['对照项', '画面/口播示意', '不能单独推出'],
    ['五万元', '作者建议先别开；不是启动线', '任何城市都绝对开不了任何档口'],
    ['十万元', '作者建议的保底启动资金', '全国统一开工标准或必然盈利'],
    ['6–7万 / 3–4万', '小店模型下开门钱/养店钱拆分示意', '你的城市房租与设备价也刚好落在此区间'],
    ['8万店 vs 30万店', '同月赚1万时回收难度不同', '低投入一定更好或高投入一定更差'],
    ['三张表', '开业前必须做的现金规划动作', '做完表就等于已验证市场'],
  ],
  actions: [
    '列出开业前一次性投入，并标注「现在必须买」与「以后再加」。',
    '另列每月固定与变动支出（房租、人工、水电、平台、原料等）。',
    '用保守销量测算开业后月净流出与现金覆盖月数（调整时间）。',
    '把总现金拆成开门钱与养店钱两本账；开业当天保留缓冲。',
    '评估贵设备/复杂装修是否提升效率、营业额、复购或降低停机风险。',
  ],
  pitfalls: [
    '只算开门清单，不算开业后持续支出与爬坡期现金。',
    '把五万当成「低成本试错」而忽略恶性循环风险。',
    '有十万就全砸装修设备，开业当天账户见底。',
    '因有二十/三十万就盲目做大、买贵机。',
    '靠感觉估计缓冲能撑多久，不做保守销量测算。',
    '把本期未给出的保本杯量自行脑补成具体数字。',
  ],
  shifts: [
    ['以前：关心「总共要花多少」', '现在：同时准备开门钱与养店钱'],
    ['以前：能开门就算成功启动', '现在：用现金覆盖月数定义调整时间'],
    ['以前：有钱就升级设备装修', '现在：先问是不是有效投入、会不会抬高回本'],
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
        <div class="node ${i === d.map.length - 1 ? 'node-green' : i === 1 ? 'node-red' : i === 2 ? 'node-orange' : i === 3 ? 'node-purple' : ''}">
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
    <h3>横向对照：数字能推出什么</h3>
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
    <p>开店预算的关键不是拍一个总价，而是同时准备开门钱与养店钱，并用保守销量下的现金覆盖月数衡量调整时间。作者建议：五万先别开，保底十万再启动；有钱也不要全砸开业前，贵投入必须能证明是有效投入。</p>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>

  <div class="footer">双轨产物 · 理性分析 SVG · 与图文实录共享同一转录与画面证据 · b62g</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'b62g-svg-height.txt'),
  String(height),
  'utf8',
);
