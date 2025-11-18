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
  - "[[Python基础 - 控制流]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Python基础 - 函数

> [!abstract] 摘要
> 本笔记详细介绍Python中的函数定义、参数传递、返回值、模块化等核心概念和最佳实践。

## 🎯 Target
- [ ] 掌握函数的定义和调用方法
- [ ] 理解各种参数传递方式
- [ ] 学会使用返回值和return语句
- [ ] 掌握函数的模块化和导入方法
- [ ] 遵循函数编写的最佳实践

## 📝 Core

### 函数基础

#### 概念
函数是带名字的代码块,用于完成具体的工作。要执行函数定义的特定任务,可调用(call)该函数。

#### 定义和调用
```python
# 函数定义
def greet(name):
    """显示简单的问候语"""  # 文档字符串(docstring)
    print(f"Hello, {name}!")

# 函数调用
greet("Alice")  # 输出: Hello, Alice!
```

> [!tip] 文档字符串
> 三引号注释称为文档字符串(docstring),用于描述函数的功能。Python使用它们来生成文档。

### 参数传递

#### 形参与实参
- **形参(Parameter)**: 函数定义中的变量,如上例中的`name`
- **实参(Argument)**: 调用函数时传递的值,如上例中的`"Alice"`

#### 位置实参
按照函数定义的顺序传递参数:

```python
def describe_pet(animal_type, pet_name):
    """显示宠物的信息"""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet('hamster', 'harry')
# 输出:
# I have a hamster.
# My hamster's name is Harry.
```

> [!warning] 顺序很重要
> 位置实参的顺序必须与函数定义中的形参顺序一致。

#### 关键字实参
通过指定参数名称传递,不依赖顺序:

```python
def describe_pet(animal_type, pet_name):
    """显示宠物的信息"""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

# 两种调用方式等效
describe_pet(animal_type='hamster', pet_name='harry')
describe_pet(pet_name='harry', animal_type='hamster')
```

#### 默认值
在函数定义中可以给参数指定默认值:

```python
def describe_pet(pet_name, animal_type='dog'):
    """显示宠物的信息"""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

describe_pet('willie')  # 使用默认值'dog'
describe_pet('harry', 'hamster')  # 覆盖默认值
```

> [!tip] 默认值参数位置
> 在函数定义中,有默认值的参数必须放在没有默认值的参数后面。

#### 任意数量的位置实参 (*args)
当不知道函数需要接受多少个参数时,可以使用`*args`:

```python
def make_pizza(*toppings):
    """概述要制作的比萨"""
    print("\nMaking a pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')
```

- `*toppings`创建了一个元组,该元组可以接受所有函数收到的值
- Python中常见`*args`表示接受任意数量的位置实参

#### 任意数量的关键字实参 (**kwargs)
接受任意数量的键值对参数:

```python
def build_profile(first, last, **user_info):
    """构建包含用户所有信息的字典"""
    profile = {}
    profile['first_name'] = first
    profile['last_name'] = last
    for key, value in user_info.items():
        profile[key] = value
    return profile

user_profile = build_profile('albert', 'einstein',
                             location='princeton',
                             field='physics')
print(user_profile)
# 输出: {'first_name': 'albert', 'last_name': 'einstein',
#        'location': 'princeton', 'field': 'physics'}
```

- `**user_info`创建一个名为`user_info`的字典,存放所有收到的键值对
- Python中常见`**kwargs`表示接受任意数量的关键字实参

> [!tip] 混合使用
> 在编写函数时,可以混合使用位置实参、关键字实参和任意数量的实参,但顺序必须是:
> 1. 位置参数
> 2. *args
> 3. 关键字参数
> 4. **kwargs

### 返回值

#### 返回简单值
使用`return`语句返回值:

```python
def get_formatted_name(first_name, last_name):
    """返回整洁的姓名"""
    full_name = f"{first_name} {last_name}"
    return full_name.title()

musician = get_formatted_name('jimi', 'hendrix')
print(musician)  # 输出: Jimi Hendrix
```

#### 返回字典
函数可以返回包括列表、字典等在内的复杂结构:

```python
def build_person(first_name, last_name, age=None):
    """返回一个字典,其中包含有关一个人的信息"""
    person = {'first': first_name, 'last': last_name}
    if age:
        person['age'] = age
    return person

musician = build_person('jimi', 'hendrix', age=27)
print(musician)
# 输出: {'first': 'jimi', 'last': 'hendrix', 'age': 27}
```

### 传递列表

