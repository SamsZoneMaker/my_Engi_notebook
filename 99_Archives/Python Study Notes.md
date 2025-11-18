author: Sam [desen.li@wisewavetech.com]

---

## 数据类型

### 字符串

**用法**：用引号引起的都是字符串，此处引号不限于双引号“或单引号‘

#### **方法（method）**

method是Python对数据执行的操作。假设变量名为`name`，变量后的句点`.`会对变量 `name`执行方法的操作,如`name.title()`,title方法的作用是令每个单词的首字母大写. 方法要跟随一个括号()使用, ()是用来填充额外的信息的,即便没有/不需要额外的信息,也需要放置一个空括号。还有例如方法 

```Python
 print(name.upper())	#全大写
 print(name.lower())	#全小写
 name.rstrip()	#去除字符右端空白
 name.lstrip()	#去除字符左端空白
 name.strip()	#去除字符两段空白
 name.removeprefix(xxx)		#去除变量中的xxx前缀
```

#### **合并字符串**

通过`f(format)`字符串将需要串起的字符合并，当需要合并的字符是以变量的形式则需要使用大括号。

```python
 full_name = f"{first_name} {last_name}"
```

#### 符号

`\n` 换行符

`\t` 制表符

`%`求模运算符（求余）

`+=`值+1 或 在末尾追加字符

#### 追加字符串

运算符 `+=`  在赋给变量 prompt  的字符串末 尾追加⼀个字符串

```python
prompt = "If you share your name, we can personalize the messages you 
see." 
prompt += "\nWhat is your first name? " 

name = input(prompt) 
```



### 数

#### 浮点数

* 将任意两个数相除，结果总是浮点数，即便这两个数都是整数且能整除
* 在其他任何运算中，如果⼀个操作数是整数，另⼀个操作数是浮点数，结 果也总是浮点数
* 在 Python 中，⽆论是哪种运算，只要有操作数是浮点数，默认得到的就总 是浮点数，即便结果原本为整数

#### 赋值

* 用 `=`赋值，正常情况下建议一行进行一次赋值

* **同时赋值情况**：将一系列数赋给一组变量，可以采用如下的赋值方式：

  ```python
   x, y, z = 0, 0, 0
  ```

  需要用逗号将变量名分开；对于要赋给变量的值，也需要做 同样的处理。Python 将按顺序将每个值赋给对应的变量。只要变量数和值 的个数相同，Python 就能正确地将变量和值关联起来。

* 通常情况下，会使用全大写字母的命名方式定义一个变量为常量，该常量的值应始终不变

#### 常量

在程序的整个周期中，如果一个变量的值是保持一直不变的，Python没有内置的“常量”类型，但是可以用`全大写字母`的方式命名，该参数将被视作“常量”。

#### None

None表示变量没有值，可以视作一个占位值



## 列表 list

**列表（list）**由⼀系列按特定顺序排列的元素组成。你不仅可以创建包含字 ⺟表中所有字⺟、数字 0〜9 或所有家庭成员姓名的列表，还可以将任何东 ⻄加⼊列表，其中的元素之间可以没有任何关系。列表通常包含多个元 素，因此给列表指定⼀个表⽰复数的名称（如 letters、digits 或 names）是较为常见的。

在 Python 中，⽤⽅括号（[]）表⽰列表，⽤逗号分隔其中的元素。下⾯是⼀个简单的⽰例，其中包含⼏种⾃⾏⻋：

```py
bicycles = ['trek', 'cannondale', 'redline', 'specialized']
```



### 索引

* 要访问列表元素，可指出列表的名称，再指出元素的索引，并将后者放在方括号内。
* 索引从0开始，而不是从1，与C语言的数组一致
* Python 为访问最后⼀个列表元素提供了⼀种特殊语法。通过将索引指定为 -1，可让 Python 返回最后⼀个列表元素，并以此类推，-2 -3 则表示倒数第二个和第三个列表元素



### 元素修改

#### 修改

`列表名+[x] = xxx` 即可修改单个元素

#### 添加

1. 末尾添加 (append)

   `列表名.append('xxx')`即可在列表的末尾直接添加元素xxx

2. 列表中添加 (insert)

   `列表名.insert(a，'xxx')` 表示在索引位置a处添加元素xxx

3. 添加另一列表至一列表的末尾

   `.extend()` 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）

#### 删除

1. 使用`del`

   `del xxx[a]`删除xxx列表中的第a+1个元素

2. 使用pop()方法

   ```python
   motorcycles = ['honda', 'yamaha', 'suzuki']
   print(motorcycles)
   popped_motorcycle = motorcycles.pop()
   ```

