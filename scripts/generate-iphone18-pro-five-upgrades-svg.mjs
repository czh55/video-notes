#!/usr/bin/env node
/**
 * b62b：生成 iphone18-pro-five-upgrades 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'iphone18-pro-five-upgrades-理性分析.svg');

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
  title: '为了这5个升级，还是换了iPhone 18 Pro',
  duration: '3分59秒',
  url: 'https://xhslink.cn/o/6GrB9slekhu',
  tags: ['iPhone18Pro', '原相机', '可变光圈', '演唱会摄影', '电影效果'],
  perspective: '理性分析 · 消费数码影像',
  summary:
    '核心命题：该不该为「影像玩法」换 iPhone 18 Pro，取决于五个可复用能力是否命中你的高频场景——星芒光圈、胶片风格、追踪对焦、电影效果虚化/降噪、慢门手动控制——而不是抽象参数表。作者结论是「用得到就不亏」；证据层级以口播体验+界面演示为主，非实验室评测。',
  timeline: [
    ['00:00', '原相机直出样片定调：影像是今年主线'],
    ['00:21', '星芒：光圈收到 f/4；仅 1×/2×'],
    ['00:56', '调色盘：反差色+胶片+纹理颗粒'],
    ['01:32', '双击追踪：对标 17 Pro Max 失焦痛点'],
    ['02:06', '电影效果：后期虚化 + 环境降噪滑杆'],
    ['02:47', 'Pro 控制：快门/光圈/白平衡 → 慢门拖影'],
    ['03:16', '设置兜底：4K60 / 空间音频 / 高效 / HEIF 48MP'],
  ],
  map: [
    ['问题', '影像升级值不值换机'],
    ['场景过滤', '演唱会/Vlog/慢门'],
    ['五能力', '星芒·胶片·追踪·电影·慢门'],
    ['结论', '命中场景则值得'],
  ],
  corrections: [
    '误解：星芒是滤镜一键特效。纠偏：作者归因于可变光圈收到约 f/4，且长焦焦段会自动取消。',
    '误解：电影效果只等于浅景深虚化。纠偏：片中同时强调声音侧降噪滑杆，服务后置 Vlog 拾音。',
    '误解：慢门=自动王家卫滤镜。纠偏：需要手动压低快门并配合运镜/转动，属可控参数玩法。',
    '立场分层：界面路径与操作步骤可核验；「不亏」「神图」「大拇哥」属作者体验与价值判断。',
  ],
  cards: [
    {
      title: '在讲什么：可变光圈 → 星芒出片',
      body: '关键理解：把「华丽舞台感」落实为可操作的光圈档位，而不是玄学滤镜。用法：演唱会先在 1×/2× 收到 f/4 抓星芒，再考虑构图与变焦。',
      quote: '这个星芒效果目前是只能在1倍和2倍的焦段下面用',
      relation: '硬件光圈能力 × 焦段限制 = 可预期的现场策略。',
      tone: 'card',
    },
    {
      title: '在讲什么：摄影风格调色盘',
      body: '关键理解：纹理/颗粒/柔肤进入原相机风格，降低「直出就要进后期」的摩擦。用法：舞台优先试「反差色+胶片」，再叠纹理颗粒加强复古。',
      quote: '用原相机呢，就能指出胶片感的照片了',
      relation: '风格预设降低演唱会快速出片成本；「4S 味道」是主观比喻。',
      tone: 'card-purple',
    },
    {
      title: '在讲什么：双击追踪对焦',
      body: '关键理解：把痛点从「画质」换成「能不能稳住主体」。用法：舞台/宠物等运动主体，双击锁定后少手动追焦。',
      quote: '双击屏幕就能追踪，而且跟得非常的稳',
      relation: '相对上一代雨天失焦的对比叙事，证据为单人体验。',
      tone: 'card-green',
    },
    {
      title: '在讲什么：电影效果双通道',
      body: '关键理解：视频虚化可后期调，且声音有独立「电影效果」降噪。用法：路边/嘈杂环境拍口播或 Vlog 时拉开滑杆做人声优先。',
      quote: '越往右拉环境噪音就越小，基本上就只能听到我的声音了',
      relation: '画面景深控制与拾音策略捆绑，服务创作者完整链路。',
      tone: 'card-orange',
    },
    {
      title: '在讲什么：Pro 控制慢门',
      body: '关键理解：原相机暴露快门/光圈/白平衡后，手机也能玩「拖影叙事」。用法：降低快门并转动手机；白天也可拍电影感拖影。',
      quote: '终于可以直接用原生相机，拍出王家卫同款的慢门照片了',
      relation: '从脚架车流光轨的传统玩法，迁移到口袋机即时创作。',
      tone: 'card',
    },
  ],
  table: {
    title: '五个升级：场景匹配与证据强度',
    head: ['升级', '最匹配场景', '可核验操作', '证据强度'],
    rows: [
      ['星芒 f/4', '演唱会舞台灯', '镜头光圈→4；限1×/2×', '界面+样片（中高）'],
      ['调色盘胶片', '舞台/夜景氛围照', '反差色+胶片+纹理颗粒', '界面+前后对比（中）'],
      ['双击追踪', '运动主体/宠物', '双击屏幕锁定', '口播对比（中低）'],
      ['电影效果', '后置 Vlog/口播', '后期虚化+声音滑杆', '分屏+路边演示（中）'],
      ['慢门控制', '车流/拖影创意', '降快门+运镜', '样片+参数宣称（中）'],
    ],
  },
  boundary: [
    '内容为创作者个人换机理由与操作演示，不构成购买保证或官方规格说明书。',
    '未做多机位盲测；与 17 Pro Max 的对比依赖作者雨天演唱会回忆。',
    '机身外观镜头模组在片中有概念化展示，勿将渲染/概念图当作量产外观定论。',
    '「高效 / HEIF 48MP / 4K60」等设置建议需结合你的存储与剪辑工作流取舍。',
  ],
  pitfalls: [
    '以为切到长焦仍能保留星芒——作者明确 4×/8× 会自动取消。',
    '把电影效果降噪当成「任何环境都无损人声」——路边演示有效，极端噪声未验证。',
    '慢门拖影手持不稳或曝光失控，导致糊成一团而非「电影感」。',
    '只为清单式功能换机，但日常几乎不拍演唱会/Vlog/慢门——场景不匹配则溢价难回本。',
  ],
  conclusion: {
    key: [
      '换机问题应改写成：五个影像能力是否覆盖你的高频拍摄。',
      '星芒与胶片风格偏「出片审美」；追踪、电影降噪、慢门偏「过程可控」。',
      '系统设置是放大器：把控制键误触、码率与后期弹性先设对。',
    ],
    actions: [
      '列出你最近 30 天真实拍摄场景，逐条对照五能力打勾。',
      '演唱会：先练 1×/2× + f/4 星芒，再试反差色+胶片预设。',
      '口播/Vlog：到嘈杂路边试电影效果声音滑杆，听人声是否够干净。',
      '创意向：用 Pro 控制压低快门拍一组拖影，确认你愿意为这玩法付溢价。',
      '换机当天按片尾清单检查：关相机调整、4K60、空间音频、高效、HEIF 48MP。',
    ],
    shift: '从「新 iPhone 参数更强吗」转向「这些影像控制是否让我少靠运气、多靠流程出片」。',
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
  <div class="section"><h2 class="sec-title">观点卡片：五能力怎么用</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">${esc(data.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${bound}</ul><h3>避坑</h3>${pits}</div></div>
  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3><ul>${key}</ul>
    <h3>行动清单</h3><ol>${act}</ol>
    <h3>关键认知转变</h3><p>${esc(data.conclusion.shift)}</p>
  </div>
  <div class="footer">双轨产物之二 · 理性分析 · b62b · ${esc(data.duration)}</div>
</div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: body(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
fs.mkdirSync(path.join(DIR, '..', '_work'), { recursive: true });
fs.writeFileSync(path.join(DIR, '..', '_work', 'b62b-svg-height.txt'), String(height));
