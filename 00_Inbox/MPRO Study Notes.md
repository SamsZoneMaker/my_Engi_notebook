author: Sam (desen.li@wisewavetech.com)

sources: 

[1] alphawave_ip_fw_user_guilde

[2] alphawave_ip_fw_app_note

---

# MPRO Study Notes



## Overview

**MPRO** 是一个代码仓库，包含用 Python 编写的固件代码 (fw code)、设计规范 (spec) 以及用于编译固件的工具链 (toolchains)。这些工具可以将固件代码编译成适用于硬件加载的 hex 文件，这些文件会被加载到设备的 SRAM 和 CSR 空间中，并最终在 MFSM 硬件上运行。

[**fw code**] 固件代码是直接运行在硬件设备上的程序，通常负责底层硬件的控制和管理

[**spec**] 描述了固件的设计、功能或使用的详细文档

[**toolchains**] 指的是编译和构建固件所需的工具集合，包括编译器、链接器、调试器等

[**hex files**] 一种用于表示二进制数据的文本格式，常用于存储机器代码，便于加载到硬件设备中，Hex 文件是嵌入式开发的最终产物，包含编译好的机器指令，用于在目标硬件上运行

[**SRAM**] Static RAM，是一种高速内存，用于存储程序数据

[**CSR**] Control and Status Registers，是硬件中的控制寄存器，用于设置或获取硬件状态。

[**MFSM**] Multi-Function State Machine，一个特定的硬件模块、处理器或微架构的名称



## Repo Structure - 

### Programmer/

#### Sequences/

一个代码块，既包含Python的脚本代码，也包含原生汇编代码（raw assembly code）

​      **Python代码**：用于描述算法、逻辑控制和数据处理，具有更高的抽象性，便于开发和维护。

​      **汇编代码**：用于实现与硬件直接交互的功能，例如控制寄存器、设置硬件状态，或者执行精确时间控制的操作。

Python 代码和汇编代码通过一个特定的编译器被转换为 **Hex 文件**，这个编译器需要能够将 Python 代码翻译为底层指令，同时正确处理汇编代码，编译得到的 Hex 文件会被加载到 **MFSM**上运行。

##### 用处

**开发效率与性能兼顾**：

- 使用 Python 提高开发效率和可读性。
- 使用汇编实现对硬件的精细控制。

**面向硬件的程序开发**：

- 这种方法适合硬件驱动程序开发、实时系统或嵌入式系统开发。
- 汇编代码可以直接操控寄存器或内存，而 Python 提供逻辑控制的便捷接口。

##### 目录

~~~
|-- sequences
|   |-- Power/*.py          # for power state changes
|   |-- Rate/*.py           # for rate and width changes
|   |-- Equalization/*.py   # for equalization and evaluation
|   |-- Anlt/*.py           # auto negotiation and link training for Eth
~~~



#### configurator/

##### Function

1. **Auto-generates per-rate digital PHY settings**
   - **含义**
     这部分功能会根据每个速率（rate）自动生成数字 PHY（物理层）设置。
   - **背景**
     在通信系统中，PHY 是硬件的一部分，负责处理物理层的通信（例如信号调制和解调、信号编码等）。不同的数据速率（rate）可能需要不同的设置（例如时钟频率、信号幅度、采样率等）。此脚本的作用是为每种速率自动生成适合的配置，减少手动调整的工作量。

2. **Function of refclk, symbol rate, modulation**

   - **含义**
     脚本的功能可能依赖于以下三个关键参数：

     - **refclk（参考时钟）：** 用于驱动系统的基准时钟信号。
     - **symbol rate（符号率）：** 指每秒传输的符号数量，是衡量通信系统速率的一个指标。
     - **modulation（调制方式）：** 指信号如何被编码（例如 QAM、PSK 等），用于表示数据的具体方法。

   - **作用**

     这些参数会影响 PHY 的配置。例如，符号率和调制方式会决定所需的频宽和信号处理方式，而参考时钟（refclk）决定了系统时序。

3. **PLL calibration config （锁相环校准配置）**

   - **含义**
     负责设置和校准锁相环（PLL，Phase-Locked Loop），用于生成所需频率的信号。校准确保生成的时钟信号具有高精度和低抖动。
   - **作用**
     配置脚本可能包括参数的自动调整，以适配各种速率或符号率，确保时钟信号在不同情况下正常工作。

4. **Datapath（数据路径）**

   - **含义**
     数据路径是指数据从输入到输出的处理流程，包括信号编码、解码、调制、均衡等操作。
   - **作用**
     脚本可能还配置或优化数据在处理链路中的传输，确保其性能和效率符合设计要求。



##### User

运行代码之后会生成 `out_dir` 文件夹，里面包含`rate_out.csv` 和 `delay.csv`表格，这些表格可用于debug。



#### complier/

编译器会将 Python 代码转换成专用的汇编代码，Hex 文件通常包含地址和值的列表，表示每条指令或数据在硬件存储中的位置（地址）及其内容（值），格式类似：

~~~assembly
0x0002: 0x1234
0x0001: 0xABCD
~~~



#### specs/

速率等规格的设置，定义了速率以及时钟的频率



### Scripts/

some util scripts for gitlab ci/cd pipeline and svn Mpro updates



### Integration/

contains RTL.Makefile which generates the fw for use in Digital Simulations



### Release/

Scripts to package the Mpro toolchain for delivering to the customers.



