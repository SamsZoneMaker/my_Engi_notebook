---
created: 2025-11-18
tags:
  - type/knowledge
  - topic/programming/python
---
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

### 高级函数特性

#### Lambda表达式(匿名函数)

```python
# 普通函数
def square(x):
    return x ** 2

# Lambda表达式(匿名函数)
square_lambda = lambda x: x ** 2

print(square(5))        # 25
print(square_lambda(5)) # 25

# Lambda常用于临时的简单函数
numbers = [1, 2, 3, 4, 5]

# 使用lambda配合map
squares = list(map(lambda x: x**2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

# 使用lambda配合filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# 使用lambda配合sorted排序
students = [
    {'name': 'Alice', 'score': 85},
    {'name': 'Bob', 'score': 92},
    {'name': 'Charlie', 'score': 78}
]
# 按成绩排序
sorted_students = sorted(students, key=lambda s: s['score'], reverse=True)
print([s['name'] for s in sorted_students])  # ['Bob', 'Alice', 'Charlie']

# Lambda的限制:只能包含单个表达式
# 不能使用语句(如print、赋值等)
# 适合简单操作,复杂逻辑应使用普通函数
```

#### 高阶函数

```python
# 高阶函数:接受函数作为参数或返回函数的函数

# 例1:接受函数作为参数
def apply_operation(numbers, operation):
    """对列表中的每个数应用操作"""
    return [operation(x) for x in numbers]

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

numbers = [1, 2, 3, 4, 5]
print(apply_operation(numbers, square))  # [1, 4, 9, 16, 25]
print(apply_operation(numbers, cube))    # [1, 8, 27, 64, 125]

# 例2:返回函数
def make_multiplier(factor):
    """创建一个乘法函数"""
    def multiplier(x):
        return x * factor
    return multiplier

times_two = make_multiplier(2)
times_three = make_multiplier(3)

print(times_two(5))    # 10
print(times_three(5))  # 15

# 例3:装饰器的简单实现
def timing_decorator(func):
    """装饰器:测量函数执行时间"""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}执行时间: {end-start:.4f}秒")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """模拟耗时操作"""
    import time
    time.sleep(1)
    return "完成"

result = slow_function()  # 会自动打印执行时间
```

#### 递归函数

```python
# 递归:函数调用自己

# 例1:计算阶乘
def factorial(n):
    """计算n的阶乘"""
    if n == 0 or n == 1:  # 基础情况
        return 1
    return n * factorial(n - 1)  # 递归调用

print(factorial(5))  # 120 (5! = 5*4*3*2*1)

# 例2:斐波那契数列
def fibonacci(n):
    """返回第n个斐波那契数"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# 例3:列表求和(递归方式)
def recursive_sum(lst):
    """递归计算列表总和"""
    if not lst:  # 基础情况:空列表
        return 0
    return lst[0] + recursive_sum(lst[1:])  # 递归调用

print(recursive_sum([1, 2, 3, 4, 5]))  # 15

# 注意:递归深度限制
# Python默认递归深度约1000
# 可以通过sys.setrecursionlimit()调整,但要谨慎
import sys
print(sys.getrecursionlimit())  # 默认限制
```

#### 闭包(Closure)

```python
# 闭包:内层函数引用外层函数的变量

def make_counter():
    """创建一个计数器"""
    count = 0  # 自由变量

    def counter():
        nonlocal count  # 声明使用外层的count变量
        count += 1
        return count

    return counter

# 创建两个独立的计数器
counter1 = make_counter()
counter2 = make_counter()

print(counter1())  # 1
print(counter1())  # 2
print(counter1())  # 3

print(counter2())  # 1
print(counter2())  # 2

# 实用示例:创建配置函数
def create_logger(prefix):
    """创建带前缀的日志函数"""
    def log(message):
        print(f"[{prefix}] {message}")
    return log

info_logger = create_logger("INFO")
error_logger = create_logger("ERROR")

info_logger("应用启动")     # [INFO] 应用启动
error_logger("连接失败")    # [ERROR] 连接失败
```

### 常见陷阱和错误