3. 删除任意位置的元素

   利用`pop(num)`可以弹出第num+1位置处的元素

   ```
   如果不确定该使⽤ del 语句还是 pop() ⽅法，下⾯是⼀个简单的判断标准：
   如果要从列表中删除⼀个元素，且不再以任何⽅式使⽤它，就使⽤ del 语句；如果要在删除元素后继续使⽤它，就使⽤ pop() ⽅法。
   ```

4. 删除特定的“值”

   ```python
   motorcycles = ['honda', 'yamaha', 'suzuki', 'ducati']
   print(motorcycles)
   motorcycles.remove('ducati')
   ```

   列表名后加方法`remove`即可删除指定值，但是一次只会删除列表中第一次出现的值，如果需要删除多个，可以用循环



### 管理列表

列表中元素的添加可能是无序的，但是有时希望其输出可以是有序的，则需要用到一些管理的方法

#### sort()

`sort`可以按照首字母的顺序将list中的元素排序，如果需要方向排序，则可以使用

```python
cars = ['bmw', 'audi', 'toyota', 'subaru']
cars.sort(reverse=True)
```

#### sorted()

sort()对列表的修改是永久的，如果只是需要暂时的排序，可以使用`sorted()`，使用方法与`sort`一致

#### .reverse()

该方法用来调转列表的排序，与首字母排序无关

该调转是永久的，恢复再用一次`reverse`即可

#### len(xxx)

该函数用来确定列表的长度（元素个数）



### 数值列表

在python中，字符串列表和数字列表是分开定义的，Python中有不少工具用于处理存放数值的列表

#### range()

该函数可用于生成一系列的数

```python
for value in range(1, 5):
    print(value)
    
#输出结果
1
2
3
4
```

上述代码中会生成一个临时变量名为`value`的数值（非列表），该数值实际上生成从1开始 到5停止（不包含5）的结果，这是编程语言中常见的差一行为

* **指定步长**

  `list(range(2, 11, 2))`可以指定为从2开始到11结束每隔2生成一个数，从而得到一个1~10的偶数集合

* **代码优化示例 （列表推导式）**

  **列表推导式**是将for循环和创建新元素的代码合并一起的方式，需要注意的是列表推导式中的for循环末尾不需要冒号`:`

  ```python
  # 该代码功能是得到一个1~10的平方结果列表 （** 表示乘方运算）
  # 源代码
  squares = []
  for value in range(1, 11):
      square = value ** 2
      squares.append(square)
  print(squares)
  
  # 以上代码可以简化为
  squares = []
  for value in range(1,11):
      squares.append(value**2)
  
  print(squares)
  
  # 以上代码仍可继续简化为
  squares = [value**2 for value in range(1, 11)]
  print(squares)
  
  # 优化后的代码提高运行效率同时提升了可读性
  ```

* **统计计算**

  类似于Excel，可以用`min`、`max`、`sum`等函数求出列表的最值，总值



#### 如何创建数值列表？

在`list()`函数中嵌套`range()`函数

```python
numbers = list(range(1, 6))
print(numbers)

# Output
[1, 2, 3, 4, 5]
```



### 使用列表

#### 切片

要处理列表中的元素是，会使用到**切片(Slice)**，例如指定打印列表中的某几个元素：

```python
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(players[0:3]\n)
print(players[1:4]\n)
print(players[:4]\n)
print(players[2:]\n)
print(players[-3:]\n)
print(players[:]\n) 



# 输出结果
['charles', 'martina', 'michael']
['martina', 'michael', 'florence']
['charles', 'martina', 'michael', 'florence']
['michael', 'florence', 'eli']
['michael', 'florence', 'eli']
['charles', 'martina', 'michael', 'florence', 'eli']
```

#### 复制列表

步骤

* 创建新列表
* 遍历已有列表写入新列表

```python
my_foods = ['pizza', 'falafel', 'carrot cake']
riend_foods = my_foods[:]

# 这是⾏不通的：friend_foods = my_foods
# 当更改my_foods的时候，friend_foods也会同时更改，相当于生成了一个
```



### 元祖（tuple）

元祖是一种很像列表的特殊形式，元祖里面的值是不可以被修改的，与列表做如下区分：`元祖用()定义，列表用[]定义`


#### 元祖编辑

元祖虽然不能更改其中的某个值，但是可以整个元祖重新赋值，例如
初始：`dimensions = (200, 50)`
重新赋值：`dimensions = (400, 100)`

#### **<font color=red>注意</font>**

* 元祖是由`,`标识的  即使只有一个元素，也要在末尾加上`,`
* 元祖不能被更改，尝试更改会被python报错






## 循环

### for循环

#### 命名

在for循环中，建议使用有意义的临时变量有助于理解代码，例如

```python
for cat in cats:
for dog in dogs:
for item in list_of_items:
#这里的cats、dogs......可以是任何可以被迭代的对象，如列表（List）、元组（Tuple）、字符串（String）、字典（Dictionary）、集合（Set）、range（用于生成数字序列）
```

