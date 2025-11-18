---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/basic"
  - "#lang/shell"
status: 完善中
complexity: 基础
notetype: 学习笔记
resource: Shell教程 - 菜鸟教程
related:
  - "[[00_Shell_MOC]]"
  - "[[00_Linux_MOC]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Shell脚本编程基础

> [!abstract] 摘要
> 本笔记介绍Shell脚本编程的基础知识,包括变量、数组、运算符、控制流程和常用命令的使用方法。

## 🎯 Target
- [ ] 理解Shell的基本概念和常见类型
- [ ] 掌握Shell脚本的执行方式
- [ ] 熟练使用变量和数组
- [ ] 掌握Shell的运算符和控制流程
- [ ] 学会使用常用的Shell命令

## 📝 Core

### Shell基础概念

#### Shell的种类
Linux的Shell种类众多,常见的有:
- **Bourne Shell** (`/usr/bin/sh`或`/bin/sh`)
- **Bourne Again Shell** (`/bin/bash`) - 最常用
- **C Shell** (`/usr/bin/csh`)
- **K Shell** (`/usr/bin/ksh`)

> [!tip] 实际使用
> 在项目开发中,主要使用Bash。一般情况下,人们并不区分Bourne Shell和Bourne Again Shell,所以`#!/bin/sh`可以改为`#!/bin/bash`。

**Shebang说明:**
```bash
#!/bin/bash
# 其中#!告诉系统其后路径所指定的程序即是解释此脚本文件的Shell程序
```

#### Shell脚本的执行方式

**主要有四种执行方式:**

| 命令     | 是否需要子Shell | 是否需要执行权限 | 是否影响当前Shell | 使用场景                         |
| -------- | --------------- | ---------------- | ----------------- | -------------------------------- |
| `./`     | 是              | 是               | 否                | 独立运行脚本,不影响当前环境      |
| `bash`   | 是              | 否               | 否                | 用Bash运行脚本,不影响当前环境    |
| `.`      | 否              | 否               | 是                | 加载脚本内容到当前环境           |
| `source` | 否              | 否               | 是                | 与`.`一样,习惯问题               |

**示例:**
```bash
# 方式1: 作为可执行程序
./build.sh           # 需要执行权限
bash build.sh        # 不需要执行权限

# 方式2: 作为解释器参数
/bin/sh test.sh      # 不需要在脚本第一行指定解释器

# 方式3: 加载到当前环境
source setup_env.sh  # 常用于加载环境变量
. setup_env.sh       # 与source等效
```

> [!warning] 注意事项
> 1. **执行权限**: 使用`./`时,脚本需要有执行权限,可通过`chmod +x build.sh`添加
> 2. **变量和作用域**: `source`和`.`会影响当前环境,慎用以免污染环境
> 3. **推荐方式**: `./`和`bash`是推荐方式,尤其在希望脚本独立运行时

### 变量

#### 定义和使用变量
```bash
# 定义变量(等号两边不能有空格)
your_name="runoob"

# 使用变量
echo $name
echo ${name}  # 推荐:花括号帮助解释器识别变量边界

# 在判断时使用双引号,避免$1为空时出错
if [ "$1" = "test" ]; then
    echo "Test mode"
fi
```

> [!important] 重要特性
> 在Shell中,所有变量都默认以**字符串**形式存储,但根据使用上下文可以表现为整数或其他类型。

#### 只读变量和删除变量
```bash
# 只读变量
readonly name
# name="new"  # 错误!只读变量不能修改

# 删除变量
unset name  # 不能删除只读变量
```

#### 变量类型

**1. 字符串变量**
```bash
str1='single quotes'
str2="double quotes"
```

**2. 整数变量**
```bash
declare -i num=10
# 或
typeset -i num=10
```

**3. 数组变量**
```bash
# 整数数组
array=(1 2 3 4 5)

# 关联数组(类似字典)
declare -A assoc_array
assoc_array["key1"]="value1"
assoc_array["key2"]="value2"
```

**4. 环境变量**
```bash
echo $PATH    # 可执行程序的路径列表
echo $HOME    # 当前用户主目录
echo $SHELL   # Shell程序的路径
```

