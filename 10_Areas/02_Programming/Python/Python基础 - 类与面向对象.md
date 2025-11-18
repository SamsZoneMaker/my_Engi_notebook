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
# Python基础 - 类与面向对象

> [!abstract] 摘要
> 本笔记详细介绍Python中的类(Class)和面向对象编程(OOP),包括类的定义、实例创建、继承、组合和模块化等核心概念。

## 🎯 Target
- [ ] 理解面向对象编程的基本概念
- [ ] 掌握类的定义和实例的创建
- [ ] 熟练使用__init__()方法初始化对象
- [ ] 理解继承和组合的使用场景
- [ ] 学会类的模块化和导入

## 📝 Core

### 面向对象编程基础

#### 概念
**面向对象编程(Object-Oriented Programming, OOP)**: 在面向对象编程中,你编写表示现实世界中的事物和情景的**类(class)**,并基于这些类来创建**对象(object)**。

在编写类的时候,要定义一批具有**通用行为**的对象,达到的目的是用更少的代码做更多的事情。

#### 类与实例
- **类(Class)**: 对象的蓝图或模板
- **实例(Instance/Object)**: 根据类创建的具体对象

### 创建和使用类

#### 示例:Dog类
```python
class Dog:
    """A simple attempt to model a dog."""

    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name
        self.age = age

    def sit(self):
        """Simulate a dog sitting in response to a command."""
        print(f"{self.name.title()} is now sitting.")

    def roll_over(self):
        """Simulate rolling over in response to a command."""
        print(f"{self.name.title()} rolled over!")
```

> [!tip] 类命名约定
> - 类名采用驼峰命名法(CamelCase),首字母大写
> - 类名后面不需要括号(除非继承其他类)

#### 方法的概念
类中的函数统称为**方法(Method)**。方法与函数的主要区别是方法与对象相关联。

### __init__()方法

#### 特殊方法(构造函数)
`__init__()`是一个特殊方法,当创建类的实例时会自动调用,用于初始化对象。

```python
def __init__(self, name, age):
    """Initialize name and age attributes."""
    self.name = name
    self.age = age
```

**关键点:**
- `self`是必不可少的,且需放在第一位
- `self`是指向实例本身的引用,让实例可以访问类中的属性和方法
- 创建实例时,Python会自动传入实参给`self`
- 通过实参传送的参数会直接交给`name`和`age`

#### 属性(Attributes)
前缀带有`self`的变量称为**属性**,可以被类中所有的方法使用。

```python
self.name = name  # 将参数值赋给属性
self.age = age
```

### 根据类创建实例

#### 创建实例
```python
my_dog = Dog('doudou', 3)
```

- `Dog`是类,首字母大写
- `my_dog`是创建的实例
- 可理解为此时其中一个`self = my_dog`

#### 访问属性
```python
print(my_dog.name)  # 输出: doudou
print(my_dog.age)   # 输出: 3
```

#### 调用方法
```python
my_dog.sit()        # 输出: Doudou is now sitting.
my_dog.roll_over()  # 输出: Doudou rolled over!
```

#### 创建多个实例
```python
my_dog = Dog('doudou', 3)
your_dog = Dog('lucy', 5)

print(f"My dog is {my_dog.name}.")
print(f"Your dog is {your_dog.name}.")
```

### 使用类和实例

#### 修改属性的值

**1. 直接修改属性**
```python
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0  # 默认值

my_car = Car('audi', 'a4', 2019)
my_car.odometer_reading = 23  # 直接修改
```

**2. 通过方法修改属性**
```python
class Car:
    # ...省略__init__...

    def update_odometer(self, mileage):
        """Set the odometer reading to the given value."""
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")

my_car = Car('audi', 'a4', 2019)
my_car.update_odometer(23)  # 通过方法修改
```

> [!tip] 为什么使用方法修改?
> 通过方法修改属性的好处:
> - 可以添加验证逻辑
> - 可以保留更新前的数据
> - 提供更好的封装性

**3. 通过方法让属性递增**
```python
class Car:
    # ...省略其他方法...

    def increment_odometer(self, miles):
        """Add the given amount to the odometer reading."""
        self.odometer_reading += miles

my_car = Car('audi', 'a4', 2019)
my_car.update_odometer(23000)
my_car.increment_odometer(100)
print(my_car.odometer_reading)  # 输出: 23100
```

### 继承

#### 概念和优势
- 当一个类是既有类的特殊版本时,可以使用继承
- 子类会自动获取父类的所有属性和方法
- 子类可以自定义新的属性和方法

#### 基本语法
```python
class Car:
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        print(f"This car has {self.odometer_reading} miles on it.")

class ElectricCar(Car):
    """Represent aspects of a car, specific to electric vehicles."""

    def __init__(self, make, model, year):
        """Initialize attributes of the parent class."""
        super().__init__(make, model, year)
        self.battery_size = 75  # 子类特有的属性

my_tesla = ElectricCar('tesla', 'model s', 2019)
print(my_tesla.get_descriptive_name())  # 继承父类方法
```

**关键点:**
- 父类必须在当前文件中,且位于子类的前面
- 子类定义时,括号内是父类的名称
- `super().__init__()`调用父类的初始化方法
- `super()`不需要`self`参数