* 在Python中，for循环不会使用大括号{}，以同一缩进作为for循环内的内容，所以在Python中要极度注意缩进的使用，不建议随意的缩进，且缩进建议使用四个空格而非`tab`键



### if循环

if循环的底层逻辑是条件测试，根据测试结果的**True**和**False**来判断代码的执行方式

* 因为python是大小写敏感的语言，所以判断的时候需要区分大小写；如果判断时不看重或无法判断字符内的大小写情况，可以将所以变量变为全小写，在进行逻辑判断

#### 特殊用法

* 使用`and`和`or`表示与和或的情况
* 检查列表中是否存在某个值用 `if abc in xyz`，检查不存在用 `if abd not in xyz`
* 可以省略`else`
* 确定列表非空的情况  直接使用 `if + 列表名:`



### while循环

* 使用`break`退出循环，break可以退出任何Python中的循环，用法直接使用`break`即可
* 用`continue`表示继续循环的运行





## 字典

Brief：用来存放对应信息的**键值对**，键值对分别是key和value



### 字典示例

```python
alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])
print(alien_0['points'])

# Output
'green'
'5'
```



### 字典的用法

#### 基础语法

```python
alien_0 = {}    # 创建一个空字典
alien_0 = {'color': 'green', 'points': 5}

point_s = alien_0['points']     # 获取某个键值对的方法
alien_0['x_position'] = 25    # 增加键值对的方法
alien_0['color'] = 'yellow'    # 修改字典值
del alien_0['points']    # 删除某个键值对 （永久删除）
```

#### 遍历方法

1. 遍历键值对、键、值
   ```python
   # dict定义
   user_0 = {
    'username': 'efermi',
    'first': 'enrico',
    'last': 'fermi',
    }
   
   # 遍历键值对
   for key, value in user_0.items():
       print(f"\nKey: {key}")
       print(f"Value: {value}")
       
   # 遍历 键
   for k in user_0.keys():
       print(k.title())
   
   # 遍历 值
   for v in user_0.values():
       print(v.upper())
   ```

当遍历的结果有多的重复值，可以用`set()`提取有的元素，用法：`for v in set(user_0.values()):`



### get()的用法

get() 主要用于字典(dict)和一些其他数据结构中，使用场景：

* 当你不确定键是否存在时，优先使用 get() 方法
* 需要提供默认值时，明确指定第二个参数
* 在处理可能存在的空值或缺失值时，get() 特别有用

#### **基本语法**

```python
# 基本语法
dict.get(key, default=None)

# 示例
my_dict = {'name': 'Tom', 'age': 25}

# 获取存在的键的值
print(my_dict.get('name'))  # 输出: Tom

# 获取不存在的键,返回默认值 None
print(my_dict.get('height'))  # 输出: None

# 指定默认值
print(my_dict.get('height', 180))  # 输出: 180

# ---------------------------------------------------------------------------------- #
# 在条件判断中的应用
settings = {'debug': True}

# 检查配置项,使用默认值
is_debug = settings.get('debug', False)    # Output:True
log_level = settings.get('log_level', 'INFO')    # Output:INFO (不存在该值时输出默认值)

# ---------------------------------------------------------------------------------- #
# 处理集合类型
from collections import Counter

# 统计词频
words = ['apple', 'banana', 'apple', 'orange']
word_count = Counter(words)

# 安全获取词频
apple_count = word_count.get('apple', 0)  # Output:2
kiwi_count = word_count.get('kiwi', 0)    # OUtput:0
```



### 字典嵌套用法

1. 与列表的嵌套

   ```python
   alien_0 = {'color': 'green', 'points': 5}
   alien_1 = {'color': 'yellow', 'points': 10}
   alien_2 = {'color': 'red', 'points': 15}
   aliens = [alien_0, alien_1, alien_2]
   
   for alien in aliens:
       print(alien)
   
   # Output：
   {'color': 'green', 'points': 5}
   {'color': 'yellow', 'points': 10}
   {'color': 'red', 'points': 15}
   ```

2. 在字典中存储列表

   针对的情况是键值对中的值不止有一个的情况，例如：

   ```python
   pizza = { 
       'crust': 'thick', 
       'toppings': ['mushrooms', 'extra cheese'], 
       } 
   
   # 概述顾客点的⽐萨
    
   print(f"You ordered a {pizza['crust']}-crust pizza " 
       "with the following toppings:")     # 这里是print里面的内容在编码时需要换行的写法
   for topping in pizza['toppings']: 
       print(f"\t{topping}")
   ```

   因为有超过一个值，这种时候就会依次输出，因此也可以直接用for循环遍历得到

3. 字典中嵌套字典

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



### 使用while循环处理dict

通过将 while  循环与列表和字典结合起来使⽤，可收 集、存储并组织⼤量的输⼊，供以后查看和使⽤。

