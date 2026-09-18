---
title: 讲义 02 DLLP 与信用协议
tags: [pcie, gen5, dllp, flow-control, lecture]
---

# 学习目标

把 DLLP 当作一套“链路本地控制语言”，而不是把类型表当孤立编码背诵；理解 Flow Control 和可靠确认是两套独立账本。

# 1. DLLP 的固定骨架

Gen5 DLLP 固定 6 Byte：

```text
Byte 0      DLLP Type
Byte 1..3   type-specific information
Byte 4..5   16-bit CRC
```

CRC 覆盖 Byte 0–3，按每字节 bit0→bit7 的顺序输入，seed=`FFFFh`，多项式系数=`100Bh`，最终结果取反并按规范位映射写入 CRC 字段。Reserved 位虽然语义上忽略，物理收到的值仍参与 CRC。

坏 CRC 的 DLLP：**丢弃并报告 Bad DLLP**。DLLP 不进入 Retry Buffer。

# 2. 不要按十几个名字背，按“谁消费”分组

| 组 | 典型类型 | 最终消费者 | 自愈方式 |
|---|---|---|---|
| 可靠传输 | Ack / Nak | 数据链路层发送状态机 | Ack 累计覆盖；Nak 丢失由 Replay Timer 兜底 |
| Flow Control | InitFC1/2、UpdateFC | 初始化时 DLL 参与，稳态信息交事务层 | Init 周期重发；Update 为累计/绝对计数状态 |
| 能力交换 | Data Link Feature | 数据链路层 | 至少每 34 µs 重发，Ack bit 握手 |
| 电源管理 | PM_* | 组件 PM 逻辑 | 由第 5 章协议定义 |
| 其他 | NOP、Vendor-specific | 丢弃或私有逻辑 | NOP 校验后丢弃；未知 Type 静默丢弃 |

这里最重要的不是“DLLP 都是状态”，而是**每个类型都明确了丢失后的收敛机制**。

# 3. FC DLLP 的 Byte 0 解码

Gen5 三类家族：

```text
bit[7:6]  01 InitFC1 / 10 UpdateFC / 11 InitFC2
bit[5:4]  00 P / 01 NP / 10 Cpl
bit[3]    0
bit[2:0]  VC number
```

例：`1001 0010b`：`10`=UpdateFC，`01`=NP，bit3=0，`010`=VC2，所以是 UpdateFC-NP VC2。

# 4. FC DLLP 的 24 bit 内容

Figure 3-7/8/9 明确给出：

```text
Byte1[7:6] = HdrScale
Byte1[5:0] + Byte2[7:6] = HdrFC[7:0]
Byte2[5:4] = DataScale
Byte2[3:0] + Byte3[7:0] = DataFC[11:0]
```

Scale 编码：

| Scale | 支持 Scaled FC | 因子 |
|---|---|---|
| 00 | 否 | 1 |
| 01 | 是 | 1 |
| 10 | 是 | 4 |
| 11 | 是 | 16 |

`00` 与 `01` 数值因子相同，但语义不同：一个表示不使用扩展，一个表示支持/激活扩展且本字段因子为 1。

缩放不是把线上的字段变宽，而是恢复隐含低位：factor 4/16 等价于补 2/4 个低位 0。代价是粒度变粗，收益是量程变大。

# 5. Credit 账本和 Ack 账本为什么不能混

设 A 向 B 发送 TLP：

- B 通过 FC 告诉 A：我为各类流量还能提供多少接收资源；
- A 在第一次发送前做 credit gating；
- B 正确收到后，通过 Ack 告诉 A：这个序号以前的 TLP 不必再保留副本。

FC 回答“**能不能接收新的逻辑事务**”；Ack 回答“**旧事务的重传副本能不能释放**”。

因此 replay 不再次扣 credit：重发的是同一逻辑 TLP，第一次发送已经通过 gating。反过来，收到 Ack 也不等于 B 的接收资源此刻才释放；credit 何时回报由 §2.6 的缓冲语义决定。

# 6. 六类 credit 的边界

P/NP/Cpl 各有 Header/Data 两类，共六套 credit。一个 Data credit=4 DW=16 B。

Figure 3-3 中 MPS=1024 B，某些带数据类型的 `040h` 可由 `1024/16=64` 算出。但不能把它推广成“六类最小 credit 都必须容纳一个最大 TLP”；正式最小值因类型而异，需查 §2.6，NP Data 等场景可为 0。

# 7. 三个解码练习

1. `1110 0101b` 是什么？
2. Scale=`10b`、HdrFC 字段=`7Fh`，逻辑 credit 值是多少？
3. Data Link Feature 的 Ack 位在哪里？

答案：

1. InitFC2-Cpl VC5；
2. factor 4，`127×4=508`；
3. Byte1 bit7，剩余 23 bit 为 Feature Supported。

## 细节索引

- [[01_32_S2_DLLP初识]]
- [[01_36_S6_ScaledFC]]
- [[01_37_S7_DLLP详解]]
- [[讲义03_TLP可靠传输与Replay]]
