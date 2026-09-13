#!/usr/bin/env node
/** 达芬奇调色师操作动线 · 讨论整理 · 理性分析 SVG */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../../svg-auto-height.mjs';
import fs from 'node:fs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const SLUG = 'davinci-colorist-workflow';
const OUT = path.join(DIR, '..', '..', 'docs', `${SLUG}-理性分析.svg`);

const d = {
  title: '达芬奇调色师操作动线',
  tags: ['个人专栏', '达芬奇', '调色', '节点', '白平衡', '二级调色'],
  duration: '讨论整理',
  perspective: '理性分析',
  url: `personal:${SLUG}`,
  summary:
    '把 Color 页面板按专业动线重排：工作台 → 节点 → 清理 → LUT 前立轴 → 影调 → 二级分区 → 质感 → 动态 → 交付。核心不是会拧每个旋钮，而是知道当前在流水线的哪一站。',
  timeline: [
    ['01 工作台', '时间线·节点·示波器就位；光箱留给整场统一'],
    ['02 节点', '一事一节点；串行打底、并行纠偏'],
    ['03 清理', '降噪/修复 FX/输入大小，脏信号不进校色'],
    ['04 立轴', '色彩匹配或 Offset/色温；必须在技术 LUT 前'],
    ['05 影调', 'HDR 分区塑光；曲线精确映射与哑光'],
    ['06 二级', '限定器·窗口·跟踪·键·切片·扭曲'],
    ['07 质感', 'RGB 混合器防滤镜感；模糊控清晰度'],
    ['08 动态', '关键帧做光比/Look 渐变；遮罩跟人用跟踪'],
    ['09 交付', '光箱对白 → 示波器验收 → 快捷导出验证'],
  ],
  map: [
    ['清理信号', 'NR / 修复 / 构图'],
    ['一级立轴', 'WB · 曝光 · LUT'],
    ['影调二级', 'HDR · 蒙版 · 切片'],
    ['质感交付', '混合器 · 光箱'],
  ],
  corrections: [
    '不是从左到右点一遍图标；面板按「工位」挂到动线上才有意义。',
    '白平衡主战场在技术 LUT 之前（Log 域 Offset）；LUT 后再拧全局色温是打补丁。',
    'HDR 校色轮不是「只给 HDR 成片用」，而是按亮度带分区塑光的一级增强工具。',
    '键面板不画选区，只修蒙版力度与软硬；Look 浓度常用键输出增益控制。',
    'FCP 要严格 LUT 前后分工须用 Custom LUT 堆栈，Camera LUT 会钉死在最前。',
  ],
  cards: [
    {
      tone: '',
      title: '动线优先于面板词典',
      body: '专业习惯是先问「我现在在清理、立轴、影调还是二级」。同一色轮在 LUT 前做白平衡、在 LUT 后做口味，工具身份不变、工位变了。示波器（Parade/Waveform）是裁判。',
      quote: '面板都会用，不如每次只问：我在动线的哪一站？',
      relation: '机制：先干净坐标系，再谈好看。',
    },
    {
      tone: 'card-orange',
      title: '节点 = 可开关的流水线',
      body: '串行承载线性职责（还原→变换→风格）；并行从同源分流保护肤色/局部暖色，避免串行污染。绿口传 RGB，蓝口传键；一事一节点便于粘贴同场与 Bypass 对比。',
      quote: '顺序即工位',
      relation: '对照：FCP 用效果堆栈模拟同一逻辑，上限在并行与键传递。',
    },
    {
      tone: 'card-green',
      title: '立轴：色卡或 Offset，且在变换前',
      body: '有 ColorChecker 用色彩匹配自动立中性与黑白位；无色卡用吸管/色温/Offset，Parade 三列对齐。技术 LUT/CST 放在立轴之后；之后节点只做饱和补偿与风格。',
      quote: '白平衡动轴，饱和动距',
      relation: '避坑：LUT 钉在首节点再校白 → 显示域分段打补丁。',
    },
    {
      tone: 'card-purple',
      title: '二级选型：色 / 形 / 动 / 力度',
      body: '同色物体→HSL 限定器；光区暗角→窗口（+跟踪）；整类色相收艳→切片器；某团颜色要挪→色度扭曲；软边与 Look 浓度→键面板。',
      quote: '先选对蒙版类型，再拧色轮',
      relation: '性价比：大窗口+柔化优先于像素级钢笔。',
    },
    {
      tone: 'card-red',
      title: '质感与交付收束',
      body: 'RGB 混合器改通道关系防一键滤镜感；模糊/锐化配窗口做局部清晰度。关键帧管参数随时间变；遮罩跟人优先跟踪。最后光箱统一、示波器验收、快捷导出在真环境复看。',
      quote: '界面色 ≠ 成片色',
      relation: '行动：锚点镜定 Look，同场粘贴节点再微调。',
    },
  ],
  boundary: [
    '本文覆盖 Color 页常用面板导览级理解，不是 Fusion/交付页完整手册。',
    'ACES/RCM 标签细节、监视器校准流程未展开。',
    '重度降噪与物体移除依赖机器性能；预览可关、导出再开。',
    '混合色温场景全局白平衡无解，必须窗口/限定器分区。',
  ],
  pitfalls: [
    '每个面板都拧一点，没有节点职责与 Bypass 对比。',
    '技术 LUT 在前、白平衡在后，高光色偏修不齐。',
    '一级轮硬拧亮暖暗冷当风格，像错白平衡滤镜。',
    '提亮暗部不保黑位，画面发灰。',
    'Look/LUT 浓度拉满且不用键输出降浓度，全局易脏。',
  ],
  conclusion: {
    key: [
      '九段动线：工作台 → 节点 → 清理 → 立轴 → 影调 → 二级 → 质感 → 动态 → 交付',
      '三条铁律：LUT 前立轴；串行打底并行纠偏；示波器裁决',
      '二级先选型（色/形/动/力度），再调颜色',
    ],
    actions: [
      '建串行模板节点：NR → WB/曝光 → 技术 LUT → HDR/曲线 → 二级 → Look',
      '一级节点强制开 RGB Parade；交付前开光箱对白',
      '二级优先窗口+柔化；跟人加跟踪；Look 用键输出控浓度',
      '预览卡时关时域降噪，导出再开',
      '每镜结束问：此刻 Bypass 掉风格节点，校正是否仍成立？',
    ],
    shift:
      '以前：把达芬奇当成滤镜面板词典从左点到右；现在：按调色师流水线给每个面板分配工位，先立轴再染色，用示波器和 Bypass 结案。',
  },
};

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#a4622d,#356e68);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#7c4920;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #a4622d;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#7c4920;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#a4622d;min-width:110px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#fbf6ec,#f6e9db);border:2px solid #e0c6a8;border-radius:16px;padding:20px 28px;text-align:center;min-width:140px;font-weight:700;font-size:16px;color:#7c4920}
.node-green{background:linear-gradient(135deg,#edf2ee,#d1e7e0);border-color:#9fc0b8;color:#26524d}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#7c4920;margin-bottom:16px;padding-left:16px;border-left:4px solid #a4622d}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #a4622d}
.card.card-green{border-left-color:#356e68}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#7c4920;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#edf2ee;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#26524d}
.conclusion{background:linear-gradient(135deg,#7c4920,#356e68);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#a4622d;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function buildBody(d) {
  const tags = (d.tags || [])
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`)
    .join('');
  const timeline = (d.timeline || [])
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const mapNodes = (d.map || [])
    .map(([label], i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node'][i % 4];
      const arrow = i < d.map.length - 1 ? '<span class="arrow">→</span>' : '';
      return `<div class="${cls}">${esc(label)}</div>${arrow}`;
    })
    .join('');
  const corrections = (d.corrections || []).map((c) => `<p>· ${esc(c)}</p>`).join('');
  const cards = (d.cards || [])
    .map((c) => {
      const tone = c.tone ? ` card ${c.tone}` : ' card';
      return `<div class="${tone.trim()}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p><div class="quote">${esc(c.quote)}</div><div class="relation">${esc(c.relation)}</div></div>`;
    })
    .join('');
  const boundary = (d.boundary || []).map((b) => `<li>${esc(b)}</li>`).join('');
  const pitfalls = (d.pitfalls || []).map((p) => `<li>${esc(p)}</li>`).join('');
  const keyHtml = (d.conclusion?.key || []).map((k) => `<li>${esc(k)}</li>`).join('');
  const actionsHtml = (d.conclusion?.actions || []).map((a) => `<li>${esc(a)}</li>`).join('');
  const shift = d.conclusion?.shift || '';

  return `<div class="container root-wrap">
  <h1>${esc(d.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">${esc(d.duration)}</span><span class="tag tag-gray">${esc(d.perspective)}</span></div>
  <a class="source-link" href="${esc(SLUG)}-图文实录.html">← 图文实录</a>
  <div class="summary-line">${esc(d.summary)}</div>
  <div class="timeline"><h3>结构时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>
  <div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul><h3>避坑</h3><ul>${pitfalls}</ul></div></div>
  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${keyHtml}</ul><h3>行动清单</h3><ol>${actionsHtml}</ol><h3>关键认知转变</h3><p>${esc(shift)}</p></div>
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自讨论整理全文</div>
</div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: buildBody(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated', OUT, 'height', height);

const indexPath = path.join(DIR, '..', '..', 'docs', 'index.json');
const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const url = `personal:${SLUG}`;
let entry = index.find((e) => e.url === url);
const today = new Date().toISOString().slice(0, 10);
const payload = {
  date: today,
  title: '达芬奇调色师操作动线',
  summary:
    '九段动线重排 Color 页：工作台→节点→清理→LUT前立轴→影调→二级分区→质感→动态→交付；含面板截图与达芬奇/FCP 工位对照。',
  tags: ['个人专栏', '达芬奇', '调色', '节点', '白平衡', '二级调色', 'HDR', 'LUT'],
  platform: 'personal',
  url,
  duration: '讨论整理',
  outputs: {
    html: `${SLUG}-图文实录.html`,
    svg: `${SLUG}-理性分析.svg`,
  },
  screenshot_count: 18,
  transcript_segments: 9,
  svg_height: height,
  slug: SLUG,
};
if (!entry) {
  index.push(payload);
} else {
  Object.assign(entry, payload);
}
fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');
console.log('index updated', url, 'svg_height', height);
