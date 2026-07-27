---
created: 2025-11-18
tags:
  - type/knowledge
  - topic/programming/python
---
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

### 高级控制流技巧

#### 嵌套循环

```python
# 打印乘法表
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i} × {j} = {i*j:2}", end="  ")
    print()  # 每行结束后换行

# 矩阵操作
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# 遍历矩阵
for row in matrix:
    for element in row:
        print(element, end=' ')
    print()

# 找出所有偶数
evens = []
for row in matrix:
    for element in row:
        if element % 2 == 0:
            evens.append(element)
print(evens)  # [2, 4, 6, 8]

# 使用列表推导式(更简洁)
evens = [element for row in matrix for element in row if element % 2 == 0]
```

#### for-else和while-else结构

```python
# for-else: 循环正常结束时执行else
def find_number(numbers, target):
    """在列表中查找目标数字"""
    for num in numbers:
        if num == target:
            print(f"找到了: {target}")
            break
    else:
        # 只有当循环正常结束(没有break)时才执行
        print(f"没找到: {target}")

find_number([1, 2, 3, 4, 5], 3)  # 找到了: 3
find_number([1, 2, 3, 4, 5], 10) # 没找到: 10

# while-else: 条件变为False时执行else
count = 0
while count < 5:
    print(count, end=' ')
    count += 1
else:
    print("\n循环正常结束")

# 使用break会跳过else
count = 0
while count < 10:
    if count == 3:
        break
    count += 1
else:
    print("这不会打印")  # 不会执行,因为使用了break

# 实用示例:验证输入
def get_valid_number():
    """获取有效的正整数"""
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            num = int(input("请输入正整数: "))
            if num > 0:
                return num
            else:
                print("必须是正数")
        except ValueError:
            print("无效输入")
        attempts += 1
    else:
        print("超过最大尝试次数")
        return None
```

#### 循环控制语句的高级用法

```python
# 在嵌套循环中使用break和continue

# 例1:九九乘法表(只打印下三角)
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j:2}", end="  ")
    print()

# 例2:查找质数
def is_prime(n):
    """判断是否为质数"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False  # 找到因子,不是质数
    else:
        return True  # 循环正常结束,是质数

# 打印100以内的质数
primes = [n for n in range(2, 101) if is_prime(n)]
print(primes)

# 例3:跳过特定条件
for i in range(1, 21):
    # 跳过能被3整除的数
    if i % 3 == 0:
        continue
    # 遇到15停止
    if i == 15:
        break
    print(i, end=' ')
print()  # 输出: 1 2 4 5 7 8 10 11 13 14
```

#### 列表推导式中的条件

```python
# 基础:过滤
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# if-else表达式(三元运算符)
labels = ['even' if x % 2 == 0 else 'odd' for x in range(5)]
print(labels)  # ['even', 'odd', 'even', 'odd', 'even']

# 多重条件
numbers = [x for x in range(1, 101)
           if x % 2 == 0  # 偶数
           if x % 3 == 0  # 且能被3整除
           if x % 5 == 0] # 且能被5整除
print(numbers)  # [30, 60, 90]

# 嵌套推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 带条件的嵌套推导式
evens_from_matrix = [num for row in matrix for num in row if num % 2 == 0]
print(evens_from_matrix)  # [2, 4, 6, 8]
```

### 常见陷阱和错误

#### 陷阱1: 无限循环

```python
# 错误示例:忘记更新循环条件
# count = 0
# while count < 5:
#     print(count)
#     # 忘记增加count,导致无限循环!
#     # count += 1

# 正确示例
count = 0
while count < 5:
    print(count)
    count += 1  # 必须更新条件

# 常见错误:条件永远为True
# while True:
#     print("This will run forever")
#     # 没有break语句!

# 正确:提供退出条件
while True:
    user_input = input("输入'quit'退出: ")
    if user_input == 'quit':
        break

# 陷阱:使用浮点数作为循环条件
# 错误
# x = 0.0
# while x != 1.0:  # 由于浮点精度问题,可能永远不等于1.0
#     x += 0.1
#     print(x)

# 正确:使用范围判断
x = 0.0
while x < 1.0:
    x += 0.1
    print(f"{x:.1f}")
```

