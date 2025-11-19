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

### 字符串进阶操作

#### 字符串切片详解
字符串切片使用`[start:end:step]`语法,可以灵活地提取字符串的子串:

```python
text = "Python Programming"

# 基本切片
print(text[0:6])      # 输出: Python (索引0到5)
print(text[7:])       # 输出: Programming (从索引7到末尾)
print(text[:6])       # 输出: Python (从开头到索引5)
print(text[:])        # 输出: Python Programming (完整字符串)

# 负索引切片
print(text[-11:])     # 输出: Programming (倒数11个字符到末尾)
print(text[:-12])     # 输出: Python (从开头到倒数第12个字符之前)

# 步长切片
print(text[::2])      # 输出: Pto rgamn (每隔一个字符取一个)
print(text[1::2])     # 输出: yhn ormig (从索引1开始,每隔一个字符)
print(text[::-1])     # 输出: gnimmargorP nohtyP (反转字符串)
print(text[7::-1])    # 输出: P nohtyP (从索引7反向到开头)

# 实用技巧
# 1. 反转字符串
reversed_text = text[::-1]

# 2. 获取偶数位置字符
even_chars = text[::2]

# 3. 获取前半部分
half_length = len(text) // 2
first_half = text[:half_length]
```

> [!tip] 切片不会引发索引错误
> 与直接索引不同,切片操作即使超出范围也不会报错,会自动调整到有效范围。

#### 字符串查找和替换
Python提供了丰富的字符串搜索和修改方法:

```python
text = "Python is powerful. Python is easy. Python is popular."

# 查找方法
print(text.find("Python"))        # 输出: 0 (首次出现的位置)
print(text.find("Java"))          # 输出: -1 (未找到返回-1)
print(text.find("Python", 10))    # 输出: 20 (从索引10开始查找)
print(text.rfind("Python"))       # 输出: 40 (从右向左查找)
print(text.index("Python"))       # 输出: 0 (类似find,但未找到会抛出异常)
print(text.count("Python"))       # 输出: 3 (出现次数)

# 替换方法
new_text = text.replace("Python", "Java")
print(new_text)  # 所有"Python"都被替换为"Java"

# 只替换前2次出现
new_text = text.replace("Python", "Java", 2)
print(new_text)  # Python is powerful. Java is easy. Java is popular.

# 分割字符串
words = "apple,banana,orange,grape".split(",")
print(words)  # ['apple', 'banana', 'orange', 'grape']

# 按空白字符分割(默认)
sentence = "Python  is   awesome"
words = sentence.split()  # 自动处理多个空格
print(words)  # ['Python', 'is', 'awesome']

# 分割为行
multiline = "Line1\nLine2\nLine3"
lines = multiline.splitlines()
print(lines)  # ['Line1', 'Line2', 'Line3']

# 连接字符串列表
fruits = ['apple', 'banana', 'orange']
result = ", ".join(fruits)
print(result)  # apple, banana, orange

# 实用示例:清理CSV数据
csv_line = "  John , 25 , New York  "
cleaned_data = [item.strip() for item in csv_line.split(",")]
print(cleaned_data)  # ['John', '25', 'New York']
```

#### 字符串判断方法
这些方法用于检查字符串的特征,返回布尔值:

```python
# 数字判断
print("12345".isdigit())       # True (纯数字)
print("123.45".isdigit())      # False (包含小数点)
print("①②③".isdigit())        # True (Unicode数字也算)
print("123".isnumeric())       # True (包括Unicode数字字符)
print("½".isnumeric())         # True (分数也算数字)

# 字母判断
print("Python".isalpha())      # True (纯字母)
print("Python3".isalpha())     # False (包含数字)
print("中文".isalpha())         # True (中文字符也是字母)

# 字母数字判断
print("Python3".isalnum())     # True (字母或数字)
print("Python 3".isalnum())    # False (包含空格)

# 大小写判断
print("PYTHON".isupper())      # True (全大写)
print("python".islower())      # True (全小写)
print("Python".istitle())      # True (标题格式:每个单词首字母大写)

# 空白判断
print("   ".isspace())         # True (只包含空白字符)
print("  \n\t  ".isspace())    # True (包括换行符和制表符)
print("".isspace())            # False (空字符串不算)

# 前缀和后缀判断
filename = "document.pdf"
print(filename.startswith("doc"))      # True
print(filename.endswith(".pdf"))       # True
print(filename.endswith((".pdf", ".docx")))  # True (可检查多个后缀)

url = "https://www.example.com"
print(url.startswith(("http://", "https://")))  # True

# 实用示例:验证用户输入
def validate_username(username):
    """验证用户名:只能包含字母数字,长度3-20"""
    if not username.isalnum():
        return False, "用户名只能包含字母和数字"
    if len(username) < 3 or len(username) > 20:
        return False, "用户名长度必须在3-20之间"
    return True, "用户名有效"

# 测试
print(validate_username("user123"))    # (True, '用户名有效')
print(validate_username("user@123"))   # (False, '用户名只能包含字母和数字')
```

