---
created: 2026-07-30
tags:
  - type/knowledge
---
> [!abstract] 核心结论
> 记录关于DLLP的内容，区别Flit mode中的DLP

## 引入概念
| 名称           | 是什么                               |
| ------------ | --------------------------------- |
| DLLP         | 一条具有明确语义的数据链路层协议消息                |
| DLP bytes    | Flit 中固定的数据链路控制区域                 |
| DLLP Payload | DLP 区域中可承载的 4-Byte 普通 DLLP 内容     |
| DLP Symbol   | Flit Mode DLP 中的专用控制编码，例如 Ack/Nak |

关系可以画成：
```
Flit 的 DLP 信息
│
├── 普通 DLLP
│   ├── InitFC1 / InitFC2
│   ├── UpdateFC
│   ├── Data Link Feature
│   ├── Power Management
│   └── Link Management
│
├── Optimized_Update_FC
├── Flit_Marker
└── 专用 Ack/Nak DLP Symbols
```


DLLP的作用是支持在link上的操作，那dllp的种类有：
- Data Link Feature DLLP：协商双方支持的数据链路 Feature
- Ack/Nak DLLP：对TLP进行反馈确认，Nak DLLP会用于启动 Retry/Replay，仅用于non-flit mode
- InitFC1、InitFC2、UpdateFC：用于Flow control
- Power Management DLLP：用于电源管理
- Link Management DLLP：用于L0p



## DLLP Rules

> In Flit Mode, DLLPs are transmitted in the DLP bytes of a Flit.

其中，dllp type specific info 会根据不同的dllp type继续细分里面的内容，例如Ack/Nak dllp
![[dllp_acknak.png]]


> 在spec原文中，提到fields内被标记为Reserved的bit位必须全部填`0`，这样在接收端会忽略这些`0`不做任何特殊处理。


