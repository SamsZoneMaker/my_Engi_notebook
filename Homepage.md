---
modified: 2025-10-22  16:54:48
---
# 🏠 Dashboard

## 🔥 今日聚焦
- [[<% tp.date.now("YYYY-MM-DD") %>|今日笔记]]
- [[待办]]

## 📚 最近笔记
\```dataview
LIST
FROM ""
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 5
\```

## 🎯 进行中的项目
```dataview
TABLE 
  status,
  priority
FROM #type/project
WHERE status = "active"
```