#### 多行字符串和原始字符串

```python
# 多行字符串(三引号)
# 方式1: 三个单引号
multiline1 = '''第一行
第二行
第三行'''

# 方式2: 三个双引号
multiline2 = """这是一个
跨越多行的
字符串"""

print(multiline1)

# 多行字符串常用于文档字符串
def example_function():
    """
    这是一个示例函数。

    参数说明:
        无参数

    返回值:
        返回None
    """
    pass

# 多行字符串用于SQL查询
sql_query = """
    SELECT name, age, city
    FROM users
    WHERE age > 18
    ORDER BY name
"""

# 多行字符串用于HTML模板
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <h1>Welcome</h1>
</body>
</html>
"""

# 原始字符串(r前缀)
# 不转义反斜杠,特别适合正则表达式和文件路径
normal_string = "C:\\Users\\name\\Documents"  # 需要转义
raw_string = r"C:\Users\name\Documents"       # 原始字符串,不需要转义
print(normal_string == raw_string)  # True

# 正则表达式中的应用
import re
pattern_normal = "\\d+\\.\\d+"    # 需要大量转义
pattern_raw = r"\d+\.\d+"          # 原始字符串,更清晰
# 两者等效,但原始字符串更易读

# 原始字符串的注意事项
# raw_string = r"test\"  # 错误! 原始字符串不能以单个反斜杠结尾
raw_string = r"test\\"   # 正确

# 组合使用:原始多行字符串
raw_multiline = r"""
Line 1: \n不会换行
Line 2: \t不会制表
Line 3: C:\path\to\file
"""
print(raw_multiline)
```

> [!tip] 最佳实践
> - 使用三引号字符串编写多行文本和文档字符串
> - 使用原始字符串r''处理Windows路径和正则表达式
> - 在需要保留格式的文本中使用多行字符串

### 数字类型 (Numbers)

#### 整数 (Integer)
Python中的整数可以进行基本的数学运算:`+`, `-`, `*`, `/`, `**`(幂运算)

#### 浮点数 (Float)
浮点数的特性:
- 将任意两个数相除,结果总是浮点数,即便这两个数都是整数且能整除
- 在其他任何运算中,如果一个操作数是整数,另一个操作数是浮点数,结果也总是浮点数
- 在Python中,无论是哪种运算,只要有操作数是浮点数,默认得到的就总是浮点数,即便结果原本为整数

### 数字类型详解

#### 整数除法和浮点除法的区别

```python
# 浮点除法 (/)
# 总是返回浮点数,即使能整除
print(10 / 2)      # 输出: 5.0 (浮点数)
print(10 / 3)      # 输出: 3.3333333333333335
print(7 / 2)       # 输出: 3.5

# 整数除法 (//)
# 也叫地板除,向下取整,返回整数部分
print(10 // 2)     # 输出: 5 (整数)
print(10 // 3)     # 输出: 3 (舍弃小数部分)
print(7 // 2)      # 输出: 3
print(-7 // 2)     # 输出: -4 (向下取整,不是向零取整!)

# 负数的地板除要特别注意
print(-10 // 3)    # 输出: -4 (不是-3!)
print(10 // -3)    # 输出: -4

# 取模运算 (%)
# 返回除法的余数
print(10 % 3)      # 输出: 1
print(7 % 2)       # 输出: 1
print(10 % 2)      # 输出: 0 (能整除,余数为0)

# 整数除法和取模的关系
# a == (a // b) * b + (a % b)
a, b = 17, 5
print(a == (a // b) * b + (a % b))  # True
print(f"{a} = {a // b} * {b} + {a % b}")  # 17 = 3 * 5 + 2

# 实用示例1: 判断奇偶数
def is_even(n):
    return n % 2 == 0

print(is_even(10))  # True
print(is_even(7))   # False

# 实用示例2: 时间转换
total_seconds = 3725
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
print(f"{total_seconds}秒 = {hours}小时{minutes}分{seconds}秒")
# 输出: 3725秒 = 1小时2分5秒
```

