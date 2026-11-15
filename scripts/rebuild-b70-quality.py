#!/usr/bin/env python3
"""重建 b70 四篇双轨文章：简体化 + 术语校对 + 真实总结/章节 + 内容对齐截图与双语图注。

- 读取本地 whisper json（t2s + 术语表校正）作为转录证据
- 用人工撰写的内容（导语/章节/图注/英文翻译/行动清单）重新生成 HTML + SVG
- 重抽截图到内容时间点，图注时间戳与画面一致
- 更新 translations.json 与 docs/index.json（本地，不访问小红书）
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import html as html_mod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from opencc import OpenCC
from b70_dualtrack_lib import HTML_CSS, SVG_CSS, build_svg  # noqa: E402

CC = OpenCC("t2s")
WORK = ROOT / "_work" / "b70"


def esc(s: str) -> str:
    return html_mod.escape(s or "", quote=True)


def ts(seconds: float) -> str:
    t = int(round(seconds))
    m, s = divmod(t, 60)
    return f"{m:02d}:{s:02d}"


def to_sec(label: str) -> int:
    m, s = label.split(":")
    return int(m) * 60 + int(s)


def apply_fixes(text: str, fixes: list[tuple[str, str]]) -> str:
    for a, b in fixes:
        text = text.replace(a, b)
    return text


# ---------------- 术语校正表 ----------------

H264_FIX = [
    ("商编码", "熵编码"), ("伤编码", "熵编码"),
    ("红块", "宏块"),
    ("向速", "像素"), ("每个点多量", "每个点的亮度"), ("频款", "频率"),
    ("Cutback", "CABAC"),
    ("快效益", "块效应"), ("按快压", "按块压"), ("快与快", "块与块"),
    ("快的大小", "块的大小"), ("最大的快", "最大的块"), ("的快最大", "的块最大"),
    ("区块滤波", "去块滤波"),
    ("针", "帧"),
    ("运动时量", "运动矢量"),
    ("止泄", "纸屑"),
    ("造点", "噪点"),
    ("马律", "码率"),
    ("不够实", "不够时"),
    ("纹造", "噪点"),
    ("他们十二各做各的", "他们时而各做各的"), ("十二联手", "时而联手"),
    ("避震", "B帧"),
    ("DIVX", "DivX"), ("ATID", "Xvid"),
    ("VCE", "VC-1"),
    ("应节", "硬解"),
    ("HEDC", "HEVC"),
    ("Vellos", "Velos"), ("VLA", "Vela"),
    ("ONR", "On2"),
    ("司科", "思科"),
    ("Mazilla", "Mozilla"),
    ("AVE", "AV1"),
    ("AVR", "AV1"),
    ("连版税", "免版税"),
    ("代宽", "带宽"),
    ("全真内", "全帧内"),
    ("DNX", "DNxHR"),
    ("反拜尔", "去拜耳"),
    ("装饰品的盒子", "装视频的盒子（容器）"),
    ("MPV", "MKV"),
    ("AV一排第一", "AV1 排第一"),
    ("不明感", "不敏感"),
    ("长G,OP", "长GOP"), ("G,OP", "GOP"),
    ("拖进补调", "拖进剪辑软件"),
    ("H266", "H.266"), ("H265", "H.265"), ("H264", "H.264"),
    ("H263", "H.263"), ("H262", "H.262"), ("H261", "H.261"), ("H120", "H.120"),
    ("IOS11", "iOS 11"),
    ("ProResRAW", "ProRes RAW"), ("ProRes 422HQ", "ProRes 422 HQ"),
    ("BlackMagicRAW", "Blackmagic RAW"), ("NRAW", "N-RAW"),
    ("X-AVC-S", "XAVC-S"), ("X-AVC-HS", "XAVC-HS"), ("X-AVC-SI", "XAVC-SI"),
    ("TV3.0", "TV 3.0"),
    ("坦纳", "采纳"),
    ("4-10倍", "4–10 倍"),
]

BAYER_FIX = [
    ("拜尔滤镜", "拜耳滤镜"), ("拜尔", "拜耳"),
    ("反败尔", "反拜耳"), ("反败耳", "反拜耳"), ("败耳", "拜耳"),
    ("马滤", "码率"),
    ("归里", "硅里"),
    ("分三数", "分三束"),
    ("科达", "柯达"),
    ("尾色和姆尔纹", "伪色和摩尔纹"), ("姆尔纹", "摩尔纹"), ("母耳闻", "摩尔纹"),
    ("抄袭的细节", "细碎的细节"),
    ("另外2%的颜色", "另外三分之二的颜色"),
    ("丢掉了2%的颜色测量", "丢掉了2/3的颜色测量"),
    ("下彩样", "下采样"),
    ("Dyre", "拜耳"),
    ("世马", "适马"), ("Phobium", "Foveon"),
    ("砖的最深", "钻得最深"),
    ("撑近光亮多了四成", "进光量多了四成"),
    ("代价试算颜色更蓝", "代价是算颜色更难"),
    ("极数", "级数"),
    ("盛起来", "乘起来"),
    ("10.7一种", "10.7亿种"),
    ("卫生", "位深"),
    ("线线", "分辨率极限"),
    ("C2", "Cr"),
    ("绿目抠向", "绿幕抠像"),
    ("拉薄合度", "拉饱和度"),
    ("长距OP", "长GOP"),
    ("多痕", "多狠"),
    ("拍Roll", "拍RAW"),
    ("原眼其实不在乎", "人眼其实不在乎"),
    ("尼康G8", "尼康Z8"),
    ("422H2", "422 HQ"),
    ("High Log", "拍Log"),
    ("断层法更明显", "断层反而更明显"),
    ("就没那么明暗", "就没那么敏感"),
    # 色度抽样记号（先处理连写形式，再处理独立写法）
    ("4208比特", "4:2:0 8比特"), ("42210比特", "4:2:2 10比特"),
    ("44410比特", "4:4:4 10比特"), ("42010比特", "4:2:0 10比特"),
    ("4K420", "4K 4:2:0"), ("4K422", "4K 4:2:2"),
    ("444", "4:4:4"), ("422", "4:2:2"), ("420", "4:2:0"), ("411", "4:1:1"),
]

LOG_FIX = [
    ("懶", "懒"),
    ("完撰", "玩转"),
    ("Go加RAW", "JPEG加RAW"), ("GoPG", "JPEG"),
    ("吴操作", "误操作"),
    ("播信图", "波形图"),
    ("期赛", "期待"),
    ("RedLatin", "RED LUT"),
    ("东南范围", "动态范围"),
    ("A71C2", "A7C2"),
    ("C-Log3", "S-Log3"), ("C-Log", "S-Log"),
    ("CanonLog3", "Canon Log 3"), ("CanonLog2", "Canon Log 2"),
    ("N-Log2", "N-Log2"), ("N-Log", "N-Log"),
    ("F-Log2C", "F-Log2"), ("F-Log2", "F-Log2"), ("F-Log", "F-Log"),
    ("V-Log", "V-Log"),
    ("4,2,2,10比特", "4:2:2 10比特"),
    ("RedCode", "REDCODE"),
    ("Rog", "RAW"),
    ("Lot", "LUT"),
    ("王家位", "王家卫"),
    ("阿莱", "ARRI（阿莱）"),
]


def load_transcript(slug: str, key: str, fixes: list[tuple[str, str]], json_name: str | None = None):
    data = json.loads((WORK / key / (json_name or f"{slug}.json")).read_text(encoding="utf-8"))
    segs = [s for s in data.get("segments", []) if str(s.get("text", "")).strip()]
    out = []
    for s in segs:
        text = CC.convert(s["text"].strip())
        text = apply_fixes(text, fixes)
        out.append((ts(float(s["start"])), text))
    return out


# ---------------- 内容作者区 ----------------

ARTICLES = {}

ARTICLES["h264-h265-av1-video-codecs"] = {
    "key": "b70d",
    "title": "H.264、H.265、AV1 到底差在哪？讲透视频压缩",
    "url": "https://xhslink.cn/o/vrlJMDmovO",
    "duration": "13分15秒",
    "uploader": "克劳德知识科普",
    "primary": "photo",
    "tags": ["摄影", "视频技术", "原理"],
    "bound": "影像技术科普；码率、编码参数与行业调查数据为视频作者口径，具体机型参数以相机说明书为准。",
    "pitfall": "口播含较多专业同音词，已按语境校正（如熵编码、运动矢量、HEVC、AV1、On2、思科、Mozilla 等）；个别口误以原视频为准。",
    "summary": "讲透视频压缩原理与 H.264/H.265/AV1 三代标准：四种冗余如何被压缩、单帧五步流水线、40 年标准演进（每 10 年码率减半），以及拍摄/剪辑/导出/存档该选哪个编码。",
    "takeaway": "视频压缩本质是用算力换带宽。选格式不只看压缩率，更要看硬件解码与专利是否清楚：H.264 兼容最稳、H.265/AV1 更省流量、剪辑用 ProRes/全帧内、存档留高码率原素材。",
    "chapters": [
        {
            "id": "ch1", "time": "00:00–05:04",
            "title": "压缩原理：四种冗余 + 单帧五步流水线",
            "blurb": "视频能被压缩，靠的是空间、时间、视觉、统计四种重复；单帧压缩从 1988 年至今都是切块→预测→变换→量化→熵编码五步。",
            "body": "视频之所以能压上百倍，是因为里面全是重复：空间重复（蓝天相邻像素几乎一样）、时间重复（相邻帧大部分没变）、视觉冗余（人眼对细纹理不敏感）、统计重复（常见数字用短编码）。压缩分无损与有损，视频几乎都用有损，主动丢掉信息换压缩比。单帧编码从 1988 年至今都是五步：切块（H.264 基本单位是 16×16 宏块，新格式最大 128×128）→ 预测（按方向猜这一块，只存残差，H.264 有 9 种方向、H.265 35 种、H.266 67 种）→ 变换（离散余弦变换，把像素转成频率描述）→ 量化（真正丢信息的一步，码率高低主要调这里）→ 熵编码（H.264 引入 CABAC 能再省约 10%）。更大的压缩来自时间：编码器在上一帧找最像的位置只存一个运动矢量，帧分 I/P/B 三种，从 I 帧到下一个 I 帧为一组 GOP——这也是长 GOP 素材拖进剪辑软件会卡的原因。码率分配有固定码率、可变码率、恒定画质（CRF）三种。",
            "shots": [
                ("00:10", "开场：一部 2 小时的 4K 电影不压缩要 2.15TB，按流媒体 15Mbps 只要 13.5GB，小了约 160 倍", "A 2-hour 4K movie shrinks ~160× when compressed"),
                ("00:46", "四种重复之一：空间重复——一片蓝天的相邻像素几乎一样，没必要每个都存", "Spatial redundancy: adjacent pixels in a blue sky are nearly identical"),
                ("01:47", "单帧五步第一步「切块」：H.264 的基本单位是 16×16 宏块", "Step 1 partitioning: H.264's basic unit is the 16×16 macroblock"),
                ("02:36", "第四步「量化」：真正丢信息的一步，码率高低主要调这里", "Step 4 quantization: where data is actually dropped"),
                ("03:30", "帧分三种：I 帧只靠自己、P 帧参考前帧、B 帧参考前后，体积依次最小", "I/P/B frames: reference themselves, the previous, or both neighbours"),
            ],
        },
        {
            "id": "ch2", "time": "05:04–09:32",
            "title": "40 年标准演进：从 H.120 到 AV1/VVC/AVS3",
            "blurb": "标准由 ITU 与 MPEG 两个组织制定；从 H.120、H.261、MPEG-1/2 到 H.264 称霸，再到 H.265 专利混乱逼出免版税的 AV1。",
            "body": "标准由国际电联 ITU（管通信）与国际标准化组织 MPEG（管媒体）制定，时而各自为政、时而联手。1984 年 H.120 几乎不能用；1988 年 H.261 为视频会议而生，奠定切块+运动补偿+变换编码的骨架；MPEG-1 加入 B 帧成就 VCD；MPEG-2（H.262）撑起 DVD 与数字电视。2003 年 H.264（AVC）以一半码率称霸，靠的是生态与集中在单一专利池的收费。2013 年 H.265（HEVC）更省一半，但专利分散在三个池、算不清该交谁；这直接逼出 2015 年开放媒体联盟与 2018 年免版税的 AV1（块更大、可分离胶片颗粒），比 H.265 再省 10–20%。其后还有 H.266/VVC、2026 年发布的 AV2，以及中国的 AVS3。",
            "shots": [
                ("05:12", "1988 年 H.261 是第一个能用的标准，为视频会议而生，骨架沿用至今", "H.261 (1988), the first usable standard, built for video conferencing"),
                ("06:35", "2013 年 H.265（HEVC）最大的块从 16 涨到 64，预测方向增加到 35 种", "H.265/HEVC: blocks grew to 64, prediction directions to 35"),
                ("07:54", "2018 年免版税的 AV1：块最大 128×128，胶片颗粒可分离后合成", "Royalty-free AV1 (2018): 128×128 blocks and separable film grain"),
            ],
        },
        {
            "id": "ch3", "time": "09:37–13:15",
            "title": "现实怎么选：发布 / 剪辑 / RAW 三类编码",
            "blurb": "拍视频的编码分发布、剪辑、RAW 三类；MP4/MOV/MKV 只是容器。2026 年调查里 H.264 仍占 85%，未来最想用的是 AV1。",
            "body": "拍视频的编码分三类：发布用（H.264/H.265，省空间但剪辑吃力）、剪辑用（ProRes、DNxHR，全帧内好剪但文件大）、RAW（N-RAW、ProRes RAW、Blackmagic RAW、REDCODE，压的是传感器原始数据）。MP4/MOV/MKV 只是容器，换容器不损画质。2026 年行业调查：生产环境 H.264 85%、H.265 58%、AV1 19%、H.266 5%，而未来一年最想采用的是 AV1（35%）。选型建议：拍摄空间够就选高码率、重度调色选 10bit；剪辑卡就转 ProRes 或生成代理；导出 H.264 兼容最稳、H.265 文件更小；上传前给高质量原文件；存档留原素材——每压缩一次就多丢一点。四十年都在回答同一个问题：哪些信息可以不存，哪些信息可以用算的。",
            "shots": [
                ("09:48", "主要格式对照表：发布年份 / 相对效率 / 编码复杂度 / 专利 / 主要用途", "Codec comparison table: year, efficiency, complexity, patents, use cases"),
                ("12:14", "选型建议：拍摄 / 剪辑 / 导出 / 存档各该用什么编码", "Choosing a codec by use case: capture, edit, export, archive"),
            ],
        },
    ],
    "svg": """
