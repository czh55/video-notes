#!/usr/bin/env node
/**
 * b62s：生成 car-not-fmcg-dont-test-customers 图文实录 HTML（未增强图注，供后续 gen-caption-audio + enhance）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const SLUG = 'car-not-fmcg-dont-test-customers';
const OUT = path.join(DIR, '..', 'docs', `${SLUG}-图文实录.html`);
const whisper = JSON.parse(fs.readFileSync(path.join(DIR, '..', 'b62s.json'), 'utf8'));

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function timestamp(seconds) {
  const total = Math.max(0, Math.floor(Number(seconds) || 0));
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const secs = total % 60;
  return hours
    ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    : `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

const segments = (whisper.segments || []).filter(
  (segment) => String(segment.text || '').trim()
);

const transcript = segments
  .map(
    (segment, index) => `
  <li class="transcript-row" id="transcript-${index + 1}">
    <time datetime="PT${Math.floor(segment.start || 0)}S">${timestamp(segment.start)}</time>
    <p>${escapeHtml(segment.text.trim())}</p>
  </li>`
  )
  .join('');

const CSS = `*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}header{margin-bottom:40px}
header h1{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.meta-tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}
.tag-platform{background:#ff2442;color:#fff}.tag-duration{background:#f1f5f9;color:#64748b}.tag-topic{background:#dbeafe;color:#1e40af}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none}.source-link:hover{text-decoration:underline}
.toc{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.toc h3{font-size:16px;color:#1e40af;margin:0 0 12px}.toc a{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}.toc a:hover{color:#3b82f6}
.documentary{font-size:17px}.story-section{margin:48px 0}
.story-section h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.story-section p{margin:0 0 14px;color:#44403c}
.story-section .quote{color:#57534e;font-style:italic}
.time-marker{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}
img{display:block;max-width:100%;height:auto}figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e;font-size:14px}
.transcript-section{margin-top:48px}
.transcript-note{font-size:14px;color:#78716c;margin-bottom:24px}.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}.transcript-row p{margin:0}
@media(max-width:640px){.container{padding:28px 18px 56px}header h1{font-size:24px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}
.transcript-collapsible{border:none;margin:0;padding:0}.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}
.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}
.transcript-collapsible[open] summary::before{transform:rotate(90deg)}.transcript-collapsible[open] summary{margin-bottom:16px}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
.content-points h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.content-points h3{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}`;

const documentaryBody = `
<header><h1>汽车不是快消品！千万不要把客户当小白鼠</h1>
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span><span class="meta-tag tag-duration">11分38秒</span><span class="meta-tag tag-topic">汽车 耐用品 安全 脆脆鲨 劣币驱逐良币</span></div>
<a class="source-link" href="https://xhslink.cn/o/2Ii0OJvl8V7" target="_blank" rel="noopener">→ 原视频链接</a>
<p style="margin:12px 0 0;color:#78716c;font-size:14px">UP：付鹏的财经世界 · 日期 2026-10-13 · 画面标注录制于 10 月 10 日</p></header>
<nav class="toc"><h3>内容导航</h3>
<a href="#ch-hook">犹豫开场：借「脆脆鲨」谈背后逻辑</a>
<a href="#ch-durable">汽车是耐用品：消费电子逻辑在指挥造车</a>
<a href="#ch-not-phone">汽车≠手机：安全第一与「一千匹」宣传</a>
<a href="#ch-brainwash">「移动的家」洗脑与劣币驱逐良币</a>
<a href="#ch-testing">为何换代慢：路试疲劳与抠标蒙布</a>
<a href="#ch-forced">被逼着卷：消费者被培育成快消品</a>
<a href="#ch-system">财务逼快与制度推手：代价落在个体</a>
<a href="#ch-backlash">企业家IP反噬：小白鼠感与玩火自焚</a>
<a href="#transcript">完整转录</a></nav>
<article class="documentary"><div class="content-points"><h2>内容要点</h2>
<p>财经博主付鹏借第三方测试中「脆脆鲨」（作者对某部件被踩断事件的代号，画面以雀巢威化作道具）谈汽车产业：汽车本质是耐用品与交通工具，安全必须排第一；把快消品/手机逻辑搬进造车，会催生「速成车」、劣币驱逐良币，并把消费者当小白鼠。他批评抠标蒙布式公关、财务逼「快」与宏大叙事透支信任，收束为：别让营销指挥专业造车，玩火终自焚。</p>
<h3>知识结构</h3>
<div class="summary-row"><span class="time-marker">[00:00→00:21]</span><div><strong>开场立场</strong><p>「别把用户当傻子，别把吹牛当文化」；犹豫仍要录，因「脆脆鲨」背后值得反思。</p></div></div>
<div class="summary-row"><span class="time-marker">[00:21→01:14]</span><div><strong>品类定性</strong><p>汽车是耐用品不是快消品；做手机/消费电子的逻辑在指挥专业造车；敬畏真心爱好经营的造车人。</p></div></div>
<div class="summary-row"><span class="time-marker">[01:14→02:48]</span><div><strong>安全边界</strong><p>手机可重启换电池，汽车关人命；「百公里几秒、一千匹」式宣传易催生马路杀手；「速成车」是巨大讽刺。</p></div></div>
<div class="summary-row"><span class="time-marker">[02:48→04:15]</span><div><strong>认知洗脑</strong><p>「移动的家」话术忽视驾驶与安全；年轻人只看屏与舒适；若断在真路上，厂家或推「使用不当」。</p></div></div>
<div class="summary-row"><span class="time-marker">[04:15→05:43]</span><div><strong>工业节奏</strong><p>传统换代慢因研发/测试/极寒湿热高压路试与金属疲劳；血案换谨慎；勿等出人命再反思；抠标蒙布是掩耳盗铃。</p></div></div>
<div class="summary-row"><span class="time-marker">[05:43→07:10]</span><div><strong>卷与培育</strong><p>低毛利率逼卷，现实劣币驱逐良币；消费者被培育成快消品认知，安全参数被忽略。</p></div></div>
<div class="summary-row"><span class="time-marker">[07:10→08:50]</span><div><strong>结构压力</strong><p>估值与融资逼「每月交新车」；补贴与弯道超车叙事违背经济常识；事故代价落在个体生命。</p></div></div>
<div class="summary-row"><span class="time-marker">[08:50→11:38]</span><div><strong>信任反噬</strong><p>企业家IP正反馈变反噬；家国情怀后发现成小白鼠/韭菜；理性舆论兴起；勿让营销指挥造车——玩火自焚。</p></div></div>
<div class="takeaway-box"><strong>总结</strong><p>汽车不是快消品：安全与耐用优先于参数营销；把客户当试验品、出事后撇责，终将透支信任并反噬品牌与行业。</p></div></div>

<section class="story-section" id="ch-hook">
  <h2><span class="time-marker">00:00–00:21</span>犹豫开场：借「脆脆鲨」谈背后逻辑</h2>
  <p>视频一上来叠出两句口号：<span class="quote">别把用户当傻子，别把吹牛当文化</span>。付鹏说自己其实挺犹豫要不要录这期——话题围绕他口中的「脆翠鲨 / 翠翠杀」（画面标题与道具已标明为「脆脆鲨」：后文他手持红包装雀巢威化，把「一踩就断」的脆性做成具象比喻）。他声明：不想只八卦事件本身，而要聊背后几件值得思考的事。</p>
  <p>画面始终是室内口播：木门背景、领夹麦、黄字大标题「汽车不是快消品！“脆脆鲨”事件给行业敲响警钟」，右下角「录制于10月10日」。具体车型与零件名视频未点名，正文按作者观点与画面证据展开，不补外部新闻细节。</p>
  <figure>
    <img src="assets/${SLUG}/shot-01.jpg" alt="作者直面镜头，黄字标题汽车不是快消品脆脆鲨事件给行业敲响警钟" loading="lazy">
    <figcaption>[00:08] 开场犹豫：借「脆脆鲨」被踩断一事，谈背后值得思考的几件事</figcaption>
  </figure>
</section>

<section class="story-section" id="ch-durable">
  <h2><span class="time-marker">00:21–01:14</span>汽车是耐用品：消费电子逻辑在指挥造车</h2>
  <p>他回顾几年前就反复讲过的观点：<span class="quote">汽车本质上来讲应该是个耐用品</span>，不应该被宣传、做成快消品概念。在「弯道超车、新能源」大背景下，他看到一群做手机、做消费电子的人，用快消品逻辑指挥专业造车的人——这是后文所有批评的总前提。</p>
  <p>他自己年轻时玩赛车、有赛车手执照。国内车圈他比较敬畏长城的魏建军：认为那是「真心用爱好经营一番事业」；而对其他一些做法，他认为本质跟蹭流量赚快钱差不多。此处是明确的<strong>作者立场</strong>，不是可独立核验的排行榜。</p>
  <figure>
    <img src="assets/${SLUG}/shot-02.jpg" alt="作者口播，字幕提及快消品逻辑在指挥专业造车" loading="lazy">
    <figcaption>[00:45] 新能源弯道超车背景下：做手机/消费电子的逻辑，在指挥专业造车的人</figcaption>
  </figure>
</section>

<section class="story-section" id="ch-not-phone">
  <h2><span class="time-marker">01:14–02:48</span>汽车≠手机：安全第一与「一千匹」宣传</h2>
  <p>核心对比：手机死机能重启，电池坏了大不了换一块；汽车本质是交通工具，<span class="quote">本质就是应该安全</span>，所有核心都要围着安全走。他举去年谈「小米造车相关宣传」（转录作「牟米」）时说过的话：不能拿「百公里几秒、一千匹」当口号——一千匹电机驱动当宣传，买车的人很容易变成「马路杀手」，刹不住。</p>
  <p>这被他概括为「行外人指挥行内人」。汽车也一样：怎么能说别人三年一辆、我一年三辆？涉及整车架构、结构应力与金属疲劳，万分之一也可能关人命——跟电视死机、家电故障完全不是一回事。卷到最后出现所谓「速成车」，他认为今年这个词快速活起来「简直是巨大的讽刺」。</p>
  <figure>
    <img src="assets/${SLUG}/shot-03.jpg" alt="作者严肃表情，字幕它的本质就是应该安全" loading="lazy">
    <figcaption>[01:30] 汽车≠手机：本质是交通工具，核心必须围着安全转</figcaption>
  </figure>
  <figure>
    <img src="assets/${SLUG}/shot-04.jpg" alt="作者口播，字幕我一年三辆车呢" loading="lazy">
    <figcaption>[02:10] 讽刺「别人三年一辆、我一年三辆」：架构与金属疲劳关乎人命，不是玩笑</figcaption>
  </figure>
</section>

<section class="story-section" id="ch-brainwash">
  <h2><span class="time-marker">02:48–04:15</span>「移动的家」洗脑与劣币驱逐良币</h2>
  <p>传统车企百年工业并不只是「慢」：年轻人被洗脑说车不是交通工具，是「移动的家」。付鹏纠正：车首先是交通运输工具，驾驶性、安全性应排第一；车里多卖两三万的舒适配置，一年能用几回？可营销、话术、洗脑方式全按快消品那套——「标准的一堆做消费电子、做快消品的人来跨界做汽车」。</p>
  <p>关键后果：市场环境竟是劣币驱逐良币。年轻人买车忽略参数与硬件，觉得「跟我没关系太难了」——直到「马路杀手」「脆脆鲨」这类事发生。他强调这次还好发生在第三方路试：若真断在路上，会不会来一份「与厂家无关、用户使用不当导致脆脆鲨折断」的声明？他认为<span class="quote">很有可能会</span>——属作者推测，视频未展示真实声明原文。</p>
  <figure>
    <img src="assets/${SLUG}/shot-05.jpg" alt="作者口播，字幕谈营销洗脑方式与快消品同套" loading="lazy">
    <figcaption>[03:25] 连营销、话术、洗脑方式都按快消品那套——标准的跨界错位</figcaption>
  </figure>
  <figure>
    <img src="assets/${SLUG}/shot-06.jpg" alt="作者口播，字幕发这样的一个声明" loading="lazy">
    <figcaption>[04:10] 推演：若断在真路上，厂家或会发「用户使用不当」式撇责声明</figcaption>
  </figure>
</section>

<section class="story-section" id="ch-testing">
  <h2><span class="time-marker">04:15–05:43</span>为何换代慢：路试疲劳与抠标蒙布</h2>
  <p>以前车型换代慢是有原因的：研发五年、测试五年（作者概括），上百辆测试车跑极寒、高湿、高压地区，几十万公里真实路试，就是为了看零件在成千上万次剧烈受力下的疲劳程度。传统汽车工业也经历过惨痛案例——每个真实案例背后是生命，所以车企越来越谨慎。他希望新势力能借这次认真反思，<span class="quote">不要等发生了血淋淋的生命的时候，再去思考这个问题</span>。</p>
  <p>过去一年即便路上已出事故，第一反应却是抠轮毂标、抠前脸标，或者蒙布——「掩耳盗铃」外加「皇帝的新装」。他举着脆脆鲨道具强调：这几年的事已经够让人认真思考和警示。</p>
  <figure>
    <img src="assets/${SLUG}/shot-07.jpg" alt="作者手持红色脆脆鲨威化，谈车企因血淋淋案例而更谨慎" loading="lazy">
    <figcaption>[05:00] 亮出脆脆鲨道具：传统工业用惨痛案例换来越来越谨慎，新势力勿等出人命再反思</figcaption>
  </figure>
  <figure>
    <img src="assets/${SLUG}/shot-08.jpg" alt="作者手持脆脆鲨挥动，谈近年事故后抠标蒙布" loading="lazy">
    <figcaption>[05:55] 路上出事后第一反应抠标、蒙布——掩耳盗铃式公关，作者呼吁认真警示</figcaption>
  </figure>
</section>

<section class="story-section" id="ch-forced">
  <h2><span class="time-marker">05:43–07:10</span>被逼着卷：消费者被培育成快消品</h2>
  <p>新能源车企是否「被逼的」？因为卷——看看行业毛利率就知道。道路上彻底变成劣币驱逐良币；他相信足够长时间会良币驱逐劣币，但现在被逼成反过来。理论上充分竞争应淘汰劣币留下良币，现实却取决于消费者认知：若大家都认「安全第一、车是交通工具」，市场就能筛选；现实却是消费者已被培育成快消品概念。</p>
  <p>他观察身边零零后买车：只看颜色、屏幕、车机、舒不舒服，从不考虑安全参数；一聊就说「车是个移动的家」——老司机会反问「什么移动的家，家里还是最舒服的」。消费者不是天生傻，是被营销话术洗过脑（转录「冲冲分分」处无法确认原文，按语境写「营销话术」）。</p>
</section>

<section class="story-section" id="ch-system">
  <h2><span class="time-marker">07:10–08:50</span>财务逼快与制度推手：代价落在个体</h2>
  <p>从车企侧：财务差、投资人焦虑、毛利率极低、打价格战——逼得你无法长期主义，必须「快」。每月交不出新车、季度不增长，估值掉、投资人要凉、融资断，供应链与金融全出问题；别说磨三年车，三年后公司可能没了。这是充分内卷的结果。</p>
  <p>再往上：为什么突然充分内卷？作者归因到「制度推手」导致产业链生产关系错配——大规模补贴、产业基金、政策扶持，表面上实现国家叙事里的弯道超车，却「违背经济常识与自然规律」。结果就是一窝蜂上、不良竞争；有人买单的是新车落地到二手车没人收的高昂代价，出了安全事故则很多人买单的是生命——代价都作用在个体上。脆脆鲨事件因此「很多地方值得反思」，他判断往后还会出问题。</p>
  <figure>
    <img src="assets/${SLUG}/shot-09.jpg" alt="作者手持脆脆鲨，字幕谈季度增长与估值压力" loading="lazy">
    <figcaption>[07:30] 财务与投资人逼「快」：磨三年车可能公司已没了，内卷逼出劣币驱逐良币</figcaption>
  </figure>
</section>

<section class="story-section" id="ch-backlash">
  <h2><span class="time-marker">08:50–11:38</span>企业家IP反噬：小白鼠感与玩火自焚</h2>
  <p>他曾在播客讲过企业家IP：正向时是反馈，反向时会「反噬」。百姓对宏大叙事、「遥遥领先」已经皮了；虽不否认一定历史阶段宏大叙事能激发热情（不买某手机/某车不行、粉崇拜到必须用其商品），但故事到现在不断透支信任与信用。</p>
  <p>消费者感觉：花了那么多钱，满怀家国情怀与自豪感去用，结果发现<span class="quote">我成了小白鼠、试验品、真实的路试</span>；小毛病出来不是面对解决，第一件事撇干净——「质量没问题，是你使用不当」。时间长了谁都不是傻子，落差变成被背叛：支持家国情怀，最后发现被当成韭菜。以前公关一上就能封杀式闭嘴，再扣「不爱国」大帽子；现在舆论里越来越多理性声音，对产品傲慢开始「玩火」——长期压抑的公众反感，双刃剑落到自己身上。</p>
  <p>收束三点：不要把车当快消品；不要给消费者洗脑；不要让造手机、造快消品、干营销的人指挥专业造车的人。<span class="quote">玩火的最终会把火玩到自己身上</span>。他认为这件事会成为中国制造业与汽车行业的标志性事件，且看后续——「又愤怒又叹息」。</p>
  <figure>
    <img src="assets/${SLUG}/shot-10.jpg" alt="作者口播，谈宏大叙事与企业家IP" loading="lazy">
    <figcaption>[09:20] 企业家IP正反馈变反噬：宏大叙事透支信任，消费者感觉自己成了小白鼠</figcaption>
  </figure>
  <figure>
    <img src="assets/${SLUG}/shot-11.jpg" alt="作者口播，字幕就我在支持家国情怀" loading="lazy">
    <figcaption>[10:20] 家国情怀买单后发现被当成韭菜：落差变成被背叛感，舆论开始出现理性怒火</figcaption>
  </figure>
  <figure>
    <img src="assets/${SLUG}/shot-12.jpg" alt="作者举起脆脆鲨，收束谈标志性事件" loading="lazy">
    <figcaption>[11:20] 收束：勿把车当快消品、勿让营销指挥造车；玩火终自焚——且看后续</figcaption>
  </figure>
</section>
</article>`;

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="付鹏借「脆脆鲨」谈汽车不是快消品：安全优先于参数营销；快消逻辑指挥造车会劣币驱逐良币并把客户当小白鼠；勿抠标撇责，玩火终自焚。">
  <title>汽车不是快消品！千万不要把客户当小白鼠｜图文实录</title>
  <style>${CSS}</style>
</head>
<body>
  <main class="container">
    ${documentaryBody}
    <section class="transcript-section" id="transcript">
      <details class="transcript-collapsible">
        <summary>详细文字转录</summary>
        <div class="transcript-body">
          <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。术语校正见正文（如翠翠沙→脆脆鲨、快销品→快消品、卫健军→魏建军、粮币→良币等）。</p>
          <ol class="transcript-list">${transcript}</ol>
        </div>
      </details>
    </section>
  </main>
  <script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script>
</body>
</html>`;

fs.writeFileSync(OUT, html, 'utf8');
console.log('Generated:', OUT, 'segments:', segments.length);
