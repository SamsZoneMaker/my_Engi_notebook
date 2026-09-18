---
title: 讲义 03 TLP 可靠传输与 Replay
tags: [pcie, gen5, replay, lcrc, lecture]
---

# 学习目标

能用发送端四个变量推演正常确认、Nak、超时、回绕和连续 replay；能解释 LCRC 与 Sequence Number 各自发现什么。

# 1. 发送端给 TLP 加的 6 Byte

```text
[4 bit Reserved/PMUX | 12 bit Sequence Number] + 原 TLP + [32 bit LCRC]
```

Sequence Number 检测丢失、重复和顺序；LCRC 检测这一跳上的比特错误。只有 LCRC，没有序号，就不知道“一个完整且正确的包是否根本没出现”；只有序号，没有 LCRC，就不知道内容是否被破坏。

# 2. 四个概念状态

| 变量 | 复位值 | 含义 |
|---|---|---|
| `NEXT_TRANSMIT_SEQ` | `000h` | 下一个新 TLP 要分配的序号 |
| `ACKD_SEQ` | `FFFh` | 对端累计确认到的最后序号 |
| `REPLAY_NUM` | `00b` | 当前未取得前进期间，已启动多少轮 replay |
| `REPLAY_TIMER` | 0 | 等待最老未确认进展的超时保护 |

`ACKD_SEQ=FFFh` 是因为它表示“0 的前一个已确认序号”。于是初始状态与跨回绕状态使用同一套模运算。

# 3. Equation 3-1 最容易被讲错

```text
(NEXT_TRANSMIT_SEQ - ACKD_SEQ) mod 4096 >= 2048
```

满足时，发送端停止从事务层接收新 TLP。

若实际有 `N` 个未确认 TLP，则：

```text
NEXT - ACKD = N + 1
```

初始 `000 - FFF mod4096 = 1`，而不是 0。因此阈值 2048 对应 2047 个未确认 TLP；把公式左边直接叫“在途数量”会产生 off-by-one。

# 4. 正常发送与确认

发送新 TLP：

1. 通过 Equation 3-1 与 Flow Control gating；
2. 附上 `NEXT_TRANSMIT_SEQ`；
3. 计算覆盖序号前缀和 TLP 的 LCRC；
4. 把副本存入 Retry Buffer（nullified TLP 除外）；
5. 序号加一。

收到合法 Ack(k)：

1. 从 Retry Buffer 最老条目开始，清到 k（含）；
2. `ACKD_SEQ=k`；
3. `REPLAY_NUM=0`；
4. 若仍有未确认 TLP 且 Ack 确实带来 forward progress，重启 Replay Timer；否则按规则停/保持。

Ack 是累计确认，所以 Ack(105) 包含 Ack(100) 的意义。

# 5. 三类失败的恢复路径

## 丢 TLP 或 TLP 损坏

接收端发现 LCRC 错或序号缺口，发 Nak。发送端处理合法 Nak 后，先承认 Nak 序号之前已正确收到的包，再从最老未确认项开始 replay。

## 丢 Ack

发送端 Timer 超时，重发未确认 TLP。接收端看到旧序号，判为 duplicate，丢弃其事务内容但再次安排 Ack。这个 Ack 打破循环。

## 丢 Nak

接收端不会无限重复同一个 Nak；发送端最终由 Replay Timer 超时触发同样的 replay。因此 Nak 是快速路径，Timer 是必达兜底。

# 6. Replay 的执行边界

开始 replay 后：

- 重发 Retry Buffer 中全部未确认 TLP，保持原序号与顺序；
- 重发第一个 TLP 的最后 Symbol 时重启 Timer；
- replay 期间收到 Ack/Nak **必须处理**；实现可继续当前重发列表，也可跳过尚未开始且已被确认的 TLP；
- 已开始发送的单个 TLP 必须完成，不能腰斩；
- 不重新申请 credit，因为这是同一逻辑 TLP，不是新事务。

连续第四次启动 replay 使 2-bit `REPLAY_NUM` 回绕，此时先让物理层进入 Recovery，再继续 replay。Recovery 本身不清 Retry Buffer；只有最终 LinkUp 变 0、进入 DL_Inactive 才清。

# 7. Ack/Nak 合法窗口

收到 Ack/Nak 序号 `S` 时，发送端先检查它是否落在自己可能发过、且没有倒退到歧义半环的范围：

```text
((NEXT_TRANSMIT_SEQ - 1) - S) mod4096 <= 2048
(S - ACKD_SEQ) mod4096 < 2048
```

两式边界一个 `≤`、一个 `<`，不能凭“半环口诀”自行改写。通过后再根据 `S == ACKD_SEQ` 判断是否带来前进。

# 8. 跨回绕例子

已确认到 `FFDh`，随后发送 `FFEh, FFFh, 000h, 001h`，此时：

```text
ACKD_SEQ = FFDh
NEXT_TRANSMIT_SEQ = 002h
未确认数量 = 4
(002 - FFD) mod4096 = 5 = 未确认数 + 1
```

Ack(000h) 表示累计确认 FFE、FFF、000，Retry Buffer 只剩 001。模运算让回绕点不需要特殊分支。

# 自测

- 为什么 Ack(ACKD_SEQ) 是合法但不产生 forward progress 的？
- replay 时收到更大的 Ack，为何可以跳过尚未开始重发的旧条目？
- 为什么 Receiver 处理 duplicate 必须避免再次交给事务层？
- 第四轮 replay 为什么进 Recovery，但不立即清 Retry Buffer？

## 细节索引

- [[01_38_S8_数据完整性_发送端]]
- [[01_39_S9_数据完整性_收DLLP]]
- [[讲义04_接收判定_计时器与调试]]
