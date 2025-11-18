---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/basic"
  - "#lang/c"
status: 完善中
complexity: 基础
notetype: 学习笔记
resource: C语言程序设计
related:
  - "[[00_C_MOC]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# C语言基础 - 数据类型与变量

> [!abstract] 摘要
> 本笔记介绍C语言中的基本数据类型、变量定义、运算符和格式化输出的基础知识。

## 🎯 Target
- [ ] 掌握C语言的基本数据类型
- [ ] 理解变量的定义和命名规则
- [ ] 熟练使用占位符进行格式化输出
- [ ] 了解数据类型的取值范围

## 📝 Core

### 变量基础

#### 变量的组成
程序变量包括三个要素:
- **类型**: 如`int`、`char`、`float`等
- **变量名**: 遵循命名规则
- **变量值**: 存储的数据

```c
int num = 1;  // 类型 变量名 = 变量值
```

#### 命名规则
- 变量名不以数字开头
- 可以使用字母、数字和下划线
- 区分大小写
- 不能使用C语言关键字

### 基本数据类型

#### 整型 (Integer)
```c
int a = 10;           // 整型
short b = 5;          // 短整型
long c = 100000L;     // 长整型
unsigned int d = 20;  // 无符号整型
```

**特点:**
- 整型变量存储整数值
- 不同类型占用不同的内存空间
- 有符号整型可以存储负数,无符号整型只能存储非负数

#### 字符型 (Character)
```c
char c = 'A';  // 字符型变量
```

**说明:**
- `char`用来定义字符,定义方法类似于`int`
- 单个字符用单引号括起来
- 使用`getchar()`获取输入的字符

#### 浮点型 (Floating Point)
```c
float f = 3.14f;      // 单精度浮点数
double d = 3.1415926; // 双精度浮点数
```

**注意事项:**
- `float`为单精度的小数值
- 不同类型数据进行运算时,比如两个整数相除,必须将除数或被除数强制转换成小数,否则小数点后面的数据会被忽略

```c
int a = 5, b = 2;
float result = (float)a / b;  // 强制类型转换
```

### 数据类型范围查询

使用`<limits.h>`头文件可以查询各数据类型的取值范围:

```c
#include <stdio.h>
#include <limits.h>

int main() {
    puts("该环境下各字符型,整型数值的范围");
    printf("char            :%d~%d\n", CHAR_MIN , CHAR_MAX);
    printf("signed char     :%d~%d\n", SCHAR_MIN, SCHAR_MAX);
    printf("unsigned char   :%d~%d\n", 0, UCHAR_MAX);

    printf("short           :%d~%d\n", SHRT_MIN, SHRT_MAX);
    printf("int             :%d~%d\n", INT_MIN, INT_MAX);
    printf("long            :%ld~%ld\n", LONG_MIN, LONG_MAX);

    printf("unsigned short  :%u~%u\n", 0, USHRT_MAX);
    printf("unsigned        :%u~%u\n", 0, UINT_MAX);
    printf("unsigned long   :%u~%u\n", 0, ULONG_MAX);

    return 0;
}
```

### 占位符(格式说明符)

占位符代表在输出的地方占一个位,其输出的值取决于后面的变量值。

#### 常用占位符
```c
%d    // 整型(int)
%u    // 无符号整型(unsigned int)
%ld   // 长整型(long)
%f    // 浮点型(float/double)
%c    // 字符型(char)
%s    // 字符串(string)
%p    // 指针地址
```

#### 格式控制示例
```c
// %3d - 输出3位整型数,不够3位则右对齐
printf("%3d\n", 5);  // 输出: "  5"

// %9.2f - 输出为9位的浮点数,小数位为2,整数位为7,小数点占一位
printf("%9.2f\n", 3.14);  // 输出: "     3.14"
```

### 输入输出

#### printf - 格式化输出
```c
int num = 10;
printf("num = %d\n", num);  // 记得在printf后加\n换行
```

> [!tip] 提示
> 记得在`printf`后加`\n`换行符,保持输出格式整洁。

#### scanf - 格式化输入
```c
int num;
scanf("%d", &num);  // 注意要加地址符&
```

