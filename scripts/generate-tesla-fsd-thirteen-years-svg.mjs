#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'tesla-fsd-thirteen-years-理性分析.svg');
const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:26px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:20px;font-weight:700;color:#1e40af;margin:20px 0 10px;padding-bottom:6px;border-bottom:2px solid #e2e8f0}
h3{font-size:15px;font-weight:700;color:#334155;margin-bottom:8px}
p,li{font-size:13px;line-height:1.65;color:#475569;margin-bottom:4px}
ul,ol{padding-left:20px}
.tag{display:inline-block;padding:3px 10px;border-radius:16px;font-size:12px;font-weight:600;margin-right:6px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:8px 0 12px}
.summary-line{font-size:15px;line-height:1.65;padding:14px 16px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:12px;color:#334155;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:14px;padding:14px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline-item{display:flex;gap:10px;padding:4px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:12px;font-weight:700;color:#3b82f6;min-width:58px}
.timeline-text{font-size:13px;color:#475569}
.map{background:#fff;border-radius:16px;padding:18px;margin-bottom:12px;box-shadow:0 4px 20px rgba(0,0,0,.05)}
.map h2{margin:0;border:none;padding:0}
.diagram{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;padding:10px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:12px;padding:10px 14px;text-align:center;min-width:110px;font-weight:700;font-size:12px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:18px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:12px 14px;border-radius:10px;margin-bottom:12px}
.correction h3,.correction p{color:#92400e}
.sec-title{font-size:17px;font-weight:700;color:#1e40af;margin:6px 0 10px;padding-left:10px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:12px;padding:14px;margin-bottom:8px;border-left:5px solid #3b82f6;box-shadow:0 3px 16px rgba(0,0,0,.04)}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:14px;color:#1e40af}
.card .quote{background:#f8fafc;padding:8px 10px;border-radius:8px;margin:6px 0;font-size:12px;color:#64748b;border-left:3px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:8px 10px;border-radius:8px;font-size:12px;color:#166534}
.card .pitfall{background:#fef2f2;padding:8px 10px;border-radius:8px;margin:6px 0;font-size:12px;color:#991b1b;border-left:3px solid #ef4444}
table{width:100%;border-collapse:collapse;font-size:12px}
th{background:#f1f5f9;padding:8px;text-align:left;color:#1e40af}
td{padding:8px;border-bottom:1px solid #e2e8f0;vertical-align:top;color:#475569}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:16px;padding:20px;margin-top:14px}
.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}
.conclusion h3{color:rgba(255,255,255,.9);margin:10px 0 6px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9)}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:16px 0}
.source-link{color:#3b82f6;font-size:13px;text-decoration:none;display:inline-block;margin-bottom:10px}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

const esc = (s) => String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');

const d = {
  title: '特斯拉 FSD 十三年｜交出方向盘的冒险与经济之战',
  duration: '62分35秒',
  url: 'https://b23.tv/QQer1jF',
  tags: ['FSD', 'CyberCab', '端到端', 'Waymo', '硅谷101'],
  perspective: '理性分析 · 自动驾驶产业',
  summary: '核心判断：FSD 故事的主轴不是「纯视觉是否正确」，而是特斯拉用成本纪律+风险偏好，把未成熟系统装进量产车飞轮；硬件/软件反复推倒重来后，下半场改名经济之战——谁能在可证明安全下把单位出行成本打下来。',
  timeline: [
    ['00:20', 'CyberCab 无方向盘'],
    ['04:00', '与谷歌分道 / HW1'],
    ['06:30', 'Mobileye 分手'],
    ['09:40', 'AI3 自研成功'],
    ['17:40', 'Karpathy 重构感知'],
    ['21:40', '去雷达（供应链）'],
    ['23:40', 'Occupancy Network'],
    ['31:00', 'HW4 三→双芯片'],
    ['39:20', '端到端 V12'],
    ['50:20', 'Robotaxi 远程监管'],
    ['53:00', 'Dojo 停 / AI5 瞒报'],
    ['59:30', '经济之战收束'],
  ],
  map: [
    ['问题', '为何是特斯拉做出FSD'],
    ['证据', '13年软硬拉扯史'],
    ['判断', '风险偏好=飞轮燃料'],
    ['行动', '看成本/安全扩城'],
  ],
  corrections: [
    '误解：去雷达=技术已经完美。纠偏：口播称疫情供应链是催化剂，团队被迫补纯视觉测距。',
    '误解：端到端是特斯拉发明。纠偏：理念更早出现；特斯拉强在量产车落地与数据闭环。',
    '误解：路线已分胜负。纠偏：Waymo 运营仍领先；CyberCab 刚起步且面临监管调查。',
  ],
  cards: [
    { title: '路线分叉：L2 飞轮 vs L4 划界', body: '谷歌/Waymo 贵传感器+地理围栏做稳再扩；特斯拉摄像头进数百万车、事故与更新中迭代。', quote: '两条路线依然没有分出胜负', relation: '比较对象应从口号改为运营里程、干预率与单位成本。', tone: 'card-purple' },
    { title: '硬件主线：掌控感>纸面算力', body: 'Mobileye 黑盒→英伟达过渡→AI3/AI4 自研；AI5 因瞒报失控后双工艺并行。', quote: '你没有这个控制权', relation: '供应商扯皮与成本逼迫，解释了为何死磕自研。', tone: 'card-blue' },
    { title: '软件主线：感知重构→端到端', body: 'HydraNet/BEV/占据网络铺路；V12 替换规则；V13 剪枝提效；V14 放大+强化学习。', quote: '把三十万行代码精简到极少输出', relation: '可解释性靠中间表征头；验证靠世界模型仿真。', tone: 'card-green' },
    { title: '商业化瓶颈：远程监管可扩展性', body: 'CyberCab 现阶段安全靠远程兜底；扩到规模后人工比例决定经济性。', quote: '如何在保证安全的情况下快速扩城才是最大的挑战', relation: '下半场名字叫经济之战。', tone: 'card-orange' },
  ],
  table: {
    title: '关键里程碑对照',
    head: ['阶段', '硬件锚点', '软件/产品锚点', '张力'],
    rows: [
      ['2014–16', 'HW1 Mobileye', 'Autopilot 基础；事故与决裂', '黑盒接口'],
      ['2016–19', 'HW2/2.5→AI3', '自研感知起步', '人手与冗余'],
      ['2018–21', 'HW3', 'HydraNet/BEV；去雷达', '供应链 vs 叙事'],
      ['2020–23', 'HW4 AI4', '占据网络；端到端前夜', '芯片数/GDDR'],
      ['2023–25', 'AI4 车端', 'V12–V14；Robotaxi', '黑盒可验证性'],
      ['2025–', 'AI5 双工艺', 'Dojo 停；扩城/监管', '经济性证明'],
    ],
  },
  boundary: ['内容含前员工口述与媒体传言，作产业笔记非官方时间表。', '版本号（V14/V15）与装车策略可能随官方发布变化。', '「伊朗」等 ASR 指马斯克（Elon），文中已按语境校正。'],
  pitfalls: ['只站队摄像头/激光雷达而不看单位出行成本。', '把演示里程碑等同于无安全员规模化运营。', '忽略远程监管人力在早期 Robotaxi 成本中的占比。'],
  conclusion: {
    key: ['差分是风险偏好与成本闭环，不是单点算法神话。', '软硬反复推倒是飞轮副作用也是能力训练。', '下半场看安全可证明下的规模化经济性。'],
    actions: ['跟踪 Robotaxi 城市扩张与远程监管人车比。', '对照 Waymo 运营数据与特斯拉干预率口径。', '把 HW5/AI5 装车声明当变量而非定数。'],
    shift: '从「哪条技术路线正确」转向「谁能把无方向盘出行做成可审计的生意」。',
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
fs.writeFileSync(path.join(DIR, '..', '_work/b61/tesla-fsd-height.txt'), String(height));
