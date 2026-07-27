## 今日聚焦

- `= link("40_Periodic_notes/Daily/" + dateformat(date(today), "yyyy-MM-dd"), "今日笔记")`
- [[待办]]

## 最近笔记

```dataview
LIST
FROM ""
WHERE file.name != this.file.name
  AND !contains(file.path, "90_obsystem/Templates")
  AND !contains(file.path, "99_Archives")
SORT file.mtime DESC
LIMIT 8
```

## 最近项目文档

```dataview
LIST
FROM "20_Project"
SORT file.mtime DESC
LIMIT 10
```
