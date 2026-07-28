---
created: 2026-07-27
tags:
  - type/moc
  - topic/risc-v
---
> [!abstract] 学习路径
> RISC-V 主题从指令集和特权级出发，逐步进入异常中断、启动流程、内存系统与实际固件。

## 当前笔记

- [[RISCV - 中断机制]]：中断、异常、特权模式和向量入口。

## 学习框架

1. 指令集、寄存器和调用约定。
2. M/S/U 特权级与 CSR。
3. 异常、中断、委托与向量模式。
4. 启动流程、内存映射和链接布局。
5. 缓存、MMU 与多核协同。
6. 在项目中完成启动、中断和调试实践。

## 相邻主题

- [[MOC - Computer Architecture]]：提供处理器、内存和执行模型基础。
- [[MOC - Embedded Systems]]：RISC-V 在固件和 SoC 中的落地场景。
- [[MOC - Toolchain]]：编译、链接和 ELF 是构建 RISC-V 固件的基础。
- [[Dragon 项目主页]]：当前向量中断学习的项目背景。