#### 陷阱2: 修改正在遍历的列表

```python
# 错误示例:在循环中删除元素
numbers = [1, 2, 3, 4, 5, 6]
# 错误!
# for num in numbers:
#     if num % 2 == 0:
#         numbers.remove(num)  # 会跳过元素
# print(numbers)  # 结果不符合预期

# 正确方法1:创建新列表
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

#### 陷阱3: range()的边界问题

```python
# 常见错误:认为range包含结束值
# range(1, 5)生成的是1, 2, 3, 4,不包括5
for i in range(1, 5):
    print(i, end=' ')  # 输出: 1 2 3 4
print()

# 访问列表最后一个元素
numbers = [10, 20, 30, 40, 50]
# 错误:使用len()作为索引
# print(numbers[len(numbers)])  # IndexError!

# 正确:减1或使用-1
print(numbers[len(numbers) - 1])  # 50
print(numbers[-1])  # 50

# 遍历列表索引
numbers = [10, 20, 30]
# 正确
for i in range(len(numbers)):
    print(f"Index {i}: {numbers[i]}")

# 更Pythonic:使用enumerate
for i, num in enumerate(numbers):
    print(f"Index {i}: {num}")
```

#### 陷阱4: 条件判断的逻辑错误

```python
# 错误:使用and时应该用or
age = 25
# 错误逻辑:年龄不可能同时小于18且大于65
# if age < 18 and age > 65:
#     print("特殊票价")

# 正确:使用or
if age < 18 or age > 65:
    print("特殊票价")

# 错误:判断多个值时的写法
x = 5
# 错误写法
# if x == 1 or 2 or 3:  # 永远为True!因为2和3总是True
#     print("x is 1, 2, or 3")

# 正确写法1
if x == 1 or x == 2 or x == 3:
    print("x is 1, 2, or 3")

# 正确写法2(更简洁)
if x in [1, 2, 3]:
    print("x is 1, 2, or 3")

# 正确写法3
if x in (1, 2, 3):
    print("x is 1, 2, or 3")
```

#### 陷阱5: 可变对象作为默认参数

```python
# 虽然这不是控制流问题,但经常在循环中暴露

# 错误示例
def add_to_list(value, lst=[]):
    """危险!默认列表只创建一次"""
    lst.append(value)
    return lst

# 问题:多次调用共享同一个列表
print(add_to_list(1))  # [1]
print(add_to_list(2))  # [1, 2] - 不是预期的[2]!
print(add_to_list(3))  # [1, 2, 3]

# 正确示例
def add_to_list_correct(value, lst=None):
    if lst is None:
        lst = []
    lst.append(value)
    return lst

print(add_to_list_correct(1))  # [1]
print(add_to_list_correct(2))  # [2] - 正确!
print(add_to_list_correct(3))  # [3]
```

### 最佳实践建议

#### 实践1: 优先使用for循环而非while循环

```python
# 不推荐:使用while实现计数
i = 0
while i < 10:
    print(i)
    i += 1

# 推荐:使用for循环
for i in range(10):
    print(i)

# 原因:
# 1. for循环更简洁
# 2. 不容易出现无限循环
# 3. 更符合Python风格

# while循环适用场景:
# 1. 不知道循环次数
# 2. 等待某个条件满足
# 3. 用户交互程序

# 示例:等待用户输入
while True:
    response = input("继续吗?(y/n): ")
    if response.lower() == 'n':
        break
```

#### 实践2: 使用enumerate代替range(len())

```python
items = ['apple', 'banana', 'orange']

# 不推荐
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# 推荐:更Pythonic
for i, item in enumerate(items):
    print(f"{i}: {item}")

# enumerate还可以指定起始索引
for i, item in enumerate(items, start=1):
    print(f"{i}. {item}")
```

#### 实践3: 避免深层嵌套

```python
# 不推荐:深层嵌套
def process_data(data):
    if data:
        if isinstance(data, list):
            if len(data) > 0:
                for item in data:
                    if item > 0:
                        print(item)

