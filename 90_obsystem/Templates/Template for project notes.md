---
tags:
status:
notetype: Structure
created: ${tp.date.now("YYYY-MM-DD HH:mm")}
modified:
---
# 🎯 Project Name

> [!abstract] 项目概述
> 

---

## 📋 项目信息

- **负责人**: 
- **开始时间**: 
- **目标完成**: 
- **当前状态**: 
- **优 先 级**: <%* tR += DataviewAPI.page(tp.file.title).priority %>

---

## 🎯 项目目标 (Goals & Success Criteria)

### 主要目标
- 

### 成功标准 (如何算成功?)
- 

---

## ✅ 任务清单 (Actionable Tasks)

所有链接到此项目并且是待办事项的任务都会被汇总在这里。

```dataview
TASK
FROM [[<%* tR += tp.file.title %>]]
WHERE !completed
GROUP BY file.link
```

---

## 📚 相关笔记与文档 (Related Notes & Documents)

所有链接到此项目的笔记（不包括项目本身和任务）都会被汇总在这里。

```dataview
TABLE WITHOUT ID
  file.link as "笔记名称",
  file.cday as "创建日期"
FROM [[<%* tR += tp.file.title %>]]
WHERE file.name != this.file.name AND !file.tasks
SORT file.cday DESC
```

---

## 🔍 问题与决策 (Issues & Decisions)

手动记录遇到的关键问题和做出的重要决策。

- [[ ]]
- [[ ]]

---

## 🎉 项目里程碑 (Milestones)

- [ ] 里程碑1：
- [ ] 里程碑2：