<div class="container">
  <h1>H.264 / H.265 / AV1：选编码不只看压缩率</h1>
  <div><span class="tag">视频压缩</span><span class="tag">编码标准</span><span class="tag">选型</span></div>
  <p class="summary-line">视频压缩的本质是用算力换带宽；一个新格式能不能普及，技术只是一半，硬件解码与专利是否说得清才是另一半。</p>
  <div class="card"><h3>核心机制：四种冗余 + 五步流水线</h3>
  <p>空间重复、时间重复、视觉冗余、统计重复是可压缩的来源；单帧走「切块→预测→变换→量化→熵编码」，量化是真正丢信息的环节。</p>
  <div class="relation">帧间压缩更猛：运动矢量 + I/P/B 帧 + GOP，代价是长 GOP 素材剪辑卡顿。</div></div>
  <div class="card card-purple"><h3>三代标准的取舍（作者观点）</h3>
  <p>H.264 胜在生态与集中专利池；H.265 更省但专利分散三池，算不清交谁；这逼出免版税的 AV1。AV1 比 H.265 省 10–20%，但编码慢 4–10 倍。</p></div>
  <div class="card"><h3>三类编码用途</h3><table>
  <tr><th>类型</th><th>代表</th><th>特点</th><th>适用</th></tr>
  <tr><td>发布用</td><td>H.264 / H.265</td><td>省空间、剪辑吃力</td><td>成片、上传</td></tr>
  <tr><td>剪辑用</td><td>ProRes / DNxHR</td><td>全帧内、好剪、文件大</td><td>剪辑中间格式</td></tr>
  <tr><td>RAW</td><td>N-RAW / ProRes RAW / BRAW / REDCODE</td><td>传感器原始数据</td><td>重度后期</td></tr>
  </table></div>
  <div class="card card-orange"><h3>避坑</h3><div class="pitfall">免版税≠零风险（杜比已就 AV1/H.265 起诉 Snap）；MP4/MOV/MKV 只是容器，换容器不损画质。</div></div>
  <div class="conclusion"><h2>结论与行动</h2>
  <p>拍摄空间够选高码率、重度调色选 10bit；剪辑卡转 ProRes 或生成代理；导出 H.264 兜底、H.265 省流量；存档留高码率原素材——每压缩一次就多丢一点。</p></div>
