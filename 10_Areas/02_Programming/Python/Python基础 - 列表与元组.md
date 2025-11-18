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
  - "[[Python基础 - 数据类型]]"
  - "[[Python基础 - 控制流]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Python基础 - 列表与元组

> [!abstract] 摘要
> 本笔记详细介绍Python中的列表(list)和元组(tuple)数据结构,包括创建、访问、修改、管理和高级操作技巧。

## 🎯 Target
- [ ] 掌握列表的创建和基本操作
- [ ] 熟练使用列表的增删改查方法
- [ ] 理解列表推导式的使用
- [ ] 掌握元组的特性和使用场景
- [ ] 学会列表切片和复制技巧

## 📝 Core

### 列表 (List)

#### 基本概念
**列表(list)** 由一系列按特定顺序排列的元素组成。你不仅可以创建包含字母表中所有字母、数字0〜9或所有家庭成员姓名的列表,还可以将任何东西加入列表,其中的元素之间可以没有任何关系。

在Python中,用方括号`[]`表示列表,用逗号分隔其中的元素。

```python
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
numbers = [1, 2, 3, 4, 5]
mixed = ['python', 3.14, 42, True]  # 列表可以包含不同类型的元素
```

> [!tip] 命名建议
> 列表通常包含多个元素,因此给列表指定一个表示复数的名称(如letters、digits或names)是较为常见的做法。

#### 索引访问
- 要访问列表元素,可指出列表的名称,再指出元素的索引,并将后者放在方括号内
- 索引从0开始,而不是从1,与C语言的数组一致
- Python为访问最后一个列表元素提供了一种特殊语法。通过将索引指定为-1,可让Python返回最后一个列表元素,并以此类推,-2、-3则表示倒数第二个和第三个列表元素

```python
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
print(bicycles[0])   # 输出: trek
print(bicycles[-1])  # 输出: specialized
print(bicycles[-2])  # 输出: redline
```

#### 元素修改

**修改单个元素:**
```python
motorcycles = ['honda', 'yamaha', 'suzuki']
motorcycles[0] = 'ducati'  # 将第一个元素修改为'ducati'
```

**添加元素:**

1. **末尾添加 (append)**
```python
motorcycles = ['honda', 'yamaha', 'suzuki']
motorcycles.append('ducati')
# 结果: ['honda', 'yamaha', 'suzuki', 'ducati']
```

2. **指定位置插入 (insert)**
```python
motorcycles = ['honda', 'yamaha', 'suzuki']
motorcycles.insert(0, 'ducati')  # 在索引0处插入
# 结果: ['ducati', 'honda', 'yamaha', 'suzuki']
```

3. **扩展列表 (extend)**
```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list1.extend(list2)
# 结果: [1, 2, 3, 4, 5, 6]
```

**删除元素:**

1. **使用del语句**
```python
motorcycles = ['honda', 'yamaha', 'suzuki']
del motorcycles[0]  # 删除第一个元素
```

2. **使用pop()方法**
```python
motorcycles = ['honda', 'yamaha', 'suzuki']
popped_motorcycle = motorcycles.pop()  # 弹出并返回最后一个元素
print(popped_motorcycle)  # 输出: suzuki

# 弹出指定位置的元素
first_motorcycle = motorcycles.pop(0)
```

> [!tip] del vs pop()
> 如果要从列表中删除一个元素,且不再以任何方式使用它,就使用del语句;如果要在删除元素后继续使用它,就使用pop()方法。

3. **删除特定值 (remove)**
```python
motorcycles = ['honda', 'yamaha', 'suzuki', 'ducati']
motorcycles.remove('ducati')
# 注意:一次只会删除列表中第一次出现的值,如需删除多个,可用循环
```

#### 列表管理与排序

**永久排序 (sort)**
```python
cars = ['bmw', 'audi', 'toyota', 'subaru']
cars.sort()  # 按字母顺序排序
print(cars)  # ['audi', 'bmw', 'subaru', 'toyota']

cars.sort(reverse=True)  # 反向排序
print(cars)  # ['toyota', 'subaru', 'bmw', 'audi']
```

**临时排序 (sorted)**
```python
cars = ['bmw', 'audi', 'toyota', 'subaru']
print(sorted(cars))  # 临时排序输出
print(cars)          # 原列表顺序不变
```

**反转列表 (reverse)**
```python
cars = ['bmw', 'audi', 'toyota', 'subaru']
cars.reverse()  # 反转列表顺序(永久性)
# 再次调用reverse()可恢复原顺序
```

**获取列表长度 (len)**
```python
cars = ['bmw', 'audi', 'toyota', 'subaru']
print(len(cars))  # 输出: 4
```

### 数值列表

#### range()函数
该函数可用于生成一系列的数