#### 陷阱1: 可变默认参数

```python
# 错误示例:使用可变对象作为默认参数
def append_to_list(item, lst=[]):
    """危险!默认列表只创建一次"""
    lst.append(item)
    return lst

# 问题:多次调用共享同一个列表
print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - 不是预期的[2]!
print(append_to_list(3))  # [1, 2, 3]

# 正确示例:使用None作为默认值
def append_to_list_correct(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(append_to_list_correct(1))  # [1]
print(append_to_list_correct(2))  # [2] - 正确!
print(append_to_list_correct(3))  # [3]

# 原理:默认参数在函数定义时求值,只创建一次
# 可变对象(列表、字典)会在多次调用间共享
```

#### 陷阱2: 闭包中的变量绑定

```python
# 错误示例:循环中创建闭包
def create_multipliers_wrong():
    """错误的闭包示例"""
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)
    return multipliers

funcs = create_multipliers_wrong()
# 预期:[0, 2, 4, 6, 8],实际:
print([f(2) for f in funcs])  # [8, 8, 8, 8, 8]
# 所有函数都使用最后的i值(4)!

# 正确示例1:使用默认参数绑定值
def create_multipliers_correct1():
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x, i=i: x * i)  # i=i绑定当前值
    return multipliers

funcs = create_multipliers_correct1()
print([f(2) for f in funcs])  # [0, 2, 4, 6, 8] - 正确!

# 正确示例2:使用列表推导式
def create_multipliers_correct2():
    return [lambda x, i=i: x * i for i in range(5)]

funcs = create_multipliers_correct2()
print([f(2) for f in funcs])  # [0, 2, 4, 6, 8]
```

#### 陷阱3: 修改函数参数的副作用

```python
# 陷阱:修改可变参数会影响原对象
def remove_duplicates_wrong(lst):
    """错误:直接修改输入列表"""
    seen = set()
    for item in lst[:]:  # 必须遍历副本
        if item in seen:
            lst.remove(item)
        else:
            seen.add(item)
    return lst

original = [1, 2, 2, 3, 3, 3, 4]
result = remove_duplicates_wrong(original)
print(f"原列表: {original}")  # 被修改了!
print(f"结果: {result}")

# 正确方法1:返回新列表
def remove_duplicates_correct(lst):
    """不修改原列表"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

original = [1, 2, 2, 3, 3, 3, 4]
result = remove_duplicates_correct(original)
print(f"原列表: {original}")  # [1, 2, 2, 3, 3, 3, 4] - 未改变
print(f"结果: {result}")      # [1, 2, 3, 4]

# 正确方法2:使用列表推导式和dict.fromkeys
def remove_duplicates_better(lst):
    return list(dict.fromkeys(lst))  # 保持顺序且去重
```

#### 陷阱4: 递归深度限制

```python
# 递归函数的深度限制
def fibonacci_naive(n):
    """简单递归实现,效率低"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

# 问题1:计算大数时极慢
# print(fibonacci_naive(40))  # 需要几秒钟

# 问题2:递归太深会栈溢出
# print(fibonacci_naive(2000))  # RecursionError

# 解决方案1:使用记忆化(memoization)
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

print(fibonacci_memo(100))  # 很快!

# 解决方案2:使用迭代
def fibonacci_iter(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(fibonacci_iter(100))
```

#### 陷阱5: 全局变量的使用

```python
# 陷阱:意外使用全局变量
counter = 0

def increment_wrong():
    """错误:尝试修改全局变量"""
    # counter += 1  # UnboundLocalError!
    # Python认为counter是局部变量,但未赋值就使用
    pass

# 正确方法1:使用global声明
counter = 0

def increment_global():
    global counter
    counter += 1

increment_global()
print(counter)  # 1

# 正确方法2:返回新值(推荐)
def increment(value):
    return value + 1

counter = 0
counter = increment(counter)
print(counter)  # 1

# 最佳实践:避免使用全局变量
# 使用类或闭包代替
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

counter = Counter()
print(counter.increment())  # 1
print(counter.increment())  # 2
```

