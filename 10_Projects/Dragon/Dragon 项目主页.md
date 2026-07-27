---
created: 2026-07-27
tags:
  - type/project
  - project/dragon
status: active
---
> [!abstract] 项目入口
> Dragon 项目的构建系统与日志模块设计资料。

## 当前重点

- 日志模块需求、方案与实现文档的一致性。
- 构建脚本和 Makefile 的调用关系。

## 日志模块

- [[日志模块更新设计要求]]
- [[日志模块重构设计方案]]：从需求到接口、缓冲区、解析工具和测试计划的完整设计。

## 构建系统

- [[Dragon 构建脚本解析]]
- [[日志系统 Makefile 解析]]
- [[Kbuild - fixdep 依赖优化]]

## 项目任务

```tasks
not done
folder includes 10_Projects/Dragon
sort by priority
sort by due
hide tags
```

## 最近更新

```dataview
LIST
FROM "10_Projects/Dragon"
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 8
```