#### 数值类型转换

```python
# int() - 转换为整数
print(int(3.9))           # 输出: 3 (截断小数部分,不是四舍五入!)
print(int(-3.9))          # 输出: -3
print(int("123"))         # 输出: 123 (字符串转整数)
print(int("1010", 2))     # 输出: 10 (二进制字符串转整数)
print(int("FF", 16))      # 输出: 255 (十六进制字符串转整数)

# 注意:包含小数点的字符串不能直接转为int
# print(int("3.14"))      # ValueError! 需要先转为float
print(int(float("3.14"))) # 正确: 先转float再转int

# float() - 转换为浮点数
print(float(3))           # 输出: 3.0
print(float("3.14"))      # 输出: 3.14
print(float("inf"))       # 输出: inf (无穷大)
print(float("-inf"))      # 输出: -inf (负无穷大)

# str() - 转换为字符串
print(str(123))           # 输出: '123'
print(str(3.14))          # 输出: '3.14'
print(str(True))          # 输出: 'True'

# 类型转换的常见用途
# 1. 用户输入处理
age = int(input("请输入您的年龄: "))  # input()返回字符串,需要转换

# 2. 字符串拼接
score = 95
message = "你的分数是: " + str(score)  # 数字需要先转为字符串

# 3. 数值计算
result = int("100") + int("200")  # 字符串转数字后计算

# 转换失败会抛出异常
try:
    num = int("abc")  # ValueError: invalid literal for int()
except ValueError as e:
    print(f"转换失败: {e}")
```

#### 数学运算函数

```python
# abs() - 绝对值
print(abs(-10))          # 输出: 10
print(abs(-3.14))        # 输出: 3.14
print(abs(5))            # 输出: 5

# round() - 四舍五入
print(round(3.14159))         # 输出: 3 (默认取整)
print(round(3.14159, 2))      # 输出: 3.14 (保留2位小数)
print(round(3.14159, 3))      # 输出: 3.142
print(round(2.5))             # 输出: 2 (偶数舍入,遇到.5时向最近的偶数舍入)
print(round(3.5))             # 输出: 4

# pow() - 幂运算
print(pow(2, 3))         # 输出: 8 (2的3次方)
print(pow(2, -1))        # 输出: 0.5 (2的-1次方)
print(pow(2, 3, 5))      # 输出: 3 (2^3 % 5, 模幂运算,用于加密算法)

# 也可以使用 ** 运算符
print(2 ** 3)            # 输出: 8
print(9 ** 0.5)          # 输出: 3.0 (平方根)

# divmod() - 同时获取商和余数
quotient, remainder = divmod(17, 5)
print(f"17除以5,商为{quotient},余数为{remainder}")  # 商为3,余数为2

# 这等价于:
quotient = 17 // 5
remainder = 17 % 5

# max() 和 min() - 最大值和最小值
print(max(1, 5, 3, 9, 2))    # 输出: 9
print(min(1, 5, 3, 9, 2))    # 输出: 1
print(max([1, 5, 3, 9, 2]))  # 也可以传入列表

# sum() - 求和
print(sum([1, 2, 3, 4, 5]))  # 输出: 15
print(sum([1, 2, 3], 10))    # 输出: 16 (初始值为10)

# 更多数学函数需要导入math模块
import math

print(math.sqrt(16))         # 输出: 4.0 (平方根)
print(math.ceil(3.2))        # 输出: 4 (向上取整)
print(math.floor(3.8))       # 输出: 3 (向下取整)
print(math.pi)               # 输出: 3.141592653589793
print(math.e)                # 输出: 2.718281828459045

# 实用示例: 计算圆的面积
def circle_area(radius):
    """计算圆的面积"""
    return math.pi * radius ** 2

print(f"半径为5的圆面积: {circle_area(5):.2f}")
```