### 最佳实践建议

#### 实践1: 单一职责原则

```python
# 不推荐:一个函数做太多事
def process_user_data_wrong(data):
    """不好:函数职责太多"""
    # 验证数据
    if not data or not isinstance(data, dict):
        return None

    # 清理数据
    name = data.get('name', '').strip().title()
    email = data.get('email', '').lower()

    # 验证邮箱
    if '@' not in email:
        return None

    # 格式化输出
    return f"{name} <{email}>"

# 推荐:拆分为多个单一职责的函数
def validate_user_data(data):
    """只负责验证"""
    if not data or not isinstance(data, dict):
        return False
    if not data.get('name') or not data.get('email'):
        return False
    return True

def clean_user_data(data):
    """只负责清理"""
    return {
        'name': data.get('name', '').strip().title(),
        'email': data.get('email', '').lower()
    }

def validate_email(email):
    """只负责邮箱验证"""
    return '@' in email and '.' in email.split('@')[1]

def format_user_info(name, email):
    """只负责格式化"""
    return f"{name} <{email}>"

def process_user_data(data):
    """组合各个单一职责的函数"""
    if not validate_user_data(data):
        return None

    cleaned = clean_user_data(data)

    if not validate_email(cleaned['email']):
        return None

    return format_user_info(cleaned['name'], cleaned['email'])
```

#### 实践2: 使用类型提示(Type Hints)

```python
# Python 3.5+支持类型提示
from typing import List, Dict, Optional, Union

def greet(name: str) -> str:
    """带类型提示的函数"""
    return f"Hello, {name}!"

def sum_numbers(numbers: List[int]) -> int:
    """列表类型提示"""
    return sum(numbers)

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    """可选返回值"""
    # 返回用户字典或None
    if user_id > 0:
        return {'name': 'Alice', 'email': 'alice@example.com'}
    return None

def process_value(value: Union[int, float]) -> float:
    """联合类型"""
    return float(value) * 2

# 类型提示的好处:
# 1. 提高代码可读性
# 2. IDE可以提供更好的自动完成
# 3. 可以使用mypy等工具进行静态类型检查
# 4. 作为文档的一部分
```

#### 实践3: 使用文档字符串(Docstrings)

```python
def calculate_bmi(weight: float, height: float) -> float:
    """
    计算身体质量指数(BMI)。

    BMI = 体重(kg) / 身高²(m)

    参数:
        weight (float): 体重,单位为千克
        height (float): 身高,单位为米

    返回:
        float: BMI值

    异常:
        ValueError: 如果weight或height小于等于0

    示例:
        >>> calculate_bmi(70, 1.75)
        22.86

    注意:
        BMI标准:
        - 偏瘦: < 18.5
        - 正常: 18.5 - 24.9
        - 超重: 25 - 29.9
        - 肥胖: >= 30
    """
    if weight <= 0 or height <= 0:
        raise ValueError("体重和身高必须大于0")

    return round(weight / (height ** 2), 2)

# 访问文档字符串
print(calculate_bmi.__doc__)
# 或使用help()
# help(calculate_bmi)
```

#### 实践4: 错误处理

```python
# 不推荐:忽略错误或返回特殊值
def divide_wrong(a, b):
    """不好:返回None表示错误"""
    if b == 0:
        return None
    return a / b

# 推荐:抛出异常,让调用者处理
def divide_correct(a, b):
    """好:抛出异常"""
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

# 使用异常处理
try:
    result = divide_correct(10, 0)
except ValueError as e:
    print(f"错误: {e}")

# 自定义异常
class InvalidInputError(Exception):
    """自定义异常"""
    pass

def process_data(data):
    if not data:
        raise InvalidInputError("数据不能为空")
    return data.upper()

try:
    process_data("")
except InvalidInputError as e:
    print(f"输入错误: {e}")
```

#### 实践5: 合理使用*args和**kwargs

