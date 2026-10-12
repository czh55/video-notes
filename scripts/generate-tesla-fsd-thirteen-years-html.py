#!/usr/bin/env python3
"""特斯拉 FSD 十三年（硅谷101）→ 图文实录。"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("b60_html", ROOT / "scripts" / "b60-html.py")
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

DATA = {
    "tesla-fsd-thirteen-years": {
        "key": "tesla-fsd-thirteen-years",
        "title": "让人类交出方向盘：特斯拉FSD十三年的冒险、争议与进化【硅谷101】",
        "duration": "62分35秒",
        "tags": "FSD Robotaxi CyberCab Waymo 端到端",
        "url": "https://b23.tv/QQer1jF",
        "primary": "auto-digital",
        "intro": "硅谷101 横跨数月采访特斯拉十余年硬件/软件工程师，并实地体验奥斯汀 CyberCab：无方向盘、远程监管兜底。主线是 FSD 硬件从 Mobileye 黑盒→英伟达过渡→自研 AI3/AI4/AI5，软件从规则感知到 HydraNet/BEV/占据网络再到端到端 V12–V14；对照 Waymo「谨慎划界」与特斯拉「量产车数据飞轮」。收束：技术路线之争进入下半场经济之战——Waymo 运营仍领先，CyberCab 刚起步且面临监管，特斯拉证明激进路线仍留在决赛圈。",
        "summary_rows": [
            ["00:00→07:00", "CyberCab 与 HW1–2.5", "奥斯汀体验；与谷歌分道；Mobileye 分手；八摄+英伟达双芯片冗余。"],
            ["07:00→21:00", "AI3 与感知重构", "Jim Keller/Peter；AI3 流片；Karpathy；HydraNet/时序/BEV。"],
            ["21:00→38:00", "去雷达与 HW4", "供应链催生纯视觉；占据网络；HW4 像素/芯片数/GDDR 拉扯。"],
            ["38:00→52:00", "端到端与 Robotaxi", "V12 替换规则代码；V13/V14 放大模型；远程监管扩城。"],
            ["52:00→62:35", "AI5 与下半场", "Dojo 叫停；AI5 瞒报与双工艺；经济之战未分胜负。"],
        ],
        "takeaway": "特斯拉 FSD 的「差分」不是单点算法，而是愿意把未成熟系统装进数百万量产车、用成本与风险偏好倒逼工程闭环；下半场胜负手是规模化安全下的单位出行成本，而非摄像头 vs 激光雷达口号。",
        "chapters": [
            {
                "id": "ch1",
                "time": "00:00-07:00",
                "title": "CyberCab 开场：两条路线如何分道",
                "paras": [
                    "开场坐进奥斯汀刚运营的 CyberCab：无方向盘、无踏板；后台远程工作人员兜底，乘客有 Emergency Stop / Pull over。德州登记 Robotaxi 约 476 辆，其中 CyberCab 67、其余多为带方向盘的 Model Y。",
                    "2013 年特斯拉想做自动驾驶，谷歌高精地图+激光雷达太贵且主张一步 L4；马斯克坚持 L2 迭代到 L4，双方分道。特斯拉先找供应商：Hardware 1.0（单前摄+毫米波+超声波+Mobileye EyeQ3）。2015 Autopilot 上线惊艳但也诱发误用；2016 佛罗里达致死事故后与 Mobileye 决裂——根因不止事故，更是感知黑盒接口无法由特斯拉掌控。HW2.0 八摄换 NVIDIA Drive PX2，HW2.5 加冗余 GPU，自研算法六个月内替换 Mobileye。",
                ],
                "figs": [1, 2, 3],
            },
            {
                "id": "ch2",
                "time": "07:00-21:00",
                "title": "AI3 自研与感知四大升级",
                "paras": [
                    "2016 引入 Jim Keller、Peter Bannon；在三星协助下 AI3 约 18 个月设计、首次流片近乎可用——专为神经网络场景优化，利用率远高于通用 GPU。AI3 量产前三个月软件人手极度不足，硬件团队 hack 自测；自研换来成本与主动权（含逼 TI 降价、英伟达驱动扯皮等供应商故事）。",
                    "Karpathy 入局后重构感知：深度学习替代手工任务；HydraNet 共享 backbone 多任务头；从单帧图像走向时序视频记忆；多摄融合到 BEV。2017 Transformer 论文改写 AI 史，而 HW3 仍偏 CNN 时代设计——为后续端到端埋下算力与架构张力。",
                ],
                "figs": [4, 5],
            },
            {
                "id": "ch3",
                "time": "21:00-38:00",
                "title": "去雷达、占据网络与 HW4 拉扯",
                "paras": [
                    "2021 移除毫米波雷达：口播称真实触发是疫情供应链（Continental 等供不上货被马斯克「拉黑」），而非纯技术成熟。纯视觉需补测距；Occupancy Network 用体素表达任意形状障碍，靠自动标注与少量激光雷达采集车做 ground truth。",
                    "HW4 全板重设计：摄像头 1.2MP→5MP、布局被砍又因盲区在 Cybertruck 前杠补回；软件要三芯片、量产前被砍回双芯片；改用 GDDR 追带宽却遭遇车规容量瓶颈（内部讨论改回 LPDDR 的 HW4.3）。成本仍压到「普通 iPad」量级；AI4 芯片亦进服务器做像素注入仿真与决策回放验证。",
                ],
                "figs": [6, 7],
            },
            {
                "id": "ch4",
                "time": "38:00-52:00",
                "title": "端到端 V12–V14 与 Robotaxi",
                "paras": [
                    "Karpathy 离开后，工程师提出用神经网络替代规则（「车用 ChatGPT」），击中马斯克：端到端把约 30 万行代码压到极少控制输出。2023 公开演示虽闯红灯却被业内视为强信号；V12 落地验证可行性，V13 简化控制栈、光子直入模型，V14/14.1 参数再放大并用强化学习等——内部喻为种树：存活→剪枝→施肥。可解释性靠中间 3D 表征头；验证靠世界模型仿真。",
                    "Robotaxi：硬件与量产车同源，软件更新更勤、获 L4 运行资质；关键差异是远程监管——扩到数千上万辆时，人工兜底成本与安全证明才是扩城瓶颈。",
                ],
                "figs": [8, 9],
            },
            {
                "id": "ch5",
                "time": "52:00-62:35",
                "title": "AI5 风波与下半场经济之战",
                "paras": [
                    "Dojo 训练集群被叫停，马斯克称 AI5/AI6 可兼训练。AI5 完全自研后人手/经验不足，项目主管瞒报进度，台积电指出图纸远未可流片，马斯克震怒裁撤；后双线并行（外包+三星回流），三星版 AI5 已流片，亦有「AI5 主要进算力中心/机器人、车上 AI4 够用」的内部变数。",
                    "收束：特斯拉敢用新技术、流程少、盯产品；与 Waymo「九线区域谨慎扩张」对照。13 年后路线未分胜负，战争改名经济之战——Waymo 运营领先，CyberCab 有限区域起步且遭监管调查。真正难题：无安全员、无方向盘时面对百万次真实出行能否稳住安全，并把成本打到大规模商业化。",
                ],
                "figs": [10],
            },
        ],
    }
}


def main() -> None:
    _mod.generate("tesla-fsd-thirteen-years", DATA["tesla-fsd-thirteen-years"])
    # B 站角标
    out = ROOT / "docs" / "tesla-fsd-thirteen-years-图文实录.html"
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
