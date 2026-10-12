#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'top10-british-drama-21c-理性分析.svg');
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
  title: '21世纪十大英剧｜爆剧不少，但你至少漏了一半',
  duration: '36分42秒',
  url: 'https://b23.tv/Bov7aJG',
  tags: ['英剧', '片单', 'Fleabag', '慢马', '黑镜'],
  perspective: '理性分析 · 影视审美',
  summary: '核心判断：英剧「贵」在短季、删水与拒绝廉价大团圆——榜单价值不是追热，而是用类型覆盖校准审美：智性犯罪、时代告别、少数派喜剧、后真相监控、打破第四堵墙、伤痕黑帮、倒霉间谍、单元诡计、评分暴政、乡间善意。',
  timeline: [
    ['00:20', '短纯不注水'],
    ['02:00', '夏洛克思维宫殿'],
    ['05:00', '唐顿体面告别'],
    ['08:00', 'IT狂人少数派'],
    ['11:00', '真相捕捉改写监控'],
    ['15:30', 'Fleabag告解'],
    ['20:00', '浴血黑帮伤痕'],
    ['24:00', '慢马倒霉特工'],
    ['27:00', '九号秘事不信表象'],
    ['34:00', '万物生灵善意'],
  ],
  map: [
    ['问题', '英剧鄙视链为何高'],
    ['证据', '十部类型覆盖'],
    ['判断', '养刁廉价反转胃口'],
    ['行动', '补漏喜剧/单元/间谍'],
  ],
  corrections: [
    '误解：榜单=热度排名。纠偏：口播强调审美与漏看冷门类型。',
    '误解：英剧全是严肃正剧。纠偏：IT狂人、九号秘事、Fleabag 占喜剧/元叙事半壁。',
    '误解：看完大热即「懂英剧」。纠偏：后真相监控与评分社会篇章才触及当代焦虑。',
  ],
  cards: [
    { title: '审美引擎：短季删水', body: '三五集一季逼编剧砍水；主角千疮百孔，黑屏留给怀疑而非鸡汤。', quote: '养刁审美后会对「快节奏反转」产生错觉', relation: '先问「是否注水」再问「好不好看」。', tone: 'card-purple' },
    { title: '双峰：智性 vs 体面', body: '夏洛克=思维宫殿与情谊软肋；唐顿=考据偏执与旧世界告别。', quote: '体面是盔甲', relation: '两类「高级感」来源不同：脑内戏 vs 礼仪崩解。', tone: 'card-blue' },
    { title: '当代：监控与羞耻', body: '真相捕捉=证据可被重写；Fleabag=第四堵墙告解「错了」的恐惧。', quote: '对抗握笔改史的傲慢', relation: '后真相日常化后，信任机制成为剧核。', tone: 'card-green' },
    { title: '漏看区：间谍/单元/乡间', body: '慢马=尽职不被承认；九号=永不信表象；万物生灵=平凡善意收束。', quote: '伟大藏在日常微不足道的坚持里', relation: '漏一半常漏在非热搜类型。', tone: 'card-orange' },
  ],
  table: {
    title: '十部类型对照（口播片单）',
    head: ['作品', '类型锚点', '抓什么'],
    rows: [
      ['神探夏洛克', '智性犯罪', '软肋与思维可视化'],
      ['唐顿庄园', '时代剧', '体面与告别'],
      ['IT狂人', '职场荒诞喜剧', '少数派氛围笑'],
      ['真相捕捉', '后真相惊悚', '可改写的监控'],
      ['Fleabag', '元叙事喜剧', '羞耻与告解'],
      ['浴血黑帮', '黑帮史诗', '一战一代伤痕'],
      ['慢马', '间谍黑色喜剧', '倒霉与资格'],
      ['九号秘事', '单元诡计', '别信表象'],
      ['分数社会（黑镜式）', '科幻寓言', '评分暴政'],
      ['万物生灵', '乡间传记', '平凡善意'],
    ],
  },
  boundary: ['主观片单非客观「十大」权威榜。', '含剧透级场景描述，追新勿先读图注细节。', '部分片名口播与常见译名可能略有出入，以类型锚点为准。'],
  pitfalls: ['只追 Netflix 热搜漏掉 BBC 单元/喜剧。', '把「英式高级」等同于慢节奏考据剧。', '收藏片单从不按类型补漏。'],
  conclusion: {
    key: ['英剧训练的是对注水与廉价反转的免疫。', '类型覆盖>单部爆款。', '漏一半往往漏在喜剧、单元与间谍冷门。'],
    actions: ['从十部里勾出未看类型各补一部。', '看完一季用一句话写「它删了什么水」。', '把真相捕捉/Fleabag 当当代焦虑样本对照短视频时代。'],
    shift: '从「追英剧热度」转向「用片单校准自己嫌弃什么」。',
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
fs.writeFileSync(path.join(DIR, '..', '_work/b61/top10-british-height.txt'), String(height));
