#!/usr/bin/env node
/**
 * b62c：生成 english-rhythm-melody-rules 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'english-rhythm-melody-rules-理性分析.svg');

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
  title: '说英语必须掌握节奏和旋律规律',
  duration: '1分09秒',
  url: 'https://xhslink.cn/o/1zY9O3Ur17C',
  tags: ['美音语调', '口语节奏', '短语从句', '张力释放', '跟练模板'],
  perspective: '理性分析 · 职场口语表达',
  summary:
    '核心命题：口语难懂，往往不是单词错，而是缺少可预期的旋律线——未完成信息块上扬吊住听者，完成后下落释放。作者给出可立刻跟练的「上-上-下」节奏型，并用介词短语与 if 从句链举证。证据层级：画面硬字幕+口播示范（可核验操作）；「更有音乐性/更易懂」属作者教学主张。',
  timeline: [
    ['00:00', '命题：English is music / 每句有上下'],
    ['00:09', '规则：往上造张力 → 往下释放'],
    ['00:18', '落点：短语/从句结束后上扬'],
    ['00:28', '示例：介词短语 on the table 等'],
    ['00:42', '示例：clause 定义 + if…if…we can…'],
    ['00:53', '主张：更有音乐性与逻辑，更易被理解'],
    ['01:02', 'CTA：点赞关注（无新知识点）'],
  ],
  map: [
    ['问题', '口语为何难懂'],
    ['机制', '张力↑ / 释放↓'],
    ['落点', '短语·从句边界'],
    ['模板', '介词短语 / if链'],
    ['结果', '更好懂'],
  ],
  corrections: [
    '误解：学口语=把每个词读清楚。纠偏：作者强调的是信息块边界上的音高走向，而不是逐词用力。',
    '误解：上扬只用于一般疑问句。纠偏：片中把上扬用在「信息尚未结束」的短语/从句后，属于话语组织信号。',
    '误解：clause 很难。纠偏：作者给极简定义——带动词的短语；先用于节奏练习，不展开语法体系。',
    '立场分层：字幕中的操作句可核验；「听起来更有音乐性/人们会理解你」是教学效果主张，非受控实验结论。',
  ],
  cards: [
    {
      title: '在讲什么：英语=音乐（命题）',
      body: '关键理解：先建立「句子有旋律线」的听感，再谈具体规则。用法：跟练前先用 da-da-da 或无意义音节感受起伏，再套真实词。',
      quote: 'English is music / 英语就是音乐',
      relation: '命题（音乐隐喻）→ 为张力/释放规则提供直觉锚点。',
      tone: 'card',
    },
    {
      title: '在讲什么：张力与释放（机制）',
      body: '关键理解：上扬不是「激动」，而是制造未完成感；下落不是「小声」，而是标记信息结束。用法：录自己说长句，标出哪里该吊住、哪里该落地。',
      quote: 'You go up and build up the tension… go down to release it',
      relation: '机制（张力↔释放）→ 决定听者何时继续等、何时可以处理完整意群。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：短语/从句边界上扬（落点）',
      body: '关键理解：真正要练的是「边界选择」——说完 phrase/clause 后上扬。用法：先切块再发音，不要边想边平推整句。',
      quote: 'go up after you finish saying a phrase or a clause',
      relation: '语法单位（短语/从句）被借用为节奏切点，服务可预期性。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：两套跟练模板',
      body: '关键理解：介词短语练短边界；if 从句链练「上-上-下」长边界。用法：每天各跟读 5 遍，刻意夸张音高差，再收回自然幅度。',
      quote: 'on the table… if I also have time… we can eat together',
      relation: '短模板练切块，长模板练多级张力后再释放。',
      tone: 'card-orange',
    },
  ],
  table: {
    title: '节奏决策：何时上扬 / 何时下落',
    head: ['信号', '典型位置', '听者感受', '片中证据'],
    rows: [
      ['上扬', '短语/从句刚结束、信息未完', '还会继续，先别下结论', 'phrase or clause 后 go up'],
      ['下落', '完整信息结束', '可以处理/回应', 'release / we can eat together'],
      ['上-上-下', '并列条件 + 结论', '逻辑链清晰', 'if… / if… / we can…'],
      ['平推', '整句同高（反例）', '难抓重点、像念词表', '作者隐含对照，未做实验数据'],
    ],
  },
  boundary: [
    '片长约 69 秒，只覆盖一种常用语调策略，不覆盖全部英语语调（如列举调、反问调、强调重音系统）。',
    '作者以美音教学口吻示范；其他口音/正式演讲场景可能需要不同幅度，不能直接当「唯一正确」。',
    'clause 定义被极度简化，服务节奏练习，不能替代系统语法学习。',
    '「更易理解」是作者主张；未提供听辨实验或母语者评分数据。',
  ],
  pitfalls: [
    '每个词都上扬，听起来像一直没说完——上扬只挂在信息块边界。',
    '把疑问句上扬习惯硬套到陈述收束，导致该落地时仍吊着。',
    '只背「上-上-下」口号，不先切短语/从句，节奏会落在错误音节上。',
    '夸张练习后不回收：日常对话需要自然幅度，课堂夸张只是肌肉记忆阶段。',
  ],
  conclusion: {
    key: [
      '口语可懂度≈可预期旋律：未完成上扬、完成下落。',
      '练边界比练单词更优先：phrase/clause 是切点。',
      '两套模板够入门：介词短语短练 + if 链长练。',
    ],
    actions: [
      '选 3 个你常说的介词短语，录一遍「边界上扬→后续下落」。',
      '用 if A / if B / we can C 造一句与自己相关的条件链，标出两上一下。',
      '对着片中字幕跟读，手势同步上抬/下压，强化肌肉记忆。',
      '找一段自己过去的英文语音，标出本该释放却仍平推的位置并重录。',
      '把「上-上-下」写进手机备忘，开会开口前先切块再发音。',
    ],
    shift: '从「把音素念对」转向「让听者知道信息何时未完、何时可落地」。',
  },
};

function body(data) {
  const tags = data.tags
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`)
    .join('');
  const timeline = data.timeline
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const map = data.map
    .map(([a, b], i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node-purple'][i % 4];
      const ar = i < data.map.length - 1 ? '<span class="arrow">→</span>' : '';
      return `<div class="${cls}">${esc(a)}<br/>${esc(b)}</div>${ar}`;
    })
    .join('');
  const corr = data.corrections.map((c) => `<p>${esc(c)}</p>`).join('');
  const cards = data.cards
    .map(
      (c) =>
        `<div class="card ${c.tone}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p><div class="quote">${esc(c.quote)}</div><div class="relation">${esc(c.relation)}</div></div>`,
    )
    .join('');
  const thead = `<tr>${data.table.head.map((h) => `<th>${esc(h)}</th>`).join('')}</tr>`;
  const tbody = data.table.rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
  const bound = data.boundary.map((b) => `<li>${esc(b)}</li>`).join('');
  const pits = data.pitfalls.map((p) => `<div class="pitfall">${esc(p)}</div>`).join('');
  const key = data.conclusion.key.map((k) => `<li>${esc(k)}</li>`).join('');
  const act = data.conclusion.actions.map((a) => `<li>${esc(a)}</li>`).join('');

  return `<div class="container root-wrap">
  <h1>${esc(data.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(data.duration)}</span><span class="tag tag-gray">${esc(data.perspective)}</span></div>
  <a class="source-link" href="${esc(data.url)}">原视频</a>
  <div class="summary-line">${esc(data.summary)}</div>
  <div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${map}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corr}</div>
  <div class="section"><h2 class="sec-title">观点卡片：命题→机制→模板</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">${esc(data.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${bound}</ul><h3>避坑</h3>${pits}</div></div>
  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3><ul>${key}</ul>
    <h3>行动清单</h3><ol>${act}</ol>
    <h3>关键认知转变</h3><p>${esc(data.conclusion.shift)}</p>
  </div>
  <div class="footer">双轨产物之二 · 理性分析 · b62c · ${esc(data.duration)}</div>
</div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: body(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(path.join(DIR, '..', '_work', 'b62c-svg-height.txt'), String(height));
