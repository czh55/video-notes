#!/usr/bin/env node
/**
 * b62p：生成 chat-for-feelings-not-facts 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'chat-for-feelings-not-facts-理性分析.svg');

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
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:14px;padding:14px 18px;text-align:center;min-width:120px;font-weight:700;font-size:14px;color:#1e40af}
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
  title: '聊天不要聊事实，要聊点让人爽的',
  duration: '9分46秒',
  url: 'https://xhslink.cn/o/8hOsu422nrh',
  tags: ['职场社交', '情绪价值', '闲聊', '感受回应', '沟通训练'],
  perspective: '理性分析 · 职场社交',
  summary:
    '核心命题：为什么「说得对」却接不上话？作者主张闲聊的交付物不是事实同步，而是情绪、感受与共鸣；用十天微习惯（感受词→翻译→夸张→听弦外音→共同体验→情绪反馈→追问→四步串联）把情绪价值练成肌肉记忆。证据层级为口播教学与示范句，属社交策略建议，非普适沟通定律。',
  timeline: [
    ['00:00', '反差：招人喜欢 vs 说对却冷场'],
    ['00:39', 'Day1 自检：事实回应 / 感受回应'],
    ['01:26', 'Day2 感受词口头禅'],
    ['02:19', 'Day3 事实翻译法公式'],
    ['03:10', 'Day4 适度夸张+语气词'],
    ['04:08', 'Day5 隐藏情绪与共鸣目的'],
    ['04:50', 'Day6 共同体验法'],
    ['05:47', 'Day7 情绪反馈/共同体'],
    ['06:37', 'Day8 追问感受公式'],
    ['07:34', 'Day9 四步流程+书《学会闲聊》'],
    ['08:49', 'Day10 一个月每日三次固化'],
  ],
  map: [
    ['问题', '说对却冷场'],
    ['诊断', '只回事实'],
    ['技能栈', '感受工具箱'],
    ['流程', '四步串联'],
    ['目标', '情绪价值'],
  ],
  corrections: [
    '误解：闲聊=找话题。纠偏：作者明确核心是读懂言语背后的情绪，并持续提供情绪价值。',
    '误解：感受回应=否定事实/瞎吹。纠偏：事实翻译仍承认事实，再补情绪与认同；夸张是「放大一点点」，不是编造。',
    '误解：职场任何场合都应优先情绪。纠偏：视频场景偏生活闲聊与关系维护；正式汇报、跨部门对齐仍须先保证信息准确（补充边界）。',
    '立场分层：示范句与十天作业可验证为作者教法；「身边所有人都喜欢跟你聊天」属效果承诺，证据仅为口播推断，应降级为可能改善。',
  ],
  cards: [
    {
      title: '在讲什么：把「对」换成「懂」',
      body: '关键理解：事实回应完成听懂信息的最低义务；感受回应完成「被理解」的社交义务。用法：回消息前先问——我是在复述事实，还是在命名对方的感受？',
      quote: '事实只是让人知道你在听，而感受会让人觉得你懂他',
      relation: '听懂信息 ≠ 让人愿意继续聊',
      tone: 'card',
    },
    {
      title: '在讲什么：事实翻译公式',
      body: '关键理解：对方抛出的是事件，你要译出情绪标签并加上认同。用法：事件（跑五公里/买新包）→ 情绪（爽/解压/有气质）→ 认同（眼光真好）。',
      quote: '就是你要说出对方的情绪，再加上你的认同',
      relation: '事实 → 情绪标签 → 认同 = 可复用模板',
      tone: 'card-green',
    },
    {
      title: '在讲什么：从单句到四步流程',
      body: '关键理解：单点技巧可叠成本能：感受词开头 → 翻译情绪 → 联结体验 → 追问感受。用法：选一个真实场景完整走一遍，而不是只背词库。',
      quote: '先用感受词开头，然后再翻译对方的情绪……最后呢追问对方的感受',
      relation: '工具箱 → 串联流程 → 本能反应',
      tone: 'card-purple',
    },
    {
      title: '风险边界：情绪价值也有适用条件',
      body: '关键理解：过度夸张、过度共情或在正式场合抢先情绪化，可能显得假或耽误事。用法：朋友吐槽可用共情；领导要数据时先交事实。',
      quote: '说话的目的不是传递信息，而是寻求共鸣',
      relation: '作者闲聊立场 ≠ 全场景沟通原则；需按关系与任务切换。',
      tone: 'card-orange',
    },
  ],
  compare: [
    ['维度', '事实回应', '感受回应（作者教法）', '适用提醒'],
    ['加班到十点', '辛苦了，早点休息', '十点才下班，老板也太黑了吧', '注意对方是否想吐槽还是求建议'],
    ['跑五公里', '不错，坚持锻炼', '跑完肯定特别爽，出汗太解压', '别抢着给运动建议'],
    ['被领导表扬', '哎呀恭喜', '当时什么感受？有被看见的感觉吗？', '公开场合追问要看关系亲疏'],
    ['闲聊目标', '同步信息', '提供情绪价值/共鸣', '正式协作仍优先信息准确'],
  ],
  actions: [
    '今天翻三段聊天记录，标出事实句与感受句比例。',
    '对五条朋友圈只用感受词开头回复（太棒了/心疼你/好气啊…）。',
    '选十个日常事实句，各写一句「情绪+认同」翻译。',
    '用四步流程回复一次真实吐槽：感受词→翻译→我也懂→追问还好吗。',
    '接下来七天每天至少三次「感受回应」，周末复盘哪一步最卡。',
  ],
  pitfalls: [
    '夸张不配语气词，听感假、用力过猛。',
    '把「寻求共鸣」用到必须对齐事实的会议纪要场景。',
    '共同体验变成抢戏：「我也…」讲太长，对方没空间。',
    '追问感受像审讯：连珠炮「是不是特别…」不顾对方不愿展开。',
    '把「所有人都喜欢跟你聊」当保证，忽视性格与边界差异。',
  ],
  shifts: [
    ['以前：把闲聊当成找话题', '现在：先读情绪，再提供情绪价值'],
    ['以前：回「辛苦了/不错/真好」收工', '现在：命名感受+认同+可选追问'],
    ['以前：技巧零散记几句漂亮话', '现在：按十天微习惯叠成四步本能'],
  ],
};

const timelineHtml = d.timeline
  .map(
    ([t, text]) =>
      `<div class="timeline-item"><div class="timeline-time">${esc(t)}</div><div class="timeline-text">${esc(text)}</div></div>`,
  )
  .join('');

const mapHtml = d.map
  .map((node, i) => {
    const cls =
      i === 0 ? 'node' : i === d.map.length - 1 ? 'node-green' : i === 1 ? 'node-orange' : 'node-purple';
    const [a, b] = node;
    return `${i ? '<div class="arrow">→</div>' : ''}<div class="${cls}"><div>${esc(a)}</div><div style="font-size:12px;font-weight:600;margin-top:4px">${esc(b)}</div></div>`;
  })
  .join('');

const cardsHtml = d.cards
  .map(
    (c) => `<div class="card ${c.tone}">
  <h3>${esc(c.title)}</h3>
  <p>${esc(c.body)}</p>
  <div class="quote">${esc(c.quote)}</div>
  <div class="relation">${esc(c.relation)}</div>
</div>`,
  )
  .join('\n');

const tableHtml = `<table><tr>${d.compare[0].map((h) => `<th>${esc(h)}</th>`).join('')}</tr>${d.compare
  .slice(1)
  .map((row) => `<tr>${row.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`)
  .join('')}</table>`;

const body = `<div class="root-wrap"><div class="container">
  <h1>${esc(d.title)}</h1>
  <div class="meta">
    ${d.tags.map((t) => `<span class="tag tag-blue">${esc(t)}</span>`).join('')}
    <span class="tag tag-gray">${esc(d.duration)}</span>
    <span class="tag tag-purple">${esc(d.perspective)}</span>
  </div>
  <a class="source-link" href="${esc(d.url)}">原视频（小红书短链）</a>
  <div class="summary-line">${esc(d.summary)}</div>

  <div class="timeline"><h3>关键证据时间轴</h3>${timelineHtml}</div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">${mapHtml}</div>
  </div>

  <div class="correction">
    <h3>常见误解与认知纠偏</h3>
    ${d.corrections.map((x) => `<p>${esc(x)}</p>`).join('')}
  </div>

  <div class="section">
    <h2 class="sec-title">观点卡片</h2>
    ${cardsHtml}
  </div>

  <div class="card">
    <h3>横向对比：事实回应 vs 感受回应</h3>
    ${tableHtml}
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <ul>
      <li>闲聊交付的是情绪价值，不是事实同步。</li>
      <li>可复用栈：感受词、事实翻译、适度夸张、听弦外音、共同体验、情绪反馈、追问。</li>
      <li>第九天四步串联：感受词→翻译→联结→追问；第十天用每日三次固化。</li>
    </ul>
    <h3>行动清单</h3>
    <ol>${d.actions.map((a) => `<li>${esc(a)}</li>`).join('')}</ol>
    <h3>避坑</h3>
    <ul>${d.pitfalls.map((p) => `<li>${esc(p)}</li>`).join('')}</ul>
    <h3>关键认知转变</h3>
    <ul>${d.shifts.map(([a, b]) => `<li>${esc(a)} → ${esc(b)}</li>`).join('')}</ul>
  </div>
  <div class="footer">双轨产物 · 理性分析 · 证据来自 Whisper 转录与片内字幕 · 未访问小红书</div>
</div></div>`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(
  path.join(DIR, '..', '_work', 'chat-for-feelings-not-facts-svg-height.txt'),
  String(height),
  'utf8',
);
