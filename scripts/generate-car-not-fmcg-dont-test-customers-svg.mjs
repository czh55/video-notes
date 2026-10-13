#!/usr/bin/env node
/**
 * b62s：生成 car-not-fmcg-dont-test-customers 理性分析 SVG。
 * 必须使用仓库根目录 svg-auto-height.mjs 的 buildSvg。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'car-not-fmcg-dont-test-customers-理性分析.svg');

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
.node-red{background:linear-gradient(135deg,#fef2f2,#fee2e2);border-color:#fca5a5;color:#991b1b}
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
.card .highlight{background:#fef3c7;padding:10px 12px;border-radius:8px;margin:8px 0;font-size:13px;color:#92400e;border-left:3px solid #f59e0b}
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
<div class="container root-wrap">
  <h1>汽车不是快消品！千万不要把客户当小白鼠</h1>
  <div class="meta">
    <span class="tag tag-blue">理性分析</span>
    <span class="tag tag-orange">汽车数码</span>
    <span class="tag tag-gray">11分38秒</span>
    <span class="tag tag-purple">付鹏的财经世界</span>
    <span class="tag tag-red">观点分层</span>
  </div>
  <a class="source-link" href="https://xhslink.cn/o/2Ii0OJvl8V7">原视频（小红书短链）</a>
  <div class="summary-line">核心命题：汽车是关乎生命的耐用交通工具，还是可快速迭代的快消电子品？作者借「脆脆鲨」事件论证——用手机营销逻辑指挥造车，会劣币驱逐良币、把客户当路试小白鼠；抠标撇责与宏大叙事终将反噬信任。</div>

  <div class="timeline">
    <h3>关键证据时间轴</h3>
    <div class="timeline-item"><div class="timeline-time">00:00</div><div class="timeline-text">口号：别把用户当傻子 / 别把吹牛当文化；引出脆脆鲨话题</div></div>
    <div class="timeline-item"><div class="timeline-time">00:25</div><div class="timeline-text">定性：汽车应是耐用品，非快消品；消费电子逻辑指挥造车</div></div>
    <div class="timeline-item"><div class="timeline-time">01:18</div><div class="timeline-text">质别：手机可重启换电池；汽车核心必须是安全</div></div>
    <div class="timeline-item"><div class="timeline-time">01:38</div><div class="timeline-text">批评「百公里几秒、一千匹」式宣传催生马路杀手</div></div>
    <div class="timeline-item"><div class="timeline-time">02:40</div><div class="timeline-text">「速成车」词活起来 = 巨大讽刺</div></div>
    <div class="timeline-item"><div class="timeline-time">03:00</div><div class="timeline-text">纠正「移动的家」：驾驶性/安全性应排第一</div></div>
    <div class="timeline-item"><div class="timeline-time">04:06</div><div class="timeline-text">推测：真上路断裂或发「用户使用不当」声明</div></div>
    <div class="timeline-item"><div class="timeline-time">04:25</div><div class="timeline-text">传统节奏：研发/测试多年 + 极寒湿热高压路试看金属疲劳</div></div>
    <div class="timeline-item"><div class="timeline-time">05:25</div><div class="timeline-text">事故后抠标、蒙布 = 掩耳盗铃</div></div>
    <div class="timeline-item"><div class="timeline-time">06:33</div><div class="timeline-text">消费者被培育成快消品认知：只看屏与舒适</div></div>
    <div class="timeline-item"><div class="timeline-time">07:25</div><div class="timeline-text">估值/融资逼快：磨三年公司可能没了</div></div>
    <div class="timeline-item"><div class="timeline-time">08:01</div><div class="timeline-text">补贴与弯道超车叙事 → 不良竞争；代价落个体生命</div></div>
    <div class="timeline-item"><div class="timeline-time">09:52</div><div class="timeline-text">家国情怀后发现成小白鼠/韭菜</div></div>
    <div class="timeline-item"><div class="timeline-time">11:02</div><div class="timeline-text">收束：勿快消化、勿洗脑、勿营销指挥造车；玩火自焚</div></div>
  </div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">
      <div class="node">品类错位<br/>快消逻辑→汽车</div>
      <div class="arrow">→</div>
      <div class="node node-orange">忽略安全<br/>参数营销优先</div>
      <div class="arrow">→</div>
      <div class="node node-red">劣币驱逐良币<br/>客户当小白鼠</div>
      <div class="arrow">→</div>
      <div class="node node-purple">信任透支<br/>IP 反噬</div>
      <div class="arrow">→</div>
      <div class="node node-green">回归：安全第一<br/>专业造车主导</div>
    </div>
  </div>

  <div class="correction">
    <h3>常见误解纠偏</h3>
    <p>✗「车是移动的家，舒服和屏幕最重要」→ ✓ 作者：首先是交通工具，驾驶性与安全性排第一，舒适是加价可选项。</p>
    <p>✗「加速参数/马力越大越好」→ ✓ 作者：千匹级口号可能把驾驶者推向马路风险；关人命的环节不能当快消卖点。</p>
    <p>✗「充分竞争自然出好物」→ ✓ 作者：若消费者认知已被快消化，现实可变成劣币驱逐良币；长期才可能反转。</p>
  </div>

  <h2 class="sec-title">观点卡片</h2>

  <div class="card">
    <h3>1. 品类：耐用品 vs 快消品</h3>
    <p><strong>在讲什么</strong>：汽车不应按手机/快消节奏宣传与迭代。</p>
    <p><strong>关键理解</strong>：耐用品逻辑要求长周期验证；快消逻辑奖励上新速度与营销话术。</p>
    <p><strong>怎么用</strong>：购车时把「换代速度」当风险信号而非进步证明。</p>
    <div class="quote">「汽车本质上来讲应该是个耐用品……不应该把它宣传或者是做成快消品的这个概念。」[00:25]</div>
    <div class="relation">立场：作者长期观点；画面标题同向强化。</div>
  </div>

  <div class="card card-purple">
    <h3>2. 质别：汽车 ≠ 手机</h3>
    <p><strong>在讲什么</strong>：电子产品故障可重启/换件；汽车故障可能夺命。</p>
    <p><strong>关键理解</strong>：安全是硬约束，不是可后置的「体验项」。</p>
    <p><strong>怎么用</strong>：评估新势力时优先结构/制动/疲劳验证证据，而非车机演示。</p>
    <div class="quote">「它的本质就是一个交通工具，它的本质就是应该安全。」[01:26]</div>
    <div class="relation">事实层：交通工具属性；观点层：一切核心围着安全。</div>
  </div>

  <div class="card card-orange">
    <h3>3. 宣传风险：「一千匹」与速成车</h3>
    <p><strong>在讲什么</strong>：极端性能口号可能塑造危险驾驶预期；仓促上市成「速成车」。</p>
    <p><strong>关键理解</strong>：行外人用消费电子 KPI 指挥行内人，会系统性低估应力与疲劳。</p>
    <p><strong>怎么用</strong>：把「一年多款上新」与「路试公里/工况覆盖」对照看。</p>
    <div class="quote">「所谓的叫速成车，这个词今年快速的活起来，我觉得这简直就是一个巨大的讽刺。」[02:40]</div>
    <div class="pitfall">陷阱：把参数竞赛当成安全进步。</div>
  </div>

  <div class="card card-green">
    <h3>4. 工业节奏：为何必须「慢」</h3>
    <p><strong>在讲什么</strong>：长研发、多工况路试、金属疲劳验证换来谨慎。</p>
    <p><strong>关键理解</strong>：慢不是落后，是对万分之一人命风险的定价。</p>
    <p><strong>怎么用</strong>：问厂商：极寒湿热高压与多少万公里真实路试是否公开可核验。</p>
    <div class="quote">「你得有这种几十万公里的真实路试跑下来……测试你的零件在……剧烈的应力受力下它的整个疲劳的程度。」[04:34]</div>
    <div class="highlight">「研发五年、测试五年」为作者概括传统节奏，非某厂官方数据。</div>
  </div>

  <div class="card card-red">
    <h3>5. 公关与信任：抠标、撇责、小白鼠感</h3>
    <p><strong>在讲什么</strong>：事故后抠标蒙布、推「使用不当」会摧毁家国情怀式信任。</p>
    <p><strong>关键理解</strong>：企业家 IP 正向时吸粉，反向时反噬；宏大叙事透支信用。</p>
    <p><strong>怎么用</strong>：看危机应对是否直面质量，而非先撇干净。</p>
    <div class="quote">「结果换来的却是这种我成了小白鼠，我成了这个试验品。」[09:52]</div>
    <div class="pitfall">「若上路断裂必发使用不当声明」属作者推测，非已出示的文件。</div>
  </div>

  <div class="card">
    <h3>横向对比：快消逻辑 vs 汽车工业逻辑</h3>
    <table>
      <thead><tr><th>维度</th><th>快消 / 消费电子逻辑</th><th>汽车工业逻辑（作者主张）</th></tr></thead>
      <tbody>
        <tr><td>产品本质</td><td>体验、更新、营销话题</td><td>交通工具；安全第一</td></tr>
        <tr><td>故障后果</td><td>重启、换电池、低成本</td><td>可能关人命</td></tr>
        <tr><td>迭代节奏</td><td>季度/月度上新、保值营销</td><td>长研发 + 多工况路试</td></tr>
        <tr><td>买家关注</td><td>颜色、屏幕、车机、舒适</td><td>驾驶性、安全性、结构疲劳</td></tr>
        <tr><td>竞争结果</td><td>可能劣币驱逐良币（认知被培育时）</td><td>应用血案教训换谨慎</td></tr>
        <tr><td>信任关系</td><td>粉丝/宏大叙事驱动购买</td><td>质量问题须直面，忌撇责</td></tr>
      </tbody>
    </table>
  </div>

  <div class="card card-orange">
    <h3>方法边界与立场分层</h3>
    <ul>
      <li><strong>可验证画面</strong>：口播者手持脆脆鲨；标题叠字「脆脆鲨事件」；录制标注 10 月 10 日。</li>
      <li><strong>作者观点</strong>：敬畏魏建军式经营；批评部分新势力蹭流量；制度推手导致错配；标志性事件判断。</li>
      <li><strong>推断/推测</strong>：上路后必发「使用不当」声明；三年后公司可能没了；往后还会出问题。</li>
      <li><strong>未核实</strong>：脆脆鲨事件对应的具体车型与零件；行业毛利率具体数字；补贴规模。</li>
      <li><strong>适用边界</strong>：本文是财经评论视角的产业批评，不是事故鉴定报告或购车型号推荐。</li>
    </ul>
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <ul>
      <li>汽车是耐用交通工具，安全约束硬于快消体验卖点。</li>
      <li>用手机营销逻辑指挥造车，易催生速成车与劣币市场。</li>
      <li>抠标蒙布、撇责「使用不当」会把家国情怀买家推成「韭菜感」。</li>
      <li>财务与叙事逼「快」时，代价常落在个体生命与二手残值上。</li>
    </ul>
    <h3>行动清单</h3>
    <ul>
      <li>购车清单把被动安全、制动、结构与路试信息放在屏幕参数之前。</li>
      <li>警惕「一年三款」「千匹」「移动的家」话术，追问验证周期。</li>
      <li>看品牌危机公关：是否直面质量，而非先抠标、蒙布、甩锅用户。</li>
      <li>把「上新速度」与「验证里程/工况」对照，避免只被宏大叙事打动。</li>
      <li>传播时区分：作者观点 vs 已核验事故事实，不二次造谣具体车型。</li>
    </ul>
    <h3>关键认知转变</h3>
    <ul>
      <li>以前：参数与车机越新越好 → 现在：关人命的验证节奏优先。</li>
      <li>以前：充分竞争自然出好车 → 现在：认知被快消化时可能劣币驱逐良币。</li>
      <li>以前：支持国货叙事即爱国 → 现在：被当小白鼠后信任反噬，理性声音在累积。</li>
    </ul>
  </div>

  <div class="footer">基于 Whisper 341 段转录 · 术语已校正脆脆鲨/快消品/魏建军等 · 分析视角非事故鉴定</div>
</div>`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