`while abcd:`用于判断abcd内是否不为空





## 函数Function

函数是带名字的代码块， ⽤于完成具体的⼯作。要执⾏函数定义的特定任务，可调⽤（call）该函数。



### 示例

```python
# 函数定义
def greet(name):
    print(f"Hello, {name}!")

# 函数调用
greet("Alice")  # 调用函数，输出: Hello, Alice!    
```



### 参数

在示例代码中，`name`是一个形参，而`'Alice'`作为传递过去的实参。

同时在函数定义中，也可以使用设定**默认值**的方式，当有实参传到函数，使用实参；如无，则使用默认值

#### 位置实参

指函数定义了多少个形参，调用函数时就传送多少个实参过去

#### 关键词实参

```python
def describe_pet(animal_type, pet_name):
    """显⽰宠物的信息"""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}.")

# 函数调用，两行代码作用是等效的
describe_pet(animal_type='hamster', pet_name='harry')
describe_pet(pet_name='harry',animal_type='hamster')
```

#### 传递多个参数的情况

有时并不清楚函数需要多少个参数，又或者函数可以接受不止一个参数的情况

```python
def make_pizza(*toppings):
    """概述要制作的⽐萨"""
    print("\nMaking a pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')
```

* 在上代码中，`*toppings `是创建了一个元祖，该元祖可以接受所有函数收到的值，但即使只有一个值，这个值也依然会存放在元祖当中
* Python中常见 `*args`表示接受任意数量的位置实参
* Python中常见 `**kwargs`表示接受任意数量的关键字实参

#### 传递多个关键字的情况

```python
def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
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
```

在此代码中，`**user_info `用于创建一个名为 `user_info` 字典，存放所有收到的键值对

**在编写函数时，可以⽤各种⽅式混合使⽤位置实参、关键字实参和任意数 量的实参。**



### 返回值

在函数的末尾使用 `return`设定返回给函数调用处的结果值

#### 返回字典

除了返回某项值之外，`return`也可以返回包括列表、字典等在内的复杂结构





### 传递列表

代码优化的示例：

```python
# 源代码
# ⾸先创建⼀个列表，其中包含⼀些要打印的设计
unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []
# 模拟打印每个设计，直到没有未打印的设计为⽌
# 打印每个设计后，都将其移到列表 completed_models 中
while unprinted_designs:
    current_design = unprinted_designs.pop()
    print(f"Printing model: {current_design}")
    completed_models.append(current_design)
# 显⽰打印好的所有模型
print("\nThe following models have been printed:")
for completed_model in completed_models:
    print(completed_model)
    
# -------------------------------------------------------------------------------- #
# 使用函数优化
def print_models(unprinted_designs, completed_models):
    """
    模拟打印每个设计，直到没有未打印的设计为⽌
    打印每个设计后，都将其移到列表 completed_models 中
    """
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        print(f"Printing model: {current_design}")
        completed_models.append(current_design)
def show_completed_models(completed_models):
    """显⽰打印好的所有模型"""
    print("\nThe following models have been printed:")
    for completed_model in completed_models:
        print(completed_model)
 
unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

print_models(unprinted_designs, completed_models)
show_completed_models(completed_models)
```

**传递列表副本的方法**

当只想传递列表但不修改列表的时候，可以将列表的副本传送给函数，方式是调用函数时传递一个列表的副本，如`function_name(list_name[:])`这里的[:]即切片表示法创建了副本



### 函数模块化(import)

将函数存储在称为模块的独⽴⽂件中，再将模块导⼊（**import**）主程序。**import** 语句可让你在 当前运⾏的程序⽂件中使⽤模块中的代码，通过将函数存储在独⽴的⽂件中，可隐藏程序代码的细节，将重点放在程 序的⾼层逻辑上

* **模块**：

  模块是扩展名为 .py 的⽂件，包含要导⼊程序的代码

#### 示例代码

```python
# pizza.py
def make_pizza(size, *toppings):
    """概述要制作的⽐萨"""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")
        
# main.py
import pizza
pizza.make_pizza(16, 'pepperoni')
pizza.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
```

#### 几种模块导入的方法：

1. 导入整个模块

   * 示例代码中采用的就是全模块导入，这种方式可以取用`pizza.py`中的所有函数
   * 导入方法：`import module_name`
   * 调用函数时，指定模块的名称和模块内需要被调用的函数，两者之间用句点 `.` 隔开，示例 `module_name.function_name()` 
2. 导入模块中的特定函数
   * 不导入完整的库，导入库内的某个函数，以示例代码为例，可以改成 `from pizza import make_pizza`
   * 标准的格式为 `from module_name import function_0, function_1, function_2` 
   * 采用这种方法就不需要使用句点 `.` 了