</div>""",
}

ARTICLES["bayer-filter-and-10bit422"] = {
    "key": "b70c",
    "title": "拜耳滤镜和10bit422都是什么？这期详解",
    "url": "https://xhslink.cn/o/1TqHWSh198d",
    "duration": "13分13秒",
    "uploader": "克劳德知识科普",
    "primary": "photo",
    "tags": ["摄影", "相机", "原理"],
    "bound": "相机科普；机型参数（Z8/A7M5、码率档位）为视频作者口径，以说明书为准。",
    "pitfall": "口播含较多专业同音词，已按语境校正（拜耳、码率、反拜耳、摩尔纹、适马 Foveon、位深、长 GOP 等）；个别口误以原视频为准。",
    "summary": "从一粒光子到一个视频文件：拜耳滤镜为何只测 1/3 颜色、8bit/10bit 的位深差别、4:2:2/4:2:0 色度抽样怎么省数据，以及拍 Log、抠像、直出各该选什么。",
    "takeaway": "拜耳滤镜丢掉 2/3 颜色测量、色度抽样又丢掉一半、压缩再丢几十倍，但画面几乎不变——因为人眼不在乎这些。选参数按用途：直出 4:2:0 8bit 够，拍 Log 先保 10bit，抠像/大调色再上 4:2:2 并开高码率。",
    "chapters": [
        {
            "id": "ch1", "time": "00:00–03:34",
            "title": "传感器怎么拿到颜色：拜耳滤镜与反拜耳",
            "blurb": "传感器天生色盲，拜耳滤镜让每个格子只放一种颜色，其余 2/3 颜色靠邻居猜出来（反拜耳）。",
            "body": "相机菜单里那串「4K、10bit、4:2:2、100M」背后有几件反常的事：一段 4K 4:2:2 10bit 视频不压缩要每秒约 4000Mbps，相机只存 100Mbps，少了近 40 倍。要从传感器到文件，共四步：拿颜色、定位深、留色度、压缩。传感器本身是色盲——红光和蓝光打出的电子一模一样，只知道来多少光。最直接的办法是用棱镜分三束给三块传感器（老式广播机），但体积大成本高。1976 年柯达工程师布莱斯·拜耳拿到专利：一块传感器、每格盖一片滤镜，一格只放一种颜色（两行两列一组：一红两绿一蓝，绿占一半）。绿色最多是因为人眼对明暗的感受主要来自绿，视频标准算亮度时绿占 72%。反拜耳（去马赛克）就是把每格缺的两种颜色靠邻居猜回来；简单平均法在边缘会出错，好算法会先重建最密的绿、判断边缘方向再猜。猜错就出现伪色和摩尔纹，传统用低通滤镜压糊细节来换，代价是锐度下降。",
            "shots": [
                ("00:13", "相机录像菜单里那串字：4K、10bit、4:2:2、100M，背后有几件反常的事", "The camera menu string: 4K, 10-bit, 4:2:2, 100M"),
                ("01:36", "拜耳滤镜：每个格子只放一种颜色，一红两绿一蓝为一组", "The Bayer filter: each pixel captures only one colour"),
                ("02:24", "反拜耳（去马赛克）：每格缺的两种颜色靠周围邻居猜出来", "Demosaicing: the two missing colours are guessed from neighbours"),
            ],
        },
        {
            "id": "ch2", "time": "03:34–06:52",
            "title": "8bit 与 10bit：位深是台阶，不是楼高",
            "blurb": "位深决定「楼梯分多少级」，动态范围决定「楼有多高」，两回事。拍 Log 必须 10bit，否则断层。",
            "body": "反拜耳后每个像素有了红绿蓝三个数，要决定用多少位存——位就是二进制的 0/1，每多一位能表示的级数翻倍：8bit 256 级、10bit 1024 级、14bit 16384 级。把最暗到最亮想成楼梯，位深是台阶数，动态范围是楼高，两回事。视频标准里亮度没被用满：8bit 用 16–235（约 220 级）、10bit 用 64–940（约 877 级），两端留给超黑超白。台阶太粗就会在天空这种缓变处出现色带（断层）；拍 Log 把十几档亮度塞进同一范围，每档分到的台阶更少，所以 Log 一定要 10bit。有意思的是噪点反而打散台阶边界、让眼睛看不出色带，所以降噪/压缩太狠时断层反而更明显。10bit 大多不是给观众看的（很多显示器只 8bit、平台也基本 8bit），真正的价值是给调色留空间。",
            "shots": [
                ("03:38", "拜耳之外还有别的排法：富士 X-Trans、适马 Foveon、华为 RYYB、四合一", "Other layouts: X-Trans, Foveon, RYYB, quad-bayer"),
                ("04:50", "8bit 是 256 级、10bit 是 1024 级：位深决定楼梯分多少级", "8-bit = 256 levels, 10-bit = 1024 levels"),
                ("05:57", "天空缓变处出现色带（断层）：台阶太粗的后果", "Banding in a smooth sky: the cost of coarse steps"),
            ],
        },
        {
            "id": "ch3", "time": "06:52–13:13",
            "title": "4:2:2 / 4:2:0 色度抽样与最后怎么选",
            "blurb": "人眼看细节靠明暗不靠颜色，所以色度可以少存。4:2:0 颜色只有 1080p，但人眼几乎看不出。",
            "body": "工程师利用人眼弱点：看细节主要靠明暗，颜色细节不敏感（颜色条纹分辨约每度 11–12 线对）。视频不直接存红绿蓝，而是换算成亮度 Y 和两个色差 Cb、Cr；把色差缩一半再放大，几乎看不出区别——这就是色度抽样。常见有 4:4:4、4:2:2、4:2:0、4:1:1 四种（三个数字描述一个 4×2 小块里保留多少颜色）。4K 视频亮度永远是 3840×2160，但 4:2:0 的颜色只有 1920×1080——明暗是 4K、颜色只是 1080p。能看出差别的是绿幕抠像、大幅调色、纯红纯蓝细小文字。把位深和色度放到一起算：4:2:0 8bit 每像素 12 位、4:2:2 10bit 20 位、4:4:4 10bit 30 位，乘 4K 的 829 万像素再乘 24fps，4:2:2 10bit 约每秒 4 千兆比特。相机实际 100M/240M 档位，分别压了约 40 倍和 17 倍。压缩分全帧内（码率高好剪）与长 GOP（省空间剪辑吃力）。422 是留多少信息、码率是压得多狠，两回事——同样码率下 4:2:2 要多包 1/3 数据，码率跟不上反而不划算。最后怎么选：直出不调色用 4:2:0 8bit 够；拍 Log 要调色必须 10bit；抠绿幕或大调色用 4:2:2 并开高码率；要最大后期空间拍 RAW。拍 Log 时优先级：先保 10bit，再保码率，最后才是 4:2:2。",
            "shots": [
                ("07:54", "色度抽样：把色差缩小一半再放大回去，和亮度合起来几乎看不出区别", "Chroma subsampling: halve the chroma and you can barely tell"),
                ("09:13", "4K 的亮度是 3840×2160，但 4:2:0 的颜色只有 1920×1080", "4K luma is 3840×2160, but 4:2:0 chroma is only 1920×1080"),
                ("10:17", "A7M5 的 4K 24p 4:2:2 10bit 有 100M 与 240M 全帧内两档", "A7M5: 4K 24p 4:2:2 10-bit in 100M and 240M all-intra"),
                ("12:17", "选型建议：直出 / 拍 Log / 抠像 / 大后期各该用什么参数", "Choosing parameters: straight-out, Log, keying, or heavy grade"),
            ],
        },
    ],
    "svg": """
