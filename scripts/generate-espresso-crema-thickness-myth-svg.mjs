#!/usr/bin/env node
/**
 * b62n：生成 espresso-crema-thickness-myth 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'espresso-crema-thickness-myth-理性分析.svg');

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
  title: '浓缩的油脂越厚，就越好喝吗？',
  duration: '2分24秒',
  url: 'https://xhslink.cn/o/3ia9NIz5I2O',
  tags: ['意式浓缩', 'Crema', '泡沫', '排气', '粉碗'],
  perspective: '理性分析 · 咖啡手作 · 感官判断',
  summary:
    '核心命题：浓缩杯面「油脂」越厚是否等于越好喝？作者结论是否定的——那一层主要是 crema 泡沫，厚度优先反映起泡能力与气体残留，不能换算成精华或品质。排气、豆种、粉碗都会改观感；决策应先搅匀，再用整杯味道判断。',
  timeline: [
    ['00:00', '反差：厚得像奶盖却苦又糙'],
    ['00:15', '正名：油脂=crema；体积靠气泡'],
    ['00:36', '机制：粉碗减压冒泡≈汽水开瓶'],
    ['00:56', '边界：能起泡≠萃出更多精华'],
    ['01:03', '排气：同一包豆泡沫可变薄'],
    ['01:24', '豆种：罗布斯塔泡沫多≠脂肪更高'],
    ['01:37', '设备：双层增压粉碗可「造」泡沫'],
    ['01:58', '行动：搅匀后评酸苦/杂味/余味'],
  ],
  map: [
    ['问题', '厚=好喝？'],
    ['正名', '油脂→crema'],
    ['机制', 'CO₂ 气泡'],
    ['变量', '排气/豆种/粉碗'],
    ['行动', '搅匀品整杯'],
  ],
  corrections: [
    '误解：杯面「油脂」越厚越好喝。纠偏：开场反例已拆开——厚得像奶盖仍可能苦又糙。',
    '误解：厚度=萃出更多精华。纠偏：泡沫多首先说明比较能起泡，不能直接换算成精华。',
    '误解：泡沫变薄=咖啡变难喝。纠偏：排气使气体减少即可变薄，不等于品质崩坏。',
    '误解：厚度=含油量。纠偏：罗布斯塔往往泡沫更多，阿拉比卡脂肪含量反而可能更高。',
    '误解：泡沫好看=萃取好。纠偏：增压粉碗也能让泡沫更好看；风味与萃取要另判。',
    '立场分层：crema 气体机制与搅匀品鉴步骤属作者科普叙事；「研究里泡沫更多香气不继续增加」为作者转述、视频未给文献名；「别用厚度打分」是作者观点。',
  ],
  cards: [
    {
      title: '在讲什么：把「油脂」还原成泡沫',
      body: '关键理解：口语「油脂」≠纯油层；crema 含液、油与其他成分，但撑起体积的是气泡。用法：看见厚 crema 时先问「起泡条件」，再问「味道」。',
      quote: '实际是一层咖啡泡沫，叫crema',
      relation: '视觉厚度 ← 气泡体积；油只是成分之一，不是厚度的充分解释。',
      tone: 'card',
    },
    {
      title: '在讲什么：气体从哪来、为何变薄',
      body: '关键理解：烘焙二氧化碳留在豆内，加压萃取带入液中，出粉碗减压冒泡；气泡破裂则变薄。用法：用「排气进度」解释同豆前后天的泡沫差异。',
      quote: '泡沫多，首先说明这杯比较能起泡，不能直接换算成萃出了更多精华',
      relation: '气体残留 ↓ → 起泡潜力 ↓ → 泡沫可变薄；味道曲线需单独测量。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：豆种与粉碗是混淆变量',
      body: '关键理解：品种与设备都能改泡沫观感，却不保证风味与含油量同向。用法：家用增压粉碗出「漂亮泡沫」时，不要据此宣称萃取成功。',
      quote: '这层油脂的厚度和真正含了多少油，并不是一回事',
      relation: '罗布斯塔/增压粉碗 → 泡沫观感↑；脂肪含量与萃取质量仍可能独立变化。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：可执行的品鉴顺序',
      body: '关键理解：泡沫会影响香气释放与入口感受，但不是「越多越好」。用法：轻轻搅匀 → 评酸苦协调、杂味、余味；禁止只尝最上面一口下结论。',
      quote: '把它当观察线索，最后用整杯的味道判断',
      relation: '泡沫=弱信号；整杯味道=主判决。',
      tone: 'card-orange',
    },
  ],
  table: [
    ['信号', '可能意味着', '不能单独推出'],
    ['刚出品泡沫很厚', '气体充足、起泡条件好', '一定好喝 / 一定萃得好'],
    ['放几天后泡沫变薄', '豆子排气，可冒出气体减少', '咖啡一定变难喝'],
    ['罗布斯塔泡沫更多', '品种起泡倾向不同', '脂肪含量一定更高'],
    ['增压粉碗泡沫好看', '出口阻力改变泡沫形成', '风味与萃取已达标'],
    ['只尝最上面一口', '主要碰到泡沫层', '代表整杯品质'],
  ],
  actions: [
    '出品后先观察泡沫，但不给分；把它记成「起泡线索」。',
    '喝前轻轻搅匀，让泡沫与咖啡液混合再入口。',
    '按清单评：酸苦是否协调、有无杂味、余味是否舒服。',
    '同豆泡沫变薄时，先查排气与新鲜度窗口，不要立刻重磨追「更厚」。',
    '家用增压粉碗场景：泡沫好看与萃取质量拆开评估。',
  ],
  pitfalls: [
    '用 crema 厚度给浓缩打分，忽略苦糙与杂味。',
    '把泡沫变薄直接等同于「豆子坏了」。',
    '以为含油更多的豆就一定泡沫更厚。',
    '被增压粉碗的漂亮泡沫误导，跳过风味判断。',
    '只尝最上面一口就给整杯下结论。',
  ],
  shifts: [
    ['以前：油脂越厚越好喝', '现在：厚度优先反映起泡，味道另判'],
    ['以前：盯杯面厚度', '现在：搅匀后评整杯'],
    ['以前：泡沫变薄=失败', '现在：可能只是排气，需对照味道'],
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
        <div class="node ${i === d.map.length - 1 ? 'node-green' : i === 2 ? 'node-orange' : ''}">
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
    <p>浓缩杯面「油脂」是 crema 泡沫，厚度不是好喝仪表。气体、豆种与粉碗都会改观感；搅匀后的整杯味道才是主判决。</p>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>

  <div class="footer">双轨产物 · 理性分析 SVG · 与图文实录共享同一转录证据 · 不同于 coffee-bean-surface-oil（整豆表面出油议题）</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'b62n-svg-height.txt'),
  String(height),
  'utf8',
);
