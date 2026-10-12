#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'future-three-valuable-jobs-理性分析.svg');
const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}.container{max-width:1200px;margin:0 auto}h1{font-size:30px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}h2{font-size:22px;font-weight:700;color:#1e40af;margin:24px 0 12px;padding-bottom:6px;border-bottom:2px solid #e2e8f0}h3{font-size:17px;font-weight:700;color:#334155;margin-bottom:8px}p,li{font-size:14px;line-height:1.7;color:#475569;margin-bottom:5px}ul,ol{padding-left:20px}.tag{display:inline-block;padding:3px 10px;border-radius:16px;font-size:12px;font-weight:600;margin-right:6px}.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}.meta{margin:8px 0 14px}.summary-line{font-size:16px;line-height:1.65;padding:16px 20px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:16px;color:#334155;box-shadow:0 2px 12px rgba(0,0,0,.04)}.timeline{background:#fff;border-radius:14px;padding:18px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,.04)}.timeline h3{color:#1e40af}.timeline-item{display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #f1f5f9}.timeline-time{font-size:12px;font-weight:700;color:#3b82f6;min-width:58px}.timeline-text{font-size:13px;color:#475569}.map{background:#fff;border-radius:16px;padding:24px;margin-bottom:16px;box-shadow:0 4px 20px rgba(0,0,0,.05)}.map h2{margin:0;border:none;padding:0}.diagram{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;align-items:center;padding:12px 0}.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:12px;padding:14px 18px;text-align:center;min-width:120px;font-weight:700;font-size:13px;color:#1e40af}.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}.arrow{font-size:20px;color:#94a3b8}.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:14px 18px;border-radius:10px;margin-bottom:14px}.correction h3,.correction p{color:#92400e}.sec-title{font-size:18px;font-weight:700;color:#1e40af;margin:6px 0 10px;padding-left:10px;border-left:4px solid #3b82f6}.card{background:#fff;border-radius:12px;padding:18px;margin-bottom:10px;border-left:5px solid #3b82f6;box-shadow:0 3px 16px rgba(0,0,0,.04)}.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}.card h3{font-size:16px;color:#1e40af}.card .quote{background:#f8fafc;padding:8px 12px;border-radius:8px;margin:8px 0;font-size:12px;color:#64748b;border-left:3px solid #cbd5e1;font-style:italic}.card .relation{background:#f0fdf4;padding:8px 10px;border-radius:8px;font-size:12px;color:#166534}.card .pitfall{background:#fef2f2;padding:8px 12px;border-radius:8px;margin:6px 0;font-size:12px;color:#991b1b;border-left:3px solid #ef4444}table{width:100%;border-collapse:collapse;font-size:13px}th{background:#f1f5f9;padding:8px;text-align:left;color:#1e40af}td{padding:8px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:16px;padding:24px;margin-top:18px}.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}.conclusion h3{color:rgba(255,255,255,.9);margin:10px 0 6px}.conclusion p,.conclusion li{color:rgba(255,255,255,.9)}.footer{text-align:center;color:#94a3b8;font-size:12px;padding:18px 0}.source-link{color:#3b82f6;font-size:13px;text-decoration:none;display:inline-block;margin-bottom:12px}.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;
const esc = (s) => String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const d = {
  title: '未来最值钱的三种工作｜硅谷创业者小鹰',
  duration: '12分35秒', url: 'https://b23.tv/P9SiN92',
  tags: ['AI创业','Founder','销售','通才','Agent'],
  perspective: '理性分析 · 职场与创业',
  summary: '核心判断：工作总量未必下降，但「老登组织里的螺丝钉岗」在漏；值钱的是定义问题与管 AI 的通才，近未来显性三类是 Founder、销售、以及 AI 暂做不好的过渡劳动。',
  timeline: [['00:40','一人公司与融资标签'],['02:00','风口+收入+圈子'],['04:30','管AI：错题本与对骂'],['06:00','打工机会变少'],['08:00','螺丝钉→通才'],['10:20','Founder/销售/苦工'],['11:40','传记与测产品']],
  map: [['问题','AI时代做什么'],['证据','管AI+组织漏岗'],['判断','通才>螺丝钉'],['行动','换圈+练定义']],
  corrections: ['误解：AI让工作消失。纠偏：工作更多，老登打工岗更少。','误解：必须立刻创业才安全。纠偏：通才与结果导向在打工市场也稀缺。','ASR：老登/斯坦福/一人公司/铁饭碗等已校正。'],
  cards: [
    {title:'在讲什么：人适应AI，不是反过来',body:'人是有肉体瓶颈的调度者；目标是让Agent干得久且靠谱。',quote:'工作肯定会越来越多了，只是给老登公司打工的机会越来越少',relation:'叙事从失业恐惧切到岗位结构重组。',tone:'card-purple'},
    {title:'管AI四件套',body:'权限一次给对、方向纠偏、AI质检AI、错题本长记性。',quote:'这就是管AI的难点',relation:'可写成个人工作流清单。',tone:'card-blue'},
    {title:'三种工作',body:'Founder；销售（人格魅力）；过渡苦工/精细体力。',quote:'一类是Founder……一类就是销售……还有一类可能就是纯的苦工',relation:'5–10年可见，非50年预言。',tone:'card-green'},
    {title:'边界：硅谷口语经验',body:'个人创业叙事与圈层偏见；「没成功创业者>大厂」是招聘偏好不是普遍真理。',quote:'一个没成功的创业者高于一个给大公司打工的',relation:'作启发式，勿当绝对阶层论。',tone:'card-orange'},
  ],
  table: {title:'三类工作对照',head:['类型','为何值钱','风险'],rows:[['Founder','定义游戏、整合资源','失败率高'],['销售','技术同质后比人格与获客','被平台规则挤压'],['过渡劳动','AI手笨/平台禁自动化','随能力进步消失']]},
  boundary: ['访谈观点非劳动经济学结论。','「老登」为口语贬称，指僵化旧组织。'],
  pitfalls: ['只焦虑裁员不换信息圈。','用开会写文档当核心产出。','把奥数/螺丝钉当唯一安全路径。'],
  conclusion: {key:['岗在重组，不是工作归零。','通才=定义问题+管AI。','Founder与销售是近端硬通货。'],actions:['本周测3个新AI产品并记手感。','找1个AI圈朋友每周同步机会。','把自己产出改成「问题定义+验收标准」。'],shift:'从「保住旧岗」转向「进入新工作方式」。'}
};
function body(data){
  const tags=data.tags.map((t,i)=>`<span class="tag ${['tag-blue','tag-green','tag-orange','tag-purple','tag-red'][i%5]}">${esc(t)}</span>`).join('');
  const timeline=data.timeline.map(([t,x])=>`<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`).join('');
  const map=data.map.map(([a,b],i)=>{const cls=['node','node-green','node-orange','node'][i%4];const ar=i<data.map.length-1?'<span class="arrow">→</span>':'';return `<div class="${cls}">${esc(a)}<br/>${esc(b)}</div>${ar}`;}).join('');
  const corr=data.corrections.map(c=>`<p>${esc(c)}</p>`).join('');
  const cards=data.cards.map(c=>`<div class="card ${c.tone}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p><div class="quote">${esc(c.quote)}</div><div class="relation">${esc(c.relation)}</div></div>`).join('');
  const thead=`<tr>${data.table.head.map(h=>`<th>${esc(h)}</th>`).join('')}</tr>`;
  const tbody=data.table.rows.map(r=>`<tr>${r.map(c=>`<td>${esc(c)}</td>`).join('')}</tr>`).join('');
  const bound=data.boundary.map(b=>`<li>${esc(b)}</li>`).join('');
  const pits=data.pitfalls.map(p=>`<div class="pitfall">${esc(p)}</div>`).join('');
  const key=data.conclusion.key.map(k=>`<li>${esc(k)}</li>`).join('');
  const act=data.conclusion.actions.map(a=>`<li>${esc(a)}</li>`).join('');
  return `<div class="container root-wrap"><h1>${esc(data.title)}</h1><div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(data.duration)}</span><span class="tag tag-gray">${esc(data.perspective)}</span></div><a class="source-link" href="${esc(data.url)}">原视频</a><div class="summary-line">${esc(data.summary)}</div><div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div><div class="map"><h2>核心脉络</h2><div class="diagram">${map}</div></div><div class="correction"><h3>常见误解与认知纠偏</h3>${corr}</div><div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div><div class="section"><h2 class="sec-title">${esc(data.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div><div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${bound}</ul>${pits}</div></div><div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${key}</ul><h3>行动清单</h3><ol>${act}</ol><h3>关键认知转变</h3><p>${esc(data.conclusion.shift)}</p></div><div class="footer">双轨产物之二 · 理性分析 · ${esc(data.duration)}</div></div>`;
}
const {svg,height}=await buildSvg({css:CSS,body:body(d),width:1320});
fs.writeFileSync(OUT,svg,'utf8');
console.log('Generated',OUT,height);
fs.writeFileSync(path.join(DIR,'..','_work/b61/future-height.txt'),String(height));