#### 科学计数法表示

```python
# 科学计数法:用e或E表示10的幂
large_number = 1.5e6     # 1.5 × 10^6 = 1500000.0
small_number = 1.5e-6    # 1.5 × 10^-6 = 0.0000015

print(large_number)      # 输出: 1500000.0
print(small_number)      # 输出: 1.5e-06

# 大数值会自动以科学计数法显示
huge_number = 10 ** 20
print(huge_number)       # 输出: 100000000000000000000

# 格式化输出科学计数法
value = 123456.789
print(f"{value:e}")      # 输出: 1.234568e+05
print(f"{value:.2e}")    # 输出: 1.23e+05 (保留2位小数)

# 实用示例: 物理常量
SPEED_OF_LIGHT = 3e8     # 光速: 3×10^8 m/s
PLANCK_CONSTANT = 6.626e-34  # 普朗克常数
AVOGADRO = 6.022e23      # 阿伏伽德罗常数

print(f"光速: {SPEED_OF_LIGHT:.2e} m/s")
print(f"普朗克常数: {PLANCK_CONSTANT} J·s")

# 科学计数法的运算
result = 1.5e6 * 2e3
print(result)            # 输出: 3000000000.0
print(f"{result:e}")     # 输出: 3.000000e+09
```

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

### 类型检查和转换

#### type()函数使用
`type()`函数用于查看变量的类型:

```python
# 基本数据类型
print(type(42))           # <class 'int'>
print(type(3.14))         # <class 'float'>
print(type("Hello"))      # <class 'str'>
print(type(True))         # <class 'bool'>
print(type(None))         # <class 'NoneType'>

# 复合数据类型
print(type([1, 2, 3]))    # <class 'list'>
print(type((1, 2, 3)))    # <class 'tuple'>
print(type({'a': 1}))     # <class 'dict'>
print(type({1, 2, 3}))    # <class 'set'>

# 比较类型
x = 42
if type(x) == int:
    print("x是整数")

# 获取类型名称
print(type(42).__name__)  # 'int'
```

#### isinstance()函数
`isinstance()`用于检查对象是否是某个类型的实例,比type()更灵活:

```python
# 基本用法
x = 42
print(isinstance(x, int))        # True
print(isinstance(x, float))      # False
print(isinstance(x, str))        # False

# 检查多个类型(元组)
y = 3.14
print(isinstance(y, (int, float)))  # True (y是int或float之一)

# isinstance vs type的区别
# isinstance支持继承关系
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True (支持父类检查)
print(type(dog) == Animal)       # False (type不支持继承)

# 实用示例:函数参数类型检查
def process_number(value):
    """处理数值,支持int和float"""
    if not isinstance(value, (int, float)):
        raise TypeError(f"期望数值类型,得到{type(value).__name__}")
    return value * 2

print(process_number(5))      # 10
print(process_number(5.5))    # 11.0
# process_number("5")         # TypeError
```

> [!tip] 最佳实践
> - 使用`isinstance()`而不是`type()`进行类型检查
> - isinstance()支持继承关系,更符合面向对象的设计原则
> - 在需要检查多个类型时,isinstance()更简洁

#### 隐式类型转换的陷阱

```python
# 陷阱1: 字符串和数字拼接
age = 25
# message = "I am " + age + " years old"  # TypeError! 不能自动转换
message = "I am " + str(age) + " years old"  # 正确:显式转换
# 或使用f-string
message = f"I am {age} years old"  # 推荐方式

# 陷阱2: 布尔值与数字运算
# Python中True等于1,False等于0
print(True + 5)       # 输出: 6
print(False * 10)     # 输出: 0
print(True == 1)      # True
print(False == 0)     # True

# 这可能导致意外结果
numbers = [1, 2, 3, 4, 5]
print(sum([True, True, False]))  # 输出: 2 (计数True的个数)

# 陷阱3: 字符串到数字的转换
num1 = "10"
num2 = "20"
# print(num1 + num2)  # 输出: "1020" (字符串拼接,不是加法!)
print(int(num1) + int(num2))  # 输出: 30 (正确的加法)

# 陷阱4: 除法返回类型
# Python 3中除法总是返回float
x = 10 / 2
print(type(x))  # <class 'float'> 而不是int!

# 如果需要整数,使用//
x = 10 // 2
print(type(x))  # <class 'int'>

# 陷阱5: 空值的布尔转换
# 以下值在布尔上下文中为False:
print(bool(0))           # False
print(bool(0.0))         # False
print(bool(""))          # False
print(bool([]))          # False
print(bool({}))          # False
print(bool(None))        # False

# 非空值为True
print(bool(1))           # True
print(bool(-1))          # True (负数也是True!)
print(bool("0"))         # True (字符串"0"不是空字符串)
print(bool([0]))         # True (包含0的列表不是空列表)

# 实用示例:避免类型转换陷阱
def safe_divide(a, b):
    """安全除法,返回int或float"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("参数必须是数字")
    if b == 0:
        raise ValueError("除数不能为零")

    result = a / b
    # 如果结果是整数,返回int类型
    if result == int(result):
        return int(result)
    return result

print(safe_divide(10, 2))    # 5 (int)
print(safe_divide(10, 3))    # 3.333... (float)
```

