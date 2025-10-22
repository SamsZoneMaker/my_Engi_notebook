---
tags:
status:
topic: "[TOPIC_NAME]"
notetype: MOC
created: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>
modified:
---
# 🗺️ [TOPIC_NAME] - 知识地图

> [!abstract] 📋 概述
> 这是关于 **[TOPIC_NAME]** 的知识索引和导航中心。在这里，你可以找到核心概念、学习路径、相关项目和参考资料。

使用方法：
1. 'Ctrl + H'开启替换功能
2. 把[topic-tag] 替换成 主题内容（例如Python）
3. 把[TOPIC_NAME] 替换成 主题内容（例如Python）

---

## 📊 统计信息与概览

此领域的笔记活跃度概览，优先显示最近修改的笔记。

```dataview
TABLE WITHOUT ID
  file.link as "笔记名称",
  length(file.inlinks) as "被引用",
  status as "状态",
  file.mday as "最后修改"
FROM #domain/[topic-tag]
WHERE file.name != this.file.name
SORT file.mday DESC
LIMIT 10
```

## 🎯 学习路径 (Learning Path)

### 1️⃣ 基础入门 (Basics)
```dataview
LIST
FROM #domain/[topic-tag] AND #level/Basics
WHERE file.name != this.file.name
SORT file.ctime ASC
```

### 2️⃣ 进阶核心 (Intermediate)
```dataview
LIST
FROM #domain/[topic-tag] AND #level/Intermediate
WHERE file.name != this.file.name
SORT file.ctime ASC
```

### 3️⃣ 高级专题 (Advanced)
```dataview
LIST
FROM #domain/[topic-tag] AND #level/Advanced
WHERE file.name != this.file.name
SORT file.ctime ASC
```

## 📚 核心笔记 (Manually Curated)

手动整理的核心概念和实践应用，请在此处填写最重要的笔记链接。

### 重要概念

- [[ ]]
- [[ ]]

### 实践应用

- [[ ]]
- [[ ]]

## 📖 参考资料 (Reference)


## 🚀 相关项目 (Projects)

```dataview
LIST
FROM #proj AND "[[[TOPIC_NAME]]]"
WHERE file.name != this.file.name
SORT file.mtime DESC
```

## 📝 最近更新 (Recent Updates)

```dataview
LIST
FROM #domain/[topic-tag]
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 5
```