<div class="container">
  <h1>拜耳滤镜 · 位深 · 色度抽样：一串参数的来龙去脉</h1>
  <div><span class="tag">相机科普</span><span class="tag">传感器原理</span><span class="tag">色度抽样</span></div>
  <p class="summary-line">从一粒光子到一个视频文件，拜耳滤镜丢掉 2/3 颜色测量、色度抽样再丢掉一半、压缩再丢几十倍，但画面几乎不变——因为人眼不在乎这些。</p>
  <div class="card"><h3>四步链路</h3>
  <p>传感器拿颜色（拜耳滤镜）→ 定多少位存（位深）→ 留多少颜色（色度抽样）→ 怎么压缩（码率）。每一步都在问「哪些信息人眼其实不在乎」。</p></div>
  <div class="card card-purple"><h3>三个常被混淆的概念</h3>
  <p>位深 ≠ 动态范围：位深是楼梯分多少级，动态范围是楼有多高。4:2:2 ≠ 高码率：4:2:2 是留多少信息，码率是压得多狠。RAW 谈不上 4:2:2：它存的是反拜耳前的原始读数。</p></div>
  <div class="card"><h3>选型对照</h3><table>
  <tr><th>场景</th><th>建议</th><th>原因</th></tr>
  <tr><td>直出不调色</td><td>4:2:0 8bit</td><td>人眼/平台都够用</td></tr>
  <tr><td>拍 Log 要调色</td><td>必须 10bit</td><td>Log 压缩台阶，8bit 会断层</td></tr>
  <tr><td>绿幕抠像/大调色</td><td>4:2:2 + 高码率</td><td>色度细、余量足</td></tr>
  <tr><td>最大后期空间</td><td>RAW</td><td>原始读数，代价是存储/剪辑压力</td></tr>
  </table></div>
  <div class="card card-orange"><h3>避坑</h3><div class="pitfall">4K 4:2:0 缩成 1080p 会变成 4:4:4，但不会变 10bit；10bit 不是给观众看的，是给调色留空间。</div></div>
  <div class="conclusion"><h2>结论与行动</h2>
  <p>拍 Log 优先级：先保 10bit，再保码率，最后才是 4:2:2。同一码率下 4:2:2 反而更挤，码率跟不上别硬上。</p></div>