### 字符串格式化进阶

#### f-string的高级用法

```python
# 基础f-string
name = "Alice"
age = 30
print(f"My name is {name} and I am {age} years old.")

# 1. 对齐和填充
text = "Python"
print(f"|{text:<10}|")   # 左对齐,总宽度10: |Python    |
print(f"|{text:>10}|")   # 右对齐,总宽度10: |    Python|
print(f"|{text:^10}|")   # 居中对齐,总宽度10:|  Python  |
print(f"|{text:*^10}|")  # 居中对齐,用*填充:|**Python**|

# 数字对齐
number = 42
print(f"|{number:5}|")   # 右对齐(默认): |   42|
print(f"|{number:<5}|")  # 左对齐: |42   |
print(f"|{number:05}|")  # 零填充: |00042|

# 2. 精度控制(浮点数)
pi = 3.141592653589793
print(f"{pi:.2f}")       # 保留2位小数: 3.14
print(f"{pi:.4f}")       # 保留4位小数: 3.1416
print(f"{pi:10.2f}")     # 总宽度10,保留2位小数: |      3.14|

# 3. 千位分隔符
large_num = 1234567890
print(f"{large_num:,}")  # 1,234,567,890
print(f"{large_num:_}")  # 1_234_567_890 (下划线分隔)

# 4. 数字进制转换
num = 255
print(f"{num:b}")        # 二进制: 11111111
print(f"{num:o}")        # 八进制: 377
print(f"{num:x}")        # 十六进制(小写): ff
print(f"{num:X}")        # 十六进制(大写): FF
print(f"{num:#x}")       # 带前缀的十六进制: 0xff

# 5. 百分比格式化
ratio = 0.875
print(f"{ratio:.1%}")    # 87.5%
print(f"{ratio:.2%}")    # 87.50%

# 6. 科学计数法
big = 1234567890
print(f"{big:e}")        # 1.234568e+09
print(f"{big:.2e}")      # 1.23e+09

# 7. 表达式求值
x = 10
y = 20
print(f"{x} + {y} = {x + y}")  # 10 + 20 = 30
print(f"Square of {x} is {x**2}")  # Square of 10 is 100

# 8. 调用函数
def get_greeting(name):
    return f"Hello, {name}!"

name = "Bob"
print(f"{get_greeting(name)}")  # Hello, Bob!

# 9. 访问字典和列表
person = {"name": "Alice", "age": 30}
print(f"{person['name']} is {person['age']} years old.")

items = ["apple", "banana", "orange"]
print(f"First item: {items[0]}")

# 10. 调试技巧(Python 3.8+)
x = 10
y = 20
print(f"{x=}, {y=}, {x+y=}")  # x=10, y=20, x+y=30

# 实用示例:格式化表格
def print_table(data):
    """打印格式化的表格"""
    print(f"{'Name':<10} {'Age':>5} {'City':<15}")
    print("-" * 32)
    for row in data:
        print(f"{row['name']:<10} {row['age']:>5} {row['city']:<15}")

data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Chicago"},
]
print_table(data)
```

#### format()方法

