---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/intermediate"
  - "#lang/python"
status: 完善中
complexity: 中级
notetype: 学习笔记
resource: Python Crash Course
related:
  - "[[🐍 00_Python_MOC]]"
  - "[[Python基础 - 函数]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Python高级 - 异常处理

> [!abstract] 摘要
> 本笔记详细介绍Python中的异常处理机制,包括try-except-else-finally语句的使用和常见异常类型的处理方法。

## 🎯 Target
- [ ] 理解异常处理的重要性
- [ ] 掌握try-except-else-finally的使用
- [ ] 熟悉Python常见的异常类型
- [ ] 学会编写健壮的错误处理代码

## 📝 Core

### 异常处理基础

#### 概念
`try`用于异常处理的关键字,允许捕获和处理代码执行过程中的错误。作用在于遇到错误时程序不会崩溃,给了一个跳过崩溃的选择。

#### 基本结构
```python
try:
    # 可能引发异常的代码
    result = 10 / 0
except ZeroDivisionError:
    # 捕获到特定异常后的处理代码
    print("You can't divide by zero!")
else:
    # 如果没有异常发生,执行这部分代码
    print(f"Result: {result}")
finally:
    # 不管有没有异常,都会执行的代码
    print("Execution completed.")
```

### 各部分说明

#### try块
用于放置可能会引发异常的代码块。如果代码块中没有异常,`except`部分将不会执行。

```python
try:
    print(5 / 0)
except ZeroDivisionError:
    print("You can't divide by zero!")
```

#### except块
用于捕获指定类型的异常,并执行相应的处理逻辑。如果`try`块中的代码发生了异常,程序会跳转到对应的`except`块。

**捕获特定异常:**
```python
try:
    result = int("abc")
except ValueError:
    print("Invalid conversion!")
```

**捕获多个异常:**
```python
try:
    # 可能引发多种异常的代码
    value = int(input("Enter a number: "))
    result = 10 / value
except ValueError:
    print("Invalid input! Please enter a number.")
except ZeroDivisionError:
    print("You can't divide by zero!")
```

**使用as获取异常对象:**
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error occurred: {e}")
    # 输出: Error occurred: division by zero
```

> [!tip] 异常对象
> **`as e`** 将捕获的异常对象赋值给变量`e`,以便在`except`块中使用它。可以查看异常信息或执行特定的处理。

#### else块
可选部分。如果没有捕获到异常,`else`块中的代码会被执行。

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error!")
else:
    print(f"Result is {result}")  # 只在没有异常时执行
```

> [!tip] else的作用
> 将可能出错的代码放在`try`块中,将依赖于`try`块成功执行的代码放在`else`块中。

#### finally块
可选部分,不管是否发生异常,`finally`中的代码都会执行。通常用于清理资源等操作,如关闭文件或数据库连接。

```python
file = None
try:
    file = open('data.txt', 'r')
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    if file:
        file.close()  # 确保文件被关闭
    print("Cleanup completed.")
```

### Python常见异常类型

#### ZeroDivisionError
除数为零的错误:
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero!")
```

#### ValueError
传递给函数的参数值不符合要求:
```python
try:
    number = int("abc")
except ValueError:
    print("Invalid value for conversion!")
```

#### TypeError
操作或函数应用于错误类型的对象:
```python
try:
    result = "2" + 2
except TypeError:
    print("Cannot add string and integer!")
```

#### FileNotFoundError
文件未找到:
```python
try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
```

#### IndexError
索引超出范围:
```python
try:
    numbers = [1, 2, 3]
    print(numbers[10])
except IndexError:
    print("Index out of range!")
```

#### KeyError
字典中查找的键不存在:
```python
try:
    person = {'name': 'John'}
    age = person['age']
except KeyError:
    print("Key not found!")
```

#### AttributeError
尝试访问对象没有的属性:
```python
try:
    number = 42
    number.append(1)
except AttributeError:
    print("Object has no such attribute!")
```

### 实际应用示例

#### 文件操作
```python
def read_file(filename):
    """安全地读取文件内容"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Sorry, the file {filename} does not exist.")
        return None
    except PermissionError:
        print(f"You don't have permission to read {filename}.")
        return None
    else:
        return content
    finally:
        print("File operation completed.")

# 使用函数
content = read_file('data.txt')
if content:
    print(content)
```

#### 用户输入验证
```python
def get_positive_integer(prompt):
    """获取一个正整数"""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input! Please enter a number.")

# 使用函数
age = get_positive_integer("Enter your age: ")
print(f"Your age is {age}")
```

#### 静默失败 vs 报告错误
```python
# 方式1: 静默失败(不推荐用于调试)
try:
    risky_operation()
except Exception:
    pass  # 忽略所有错误

# 方式2: 记录错误(推荐)
try:
    risky_operation()
except Exception as e:
    print(f"Error occurred: {e}")
    # 或者使用logging模块记录错误
```

> [!warning] 避免过度使用
> 不要使用空的`except:`来捕获所有异常,这会隐藏程序的真实问题。至少应该打印错误信息或使用日志记录。

### 最佳实践

#### 1. 捕获具体的异常
```python
# 不好的做法
try:
    risky_operation()
except:  # 捕获所有异常
    print("Something went wrong")

# 好的做法
try:
    risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except TypeError as e:
    print(f"Type error: {e}")
```

#### 2. 使用else块分离逻辑
```python
try:
    data = fetch_data()
except NetworkError:
    print("Network error")
else:
    # 只在数据获取成功时处理
    process_data(data)
```

#### 3. 使用finally清理资源
```python
resource = acquire_resource()
try:
    use_resource(resource)
except Exception as e:
    handle_error(e)
finally:
    release_resource(resource)  # 确保资源被释放
```

#### 4. 使用with语句(推荐)
```python
# 自动处理资源清理
with open('file.txt', 'r') as file:
    content = file.read()
# 文件会自动关闭,即使发生异常
```

---
## 🤔 Q&A

### Q1: 什么时候应该使用异常处理?
**A**: 当代码可能遇到可预见的错误时使用,如:
- 文件操作(文件可能不存在)
- 用户输入(可能不符合预期格式)
- 网络请求(可能超时或失败)
- 数据转换(可能失败)

### Q2: try-except会影响性能吗?
**A**: 如果没有异常发生,try-except的性能开销很小。但频繁抛出和捕获异常会影响性能,因此不应该用异常来控制正常的程序流程。

### Q3: 应该捕获Exception还是具体的异常?
**A**: 应该捕获具体的异常。捕获`Exception`会隐藏程序的真实问题,使调试变得困难。只在确实需要捕获所有异常时才使用,并且要记录详细的错误信息。

### Q4: else和finally有什么区别?
**A**:
- **else**: 只在没有异常发生时执行
- **finally**: 无论是否发生异常都会执行,通常用于清理资源

## 🚀 Tasks
- [ ] 为文件操作添加完善的异常处理
- [ ] 编写一个健壮的用户输入验证函数
- [ ] 练习使用try-except-else-finally的完整结构
- [ ] 学习使用logging模块记录异常信息

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Errors and Exceptions
* Python官方文档 - Built-in Exceptions

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的重要部分
* 与[[Python基础 - 函数]]结合使用,编写更健壮的函数
* 在[[Python基础 - 类与面向对象]]中,方法也需要适当的异常处理
