---
tags:
  - type/reference
---
# Assets

本目录统一存放笔记中使用的图片、SVG、Drawio 等附件。

## 分类规则

分类目录使用 `领域编号_子领域编号_主题` 命名，例如：

- `01_01_Networks`
- `01_02_Python`
- `01_02_Build_Tools`
- `01_03_Boot`
- `01_03_SerDes`
- `01_03_Toolchain`
- `20_02_Songshan`

只在存在对应附件时创建分类目录，不预先建立空目录。

## 文件命名

- 使用能够说明内容的英文名称，不使用时间戳或 `image-xxxx`。
- 同一图表的源文件与导出文件使用相同主文件名，例如：
  - `linker_flow.drawio`
  - `linker_flow.svg`
  - `linker_flow.png`
- PDF、规范和书籍等来源资料放在 `30_Resources`，不放入 `assets`。

Obsidian 的新附件默认先保存到 `assets`，之后根据主题移动到对应分类目录。