```python
# 好的使用场景:包装函数
def logged_function(func):
    """记录函数调用的装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用{func.__name__}, 参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__}返回: {result}")
        return result
    return wrapper

@logged_function
def add(a, b):
    return a + b

add(3, 5)

# 不好的使用:过度使用导致可读性下降
def bad_function(*args, **kwargs):
    """不好:调用者不知道需要什么参数"""
    # 难以维护和理解
    pass

# 好的实践:明确必需参数,可选参数用**kwargs
def good_function(required_param, optional_param=None, **extra_options):
    """好:清晰的参数结构"""
    print(f"必需: {required_param}")
    if optional_param:
        print(f"可选: {optional_param}")
    if extra_options:
        print(f"额外选项: {extra_options}")
```

### 实战项目示例

#### 项目1: 函数计算器

```python
def calculator_app():
    """功能完整的计算器应用"""

    def add(a, b):
        """加法"""
        return a + b

    def subtract(a, b):
        """减法"""
        return a - b

    def multiply(a, b):
        """乘法"""
        return a * b

    def divide(a, b):
        """除法"""
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b

    def power(a, b):
        """幂运算"""
        return a ** b

    def square_root(a):
        """平方根"""
        if a < 0:
            raise ValueError("不能对负数开平方根")
        return a ** 0.5

    # 操作映射
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide,
        '**': power,
        'sqrt': square_root
    }

    def get_number(prompt):
        """获取并验证数字输入"""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("❌ 无效输入,请输入数字")

    def calculate(operation, a, b=None):
        """执行计算"""
        try:
            if operation == 'sqrt':
                return operations[operation](a)
            else:
                if b is None:
                    raise ValueError("需要两个操作数")
                return operations[operation](a, b)
        except Exception as e:
            return f"错误: {e}"

    # 主程序
    print("="*50)
    print("函数计算器")
    print("="*50)
    print("支持的操作: +, -, *, /, ** (幂), sqrt (平方根)")
    print("输入 'quit' 退出")
    print("="*50)

    while True:
        operation = input("\n请选择操作: ").strip()

        if operation.lower() == 'quit':
            print("再见!")
            break

        if operation not in operations:
            print("❌ 不支持的操作")
            continue

        if operation == 'sqrt':
            num = get_number("请输入数字: ")
            result = calculate(operation, num)
            print(f"√{num} = {result}")
        else:
            num1 = get_number("请输入第一个数字: ")
            num2 = get_number("请输入第二个数字: ")
            result = calculate(operation, num1, num2)

            if isinstance(result, str):
                print(result)
            else:
                print(f"{num1} {operation} {num2} = {result}")

# 运行计算器
# calculator_app()
```

#### 项目2: 学生成绩管理系统(函数版)