```python
for value in range(1, 5):
    print(value)
# 输出: 1 2 3 4 (不包含5,这是常见的差一行为)

# 指定步长
even_numbers = list(range(2, 11, 2))  # [2, 4, 6, 8, 10]
```

#### 创建数值列表
```python
numbers = list(range(1, 6))
print(numbers)  # [1, 2, 3, 4, 5]
```

#### 列表推导式
列表推导式是将for循环和创建新元素的代码合并一起的方式,需要注意的是列表推导式中的for循环末尾不需要冒号`:`

```python
# 传统方式
squares = []
for value in range(1, 11):
    square = value ** 2
    squares.append(square)

# 简化方式
squares = []
for value in range(1, 11):
    squares.append(value**2)

# 列表推导式(最优)
squares = [value**2 for value in range(1, 11)]
```

> [!tip] 最佳实践
> 列表推导式提高了代码运行效率,同时提升了可读性,是Python的推荐用法。

#### 统计函数
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(min(numbers))  # 最小值: 1
print(max(numbers))  # 最大值: 10
print(sum(numbers))  # 总和: 55
```

### 列表切片 (Slicing)

切片是处理列表部分元素的强大工具:

```python
players = ['charles', 'martina', 'michael', 'florence', 'eli']

print(players[0:3])   # ['charles', 'martina', 'michael']
print(players[1:4])   # ['martina', 'michael', 'florence']
print(players[:4])    # 从开头到索引3: ['charles', 'martina', 'michael', 'florence']
print(players[2:])    # 从索引2到末尾: ['michael', 'florence', 'eli']
print(players[-3:])   # 最后三个元素: ['michael', 'florence', 'eli']
print(players[:])     # 复制整个列表: ['charles', 'martina', 'michael', 'florence', 'eli']
```

### 列表复制

**正确的复制方式:**
```python
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]  # 使用切片创建副本
```

**错误的复制方式:**
```python
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods  # 这只是创建了引用,不是副本!
# 当更改my_foods时,friend_foods也会同时更改
```

> [!warning] 注意
> 直接赋值`friend_foods = my_foods`不会创建新列表,而是让两个变量指向同一个列表对象。

### 元组 (Tuple)

#### 基本概念
元组是一种很像列表的特殊形式,元组里面的值是不可以被修改的。

**区别:**
- 元组用`()`定义
- 列表用`[]`定义

```python
dimensions = (200, 50)  # 创建元组
print(dimensions[0])     # 访问元组元素: 200
print(dimensions[1])     # 访问元组元素: 50

# 以下操作会报错
# dimensions[0] = 250  # TypeError: 'tuple' object does not support item assignment
```

#### 元组编辑
元组虽然不能更改其中的某个值,但是可以整个元组重新赋值:

```python
dimensions = (200, 50)
print(dimensions)  # (200, 50)

dimensions = (400, 100)  # 重新赋值整个元组
print(dimensions)  # (400, 100)
```

#### 重要注意事项

> [!danger] 注意
> - 元组是由`,`标识的,即使只有一个元素,也要在末尾加上`,`
> - 元组不能被更改,尝试更改会被Python报错
> ```python
> single_element = (42,)  # 单元素元组,注意逗号
> ```

#### 元组的使用场景
- 存储不应该被修改的数据(如坐标、RGB颜色值等)
- 作为字典的键(列表不能作为键)
- 函数返回多个值时实际返回的是元组

---
## 🤔 Q&A

### Q1: 什么时候使用列表,什么时候使用元组?
**A**: 如果数据在程序运行过程中可能需要修改,使用列表;如果数据是固定不变的(如一周的天数、坐标值),使用元组。元组还有性能优势,因为Python知道它不会改变。

### Q2: 列表推导式有什么优势?
**A**: 列表推导式不仅代码更简洁,而且运行速度通常更快。它在一行代码中完成创建列表和填充元素的操作,提高了代码的可读性和Pythonic风格。

### Q3: 为什么列表复制要用切片而不是直接赋值?
**A**: 直接赋值只是创建了引用,两个变量指向同一个列表对象。使用切片`[:]`会创建列表的完整副本,是一个独立的新列表对象,修改其中一个不会影响另一个。

### Q4: range(1, 5)为什么不包含5?
**A**: 这是编程语言中常见的"差一行为",也叫"左闭右开区间"。这样设计的好处是`range(0, n)`正好生成n个数,且索引范围与列表长度一致。

## 🚀 Tasks
- [ ] 练习使用列表推导式替换传统for循环
- [ ] 编写程序演示列表和元组的区别
- [ ] 使用切片操作处理实际数据集
- [ ] 实现一个程序,使用列表的各种方法管理待办事项

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Data Structures

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的核心部分
* 与[[Python基础 - 控制流]]结合使用,可以实现列表的遍历和过滤
* [[Python基础 - 字典]]是另一种重要的数据结构,与列表互补
