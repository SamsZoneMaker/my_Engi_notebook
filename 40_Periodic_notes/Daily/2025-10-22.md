---
tags:
  - grain/daily
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
week: <% tp.date.now("YYYY-[W]ww") %>
created: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>
---
# <% tp.date.now("YYYY-MM-DD dddd") %>

> [!quote] 💭 今日一言
> 

---

## ✅ 今日三件要事 (Top 3 Priorities)
- [ ] 
- [ ] 
- [ ] 

## 📝 今日完成的任务
```dataview
TASK
FROM ""
WHERE completed AND completion = this.file.date
SORT file.ctime asc
```

## 📚 今日小结

### 学到的关键知识

### 遇到的问题

### 思考与想法

---

## 📌 今日新增或修改的笔记
```dataview
TABLE WITHOUT ID
  file.link as "笔记",
  choice(dateformat(file.cday, "yyyy-MM-dd") = dateformat(this.file.date, "yyyy-MM-dd"), "✨ 新增", "🔄 更新") as "类型",
  file.mtime as "修改时间"
FROM ""
WHERE (dateformat(file.cday, "yyyy-MM-dd") = dateformat(this.file.date, "yyyy-MM-dd") OR dateformat(file.mday, "yyyy-MM-dd") = dateformat(this.file.date, "yyyy-MM-DD")) AND file.name != this.file.name
SORT file.mtime DESC
```