3. 使用**as**给**函数**指定别名
   * 针对要导⼊的函数的名称太⻓或者可能与程序中既有的名称冲突，类似于外号的存在
   * 导入方法：`from module_name import function_name as fn`
4. 使用**as**给**模块**指定别名
   * 除了给函数起别名，也可以直接给库起别名，这是非常常用的
   * 方法：`import module_name as mn` ，调用时 `mn.function()`
5. 导入模块中的所有函数
   * 该功能主要结合1和2的功能，由于导入了所有
   * 方法：`from module_name import *` ；调用时因为已经导入了整个模块，所以不需要句点了（参照2.）
   * **<font color=red>注意</font>**：不建议采用此方法，容易导致代码名称上的冲突，建议还是分别导入函数



### Guide Line

> [!CAUTION]
>
> 1. 在给形参指定默认值时，等号两边不要有空格；函数调用中的关键字实参也应遵循这种约定
> 2. 如果程序或模块包含多个函数，可使用两个空行将相邻的函数分开。这样将更容易知道前⼀个函数到什么地方结束，下⼀个函数从什么地方开始
> 3. 所有import语句都应该放在文件开头

 



## 类

面向对象编程 （object-oriented programming, OOP），在⾯向对象编程中，你编写表⽰现实世界中的事物和情 景的**类（class）**，并基于这些类来创建**对象（object）**。

在编写类的时候，要定义一批具有**通用行为**的对象，达到的目的是用更少的代码做更多的事情

### 示例

```python
class Dog():
    """A simple attempt to model a dog."""
    
    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name
        self.age = age
        
    def sit(self):
        """Simulate a dog sitting in response to a command."""
        print(self.name.title() + " is now sitting.")

    def roll_over(self):
        """Simulate rolling over in response to a command."""
        print(self.name.title() + " rolled over!")
```

这是一个类的定义范例

* 在定义中，首字母大写的是类，因此这里class后面的 `Dog` 的D是大写，也因此不需要加括号
* `Dog` 类中还定义了两个方法（类中的函数统称**方法**）



### \__init__()  方法

类中的函数统称为方法，也称为构造函数。参考示例代码，有以下需要注意的点

* \__init__()  方法的定义中包含三个形参 ` self、name、age`，其中 `self` 是必不可少的，且需放在第一位。因为在创建 `Dog` 的实例的时候，会自动传入实参给 `self` ，是一个接受参数属于实例本身，让实例可以访问类中的属性和方法，通过实参传送的参数会直接交给 `name` 和 `age` ；
* 可以看到在类中定义了两个前缀带有self的变量，这种变量可以为类中所有的方法使用，像这种通过实例访问的变量称之为 **属性**。



### 根据类创建实例

1. 创建

   根据示例中所创建的 class 创建一个小狗实例 `my_dog = Dog('doudou', 3)` ，此时该实例已经赋给了变量 `my_dog` ；在创建中，`Dog` 是类所以首字母大写，my_dog则是创建的实例，可理解为此时其中一个self = my_dog

2. 访问

   由于类中已经定义好了属性 `self.name` ，访问时使用 `my_god.name` 即可得到 ’doudou‘ 的结果

3. 调用

   调用时，仍需指定实例名和想调用的方法（类中的函数），例如 `my_god.roll_over`

4. 创建多个实例

   除了my_dog之外还会有很多小狗，小狗都可以通用的使用该类进行再定义，要求实例名不一样即可



### 类和实例的使用

#### 修改属性的值

1. 直接修改

   通过实例访问属性，类中的参数并非都是实参传过去的，可以在类中定义变量（属性），假设 `Dog`中定义了一个weight的属性，可以在主代码中 `my_dog.weight = 10` 进行属性的直接修改

2. 通过方法修改

   在类中定义一个新的方法用于更新属性的

   ```python
   class Dog:
       -- snip --
           
       def update_weight(self, kg)
           self.newweight = kg
           
   # 代码侧
   my_dog.update_weight(10)
   ```

   这种方法的好处在于可以保留更新前的数据（如果更新数据后还需要用更新前的数据）

3. 通过方法让属性的值递增

   ```python
   class Dog:
       -- snip --
       def now_weight(self, weight)
           self.nowweight = weight
           
       def update_weight(self, kg)
           self.nowweight += kg
           
   # 代码侧
   my_dog.update_weight(10)
   ```



### 继承

* 在用到class时，并不都要从头开始写，如果一个类是既有类的特殊版本
* 当一个类继承另一个类时，将自动获取原有类的所有属性和方法，且子类可以自定义新的属性和方法



#### 子类 \__init__() 继承方式