</div>""",
}

ARTICLES["billiards-infinite-table-max-hits"] = {
    "key": "b70b",
    "title": "假如球桌无限长，一杆最多能连撞几颗球？",
    "url": "https://xhslink.cn/o/7y6lMDYyr6D",
    "duration": "1分34秒",
    "uploader": "真和理",
    "primary": "sports",
    "tags": ["台球", "物理", "趣味"],
    "bound": "理想化物理模型（忽略摩擦、滚动衰减）；实战受台呢摩擦、出杆误差与球体碰撞非理想因素影响。",
    "pitfall": "本条为音乐 + 画面大字动画，无口播；要点来自作品描述与画面大字，细节以原笔记为准。",
    "summary": "一个理想化台球问题：无限长球桌、每两颗球之间空十个球身，一杆最多连撞几颗？答案不在手稳，而在误差每撞一次放大 10 倍。",
    "takeaway": "出杆只偏半毫米，撞过一颗就偏 5 毫米，每撞一次偏差放大 10 倍；偏差超过一个球身就碰不到下一颗。所以每想多撞一颗，就得再准 10 倍。",
    "chapters": [
        {
            "id": "ch1", "time": "00:00–00:34",
            "title": "问题设定：无限长球桌与一杆连撞",
            "blurb": "一张无限长的球桌，球一颗接一颗摆下去，每两颗之间空十个球身——一杆最多能连着撞到第几颗？",
            "body": "这是一道理想化的物理趣味题：假如球桌无限长，球一颗接一颗摆下去，每两颗之间空着十个球身的距离。一杆下去，球撞球、球再撞球，最多能连着撞到第几颗？作者先给了一个反直觉的提示：答案和手稳不稳关系不大。",
            "shots": [
                ("00:00", "无限长球桌：球一颗接一颗摆下去，每两颗之间空十个球身", "An infinitely long table with balls spaced ten ball-widths apart"),
                ("00:11", "问题：一杆下去，球撞球、球再撞球，最多连撞到第几颗？", "How many balls can one shot chain into?"),
            ],
        },
        {
            "id": "ch2", "time": "00:35–01:09",
            "title": "关键：每次碰撞误差放大 10 倍",
            "blurb": "出杆只偏半毫米，被撞球方向就歪；滚过十个球身到下一颗已偏 5 毫米，每撞一次偏差放大 10 倍。",
            "body": "先看一次碰撞：出杆只偏半毫米，被撞的球方向就歪了一点。它再滚过十个球身的距离，到下一颗跟前时已经偏了 5 毫米。每撞一次，偏差放大 10 倍；一旦偏差超过一个球身，下一颗就碰不到了。这就是为什么「手稳不稳关系不大」——误差是指数级累积的，不是靠手感能压住的。",
            "shots": [
                ("00:35", "一次碰撞：出杆只偏半毫米，方向就歪一点，滚十个球身已偏 5 毫米", "Half a millimetre of error becomes 5 mm after ten ball-widths"),
                ("00:46", "每撞一次，偏差放大 10 倍", "Each collision multiplies the error by 10"),
            ],
        },
        {
            "id": "ch3", "time": "01:10–01:34",
            "title": "结论：每多撞一颗，就得再准 10 倍",
            "blurb": "偏差超过一个球身就断链，所以每想多撞一颗，都得把出杆精度再提高 10 倍。",
            "body": "偏差超过一个球身，链条就断。所以每想多撞一颗，出杆就得再准 10 倍。结尾「世界冠军」的画面大字点出：即便是顶尖选手，在这个指数放大的模型里也撞不了几颗。",
            "shots": [
                ("01:10", "所以每想多撞一颗，就得再准 10 倍", "Each extra ball demands 10× more precision"),
                ("01:22", "结尾画面大字「世界冠军」：即便顶尖选手也撞不了几颗", "Closing title 'world champion': even pros can't chain many"),
            ],
        },
    ],
    "transcript": [
        ("00:00", "假如有一张无限长的球桌，球一颗接一颗摆下去，每两颗之间空着十个球身。"),
        ("00:11", "一杆下去，球撞球、球再撞球——最多能连着撞到第几颗？"),
        ("00:23", "答案和手稳不稳关系不大。"),
        ("00:35", "先看一次碰撞：出杆只偏半毫米，被撞的球方向就歪了一点。"),
        ("00:46", "它再滚过十个球身，到下一颗跟前，已经偏了 5 毫米。"),
        ("00:58", "每撞一次，偏差放大 10 倍。偏差超过一个球身，下一颗就碰不到了。"),
        ("01:10", "所以每想多撞一颗，就得再准 10 倍。"),
        ("01:22", "世界冠军。"),
    ],
    "svg": """
