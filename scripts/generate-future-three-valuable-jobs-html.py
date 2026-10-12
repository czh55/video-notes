#!/usr/bin/env python3
"""未来最值钱的三种工作（硅谷创业者小鹰）→ 图文实录。"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "future-three-valuable-jobs": {
        "key": "future-three-valuable-jobs",
        "title": "未来最值钱的三种工作，硅谷创业者讲透真相",
        "duration": "12分35秒",
        "tags": "AI创业 一人公司 Founder 销售 通才",
        "url": "https://b23.tv/P9SiN92",
        "primary": "workplace",
        "intro": "硅谷连续创业者小鹰（斯坦福辍学、A16Z/OpenAI 等美元基金背景）对谈：工作不会消失，给「老登公司」打工的机会变少；人要学会管 AI（少骚扰、错题本、AI 盯 AI）；从螺丝钉变通才、能定义问题。近未来三类工作：Founder、销售（人格魅力）、过渡期苦工/精细体力。教育侧强调抗压、定义欲望、别卷可被定义的路线（如纯奥数攀比）。",
        "summary_rows": [
            ["00:00→03:30", "创投路径", "风口+先有客户收入+圈子；英语叙事加分；小团队全能+AI。"],
            ["03:30→07:00", "管 AI / 职场", "人成瓶颈；工作更多、老登岗更少；会操纵 Agent 的人稀缺。"],
            ["07:00→10:00", "通才与教育", "未成功创业者常高于大厂螺丝钉；换圈子；孩子要皮糙肉厚、会定义问题。"],
            ["10:00→12:35", "三种工作", "Founder / 销售 / 过渡苦工与精细体力；传记+测新产品+播客。"],
        ],
        "takeaway": "别守破船当中层写文档；尽快进入「定义问题 + 管 AI」的新工作方式。近未来最硬的是 Founder 与销售，螺丝钉最先被裁。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-03:30",
                "title": "背景与美元基金：风口、收入、圈子",
                "paras": [
                    "开场介绍小鹰：连续创业、融约两千万美金、现做「让每个人用 AI 打造一人公司」。谈亚裔如何拿头部美元基金：近年投中国人更多；英语表达有帮助；更关键是赶上风口（疫情虚拟活动类比今天 AI）、先有客户与收入再融资、以及硅谷融资圈子。",
                    "团队极瘦：五人以内。旧思维「十人干不过一人」的对手——对方一人兼产品设计品类还会用 AI；会议与不会用 AI 的人拖慢组织。工作碎片化：给 AI 派活、被权限与质量反复打断。",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2",
                "time": "03:30-07:00",
                "title": "管 AI：人是瓶颈；打工岗在漏",
                "paras": [
                    "管 AI 的难点：让它干得久且靠谱——权限一次给对、方向及时纠偏、派另一个 AI「骂」它质检、做错题本长记性。人要保重体力：AI 不休息，人成瓶颈；不是让 AI 适应有肉体极限的你，而是你适应 AI 的工作方式。",
                    "金句：工作肯定会越来越多，只是给老登公司打工的机会越来越少。围绕 Agent 的新组织尚未成型，会操纵智能体的人各公司都缺；能自己写代码收尾的新型产品经理值钱，传统开会写文档型会变少。破船裁员逻辑：不需要那么多人 + 降本增效叙事。",
                ],
                "figs": [3, 4],
            },
            {
                "id": "ch3",
                "time": "07:00-12:35",
                "title": "通才、三种工作与怎么迈第一步",
                "paras": [
                    "硅谷常觉得「没那么成功的创业者」高于大厂打工人——通才、对结果负责、主动。与其纠结创业/打工标签，不如从螺丝钉变成 AI 时代需要的人。第一步：换掉只聊裁员的圈子，接触 AI 淘金场的朋友与年轻人，放下旧架子。",
                    "对孩子：皮糙肉厚、心理强、知道自己喜欢什么；社会可定义的路线易被 AI 取代，要练定义问题与欲望。明确没价值的别卷（纯螺丝钉、用奥数证明牛）。三种工作：Founder（社会主人）、销售（人格魅力、更挣钱）、过渡期苦工/精细体力（AI 手笨时）。资料：名人传记、逼 AI 用「傻子方式」解释、狂测新产品、听 20VC / More or Less 等播客。",
                ],
                "figs": [5, 6, 7],
            },
        ],
    }
}

def main():
    _mod.generate("future-three-valuable-jobs", DATA["future-three-valuable-jobs"])

if __name__ == "__main__":
    main()