1. **完全继承父类的所有属性：**

   ```python
   class Dog:
       -- snip --
       def now_weight(self, weight)
           self.nowweight = weight
           
       def update_weight(self, kg)
           self.nowweight += kg
           
   class Whitedog(Dog):
       
       def __init__(self, name, age):
           """初始化父类的属性"""
           super().__init__(name,age)
   ```

   * 在创建子类时，父类必须在当前文件中，且位于子类的上面，是以上代码所示，`class Whitedog` 继承了父类 `class Dog` ，因此在前面已经定义好父类
   * 在定义子类的时候，可以看到子类名后多了一个括号，里面是父类的名称，这在类的定义中是必须的
   * 子类中的 ` __init__` 方法接受创建 `Dog`父类中的信息
   * `super()` 是一个调用父类方法的函数，其使用不需要 `self` 形参

2. **在子类创建新属性**

   * 子类可以创建新的属性，调用的前提是实例写入的是子类，这样才可以使用子类中所定义的变量和方法
   * 如果一个属性是通用的，那应该写入父类中，而非子类
3. **重写父类方法**
   * 该方法针对的情况是：有时父类的方法不适用于子类，子类可以根据需求改写此方法，但同时不影响父类中同名方法的定义
   * 重写方法为 `def subclass_method(self)` 
   * 其意义在于，继承父类时，可以从父类取其精华去其糟粕

#### 组合

**组合：**将大型类拆分成若干个协同工作的小类

```python
# car.py
"""A class that can be used to represent a car."""

class Car():
    """A simple attempt to represent a car."""

    def __init__(self, manufacturer, model, year):
        """Initialize attributes to describe a car."""
        self.manufacturer = manufacturer
        self.model = model
        self.year = year
        self.odometer_reading = 0
        
    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = str(self.year) + ' ' + self.manufacturer + ' ' + self.model
        return long_name.title()
    
    def read_odometer(self):
        """Print a statement showing the car's mileage."""
        print("This car has " + str(self.odometer_reading) + " miles on it.")
        
    def update_odometer(self, mileage):
        """
        Set the odometer reading to the given value.
        Reject the change if it attempts to roll the odometer back.
        """
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")
    
    def increment_odometer(self, miles):
        """Add the given amount to the odometer reading."""
        self.odometer_reading += miles
```

```python
# electric_car.py
"""A set of classes that can be used to represent electric cars."""

from car import Car

class Battery():
    """A simple attempt to model a battery for an electric car."""

    def __init__(self, battery_size=60):
        """Initialize the batteery's attributes."""
        self.battery_size = battery_size

    def describe_battery(self):
        """Print a statement describing the battery size."""
        print("This car has a " + str(self.battery_size) + "-kWh battery.")  
        
    def get_range(self):
        """Print a statement about the range this battery provides."""
        if self.battery_size == 60:
            range = 140
        elif self.battery_size == 85:
            range = 185
            
        message = "This car can go approximately " + str(range)
        message += " miles on a full charge."
        print(message)
    
        
class ElectricCar(Car):
    """Models aspects of a car, specific to electric vehicles."""

    def __init__(self, manufacturer, model, year):
        """
        Initialize attributes of the parent class.
        Then initialize attributes specific to an electric car.
        """
        super().__init__(manufacturer, model, year)
        self.battery = Battery()
```

```python
# my_cars.py
from car import Car
from electric_car import ElectricCar

my_beetle = Car('volkswagen', 'beetle', 2015)
print(my_beetle.get_descriptive_name())

my_tesla = ElectricCar('tesla', 'roadster', 2015)
print(my_tesla.get_descriptive_name())
```

以上3个block是一套代码，简述代码执行流程：

**以`my_tesla.get_descriptive_name()` 为例**

1. 由于创建的 `my_tesla` 是 `ElectricCar` 的对象， `ElectricCar` 作为子类继承了父类 `Car` 的所有属性，所用到的 `get_descriptive_name()` 方法并不存在于子类中，因此找到父类
2. 定位到父类的 `get_descriptive_name` 方法后，执行其代码创建新变量并返回，最终在 `my_cars.py` 中执行打印操作

**以`my_tesla.battery.describe_battery()` 为例**

1. 先定位到 `ElectricCar` 类，定位 `battery` 方法，该方法执行的代码为 `Battery()`
2. `Battery()` 属于另一个类（非被继承的父类），定位到这个类之后，可以看到其输入的形参已设定有默认值
3. 在 `Battery()` 类中找到 `describe_battery()` 的方法，执行方法内代码，打印结果



### 类的导入

* 善用多个模块，主代码中负责将模块导入 (import)
* 有时一个模块中存在不止一个类，导入时可以同时将其都导入，不同类之间用 `,` 隔开，例如 `from car import Car, ElectricCar` ；这样导入的好处在于可以直接使用类；也可以使用 `from car import *` 的方式一次导入所有类，但不推荐
* 除了导入模块中的某个类，也可以导入整个模块，使用时 `module_name.Class()` 即可，这种方式的好处在于可以不需要编写过于复杂的 import代码
* 模块中还可以导入另一个类，主要是父类子类继承的情况
* 与 `import` 的属性类似，可以指定导入类的别名使用