### dllp type encodings
[[spec_chap3.pdf#page=18|dllp type encodings table]]


## DLLP Types

| DLLP type            | Function                           | 模式说明                                                                                            |
| -------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| Data Link Feature    | 协商支持的数据链路特性                        | Flit/Non-Flit 都可能使用，用于DLCMSM的DL_Feature，详情Feature可见[[spec_chap3.pdf#page=7\|feartue supported]] |
| Ack                  | 确认一批 TLP 已正确接收                     | 仅 Non-Flit Mode                                                                                 |
| Nak                  | 请求 Data Link Layer Retry           | 仅 Non-Flit Mode                                                                                 |
| InitFC1 / InitFC2    | 初始化 Virtual Channel 的 Flow Control | 两种模式都使用                                                                                         |
| UpdateFC             | 更新接收端可用 Credit                     | 两种模式都使用                                                                                         |
| PM DLLP              | Link 电源管理                          | 两种模式都使用                                                                                         |
| Link Management DLLP | L0p Link 管理                        | Flit Mode 使用                                                                                    |
| Vendor-Specific      | 厂商自定义                              | 需要实现相关使能机制                                                                                      |
| NOP / NOP2           | 不执行普通动作的占位/特殊控制                    | NOP2 为 Flit Mode 定义                                                                             |


### Flow Control dllp

#### Flow control dllp 的type怎么看？

Flow Control DLLP 的 Type Byte 不是单纯固定常数，而是把多个信息压入同一 Byte：
- bit 7:4：DLLP 家族和 Credit 类别
- bit 3  ：Shared / Dedicated Flow Control
- bit 2:0：VC[2:0]

**先读高位**

| 高位          | DLLP         |
| ----------- | ------------ |
| `0100 xxxx` | InitFC1-P    |
| `0101 xxxx` | InitFC1-NP   |
| `0110 xxxx` | InitFC1-Cpl  |
| `1100 xxxx` | InitFC2-P    |
| `1101 xxxx` | InitFC2-NP   |
| `1110 xxxx` | InitFC2-Cpl  |
| `1000 xxxx` | UpdateFC-P   |
| `1001 xxxx` | UpdateFC-NP  |
| `1010 xxxx` | UpdateFC-Cpl |

其中：
- `P`：Posted，请求不需要 Completion，例如常见 Memory Write；
- `NP`：Non-Posted，请求需要 Completion，例如 Memory Read；
- `Cpl`：Completion，对 NP 请求的响应；
- bit 3 为 0：Shared Flow Control；
- bit 3 为 1：Dedicated Flow Control；
- bit 2:0：Virtual Channel 编号。

所以其实只看 Byte0已经可以确定
1. 是Init还是update？[[DLL_DLLP#Q Flow control中 Init 和 Update 有什么区别？|两者区别？]]
2. 是哪一类Credit (P/NP/Cpl)？[[#Q 什么是Credit|Credit？]]
3. 属于哪个VC？[[DLL_DLLP#Q 什么是VC？|什么是vc？]]
4. 是Shared还是Dedicated？


#### FC的dllp
[[spec_chap3.pdf#page=22]]

| 字段           | 含义                                       |
| ------------ | ---------------------------------------- |
| HdrFC        | 某类 TLP Header 的 Credit 值                 |
| DataFC       | 某类 TLP Data Payload 的 Credit 值           |
| HdrScale     | Header Credit 的缩放因子                      |
| DataScale    | Data Credit 的缩放因子                        |
| VC[2:0]      | Credit 属于哪个 Virtual Channel              |
| P / NP / Cpl | Credit 属于 Posted、Non-Posted 或 Completion |

#### Scaled FC
```
HdrScale + HdrFC：Header Credit 计数
DataScale + DataFC：Data Credit 计数

其中
HdrFC：8 bit
DataFC：12 bit
HdrScale：2 bit
DataScale：2 bit
```

Scale 和 FC 之间是量量对应的关系，例如 HdrScale 用于解释 HdrFC，关系是 `实际 Credit 数值 = FC 字段 × Scale Factor`

**四种编码:**
![[scale_encodings.png]]

解读：

| Scale 编码 | Scale Factor | 实际含义                            |
| -------- | ------------ | ------------------------------- |
| `00b`    | ×1           | Scaled FC 没有启用                  |
| `01b`    | ×1           | Scaled FC 已启用，但仍按 1 个 Credit 计数 |
| `10b`    | ×4           | FC 字段每增加 1，表示 4 个 Credit        |
| `11b`    | ×16          | FC 字段每增加 1，表示 16 个 Credit       |

`00b` 和 `01b` 虽然都是乘 1，但含义不同：
- `00b`：使用旧的、未缩放的 Flow Control；
- `01b`：Scaled Flow Control 已协商成功，只是当前选择的倍率为 1。

当 Scaled Flow Control 已激活时，正常情况下必须使用 `01b`、`10b` 或 `11b`，不能再使用 `00b` 表示普通的有限 Credit 数值。

**Example**
假设某个 InitFC DLLP 中：

```
HdrScale = 10b
HdrFC    = 30
```

`10b` 表示乘 4：实际 Header Credit = 30 × 4 = 120，因此，它表示的不是 30 个 Header Credit，而是 120 个。

再例如：

```
DataScale = 11b
DataFC    = 100
```

`11b` 表示乘 16：实际 Data Credit = 100 × 16 = 1600

一个 Data Credit 的基本单位通常是 4 DW，也就是 16 Byte，因此从接收缓冲区容量角度看：

```
1600 × 16 Byte = 25,600 Byte
```

**sum**：Scale 缩放的仅仅是“Credit 数量”
[[#Q 为什么需要Scaled？]]
[[#Q Scaled FC中 scaled 值有效，但是data 全 0 呢？]]


## NOP and NOP2

### NOP DLLP
- Type 为 `31h`；
- 24-bit Type-specific information 可以是任意值；
- Receiver 完成完整性检查后，不执行普通动作并丢弃。

### NOP2 DLLP
- Flit Mode 使用；
- Type 编码为 `00h`，即复用 Non-Flit Ack 的编码；
- 其余 24 bits 必须为 0。

```text
Non-Flit 00h -> Ack
Flit     00h -> NOP2
```

NOP/NOP2 的重点不是承载业务，而是提供合法的空操作或满足某些协议/实现需要。

[[#Q: NOP TLP? NOP DLLP? NOP2 DLP?]]
[[#Q:为什么要在NOP的基础上新增NOP2?]]


## Link Management DLLP
Type 为 `28h`，用于 Flit Mode 下的 L0p Link Management。

它的 Type-specific information 包含：
- Link Management Type；
- L0p Priority；
- L0p Command；
- Response Payload；
- Link Width。

在 Non-Flit Mode 中，这个编码是 Reserved。Receiver 检查完整性后必须不采取动作并丢弃。


## Power Management DLLP
常见 Type：

| Type | 含义 |
|---:|---|
| `20h` | PM_Enter_L1 |
| `21h` | PM_Enter_L23 |
| `23h` | PM_Active_State_Request_L1 |
| `24h` | PM_Request_Ack |

这些 DLLP 的发送由组件的 Power Management logic 触发。

接收端：
1. 先由数据链路层确认其完整性；
2. 再把消息交给组件的电源管理逻辑。

数据链路层负责可靠承载，电源管理逻辑负责解释“进入哪个低功耗状态”。


## Vendor-Specific DLLP
Type 为 `30h`，后面的 24 bits 由厂商定义。

规范建议：
- 除非实现特定机制已启用，否则 Receiver 静默忽略；
- 除非实现特定机制已启用，否则 Transmitter 不应发送。

不同厂商把相同 24-bit 空间解释为不同命令。




## 问题与思考
### Q:在pcie gen6发布后，新增了flit mode，flit mode中使用DLP，那相对传统的DLLP是否就没有作用了？
DLLP依旧被使用，Flit Mode 只是改变了“DLLP 独立传输”的方式，而不是 DLLP 本身。

核心关系：
- 普通 DLLP：仍然存在，放入 Flit 的 DLP bytes。
- DLLP 独立 16-bit CRC：取消，由整个 Flit 的 CRC/FEC 保护。
- Ack/Nak DLLP：Flit Mode 不再使用，改为专用 DLP Symbols。
- InitFC、UpdateFC、Data Link Feature、PM、Link Management 等 DLLP：仍会使用。
- `Optimized_Update_FC`：作为性能优化补充 UpdateFC DLLP，并未完全替代它。

Flit Mode 没有废除 DLLP，而是改变了 DLLP 的承载方式和完整性保护方式。

| 问题                   | Non-Flit Mode     | Flit Mode                         |
| -------------------- | ----------------- | --------------------------------- |
| 普通 DLLP 是否仍存在        | 是                 | 是                                 |
| DLLP 怎样传输            | 作为独立的 6-Byte 包传输  | 4-Byte DLLP 内容放入 Flit 的 DLP bytes |
| DLLP 是否有自己的 CRC      | 有独立的 16-bit CRC   | 没有独立 DLLP CRC，由 Flit 的完整性机制保护     |
| Ack/Nak 是否是 DLLP     | 是，使用 Ack/Nak DLLP | 否，使用专用 DLP Symbols                |
| 重传单位                 | TLP               | Flit                              |
| Flow Control DLLP    | InitFC、UpdateFC 等 | 仍使用，还可配合 `Optimized_Update_FC`    |
| Link Management DLLP | 对这类编码检查后丢弃        | 用于 L0p Link Management            |

所以应该说是：**Flit Mode 仍然使用多种 DLLP，但不再使用 Ack DLLP 和 Nak DLLP。**另外：
- Gen6-capable 组件与旧组件连接时，为了向后兼容，可以在较低速率和传统模式下工作；
- 64.0 GT/s 链路使用 Flit Mode；
- 因此 PCIe 6.x 规范必须同时定义 Non-Flit Mode 与 Flit Mode 的 DLLP 行为。


### Q:什么是VC？
Virtual Channel，是一条PCIe物理Link上，可以划分多个逻辑上的Virtual Channel：
- VC0：默认 VC，必须支持
- VC1～VC7：可选
- 它们共享同一组物理 Lane，并不是另外拉了一条线

VC 的作用主要是把不同流量放进不同的逻辑队列，分别进行仲裁和流控。例如：

```
在同一条 PCIe Link
├── VC0：普通业务
├── VC1：高优先级业务
└── VC2：实时业务
```

因此，Flow Control DLLP 中的 **VC 编号**是在说明：

> “我现在通告的是哪个 Virtual Channel 的 Credit 信息。”

例如：

```
VC = 2
Type = Non-Posted
Header Credit = 8
Data Credit = 32
```

意思大致是：

> 接收端为 VC2 中的 Non-Posted TLP 提供了相应的 Header 和 Data 接收空间。


### Q:Flow control中 Init 和 Update 有什么区别？
Init有两种：**InitFC1 和 InitFC2**，这两种都只用于Flow control中的初始化，
		其中 InitFC1 用于初次交换接收能力，InitFC2 用于确认双端已经获得初始化后的信息
		两项确认之后，VC可以进入正常的Flow control工作

UpdateFC 是在有Init已完成的前提下，接收端给发送端更新buffer区的资源，告诉发送端可以发送哪个类型的credit了


### Q:什么是Credit？
credit类比成“发送许可”，其功能类似于流控，控制数据是否发送

场景：假设设备B作为接收端，处理速度不及设备A端的发送速度，那必须要限制A发送，不然B的buffer会被塞满。credit用来定义B端还能接收多少个数据，并且这个数据是区分类型的。其分类同样是基于流控的需要，分为
- Posted Header 缓冲区
- Posted Data 缓冲区
- Non-Posted Header 缓冲区
- Non-Posted Data 缓冲区
- Completion Header 缓冲区
- Completion Data 缓冲区

判断的逻辑
```
Credit
│
├── 属于哪种 TLP？
│   ├── P
│   ├── NP
│   └── Cpl
│
├── 用于哪部分？
│   ├── Header
│   └── Data
│
├── 属于哪个逻辑通道？
│   └── VC 编号
│
└── 缓冲资源怎样分配？
    ├── Shared
    └── Dedicated
```


### Q:为什么需要Scaled？
因为 DLLP 的大小是固定的：
- `HdrFC` 只有 8 bit；
- `DataFC` 只有 12 bit。

在没有 Scaled FC 时，协议允许的最大 outstanding Credit 是：

|Credit 类型|最大值|
|---|---|
|Header Credit|127|
|Data Credit|2047|
> [!note]
> 因为 FC 使用的是会回卷的计数器。为了在计数器回卷时仍然能够判断“接收端释放了多少”以及“发送端消耗了多少”，尚未归还的 Credit 不能跨越计数空间的一半。
> 因此把限制设定为：
> 
> 8 bit Counter： 最大 outstanding = 2^(8-1) - 1 = 127
>  
> 12 bit Counter： 最大 outstanding = 2^(12-1) - 1 = 2047

这个数量级的 credit 在低链路速率的情况下，基本上是够用的，但是随着 PCIe 速率的提升，可能会出现一种情况：
```
发送端高速发送 （发的太快）
    ↓
迅速耗尽 Credit
    ↓
接收端虽然正在处理数据，
但新的 UpdateFC 还在返回途中
    ↓
发送端只能暂停
    ↓
链路出现空洞，性能下降
```

出现了类似“时延积”的情况，因此其实要允许更多数据同时处于传输途中，所以scale的引入，是在不改动dllp的情况下，把 credit counter的有效可表达范围扩大了，可通告的 credit 数量大大提升：

| Scale | Header 最大 Credit | Data 最大 Credit |
| ----- | ---------------- | -------------- |
| ×1    | 127              | 2,047          |
| ×4    | 508              | 8,188          |
| ×16   | 2,032            | 32,752         |


### Q:Scaled FC中 scaled 值有效，但是data 全 0 呢？
乘法规则适用于正常的有限 Credit 数值。但是在 Flit Mode 的 `InitFC1/InitFC2` 中，如果：`HdrFC = 0 or DataFC = 0`

对应的 Scale 编码会被用于表达特殊状态：

| Flit Mode InitFC 中 FC=0 | 含义                         |     |
| ----------------------- | -------------------------- | --- |
| Scale=`00b`             | Infinite Credits，无限 Credit |     |
| Scale=`01b`             | Zero Credits，确实没有 Credit   |     |
| Scale=`10b`             | Merged Shared Credits      |     |
| Scale=`11b`             | Reserved                   |     |

**Example 1**
```
HdrFC = 0
HdrScale = 00b
```

不是“0 × 1 = 0”，而是：Infinite Header Credits

**Example 2**

```
HdrFC = 0
HdrScale = 01b
```

才表示：Zero Header Credits

这是 Spec 专门规定的特殊编码，不能只按乘法理解。

`Merged` 则表示 Shared Completion Credit 和 Shared Posted Credit 使用共同的 Credit Pool。它只适用于 Spec 允许的 Shared Credit 场景。

尤其要注意：

> 这种 `FC=0 + Scale` 的特殊解释用于初始化语义，不能看到运行中的 UpdateFC Counter 回卷到 0，就简单认为它表示 Zero 或 Infinite。



### Q: NOP TLP? NOP DLLP? NOP2 DLP?
| 名称        | 所属层               | 模式          | 位置                      | Type 编码               |
| --------- | ----------------- | ----------- | ----------------------- | --------------------- |
| NOP TLP   | Transaction Layer | Flit Mode   | Flit 的 TLP Bytes        | TLP Type=`00h`        |
| NOP DLLP  | Data Link Layer   | 两种模式均可      | DLLP/DLP 的 DLLP Payload | DLLP Type=`31h`       |
| NOP2 DLLP | Data Link Layer   | 仅 Flit Mode | DLP 的 DLLP Payload      | DLLP Type=`00h`，其余全 0 |

最关键的区分方法是：
> 先看它在 Flit 的哪个位置，再看 Type。不能只看到 `00h` 就判断类型。


- Non-Flit Mode 没有 NOP TLP
- 在 Non-Flit Mode 中，相同的 TLP Type 编码不是 NOP，而是 Memory Read 的编码之一
- NOP TLP 是一个 Transaction Layer Packet，只存在于 Flit Mode。

**NOP DLLP**
在 Flit Mode 中，DLLP 被放进 Flit 的 DLP 区域，由 Flit 级 CRC/FEC 保护，不再为它单独追加 DLLP CRC。

NOP DLLP 的接收规则很简单：

```
检查完整性
→ 直接丢弃
→ 不执行任何操作
```

它的 24-bit DLLP Type Specific Information 被定义为 arbitrary value，接收端不能依靠这 24 bit 获得标准协议含义。

它可以作为一个普通的、实现相关的空操作 DLLP。Spec 也明确说，NOP DLLP 的具体使用是 implementation specific。

**NOP2 DLLP**
NOP2 同样属于 Data Link Layer，但它只存在于 Flit Mode，其整个 DLLP Payload 都是 0

接收端收到 NOP2 后同样直接丢弃，但不执行任何操作

但它与普通 NOP DLLP 相比，多了两个重要性质：
1. 整个 4 Byte DLLP Payload 全是 0；
2. 它是一个特殊的“完全中性”占位符，不表示正常 DLLP 通信已经开始。


### Q:为什么要在NOP的基础上新增NOP2?
以下内容皆为推测：NOP2 不是为了再发明一次“什么也不做”，而是为了提供一个具有特殊编码和特殊状态语义的 NOP。

### 原因一：构造全 0 的 IDLE Flit

Spec Table 4-16 规定，IDLE Flit 中：

```
236 Byte TLP Bytes = 全部00h
DLP Byte 0～1      = 全部00h
DLP Byte 2～5      = NOP2 DLLP
```

由于 NOP2 本身也是全0，因此 IDLE Flit 的整个 TLP+DLP 内容可以为：

```
236 Byte TLP Bytes
    全0
+
6 Byte DLP Bytes
    全0
=
242 Byte全部为0
```

如果使用普通 NOP DLLP，那么 DLP 区域就不可能全为 0，所以普通 NOP DLLP 无法满足 IDLE Flit 要求的全 0 DLP 内容，而 NOP2 可以；<u>此外还可能会占用crc/ecc的资源？</u>

### 原因二：Flit 中始终存在 DLP 区域
Flit Mode 每个 Flit 都有固定的 6 Byte DLP：

```
每个Flit
+----------------------+------------------+
| TLP Bytes            | DLP Bytes        |
+----------------------+------------------+
```

即使当前：
- 没有 Flow Control DLLP；
- 没有 Power Management DLLP；
- 没有 Link Management DLLP；
- 没有其他有效 DLLP；

DLP 区域仍然物理存在，不能从 Flit 中删除。

于是需要一种值表达：
> 这个 DLLP Payload 位置存在，但当前没有任何有意义的 DLLP 信息。


### 原因三：NOP2 不表示 DLLP 通信已经准备好
Spec 在eq相关流程中规定：
- 某些阶段只允许发送 NOP2 DLLP；
- Upstream Port 收到 NOP2，不能据此解除对其他 DLLP 的阻塞；
- 必须收到一个 non-NOP2 DLLP，才能认为对端已经开始允许相应 DLLP 通信。

所以 NOP2 有一种比普通 NOP 多一层语义：

```
NOP DLLP：
一个正常格式的、没有动作的DLLP

NOP2 DLLP：
Flit/DLP结构不得不存在，
所以先放一个完全中性的全0占位符；
它不证明正常DLLP流程已经开始
```

如果这里只使用普通 NOP DLLP，接收端就无法通过“是否为 NOP2”区分：只是为了维持Flit结构而发送 or 已经开始发送普通DLLP流量






## 相关笔记 Relation