**5. 特殊变量**
```bash
$0   # 脚本的名称
$1   # 第一个参数
$2   # 第二个参数
$#   # 传递给脚本的参数数量
$?   # 上一个命令的退出状态(0表示成功)
$@   # 所有参数,每个参数独立引用
$*   # 所有参数,作为一个字符串
$$   # 当前Shell的进程ID
```

### 数组

#### 读取数组
```bash
# 定义数组
array=(apple banana orange)

# 读取单个元素
echo ${array[0]}    # apple

# 读取所有元素
echo ${array[@]}    # 所有元素
echo ${array[*]}    # 所有元素(与@类似)
```

#### 获取数组长度
```bash
array=(1 2 3 4 5)

# 获取数组长度
length=${#array[@]}
echo $length  # 5

# 也可以使用*
length=${#array[*]}
```

#### 关联数组(伪二维数组)
```bash
# 声明关联数组
declare -A matrix

# 使用字符串作为索引,实现伪二维数组
matrix["0,0"]="a"
matrix["0,1"]="b"
matrix["1,0"]="c"
matrix["1,1"]="d"

# 访问元素
echo ${matrix["0,1"]}  # b

# 删除元素
unset matrix["0,0"]
```

### 运算符

#### 算术运算符
```bash
a=10
b=20

# 算术运算使用$(())
result=$((a + b))   # 加法: 30
result=$((a - b))   # 减法: -10
result=$((a * b))   # 乘法: 200
result=$((a / b))   # 除法: 0 (整数除法)
result=$((a % b))   # 取模: 10

# 自增/自减
((i++))
((i--))
```

#### 关系运算符(用于整数比较)
```bash
a=10
b=20

[ $a -eq $b ]  # 等于 (equal)
[ $a -ne $b ]  # 不等于 (not equal)
[ $a -gt $b ]  # 大于 (greater than)
[ $a -lt $b ]  # 小于 (less than)
[ $a -ge $b ]  # 大于或等于 (greater or equal)
[ $a -le $b ]  # 小于或等于 (less or equal)
```

#### 布尔运算符
```bash
[ ! false ]              # 逻辑非
[ $a -gt 0 -a $b -gt 0 ] # 逻辑与 (AND)
[ $a -gt 0 -o $b -gt 0 ] # 逻辑或 (OR)
```

#### 字符串运算符
```bash
str1="hello"
str2="world"

[ "$str1" = "$str2" ]   # 字符串相等
[ "$str1" != "$str2" ]  # 字符串不等
[ -z "$str1" ]          # 字符串长度为零
[ -n "$str1" ]          # 字符串长度非零
```

> [!warning] 字符串比较注意
> 必须将变量用引号包裹,避免空值导致错误。

#### 文件测试运算符
```bash
[ -e file ]  # 文件是否存在
[ -f file ]  # 是否为普通文件
[ -d dir ]   # 是否为目录
[ -r file ]  # 文件是否可读
[ -w file ]  # 文件是否可写
[ -x file ]  # 文件是否可执行
[ -s file ]  # 文件是否非空(大小>0)
```

### echo命令

```bash
# 显示普通字符串
echo "wisewavetech"

# 显示转义字符串
echo "\"wisewavetech\""

# 显示变量
x=10
echo "It is variable ${x}"

# 显示换行(使用-e开启转义)
echo -e "wisewavetech \n"

# 显示不换行
echo -e "wisewavetech \c"
```

### 控制流程

#### if-else语句
```bash
# 使用[]作为判断语句
if [ condition ]; then
    command
elif [ condition ]; then
    command
else
    command
fi

# 使用(())作为判断语句(用于整数运算)
if (( i > 5 )); then
    echo "i大于5"
elif (( i == 5 )); then
    echo "i等于5"
else
    echo "i小于5"
fi
```

#### for循环
```bash
# 方式1: 遍历列表
for item in apple banana orange; do
    echo $item
done

# 方式2: C风格循环
for (( i=1; i<=5; i++ )); do
    echo "Number: $i"
done

# 方式3: 遍历数组
array=(1 2 3 4 5)
for item in "${array[@]}"; do
    echo $item
done
```

