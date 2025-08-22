---
tags:
  - shell
  - projDragon
  - Linux
aliases:
create date: 2025-08-22 16:20:48
modify date: 2025-08-22  17:17:25
---
# 📝 笔记内容

`build.sh` 文件位于仓库根目录下，其设计的思想是根据不同的构建对象、构建链生成不同的编译结果，等同于对dragon库的一次编译（一般只针对需要编译的部分）

## 分类
对象有四类
- boot
- app
- demo
- test
不同的类别对编译所需条件不同

### boot类
boot类通常需要指定的是 **target file**，通过参数 `-ld` 指定。
`-o` 为选择性的方案，非必须，选择的内容为 ==xxx.option==,用于定义target的额外编译和链接参数

### app/demo/test 类
与Boot类相比