#!/usr/bin/env python3
"""单篇：王自如聊口才如何变好 → 图文实录 HTML。"""
from __future__ import annotations

import sys
from pathlib import Path

import importlib.util

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "b60_html", ROOT / "scripts" / "b60-html.py"
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
generate = _mod.generate

DATA = {
    "wangziru-how-to-improve-eloquence": {
        "key": "wangziru-how-to-improve-eloquence",
        "title": "王自如聊口才如何变好",
        "duration": "1分29秒",
        "tags": "口才 表达 思维方式 写稿 storytelling 王自如",
        "url": "https://xhslink.cn/o/4HOOivj1BL9",
        "primary": "workplace",
        "intro": "王自如短片纠偏：表达能力强≠口才好。写东西好不好、说话有没有感染力，本质是思维方式与思想高度，不是口齿训练。他批评「总分总、一二三四」式演讲课只剩形式逻辑；真正改变来自多年写稿（ZEALER 时期）与《科技相对论》对 storytelling、文字节奏甚至句尾字数与声调的推敲。ASR 将 ZEALER 识为 ZILLER，叙述已校正。",
        "summary_rows": [
            ["00:00→00:22", "重点纠偏", "别问「口才怎么变好」；文字力与感染力来自思维与思想，不是口齿；慢说话亦可穿透。"],
            ["00:22→00:45", "形式方法论陷阱", "演讲课教总分总一二三四，貌似有条理；无思维/逻辑训练则内容无内涵无关联，反而是失败表达。"],
            ["00:45→01:09", "写稿改思维", "ZEALER 十余年与创业前独立做内容：不断写稿把思维方式写通；脑子想通却落不了笔=表达垃圾。"],
            ["01:09→01:29", "Storytelling 推敲", "《科技相对论》主创：讲故事感、文字节奏；句尾留白时 15 字还是 25 字、第几声收束都要推敲。"],
        ],
        "takeaway": "练口才不如练思维与写作：把能想通的事写进片子/文章；形式条理只是外壳，内涵与关联才是表达。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-00:22",
                "title": "表达不是口才问题，是思维与思想",
                "paras": [
                    "开场直接纠偏：很多人问「我的口才怎么能变好」，其实重点放错了。一个人的文字能力——写东西好不好、说话有没有感染力——「其实是思维方式的问题和你的思想的问题，不是口齿的问题」。",
                    "证据句：有些人说话很慢，但依旧有穿透内心的能量，因为思想高度够。结论口令清晰——不要把重点放在口才本身的训练上，而是要训练思维。",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2",
                "time": "00:22-00:45",
                "title": "演讲课的「总分总」：只有形式逻辑",
                "paras": [
                    "他见过很多上过所谓演讲课、口才课的人：老师会教总分总、一二三四，说起来貌似很有条理。但若只学会具体方法论，没有在思维能力与逻辑能力上训练好，讲出来的东西除了「一二三四听起来很有逻辑」以外，细听内容「毫无内涵、毫无关联性可言」——那反倒是失败的说话。",
                    "这一段把「表达训练」拆成两层：可被训练的形式外壳，与不可被套路替代的思维内核。",
                ],
                "figs": [3, 4],
            },
            {
                "id": "ch3",
                "time": "00:45-01:29",
                "title": "写稿与 Storytelling：真正改变表达的路径",
                "paras": [
                    "他自己的转折点：做 ZEALER（口播品牌名；ASR 曾误识为 ZILLER）十余年，以及创业前独立制作内容的时间——「不断的写稿子写内容」，把自己的思维方式有了很大提升。关键检验：脑子里能想通的事，落到笔头上若说不清，表达起来「简直就是垃圾，没法进片子，没法作文」。",
                    "《科技相对论》创作过程对他提升很大，他是主创之一。当时对故事表达叫 Storytelling：讲故事的感觉、文字的节奏感；甚至句子或关键段落结尾希望留白、带来想象空间时，「到底是用 15 个字还是 25 个字，最后一个词是应该用第几声结束」，都要仔细推敲。",
                ],
                "figs": [5, 6, 7],
            },
        ],
    }
}


def main() -> None:
    slug = "wangziru-how-to-improve-eloquence"
    # 转录层 ASR 校正：仅改 whisper JSON 副本字段，生成后再还原
    whisper_path = ROOT / f"{slug}.json"
    raw = whisper_path.read_text(encoding="utf-8")
    whisper_path.write_text(raw.replace("ZILLER", "ZEALER"), encoding="utf-8")
    try:
        generate(slug, DATA[slug])
    finally:
        whisper_path.write_text(raw, encoding="utf-8")
    print(f"ASR fix applied in transcript only for {slug}")


if __name__ == "__main__":
    main()