#### 重写父类方法
子类可以重写父类的方法:

```python
class ElectricCar(Car):
    # ...省略其他代码...

    def fill_gas_tank(self):
        """Electric cars don't have gas tanks."""
        print("This car doesn't need a gas tank!")
```

> [!tip] 继承的本质
> 继承允许我们从父类取其精华去其糟粕,只保留和修改需要的部分。

### 组合

#### 概念
**组合(Composition)**: 将大型类拆分成若干个协同工作的小类。

#### 示例:电动汽车的电池
```python
class Battery:
    """A simple attempt to model a battery for an electric car."""

    def __init__(self, battery_size=75):
        """Initialize the battery's attributes."""
        self.battery_size = battery_size

    def describe_battery(self):
        """Print a statement describing the battery size."""
        print(f"This car has a {self.battery_size}-kWh battery.")

    def get_range(self):
        """Print a statement about the range this battery provides."""
        if self.battery_size == 75:
            range_miles = 260
        elif self.battery_size == 100:
            range_miles = 315

        print(f"This car can go about {range_miles} miles on a full charge.")

class ElectricCar(Car):
    """Models aspects of a car, specific to electric vehicles."""

    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()  # 组合:创建Battery实例作为属性

my_tesla = ElectricCar('tesla', 'model s', 2019)
my_tesla.battery.describe_battery()  # 调用Battery类的方法
my_tesla.battery.get_range()
```

#### 执行流程
以`my_tesla.battery.describe_battery()`为例:
1. 定位到`ElectricCar`实例`my_tesla`
2. 访问其`battery`属性,这是一个`Battery`实例
3. 调用`Battery`实例的`describe_battery()`方法

### 类的导入

#### 导入单个类
```python
# car.py
class Car:
    # ...类定义...

# my_car.py
from car import Car

my_car = Car('audi', 'a4', 2019)
```

#### 从一个模块导入多个类
```python
from car import Car, ElectricCar

my_beetle = Car('volkswagen', 'beetle', 2019)
my_tesla = ElectricCar('tesla', 'roadster', 2019)
```

#### 导入整个模块
```python
import car

my_beetle = car.Car('volkswagen', 'beetle', 2019)
my_tesla = car.ElectricCar('tesla', 'roadster', 2019)
```

> [!tip] 推荐做法
> 导入整个模块的好处是代码更清晰,能明确看出使用的类来自哪个模块。

#### 导入模块中的所有类
```python
from car import *
```

> [!danger] 不推荐
> 不推荐使用这种方式,容易引起名称冲突。

#### 使用别名
```python
# 给类指定别名
from electric_car import ElectricCar as EC

my_tesla = EC('tesla', 'roadster', 2019)

# 给模块指定别名
import electric_car as ec

my_tesla = ec.ElectricCar('tesla', 'roadster', 2019)
```

### 实际使用示例

```python
import os

class Board:
    def __init__(self):
        self.board_name = os.getenv('WLOP_CHIP_TYPE')

    def num(self):
        # 方法实现
        pass

if __name__ == "__main__":
    board = Board()  # 创建Board类的实例
    board.num()      # 调用实例的num方法
```

**说明:**
- `object`是Python 3中所有类的基类(可以省略)
- `os.getenv()`用于获取系统环境变量的值
- `self.board_name`是类实例的属性
- `if __name__ == "__main__":`确保代码只在直接运行时执行

---
## 🤔 Q&A

### Q1: 什么时候使用继承,什么时候使用组合?
**A**:
- **继承**: "is-a"关系,如ElectricCar是Car的一种
- **组合**: "has-a"关系,如Car有一个Engine
- 一般建议优先考虑组合,因为它提供更灵活的设计

### Q2: self到底是什么?
**A**: `self`是对实例本身的引用,它让实例可以访问类中的属性和方法。当调用`my_dog.sit()`时,Python会自动将`my_dog`作为`self`参数传递给`sit()`方法。

### Q3: 类属性和实例属性有什么区别?
**A**:
- **类属性**: 定义在`__init__()`之外,所有实例共享
- **实例属性**: 定义在`__init__()`中,每个实例独立拥有

```python
class Dog:
    species = 'Canis familiaris'  # 类属性

    def __init__(self, name):
        self.name = name  # 实例属性
```

### Q4: 为什么使用super()?
**A**: `super()`用于调用父类的方法,特别是在多重继承时能正确处理方法解析顺序(MRO)。它比直接调用父类名更灵活,更易于维护。

## 🚀 Tasks
- [ ] 设计一个类来表示现实世界的对象(如书籍、用户账户等)
- [ ] 使用继承创建一个类的层次结构
- [ ] 练习使用组合将复杂类拆分成多个小类
- [ ] 将类组织到模块中,练习导入和使用

## 📚 Reference
* Python Crash Course (Python编程:从入门到实践)
* Python官方文档 - Classes
* Effective Python: 90 Specific Ways to Write Better Python

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的进阶部分
* [[Python基础 - 函数]]是理解方法的基础
* [[Python高级 - 异常处理]]可以让类的方法更加健壮