#### 基本用法
```python
def greet_users(names):
    """向列表中的每位用户发出简单的问候"""
    for name in names:
        msg = f"Hello, {name.title()}!"
        print(msg)

usernames = ['hannah', 'ty', 'margot']
greet_users(usernames)
```

#### 在函数中修改列表
```python
def print_models(unprinted_designs, completed_models):
    """
    模拟打印每个设计,直到没有未打印的设计为止
    打印每个设计后,都将其移到列表completed_models中
    """
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        print(f"Printing model: {current_design}")
        completed_models.append(current_design)

def show_completed_models(completed_models):
    """显示打印好的所有模型"""
    print("\nThe following models have been printed:")
    for completed_model in completed_models:
        print(completed_model)

unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

print_models(unprinted_designs, completed_models)
show_completed_models(completed_models)
```

#### 传递列表副本
当只想传递列表但不修改原列表时,可以传递列表的副本:

```python
# 传递副本
function_name(list_name[:])  # [:]创建列表的完整副本

# 示例
print_models(unprinted_designs[:], completed_models)
# 原列表unprinted_designs不会被修改
```

### 函数模块化

#### 模块的概念
模块是扩展名为`.py`的文件,包含要导入程序的代码。将函数存储在模块中可以:
- 隐藏程序代码的细节
- 将重点放在程序的高层逻辑上
- 重用代码,提高开发效率

#### 导入整个模块
```python
# pizza.py
def make_pizza(size, *toppings):
    """概述要制作的比萨"""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

# main.py
import pizza

pizza.make_pizza(16, 'pepperoni')
pizza.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
```

**格式**: `import module_name`
**调用**: `module_name.function_name()`

#### 导入特定函数
```python
from pizza import make_pizza

make_pizza(16, 'pepperoni')  # 不需要模块名前缀
```

**格式**: `from module_name import function_0, function_1, function_2`
**调用**: `function_name()` (不需要句点)

#### 使用as给函数指定别名
针对函数名称太长或可能与程序中既有名称冲突的情况:

```python
from pizza import make_pizza as mp

mp(16, 'pepperoni')
```

**格式**: `from module_name import function_name as fn`

#### 使用as给模块指定别名
```python
import pizza as p

p.make_pizza(16, 'pepperoni')
```

**格式**: `import module_name as mn`
**调用**: `mn.function()`

> [!tip] 推荐做法
> 给模块起别名是非常常用的做法,如`import numpy as np`, `import pandas as pd`

#### 导入模块中的所有函数
```python
from pizza import *

make_pizza(16, 'pepperoni')
```

**格式**: `from module_name import *`

> [!danger] 不推荐
> 不建议采用此方法,容易导致名称冲突。建议还是明确导入需要的函数。

---
## 🤔 Q&A

### Q1: 什么时候使用位置实参,什么时候使用关键字实参?
**A**:
- **位置实参**: 参数较少且顺序明确时使用,代码更简洁
- **关键字实参**: 参数较多或有多个可选参数时使用,提高可读性
- 实际项目中经常混合使用两者

### Q2: 函数应该有多长?
**A**: 函数应该只做一件事,并做好这件事。如果函数超过20-30行,考虑是否可以拆分成更小的函数。遵循"单一职责原则"。

### Q3: *args和**kwargs的区别是什么?
**A**:
- `*args`: 接收任意数量的位置参数,在函数内部是一个元组
- `**kwargs`: 接收任意数量的关键字参数,在函数内部是一个字典

### Q4: 函数可以返回多个值吗?
**A**: Python函数可以返回多个值,实际上是返回一个元组:
```python
def get_name():
    return 'John', 'Doe'

first, last = get_name()  # 元组解包
```

## 🚀 Tasks
- [ ] 编写一个函数库,包含常用的工具函数
- [ ] 练习使用*args和**kwargs编写灵活的函数
- [ ] 将重复的代码提取为函数,提高代码复用性
- [ ] 为自己的函数编写详细的文档字符串

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Defining Functions
* PEP 8 -- Style Guide for Python Code

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的核心部分
* 在[[Python基础 - 类与面向对象]]中,方法本质上就是与对象关联的函数
* [[Python高级 - 异常处理]]可以让函数更加健壮

## 编码规范

> [!important] PEP 8函数编写规范
> 1. 在给形参指定默认值时,等号两边不要有空格;函数调用中的关键字实参也应遵循这种约定
> 2. 如果程序或模块包含多个函数,可使用两个空行将相邻的函数分开
> 3. 所有import语句都应该放在文件开头
> 4. 函数名应该使用小写字母和下划线(snake_case)
