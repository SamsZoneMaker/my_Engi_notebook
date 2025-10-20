## <%* const topic = await tp.system.prompt("主题名称（如：Python、RISC-V）:"); if (!topic) { new Notice("已取消创建"); return; } _%>

tags:

- grain/moc
- domain/<% topic.toLowerCase() %> type: moc topic: <% topic %> created: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %> modified: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>

---

# 🗺️ <% topic %> - 知识地图

> [!abstract] 📋 概述 这是关于 <% topic %> 的知识索引和导航中心

---

## 📊 统计信息

```dataview
TABLE 
  length(file.inlinks) as "被引用",
  length(file.outlinks) as "引用",
  status as "状态",
  modified as "最后修改"
FROM #domain/<% topic.toLowerCase() %>
WHERE file.name != this.file.name
SORT modified DESC
LIMIT 10
```

---

## 🎯 学习路径

### 1️⃣ 基础知识

```dataview
LIST
FROM #domain/<% topic.toLowerCase() %> AND #level/basics
WHERE file.name != this.file.name
SORT file.ctime ASC
```

### 2️⃣ 进阶内容

```dataview
LIST
FROM #domain/<% topic.toLowerCase() %> AND #level/intermediate
WHERE file.name != this.file.name
SORT file.ctime ASC
```

### 3️⃣ 高级主题

```dataview
LIST
FROM #domain/<% topic.toLowerCase() %> AND #level/advanced
WHERE file.name != this.file.name
SORT file.ctime ASC
```

---

## 📚 核心笔记

### 重要概念

- [[]]
- [[]]
- [[]]

### 实践应用

- [[]]
- [[]]

---

## 🔗 相关主题

- [[]] - 相关领域
- [[]] - 依赖知识
- [[]] - 扩展阅读

---

## 📖 参考资料

```dataview
TABLE 
  source_type as "类型",
  rating as "评分",
  status as "状态"
FROM #resource AND #domain/<% topic.toLowerCase() %>
SORT rating DESC
```

---

## 🚀 相关项目

```dataview
LIST
FROM #proj AND [[<% topic %>]]
```

---

## 🎯 学习目标

- [ ]
- [ ]
- [ ]

---

## 📝 最近更新

```dataview
LIST
FROM #domain/<% topic.toLowerCase() %>
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 5
```

---

## 🏷️ 标签

#grain/moc #domain/<% topic.toLowerCase() %>