```python
# 基本用法
print("Hello, {}!".format("World"))  # Hello, World!

# 位置参数
print("{0} and {1}".format("Tom", "Jerry"))  # Tom and Jerry
print("{1} and {0}".format("Tom", "Jerry"))  # Jerry and Tom

# 关键字参数
print("{name} is {age} years old".format(name="Alice", age=30))

# 混合使用
print("{0} loves {food}".format("Alice", food="pizza"))

# 格式说明符
print("{:.2f}".format(3.141592))     # 3.14
print("{:10}".format("test"))        # 'test      '
print("{:>10}".format("test"))       # '      test'
print("{:*^10}".format("test"))      # '***test***'

# 访问属性和索引
person = {"name": "Bob", "age": 25}
print("{0[name]} is {0[age]} years old".format(person))

# 数字格式化
print("{:,}".format(1234567))        # 1,234,567
print("{:.2%}".format(0.875))        # 87.50%
```

#### 老式%格式化

```python
# 虽然不推荐,但仍在一些老代码中使用

# 字符串
print("Hello, %s!" % "World")        # Hello, World!

# 整数
print("Number: %d" % 42)             # Number: 42

# 浮点数
print("Pi: %.2f" % 3.141592)         # Pi: 3.14

# 多个值(使用元组)
print("%s is %d years old" % ("Alice", 30))

# 字典格式化
print("%(name)s is %(age)d years old" % {"name": "Bob", "age": 25})

# 格式控制
print("%10s" % "test")               # 右对齐,宽度10
print("%-10s" % "test")              # 左对齐,宽度10
print("%05d" % 42)                   # 零填充: 00042
```

> [!tip] 格式化方法比较
> - **f-string** (推荐): 最简洁、高效、易读,Python 3.6+
> - **format()**: 兼容性好,适合模板字符串
> - **%格式化**: 老式方法,不推荐新代码使用

### 常见陷阱

#### 字符串不可变性导致的性能问题

```python
# 陷阱:在循环中反复拼接字符串(低效!)
# 错误示例
result = ""
for i in range(10000):
    result += str(i) + ","  # 每次都创建新字符串对象!
# 这会创建大量临时对象,性能很差

# 正确示例1: 使用列表和join
parts = []
for i in range(10000):
    parts.append(str(i))
result = ",".join(parts)  # 只创建一次最终字符串

# 正确示例2: 使用列表推导式
result = ",".join(str(i) for i in range(10000))

# 性能对比
import time

# 方法1: 直接拼接(慢)
start = time.time()
result = ""
for i in range(10000):
    result += str(i)
print(f"直接拼接耗时: {time.time() - start:.4f}秒")

# 方法2: join方法(快)
start = time.time()
result = "".join(str(i) for i in range(10000))
print(f"join方法耗时: {time.time() - start:.4f}秒")
```

#### 浮点数精度问题

```python
# 陷阱:浮点数不精确
print(0.1 + 0.2)         # 0.30000000000000004 (不是0.3!)
print(0.1 + 0.2 == 0.3)  # False

# 原因:二进制无法精确表示某些十进制小数
# 类似于1/3在十进制中是0.333...无限循环

# 解决方案1: 使用round()
result = round(0.1 + 0.2, 2)
print(result)  # 0.3
print(result == 0.3)  # True

# 解决方案2: 使用math.isclose()比较
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True

# 解决方案3: 使用decimal模块(精确十进制)
from decimal import Decimal
a = Decimal('0.1')
b = Decimal('0.2')
print(a + b)  # 0.3 (精确!)
print(a + b == Decimal('0.3'))  # True

# 金融计算必须使用Decimal
price = Decimal('19.99')
quantity = Decimal('3')
total = price * quantity
print(f"总价: ${total}")  # 总价: $59.97

# 陷阱:不要直接用浮点数比较
# 错误
if 0.1 + 0.2 == 0.3:
    print("Equal")  # 不会执行
else:
    print("Not equal")  # 会执行

# 正确
if math.isclose(0.1 + 0.2, 0.3):
    print("Equal")  # 会执行
```

#### 使用is vs ==比较的区别

