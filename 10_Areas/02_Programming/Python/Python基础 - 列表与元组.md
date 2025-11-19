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

### 高级列表操作

#### 列表的深拷贝与浅拷贝

```python
import copy

# 浅拷贝 - 只复制第一层
original = [[1, 2], [3, 4]]
shallow = original[:]  # 或 original.copy() 或 list(original)

# 修改内层列表会影响浅拷贝
original[0][0] = 999
print(original)  # [[999, 2], [3, 4]]
print(shallow)   # [[999, 2], [3, 4]] - 也被修改了!

# 深拷贝 - 递归复制所有层
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

original[0][0] = 999
print(original)  # [[999, 2], [3, 4]]
print(deep)      # [[1, 2], [3, 4]] - 不受影响

# 实用示例:保护原始数据
def process_data(data):
    """处理数据,不影响原始数据"""
    # 创建深拷贝避免修改原数据
    working_data = copy.deepcopy(data)
    # 安全地修改working_data
    working_data[0][0] = 0
    return working_data

original_data = [[1, 2], [3, 4]]
result = process_data(original_data)
print(f"原始数据: {original_data}")  # [[1, 2], [3, 4]] - 未改变
print(f"处理结果: {result}")        # [[0, 2], [3, 4]]
```

#### 列表的高级方法

```python
# clear() - 清空列表
fruits = ['apple', 'banana', 'orange']
fruits.clear()
print(fruits)  # []

# copy() - 创建浅拷贝
original = [1, 2, 3]
duplicate = original.copy()
duplicate.append(4)
print(original)   # [1, 2, 3]
print(duplicate)  # [1, 2, 3, 4]

# index() - 查找元素索引
numbers = [10, 20, 30, 40, 30, 50]
print(numbers.index(30))      # 2 (第一次出现的位置)
print(numbers.index(30, 3))   # 4 (从索引3开始查找)
# print(numbers.index(99))    # ValueError - 元素不存在

# 安全的查找方法
def safe_index(lst, value):
    """安全查找,不存在时返回-1"""
    try:
        return lst.index(value)
    except ValueError:
        return -1

print(safe_index(numbers, 30))  # 2
print(safe_index(numbers, 99))  # -1

# count() - 统计元素出现次数
letters = ['a', 'b', 'a', 'c', 'a', 'b']
print(letters.count('a'))  # 3
print(letters.count('b'))  # 2
print(letters.count('z'))  # 0

# insert() - 在指定位置插入
numbers = [1, 2, 4, 5]
numbers.insert(2, 3)  # 在索引2处插入3
print(numbers)  # [1, 2, 3, 4, 5]
```

#### 列表推导式的高级用法

```python
# 基础列表推导式
squares = [x**2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# 带条件的列表推导式
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# if-else表达式
labels = ['even' if x % 2 == 0 else 'odd' for x in range(5)]
print(labels)  # ['even', 'odd', 'even', 'odd', 'even']

# 嵌套列表推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 二维列表推导式(创建矩阵)
matrix = [[i*3 + j for j in range(1, 4)] for i in range(3)]
print(matrix)  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# 多条件过滤
numbers = [x for x in range(1, 51) if x % 3 == 0 if x % 5 == 0]
print(numbers)  # [15, 30, 45] - 既能被3整除又能被5整除

# 字符串处理
words = ['hello', 'world', 'python', 'programming']
capitalized = [word.upper() for word in words if len(word) > 5]
print(capitalized)  # ['PYTHON', 'PROGRAMMING']

# 实用示例:处理CSV数据
csv_data = "1,2,3\n4,5,6\n7,8,9"
matrix = [[int(num) for num in line.split(',')]
          for line in csv_data.split('\n')]
print(matrix)  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

#### 多维列表操作

```python
# 创建二维列表
# 错误方式:
wrong_matrix = [[0] * 3] * 3  # 危险!所有行指向同一个列表
wrong_matrix[0][0] = 1
print(wrong_matrix)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] - 所有行都改变了!

# 正确方式:
correct_matrix = [[0 for _ in range(3)] for _ in range(3)]
correct_matrix[0][0] = 1
print(correct_matrix)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] - 只改变第一行

# 访问二维列表
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])  # 6 (第2行,第3列)

# 遍历二维列表
for row in matrix:
    for element in row:
        print(element, end=' ')
    print()  # 换行

# 使用索引遍历
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(f"matrix[{i}][{j}] = {matrix[i][j]}")

