#!/usr/bin/env node
/**
 * b62h：生成 cafe-price-war-follow-or-not 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'cafe-price-war-follow-or-not-理性分析.svg');

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
  title: '咖啡店价格战能不能跟？',
  duration: '3分25秒',
  url: 'https://xhslink.cn/o/Axsh7cqF0dz',
  tags: ['咖啡店', '价格战', '单杯贡献', '促销测试', '经营核算'],
  perspective: '理性分析 · 咖啡经营 · 定价决策',
  summary:
    '核心命题：隔壁美式降到 9.9，小店该不该跟？作者结论是「不是不能跟，而是不能只跟价格」——先算单杯贡献与实际结算，再确认高峰产能接得住，最后用有边界的小范围测试核对让利换回了什么。真正要防的是订单涨了、利润反而没了。文中 15/5/204 等数字为示意算例。',
  timeline: [
    ['00:00', '提问：9.9 跟不跟？改写为「得多卖多少杯」'],
    ['00:20', '定义「留下」= 单杯贡献，不是净利润'],
    ['00:38', '示意：15→9.9，持平约需 204 杯；到手≠标价'],
    ['00:58', '翻倍后人力/产能/差评损耗上移'],
    ['01:16', '三项自检：贡献、结算、高峰产能'],
    ['01:25', '可以跟：先问让利换守单/获客/填闲时'],
    ['01:54', '订单≠新客；勿照抄连锁背后能力'],
    ['02:29', '入口款+范围限定+停止条件'],
    ['03:10', '收束三问：留下多少→接不接得住→换回什么'],
  ],
  map: [
    ['问题', '9.9 跟不跟'],
    ['算账', '单杯贡献'],
    ['校验', '结算×产能'],
    ['目标', '让利换什么'],
    ['行动', '有边界测试'],
  ],
  corrections: [
    '误解：价格战成败看订单有没有涨。纠偏：更危险的是订单涨了、利润没了。',
    '误解：活动页 9.9 = 门店到手 9.9。纠偏：补贴、承担比例、每单费用要回后台结算核对。',
    '误解：多出来的活动单 = 新客。纠偏：其中可能大量是本会原价购买的顾客改买便宜款。',
    '误解：连锁能卖 9.9，小店也能照抄。纠偏：采购、流量、会员、排班与库存能力不同，他人承受力不能替你证明。',
    '误解：要么全跟要么全不跟。纠偏：可用入口款+新客/时段/数量/周期限定做测试，并写停止条件。',
    '立场分层：算术示意与三项自检属作者经营叙事；「能不能跟」结论与测试框架是作者观点，非行业强制法则。',
  ],
  cards: [
    {
      title: '在讲什么：把「跟价」改写成「持平销量」',
      body: '关键理解：决策变量不是对手标价，而是降价后要多卖多少杯才能留下原来一样的钱。用法：先算出降价前后单杯贡献差，再反推所需销量倍数。',
      quote: '真正要防的不是订单下降，而是订单涨了利润反而没了',
      relation: '标价竞争 → 贡献下降 → 持平销量门槛上升；忽略门槛会把忙碌当成胜利。',
      tone: 'card',
    },
    {
      title: '在讲什么：单杯贡献 ≠ 净利润',
      body: '关键理解：「留下」= 售价 − 原料/包装/随单变动成本。用法：先用贡献算促销底线，再另算房租人工等固定成本，不要混成一笔「赚了」。',
      quote: '这里说的留下，不是门店最后的净利润',
      relation: '示意 15−5=10；9.9−5=4.9 → 1000 元贡献约需 204 杯（纸面）。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：三项自检决定能不能接单',
      body: '关键理解：单杯贡献、实际结算、高峰产能任一扛不住，订单越多可能越亏。用法：跟价前同时核对后台到手价与出杯/排班上限。',
      quote: '先看自己的单杯贡献、实际结算和高峰产能',
      relation: '销量翻倍会牵动兼职、制冰、机产能与退款差评——变动成本也会动。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：让利必须绑定可验证目标',
      body: '关键理解：同质商圈完全不回应可能丢单，但跟价不是为了「面子跟 9.9」。用法：先写清目标是守单、获新客还是填闲时，再选产品/时间/范围。',
      quote: '已经不是 9 块 9 值不值得跟，而是这次让掉利润准备换回什么',
      relation: '目标不同 → 入口款与活动边界不同；无目标跟价等于无控制让利。',
      tone: 'card',
    },
    {
      title: '在讲什么：有边界测试 + 停止条件',
      body: '关键理解：小店更稳妥的是入口款测试，而不是全店齐降。用法：限定新客/时段/数量/周期；主力利润款不一起拖；写停止条件（贡献破线、出杯变慢、差评升、无新客连带复购）。',
      quote: '你不是不能跟，而是不能只跟价格',
      relation: '促销价/原价/试用条件写清楚；禁止虚构原价制造便宜感。',
      tone: 'card-orange',
    },
  ],
  table: [
    ['决策信号', '可能意味着', '不能单独推出'],
    ['对手标 9.9', '同圈价格压力上升', '你也必须全店跟到 9.9'],
    ['活动订单涨', '销量/曝光可能上升', '一定赚到更多贡献或新客'],
    ['标价 9.9', '前台展示价', '门店实际到手就是 9.9'],
    ['连锁能扛', '其成本与流量结构不同', '小店同样可持续'],
    ['完全不跟', '可能丢部分价格敏感单', '长期一定更赚（忽略目标与产能）'],
  ],
  actions: [
    '算出降价前后单杯贡献，反推「留下原来一样的钱」需要的销量。',
    '回后台核对到手价：补贴、门店承担、每单费用。',
    '评估高峰产能：人力、备料、制冰、出杯速度与差评风险。',
    '写清让利目标（守单/获客/填闲时），再选入口款与范围。',
    '测试前写下停止条件；触发则缩范围、换产品或停活动。',
  ],
  pitfalls: [
    '只盯对手标价，不先算自己的贡献与持平销量。',
    '把活动页价格当成到手结算价。',
    '把活动订单增长等同于新客增长，忽视原价客蚕食。',
    '全店齐降，把主力利润款一起拖下水。',
    '照抄连锁 9.9，忽略采购/流量/排班/库存差异。',
    '不写停止条件，忙到无法回头。',
  ],
  shifts: [
    ['以前：跟不跟看对手卖多少', '现在：先算降价后要多卖多少杯才持平'],
    ['以前：订单涨了就高兴', '现在：先问贡献、结算、产能是否扛得住'],
    ['以前：要么全跟要么全不跟', '现在：入口款+边界测试+停止条件'],
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
        <div class="node ${i === d.map.length - 1 ? 'node-green' : i === 2 ? 'node-orange' : i === 3 ? 'node-purple' : ''}">
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
    <h3>横向对照：信号能推出什么</h3>
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
    <p>价格战的关键不是标价面子，而是单杯贡献、实际结算与高峰产能能否支撑；订单增长若不带来新客与复购，可能只是用利润换忙碌。小店更适合有边界的入口款测试，而不是全店齐降。</p>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>

  <div class="footer">双轨产物 · 理性分析 SVG · 与图文实录共享同一转录证据 · b62h</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'b62h-svg-height.txt'),
  String(height),
  'utf8',
);
