#!/usr/bin/env python3
"""b60：为批内新视频追加 index.json 条目（幂等）。"""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "docs" / "index.json"
ENTRIES = [
    {
        "date": "2026-10-09",
        "title": "舞感的关键",
        "summary": "舞感不是往脸上贴表情，而是「体感放大」与「被音乐泡开」两件事接上：身体先感受到，脸才画龙点睛。",
        "primary": "sports",
        "tags": [
            "舞感",
            "身体体感",
            "具身认知",
            "音乐感受",
            "舞蹈表演"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/2kxR9ZGSEIQ",
        "duration": "9分29秒",
        "outputs": {
            "html": "dance-feel-key-图文实录.html",
            "svg": "dance-feel-key-理性分析.svg"
        },
        "screenshot_count": 7,
        "transcript_segments": 102,
        "svg_height": 4832,
        "slug": "dance-feel-key"
    },
    {
        "date": "2026-10-09",
        "title": "一年学会背肌发力跳舞进步快",
        "summary": "跳舞说的「背肌发力」，底层常常是肩胛下沉+内收的控制；出手向前则要换前锯肌，别用背肌硬推。",
        "primary": "sports",
        "tags": [
            "背肌发力",
            "肩胛骨",
            "沉肩",
            "肩袖",
            "前锯肌",
            "街舞"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/6gDEgIiR6Ah",
        "duration": "3分30秒",
        "outputs": {
            "html": "dance-back-muscle-engage-图文实录.html",
            "svg": "dance-back-muscle-engage-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 89,
        "svg_height": 5339,
        "slug": "dance-back-muscle-engage"
    },
    {
        "date": "2026-10-09",
        "title": "吴易昺专访｜2026我和我的四大满贯",
        "summary": "阿炳把 2026 写成可核对的两件事：身体能连续参赛，以及排名站上前三十——好看网球建立在健康与基本功 baseline 上，不是标签口号。",
        "primary": "sports",
        "tags": [
            "吴易昺",
            "网球",
            "四大满贯",
            "温网",
            "健康管理",
            "亚运会"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/8u8AsmzzoUZ",
        "duration": "10分57秒",
        "outputs": {
            "html": "wu-yibing-grand-slam-2026-图文实录.html",
            "svg": "wu-yibing-grand-slam-2026-理性分析.svg"
        },
        "screenshot_count": 10,
        "transcript_segments": 311,
        "svg_height": 5682,
        "slug": "wu-yibing-grand-slam-2026"
    },
    {
        "date": "2026-10-09",
        "title": "李诞教你如何跟人沟通",
        "summary": "想表达不同意见时，先去掉带纠正意味的「其实」起手，把接话练得像即兴喜剧一样承接对方。",
        "primary": "workplace",
        "tags": [
            "李诞",
            "沟通",
            "尊重",
            "即兴喜剧",
            "其实"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/4NhiQ3hREtW",
        "duration": "18秒",
        "outputs": {
            "html": "li-dan-how-to-communicate-图文实录.html",
            "svg": "li-dan-how-to-communicate-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 1,
        "svg_height": 4631,
        "slug": "li-dan-how-to-communicate"
    },
    {
        "date": "2026-10-09",
        "title": "突然就醒悟了",
        "summary": "你以为的「规律」，经常只是筛选后的幸存者故事：反过来的样本根本没机会出现在你眼前。",
        "primary": "other",
        "tags": [
            "选择偏差",
            "段子",
            "生活观察",
            "幸存者偏差"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/2mbmYSz1MAL",
        "duration": "25秒",
        "outputs": {
            "html": "sudden-awakening-图文实录.html",
            "svg": "sudden-awakening-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 12,
        "svg_height": 4638,
        "slug": "sudden-awakening"
    },
    {
        "date": "2026-10-09",
        "title": "普通人审丑积累",
        "summary": "普通人变美的捷径往往是「审丑」：先记住哪些组合会互相放大缺陷，再决定妆造取舍。",
        "primary": "makeup",
        "tags": [
            "审丑",
            "五官搭配",
            "美商",
            "化妆",
            "面部平衡"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/AYyQhz65iZS",
        "duration": "49秒",
        "outputs": {
            "html": "amateur-ugly-taste-build-图文实录.html",
            "svg": "amateur-ugly-taste-build-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 16,
        "svg_height": 4688,
        "slug": "amateur-ugly-taste-build"
    },
    {
        "date": "2026-10-09",
        "title": "纯度、明度一看就懂",
        "summary": "明度问深浅，纯度问鲜灰；加水或加补色都会拉低纯度，所以调明度时别以为纯度还能原地不动。",
        "primary": "painting",
        "tags": [
            "明度",
            "纯度",
            "水彩",
            "补色",
            "色彩基础"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/7mFa8n6obM5",
        "duration": "1分12秒",
        "outputs": {
            "html": "chroma-vs-value-basics-图文实录.html",
            "svg": "chroma-vs-value-basics-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 12,
        "svg_height": 4536,
        "slug": "chroma-vs-value-basics"
    },
    {
        "date": "2026-10-09",
        "title": "会不会配色其实就差一点点",
        "summary": "会配色往往不是换一套色相，而是会不会在交界处「塞一点点」中性色或强调色，让夺目变成可控。",
        "primary": "painting",
        "tags": [
            "配色",
            "色彩分割",
            "色彩强调",
            "互补色",
            "设计"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/ANOOA9kPwM3",
        "duration": "2分30秒",
        "outputs": {
            "html": "color-matching-tiny-gap-图文实录.html",
            "svg": "color-matching-tiny-gap-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 41,
        "svg_height": 5367,
        "slug": "color-matching-tiny-gap"
    },
    {
        "date": "2026-10-09",
        "title": "肤色脏不是黄的错｜统一色彩才是干净",
        "summary": "脸脏优先查「色彩是否统一」和「高光是否跳」，而不是把黄当成罪犯狂减——黄色本身没有错。",
        "primary": "makeup",
        "tags": [
            "修图",
            "肤色",
            "减黄",
            "可选颜色",
            "高光",
            "统一色彩"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/5SzcDie0bJq",
        "duration": "4分30秒",
        "outputs": {
            "html": "dirty-skin-tone-not-yellow-图文实录.html",
            "svg": "dirty-skin-tone-not-yellow-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 4,
        "svg_height": 4746,
        "slug": "dirty-skin-tone-not-yellow"
    },
    {
        "date": "2026-10-09",
        "title": "30s看懂眼睛年轻感的关键",
        "summary": "眼睛年轻感看的是眉弓到泪沟、外眦之间的明暗过渡是否顺，而不是单一「眼睛有多大」。",
        "primary": "makeup",
        "tags": [
            "眼周",
            "泪沟",
            "眶外C",
            "年轻感",
            "五亚单位"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/9teipdZEnDS",
        "duration": "23秒",
        "outputs": {
            "html": "eye-youthfulness-key-30s-图文实录.html",
            "svg": "eye-youthfulness-key-30s-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 1,
        "svg_height": 4574,
        "slug": "eye-youthfulness-key-30s"
    },
    {
        "date": "2026-10-09",
        "title": "顶美侧脸骨相P图全过程",
        "summary": "侧脸好看靠的是鼻—唇角—下巴一条连续骨相线，而不是把鼻子单独拉高。",
        "primary": "makeup",
        "tags": [
            "骨相修图",
            "侧脸",
            "鼻翼",
            "鼻唇角",
            "下颌线"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/61q39hfwcX1",
        "duration": "3分14秒",
        "outputs": {
            "html": "top-beauty-side-face-retouch-图文实录.html",
            "svg": "top-beauty-side-face-retouch-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 18,
        "svg_height": 4716,
        "slug": "top-beauty-side-face-retouch"
    },
    {
        "date": "2026-10-09",
        "title": "日本模特的走路方式",
        "summary": "模特步不是「走得好看」，而是立颈+收腹+内侧一条线三件事同时在线。",
        "primary": "sports",
        "tags": [
            "模特步",
            "体态",
            "立颈",
            "收腹",
            "一条线"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/16Se6y0U3ds",
        "duration": "2分17秒",
        "outputs": {
            "html": "japanese-model-walk-posture-图文实录.html",
            "svg": "japanese-model-walk-posture-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 63,
        "svg_height": 4671,
        "slug": "japanese-model-walk-posture"
    },
    {
        "date": "2026-10-09",
        "title": "一个视频让你学会打光技巧",
        "summary": "人像别正顶光；把灯移到面前高位做蝴蝶光/主光，脸立刻立起来。",
        "primary": "photo",
        "tags": [
            "打光",
            "TopLight",
            "Butterfly",
            "KeyLight",
            "人像光"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/BqPHj1GgRI",
        "duration": "20秒",
        "outputs": {
            "html": "learn-lighting-one-video-图文实录.html",
            "svg": "learn-lighting-one-video-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 1,
        "svg_height": 4602,
        "slug": "learn-lighting-one-video"
    },
    {
        "date": "2026-10-09",
        "title": "乐理知识：转调",
        "summary": "转调难的不是新旋律，而是同一旋律被抬高后的「身体不稳」——要靠反复练熟新高度。",
        "primary": "other",
        "tags": [
            "转调",
            "升调",
            "唱歌",
            "高跟鞋比喻",
            "乐理"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/9ebEce2JnTQ",
        "duration": "3分59秒",
        "outputs": {
            "html": "music-theory-modulation-图文实录.html",
            "svg": "music-theory-modulation-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 49,
        "svg_height": 4716,
        "slug": "music-theory-modulation"
    },
    {
        "date": "2026-10-09",
        "title": "布光实用小妙招：伪色辅助分区布光",
        "summary": "伪色把「亮不亮」变成「什么颜色」——先把脸调进粉色区，再谈风格光比。",
        "primary": "photo",
        "tags": [
            "伪色",
            "分区曝光",
            "面部粉色",
            "光比",
            "LUT"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/O1hxH693rt",
        "duration": "1分29秒",
        "outputs": {
            "html": "false-color-zone-lighting-图文实录.html",
            "svg": "false-color-zone-lighting-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 43,
        "svg_height": 5339,
        "slug": "false-color-zone-lighting"
    },
    {
        "date": "2026-10-09",
        "title": "长期做饭和偶尔做饭的差别",
        "summary": "长期做饭的辛苦在「不可选择」和「要伺候众人口味」，不是偶尔秀一盘菜能等价理解的。",
        "primary": "home",
        "tags": [
            "长期做饭",
            "家务劳动",
            "理解",
            "善待"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/8Y5rBkkvg2p",
        "duration": "52秒",
        "outputs": {
            "html": "cook-often-vs-occasionally-图文实录.html",
            "svg": "cook-often-vs-occasionally-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 17,
        "svg_height": 4716,
        "slug": "cook-often-vs-occasionally"
    },
    {
        "date": "2026-10-09",
        "title": "英语听力应该怎么学",
        "summary": "听力进步=完善语音库：听得懂难度的材料 + 三遍不懂就查 + 把声音刻进脑子。",
        "primary": "workplace",
        "tags": [
            "英语听力",
            "语音库",
            "精听",
            "语感",
            "录音机"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/s3UIEceoTr",
        "duration": "6分14秒",
        "outputs": {
            "html": "how-to-learn-english-listening-图文实录.html",
            "svg": "how-to-learn-english-listening-理性分析.svg"
        },
        "screenshot_count": 7,
        "transcript_segments": 18,
        "svg_height": 5339,
        "slug": "how-to-learn-english-listening"
    },
    {
        "date": "2026-10-09",
        "title": "头前伸先看看你的脚是不是这样",
        "summary": "头前伸先查脚下重心：脚后跟承接、胸廓不后压，脖子才抬得起来。",
        "primary": "sports",
        "tags": [
            "头前伸",
            "重心",
            "脚后跟",
            "鸟狗式",
            "前足"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/8pmIQcASWyy",
        "duration": "2分09秒",
        "outputs": {
            "html": "forward-head-check-your-feet-图文实录.html",
            "svg": "forward-head-check-your-feet-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 7,
        "svg_height": 4716,
        "slug": "forward-head-check-your-feet"
    },
    {
        "date": "2026-10-09",
        "title": "这才是真正的骨相P图",
        "summary": "真骨相是少量、对点的结构位移，不是整脸拉成另一个人。",
        "primary": "makeup",
        "tags": [
            "骨相",
            "侧脸",
            "收嘴",
            "下巴",
            "头包脸"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/5ylfvu4FSqQ",
        "duration": "1分59秒",
        "outputs": {
            "html": "real-bone-structure-retouch-图文实录.html",
            "svg": "real-bone-structure-retouch-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 24,
        "svg_height": 4716,
        "slug": "real-bone-structure-retouch"
    },
    {
        "date": "2026-10-09",
        "title": "修了像没修的高清骨相修图思路",
        "summary": "隐形高清骨相=结构只挪该挪的毫米，皮肤与骨相身份绝不磨平。",
        "primary": "makeup",
        "tags": [
            "高清骨相",
            "原生质感",
            "地包天",
            "下颌角",
            "头包脸"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/6E2ZPRPtZPB",
        "duration": "2分37秒",
        "outputs": {
            "html": "invisible-hd-bone-retouch-图文实录.html",
            "svg": "invisible-hd-bone-retouch-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 42,
        "svg_height": 4716,
        "slug": "invisible-hd-bone-retouch"
    },
    {
        "date": "2026-10-09",
        "title": "阔面脸骨相修图全程：比例优先，别推成假直角肩",
        "summary": "阔面骨相修图的关键是比例与结构：先收宽再微调五官，手推保留拐角；发量与斜方肌只做「轻薄体态」，不做假直角肩。",
        "primary": "makeup",
        "tags": [
            "阔面",
            "骨相修图",
            "脸宽",
            "发际线",
            "颅顶",
            "斜方肌"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/Tk5MTFaUpu",
        "duration": "3分58秒",
        "outputs": {
            "html": "wide-face-bone-retouch-图文实录.html",
            "svg": "wide-face-bone-retouch-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 36,
        "svg_height": 4832,
        "slug": "wide-face-bone-retouch"
    },
    {
        "date": "2026-10-09",
        "title": "转场到底怎么用：懂了逻辑别套模板",
        "summary": "好用的转场服务叙事：文字卡管节奏分段，相似形管时空呼应，空镜管换空间/跳时间——懂逻辑再玩模板。",
        "primary": "video",
        "tags": [
            "转场",
            "文字卡",
            "相似形",
            "空镜",
            "剪辑节奏"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/8vk92BM6LS6",
        "duration": "5分42秒",
        "outputs": {
            "html": "how-to-use-transitions-图文实录.html",
            "svg": "how-to-use-transitions-理性分析.svg"
        },
        "screenshot_count": 7,
        "transcript_segments": 64,
        "svg_height": 5175,
        "slug": "how-to-use-transitions"
    },
    {
        "date": "2026-10-09",
        "title": "CCD真的能拍出片吗：色温场景比机型更重要",
        "summary": "CCD 出片先靠色温选择与场景匹配：近距与闪光灯稳，自动夜景先避；懂色温，手里的自动机也能「变可口」。",
        "primary": "photo",
        "tags": [
            "CCD",
            "色温",
            "阴天模式",
            "闪光灯",
            "夜景噪点"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/77xMueg8Cx1",
        "duration": "2分03秒",
        "outputs": {
            "html": "can-ccd-make-good-photos-图文实录.html",
            "svg": "can-ccd-make-good-photos-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 51,
        "svg_height": 4667,
        "slug": "can-ccd-make-good-photos"
    },
    {
        "date": "2026-10-09",
        "title": "影像科普：单反镜头3D组件解构",
        "summary": "镜头不是「一块玻璃」：镀膜抑眩光、光圈管景深、镜组汇聚、特殊玻璃校像差、马达对焦、防抖补偿——每层都在管光。",
        "primary": "photo",
        "tags": [
            "镜头解剖",
            "光圈",
            "ED镜片",
            "超声波马达",
            "光学防抖"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/9TOMMyDfB75",
        "duration": "48秒",
        "outputs": {
            "html": "dslr-lens-3d-teardown-图文实录.html",
            "svg": "dslr-lens-3d-teardown-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 2,
        "svg_height": 4593,
        "slug": "dslr-lens-3d-teardown"
    },
    {
        "date": "2026-10-09",
        "title": "影像科普：单反相机3D组件解构",
        "summary": "按下快门的一瞬间：镜子让路、前后帘开合、传感器与处理器把光写成文件——单反是光路机器，不只是「一个按键」。",
        "primary": "photo",
        "tags": [
            "单反解剖",
            "反光镜",
            "五棱镜",
            "焦平面快门",
            "CMOS"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/1S68naEsiaq",
        "duration": "1分02秒",
        "outputs": {
            "html": "dslr-body-3d-teardown-图文实录.html",
            "svg": "dslr-body-3d-teardown-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 4,
        "svg_height": 5285,
        "slug": "dslr-body-3d-teardown"
    },
    {
        "date": "2026-10-09",
        "title": "60秒看懂：光如何变成照片",
        "summary": "照片不是「按一下就有」：先有反射光，再被镜头汇聚到感光面，最后被化学或电子记录——三步缺一不可。",
        "primary": "photo",
        "tags": [
            "成像原理",
            "反射光",
            "汇聚",
            "传感器",
            "拜耳滤镜"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/4f39pXdHpT5",
        "duration": "1分01秒",
        "outputs": {
            "html": "how-light-becomes-photo-图文实录.html",
            "svg": "how-light-becomes-photo-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 25,
        "svg_height": 4638,
        "slug": "how-light-becomes-photo"
    },
    {
        "date": "2026-10-09",
        "title": "没有大光圈？4招拍出奶油般虚化",
        "summary": "虚化是四个旋钮的乘积：光圈、物距、焦距、背景距离——大光圈只是其中一个，不是唯一门票。",
        "primary": "photo",
        "tags": [
            "虚化",
            "光圈",
            "物距",
            "焦距",
            "背景距离"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/8VvaEBhebFT",
        "duration": "1分19秒",
        "outputs": {
            "html": "creamy-bokeh-without-wide-aperture-图文实录.html",
            "svg": "creamy-bokeh-without-wide-aperture-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 12,
        "svg_height": 5273,
        "slug": "creamy-bokeh-without-wide-aperture"
    },
    {
        "date": "2026-10-09",
        "title": "花两万上全画幅，白天效果竟与残幅无差？",
        "summary": "全画幅不是白天风景的必选项；它的溢价更多花在暗光干净度与浅景深从容度上——先问自己常拍什么光。",
        "primary": "photo",
        "tags": [
            "全画幅",
            "半画幅",
            "大底",
            "夜景",
            "虚化"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/6vTtHJmuHwb",
        "duration": "59秒",
        "outputs": {
            "html": "full-frame-daylight-vs-aps-c-图文实录.html",
            "svg": "full-frame-daylight-vs-aps-c-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 2,
        "svg_height": 4650,
        "slug": "full-frame-daylight-vs-aps-c"
    },
    {
        "date": "2026-10-09",
        "title": "逆光拍照片就多出一串小太阳？",
        "summary": "逆光小太阳是光学迷宫里的杂散光表演；镀膜决定抗性，劣质UV常是帮凶，遮光罩负责挡斜光——先控光再怪镜头。",
        "primary": "photo",
        "tags": [
            "逆光",
            "鬼影",
            "眩光",
            "纳米镀膜",
            "UV镜",
            "遮光罩"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/9J7ia7RPTrD",
        "duration": "1分36秒",
        "outputs": {
            "html": "backlight-sunstar-flare-图文实录.html",
            "svg": "backlight-sunstar-flare-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 2,
        "svg_height": 4724,
        "slug": "backlight-sunstar-flare"
    },
    {
        "date": "2026-10-09",
        "title": "空气透视到底是啥：越远越冷、越灰、越淡",
        "summary": "空气透视不是只把远处画小：是对比、饱和与冷暖随距离衰减——图层上「越远越冷越灰」，空间才立得住。",
        "primary": "painting",
        "tags": [
            "空气透视",
            "图层",
            "饱和度",
            "冷暖",
            "绘画"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/2WP2TsQKJey",
        "duration": "4分12秒",
        "outputs": {
            "html": "what-is-aerial-perspective-图文实录.html",
            "svg": "what-is-aerial-perspective-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 17,
        "svg_height": 4622,
        "slug": "what-is-aerial-perspective"
    },
    {
        "date": "2026-10-09",
        "title": "一片玻璃就能成像，变焦镜头为何要塞十几片",
        "summary": "镜片数量不是堆料，而是消像差的互相纠正；镀膜则是「玻璃一多」之后的透光与眩光账单。",
        "primary": "photo",
        "tags": [
            "变焦镜头",
            "像差",
            "镀膜",
            "非球面",
            "ED镜片"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/9R8xo381hcP",
        "duration": "1分26秒",
        "outputs": {
            "html": "why-zoom-needs-many-elements-图文实录.html",
            "svg": "why-zoom-needs-many-elements-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 16,
        "svg_height": 5511,
        "slug": "why-zoom-needs-many-elements"
    },
    {
        "date": "2026-10-09",
        "title": "老伴儿你真聪明",
        "summary": "笑点全在「按你的规则算到底」：计价单位、赠品边界、租期口径一旦被咬死，店家只能让步或改口。",
        "primary": "other",
        "tags": [
            "段子",
            "夫妻",
            "砍价",
            "生活喜剧"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/7mgigB0o5Dv",
        "duration": "2分3秒",
        "outputs": {
            "html": "laobanr-you-are-smart-图文实录.html",
            "svg": "laobanr-you-are-smart-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 36,
        "svg_height": 4631,
        "slug": "laobanr-you-are-smart"
    },
    {
        "date": "2026-10-09",
        "title": "顶级导演是如何拍摄一镜到底的",
        "summary": "一镜到底的丝滑，来自「盲区叙事＋遮挡转场＋人物接力调度」，不是相机一直往前推。",
        "primary": "film",
        "tags": [
            "一镜到底",
            "昆汀",
            "调度",
            "长镜头",
            "电影"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/AoNibzIRspc",
        "duration": "3分51秒",
        "outputs": {
            "html": "directors-one-take-shooting-图文实录.html",
            "svg": "directors-one-take-shooting-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 56,
        "svg_height": 5436,
        "slug": "directors-one-take-shooting"
    },
    {
        "date": "2026-10-09",
        "title": "国庆旅游打卡点一定不要这样拍",
        "summary": "打卡照输在「人是贴图」；赢在「人跟东西玩起来」。",
        "primary": "photo",
        "tags": [
            "打卡拍照",
            "姿势",
            "互动",
            "旅行摄影"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/WNupM2VEJW",
        "duration": "32秒",
        "outputs": {
            "html": "dont-shoot-checkpoints-wrong-图文实录.html",
            "svg": "dont-shoot-checkpoints-wrong-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 23,
        "svg_height": 4631,
        "slug": "dont-shoot-checkpoints-wrong"
    },
    {
        "date": "2026-10-09",
        "title": "4招把旅行照片做成超好玩vlog",
        "summary": "旅行vlog不一定缺素材，缺的是把照片「动画化」的四套模板动作。",
        "primary": "video",
        "tags": [
            "旅行vlog",
            "剪辑",
            "邮票模板",
            "色彩地标",
            "拍立得"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/46onJsgdePx",
        "duration": "2分6秒",
        "outputs": {
            "html": "travel-photos-into-fun-vlog-图文实录.html",
            "svg": "travel-photos-into-fun-vlog-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 38,
        "svg_height": 5253,
        "slug": "travel-photos-into-fun-vlog"
    },
    {
        "date": "2026-10-09",
        "title": "面试最后一个问题这样回答容易拿到offer",
        "summary": "好反问不是查资料，而是请对方预演「雇用你成功」，并把成功标准说给你听。",
        "primary": "workplace",
        "tags": [
            "面试",
            "offer",
            "反问",
            "职场",
            "沟通"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/ATnQrvXOVbs",
        "duration": "1分56秒",
        "outputs": {
            "html": "interview-last-question-offer-图文实录.html",
            "svg": "interview-last-question-offer-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 46,
        "svg_height": 4689,
        "slug": "interview-last-question-offer"
    },
    {
        "date": "2026-10-09",
        "title": "中国人造院不宜照搬日式园林",
        "summary": "造院先问中式空间要什么体验（联系、俯仰、闹静对照），而不是先搬日式符号。",
        "primary": "home",
        "tags": [
            "造院",
            "扬州园林",
            "方惠",
            "日式园林",
            "庭院"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/63hgAVxui5S",
        "duration": "1分35秒",
        "outputs": {
            "html": "chinese-courtyard-not-japanese-图文实录.html",
            "svg": "chinese-courtyard-not-japanese-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 19,
        "svg_height": 4631,
        "slug": "chinese-courtyard-not-japanese"
    },
    {
        "date": "2026-10-09",
        "title": "4万人挤进一条山沟居然不堵",
        "summary": "景区承载力靠「阀门分层」而不是靠劝人少来。",
        "primary": "other",
        "tags": [
            "九寨沟",
            "客流",
            "观光车",
            "预约",
            "调度"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/1ikXuUcnnkx",
        "duration": "1分53秒",
        "outputs": {
            "html": "jiuzhaigou-crowd-no-jam-图文实录.html",
            "svg": "jiuzhaigou-crowd-no-jam-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 36,
        "svg_height": 5334,
        "slug": "jiuzhaigou-crowd-no-jam"
    },
    {
        "date": "2026-10-09",
        "title": "12306一天卖2973万张票凭啥不崩",
        "summary": "12306扛量靠「削峰＋算段＋排队＋候补公平」，不是单靠加机器硬抗同一秒抢同一张票。",
        "primary": "other",
        "tags": [
            "12306",
            "春运",
            "候补",
            "错峰起售",
            "余票"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/4s1lOrAg1L7",
        "duration": "2分6秒",
        "outputs": {
            "html": "why-12306-handles-tickets-图文实录.html",
            "svg": "why-12306-handles-tickets-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 25,
        "svg_height": 5523,
        "slug": "why-12306-handles-tickets"
    },
    {
        "date": "2026-10-09",
        "title": "保护刹车片：长下坡的正确打开方式",
        "summary": "长下坡先用档位让发动机帮忙减速，刹车留给真正需要的时候。",
        "primary": "auto-digital",
        "tags": [
            "发动机制动",
            "长下坡",
            "M档",
            "空档",
            "刹车片"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/8iYFq47WhPm",
        "duration": "48秒",
        "outputs": {
            "html": "protect-brakes-long-downhill-图文实录.html",
            "svg": "protect-brakes-long-downhill-理性分析.svg"
        },
        "screenshot_count": 3,
        "transcript_segments": 9,
        "svg_height": 4671,
        "slug": "protect-brakes-long-downhill"
    },
    {
        "date": "2026-10-09",
        "title": "刹车时为什么发动机不会熄火",
        "summary": "不熄火靠的是「中高速断油+发动机制动」与「低速切断动力」两套剧本；顿挫与怠速微窜，多半是断接时机或半联动没处理好。",
        "primary": "auto-digital",
        "tags": [
            "发动机制动",
            "减速断油",
            "离合器",
            "变矩器",
            "刹车联动"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/7T5araLbd4F",
        "duration": "3分20秒",
        "outputs": {
            "html": "why-engine-not-stall-braking-图文实录.html",
            "svg": "why-engine-not-stall-braking-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 100,
        "svg_height": 5568,
        "slug": "why-engine-not-stall-braking"
    },
    {
        "date": "2026-10-09",
        "title": "奥迪档位正确使用教程",
        "summary": "P 停、R 倒、N 拖、D 走；长坡与堵车切 M 借发动机制动，超车往后拉进 S——按场景换模式，而不是一路 D 到底。",
        "primary": "auto-digital",
        "tags": [
            "奥迪",
            "档位",
            "P",
            "R",
            "N",
            "D",
            "M",
            "S",
            "发动机制动"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/1Lb3rndwit0",
        "duration": "1分48秒",
        "outputs": {
            "html": "audi-gear-usage-guide-图文实录.html",
            "svg": "audi-gear-usage-guide-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 34,
        "svg_height": 5637,
        "slug": "audi-gear-usage-guide"
    },
    {
        "date": "2026-10-09",
        "title": "学车干货：下坡发动机制动",
        "summary": "空档滑行等于扔掉发动机制动；长下坡用低档带档，让发动机帮你拽车，刹车才能留作余量。",
        "primary": "auto-digital",
        "tags": [
            "发动机制动",
            "长下坡",
            "带档滑行",
            "空档"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/9KyiJl02aN",
        "duration": "48秒",
        "outputs": {
            "html": "downhill-engine-braking-图文实录.html",
            "svg": "downhill-engine-braking-理性分析.svg"
        },
        "screenshot_count": 4,
        "transcript_segments": 22,
        "svg_height": 4437,
        "slug": "downhill-engine-braking"
    },
    {
        "date": "2026-10-09",
        "title": "干式双离合什么情况下会过热",
        "summary": "干式双离合怕的是「踩着刹车慢慢蹭」的半联动摩擦热，不是单纯堵车或频繁换挡；能锁档或别低速刹爬，温度就稳得多。",
        "primary": "auto-digital",
        "tags": [
            "干式双离合",
            "过热",
            "OBD",
            "蠕行",
            "半联动"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/wuzjyPzJd0",
        "duration": "5分54秒",
        "outputs": {
            "html": "dry-dct-overheat-when-图文实录.html",
            "svg": "dry-dct-overheat-when-理性分析.svg"
        },
        "screenshot_count": 8,
        "transcript_segments": 43,
        "svg_height": 5571,
        "slug": "dry-dct-overheat-when"
    },
    {
        "date": "2026-10-09",
        "title": "奥迪低速顿挫是因为你没做对这三点",
        "summary": "双离合要「明确信号、少磨半联动」：冷车预热、低速别刹爬、红灯挂 N、坡道用自动驻车——操作对了，顿挫会像换了一台箱。",
        "primary": "auto-digital",
        "tags": [
            "奥迪",
            "双离合",
            "低速顿挫",
            "半联动",
            "变速箱油"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/bXR8WjstcV",
        "duration": "2分12秒",
        "outputs": {
            "html": "audi-low-speed-jerk-three-fixes-图文实录.html",
            "svg": "audi-low-speed-jerk-three-fixes-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 51,
        "svg_height": 4896,
        "slug": "audi-low-speed-jerk-three-fixes"
    },
    {
        "date": "2026-10-09",
        "title": "奥迪双离合顿挫教你两招轻松解决",
        "summary": "顿挫先当软件/学习问题：升级程序 + 自学习校准间隙，通常比直接换上万块离合器总成更划算。",
        "primary": "auto-digital",
        "tags": [
            "奥迪",
            "双离合",
            "程序升级",
            "离合自学习",
            "防坑"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/AdMVLJoy8yZ",
        "duration": "2分09秒",
        "outputs": {
            "html": "audi-dct-jerk-two-fixes-图文实录.html",
            "svg": "audi-dct-jerk-two-fixes-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 17,
        "svg_height": 5453,
        "slug": "audi-dct-jerk-two-fixes"
    },
    {
        "date": "2026-10-09",
        "title": "德系美系和日系一上手却像三个物种",
        "summary": "三国手感差在路况目标函数：德为高速可控留锐利与声浪，日为低速好开做轻软，美为长途抗长波做虚位与隔音——到中国再被「软+大屏」改写一版。",
        "primary": "auto-digital",
        "tags": [
            "德系",
            "美系",
            "日系",
            "路感",
            "调校",
            "虚位",
            "双离合",
            "CVT"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/YhU1SLKVEf",
        "duration": "4分03秒",
        "outputs": {
            "html": "german-us-japanese-drive-feel-图文实录.html",
            "svg": "german-us-japanese-drive-feel-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 3,
        "svg_height": 5751,
        "slug": "german-us-japanese-drive-feel"
    },
    {
        "date": "2026-10-09",
        "title": "车辆过弯道遇到推头怎么办",
        "summary": "推头时先减负荷恢复前轮抓地：松油门、轻点刹、微微回方向——猛打方向或猛刹只会把前轮推得更滑。",
        "primary": "auto-digital",
        "tags": [
            "推头",
            "转向不足",
            "弯道",
            "前驱",
            "抓地力"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/1StWrH7QXR6",
        "duration": "2分48秒",
        "outputs": {
            "html": "understeer-in-corners-what-to-do-图文实录.html",
            "svg": "understeer-in-corners-what-to-do-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 12,
        "svg_height": 4793,
        "slug": "understeer-in-corners-what-to-do"
    },
    {
        "date": "2026-10-09",
        "title": "EP18 推头才知前轮极限",
        "summary": "先学会「做出并维持推头」，你才真正摸到前轮极限；油门深浅就是前后轴抓地的开关，别一上来就练甩尾。",
        "primary": "auto-digital",
        "tags": [
            "转向不足",
            "前轮极限",
            "负载转移",
            "iRacing",
            "半油门"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/4b2d5q4pxTW",
        "duration": "4分06秒",
        "outputs": {
            "html": "understeer-front-tire-limit-图文实录.html",
            "svg": "understeer-front-tire-limit-理性分析.svg"
        },
        "screenshot_count": 6,
        "transcript_segments": 140,
        "svg_height": 5556,
        "slug": "understeer-front-tire-limit"
    },
    {
        "date": "2026-10-09",
        "title": "如何看懂这个设计",
        "summary": "好看不是随便摆：字体切割、古典母题、对称骨架和角标编号，都在把「随意」收成可读的秩序。",
        "primary": "painting",
        "tags": [
            "海报设计",
            "可读性",
            "对称",
            "字体",
            "古典"
        ],
        "platform": "xiaohongshu",
        "url": "https://xhslink.cn/o/3ffdENx9kyB",
        "duration": "1分31秒",
        "outputs": {
            "html": "how-to-read-this-design-图文实录.html",
            "svg": "how-to-read-this-design-理性分析.svg"
        },
        "screenshot_count": 5,
        "transcript_segments": 23,
        "svg_height": 5511,
        "slug": "how-to-read-this-design"
    }
]

def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    existing = {e.get("slug") or e.get("outputs",{}).get("html","") for e in data}
    added = 0
    for e in ENTRIES:
        if e["slug"] in existing or e["outputs"]["html"] in existing:
            continue
        data.insert(0, e)
        added += 1
    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added {added}, total {len(data)}")

if __name__ == "__main__":
    main()