#### while循环
```bash
i=1
while (( i <= 5 )); do
    echo "Count: $i"
    ((i++))
done
```

#### case语句
```bash
case $value in
    mode1)
        command1
        ;;
    mode2)
        command2
        ;;
    *)
        default_command
        ;;
esac
```

### []和(())的区别

| 特性                 | `[]`                       | `(())`                         |
| -------------------- | -------------------------- | ------------------------------ |
| **主要用途**         | 条件测试(字符串、文件等)   | 数学运算与整数条件测试         |
| **运算符**           | `-eq, -ne, -gt, -lt`等     | `==, !=, >, <, >=, <=, ++, --` |
| **变量是否需要$**    | 需要                       | 不需要(但支持$)                |
| **支持的类型**       | 字符串、整数、文件状态     | 整数(不支持字符串或浮点数)     |
| **数学运算支持**     | 不支持                     | 支持                           |

**[]使用注意:**
```bash
# 空格敏感
[ $x -eq 1 ]       # 正确
[$x -eq 1]         # 错误!缺少空格

# 字符串比较必须加引号
[ "$str" = "test" ]  # 正确
[ $str = test ]      # 可能出错(str为空时)
```

**(())使用注意:**
```bash
# 用于数学运算
result=$((x + y))

# 用于整数判断
if (( x > 5 )); then
    echo "x大于5"
fi

# 不能用于字符串比较
# (( str == "test" ))  # 错误!
```

### 常用命令

#### find命令
**语法:** `find [路径] [匹配条件] [动作]`

**常用参数:**
- `-name pattern`: 按文件名查找,支持通配符
- `-type type`: 按文件类型查找(`f`文件,`d`目录,`l`链接)
- `-mtime days`: 按修改时间查找

**示例:**
```bash
# 查找当前目录下名为file.txt的文件
find . -name file.txt

# 查找所有.c文件
find . -name "*.c"

# 查找7天前修改过的文件
find /var/log -mtime +7

# 查找最近20天内修改的文件
find . -ctime -20
```

#### dirname命令
```bash
# 获取脚本所在目录
script_dir=$(dirname "$0")
echo "脚本目录: $script_dir"

# 常用于加载同目录下的配置文件
source "$(dirname "$0")/config.sh"
```

---
## 🤔 Q&A

### Q1: 什么时候使用source,什么时候使用./执行脚本?
**A**:
- **source/`.`**: 用于加载环境变量、函数定义等,会影响当前Shell环境。常用场景:加载配置文件(如`source ~/.bashrc`)
- **`./`/`bash`**: 用于独立运行脚本,不会影响当前Shell环境。适用于大多数脚本执行场景

### Q2: Shell变量为什么不需要声明类型?
**A**: Shell中所有变量都默认以字符串形式存储,但会根据使用上下文自动转换。例如在`$((x + y))`中会被视为整数,在`[ "$x" = "abc" ]`中被视为字符串。

### Q3: []和(())有什么实际使用建议?
**A**:
- **[]**: 用于字符串比较、文件测试、混合类型判断
- **(())**: 用于纯数学运算和整数比较,语法更简洁

### Q4: 如何调试Shell脚本?
**A**:
- 使用`bash -x script.sh`查看执行过程
- 在脚本中添加`set -x`开启调试,`set +x`关闭调试
- 使用`echo`输出变量值进行调试

## 🚀 Tasks
- [ ] 编写一个脚本,接收命令行参数并进行处理
- [ ] 使用数组和循环处理多个文件
- [ ] 实现一个菜单系统,使用case语句
- [ ] 编写脚本进行文件备份,使用find命令

## 📚 Reference
* [Shell教程 - 菜鸟教程](https://www.runoob.com/linux/linux-shell.html)
* Linux Shell脚本攻略
* Advanced Bash-Scripting Guide

## 🕸️ Relation
* 这篇笔记是[[00_Shell_MOC|Shell知识体系]]的基础部分
* [[00_Linux_MOC|Linux知识体系]] - Shell是Linux系统管理的核心工具
* [[00_Programming_MOC]] - Shell脚本编程也是编程的一部分
