---
title: 讲义 01 从 Physical LinkUp 到 DL_Active
tags: [pcie, gen5, data-link-layer, lecture]
---

# 学习目标

读完应能画出 `DL_Inactive → [DL_Feature] → DL_Init → DL_Active`，并解释 `DL_Up` 为什么在 `FC_INIT2` 就出现。

# 1. 三层的“已经好了”不是一回事

```text
Physical LinkUp = 1：物理层训练成功，可以传符号/包
DL_Up             ：数据链路层已经能与对端通信
DL_Active         ：DLCMSM 进入正常工作状态
某 VC 可发 TLP     ：还要该 VC 的 FC 初始化完成且 credit 足够
```

这四句话看似相近，实际上是四个门。最常见错误是把第一道门直接当最后一道门。

# 2. `DL_Inactive`：不是“空闲”，是协议纪元结束

进入 `DL_Inactive` 会重置链路层状态、清远端 Feature 有效位、丢弃 Retry Buffer，并报告 `DL_Down`。
这意味着旧链路纪元的序号、确认与能力信息全部作废。若 Retry Buffer 中仍有未确认事务，事务层必须按 Link Down 语义处理，DLL 不再尝试跨断链继续 replay。

关键不变量：**不同 LinkUp 周期的序号账本绝不拼接。**

# 3. `DL_Feature`：可选的能力互报

Gen5 的 Feature Supported 只有 bit0 有定义：Scaled Flow Control；bit[22:1] Reserved。

每一端维护：

```text
Local Supported          我支持什么
Remote Supported         对端支持什么
Remote Supported Valid   我是否收过对端 Feature DLLP
```

发送 Feature DLLP 时：

```text
Feature Supported = Local Supported
Feature Ack       = Remote Supported Valid
```

Ack 位不是“我同意启用”，只是“我已经收到过你的 Feature DLLP”。当 A 收到 B 的 `Ack=1`，A 可推断：

1. B 已收到 A 的能力；
2. A 自己此刻也已收到 B 的能力。

双方因此各自知道“双向信息已到达”。Feature DLLP 至少每 34 µs 发一次；若一端先退出，另一端还可以通过收到 `InitFC1` 判断对方已进入下一阶段并退出，避免死等。

Scaled FC 的激活条件是 `Local bit0 AND Remote bit0`，不是单端支持，也不是 Ack=1 本身。

# 4. `DL_Init` 里面还有两个 FC 子状态

`DL_Init` 不是一团动作，而是 `FC_INIT1 → FC_INIT2`。

## FC_INIT1：交换真正要使用的 credit 初值

每端反复按 P → NP → Cpl 的相对顺序发送三类 InitFC1，至少每 34 µs 完成一次三类发送。
接收端从收到的 InitFC1 **或 InitFC2** 记录对应的 HdrFC/DataFC，以及支持 Scaled FC 时的 Scale。
P、NP、Cpl 三类都拿到后置 `FI1=1`，进入 FC_INIT2。

为什么 InitFC2 也能作为数据源？两端并不同步；对端可能已经前进，但其中一端仍在 FC_INIT1。拒收 InitFC2 会制造不必要的死锁窗口。

## FC_INIT2：确认对端也走过了第一阶段

仍反复发送 P → NP → Cpl 三类 InitFC2，但收到的 credit 值不再更新本地记录。此时包的作用是“阶段证据”，不是重新发布一套值。

`FI2` 有三类置位证据：

- 收到任一 InitFC2；
- 收到该 VC 上的任一 TLP；
- 收到该 VC 的任一 UpdateFC。

后两条是鲁棒性路径：对端都已经发送正常期流量了，就足以证明它已经完成初始化，无须死等可能丢失的 InitFC2。

# 5. `DL_Up` 的精确时刻

```text
FC_INIT1：DL_Down
FC_INIT2：DL_Up，但该 VC 的 TLP 仍被阻塞
FI2=1 后：VC0 使 DLCMSM 进入 DL_Active
```

`DL_Up` 的语义是链路层已能通信，并不是所有正常期发送条件均已满足。这个区别也解释了为什么 FC_INIT2 能接收 TLP 作为完成证据，同时发送侧仍不能主动发送该 VC 的 TLP。

# 6. 一次非同步启动推演

1. A 先进入 FC_INIT1，不断发三类 InitFC1；B 仍在 Feature。
2. B 收到 A 的 InitFC1，从 Feature 兜底退出，进入 FC_INIT1。
3. A 收全 B 的三类 credit，先进入 FC_INIT2，开始发 InitFC2。
4. B 仍在 FC_INIT1，但收到 A 的 InitFC2，也能记录 credit 并最终置 FI1。
5. B 进入 FC_INIT2；A 收到 B 的任一 InitFC2，完成。
6. 若 A→B 的 InitFC2 全丢，B 最终收到 A 的 TLP/UpdateFC，仍可置 FI2 完成。

每一步都允许两端不同步，协议靠“周期重发 + 后续行为作为证据”收敛。

# 自测

- Feature Exchange 未实现或被关闭，状态路径是什么？
- 一端在 FC_INIT1 收到 InitFC2，要不要记录其中的 credit？
- 一端在 FC_INIT2 收到 InitFC1，要不要重写 credit？会不会置 FI2？
- `Physical LinkUp=0` 时为何必须回到 Inactive，而不能保留 Retry Buffer 等待重连？

## 细节索引

- [[01_33_S3_DLCMSM]]
- [[01_34_S4_数据链路特性交换]]
- [[01_35_S5_流控初始化]]
- [[讲义02_DLLP与信用协议]]