# 高级用法篇



## `try`用法

`try` 常用于异常处理的关键字，允许捕获和处理代码执行过程中的错误，作用在于遇到错误时程序不会崩溃，给了一个跳过崩溃的选择。try语句的基本结构如下：

```python
try:
    # 可能引发异常的代码
    pass
except SomeException as e:
    # 捕获到特定异常后的处理代码
    pass
else:
    # 如果没有异常发生，执行这部分代码
    pass
finally:
    # 不管有没有异常，都会执行的代码
    pass

```

### 详细说明：

1. **`try`**: 用于放置可能会引发异常的代码块。如果代码块中没有异常，`except`部分将不会执行。
2. **`except`**: 用于捕获指定类型的异常，并执行相应的处理逻辑。如果`try`块中的代码发生了异常，程序会跳转到对应的`except`块。
3. **`else`**: 可选部分。如果没有捕获到异常，`else`块中的代码会被执行。
4. **`finally`**: 可选部分，不管是否发生异常，`finally`中的代码都会执行。通常用于清理资源等操作，如关闭文件或数据库连接。



### 预设异常类型

Python中存在一些预设的异常类型，可以用在try的语句中，例如：

**`as e`**：将捕获的异常对象赋值给变量`e`，以便在`except`块中使用它。例如，可以查看异常信息或执行一些特定的处理。

`ZeroDivisionError` 是内置异常之一，专门用于表示除数为零的错误。

`AttributeError`：通常发生在你尝试访问对象没有的属性时。

`ValueError`：表示传递给函数的参数值不符合要求。

`IndexError`：表示索引超出范围。

`TypeError`：通常发生在操作或函数应用于错误类型的对象时（比如对一个整数执行字符串的操作）。

`FileNotFoundError`：表示文件未找到。

`KeyError`：表示字典中查找的键不存在。



## `time` 模块

time是python中的一个标准模块，用这个标准模块，可以得到一下获取时间的用法，例如`time.strftime("%Y%m%d")` 会获取到执行代码时的时间，and可以自定义日期的格式



## “类” 的实际使用

```python
class board(object):
    def __init__(self):
        self.board_name = os.getenv('WLOP_CHIP_TYPE')  # 这里是初始化方法的代码
    
    def num(self):
        xxxx  # 这里是num方法的代码

if __name__ == "__main__":
    board = board()  # 创建board类的实例
    board.num()  # 调用实例的num方法
```

代码中，`object` 是python3中所有类的基类，其他内容可以查看注释和chapter1 中的内容。

`os.getenv()` 是Python的`os`模块中的一个函数，用于获取系统环境变量的值

`'WLOP_CHIP_TYPE'` 是要获取的环境变量的名称，这可能是一个用于标识芯片类型或电路板类型的变量

`self.board_name` 是类实例的一个属性，用于存储环境变量的值

这句代码的目的是将系统环境中设置的`WLOP_CHIP_TYPE`环境变量的值读取出来，并赋值给当前对象的`board_name`属性。





## `getattr` 的用法

- Python内置的`getattr` 函数用于获取模块属性的语法

- 例如`params = getattr(testImport, 'params', [None])` 用于从testImport模块中获取名为 `params` 的属性，如果属性存在，则赋给params，不存在则赋None

- getattr函数是Python的反射机制的一部分，它允许你通过字符串名称动态地访问对象的属性。这种写法在以下情况下特别有用：
  - 处理可能缺少某些属性的模块
  - 编写能够适应不同模块结构的通用代码
  - 测试框架中，检查测试模块是否定义了特定的测试参数





# 双（多）线程

多线程类似于同时执行多个不同的程序，多线程的优点有：

- 把占用时间长的程序放在后台运行
- 程序整体的运行速度可以加快
- 在一些需要等待用户输入的、文件读写等等，线程可以释放一些珍贵的资源（内存占用等）



线程在执行过程中与进程还是有区别的。每个独立的进程有一个程序运行的入口、顺序执行序列和程序的出口。但是线程不能够独立执行，必须依存在应用程序中，由应用程序提供多个线程执行控制。



### **方法**

Python中使用线程有两种方式：函数或者用类来包装线程对象。

函数式：调用thread模块中的start_new_thread()函数来产生新线程。`thread.start_new_thread ( function, args[, kwargs] )`



### Threading 库

Python通过两个标准库thread和threading提供对线程的支持。`thread`提供了低级别的、原始的线程以及一个简单的锁。`threading` 模块建立在 `_thread` 模块之上，提供了更高级、更易用的线程管理接口。

threading 模块提供的其他方法：