```python
def student_management_system():
    """学生成绩管理系统"""

    students = {}  # 存储学生数据: {id: {'name': ..., 'scores': {...}}}

    def generate_id():
        """生成学生ID"""
        if not students:
            return 1001
        return max(students.keys()) + 1

    def add_student(name: str) -> int:
        """添加学生"""
        student_id = generate_id()
        students[student_id] = {
            'name': name,
            'scores': {}
        }
        return student_id

    def add_score(student_id: int, subject: str, score: float) -> bool:
        """添加成绩"""
        if student_id not in students:
            return False
        if not 0 <= score <= 100:
            return False

        students[student_id]['scores'][subject] = score
        return True

    def calculate_average(student_id: int) -> float:
        """计算学生平均分"""
        if student_id not in students:
            return 0.0

        scores = students[student_id]['scores']
        if not scores:
            return 0.0

        return sum(scores.values()) / len(scores)

    def get_grade(score: float) -> str:
        """根据分数获取等级"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def print_student_report(student_id: int):
        """打印学生成绩单"""
        if student_id not in students:
            print("学生不存在")
            return

        student = students[student_id]
        print("\n" + "="*50)
        print(f"学生ID: {student_id}")
        print(f"姓名: {student['name']}")
        print("-"*50)

        if not student['scores']:
            print("暂无成绩")
        else:
            print(f"{'科目':<15} {'分数':<10} {'等级':<5}")
            print("-"*50)
            for subject, score in student['scores'].items():
                grade = get_grade(score)
                print(f"{subject:<15} {score:<10.2f} {grade:<5}")

            avg = calculate_average(student_id)
            print("-"*50)
            print(f"平均分: {avg:.2f} ({get_grade(avg)})")
        print("="*50)

    def find_top_students(n: int = 3) -> list:
        """找出成绩最好的N个学生"""
        student_averages = []
        for sid, student in students.items():
            avg = calculate_average(sid)
            if avg > 0:
                student_averages.append((sid, student['name'], avg))

        # 按平均分降序排序
        student_averages.sort(key=lambda x: x[2], reverse=True)
        return student_averages[:n]

    def import_sample_data():
        """导入示例数据"""
        sample_students = [
            ("Alice", {"数学": 95, "英语": 88, "物理": 92}),
            ("Bob", {"数学": 87, "英语": 90, "物理": 85}),
            ("Charlie", {"数学": 78, "英语": 82, "物理": 80}),
            ("David", {"数学": 92, "英语": 95, "物理": 90}),
            ("Eve", {"数学": 88, "英语": 86, "物理": 89})
        ]

        for name, scores in sample_students:
            sid = add_student(name)
            for subject, score in scores.items():
                add_score(sid, subject, score)

        print(f"✓ 已导入{len(sample_students)}个学生数据")

    # 主程序
    print("="*50)
    print("学生成绩管理系统")
    print("="*50)

    while True:
        print("\n菜单:")
        print("1. 添加学生")
        print("2. 录入成绩")
        print("3. 查看成绩单")
        print("4. 显示排名")
        print("5. 导入示例数据")
        print("0. 退出")

        choice = input("\n请选择: ").strip()

        if choice == '0':
            print("再见!")
            break

        elif choice == '1':
            name = input("请输入学生姓名: ").strip()
            if name:
                sid = add_student(name)
                print(f"✓ 学生已添加,ID: {sid}")
            else:
                print("❌ 姓名不能为空")

        elif choice == '2':
            try:
                sid = int(input("请输入学生ID: "))
                if sid not in students:
                    print("❌ 学生不存在")
                    continue

                subject = input("请输入科目: ").strip()
                score = float(input("请输入分数(0-100): "))

                if add_score(sid, subject, score):
                    print("✓ 成绩已录入")
                else:
                    print("❌ 分数必须在0-100之间")

            except ValueError:
                print("❌ 输入无效")

        elif choice == '3':
            try:
                sid = int(input("请输入学生ID: "))
                print_student_report(sid)
            except ValueError:
                print("❌ 输入无效")

        elif choice == '4':
            if not students:
                print("暂无学生数据")
                continue

            top_students = find_top_students(5)
            print("\n" + "="*50)
            print("成绩排名(前5名)")
            print("="*50)
            print(f"{'排名':<6} {'学生ID':<10} {'姓名':<15} {'平均分':<10}")
            print("-"*50)

            for rank, (sid, name, avg) in enumerate(top_students, 1):
                print(f"{rank:<6} {sid:<10} {name:<15} {avg:<10.2f}")
            print("="*50)

        elif choice == '5':
            import_sample_data()

        else:
            print("❌ 无效的选择")

# 运行系统
# student_management_system()
```

> [!tip] 实战项目使用提示
> - 这些项目展示了函数在实际程序中的应用
> - 包含了参数传递、返回值、错误处理等核心概念
> - 可以运行这些程序来体验完整功能
> - 建议在理解后尝试扩展功能,如数据持久化、导出功能等

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
* 这篇笔记是[[MOC - Python|Python知识体系]]的核心部分
* 在[[Python - 类与面向对象]]中,方法本质上就是与对象关联的函数
* [[Python - 异常处理]]可以让函数更加健壮

## 编码规范

> [!important] PEP 8函数编写规范
> 1. 在给形参指定默认值时,等号两边不要有空格;函数调用中的关键字实参也应遵循这种约定
> 2. 如果程序或模块包含多个函数,可使用两个空行将相邻的函数分开
> 3. 所有import语句都应该放在文件开头
> 4. 函数名应该使用小写字母和下划线(snake_case)
