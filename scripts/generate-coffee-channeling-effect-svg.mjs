#!/usr/bin/env node
/**
 * b62e：生成 coffee-channeling-effect 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'coffee-channeling-effect-理性分析.svg');

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

const body = `
<div class="container">
  <h1>咖啡萃取之通道效应</h1>
  <div class="meta">
    <span class="tag tag-blue">小红书</span>
    <span class="tag tag-green">2分29秒</span>
    <span class="tag tag-orange">咖啡萃取</span>
    <span class="tag tag-purple">通道效应</span>
    <span class="tag tag-gray">理性分析</span>
  </div>
  <a class="source-link" href="https://xhslink.cn/o/3ncye3zBuDz" target="_blank" rel="noopener">原视频链接</a>
  <div class="summary-line">核心命题：粉量与时间「看起来正常」却又酸又苦时，优先怀疑粉饼通道（水走捷径），而不是立刻拧研磨度。先把布粉/压粉做匀，再微调研磨找味道。</div>

  <div class="timeline">
    <h3>关键证据时间轴</h3>
    <div class="timeline-item"><div class="timeline-time">00:01</div><div class="timeline-text">做咖啡犒劳自己 → 试饮酸苦涩全占齐</div></div>
    <div class="timeline-item"><div class="timeline-time">00:12</div><div class="timeline-text">误判过萃：调粗研磨 → 水流飞快，味道仍不稳</div></div>
    <div class="timeline-item"><div class="timeline-time">00:39</div><div class="timeline-text">粉饼多孔洞：时间/克重在范围内，盲区在水怎么走</div></div>
    <div class="timeline-item"><div class="timeline-time">00:45</div><div class="timeline-text">剖面：水沿松软路径钻穿 → 命名通道效应</div></div>
    <div class="timeline-item"><div class="timeline-time">01:39</div><div class="timeline-text">细布粉针打散结团；水平垂直压粉</div></div>
    <div class="timeline-item"><div class="timeline-time">02:10</div><div class="timeline-text">先改步骤再微调研磨；先萃匀再调味</div></div>
  </div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">
      <div class="node">难喝症状<br/>酸苦涩并存</div>
      <div class="arrow">→</div>
      <div class="node node-orange">误归因<br/>只拧研磨</div>
      <div class="arrow">→</div>
      <div class="node node-purple">证据<br/>粉饼孔/剖面</div>
      <div class="arrow">→</div>
      <div class="node">判断<br/>通道效应</div>
      <div class="arrow">→</div>
      <div class="node node-green">行动<br/>先萃匀再调味</div>
    </div>
  </div>

  <div class="correction">
    <h3>常见误解与认知纠偏</h3>
    <p>误解：难喝 = 磨太细过萃，拧粗就完事。纠偏：调粗可能只让水流变快，酸/淡/涩仍在；根因常是粉床密度不均导致通道。</p>
    <p>误解：时间、克重在参考范围 = 萃取没问题。纠偏：整杯均值正常，仍可能局部过萃与欠萃混在同一杯。</p>
    <p>误解：表面压平就等于布粉均匀。纠偏：作者明确指出「表面平了可不代表里面也分匀了」。</p>
    <p>立场分层：粉饼孔洞与剖面示意为可核验画面证据；「先萃匀再调味」为作者教学策略，非实验室唯一标准。</p>
  </div>

  <h2 class="sec-title">观点卡片</h2>

  <div class="card">
    <h3>在讲什么：通道 = 水走捷径</h3>
    <p>关键理解：高压下水优先从松软缝隙穿过粉饼，通道处过度萃取，未充分过水处萃取不足，最终混进同一杯，口感常表现为酸、苦、涩交织。</p>
    <div class="quote">「逮着几个好走的地方就一路钻过去了」——画面字幕</div>
    <div class="relation">关系：粉床密度差 → 优先路径 → 局部过萃+欠萃 → 整杯难喝</div>
    <div class="action">用法：难喝且参数看似正常时，先查粉饼孔洞与布粉过程，再决定是否动研磨。</div>
  </div>

  <div class="card card-purple">
    <h3>UP 主观点：先改步骤，别只会拧刻度</h3>
    <p>作者主张发现哪一步没做好就先改哪一步，再微调研磨；并提醒别把所有问题都怪在压粉上。</p>
    <div class="quote">「先萃匀，再调味，总比心疼着豆子还在来回拧刻度强。」</div>
    <div class="action">用法：建立排错顺序——布粉/压粉/结团处理 → 观察液流与粉饼 → 最后微调研磨找风味。</div>
  </div>

  <div class="card card-orange">
    <h3>风险与避坑</h3>
    <div class="pitfall">只盯整杯秒数与出液克重，不看水在粉里怎么走。</div>
    <div class="pitfall">粉堆偏、结团未打散，却指望一次压平解决一切。</div>
    <div class="pitfall">难喝就来回拧研磨度，浪费豆子且掩盖通道问题。</div>
  </div>

  <div class="card card-green">
    <h3>横向对比：排错路径</h3>
    <table>
      <thead><tr><th>路径</th><th>假设</th><th>常见结果</th><th>适用边界</th></tr></thead>
      <tbody>
        <tr><td>只调粗研磨</td><td>过萃</td><td>水流变快，酸/淡/涩仍在</td><td>粉床已均匀但仍偏苦/偏长时再考虑</td></tr>
        <tr><td>查通道+布粉压粉</td><td>粉床不均</td><td>孔洞减少、液流更稳</td><td>参数在范围却难喝；粉饼有孔</td></tr>
        <tr><td>先萃匀再调味</td><td>均匀优先于风味微调</td><td>减少无效拧刻度</td><td>作者策略；具体刻度需自家验证</td></tr>
      </tbody>
    </table>
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <ul>
      <li>通道效应：水走粉饼捷径，一杯里同时欠萃与过萃。</li>
      <li>时间/克重正常不能排除通道问题。</li>
      <li>表面压平不等于内部均匀；结团要用布粉针处理。</li>
    </ul>
    <h3>行动清单</h3>
    <ol>
      <li>难喝时先看用过粉饼是否有孔洞、液流是否单边喷射。</li>
      <li>接粉后检查结团，用细布粉针轻轻打散。</li>
      <li>分匀后手柄放稳，压粉器水平、垂直下压。</li>
      <li>确认粉床均匀后，再微调研磨找喜欢的味道。</li>
      <li>不要把所有问题都归因于压粉或研磨中的单一环节。</li>
    </ol>
    <h3>关键认知转变</h3>
    <ul>
      <li>以前：难喝 → 立刻拧研磨度。</li>
      <li>现在：难喝 → 先问水是否在粉饼里走捷径。</li>
      <li>以前：整杯参数在范围内就安心。</li>
      <li>现在：还要看粉床均匀度与粉饼痕迹。</li>
    </ul>
  </div>

  <div class="footer">证据来源：画面烧录字幕 + 粉饼/剖面演示 + 笔记文案 · ASR 残缺已标注 · 甄茶笔记&amp;大喜</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.writeFileSync(path.join(DIR, '..', '_work', 'b62e-svg-height.txt'), String(height), 'utf8');