```python
# == 比较值是否相等
# is 比较是否是同一个对象(内存地址)

# 对于小整数(-5到256),Python会缓存
a = 100
b = 100
print(a == b)  # True (值相等)
print(a is b)  # True (是同一个对象,因为在缓存范围内)

# 对于大整数,每次创建新对象
a = 1000
b = 1000
print(a == b)  # True (值相等)
print(a is b)  # False (不是同一个对象)

# 字符串的情况类似
s1 = "hello"
s2 = "hello"
print(s1 == s2)  # True
print(s1 is s2)  # True (短字符串会被缓存)

s1 = "hello world! " * 10
s2 = "hello world! " * 10
print(s1 == s2)  # True
print(s1 is s2)  # False (长字符串不缓存)

# 列表和字典永远不会缓存
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 == list2)  # True (内容相同)
print(list1 is list2)  # False (不同的对象)

# None的比较:应该用is
x = None
if x is None:  # 正确!
    print("x is None")

if x == None:  # 虽然能工作,但不推荐
    print("x == None")

# 实用建议
# 1. 比较None时,使用 is None 或 is not None
# 2. 比较True/False时,直接用布尔表达式
# 3. 比较值是否相等,用 ==
# 4. 检查是否同一对象,用 is

# 示例
def process(value=None):
    if value is None:  # 正确
        value = []
    return value

# 错误示例
def process_wrong(value=None):
    if not value:  # 危险! 0、[]、""都会被判断为True
        value = []
    return value

print(process_wrong(0))    # 返回[] (错误!)
print(process_wrong([]))   # 返回[] (正确)
```

### 实战示例

#### 实战1: 用户输入验证程序

```python
def validate_user_input():
    """完整的用户输入验证系统"""

    def validate_age(age_str):
        """验证年龄输入"""
        # 检查是否为数字
        if not age_str.isdigit():
            return False, "年龄必须是数字"

        age = int(age_str)
        if age < 0 or age > 150:
            return False, "年龄必须在0-150之间"

        return True, age

    def validate_email(email):
        """简单的邮箱验证"""
        if '@' not in email:
            return False, "邮箱必须包含@符号"

        if email.count('@') != 1:
            return False, "邮箱只能包含一个@符号"

        local, domain = email.split('@')
        if not local or not domain:
            return False, "邮箱格式不正确"

        if '.' not in domain:
            return False, "邮箱域名必须包含."

        return True, email

    def validate_phone(phone):
        """验证电话号码(仅数字,10-11位)"""
        # 移除空格和破折号
        clean_phone = phone.replace(' ', '').replace('-', '')

        if not clean_phone.isdigit():
            return False, "电话号码只能包含数字"

        if len(clean_phone) < 10 or len(clean_phone) > 11:
            return False, "电话号码长度应为10-11位"

        return True, clean_phone

    # 主程序
    print("=== 用户注册系统 ===\n")

    # 验证姓名
    while True:
        name = input("请输入姓名: ").strip()
        if len(name) >= 2:
            break
        print("错误: 姓名至少需要2个字符\n")

    # 验证年龄
    while True:
        age_input = input("请输入年龄: ").strip()
        is_valid, result = validate_age(age_input)
        if is_valid:
            age = result
            break
        print(f"错误: {result}\n")

    # 验证邮箱
    while True:
        email = input("请输入邮箱: ").strip()
        is_valid, result = validate_email(email)
        if is_valid:
            email = result
            break
        print(f"错误: {result}\n")

    # 验证电话
    while True:
        phone = input("请输入电话号码: ").strip()
        is_valid, result = validate_phone(phone)
        if is_valid:
            phone = result
            break
        print(f"错误: {result}\n")

    # 显示结果
    print("\n" + "="*40)
    print("注册成功!")
    print("="*40)
    print(f"姓名: {name}")
    print(f"年龄: {age}")
    print(f"邮箱: {email}")
    print(f"电话: {phone}")
    print("="*40)

# 运行程序
# validate_user_input()
```

#### 实战2: 简单计算器