# 推荐:早返回,减少嵌套
def process_data_better(data):
    """使用早返回和守卫语句"""
    # 守卫语句
    if not data:
        return
    if not isinstance(data, list):
        return
    if len(data) == 0:
        return

    # 主要逻辑
    for item in data:
        if item > 0:
            print(item)

# 更推荐:使用列表推导式
def process_data_best(data):
    if not data or not isinstance(data, list):
        return

    positive_items = [item for item in data if item > 0]
    for item in positive_items:
        print(item)
```

#### 实践4: 合理使用break和continue

```python
# break:立即退出循环
# continue:跳过本次迭代

# 好的使用场景
def find_first_negative(numbers):
    """查找第一个负数"""
    for num in numbers:
        if num < 0:
            return num  # 或使用break
    return None

# 使用continue简化逻辑
def process_valid_items(items):
    """只处理有效项"""
    for item in items:
        # 跳过无效项
        if not item or item == "":
            continue

        # 处理有效项
        print(f"处理: {item}")
        # 更多处理逻辑...

# 避免过度使用
# 不好:过多的continue使代码难以理解
# def process_numbers(numbers):
#     for num in numbers:
#         if num < 0:
#             continue
#         if num > 100:
#             continue
#         if num % 2 != 0:
#             continue
#         print(num)

# 好:使用清晰的条件
def process_numbers(numbers):
    for num in numbers:
        if 0 <= num <= 100 and num % 2 == 0:
            print(num)
```

#### 实践5: 使用生成器优化内存

```python
# 列表推导式:一次性创建整个列表
squares_list = [x**2 for x in range(1000000)]  # 占用大量内存

# 生成器表达式:按需生成
squares_gen = (x**2 for x in range(1000000))  # 几乎不占内存

# 如果只需要遍历一次,使用生成器
for square in squares_gen:
    pass  # 处理每个值

