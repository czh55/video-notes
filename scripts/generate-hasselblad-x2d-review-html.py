#!/usr/bin/env python3
"""哈苏 X2D 俩月真话 → 图文实录。"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "hasselblad-x2d-review": {
        "key": "hasselblad-x2d-review",
        "title": "5万多的哈苏 X2D 凭啥贵？用了俩月，真话全在这",
        "duration": "12分20秒",
        "tags": "哈苏 X2D 中画幅 动态范围 色彩 佳能对比",
        "url": "https://b23.tv/FQUJVwg",
        "primary": "photo",
        "intro": "UP 实打实用哈苏 X2D 100C 约两个月：值高定价的是动态范围/16bit RAW、自然色彩（后期极少）、1亿像素细节与十挡防抖、握持/OLED/菜单/1TB内置与软件体验；不值点在于对焦与连拍相对顶级全画幅偏慢、连机拍摄关连续对焦、几乎无可用视频。结论：多数人可能不值，极致静物/人像/风光画质党能懂贵的道理。对比样片对佳能 R5 II、R6 III。",
        "summary_rows": [
            ["00:00→03:00", "动态范围", "中画幅+1亿像素 RAW 宽容度；欠曝肤色可救；机内 HDR+OLED 回看。"],
            ["03:00→06:30", "色彩与像素", "自然色彩校准；人像少偏色；风光裁切/防抖/XPan；影棚细节怪兽。"],
            ["06:30→09:00", "体验加分", "握持、屏幕、菜单、1TB、耐高寒雨淋、手机/电脑原厂软件接近 LR。"],
            ["09:00→12:20", "妥协与结论", "AF/连拍非体育机；无视频；多数人不值，极致画质党可值。"],
        ],
        "takeaway": "X2D 是把钱砸在「拍照纯度」上的机器：画质与仪式感换对焦速度与视频能力；选购先问自己拍不拍动态与视频。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-03:00",
                "title": "贵得有理：动态范围与 RAW 容错",
                "paras": [
                    "开场承诺讲真话：哪些配得上高定价、哪些不值，并与顶配全画幅对比。第一次用数码中画幅，最直观的「贵有道理」是动态范围——1亿像素+中画幅传感器，RAW 宽容度高，拉阴影压高光幅度夸张，机内可拍真正 HDR，OLED 回看成片。",
                    "阴影干净，大幅后期色彩不易垮；对比全画幅拉多易发灰，欠曝人物肤色易崩。海边日落城市暗线+深阴影人物等场景更能体现；16bit 色深让信息更足。极光冰屋亮窗等高光场景也轻松压回细节。",
                ],
                "figs": [1, 2],
            },
            {
                "id": "ch2",
                "time": "03:00-06:30",
                "title": "色彩科学、一亿像素与影棚细节",
                "paras": [
                    "最爱点之一是色彩：人像肤色自然、少怪偏色与红色过饱和（全画幅痛点）；贴近肉眼所见，后期量极小——不是浓重直出预设，而是自然色彩方案（传感器出厂单独校准）。与佳能 R5 II、R6 III 海边人像对比留给观众判断。",
                    "一亿像素带来风光裁切重构图灵活性；十挡机身防抖手持约 1 秒曝光可行；XPan 宽幅裁切有趣。意外强项是影棚：皮肤/眼睛/布料/头发细节干净，35-100 镜头+传感器成「画质怪兽」。灯塔等与 R5 II 放大对比细节差明显。",
                ],
                "figs": [3, 4, 5],
            },
            {
                "id": "ch3",
                "time": "06:30-12:20",
                "title": "使用体验加分，以及配不上价的妥协",
                "paras": [
                    "握持（加大镜头仍舒服）、质感做工、OLED 回放、菜单直观、1TB 内置高速、耐零下与雨淋；配套手机对焦 App 与桌面软件接近 Lightroom 体验，想要正宗哈苏色建议走原厂软件。",
                    "妥协：AF 准且稳，婚礼/人像够用，但不及同价顶级全画幅速度与最新 AI，连拍约 3fps，不适合体育；电脑连机拍摄会关连续对焦；几乎无可用视频——对视频用户可直接排除，作者反而欣赏其「只做拍照」。结论：多数人可能不值（全画幅已过剩）；极致动态范围/色彩/细节与仪式感追求者能懂贵因；爱好者不必盲目冲。",
                ],
                "figs": [6, 7],
            },
        ],
    }
}


def main() -> None:
    _mod.generate("hasselblad-x2d-review", DATA["hasselblad-x2d-review"])


if __name__ == "__main__":
    main()
