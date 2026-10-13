#!/usr/bin/env node
/**
 * b62l：生成 coffee-110-aromas-myth 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'coffee-110-aromas-myth-理性分析.svg');

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
  title: '咖啡真的有 110 种香气吗？',
  duration: '4分05秒',
  url: 'https://xhslink.cn/o/5kT10zg9OBj',
  tags: ['感官词典', 'WCR', '风味轮', '鼻后嗅觉', '品鉴训练'],
  perspective: '理性分析 · 咖啡手作 · 感官语言',
  summary:
    '核心命题：「110 种香气」是不是咖啡风味的事实上限？作者结论是否定的——110 是 WCR 感官词典第一版的感官属性数（含味觉与口感），且是会更新的活词典。风味轮是地图而非答案库，应从中心往外描述；包装风味词是相似描述不是配料表；新手只喝到酸苦属正常，具体香气依赖鼻后嗅觉与感官记忆训练。',
  timeline: [
    ['00:00', '包装写草莓茉莉，却只喝到酸苦'],
    ['00:12', '答案：110≠香气总数/上限；WCR 词典属性'],
    ['00:49', '也收录霉味泥土味甚至石油气味'],
    ['01:10', '尺子描述强度，不是自动评分表'],
    ['01:28', '风味轮从中间往外：大类→子类→具体'],
    ['01:46', '酸苦靠舌；具体风味要鼻子参与'],
    ['02:46', '咖啡师差在记忆与参考物校准'],
    ['03:10', '包装「草莓」=相似描述≠配料表'],
    ['03:15', '厨房参考物练习；先问感受到了什么'],
  ],
  map: [
    ['问题', '110=香气上限？'],
    ['定义', 'WCR 感官属性'],
    ['工具', '风味轮=地图'],
    ['机制', '舌+鼻后嗅觉'],
    ['用法', '由内向外描述'],
    ['行动', '练记忆不问答案'],
  ],
  corrections: [
    '误解：咖啡正好有 110 种香气。纠偏：110 是第一版词典的感官属性条目数，含酸苦与口感质地，不是香气清单长度。',
    '误解：110 是风味天花板。纠偏：作者转述 WCR——活词典、基于有限样品，会继续更新。',
    '误解：风味轮用来从外圈对包装答案。纠偏：应从中心大类往外细化，可停在任一层。',
    '误解：喝不出草莓=味觉差。纠偏：酸苦是基础味觉；具体香气依赖鼻后通路与感官记忆，可训练。',
    '误解：包装写草莓=加了草莓或必须喝出草莓汁。纠偏：对未额外加味豆，草莓是交流用相似描述；加味/共发酵另判。',
    '立场分层：WCR 词典定义与活词典说法属作者科普转述（未在视频中展示原文出处页）；用法建议与训练步骤是作者观点。',
  ],
  cards: [
    {
      title: '在讲什么：110 的准确定义',
      body: '关键理解：把「香气种数」改写成「可共享的描述条目」。用法：看见营销文案写 110 种香气时，先问它指的是词典属性还是化学挥发物种类。',
      quote: '110指的是世界咖啡研究组织也就是WCR建立的咖啡感官词典第一版里的110个感官属性',
      relation: '属性集合 ⊃ 香气词；样本有限 → 词典可更新 → 110 不是自然常数。',
      tone: 'card',
    },
    {
      title: '在讲什么：词典是尺子不是排行榜',
      body: '关键理解：负面描述与正面描述同一套语言系统。用法：杯测或交流时先记录「出现了什么 / 强度」，再另开评价层讨论喜不喜欢。',
      quote: '它是一把用来描述和测量的尺子，不是一张自动评分表',
      relation: '描述词库 ≠ 品质排序；收录石油气味 ≠ 推荐该风味。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：风味轮的读写方向',
      body: '关键理解：外圈具体词是终点可选，不是起点必答。用法：先水果/坚果可可，再莓果核果柑橘，再橙子——停在你能稳定复述的那一层。',
      quote: '正确的方法恰恰是从中间往外走',
      relation: '地图导航：中心定位 → 分层细化；对包装外圈「找答案」会反向放大自我怀疑。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：为什么你只感到酸苦',
      body: '关键理解：舌头负责基础味觉，具体风味大量依赖鼻后嗅觉。用法：品鉴时留意吞咽/呼气后的回香；用黄连 vs 黑巧克力理解「同苦不同风味」。',
      quote: '你以为自己在尝草莓，其实其中很大一部分信息是闻到的',
      relation: '基础味觉（舌）× 气味记忆（鼻）× 口感余味 → 可交流的风味词。',
      tone: 'card-orange',
    },
    {
      title: '在讲什么：包装词与训练路径',
      body: '关键理解：咖啡师优势常在校准过的记忆库，不在神秘舌头。用法：厨房参考物先建立气味锚点；包装「草莓」先落到莓果大类再比相似度；加味豆单独标注。',
      quote: '所以草莓是帮助交流的相似描述，不是配料表',
      relation: '未加味豆：相似描述；加味/共发酵：成分叙事另判。',
      tone: 'card-red',
    },
  ],
  table: [
    ['说法', '更准确的理解', '不要推出'],
    ['110 种香气', '第一版词典约 110 个感官属性', '化学上只有 110 种挥发物'],
    ['风味轮外圈草莓', '可选的具体相似描述', '必须从外圈对答案'],
    ['只喝到酸苦', '舌头基础味觉优先被感知', '味觉天生不合格'],
    ['包装写草莓', '莓果类相似沟通词（未加味语境）', '豆子加了草莓/等于草莓汁'],
    ['咖啡师说蓝莓', '记忆与参考物校准后的命名', '舌头必然更灵'],
  ],
  actions: [
    '看到「110 种香气」：改读为「感官描述条目」，并记住词典会更新。',
    '读风味轮：强制从中心大类开始，外圈词只在有把握时使用。',
    '品鉴时：先记酸苦甜咸，再主动关注鼻后回香，用「更像什么」而不是「必须等于」。',
    '训练：用橙子/柠檬/葡萄柚 + 杏仁花生黑巧红糖做闭眼辨闻，建立气味记忆。',
    '读包装：把风味词当交流提示；遇明确加味或共发酵，单独标注再判断。',
  ],
  pitfalls: [
    '把 110 当成香气上限或营销神数。',
    '拿风味轮从最外圈硬找包装答案，越找越自我怀疑。',
    '把「喝不出具体水果」等同于味觉失败。',
    '把包装风味词读成配料表或唯一标准答案。',
    '未区分普通豆与加味/共发酵豆，用同一套「相似描述」逻辑硬套。',
  ],
  shifts: [
    ['以前：110=香气种数天花板', '现在：110=词典属性条目，且可更新'],
    ['以前：风味轮用来对答案', '现在：风味轮用来分层表达当下感受'],
    ['以前：喝不出草莓=我不行', '现在：先大类再细化，酸苦正常、香气可练'],
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
    <h3>横向对照：说法能推出什么</h3>
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
    <p>110 是感官描述语言的版本快照，不是香气自然上限；风味轮服务表达，不服务对答案。酸苦正常，具体香气靠鼻后嗅觉与记忆训练；包装词是沟通提示。</p>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>

  <div class="footer">双轨产物 · 理性分析 SVG · 与图文实录共享同一转录证据 · b62l / coffee-110-aromas-myth</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'b62l-svg-height.txt'),
  String(height),
  'utf8',
);