# 转置矩阵
transposed = [[matrix[j][i] for j in range(len(matrix))]
              for i in range(len(matrix[0]))]
print(transposed)  # [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# 使用zip转置(更简洁)
transposed = list(zip(*matrix))
print(transposed)  # [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
# 转换为列表的列表
transposed = [list(row) for row in zip(*matrix)]
```

#### enumerate和zip的妙用

```python
# enumerate() - 同时获取索引和值
fruits = ['apple', 'banana', 'orange']
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 输出:
# 0: apple
# 1: banana
# 2: orange

# 从1开始计数
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")

# zip() - 并行遍历多个列表
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['NYC', 'LA', 'Chicago']

for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age}, from {city}")

# 创建字典
person_dict = dict(zip(names, ages))
print(person_dict)  # {'Alice': 25, 'Bob': 30, 'Charlie': 35}

# zip处理不同长度的列表(截断到最短)
list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c']
result = list(zip(list1, list2))
print(result)  # [(1, 'a'), (2, 'b'), (3, 'c')]

# 解压缩(unzip)
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*pairs)
print(numbers)  # (1, 2, 3)
print(letters)  # ('a', 'b', 'c')

# 实用示例:同时修改多个列表
scores = [85, 90, 78]
weights = [0.3, 0.4, 0.3]
weighted_scores = [score * weight for score, weight in zip(scores, weights)]
print(weighted_scores)  # [25.5, 36.0, 23.4]
```

### 常见陷阱和错误

#### 陷阱1: 可变默认参数

```python
# 错误示例:使用可变对象作为默认参数
def add_item_wrong(item, items=[]):
    """危险!默认参数只创建一次"""
    items.append(item)
    return items

# 问题:多次调用会共享同一个列表
print(add_item_wrong('apple'))   # ['apple']
print(add_item_wrong('banana'))  # ['apple', 'banana'] - 不是预期的!
print(add_item_wrong('orange'))  # ['apple', 'banana', 'orange']

# 正确示例:使用None作为默认值
def add_item_correct(item, items=None):
    """正确的方式"""
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item_correct('apple'))   # ['apple']
print(add_item_correct('banana'))  # ['banana'] - 正确!
print(add_item_correct('orange'))  # ['orange']

# 或者每次都传入新列表
result1 = add_item_correct('apple', [])
result2 = add_item_correct('banana', [])
```

#### 陷阱2: 循环中修改列表

```python
# 错误示例:在遍历时删除元素
numbers = [1, 2, 3, 4, 5, 6]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # 危险!会跳过元素
print(numbers)  # [1, 3, 5, 6] - 6没有被删除!

# 正确方法1:使用列表推导式创建新列表
numbers = [1, 2, 3, 4, 5, 6]
numbers = [num for num in numbers if num % 2 != 0]
print(numbers)  # [1, 3, 5]

# 正确方法2:反向遍历
numbers = [1, 2, 3, 4, 5, 6]
for i in range(len(numbers) - 1, -1, -1):
    if numbers[i] % 2 == 0:
        del numbers[i]
print(numbers)  # [1, 3, 5]

# 正确方法3:使用filter
numbers = [1, 2, 3, 4, 5, 6]
numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(numbers)  # [1, 3, 5]
```

#### 陷阱3: 列表乘法的引用问题

```python
# 一维列表没问题
simple = [0] * 5
simple[0] = 1
print(simple)  # [1, 0, 0, 0, 0] - 正确

# 二维列表有问题
wrong_2d = [[0] * 3] * 3  # 所有行引用同一个列表!
wrong_2d[0][0] = 1
print(wrong_2d)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] - 错误!

# 验证都是同一个对象
print(wrong_2d[0] is wrong_2d[1])  # True - 是同一个列表!

# 正确方式:使用列表推导式
correct_2d = [[0] * 3 for _ in range(3)]
correct_2d[0][0] = 1
print(correct_2d)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] - 正确!
```

#### 陷阱4: 列表作为函数参数的修改

```python
def modify_list(lst):
    """函数内部修改列表会影响原列表"""
    lst.append(999)
    lst[0] = 0

my_list = [1, 2, 3]
modify_list(my_list)
print(my_list)  # [0, 2, 3, 999] - 原列表被修改了!

# 如果不想修改原列表,传入副本
my_list = [1, 2, 3]
modify_list(my_list[:])  # 传入副本
print(my_list)  # [1, 2, 3] - 原列表未改变