# 生成器函数
def fibonacci_generator(n):
    """生成斐波那契数列"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# 使用生成器
for num in fibonacci_generator(10):
    print(num, end=' ')
print()  # 输出: 0 1 1 2 3 5 8 13 21 34
```

### 实战项目示例

#### 项目1: 猜数字游戏

```python
import random

def guessing_game():
    """猜数字游戏"""

    print("=== 猜数字游戏 ===")
    print("我想了一个1到100之间的数字,你能猜中吗?\n")

    # 生成随机数
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    while attempts < max_attempts:
        remaining = max_attempts - attempts

        try:
            # 获取用户输入
            guess = int(input(f"还有{remaining}次机会,请输入你的猜测: "))

            # 验证输入范围
            if guess < 1 or guess > 100:
                print("请输入1到100之间的数字!")
                continue

            attempts += 1

            # 判断结果
            if guess == secret_number:
                print(f"\n🎉 恭喜!你猜对了!")
                print(f"答案是 {secret_number}")
                print(f"你用了 {attempts} 次机会")
                break
            elif guess < secret_number:
                print("❌ 太小了!往大了猜")
            else:
                print("❌ 太大了!往小了猜")

        except ValueError:
            print("无效输入!请输入数字")
            continue

    else:
        # 循环正常结束(没有break),说明没猜中
        print(f"\n😢 游戏结束!你没有猜中")
        print(f"正确答案是: {secret_number}")

    # 询问是否再玩一次
    play_again = input("\n再玩一次吗?(y/n): ")
    if play_again.lower() == 'y':
        guessing_game()  # 递归调用

# 运行游戏
# guessing_game()
```

#### 项目2: 简单ATM系统

```python
def atm_system():
    """简单的ATM系统"""

    # 模拟账户数据
    accounts = {
        '1001': {'name': 'Alice', 'pin': '1234', 'balance': 5000},
        '1002': {'name': 'Bob', 'pin': '5678', 'balance': 3000},
        '1003': {'name': 'Charlie', 'pin': '9999', 'balance': 10000}
    }

    print("="*50)
    print("欢迎使用ATM系统")
    print("="*50)

    # 登录验证
    max_login_attempts = 3
    login_attempts = 0
    current_account = None

    while login_attempts < max_login_attempts:
        account_id = input("\n请输入账号: ")

        if account_id not in accounts:
            print("❌ 账号不存在")
            login_attempts += 1
            continue

        pin = input("请输入密码: ")

        if pin != accounts[account_id]['pin']:
            print("❌ 密码错误")
            login_attempts += 1
            remaining = max_login_attempts - login_attempts
            if remaining > 0:
                print(f"还有{remaining}次尝试机会")
            continue

        # 登录成功
        current_account = account_id
        print(f"\n✓ 欢迎, {accounts[current_account]['name']}!")
        break
    else:
        print("\n❌ 登录失败次数过多,系统锁定")
        return

    # 主菜单
    while True:
        print("\n" + "="*50)
        print("ATM主菜单")
        print("="*50)
        print("1. 查询余额")
        print("2. 存款")
        print("3. 取款")
        print("4. 转账")
        print("0. 退出")
        print("="*50)

        choice = input("\n请选择操作: ")

        if choice == '0':
            print(f"\n感谢使用,再见 {accounts[current_account]['name']}!")
            break

        elif choice == '1':
            # 查询余额
            balance = accounts[current_account]['balance']
            print(f"\n当前余额: ¥{balance:.2f}")

        elif choice == '2':
            # 存款
            try:
                amount = float(input("请输入存款金额: "))
                if amount <= 0:
                    print("❌ 金额必须大于0")
                    continue

                accounts[current_account]['balance'] += amount
                new_balance = accounts[current_account]['balance']
                print(f"✓ 存款成功!")
                print(f"存款金额: ¥{amount:.2f}")
                print(f"当前余额: ¥{new_balance:.2f}")

            except ValueError:
                print("❌ 无效的金额")

        elif choice == '3':
            # 取款
            try:
                amount = float(input("请输入取款金额: "))

                if amount <= 0:
                    print("❌ 金额必须大于0")
                    continue

                current_balance = accounts[current_account]['balance']

                if amount > current_balance:
                    print(f"❌ 余额不足!当前余额: ¥{current_balance:.2f}")
                    continue

                accounts[current_account]['balance'] -= amount
                new_balance = accounts[current_account]['balance']
                print(f"✓ 取款成功!")
                print(f"取款金额: ¥{amount:.2f}")
                print(f"当前余额: ¥{new_balance:.2f}")

            except ValueError:
                print("❌ 无效的金额")

        elif choice == '4':
            # 转账
            target_account = input("请输入对方账号: ")

            if target_account not in accounts:
                print("❌ 对方账号不存在")
                continue

            if target_account == current_account:
                print("❌ 不能转账给自己")
                continue

            try:
                amount = float(input("请输入转账金额: "))

                if amount <= 0:
                    print("❌ 金额必须大于0")
                    continue

                current_balance = accounts[current_account]['balance']

                if amount > current_balance:
                    print(f"❌ 余额不足!当前余额: ¥{current_balance:.2f}")
                    continue

                # 确认转账
                target_name = accounts[target_account]['name']
                confirm = input(f"确认转账¥{amount:.2f}给{target_name}?(y/n): ")

                if confirm.lower() == 'y':
                    # 执行转账
                    accounts[current_account]['balance'] -= amount
                    accounts[target_account]['balance'] += amount

                    new_balance = accounts[current_account]['balance']
                    print(f"✓ 转账成功!")
                    print(f"转账金额: ¥{amount:.2f}")
                    print(f"收款人: {target_name}")
                    print(f"当前余额: ¥{new_balance:.2f}")
                else:
                    print("转账已取消")

            except ValueError:
                print("❌ 无效的金额")

        else:
            print("❌ 无效的选择")

# 运行ATM系统
# atm_system()
```

> [!tip] 实战项目使用提示
> - 这些项目展示了控制流在实际程序中的应用
> - 包含了if-elif-else、while循环、break/continue等控制流语句
> - 可以运行这些程序来体验完整功能
> - 建议在理解后尝试扩展功能,如添加交易历史、利息计算等

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
* 这篇笔记是[[MOC - Python|Python知识体系]]的核心部分
* 与[[Python - 列表与元组]]结合使用,实现数据的遍历和处理
* 在[[Python - 函数]]和[[Python - 类与面向对象]]中会频繁使用控制流
