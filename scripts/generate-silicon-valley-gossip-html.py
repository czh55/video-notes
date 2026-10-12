#!/usr/bin/env python3
"""硅谷八卦 → 图文实录。"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "silicon-valley-gossip": {
        "key": "silicon-valley-gossip",
        "title": "硅谷八卦",
        "duration": "16分30秒",
        "tags": "硅谷 AI Buck's PayPal AGI 风投",
        "url": "https://b23.tv/b7mTZUi",
        "primary": "workplace",
        "intro": "探访式短片：从传奇早餐店 Buck's（ASR 作 Bugs）的特斯拉创业桌与「马斯克最爱培根」，到 Facebook/PayPal 早期办公室与斯坦福果园史；采访投资人对照 AI 热潮为何比移动互联网更快（Utility 无需网络效应冷启动），把 AGI 类比为蒸汽机/电力级通用生产力，并以图片搜索上线故事说明技术理想主义；收束于邀请制 AGA House 周六社交。开场电视英语音轨 ASR 嘈杂，正文以探访与访谈为准。",
        "summary_rows": [
            ["00:00→04:40", "Buck's 餐桌传说", "传奇餐厅；特斯拉创业桌；边吃边抛「矽谷 AI 到底怎样」的问题。"],
            ["04:40→09:50", "地标与历史", "Apple I 文物；FB/PayPal 办公室；斯坦福租地与军工订单塑形。"],
            ["09:50→16:30", "AI 热潮对照", "速度因 Utility；AGI≈蒸汽/电力；工程师理想主义；AGA House。"],
        ],
        "takeaway": "这集「八卦」的信息密度在现场感：地标证明叙事、早餐桌串联创业神话；访谈给出可带走的框架——AI 是基础设施式扩散，热潮像 2000 年估值狂欢也像生产力革命，关键在速度与通用性。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-04:40",
                "title": "Buck's：吃着传说问 AI",
                "paras": [
                    "开场环境音嘈杂（电视英语音轨 ASR 混乱），很快切到美食探访：Buck's 面积不大但桌桌有故事——主持人坐的位置被指为特斯拉创业早餐桌（当时还没有马斯克入局的版本叙事）。",
                    "点了号称马斯克最爱的培根配餐，抛出本集问题：这边 AI 发展到什么程度、从业者什么状态。吃完还半开玩笑说要给马斯克发推。",
                ],
                "figs": [1, 2, 3],
            },
            {
                "id": "ch2",
                "time": "04:40-09:50",
                "title": "办公室巡礼与矽谷成因",
                "paras": [
                    "店内展示 Apple I 等文物，店主口述从 PC 到 1995 网络爆发再到当下对 AI「惊讶又害怕」。外景：Facebook 第一间正式办公室（对面越南粉）、PayPal 所在「最幸运办公室」——租金贵本身是信号（有名风投投了才住得起）。",
                    "下行到斯坦福：上世纪 30 年代前本地是果园；校方鼓励学生租地创业催生车库形态；冷战军工订单带动半导体；80 年代养老金入私募叠加 PC/互联网热潮，理想主义与资本狂欢交替至今。",
                ],
                "figs": [4, 5, 6],
            },
            {
                "id": "ch3",
                "time": "09:50-16:30",
                "title": "AI 热潮：更快、更通用、更社交",
                "paras": [
                    "投资人对照：像 2000 年估值狂奔+高房价高薪；不同在于速度——移动互联网要网络效应（如 Facebook「五个好友」），AI 更像 Utility：自己用上 ChatGPT/DeepSeek 就能受益。大厂竞争反而给普通人机会；不宜只把 AI 比作又一次互联网，更接近蒸汽机/电力级通用生产力（AGI 的 G=General），「涌现」带来跨任务融会。",
                    "技术理想主义样本：合伙人周末做图片搜索被谷歌创始人看中上线，工程师命运被改写，激励周围人「下一个为什么不是我」。结尾当地时间 2026-06-27 周六下午进入邀请制 AGA House：上午行业报告不对镜头开放，下午窥探矽谷社交在干什么。",
                ],
                "figs": [7, 8, 9, 10],
            },
        ],
    }
}


def main() -> None:
    _mod.generate("silicon-valley-gossip", DATA["silicon-valley-gossip"])
    out = ROOT / "docs" / "silicon-valley-gossip-图文实录.html"
    t = out.read_text(encoding="utf-8")
    t = t.replace(">小红书</span>", ">B站</span>", 1)
    t = t.replace(
        ".tag-platform{background:#ff2442;color:#fff}",
        ".tag-platform{background:#00a1d6;color:#fff}",
        1,
    )
    out.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    main()
