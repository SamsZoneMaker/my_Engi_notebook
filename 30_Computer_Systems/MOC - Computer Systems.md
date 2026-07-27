---
created: 2026-07-27
tags:
  - type/moc
  - topic/computer-systems
---
> [!abstract] 使用方式
> 从处理器与内存、指令集和操作系统，理解程序如何在真实计算机系统中执行。

## 核心入口

- [[MOC - Computer Architecture]]：程序、指令、内存和处理器的基础关系。
- [[MOC - RISC-V]]：从具体指令集进入特权架构、中断和启动流程。
- [[MOC - Operating Systems]]：进程、文件接口和运行时资源管理。
- [[MOC - Toolchain]]：源码如何经过编译、链接形成 ELF 和固件。

## 相邻主题

- [[MOC - Programming]]：从系统原理进入具体语言。
- [[MOC - Embedded Systems]]：计算机系统知识在芯片与固件中的应用。

## 最近更新

```dataview
LIST
FROM #topic/computer-systems OR #topic/computer-architecture OR #topic/risc-v OR #topic/operating-systems
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 10
```
