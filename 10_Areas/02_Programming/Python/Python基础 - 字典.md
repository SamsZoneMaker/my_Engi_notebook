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
  - "[[Python基础 - 控制流]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Python基础 - 字典

> [!abstract] 摘要
> 本笔记详细介绍Python中的字典(dict)数据结构,包括创建、访问、修改、遍历和嵌套使用的方法。

## 🎯 Target
- [ ] 掌握字典的创建和基本操作
- [ ] 熟练使用字典的增删改查方法
- [ ] 理解字典的遍历方式
- [ ] 学会get()方法的安全访问
- [ ] 掌握字典的嵌套使用

## 📝 Core

### 字典基础

#### 概念
字典用来存放对应信息的**键值对(key-value pairs)**。字典是一种动态结构,可随时在其中添加键值对。

#### 创建和访问
```python
# 创建字典
alien_0 = {'color': 'green', 'points': 5}

# 访问值
print(alien_0['color'])   # 输出: green
print(alien_0['points'])  # 输出: 5

# 将值赋给变量
point_s = alien_0['points']
```

### 基本操作

#### 创建空字典
```python
alien_0 = {}  # 创建一个空字典
```

#### 添加键值对
```python
alien_0 = {}
alien_0['color'] = 'green'     # 添加color键
alien_0['x_position'] = 0      # 添加x_position键
alien_0['y_position'] = 25     # 添加y_position键

print(alien_0)
# 输出: {'color': 'green', 'x_position': 0, 'y_position': 25}
```

> [!tip] 键值对顺序
> 从Python 3.7开始,字典会保持插入顺序。但不应该依赖这个顺序来编写程序逻辑。

#### 修改字典值
```python
alien_0 = {'color': 'green', 'points': 5}
print(f"The alien is {alien_0['color']}.")

alien_0['color'] = 'yellow'  # 修改值
print(f"The alien is now {alien_0['color']}.")
```

#### 删除键值对
```python
alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

del alien_0['points']  # 永久删除
print(alien_0)
# 输出: {'color': 'green'}
```

### get()方法

#### 概念和优势
get()方法用于安全地访问字典中的值,当键不存在时不会引发错误,而是返回默认值。

> [!tip] 使用场景
> - 当你不确定键是否存在时,优先使用get()方法
> - 需要提供默认值时,明确指定第二个参数
> - 在处理可能存在的空值或缺失值时,get()特别有用

#### 基本语法
```python
# 基本语法
dict.get(key, default=None)

# 示例
my_dict = {'name': 'Tom', 'age': 25}

# 获取存在的键的值
print(my_dict.get('name'))  # 输出: Tom

# 获取不存在的键,返回默认值None
print(my_dict.get('height'))  # 输出: None

# 指定默认值
print(my_dict.get('height', 180))  # 输出: 180
```

#### 实际应用

**在条件判断中的应用:**
```python
settings = {'debug': True}

# 检查配置项,使用默认值
is_debug = settings.get('debug', False)         # 输出: True
log_level = settings.get('log_level', 'INFO')   # 输出: INFO
```

**统计词频:**
```python
from collections import Counter

words = ['apple', 'banana', 'apple', 'orange']
word_count = Counter(words)

# 安全获取词频
apple_count = word_count.get('apple', 0)  # 输出: 2
kiwi_count = word_count.get('kiwi', 0)    # 输出: 0
```

### 遍历字典

#### 遍历所有键值对
```python
user_0 = {
    'username': 'efermi',
    'first': 'enrico',
    'last': 'fermi',
}

# 遍历键值对
for key, value in user_0.items():
    print(f"\nKey: {key}")
    print(f"Value: {value}")
```

#### 遍历所有键
```python
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

# 遍历键
for name in favorite_languages.keys():
    print(name.title())

# 也可以省略.keys(),效果相同
for name in favorite_languages:
    print(name.title())
```

