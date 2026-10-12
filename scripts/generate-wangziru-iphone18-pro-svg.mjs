#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';
const DIR=path.dirname(fileURLToPath(import.meta.url));
const OUT=path.join(DIR,'..','docs','wangziru-iphone18-pro-理性分析.svg');
const CSS=`*{margin:0;padding:0;box-sizing:border-box}body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}.container{max-width:1200px;margin:0 auto}h1{font-size:28px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}h2{font-size:22px;font-weight:700;color:#1e40af;margin:22px 0 12px;padding-bottom:6px;border-bottom:2px solid #e2e8f0}h3{font-size:16px;font-weight:700;color:#334155;margin-bottom:8px}p,li{font-size:14px;line-height:1.7;color:#475569;margin-bottom:5px}ul,ol{padding-left:20px}.tag{display:inline-block;padding:3px 10px;border-radius:16px;font-size:12px;font-weight:600;margin-right:6px}.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}.meta{margin:8px 0 12px}.summary-line{font-size:16px;line-height:1.65;padding:16px 18px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:14px;color:#334155;box-shadow:0 2px 12px rgba(0,0,0,.04)}.timeline{background:#fff;border-radius:14px;padding:16px;margin-bottom:14px;box-shadow:0 2px 12px rgba(0,0,0,.04)}.timeline-item{display:flex;gap:10px;padding:5px 0;border-bottom:1px solid #f1f5f9}.timeline-time{font-size:12px;font-weight:700;color:#3b82f6;min-width:58px}.timeline-text{font-size:13px;color:#475569}.map{background:#fff;border-radius:16px;padding:22px;margin-bottom:14px;box-shadow:0 4px 20px rgba(0,0,0,.05)}.map h2{margin:0;border:none;padding:0}.diagram{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;padding:12px 0}.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:12px;padding:12px 16px;text-align:center;min-width:118px;font-weight:700;font-size:13px;color:#1e40af}.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}.arrow{font-size:20px;color:#94a3b8}.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:14px 16px;border-radius:10px;margin-bottom:12px}.correction h3,.correction p{color:#92400e}.sec-title{font-size:18px;font-weight:700;color:#1e40af;margin:6px 0 10px;padding-left:10px;border-left:4px solid #3b82f6}.card{background:#fff;border-radius:12px;padding:16px;margin-bottom:10px;border-left:5px solid #3b82f6;box-shadow:0 3px 16px rgba(0,0,0,.04)}.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}.card h3{font-size:15px;color:#1e40af}.card .quote{background:#f8fafc;padding:8px 10px;border-radius:8px;margin:6px 0;font-size:12px;color:#64748b;border-left:3px solid #cbd5e1;font-style:italic}.card .relation{background:#f0fdf4;padding:8px 10px;border-radius:8px;font-size:12px;color:#166534}.card .pitfall{background:#fef2f2;padding:8px 10px;border-radius:8px;margin:6px 0;font-size:12px;color:#991b1b;border-left:3px solid #ef4444}table{width:100%;border-collapse:collapse;font-size:12px}th{background:#f1f5f9;padding:8px;text-align:left;color:#1e40af}td{padding:8px;border-bottom:1px solid #e2e8f0;vertical-align:top;color:#475569}.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:16px;padding:22px;margin-top:16px}.conclusion h2{color:#fff;border-bottom:1px solid rgba(255,255,255,.2);margin-top:0}.conclusion h3{color:rgba(255,255,255,.9);margin:10px 0 6px}.conclusion p,.conclusion li{color:rgba(255,255,255,.9)}.footer{text-align:center;color:#94a3b8;font-size:12px;padding:16px 0}.source-link{color:#3b82f6;font-size:13px;text-decoration:none;display:inline-block;margin-bottom:10px}.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const d={
 title:'王自如｜iPhone18 Pro 与苹果商业逻辑',
 duration:'19分28秒',url:'https://b23.tv/ncSlkm6',
 tags:['iPhone','苹果','商业策略','换机','Duo'],
 perspective:'理性分析 · 消费电子',
 summary:'核心判断：今年 Pro 是小年机，换机动力弱；真正值得读的是苹果用排期、涨价克制与折叠布局做的商业驱动——把产品推到消费者买/不买阈值「刚好触达」。',
 timeline:[['00:20','小年+别换'],['02:30','铝合金ID逻辑'],['05:00','内存服务AI'],['07:40','三轴评价模型'],['09:00','两波换机曲线'],['14:00','克制涨价'],['16:00','Duo指向中国'],['18:20','2TB银色建议']],
 map:[['问题','该不该换Pro'],['证据','小年+商业排期'],['判断','别为社交货币溢价'],['行动','多数观望']],
 corrections:['误解：每年Pro都值得升级。纠偏：小年缺社交与体验双重增益。','误解：参数提升=换机理由。纠偏：国行AI用不上则内存带宽溢价虚。','内容含对尚未全面铺开机型的商业推演，作视角笔记而非购买保证。'],
 cards:[
  {title:'产品：三轴占不满',body:'高感知/高频/高价值；可变光圈偏发布会感知，AI内存国行难高频。',quote:'能够将这三个维度都占满的其实几乎没有',relation:'用三轴过滤发布会话术。',tone:'card-purple'},
  {title:'商业：两波曲线',body:'标准版+Air上半年，Pro+Duo下半年；减少决策混淆，捕捉摇摆人群。',quote:'摇摆人群决定商业走向',relation:'排期即产品策略。',tone:'card-blue'},
  {title:'涨价：克制吃红利',body:'约100–150美金；供应链锁定 vs 安卓行情价；留竞争与未来缓冲。',quote:'依旧选择了将这一波涨价红利吃到嘴里，但是它吃的幅度非常克制',relation:'品牌溢价+成本结构综合竞争。',tone:'card-green'},
  {title:'怎么买',body:'默认不换；非买不可→大容量银色Max；社交货币看Duo。',quote:'我也不建议大家换今年的Pro系列',relation:'经济环境纳入决策。',tone:'card-orange'},
 ],
 table:{title:'换机理由检查',head:['理由','今年是否成立'],rows:[['ID新鲜感','弱（延续）'],['续航/性能跃迁','有限增量'],['AI体验','国行常用不上'],['社交货币','更多在Duo'],['价格','涨且溢价问号']]},
 boundary:['个人商业解读，非财报级证据。','机型命名与排期含产业链传闻成分。'],
 pitfalls:['为颜色话题换机。','把发布会高感知功能当日常高频价值。','忽略总持有成本与旧机残值。'],
 conclusion:{key:['小年默认不换。','读懂排期比读懂跑分重要。','阈值触达是苹果手艺。'],actions:['用三轴给自己场景打分。','若旧机够用，跳过本轮Pro。','关注Duo与上半年标准版/Air节奏。'],shift:'从「新品是否更强」转向「苹果是否在用节奏收割摇摆人群」。'}
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
fs.writeFileSync(path.join(DIR,'..','_work/b61/wangziru18-height.txt'),String(height));