```python
def calculator():
    """支持基本运算的计算器"""

    print("=== 简单计算器 ===")
    print("支持的运算: +, -, *, /, //, %, **")
    print("输入'quit'退出\n")

    while True:
        # 获取表达式
        expression = input("请输入计算表达式(如: 10 + 5): ").strip()

        if expression.lower() == 'quit':
            print("感谢使用!")
            break

        try:
            # 分割表达式
            parts = expression.split()

            if len(parts) != 3:
                print("错误: 请输入格式如: 10 + 5\n")
                continue

            num1_str, operator, num2_str = parts

            # 转换为数字
            num1 = float(num1_str)
            num2 = float(num2_str)

            # 执行运算
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    print("错误: 除数不能为零\n")
                    continue
                result = num1 / num2
            elif operator == '//':
                if num2 == 0:
                    print("错误: 除数不能为零\n")
                    continue
                result = num1 // num2
            elif operator == '%':
                if num2 == 0:
                    print("错误: 除数不能为零\n")
                    continue
                result = num1 % num2
            elif operator == '**':
                result = num1 ** num2
            else:
                print(f"错误: 不支持的运算符 '{operator}'\n")
                continue

            # 显示结果
            # 如果结果是整数,显示为整数
            if isinstance(result, float) and result == int(result):
                print(f"结果: {int(result)}\n")
            else:
                print(f"结果: {result:.6g}\n")  # 最多6位有效数字

        except ValueError:
            print("错误: 请输入有效的数字\n")
        except Exception as e:
            print(f"错误: {e}\n")

# 运行计算器
# calculator()
```

#### 实战3: 文本格式化工具

```python
def text_formatter():
    """文本格式化工具"""

    def format_title_case(text):
        """转换为标题格式"""
        return text.title()

    def format_sentence_case(text):
        """转换为句子格式(首字母大写)"""
        return text.capitalize()

    def format_snake_case(text):
        """转换为蛇形命名(snake_case)"""
        # 移除多余空格并用下划线连接
        words = text.lower().split()
        return "_".join(words)

    def format_camel_case(text):
        """转换为驼峰命名(camelCase)"""
        words = text.split()
        if not words:
            return ""
        return words[0].lower() + "".join(word.capitalize() for word in words[1:])

    def format_pascal_case(text):
        """转换为帕斯卡命名(PascalCase)"""
        words = text.split()
        return "".join(word.capitalize() for word in words)

    def count_words(text):
        """统计单词数"""
        return len(text.split())

    def count_chars(text):
        """统计字符数(包含空格)"""
        return len(text)

    def reverse_text(text):
        """反转文本"""
        return text[::-1]

    def remove_extra_spaces(text):
        """移除多余空格"""
        return " ".join(text.split())

    # 主程序
    print("=== 文本格式化工具 ===\n")

    text = input("请输入要格式化的文本: ")

    while True:
        print("\n" + "="*50)
        print("选择操作:")
        print("1. 标题格式 (Title Case)")
        print("2. 句子格式 (Sentence case)")
        print("3. 蛇形命名 (snake_case)")
        print("4. 驼峰命名 (camelCase)")
        print("5. 帕斯卡命名 (PascalCase)")
        print("6. 全大写 (UPPER CASE)")
        print("7. 全小写 (lower case)")
        print("8. 反转文本")
        print("9. 移除多余空格")
        print("10. 文本统计")
        print("0. 退出")
        print("="*50)

        choice = input("\n请选择操作(0-10): ").strip()

        if choice == '0':
            print("感谢使用!")
            break
        elif choice == '1':
            print(f"\n结果: {format_title_case(text)}")
        elif choice == '2':
            print(f"\n结果: {format_sentence_case(text)}")
        elif choice == '3':
            print(f"\n结果: {format_snake_case(text)}")
        elif choice == '4':
            print(f"\n结果: {format_camel_case(text)}")
        elif choice == '5':
            print(f"\n结果: {format_pascal_case(text)}")
        elif choice == '6':
            print(f"\n结果: {text.upper()}")
        elif choice == '7':
            print(f"\n结果: {text.lower()}")
        elif choice == '8':
            print(f"\n结果: {reverse_text(text)}")
        elif choice == '9':
            cleaned = remove_extra_spaces(text)
            print(f"\n结果: {cleaned}")
            text = cleaned  # 更新文本
        elif choice == '10':
            print(f"\n文本统计:")
            print(f"  字符数(含空格): {count_chars(text)}")
            print(f"  字符数(不含空格): {len(text.replace(' ', ''))}")
            print(f"  单词数: {count_words(text)}")
            print(f"  行数: {text.count(chr(10)) + 1}")
        else:
            print("错误: 无效的选择")

# 运行文本格式化工具
# text_formatter()
```

> [!tip] 实战示例使用提示
> - 这些示例展示了字符串和数字类型的实际应用
> - 可以直接运行这些函数来体验功能
> - 建议在理解后尝试自己扩展功能

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