#### 按顺序遍历键
```python
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

for name in sorted(favorite_languages.keys()):
    print(f"{name.title()}, thank you for taking the poll.")
```

#### 遍历所有值
```python
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

# 遍历值
for language in favorite_languages.values():
    print(language.title())

# 去除重复值
for language in set(favorite_languages.values()):
    print(language.title())
```

> [!tip] set()函数
> 当遍历的结果有重复值时,可以用`set()`提取唯一元素。

### 字典嵌套

#### 在列表中存储字典
```python
alien_0 = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

aliens = [alien_0, alien_1, alien_2]

for alien in aliens:
    print(alien)

# 输出:
# {'color': 'green', 'points': 5}
# {'color': 'yellow', 'points': 10}
# {'color': 'red', 'points': 15}
```

**批量创建字典:**
```python
# 创建一个用于存储外星人的空列表
aliens = []

# 创建30个绿色的外星人
for alien_number in range(30):
    new_alien = {'color': 'green', 'speed': 'slow', 'points': 5}
    aliens.append(new_alien)

# 显示前5个外星人
for alien in aliens[:5]:
    print(alien)
print(f"Total number of aliens: {len(aliens)}")
```

#### 在字典中存储列表
针对的情况是键值对中的值不止有一个的情况:

```python
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'],
}

# 概述顾客点的比萨
print(f"You ordered a {pizza['crust']}-crust pizza "
      "with the following toppings:")

for topping in pizza['toppings']:
    print(f"\t{topping}")
```

**更复杂的示例:**
```python
favorite_languages = {
    'jen': ['python', 'ruby'],
    'sarah': ['c'],
    'edward': ['ruby', 'go'],
    'phil': ['python', 'haskell'],
}

for name, languages in favorite_languages.items():
    print(f"\n{name.title()}'s favorite languages are:")
    for language in languages:
        print(f"\t{language.title()}")
```

#### 在字典中嵌套字典
```python
users = {
    'aeinstein': {
        'first': 'albert',
        'last': 'einstein',
        'location': 'princeton',
    },
    'mcurie': {
        'first': 'marie',
        'last': 'curie',
        'location': 'paris',
    },
}

for username, user_info in users.items():
    print(f"\nUsername: {username}")
    full_name = f"{user_info['first']} {user_info['last']}"
    location = user_info['location']

    print(f"\tFull name: {full_name.title()}")
    print(f"\tLocation: {location.title()}")
```

---
## 🤔 Q&A

### Q1: 什么时候使用字典,什么时候使用列表?
**A**:
- **字典**: 当需要存储关联数据(键值对),或需要通过描述性的键快速查找值时使用
- **列表**: 当需要存储有序的元素集合,或主要通过位置(索引)访问元素时使用

### Q2: 字典的键可以是什么类型?
**A**: 字典的键必须是**不可变类型**,如字符串、数字、元组。列表不能作为键,因为列表是可变的。值可以是任何Python对象。

### Q3: 访问不存在的键会发生什么?
**A**: 直接使用`dict[key]`访问不存在的键会引发`KeyError`异常。使用`get()`方法可以安全访问,返回None或指定的默认值。

### Q4: 字典是有序的吗?
**A**: 从Python 3.7开始,字典会保持插入顺序。但在设计程序时不应该依赖这个顺序,如果顺序很重要,考虑使用`collections.OrderedDict`。

## 🚀 Tasks
- [ ] 创建一个程序,使用字典存储和管理联系人信息
- [ ] 练习使用get()方法处理可能缺失的配置项
- [ ] 实现字典嵌套结构,如学生成绩管理系统
- [ ] 使用while循环收集用户输入并存储到字典中

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Dictionaries

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的核心部分
* 与[[Python基础 - 列表与元组]]共同构成Python的主要数据结构
* 在[[Python基础 - 类与面向对象]]中,实例属性存储在特殊的字典`__dict__`中
