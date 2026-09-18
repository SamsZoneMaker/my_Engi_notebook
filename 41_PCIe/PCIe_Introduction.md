---
created: 2026-07-29
tags:
  - type/knowledge
---
> [!abstract] 核心结论
> 这篇补笔记主要用于记录入门PCIe时刚接触到宏观理念，不涉及细节

## 技术参数
PCIe 全称**Peripheral Component Interconnect express**，中文 **高速串行计算机扩展总线**

PCIe是第三代I/O互联标准，ISA → PCI → PCIe

### Lane
把 PCIe 想象成一捆"水管"，每一根水管就是一条 **lane**，是最基本的物理传输通道，由一对差分信号线组成（发送方向 + 接收方向，各一对，所以其实是 2 对 4 根线）。

多条 lane 可以捆在一起工作，形成更宽的链路，常见宽度 x1/x2/x4/x8/x16/x32，数字越大代表带宽越大。比如显卡通常用 x16，M.2 SSD 常用 x4。
<br>
### 速率单位 GT/s
GT/s = **G**iga**T**ransfers per **s**econd

这个单位算的是"传输次数"，不是"比特数"。[[PCIe_Introduction#Q 为什么不直接用 Gbps？|?为什么不直接用 Gbps表示速度？]]
<br>
### 编码开销
- **8b/10b 编码**（Gen1/Gen2）：每传输 10 bit，其中只有 8 bit 是有效数据，2 bit 是开销 → 有效效率 80%
- **128b/130b 编码**（Gen3/Gen4/Gen5）：每传输 130 bit，其中 128 bit 是有效数据 → 有效效率约 98.5%，这也是为什么从 Gen3 开始换算比例明显提高了（不再是简单的 ×0.8）

结合编码开销和速率，可以知道Gbps是什么单位
```
Gen1: 2.5 GT/s × (8/10)  = 2.0 Gbps/lane
Gen3: 8 GT/s × (128/130) ≈ 7.877 Gbps/lane
```
  
| gen  | GT/s per lane | 编码      | Gbps per lane |
| ---- | ------------- | ------- | ------------- |
| gen1 | 2.5           | 8/10    | 2Gbps         |
| gen2 | 5             | 8/10    | 4Gbps         |
| gen3 | 8             | 128/130 | 7.877Gbps     |
| gen4 | 16            | 128/130 | 15.75Gbps     |
| gen5 | 32            | 128/130 | 31.50Gbps     |
| gen6 | 64            | 128/130 | 63.00Gbps     |

<br>

### 带宽
**总速率 = 单 lane 速率 × lane 数量**，并且 PCIe 是**全双工**（发送和接收各自独立、互不占用带宽），所以一个 x16 的 Gen4 链路：
- 单向带宽 = 16 GT/s × 128/130 × 16 lane ≈ 252 Gbps ≈ 31.5 GB/s
- 因为全双工，收发方向各有这么多带宽，不是共享的

> [!tip]
> GT/s 描述的是单个 lane 的"传输次数速率"，它和 lane 数量无关，是一个固定值（由 PCIe 代数决定），带宽的增长靠堆 lane 数量或者升代两种方式。



## PCIe Topology
![[pcie_topology.png|500]]
如图所示是pcie的经典拓扑结构，其拓扑本质是一棵树，包括了
### 1. 三种核心组件
- **RC（Root Complex）**：树的根，挂在 CPU/内存控制器上，是 CPU 访问 PCIe 设备的入口。RC 内部通常包含：
    - Host Bridge：连接 CPU 总线和 PCIe 域的桥
    - PCI-PCI Bridge：RC 往下引出的端口（有时叫 Root Port）
    - RCiEP（Root Complex Integrated Endpoint）：直接集成在 RC 里的端点设备，不通过 Root Port 挂载
- **Switch（交换机）**：用来扩展端口数量，可以级联（一个 switch 下面再接 switch）。内部结构：
    - Upstream Port（连向 RC 方向的口）
    - Downstream Port（若干个，连向下游设备的口，本质也是 PCI-PCI Bridge）可以理解成 switch 就是"网线的交换机"，一进多出，把一条链路分给多个下游设备。
- **Endpoint（端点）**：树的叶子节点，真正的功能设备，比如网卡、SSD、显卡。

### 2. Link 和 Port

- **Link**：两个 PCIe 组件之间实际的物理连接（一组 lane）
- **Port**：Link 两端各自设备上对应的**逻辑接口**。注意 Port 不是一个实体元件，而是设备内部"这一路连接对应的逻辑概念"——比如 RC 上引出的一个 Root Port，或者 switch 上的一个 Downstream Port。

可以这样理解：Link 是"线"，Port 是"线两端插头所在的逻辑位置"。

### 3. Host

拓扑图里最顶层是 RC，RC 挂在 CPU 上。跑在 CPU 上、负责管理和枚举这整棵 PCIe 树的操作系统/软件系统，就称为 **Host**（比如 Linux 内核里的 PCIe 子系统，负责扫描总线、分配资源、加载驱动）。


## BDF
![[PCIe_BDF.png|500]]

BDF 是 **Bus + Device + Function** 的总称，是 PCIe 拓扑中给每一个"功能单元"分配的唯一地址编号，格式通常写作 `BB:DD.F`（总线号:设备号.功能号）。它的作用类似于 PCIe 世界里设备的"门牌号"——Host 软件枚举总线时，靠这个三元组来唯一定位、访问、配置每一个设备
<br>
### Bus 总线
参考图，每个component之间的黑色粗线，都标明了Bus号，Bus 0、Bus 1、Bus 2…

有意思的点在于，每经过一个 P2P（PCI-PCI Bridge，包括 Virtual P2P）桥接后，总线号就会 +1（或者跳到桥分配的新总线号）

例如.
- Host/PCI Bridge 直接管的是 **Bus 0**（RC 内部这一层）
- Bus 0 上的 Virtual P2P 往下桥接出去后，链路变成了 **Bus 1**
- Bus 1 上的 Virtual P2P 再往下桥接，又分出了 **Bus 2**
<br>
### Device
同一条总线（Bus）上可以挂多个独立设备，Device 号就是用来区分同一条总线下的不同设备的。

图中 Bus 0 这条总线上就挂了 3 个东西：

- Bus 0, **Dev 0**, Func 0 → 左边的 Virtual P2P
- Bus 0, **Dev 1**, Func 0 → 中间的 Virtual P2P
- Bus 0, **Dev 2**（图中另一个 Integr. EP）

可以看到它们都在 Bus 0 上，但 Dev 号不同，说明它们是挂在同一条总线上的不同"槽位"设备。同理 Bus6 上也挂了 Dev1、Dev2、Dev3 三个 Virtual P2P。
<br>
### Function（功能号）
**一个 Device 内部还可以细分出多个 Function**，也就是一个物理设备对外表现为多个逻辑功能。这在你图里体现得非常直观，右下角两个红字标注正好是两种典型情况：

#### 单D多F（单设备多功能）
左下角 Bus3 上的 `Dev0` 下面同时有 `Function 0` 和 `Function 1` 两个方框——这是**同一个物理设备**（比如一张网卡）对外暴露了两个独立的功能接口，各自有自己的配置空间，可以被当成两个"独立设备"分别驱动。这在多功能网卡、多队列控制器上很常见。

#### 多D单F（多设备单功能）
右下角红框里的 PCI Bus9 上，挂了三个 **PCI Device**（Dev 1、Dev2、Dev3），每个都只有 Func0——这是传统并行 PCI 总线的典型拓扑：一条总线上并排挂多个独立设备，每个设备只有一个功能。这也说明了为什么需要 `Express PCI Bridge`：PCIe 要连接传统 PCI 总线时，需要一个桥接器做协议转换。
<br>
### 总结
每一个方框在图中的唯一坐标，就是它的 BDF。**Host 软件枚举 PCIe 拓扑时，本质上就是从 Bus0 开始，沿着每个 P2P 桥往下递归遍历，给沿途发现的每个 Device/Function 分配并记录一个 BDF**，这样后续访问某个具体设备的配置空间时，直接用 BDF 做索引即可定位。
[[PCIe_Introduction#Q 为什么 PCIe_Introduction BDF 图中用了大量的"Virtual" P2P？why virtual？|❓为什么图里的P2P是'virtual'?]]

## 分层结构
要理解PCIe，其分层架构的设计是必须要理解的。
![[PCIe_Layer_Structure.png|1200]]
### 为什么要分层？
参考OSI模型的思路，**每一层只负责自己的事，向上提供服务，向下依赖服务**。发送时逐层"加头加尾"（封装），接收时逐层"校验并剥离"（解封装）。好处是协议演进时各层可以独立替换 —— 比如 Gen3 把物理层的 8b/10b 换成 128b/130b，事务层完全不用改。

PCIe 规范定义的是 三层：
- Transaction Layer 
- Data Link Layer
- Physical Layer

图中最上层有一层 `Software Layer`，但是**Software Layer 不是协议的一部分**，它是OS和驱动对配置空间、MMIO的读写行为。CPU一条 `mov` 指令访问BAR空间，由RC硬件翻译成一个Memory Write TLP —— 软件层只提供"地址 + 事务类型 + 数据"
<br>
### Transaction Layer 事务层
事务层也称传输层

核心产物：TLP = Header + Data Payload + ECRC [[PCIe_Introduction#Q 什么是TLP?为什么说是事务层的核心？|TLP详解]]
- **Header**：3 或 4 个 DW（32/64 位地址），含事务类型、长度、Requester ID、Tag、地址等
- **Data Payload**：可选，读请求就没有 payload
- **ECRC**：可选的 32 位端到端校验，**跨 Switch 也有效**

图中该层的四个方框是其四大职能：

|模块|作用|
|---|---|
|**Flow Control**|基于 Credit 的流控。接收方通过 DLLP 告知自己还有多少 buffer，发送方额度不够就不发。**这是 PCIe 不会因缓冲区溢出而丢包的根本原因**|
|**Virtual Channel Management**|TC（Traffic Class）→ VC 映射，为不同流量提供独立的 buffer 和 credit，实现 QoS|
|**Ordering**|生产者-消费者模型的排序规则，Posted 不能被 Non-Posted 超越等；可用 Relaxed Ordering 放松|
|**VC Arbitration**|多个 VC 争抢链路时的仲裁策略（严格优先级 / Round Robin 等）|

另外图上没画但很重要的分类：
- **Posted**：Memory Write、Message —— 发出去不等回复
- **Non-Posted**：Memory Read、IO、Configuration —— 必须等 Completion（CplD）
<br>
### Data Link Layer（数据链路层）
**职责：保证链路两端之间的可靠传输（逐跳，link-by-link，不跨 Switch）**- 负责“可靠传输”。确保 TLP 包能“安全、按序”地从 A 点传到 B 点。它会给 TLP 加上序号和 CRC 校验，并使用 **DLLP** (Data Link Layer Packet) 包来进行 ACK/NAK 确认。

对 TLP 做的事很简单 —— 前面加 **Sequence Number**（2B），后面加 **LCRC**（4B），就成了图中的 Link Packet：

```
[Seq(2B)] [        TLP        ] [LCRC(4B)]
```

配套的重传机制（图中左侧）：
- **TLP Retry Buffer**：每个发出的 TLP 都留一份副本，收到对端 Ack 才释放
- 收到 **Nak** 或超时 → 从 Retry Buffer 重传
- 接收侧 **TLP Error Check**：校验 LCRC 和序列号连续性，对了回 Ack，错了回 Nak


**DLLP**（Data Link Layer Packet）是这一层自己的包，固定长度，不来自事务层也不上交给事务层：
- Ack / Nak
- Flow Control：InitFC1、InitFC2、UpdateFC
- Power Management

**DLLP报文的核心：** 
1. 对tlp的封装
2. 用于数据链路层的控制，继而保证dllp传输的可靠性

**Mux / De-mux**：发送时把 TLP 和 DLLP 复用进同一条链路，接收时靠帧符号区分开 —— 图里的梯形。
<br>
### Physical Layer（物理层）
物理层分为逻辑层和电器层，内容较多，暂不赘述

发送路径（参考图中自上而下）：
1. **加帧**：Start / End 符号 → Physical Packet。（注：图画的是 Gen1/2 的 STP/END 控制字符；Gen3+ 改用 4 字节 STP Token，结束由 token 里的长度字段隐含，不再有独立 End）
2. **Encode**：Gen1/2 用 8b/10b；Gen3+ 用 128b/130b + 扰码
3. **Parallel-to-Serial**：并串转换，多 lane 时还要做 byte striping
4. **Differential Driver**：差分信号驱动出去

接收路径完全对称：差分接收 → 串并转换 → 解码 → 去帧。

**Link Training（LTSSM）** 单独画在中间，因为它双向都要用：链路宽度/速率协商、lane 极性反转、lane 反序、去偏斜（deskew）、Gen3+ 的均衡（Equalization）。
[[PCIe_Introduction#Q 什么是LTSSM?|什么是LTSSM?]]
<br>
### 补充
图中在Receive路径上，有几个红叉，代表**这些信息在该层处理完毕之后，不会往上传（往下一个待处理层传）**，具体如下

| 位置  | 去掉            | 为什么                             |
| --- | ------------- | ------------------------------- |
| 物理层 | Start / End   | 帧定界符只在物理层有意义                    |
| 链路层 | Sequence、LCRC | 校验完就没用了；DLLP（Ack/Nak/CRC）整个被消费掉 |
| 事务层 | ECRC          | 端到端校验做完即丢弃，交给软件层的只有地址/类型/数据     |

**所以红叉 = 解封装。** 一个包从线上进来，每往上走一层就"瘦"一圈，最后交到软件





## 问题与思考
### Q:为什么不直接用 Gbps？
因为 PCIe 物理层传输时会加入**编码**，编码会引入额外的冗余位（用于时钟恢复、保证信号翻转等），所以"传输次数"和"有效数据速率"不是一回事，需要做换算。

### Q:为什么[[PCIe_Introduction#BDF]]图中用了大量的"Virtual" P2P？why virtual？
图中很多桥叫 **Virtual P2P**，这是因为在 PCIe 里，一个物理 Switch 内部的多个 Downstream Port，从软件枚举的角度看，都被抽象成标准的 PCI-PCI Bridge 结构（哪怕物理上并不是真正独立的 PCI 桥芯片），这样可以复用传统 PCI 总线枚举的软件逻辑，兼容性更好。这也是为什么 Switch 内部会画出多个"Virtual P2P"框而不是画成一个整体。

### Q:什么是TLP?为什么说是事务层的核心？
TLP 是**Transaction Layer Packet事务层数据包**，PCIe 上传输"有意义的业务数据"的唯一载体。你在 PCIe 上做的一切实际工作 —— 读寄存器、写内存、发中断 —— 最终都是一个 TLP，TLP通常的结构

```
结构（DW = 4 字节）：
+--------+------------------+---------+---
| Header | Data Payload     | ECRC    | 
| 3~4 DW | 0 ~ 1024 DW      | 0/1 DW  | 
+--------+------------------+---------+---
```

**四大类事务：**

|类型|例子|是否等回复|
|---|---|---|
|Memory|MRd / MWr|读要等，写不等|
|I/O|IORd / IOWr|要等（已废弃，仅兼容）|
|Configuration|CfgRd0/1, CfgWr0/1|要等|
|Message|INTx、PME、Error|不等|

> **Posted vs Non-Posted** 是理解 TLP 行为的关键分水岭：
> - **Posted**（MWr、Message）：发出去就当完成了，不需要对方回任何东西。所以写操作很快，但你**不知道它到底成没成功**。
> - **Non-Posted**（MRd、Cfg、IO）：发出去必须等一个 **Completion**（CplD 带数据 / Cpl 不带数据）回来。

**补充：Header 里几个常用字段**
- `Fmt/Type`：事务类型 + 有无 payload + 3DW 还是 4DW 头
- `Length`：payload 长度，单位是 DW，最大 1024 DW = 4KB
- `Requester ID`：Bus:Device:Function，Completion 靠它路由回来
- `Tag`：区分同一个 Requester 发出的多个未完成读；Tag 数量决定了你能同时挂多少个 outstanding read，**是读带宽的直接瓶颈**
- `TC`：Traffic Class，映射到 VC
- `Attr`：Relaxed Ordering、No Snoop

### Q:什么是LTSSM?
Link Training and Status State Machine, **链路训练与状态状态机**，物理层里的控制逻辑。它的任务是：**在完全没有软件参与的情况下，让两端硬件自己把链路协商起来**。换言之，上电后什么都还没做，LTSSM 已经在跑了。等 BIOS 开始枚举时，链路早就是 L0 了

```
Detect → Polling → Configuration → L0 
  ↑                                ↓ 
  └────── Recovery ←────────────── ┤ 
                                   ↓ 
                            L0s / L1 / L2 (低功耗)
```
其中：

| 状态                                  | 干什么                                                             |
| ----------------------------------- | --------------------------------------------------------------- |
| **Detect**                          | 上电起点。通过检测接收端的电气阻抗，判断对面有没有插东西                                    |
| **Polling**                         | 收发 TS1/TS2 训练序列，建立位同步和符号同步，确定极性是否接反（Polarity Inversion）         |
| **Configuration**                   | 协商链路宽度（x1/x4/x16）、分配 Lane 号、处理 Lane Reversal、多 lane 去偏斜（Deskew） |
| **L0**                              | **正常工作态**，TLP 和 DLLP 在这里跑                                       |
| **Recovery**                        | 出错或要变速时进来。Gen1→Gen3 的速率切换、Gen3+ 的均衡（Equalization）都在这里做          |
| **L0s / L1**                        | ASPM 低功耗态，L0s 恢复快（ns 级），L1 省得多但恢复慢（μs 级）                        |
| **L2 / L3**                         | 深度省电 / 完全断电                                                     |
| **Disabled / Loopback / Hot Reset** | 调试和复位用                                                          |





## 相关笔记 Relation

- [[ ]]

## 来源 Reference