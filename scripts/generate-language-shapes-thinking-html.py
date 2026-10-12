#!/usr/bin/env python3
"""单篇：语言决定思维 → 图文实录 HTML（全英口播，正文简体解读）。"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "language-shapes-thinking": {
        "key": "language-shapes-thinking",
        "title": "全英｜语言决定了你的思维 你的内耗很可能是语言带来的",
        "duration": "3分25秒",
        "tags": "语言 外语效应 情绪粒度 内耗 维特根斯坦",
        "url": "https://b23.tv/VzNHL8C",
        "primary": "workplace",
        "intro": "全英短片谈「语言如何塑造思维」：说英语时常更理性、少情绪反应，背后是外语效应（母语承载更强情绪记忆）与英汉差异（英语更爱把过程名词化）。后半连接算法偏爱极端标签与 Lisa Feldman Barrett 的情绪粒度研究——具体描述感受比贴「内耗/愤怒」标签更能减少冲动。收束于维特根斯坦：语言的边界即世界的边界。口播为英文，正文为简体解读；专名 ASR 已校正（Wittgenstein、Barrett、Perry Link）。",
        "summary_rows": [
            ["00:00→00:40", "外语效应", "母语情绪权重更大；切换二语→与情绪拉开距离，更开放理性。"],
            ["00:40→01:40", "名词化 vs 动作", "Perry Link：英语常把过程变成「可打击的事物」；名词多→更盯具体物而非情绪流。"],
            ["01:40→02:50", "标签与情绪粒度", "算法爱极端关键词；具体描述身体/念头 vs 贴单一标签；粒度高→少冲动、身心更好。"],
            ["02:50→03:25", "世界边界", "学语言不是为了考试，是多套思维模板；语言窄则世界窄。"],
        ],
        "takeaway": "内耗常被「一个词」放大；换语言或换更细的描述，等于换一套处理情绪的模板。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-00:40",
                "title": "说英语时像换了一个人：外语效应",
                "paras": [
                    "开场承认：语言能塑造心智，说话方式会影响思维方式。说英语时你可能像另一个人——更逻辑、更关注事情而非情绪感受。",
                    "第一原因是研究者所称的外语效应（foreign language effect）：母语承载更强情绪重量，童年与深层感受都编码在其中；切到二语，自然与那些情绪拉开一点距离，「更开放、更理性、更少反应性」。",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2",
                "time": "00:40-01:40",
                "title": "英汉差异：把过程变成「东西」",
                "paras": [
                    "第二点：说英语时更注意具体事物。引用 Perry Link《Anatomy of Chinese》（哈佛大学出版社）：英语常把过程名词化——例如 inflation 变成可以「打击/战胜」的东西，尽管它本质是时间中的过程；中文更常以动作与运动表达同一观念。",
                    "多用名词时，你可能更盯「具体物」而非情绪流：说 “I have a feeling of sadness” 像从远处看待情绪，因而更理性。学不同语言，等于多几套处理情绪与问题的模板。",
                ],
                "figs": [3],
            },
            {
                "id": "ch3",
                "time": "01:40-03:25",
                "title": "标签、情绪粒度与语言边界",
                "paras": [
                    "当下更容易极端与极化：极端标签更易被算法索引。发帖盯标题与标签、用一个关键词引流，会强化「单字定义体验」的机制；但人类感受无法被一个词识别干净。对比：只喊「内耗/愤怒/内卷」，vs 「我不同意他的话，脑子有点乱，体温在升」——更具体就不那么容易被坏消息点燃。",
                    "连接到情绪粒度（emotional granularity，神经科学家 Lisa Feldman Barrett，东北大学）：能更具体描述情绪的人更少冲动反应，身心健康也更好。收束：日常语言影响力大；模型灵感来自维特根斯坦——「我的语言的边界意味着我的世界的边界」：语言窄，世界就窄。",
                ],
                "figs": [4, 5, 6],
            },
        ],
    }
}


def main() -> None:
    slug = "language-shapes-thinking"
    _mod.generate(slug, DATA[slug])


if __name__ == "__main__":
    main()