```python
threading.currentThread() # 返回当前的线程变量。
threading.enumerate()  # 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
threading.activeCount()  #  返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。

# 除了使用方法外，线程模块同样提供了Thread类来处理线程，Thread类提供了以下方法:

run()  #  用以表示线程活动的方法。
start()  #  启动线程活动。
join([time])  #  等待至线程中止。这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
isAlive()  #  返回线程是否活动的。
getName()  #  返回线程名。
setName()  #  设置线程名。
```

使用Threading模块创建线程，直接从`threading.Thread`继承，然后重写__init__方法和run方法，示例：

```python
#!/usr/bin/python
 
import threading
import time
 
exitFlag = 0
 
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name
 
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
 
# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
 
# 开启线程
thread1.start()
thread2.start()
 
print "Exiting Main Thread"
```



#### 创建线程基本步骤：

1. **通过函数创建**
   1. **导入 `threading` 模块。**
   2. **定义一个函数作为线程的执行体。**
   3. **创建 `threading.Thread` 对象，** 将定义的函数作为 `target` 参数，函数的参数通过 `args` (元组) 或 `kwargs` (字典) 传递。
   4. **调用线程对象的 `start()` 方法启动线程。**
   5. **(可选但常用) 调用线程对象的 `join()` 方法等待线程执行完毕。**

2. **通过继承 `threading.Thread` 类创建**
   1. **导入 `threading` 模块。**
   2. **定义一个新的类，继承自 `threading.Thread`。**
   3. **重写父类的 `__init__()` 方法** (如果需要传递额外参数或进行初始化)。**务必调用 `super().__init__()`。**
   4. **重写父类的 `run()` 方法，** 将线程要执行的代码放在 `run()` 方法中。
   5. **创建该子类的实例。**
   6. **调用实例的 `start()` 方法启动线程。** `start()` 方法会自动调用 `run()` 方法。
   7. **(可选但常用) 调用实例的 `join()`好的，在 Python 中实现多线程（双线程是多线程的一种特殊情况，即只有两个线程）







### 线程同步

如果多个线程共同对某个数据进行修改，可能会产生不可预料的结果，因此多个线程之间需要进行同步。

实现同步的方法是上锁，使用`Thread`对象的 `Lock`和 `Rlock` 可以实现简单的线程同步，这两个对象都有acquire方法和release方法，对于那些需要每次只允许一个线程操作的数据，可以将其操作放到acquire和release方法之间。

多线程的优势在于可以同时运行多个任务（至少感觉起来是这样）。但是当线程需要共享数据时，可能存在数据不同步的问题。

考虑这样一种情况：一个列表里所有元素都是0，线程"set"从后向前把所有元素改成1，而线程"print"负责从前往后读取列表并打印。那么，可能线程"set"开始改的时候，线程"print"便来打印列表了，输出就成了一半0一半1，这就是数据的不同步。为了避免这种情况，引入了锁的概念。

锁有两种状态——锁定和未锁定。每当一个线程比如"set"要访问共享数据时，必须先获得锁定；如果已经有别的线程比如"print"获得锁定了，那么就让线程"set"暂停，也就是同步阻塞；等到线程"print"访问完毕，释放锁以后，再让线程"set"继续。经过这样的处理，打印列表时要么全部输出0，要么全部输出1，不会再出现一半0一半1的尴尬场面。

示例：

```python
#!/usr/bin/python

import threading
import time
 
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release()
 
def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
 
threadLock = threading.Lock()
threads = []
 
# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
 
# 开启新线程
thread1.start()
thread2.start()
 
# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)
 
# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"
```



### 线程优先级Queue

除了线程之间的同步，线程之间也可以实现队列，包括 FIFO sequence、LIFO sequence、Priority Queue etc.

这些队列都实现了锁原语，能够在多线程中直接使用。也可以使用队列来实现线程间的同步。

Queue模块中的常用方法:

- `Queue.qsize()` 返回队列的大小
- `Queue.empty()` 如果队列为空，返回True,反之False
- `Queue.full()` 如果队列满了，返回True,反之False
- Queue.full 与 maxsize 大小对应
- `Queue.get([block[, timeout]])` 获取队列，timeout等待时间
- `Queue.get_nowait()` 相当Queue.get(False)
- `Queue.put(item, block=True, timeout=None)` 写入队列，timeout等待时间
- `Queue.put_nowait(item)` 相当 Queue.put(item, False)
- `Queue.task_done()` 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
- `Queue.join()` 实际上意味着等到队列为空，再执行别的操作



```python
#!/usr/bin/python
 
import Queue
import threading
import time
 
exitFlag = 0
 
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name
 
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)
 
threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1
 
# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1
 
# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()
 
# 等待队列清空
while not workQueue.empty():
    pass
 
# 通知线程是时候退出
exitFlag = 1
 
# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"
```

