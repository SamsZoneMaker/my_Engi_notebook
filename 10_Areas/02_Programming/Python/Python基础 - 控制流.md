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
# Python基础 - 控制流

> [!abstract] 摘要
> 本笔记详细介绍Python中的控制流语句,包括for循环、if条件语句和while循环的使用方法和最佳实践。

## 🎯 Target
- [ ] 掌握for循环的使用和命名规范
- [ ] 熟练运用if条件判断
- [ ] 理解while循环及其控制语句
- [ ] 学会在循环中使用break和continue

## 📝 Core

### for循环

#### 基本用法
for循环用于遍历可迭代对象(列表、元组、字符串、字典、集合、range等)中的每个元素。

```python
cats = ['persian', 'siamese', 'maine coon']
for cat in cats:
    print(f"I love {cat} cats!")
```

#### 命名建议
在for循环中,建议使用有意义的临时变量,有助于理解代码:

```python
for cat in cats:        # 单数形式的临时变量
for dog in dogs:
for item in list_of_items:
```

> [!tip] 可迭代对象
> for循环中的对象可以是任何可以被迭代的对象:
> - 列表(List)
> - 元组(Tuple)
> - 字符串(String)
> - 字典(Dictionary)
> - 集合(Set)
> - range(用于生成数字序列)

#### 缩进规则

> [!warning] 重要
> - 在Python中,for循环不使用大括号`{}`,以**相同的缩进**作为for循环内的内容
> - 在Python中要极度注意缩进的使用,不建议随意缩进
> - 缩进建议使用**四个空格**而非`tab`键

```python
for cat in cats:
    print(f"I love {cat}!")      # 缩进4个空格,属于循环体
    print("Cats are amazing!")   # 缩进4个空格,属于循环体
print("Loop finished!")           # 无缩进,不属于循环体
```

### if条件语句

#### 基本概念
if循环的底层逻辑是**条件测试**,根据测试结果的**True**和**False**来判断代码的执行方式。

```python
age = 18
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")
```

#### 条件测试运算符
```python
# 比较运算符
x == y    # 等于
x != y    # 不等于
x > y     # 大于
x < y     # 小于
x >= y    # 大于等于
x <= y    # 小于等于

# 逻辑运算符
condition1 and condition2  # 与运算
condition1 or condition2   # 或运算
not condition              # 非运算
```

#### 大小写敏感性
因为Python是大小写敏感的语言,所以判断的时候需要区分大小写;如果判断时不看重或无法判断字符内的大小写情况,可以将所有变量变为全小写,再进行逻辑判断:

```python
car = 'Audi'
if car.lower() == 'audi':  # 转换为小写后比较
    print("Match!")
```

#### 检查列表元素
```python
# 检查元素是否存在
requested_topping = 'mushrooms'
if requested_topping in available_toppings:
    print("Adding mushrooms.")

# 检查元素是否不存在
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'
if user not in banned_users:
    print(f"{user.title()}, you can post a response.")
```

#### if-elif-else结构
```python
age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
elif age < 65:
    price = 40
else:
    price = 20

print(f"Your admission cost is ${price}.")
```

> [!tip] else子句是可选的
> 可以省略`else`子句,只使用if-elif结构,这在某些情况下逻辑更清晰。

#### 检查列表是否为空
```python
requested_toppings = []
if requested_toppings:  # 非空列表为True
    for topping in requested_toppings:
        print(f"Adding {topping}.")
else:
    print("Are you sure you want a plain pizza?")
```

### while循环

#### 基本用法
while循环会在条件为True时持续执行代码块:

```python
current_number = 1
while current_number <= 5:
    print(current_number)
    current_number += 1
```

#### break语句
使用`break`退出循环,break可以退出任何Python中的循环,包括for和while循环:

```python
prompt = "\nPlease enter the name of a city you have visited:"
prompt += "\n(Enter 'quit' when you are finished.) "

while True:
    city = input(prompt)
    if city == 'quit':
        break  # 立即退出循环
    else:
        print(f"I'd love to go to {city.title()}!")
```

#### continue语句
用`continue`跳过当前迭代,继续下一次循环:

```python
current_number = 0
while current_number < 10:
    current_number += 1
    if current_number % 2 == 0:
        continue  # 跳过偶数
    print(current_number)  # 只打印奇数
```

#### while循环处理列表和字典
通过将while循环与列表和字典结合起来使用,可收集、存储并组织大量的输入,供以后查看和使用。

```python
# 示例:将未确认的用户移动到已确认列表
unconfirmed_users = ['alice', 'brian', 'candace']
confirmed_users = []

while unconfirmed_users:  # 列表不为空时为True
    current_user = unconfirmed_users.pop()
    print(f"Verifying user: {current_user.title()}")
    confirmed_users.append(current_user)

print("\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:
    print(confirmed_user.title())
```

#### 删除列表中所有特定值
```python
pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
print(pets)

while 'cat' in pets:
    pets.remove('cat')  # 循环直到删除所有'cat'

print(pets)
# 输出: ['dog', 'dog', 'goldfish', 'rabbit']
```

---
## 🤔 Q&A

### Q1: for循环和while循环有什么区别,如何选择?
**A**:
- **for循环**: 用于已知迭代次数或需要遍历序列的情况。更Pythonic,推荐优先使用。
- **while循环**: 用于不确定迭代次数,需要根据条件动态判断的情况,如用户交互、等待某个事件发生等。

### Q2: break和continue的区别是什么?
**A**:
- **break**: 完全终止循环,跳出循环体
- **continue**: 跳过本次迭代的剩余代码,直接进入下一次迭代

### Q3: 为什么Python使用缩进而不是大括号?
**A**: Python使用缩进来表示代码块是其设计哲学的一部分,目的是强制代码具有良好的可读性。这使得Python代码看起来更整洁,但要求开发者必须保持一致的缩进风格。

### Q4: if循环中什么值被视为False?
**A**: 以下值在条件判断中被视为False:
- False
- None
- 0(数字零)
- 空序列: '', [], ()
- 空字典: {}
- 空集合: set()

## 🚀 Tasks
- [ ] 编写程序使用for循环遍历列表并应用条件判断
- [ ] 实现一个用户交互程序,使用while循环和break/continue
- [ ] 练习使用if-elif-else处理多种条件分支
- [ ] 使用while循环处理列表,实现元素的移动或删除

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Control Flow

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的核心部分
* 与[[Python基础 - 列表与元组]]结合使用,实现数据的遍历和处理
* 在[[Python基础 - 函数]]和[[Python基础 - 类与面向对象]]中会频繁使用控制流
