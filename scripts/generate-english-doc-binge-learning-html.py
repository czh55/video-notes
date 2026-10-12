#!/usr/bin/env python3
"""超下饭英文纪录片推荐 → 图文实录（全英口播，正文简体）。"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "english-doc-binge-learning": {
        "key": "english-doc-binge-learning",
        "title": "超下饭英文纪录片！边看边学英语",
        "duration": "3分25秒",
        "tags": "英语学习 纪录片 Explained F1 OJ 输入",
        "url": "https://b23.tv/sQSCjkh",
        "primary": "workplace",
        "intro": "全英短片主张：学英语最好的方式，是用英语去学你本来就感兴趣的事——历史、经济、娱乐与社会结构。UP 推荐三部「比剧还上头」的纪录片：Netflix《Explained》（约 20 分钟/集、话题广、发音清、有数据）、F1《Drive to Survive》（看懂陌生产业与多口音访谈）、经典《OJ: Made in America》（悬疑节奏+美国社会与名人文化）。收束：不是英文纪录片天然更好，而是要把自己放进语言里，从一开始就用语言学东西。",
        "summary_rows": [
            ["00:00→00:22", "方法总纲", "用英语学感兴趣内容；打开新学习路径，三部片优于剧集。"],
            ["00:22→01:17", "Explained", "Netflix；约20分钟/集；电竞到股市；补世界观；发音清晰可练演讲。"],
            ["01:17→02:18", "Drive to Survive", "从零懂 F1；多季过山车叙事；非英语母语者口音→口音不重要、说清想法才重要。"],
            ["02:18→03:25", "OJ Made in America", "连环上瘾；社会问题与名人文化；结论：用语言学东西，把自己放进语言。"],
        ],
        "takeaway": "别只为学英语而学英语：选一部你真想看完的纪录片，让输入变成「用英语理解世界」。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-01:17",
                "title": "方法 + 第一部：《Explained》",
                "paras": [
                    "开场定调：最好的英语学习是用英语去学你真正感兴趣的事——历史、经济、娱乐，理解世界如何运转、社会结构如何织成。本片给出三部最爱纪录片，并称「甚至比剧集更好」，能打开全新学习方式。",
                    "第一部 Netflix《Explained》：每集约 20 分钟，不像传统纪录片一集一两小时；好跟、讲得清楚。最大卖点是每集不同话题——电竞、K-pop、占星、股市，覆盖社会经济、政治、娱乐，补齐成为「更完整的人」所需的知识碎片。发音清晰、有证据与数据，话题还可拿去练演讲。学生或职场人都适用。",
                ],
                "figs": [1, 2, 3],
            },
            {
                "id": "ch2",
                "time": "01:17-02:18",
                "title": "第二部：F1《Drive to Survive》",
                "paras": [
                    "第二部《Formula One: Drive to Survive》。作者自称看前对 F1 一无所知、觉得遥远，看后对整个产业有清晰图景——不只是成粉，学一个完全不同的行业能补全「世界如何运转」的拼图。",
                    "多季内容；从 2019 季开始「每集都狠」：像过山车，冠军不到最后不知谁属。看到烧钱又拼天赋的产业如何运作，叙事紧、一直拉人。学英语加分点：大量车手与受访者并非英语文化出身，口音各异——证明口音不重要，关键是能否把想法说清楚（口播 across key，按语境为 get ideas across）。",
                ],
                "figs": [4, 5],
            },
            {
                "id": "ch3",
                "time": "02:18-03:25",
                "title": "第三部 OJ + 把语言当工具",
                "paras": [
                    "第三部《OJ: Made in America》：经典案件/谋杀叙事，停不下来；单集约一小时但集与集咬得很紧。爱悬疑/犯罪片可看——不仅因真实往事，更因深入美国社会运作，并触发对名人文化与名声机制的停顿反思；对美国历史与当下社会问题都有洞察。",
                    "收束：不只为学英语，更鼓励多看英文纪录片。不是英文片一定优于中文片，而是学好语言需要「真的用它去学东西」，从一开始就把自己放进那种语言里。",
                ],
                "figs": [6, 7],
            },
        ],
    }
}


def main() -> None:
    _mod.generate("english-doc-binge-learning", DATA["english-doc-binge-learning"])


if __name__ == "__main__":
    main()