<div class="container">
  <h1>无限长球桌：误差如何指数放大</h1>
  <div><span class="tag">台球</span><span class="tag">物理</span><span class="tag">趣味</span></div>
  <p class="summary-line">一杆最多能连撞几颗球，答案不在手稳，而在误差每撞一次放大 10 倍——超过一个球身就断链。</p>
  <div class="card"><h3>核心机制</h3>
  <p>出杆偏半毫米 → 被撞球方向歪一点 → 滚过十个球身到下一颗已偏 5 毫米 → 每撞一次偏差×10 → 偏差超过一个球身即断。</p>
  <div class="relation">误差是指数累积，不是靠手感能线性修正的。</div></div>
  <div class="card card-purple"><h3>反直觉之处</h3>
  <p>「手稳不稳关系不大」——因为在指数放大面前，再多练习也只能多撞有限的几颗。</p></div>
  <div class="card card-orange"><h3>边界</h3><div class="pitfall">理想化模型，忽略摩擦、滚动衰减与非理想碰撞；实战台呢摩擦会让偏差衰减更快。</div></div>
  <div class="conclusion"><h2>结论</h2><p>每想多撞一颗，就得再准 10 倍；所以「一杆清台」式的无限连撞，在这个模型里本就不存在。</p></div>
</div>""",
}

ARTICLES["why-shoot-log-grey"] = {
    "key": "b70a",
    "json_name": "why-shoot-log-grey.full.json",
    "title": "05从零玩转视频创作 为什么要开Log拍灰片",
    "url": "https://xhslink.cn/o/17qneAzhyQK",
    "duration": "8分52秒",
    "uploader": "摄影高老师",
    "primary": "photo",
    "tags": ["摄影", "视频技术", "原理"],
    "bound": "影像技术科普；各家 Log 名称、机型（A7C2 等）与后期流程为视频作者口径，以说明书与实机为准。",
    "pitfall": "口播含同音错字已按语境校正（波形图、误操作、玩转、JPEG、S-Log3 等）；作者口误把索尼 S-Log3 说成 C-Log3（C-Log 是佳能），正文按 S-Log3 校正。",
    "summary": "为什么拍视频要开 Log 拍灰片：用 JPEG 与 RAW 的类比讲清「灰片≈视频版 RAW」的道理，实拍对比直方图与波形图的区别，再梳理索尼/佳能/尼康/富士/松下各家 Log。",
    "takeaway": "开 Log 拍灰片≈拍视频版 RAW：把高光压低、阴影提亮集中到中灰区，配合 4:2:2 10bit 保留最大后期空间。后期别怕调：有大量第三方电影感还原 LUT（ARRI/RED/柯达 2383）拖进去就能用。",
    "chapters": [
        {
            "id": "ch1", "time": "00:00–02:27",
            "title": "为什么开 Log：JPEG 与 RAW 的类比",
            "blurb": "拍照片时 JPEG 8bit 后期空间小、RAW 14bit 动态范围大；拍视频开 Log 拍灰片，相当于拍「视频版 RAW」。",
            "body": "作者先用照片举例：拍照片选「JPEG+RAW」时，回放看到的是讨喜的 JPEG，但真要精细调整一定会去调 RAW——JPEG 是 8bit，色彩与明暗宽容度后期已经很小；RAW 是 14bit，有 14–15 档动态范围，后期空间大。把同样的逻辑搬到视频上：开 Log 拍灰片，就相当于拍「RAW 格式的视频」，后期拥有更大的调整空间。作者还主动回应「灰片不是 RAW」的质疑：正儿八经的 4K/8K RAW 视频内录才是真 RAW，但 RAW 后期流程更麻烦，而开 Log 的调色流程相对固定、简单、门槛更低，所以用这个比喻帮助理解。",
            "shots": [
                ("00:14", "开 Log 拍灰片，相当于拍「RAW 格式的视频」", "Shooting Log is like shooting RAW video"),
                ("00:57", "JPEG 8bit vs RAW 14bit：后期空间差在哪", "JPEG 8-bit vs RAW 14-bit: the editing headroom gap"),
            ],
        },
        {
            "id": "ch2", "time": "02:28–05:25",
            "title": "实拍对比：误拍的 JPEG 视频 vs 开 Log 灰片",
            "blurb": "带娃玩水时先误拍了一段 JPEG 风格视频（波形图顶天立地、明暗到极限），切 Log 重拍后波形图集中在中间、层次全保留。",
            "body": "上周末带娃玩水，先是在拍照模式下误拍了一段视频：成像风格和 JPEG 照片差不多，饱和度反差都到位，但看波形图，明暗反差已经顶天立地——最高光顶到 100、最低端贴到 0，意味着后期几乎没有调整空间，最亮处信息已经缺失。意识到误操作后立刻切到视频模式开 Log 重拍：波形图所有明暗信息集中在中央，既没顶到头也没压到底，往上提亮、往下压暗都有大量空间，动态范围和明暗层次保留得非常到位。作者现场示意调色：加一点对比度、调整曝光倾向和色温，灰片就能调出远好于直出的层次感。",
            "shots": [
                ("02:28", "误拍片段：JPEG 风格、波形图顶天立地，后期没空间", "The accidental shot: clipped waveform, no headroom"),
                ("03:15", "开 Log 重拍：波形图集中在中间，明暗层次全保留", "Log retake: waveform centred, full tonal range kept"),
            ],
        },
        {
            "id": "ch3", "time": "05:26–08:52",
            "title": "各家 Log 与为什么灰片是折中方案",
            "blurb": "索尼 S-Log3、佳能 Canon Log、尼康 N-Log、富士 F-Log2、松下 V-Log；开 Log 是高光压低、阴影提亮的折中，配合 4:2:2 10bit 保后期空间。",
            "body": "作者用的是索尼 A7C2，索尼家是 S-Log3，动态范围大、后期空间大；佳能有 Canon Log 3/2、尼康有 N-Log（配 RED LUT 可用性也高）、富士有 F-Log2、松下 V-Log。为什么拍出来灰不拉几：开 Log 不套 LUT 时回放就灰蒙蒙、没色彩，是因为它把高光往下压、阴影往上提，集中在中灰区域，更好地记录明暗层次。为什么要这么折中：拍照片 RAW 单张体积就大，视频每秒 25 张 RAW 体积太恐怖，开 Log 就是折中方案——通常拍 4:2:2 10bit，色彩记录空间比 8bit 大得多，动态范围又高、色彩又丰富。所以作者强烈建议拍视频开 Log。面对「后期还得调」的头疼，作者反过来劝：创作视频本来就要走这个流程，又想好、又想简单、又想一键出片，哪那么好的事；而且开 Log 后期反而更简单——有大量第三方电影感还原 LUT（ARRI、RED、柯达 2383 等），拖进去就能用（当然还要微调）。灰片怎么还原成正常模式、如何赋予电影化风格，作者说后续会详细分享。",
            "shots": [
                ("04:50", "作者用索尼 A7C2，索尼家是 S-Log3", "The author shoots Sony A7C2 with S-Log3"),
                ("05:26", "各家 Log：佳能 Canon Log、尼康 N-Log、富士 F-Log2、松下 V-Log", "Log flavours: Canon Log, N-Log, F-Log2, V-Log"),
                ("06:30", "开 Log = 高光压低、阴影提亮，集中到中灰区的折中方案", "Log: crush highlights, lift shadows into mid-grey"),
                ("07:11", "拍视频强烈建议开 Log，换取最广的后期空间", "Shoot Log for the widest grading headroom"),
            ],
        },
    ],
    "svg": """
