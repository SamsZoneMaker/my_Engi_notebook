---
tags:
  - type/dashboard
---
## 快速入口

- `= link("80_Periodic/Daily/" + dateformat(date(today), "yyyy-MM-dd"), "今日笔记")`
- [[任务|任务中心]]
- [[笔记工作流]]
- [[MOC - Programming]]
- [[MOC - Computer Systems]]
- [[MOC - Embedded Systems]]
- [[MOC - PCIe]]

## 笔记活动

```contributionGraph
title: '过去 365 天创建的笔记'
days: 365
query: '-"90_System/Templates" and -"99_Archive"'
dateField: 'file.ctime'
startOfWeek: 1
showCellRuleIndicators: true
```

## 逾期任务

```tasks
not done
due before today
sort by priority
sort by due
hide tags
```

## 今日到期

```tasks
not done
due today
sort by priority
hide tags
```

## 高优先级任务

```tasks
not done
priority is above medium
sort by due
hide tags
```

## 接下来 14 天

```tasks
not done
due after today
due on or before in 14 days
sort by due
sort by priority
hide tags
```

## 无截止日期的任务

```tasks
not done
no due date
sort by priority
limit 10
hide tags
```

## Inbox 待整理

```dataview
TABLE WITHOUT ID
  file.link AS "笔记",
  file.ctime AS "收集时间",
  file.mtime AS "最近修改"
FROM "00_Inbox"
SORT file.ctime ASC
```

## 活跃项目

```dataview
TABLE WITHOUT ID
  file.link AS "项目笔记",
  status AS "状态",
  file.mtime AS "最近修改"
FROM "10_Projects"
WHERE status = "active"
  AND endswith(file.name, "项目主页")
SORT file.mtime DESC
```

## 最近编辑

```dataview
TABLE WITHOUT ID
  file.link AS "笔记",
  file.folder AS "位置",
  file.mtime AS "修改时间"
FROM ""
WHERE file.name != this.file.name
  AND !contains(file.path, "90_System/Templates")
  AND !contains(file.path, "99_Archive")
  AND !contains(file.path, "assets")
SORT file.mtime DESC
LIMIT 10
```

## 待建立连接

```dataview
LIST
FROM #type/knowledge
WHERE length(file.inlinks) = 0
  AND length(file.outlinks) = 0
SORT file.mtime DESC
LIMIT 10
```
