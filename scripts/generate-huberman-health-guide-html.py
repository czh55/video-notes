#!/usr/bin/env python3
"""Huberman 健康指南精讲 → 图文实录。"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "huberman-health-guide": {
        "key": "huberman-health-guide",
        "title": "斯坦福教授Huberman最新健康指南：代谢、睡眠、压力，很多人都做反了",
        "duration": "8分42秒",
        "tags": "Huberman 皮质醇 睡眠 NEAT 代谢 晨光",
        "url": "https://b23.tv/W8Afjck",
        "primary": "fitness",
        "intro": "凯莉精讲 Andrew Huberman 长访谈要点：①早晨要升高而非一味压制皮质醇（户外见光）；②晚餐适量淀粉碳水有助睡眠；③半夜醒可用极限眼球运动退出警觉；④「30岁代谢断崖」是伪命题，差在肌肉流失与 NEAT（非运动性活动产热）。文末提补剂清单但明确不建议盲目抄作业。口播繁体 ASR 已转简并校正「皮质醇 / 视交叉上核 / soleus」等。",
        "summary_rows": [
            ["00:00→01:50", "晨升皮质醇", "昼夜曲线：晨飙升、日夜渐降；见光启动觉醒并校准夜间睡眠；阴天也要出门。"],
            ["01:50→03:50", "晚间淀粉", "皮质醇更像备战激素；晚餐有淀粉→血糖充足→少启动夜间应激；长期低碳+睡差者优先试。"],
            ["03:50→05:20", "半夜眼球技巧", "闭眼极限左右上下+顺逆时针转2–3遍，配合延长呼气，帮助退出警觉入眠。"],
            ["05:20→08:42", "代谢伪命题", "20–65岁基础能耗差不大；抓增肌与 NEAT；饭后走、soleus push-up；补剂下期拆。"],
        ],
        "takeaway": "别把皮质醇当绝对坏人：早上用阳光把它「升到位」，晚上用节律与碳水让它降下来；体重体感差更多来自肌肉与无意识活动，不是生日蛋糕。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-01:50",
                "title": "早晨：升皮质醇，而不是打压",
                "paras": [
                    "开场四条颠覆：早上升皮质醇、晚上吃淀粉碳水、半夜眼球复位睡眠、30+代谢降低是伪命题。Huberman 长访谈被浓缩：皮质醇被网络妖魔化，但正常昼夜节律是晨间飙升、随后白天到晚上逐步下降。",
                    "关键：早晨升不够高，后面更难降下来。方法简单——起床喝水后尽快户外见自然光；视网膜特殊感光细胞把「天亮」信号传给视交叉上核（中央生物钟），启动觉醒并校准十几个小时后的睡眠。阴天也要出门：户外阴天光强仍远高于室内灯光。缺的不是「降皮质醇补剂」，而是早上用来升皮质醇的阳光。",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2",
                "time": "01:50-05:20",
                "title": "晚间碳水与半夜眼球技巧",
                "paras": [
                    "第二条：晚餐适量淀粉类碳水。长期把碳水压很低的人睡眠常不好，与皮质醇扰动有关。纠正：Cortisol 更像「备战激素」——危险或上台前调动葡萄糖供脑与肌肉。夜间有一定淀粉→血糖相对充足→身体少再调皮质醇进应激。非人人每晚必吃；长期低碳且睡差者强烈建议晚餐保留适量淀粉。",
                    "第三条：半夜醒难回睡。Huberman 技巧——闭眼极限转眼球：极力右/左/上/下，再顺时针、逆时针各一圈，幅度做到略酸，整套 2–3 遍；可配合延长呼气的深呼吸。原理简述：特定眼球运动关联本体感觉，帮助大脑退出警觉监测状态从而重新入睡。",
                ],
                "figs": [3, 4],
            },
            {
                "id": "ch3",
                "time": "05:20-08:42",
                "title": "30+代谢：肌肉、NEAT 与补剂边界",
                "paras": [
                    "第四条：引用 Science 相关研究——成年人能量消耗 20–65 岁无明显断崖，「30岁代谢断崖」不成立。体感变胖差在两变量：肌肉含量下降，以及 spontaneous movement / NEAT（非运动性活动产热）。肌肉比例相同则代谢不必低于二十岁；要做增肌与保肌。拉开日常消耗的是接水、换房间、爬楼、家务、边走边打电话等 App 记不到的活动；极端情况下 NEAT 差异可达约 1000–1800 kcal。",
                    "增加 NEAT 两招：饭后走 5–10 分钟助处理餐后葡萄糖、减 energy crash；久坐时做 soleus push-up（比目鱼肌：前脚掌踩地反复抬脚跟）。片尾整理一日 Protocol 引流，并列出 Huberman 核心补剂方向（Omega-3、维生素D、肌酸、镁、α-GPC），但明确不建议直接抄作业，剂型剂量下期拆解。",
                ],
                "figs": [5, 6, 7],
            },
        ],
    }
}


def main() -> None:
    slug = "huberman-health-guide"
    _mod.generate(slug, DATA[slug])


if __name__ == "__main__":
    main()