<div class="container">
  <h1>为什么要开 Log 拍灰片：视频版的 RAW</h1>
  <div><span class="tag">视频拍摄</span><span class="tag">Log</span><span class="tag">灰片</span></div>
  <p class="summary-line">开 Log 拍灰片，相当于拍「RAW 格式的视频」：把高光压低、阴影提亮集中到中灰区，配 4:2:2 10bit 保留最大后期空间。</p>
  <div class="card"><h3>照片的启示</h3>
  <p>JPEG 是 8bit、后期空间小；RAW 是 14bit、14–15 档动态范围。视频同理：直出（JPEG 风格）波形图顶天立地，开 Log（RAW 风格）波形图集中在中间。</p>
  <div class="relation">波形图顶到 100 或贴到 0 = 明暗信息已丢；集中在中间 = 上下都有余量。</div></div>
  <div class="card card-purple"><h3>作者澄清</h3>
  <p>灰片不是真 RAW（4K/8K RAW 内录才是），但开 Log 的调色流程更简单、门槛更低，所以用这个比喻。</p></div>
  <div class="card"><h3>各家 Log</h3><table>
  <tr><th>品牌</th><th>Log</th></tr>
  <tr><td>索尼</td><td>S-Log3</td></tr>
  <tr><td>佳能</td><td>Canon Log 3 / Log 2</td></tr>
  <tr><td>尼康</td><td>N-Log</td></tr>
  <tr><td>富士</td><td>F-Log2</td></tr>
  <tr><td>松下</td><td>V-Log</td></tr>
  </table></div>
  <div class="card card-orange"><h3>边界</h3><div class="pitfall">开 Log 要配合后期（不套 LUT 回放就是灰蒙蒙）；通常拍 4:2:2 10bit，比 8bit 色彩空间大得多。</div></div>
  <div class="conclusion"><h2>结论</h2><p>拍视频强烈建议开 Log：动态范围高、色彩丰富、后期空间最大；头疼后期的话，先记住「灰片要调」，具体流程后续有专门教程。</p></div>
