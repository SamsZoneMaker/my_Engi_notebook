---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/basic"
  - "#lang/python"
status: 完善中
complexity: 基础
notetype: 学习笔记
resource: Python Crash Course
related:
  - "[[🐍 00_Python_MOC]]"
  - "[[Python基础 - 列表与元组]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Python基础 - 数据类型

> [!abstract] 摘要
> 本笔记系统介绍Python的基础数据类型,包括字符串、数字和None类型的使用方法、常用操作和最佳实践。

## 🎯 Target
- [ ] 掌握字符串的各种方法和操作
- [ ] 理解Python中的数字类型及其特性
- [ ] 学会使用None作为占位值
- [ ] 熟练运用字符串格式化技术

## 📝 Core

### 字符串 (String)

#### 基本概念
用引号引起的都是字符串,此处引号不限于双引号`"`或单引号`'`

#### 常用方法 (Methods)
method是Python对数据执行的操作。假设变量名为`name`,变量后的句点`.`会对变量`name`执行方法的操作,如`name.title()`,title方法的作用是令每个单词的首字母大写。

方法要跟随一个括号`()`使用,`()`是用来填充额外的信息的,即便没有/不需要额外的信息,也需要放置一个空括号。

```python
# 大小写转换
print(name.upper())     # 全大写
print(name.lower())     # 全小写
print(name.title())     # 每个单词首字母大写

# 空白处理
name.rstrip()           # 去除字符右端空白
name.lstrip()           # 去除字符左端空白
name.strip()            # 去除字符两端空白

# 前缀/后缀处理
name.removeprefix(xxx)  # 去除变量中的xxx前缀
```

#### 字符串合并
通过`f(format)`字符串将需要串起的字符合并,当需要合并的字符是以变量的形式则需要使用大括号。

```python
first_name = "Sam"
last_name = "Li"
full_name = f"{first_name} {last_name}"
```

#### 常用符号
- `\n` - 换行符
- `\t` - 制表符
- `%` - 求模运算符(求余)
- `+=` - 值递增 或 在末尾追加字符

#### 字符串追加
运算符`+=`在赋给变量的字符串末尾追加一个字符串

```python
prompt = "If you share your name, we can personalize the messages you see."
prompt += "\nWhat is your first name? "
name = input(prompt)
```

### 数字类型 (Numbers)

#### 整数 (Integer)
Python中的整数可以进行基本的数学运算:`+`, `-`, `*`, `/`, `**`(幂运算)

#### 浮点数 (Float)
浮点数的特性:
- 将任意两个数相除,结果总是浮点数,即便这两个数都是整数且能整除
- 在其他任何运算中,如果一个操作数是整数,另一个操作数是浮点数,结果也总是浮点数
- 在Python中,无论是哪种运算,只要有操作数是浮点数,默认得到的就总是浮点数,即便结果原本为整数

#### 变量赋值

**单个赋值:**
```python
x = 10
```

**同时赋值:**
将一系列数赋给一组变量,可以采用如下的赋值方式:
```python
x, y, z = 0, 0, 0
```
需要用逗号将变量名分开;对于要赋给变量的值,也需要做同样的处理。Python将按顺序将每个值赋给对应的变量。只要变量数和值的个数相同,Python就能正确地将变量和值关联起来。

#### 常量 (Constants)
在程序的整个周期中,如果一个变量的值是保持一直不变的,Python没有内置的"常量"类型,但是可以用`全大写字母`的方式命名,该参数将被视作"常量"。

```python
MAX_CONNECTIONS = 100
PI = 3.14159
```

> [!tip] 最佳实践
> 通常情况下,会使用全大写字母的命名方式定义一个变量为常量,该常量的值应始终不变

### None 类型

None表示变量没有值,可以视作一个占位值。在以下场景中特别有用:
- 初始化变量时表示"暂时没有值"
- 函数没有显式返回值时的默认返回
- 作为可选参数的默认值

```python
result = None  # 初始化为空值
if result is None:
    print("还没有结果")
```

---
## 🤔 Q&A

### Q1: 字符串方法和字符串格式化有什么区别?
**A**: 字符串方法是对已有字符串进行操作(如大小写转换、去除空白),而字符串格式化(f-string)是用来构建新的字符串,将变量值嵌入到字符串模板中。

### Q2: 为什么Python中除法结果总是浮点数?
**A**: 这是Python 3的设计决策,为了保证数学运算的准确性和一致性。如果需要整数除法,可以使用`//`运算符。

### Q3: None和空字符串''有什么区别?
**A**: None表示"没有值",是NoneType类型的唯一值;而空字符串''是一个字符串类型,表示"长度为0的字符串"。它们在逻辑判断中都为False,但类型不同。

## 🚀 Tasks
- [ ] 练习使用各种字符串方法处理用户输入
- [ ] 编写程序演示整数和浮点数的运算差异
- [ ] 使用f-string创建格式化的输出信息

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Built-in Types

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的基础部分
* 与[[Python基础 - 列表与元组]]共同构成Python的基础数据结构知识
* 字符串格式化在[[Python基础 - 函数]]中也会频繁使用