> [!warning] 重要提示
> - `scanf`双引号中除了占位符尽量不要写其他东西,否则输入时很有可能会产生错误
> - 占位符只是代表从键盘中输入一个数,输入要比输出多了一个地址的约束,也就是加一个`&`
> - 当连续输入多个变量时,最好分开写`scanf`,或者写成`scanf("%d%d", &num1, &num2);`的形式

### 运算符

#### 算术运算符
```c
+   // 加法
-   // 减法
*   // 乘法
/   // 除法
%   // 求模运算符(求余)
++  // 自增
--  // 自减
```

**自增/自减运算符:**
- `a++`: 先使用`a`的值再+1
- `++a`: 把现有的`a`的值+1后使用

```c
int a = 5;
printf("%d\n", a++);  // 输出5,之后a变为6
printf("%d\n", ++a);  // a先变为7,然后输出7
```

#### 逻辑运算符
```c
&&  // 逻辑与(and)
||  // 逻辑或(or)
!   // 逻辑非(not)
```

```c
int a = 5, b = 10;
if (a > 0 && b > 0) {  // 两个条件都为真
    printf("Both positive\n");
}
```

#### 按位运算符
```c
~   // 按位取反(计算反码)
<<  // 左移
>>  // 右移
&   // 按位与
|   // 按位或
^   // 按位异或
```

**位移运算示例:**
```c
int a = 8;
int b = a << 2;  // 将a左移2位,相当于a*4,结果为32
int c = a >> 1;  // 将a右移1位,相当于a/2,结果为4
```

### sizeof运算符

`sizeof`用于获取数据类型或变量占用的字节数:

```c
int a = 10;
printf("int占用的字节数: %lu\n", sizeof(int));
printf("变量a占用的字节数: %lu\n", sizeof(a));

// 数组示例
int arr[10];
printf("数组大小: %lu\n", sizeof(arr));  // 40字节(10*4)
printf("元素个数: %lu\n", sizeof(arr) / sizeof(arr[0]));  // 10
```

### const修饰符

`const`类型修饰符用于声明常量,确保变量值不能被修改:

```c
const int MAX = 100;  // 定义常量
// MAX = 200;  // 编译错误!const变量不能修改

// 在函数参数中使用const
void print_array(const int arr[], int n) {
    // arr[0] = 10;  // 编译错误!不能修改数组元素
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
}
```

> [!tip] 最佳实践
> 在函数声明接收数组的形参时应该使用`const`,确保函数中不能改写数组的元素值。

### 数据溢出

#### 无符号整型溢出
无符号整型的运算中不会发生数据溢出,当运算结果超出最大值时,结果为:
```
数学运算结果 % (该无符号整型能够表示的最大值 + 1)
```

---
## 🤔 Q&A

### Q1: 为什么整数除法会丢失小数部分?
**A**: C语言中,两个整数相除结果还是整数,小数部分会被截断。如需保留小数,必须将至少一个操作数强制转换为浮点型:
```c
int a = 5, b = 2;
float result = (float)a / b;  // 结果为2.5
```

### Q2: 什么时候使用unsigned类型?
**A**: 当你确定变量永远不会为负数时使用`unsigned`,如:
- 数组索引
- 计数器
- 文件大小
优势是可以存储更大的正数(范围翻倍)。

### Q3: sizeof返回的单位是什么?
**A**: `sizeof`返回的是字节数(bytes)。例如在大多数系统上,`sizeof(int)`返回4,表示int类型占用4个字节。

### Q4: 为什么scanf需要&符号?
**A**: `&`是取地址运算符,`scanf`需要知道变量的内存地址才能将输入的值存储到该位置。而数组名本身就是地址,所以不需要`&`。

## 🚀 Tasks
- [ ] 编写程序测试各数据类型的大小和范围
- [ ] 练习使用各种占位符进行格式化输出
- [ ] 实现一个程序,演示类型转换的效果
- [ ] 使用按位运算符实现简单的位操作

## 📚 Reference
* C Primer Plus
* C语言程序设计(谭浩强)
* <limits.h>头文件文档

## 🕸️ Relation
* 这篇笔记是[[00_C_MOC|C语言知识体系]]的基础部分
* [[C语言基础 - 控制流]]中会大量使用数据类型和变量
* [[C语言基础 - 数组]]需要理解数据类型的概念
* [[C语言进阶 - 指针]]中的指针类型与数据类型密切相关