</div>""",
}

# ---------------- 生成逻辑 ----------------

CAPTION_AUDIO_DIR = ROOT / "docs" / "audio"


def extract_frames(slug: str, key: str, shots: list[tuple[str, str, str]]) -> None:
    mp4 = WORK / key / f"{slug}.source.mp4"
    assets = ROOT / "docs" / "assets" / slug
    assets.mkdir(parents=True, exist_ok=True)
    for i, (tlabel, _zh, _en) in enumerate(shots, 1):
        secs = to_sec(tlabel)
        out = assets / f"shot-{i:02d}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(secs), "-i", str(mp4),
             "-frames:v", "1", "-vf", "scale='min(1280,iw)':-2", "-q:v", "2", str(out)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )


def build_html(art: dict, slug: str, transcript: list[tuple[str, str]]) -> None:
    toc = "\n".join(
        f'<a href="#{c["id"]}">{esc(c["title"])}</a>' for c in art["chapters"]
    ) + '\n<a href="#transcript">口述/画面要点</a>'

    rows = "".join(
        f'<div class="summary-row"><span class="time-marker">[{esc(c["time"])}]</span>'
        f'<div><strong>{esc(c["title"])}</strong><p>{esc(c["blurb"])}</p></div></div>\n'
        for c in art["chapters"]
    )

    sections = []
    shot_i = 0
    for c in art["chapters"]:
        figs = []
        for tlabel, zh, en in c["shots"]:
            shot_i += 1
            figs.append(
                f'<figure><img src="assets/{slug}/shot-{shot_i:02d}.jpg" alt="{esc(zh)}" loading="lazy">'
                f'<figcaption>[{esc(tlabel)}] {esc(zh)}</figcaption></figure>'
            )
        sections.append(
            f'<section class="story-section" id="{c["id"]}">'
            f'<h2><span class="time-marker">{esc(c["time"])}</span>{esc(c["title"])}</h2>'
            f'<p>{esc(c["body"])}</p>{"".join(figs)}</section>'
        )

    tr_rows = "".join(
        f'<div class="transcript-row"><time>{esc(t)}</time><p>{esc(text)}</p></div>\n'
        for t, text in transcript
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{esc(art['summary'])}">
<title>{esc(art['title'])}｜图文实录</title>
<style>{HTML_CSS}</style>
</head>
<body><main class="container">
<header>
  <h1>{esc(art['title'])}</h1>
  <div class="meta-row">
    <span class="meta-tag tag-platform">小红书</span>
    <span class="meta-tag tag-duration">{esc(art['duration'])}</span>
    <span class="meta-tag tag-topic">{esc(' · '.join(art['tags'][:3]))}</span>
  </div>
  <a class="source-link" href="{esc(art['url'])}" target="_blank" rel="noopener">→ 原视频链接</a>
</header>
<nav class="toc"><h3>内容导航</h3>
{toc}
</nav>
<article>
<div class="content-points">
  <h2>内容要点</h2>
  <p>{esc(art['summary'])}</p>
  <h3>知识结构</h3>
  {rows}
  <div class="takeaway-box"><strong>总结</strong><p>{esc(art['takeaway'])}</p></div>
  <div class="bound"><strong>适用边界</strong>：{esc(art['bound'])}</div>
  <div class="pitfall"><strong>踩坑</strong>：{esc(art['pitfall'])}</div>
</div>
{"".join(sections)}
<section class="transcript-section" id="transcript">
<details class="transcript-collapsible"><summary>口述/画面要点（{len(transcript)}段）</summary>
<div class="transcript-body">
<p class="transcript-note">结合 Whisper medium 转录与画面大字整理；专有名词与同音错字已按语境校正，个别口误以原视频为准。</p>
<div class="transcript-list">{tr_rows}</div>
</div></details></section>
</article></main>
<script>(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",open)}});if(location.hash==="#transcript")open()}})();</script>
</body></html>
"""
    (ROOT / "docs" / f"{slug}-图文实录.html").write_text(html, encoding="utf-8")


def build_svg_file(art: dict, slug: str) -> int:
    script = WORK / f"build-{slug}-svg.mjs"
    script.write_text(
        "\nimport { writeFileSync } from 'fs';\n"
        "import { buildSvg } from '../../svg-auto-height.mjs';\n"
        f"const css = {json.dumps(SVG_CSS)}\n"
        f"const body = {json.dumps(art['svg'])}\n"
        "const { svg, height } = await buildSvg({ css, body, width: 1320 });\n"
        f"writeFileSync({json.dumps(str(ROOT / 'docs' / f'{slug}-理性分析.svg'))}, svg);\n"
        "console.log('svg_height', height);\n",
        encoding="utf-8",
    )
    out = subprocess.check_output(["node", str(script)], cwd=str(ROOT), text=True)
    return int(out.strip().split()[-1])


def update_translations(art: dict, slug: str) -> None:
    tr_path = ROOT / "translations.json"
    tr = json.loads(tr_path.read_text(encoding="utf-8"))
    for c in art["chapters"]:
        for _tlabel, zh, en in c["shots"]:
            tr[zh] = en
    tr_path.write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_index(art: dict, slug: str, transcript_n: int, svg_h: int) -> None:
    idx_path = ROOT / "docs" / "index.json"
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    shot_count = sum(len(c["shots"]) for c in art["chapters"])
    for e in data:
        if e.get("slug") == slug or e.get("outputs", {}).get("html") == f"{slug}-图文实录.html":
            e["summary"] = art["summary"]
            e["title"] = art["title"]
            e["tags"] = art["tags"]
            e["duration"] = art["duration"]
            e["screenshot_count"] = shot_count
            e["transcript_segments"] = transcript_n
            e["svg_height"] = svg_h
            break
    idx_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    only = sys.argv[1:] if len(sys.argv) > 1 else list(ARTICLES.keys())
    for slug in only:
        art = ARTICLES[slug]
        key = art["key"]
        print(f"=== {slug} ===")
        # transcript
        if "transcript" in art:
            transcript = art["transcript"]
        else:
            fixes = H264_FIX if slug.startswith("h264") else BAYER_FIX if slug.startswith("bayer") else LOG_FIX
            transcript = load_transcript(slug, key, fixes, art.get("json_name"))
        print(f"  transcript segments: {len(transcript)}")
        extract_frames(slug, key, [s for c in art["chapters"] for s in c["shots"]])
        build_html(art, slug, transcript)
        svg_h = build_svg_file(art, slug)
        update_translations(art, slug)
        update_index(art, slug, len(transcript), svg_h)
        print(f"  done, svg_h={svg_h}")


if __name__ == "__main__":
    main()