# 或在函数内部创建副本
def modify_list_safe(lst):
    """安全版本:不修改原列表"""
    new_list = lst[:]  # 创建副本
    new_list.append(999)
    new_list[0] = 0
    return new_list

my_list = [1, 2, 3]
result = modify_list_safe(my_list)
print(my_list)  # [1, 2, 3] - 原列表未改变
print(result)   # [0, 2, 3, 999] - 返回新列表
```

#### 陷阱5: 索引越界

```python
numbers = [1, 2, 3]

# 访问越界索引会报错
# print(numbers[10])  # IndexError: list index out of range

# 安全的访问方法
def safe_get(lst, index, default=None):
    """安全获取列表元素"""
    if 0 <= index < len(lst):
        return lst[index]
    return default

print(safe_get(numbers, 1))     # 2
print(safe_get(numbers, 10))    # None
print(safe_get(numbers, 10, 0)) # 0 (自定义默认值)

# 使用try-except
def get_element(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None

# 切片不会越界(自动调整)
print(numbers[1:100])  # [2, 3] - 不会报错
print(numbers[100:])   # [] - 返回空列表
```

### 最佳实践建议

#### 实践1: 使用列表推导式提高效率

```python
# 不推荐:传统循环
result = []
for i in range(10):
    if i % 2 == 0:
        result.append(i * 2)

# 推荐:列表推导式(更快、更清晰)
result = [i * 2 for i in range(10) if i % 2 == 0]

# 性能对比
import time

# 方法1:传统for循环
start = time.time()
result1 = []
for i in range(100000):
    result1.append(i * 2)
time1 = time.time() - start

# 方法2:列表推导式
start = time.time()
result2 = [i * 2 for i in range(100000)]
time2 = time.time() - start

print(f"传统循环: {time1:.4f}秒")
print(f"列表推导式: {time2:.4f}秒")
print(f"提升: {time1/time2:.2f}倍")
```

#### 实践2: 选择合适的数据结构

```python
# 频繁检查元素存在性:使用集合而非列表
# 不推荐
large_list = list(range(10000))
for i in range(100):
    if i in large_list:  # O(n)时间复杂度
        pass

# 推荐
large_set = set(range(10000))
for i in range(100):
    if i in large_set:  # O(1)时间复杂度
        pass

# 需要保持顺序且有重复:使用列表
# 需要保持顺序且无重复:使用列表+去重或OrderedDict
# 不关心顺序且无重复:使用集合
# 需要快速查找:使用字典或集合
```

#### 实践3: 避免不必要的列表拷贝

```python
# 不推荐:频繁创建新列表
def process_items(items):
    result = []
    for item in items:
        result = result + [item * 2]  # 每次都创建新列表!
    return result

# 推荐:就地修改
def process_items_better(items):
    result = []
    for item in items:
        result.append(item * 2)  # 就地添加
    return result

# 更推荐:列表推导式
def process_items_best(items):
    return [item * 2 for item in items]
```

#### 实践4: 使用enumerate而非range(len())

```python
fruits = ['apple', 'banana', 'orange']

# 不推荐
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# 推荐:更Pythonic
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

#### 实践5: 合理使用元组

```python
# 使用元组表示固定不变的数据
COORDINATES = (10, 20)
RGB_RED = (255, 0, 0)
SCREEN_SIZE = (1920, 1080)

# 函数返回多个值
def get_user_info():
    """返回用户信息(元组)"""
    return "Alice", 30, "NYC"  # 自动打包为元组

name, age, city = get_user_info()  # 解包

# 元组作为字典键
locations = {
    (0, 0): "origin",
    (1, 0): "east",
    (0, 1): "north"
}

# 交换变量值
a, b = 1, 2
a, b = b, a  # 使用元组实现优雅的交换
print(a, b)  # 2, 1
```

### 性能优化技巧

```python
import time

# 技巧1: 预分配列表大小(如果已知)
# 慢速方法
start = time.time()
slow_list = []
for i in range(1000000):
    slow_list.append(i)
print(f"动态增长: {time.time() - start:.4f}秒")

# 快速方法(预分配)
start = time.time()
fast_list = [0] * 1000000
for i in range(1000000):
    fast_list[i] = i
print(f"预分配: {time.time() - start:.4f}秒")

# 技巧2: 使用局部变量
def slow_sum(numbers):
    total = 0
    for num in numbers:
        total += num  # 每次都查找total
    return total

def fast_sum(numbers):
    _sum = sum  # 局部变量查找更快
    return _sum(numbers)

# 技巧3: 避免在循环中调用函数
items = ['a', 'b', 'c'] * 10000

# 慢
result = []
for item in items:
    result.append(item.upper())  # 每次都调用upper

# 快
upper = str.upper  # 提取方法到局部变量
result = [upper(item) for item in items]

# 技巧4: 使用内置函数
# 慢:手动求和
total = 0
for num in range(1000000):
    total += num

# 快:使用内置sum
total = sum(range(1000000))

# 技巧5: 列表vs生成器(内存优化)
# 列表:占用大量内存
big_list = [i**2 for i in range(1000000)]

# 生成器:按需生成,节省内存
big_gen = (i**2 for i in range(1000000))

# 如果只需要遍历一次,使用生成器
for value in big_gen:
    pass  # 处理value
```

### 实战项目示例

#### 项目1: 待办事项管理器

```python
class TodoManager:
    """待办事项管理器"""

    def __init__(self):
        self.todos = []
        self.completed = []

    def add_task(self, task):
        """添加任务"""
        if task and task not in self.todos:
            self.todos.append(task)
            print(f"✓ 已添加任务: {task}")
        else:
            print("✗ 任务为空或已存在")

    def remove_task(self, task):
        """删除任务"""
        if task in self.todos:
            self.todos.remove(task)
            print(f"✓ 已删除任务: {task}")
        else:
            print("✗ 任务不存在")

    def complete_task(self, task):
        """完成任务"""
        if task in self.todos:
            self.todos.remove(task)
            self.completed.append(task)
            print(f"✓ 已完成任务: {task}")
        else:
            print("✗ 任务不存在")

    def list_tasks(self):
        """列出所有任务"""
        if not self.todos:
            print("\n暂无待办任务")
        else:
            print("\n=== 待办任务 ===")
            for i, task in enumerate(self.todos, 1):
                print(f"{i}. [ ] {task}")

        if self.completed:
            print("\n=== 已完成 ===")
            for i, task in enumerate(self.completed, 1):
                print(f"{i}. [✓] {task}")

    def search_tasks(self, keyword):
        """搜索任务"""
        results = [task for task in self.todos if keyword.lower() in task.lower()]
        if results:
            print(f"\n找到 {len(results)} 个匹配任务:")
            for task in results:
                print(f"  - {task}")
        else:
            print("未找到匹配任务")

    def sort_tasks(self):
        """按字母顺序排序任务"""
        self.todos.sort()
        print("✓ 任务已排序")

    def clear_completed(self):
        """清空已完成任务"""
        count = len(self.completed)
        self.completed.clear()
        print(f"✓ 已清空 {count} 个已完成任务")

def todo_app():
    """待办事项应用主程序"""
    manager = TodoManager()

    print("=== 待办事项管理器 ===\n")

    while True:
        print("\n命令:")
        print("1. add     - 添加任务")
        print("2. list    - 列出任务")
        print("3. done    - 完成任务")
        print("4. remove  - 删除任务")
        print("5. search  - 搜索任务")
        print("6. sort    - 排序任务")
        print("7. clear   - 清空已完成")
        print("0. quit    - 退出")

        cmd = input("\n请选择操作: ").strip().lower()

        if cmd == '0' or cmd == 'quit':
            print("再见!")
            break
        elif cmd == '1' or cmd == 'add':
            task = input("输入任务: ").strip()
            manager.add_task(task)
        elif cmd == '2' or cmd == 'list':
            manager.list_tasks()
        elif cmd == '3' or cmd == 'done':
            manager.list_tasks()
            task_num = input("输入要完成的任务编号: ").strip()
            try:
                index = int(task_num) - 1
                if 0 <= index < len(manager.todos):
                    manager.complete_task(manager.todos[index])
                else:
                    print("✗ 无效的任务编号")
            except ValueError:
                print("✗ 请输入数字")
        elif cmd == '4' or cmd == 'remove':
            manager.list_tasks()
            task_num = input("输入要删除的任务编号: ").strip()
            try:
                index = int(task_num) - 1
                if 0 <= index < len(manager.todos):
                    manager.remove_task(manager.todos[index])
                else:
                    print("✗ 无效的任务编号")
            except ValueError:
                print("✗ 请输入数字")
        elif cmd == '5' or cmd == 'search':
            keyword = input("输入搜索关键词: ").strip()
            manager.search_tasks(keyword)
        elif cmd == '6' or cmd == 'sort':
            manager.sort_tasks()
        elif cmd == '7' or cmd == 'clear':
            manager.clear_completed()
        else:
            print("✗ 无效的命令")

# 运行应用
# todo_app()
```

#### 项目2: 成绩统计分析器

```python
def grade_analyzer():
    """学生成绩分析器"""

    students = []  # 存储学生信息: [(姓名, 成绩)]

    def add_student():
        """添加学生"""
        name = input("学生姓名: ").strip()
        if not name:
            print("姓名不能为空")
            return

        try:
            score = float(input("成绩(0-100): "))
            if not 0 <= score <= 100:
                print("成绩必须在0-100之间")
                return
            students.append((name, score))
            print(f"✓ 已添加学生: {name}, 成绩: {score}")
        except ValueError:
            print("请输入有效的成绩")

    def show_statistics():
        """显示统计信息"""
        if not students:
            print("暂无学生数据")
            return

        scores = [score for _, score in students]

        print("\n" + "="*50)
        print("成绩统计")
        print("="*50)
        print(f"学生总数: {len(students)}")
        print(f"最高分: {max(scores):.2f}")
        print(f"最低分: {min(scores):.2f}")
        print(f"平均分: {sum(scores)/len(scores):.2f}")
        print(f"中位数: {sorted(scores)[len(scores)//2]:.2f}")

        # 成绩分布
        grade_a = len([s for s in scores if s >= 90])
        grade_b = len([s for s in scores if 80 <= s < 90])
        grade_c = len([s for s in scores if 70 <= s < 80])
        grade_d = len([s for s in scores if 60 <= s < 70])
        grade_f = len([s for s in scores if s < 60])

        print("\n成绩分布:")
        print(f"  A (90-100): {grade_a} 人")
        print(f"  B (80-89):  {grade_b} 人")
        print(f"  C (70-79):  {grade_c} 人")
        print(f"  D (60-69):  {grade_d} 人")
        print(f"  F (<60):    {grade_f} 人")
        print("="*50)

    def show_ranking():
        """显示排名"""
        if not students:
            print("暂无学生数据")
            return

        # 按成绩降序排序
        sorted_students = sorted(students, key=lambda x: x[1], reverse=True)

        print("\n" + "="*50)
        print(f"{'排名':<6} {'姓名':<15} {'成绩':<10} {'等级':<5}")
        print("="*50)

        for rank, (name, score) in enumerate(sorted_students, 1):
            # 确定等级
            if score >= 90:
                grade = 'A'
            elif score >= 80:
                grade = 'B'
            elif score >= 70:
                grade = 'C'
            elif score >= 60:
                grade = 'D'
            else:
                grade = 'F'

            print(f"{rank:<6} {name:<15} {score:<10.2f} {grade:<5}")
        print("="*50)

    def search_student():
        """搜索学生"""
        keyword = input("输入学生姓名(支持模糊搜索): ").strip().lower()
        results = [(name, score) for name, score in students
                   if keyword in name.lower()]

        if results:
            print(f"\n找到 {len(results)} 个匹配结果:")
            for name, score in results:
                print(f"  {name}: {score:.2f}")
        else:
            print("未找到匹配的学生")

    def batch_import():
        """批量导入(示例数据)"""
        example_data = [
            ("Alice", 95),
            ("Bob", 87),
            ("Charlie", 92),
            ("David", 78),
            ("Eve", 88),
            ("Frank", 65),
            ("Grace", 91),
            ("Henry", 74),
            ("Iris", 89),
            ("Jack", 56)
        ]
        students.extend(example_data)
        print(f"✓ 已导入 {len(example_data)} 个学生数据")

    # 主程序
    print("=== 学生成绩分析器 ===\n")

    while True:
        print("\n命令:")
        print("1. 添加学生")
        print("2. 统计信息")
        print("3. 排名列表")
        print("4. 搜索学生")
        print("5. 导入示例数据")
        print("0. 退出")

        choice = input("\n请选择: ").strip()

        if choice == '0':
            print("再见!")
            break
        elif choice == '1':
            add_student()
        elif choice == '2':
            show_statistics()
        elif choice == '3':
            show_ranking()
        elif choice == '4':
            search_student()
        elif choice == '5':
            batch_import()
        else:
            print("无效的选择")

# 运行程序
# grade_analyzer()
```

> [!tip] 实战项目使用提示
> - 这些项目展示了列表和元组的实际应用
> - 可以运行这些程序来体验完整功能
> - 建议在理解后尝试扩展功能,如数据持久化、导出报表等

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
