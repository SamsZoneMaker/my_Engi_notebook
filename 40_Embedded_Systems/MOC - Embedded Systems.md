---
created: 2026-07-27
tags:
  - type/moc
  - topic/embedded
---
> [!abstract] 主题说明
> 从芯片架构、启动与中断，到高速接口、工具链和实际固件项目。

## 架构与处理器

- [[芯片架构 - 核心概念与分类]]
- [[MOC - RISC-V]]
- [[MOC - Computer Architecture]]

## 固件构建

- [[MOC - Toolchain]]
- [[MOC - Build Systems]]

## 高速接口

- [[MOC - PCIe]]
- [[MOC - SerDes]]
- [[MOC - Hardware]]

## 项目实践

- [[SoC 固件评审记录]]
- [[MPRO 学习笔记]]
- [[wAPI 学习笔记]]
- [[Dragon 构建脚本解析]]

## 最近更新

```dataview
LIST
FROM #topic/embedded OR #topic/pcie OR #topic/serdes OR #topic/hardware
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 10
```
