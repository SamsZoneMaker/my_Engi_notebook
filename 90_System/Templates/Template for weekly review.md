---
date: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - type/weekly
---
## 本周完成

-

## 未完成与调整

```tasks
not done
due before tomorrow
sort by priority
sort by due
hide tags
```

## Inbox 清理

```dataview
TABLE WITHOUT ID
  file.link AS "待整理",
  file.ctime AS "收集时间"
FROM "00_Inbox"
SORT file.ctime ASC
```

## 本周形成的笔记

```dataview
LIST
FROM ""
WHERE file.cday >= date(today) - dur(7 days)
  AND !contains(file.path, "80_Periodic")
  AND !contains(file.path, "90_System/Templates")
  AND !contains(file.path, "99_Archive")
SORT file.ctime DESC
```

## 下周聚焦

- [ ] 下周最重要的行动 #task ⏫

## 系统维护

- Inbox 是否已经处理？
- 新笔记是否至少进入一张 MOC？
- 无截止日期任务是否仍然需要执行？
