---

tags: - 
date: <% tp.date.now("YYYY-MM-DD") %> 
day: <% tp.date.now("dddd") %> 
week: <% tp.date.now("YYYY-[W]ww") %> 
created: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>

---
# <% tp.date.now("YYYY-MM-DD dddd") %>

> [!quote] 💭 今日一言

---

## ✅ 今日三件要事 (Top 3 Priorities) 
- [ ] 
- [ ] 


## 📚 今日小结


### 学到的关键知识

### 遇到的问题

### 思考与想法

---

## 💼 工作记录

### 完成的任务

### 项目进展

- #proj/retimer

---

## 📌今日新增/更新的笔记 
````markdown 
```dataview 
LIST 
WHERE file.cday = this.file.date OR file.mday = this.file.date 
WHERE file.name != this.file.name 
SORT file.mtime desc

```
````





