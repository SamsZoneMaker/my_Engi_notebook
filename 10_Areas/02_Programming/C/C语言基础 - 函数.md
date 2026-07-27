---
created: 2025-11-18
tags:
  - type/knowledge
  - topic/programming/c
---
> [!abstract] 摘要
> 本笔记详细介绍C语言函数的定义、调用、参数传递、返回值、作用域、递归等核心概念,帮助你掌握模块化编程的基础。

## 🎯 Target
- [ ] 理解函数的定义和声明
- [ ] 掌握函数的参数传递机制
- [ ] 了解函数的返回值和return语句
- [ ] 理解变量的作用域和生命周期
- [ ] 掌握递归函数的编写
- [ ] 了解函数指针的基本概念

## 📝 Core

### 函数的基本概念

#### 什么是函数?

**函数** 是一段完成特定任务的代码块,可以被重复调用。

**函数的优点:**
- ✅ **代码复用**: 一次编写,多次调用
- ✅ **模块化**: 将复杂问题分解为小问题
- ✅ **可维护性**: 易于调试和修改
- ✅ **可读性**: 使程序结构清晰

**C程序的结构:**
```c
#include <stdio.h>

// 函数声明
int add(int a, int b);

// 主函数
int main() {
    int result = add(5, 3);
    printf("5 + 3 = %d\n", result);
    return 0;
}

// 函数定义
int add(int a, int b) {
    return a + b;
}
```

### 函数的定义

#### 基本语法

```c
返回类型 函数名(参数列表) {
    // 函数体
    return 返回值;
}
```

**组成部分:**
1. **返回类型**: 函数返回值的数据类型(int、float、void等)
2. **函数名**: 标识符,遵循变量命名规则
3. **参数列表**: 输入参数,可以有多个或无参数
4. **函数体**: 实现函数功能的代码块
5. **return语句**: 返回结果给调用者

#### 示例

**1. 无参数无返回值**
```c
void print_hello() {
    printf("Hello, World!\n");
}
```

**2. 有参数无返回值**
```c
void print_number(int num) {
    printf("数字是: %d\n", num);
}
```

**3. 有参数有返回值**
```c
int add(int a, int b) {
    return a + b;
}
```

**4. 多个参数**
```c
int max_of_three(int a, int b, int c) {
    int max = a;
    if (b > max) max = b;
    if (c > max) max = c;
    return max;
}
```

**5. 返回浮点数**
```c
double calculate_average(int sum, int count) {
    return (double)sum / count;
}
```

### 函数的声明与定义

#### 函数声明(原型)

**作用:** 告诉编译器函数的存在,使得可以在定义之前调用

**语法:**
```c
返回类型 函数名(参数类型列表);
```

**示例:**
```c
// 函数声明
int add(int, int);  // 可以省略参数名
int multiply(int a, int b);  // 也可以包含参数名

int main() {
    int result = add(5, 3);  // 可以调用
    return 0;
}

// 函数定义
int add(int a, int b) {
    return a + b;
}
```

> [!tip] 最佳实践
> - 在头文件(.h)中放函数声明
> - 在源文件(.c)中放函数定义
> - main函数之前声明所有使用的函数

#### 函数定义的位置

**方式1: 先声明后定义(推荐)**
```c
#include <stdio.h>

// 声明
int add(int a, int b);

int main() {
    printf("%d\n", add(5, 3));
    return 0;
}

// 定义
int add(int a, int b) {
    return a + b;
}
```

**方式2: 定义在main之前**
```c
#include <stdio.h>

// 直接定义(无需声明)
int add(int a, int b) {
    return a + b;
}

int main() {
    printf("%d\n", add(5, 3));
    return 0;
}
```

### 函数的调用

#### 基本调用

```c
int sum(int a, int b) {
    return a + b;
}

int main() {
    // 方式1: 直接使用返回值
    printf("%d\n", sum(5, 3));

    // 方式2: 保存返回值
    int result = sum(10, 20);
    printf("%d\n", result);

    // 方式3: 作为表达式的一部分
    int total = sum(5, 3) + sum(10, 20);

    return 0;
}
```

#### 函数调用栈

```c
int add(int a, int b) {
    return a + b;
}

int calculate(int x, int y) {
    int result = add(x, y);  // 调用add函数
    return result * 2;
}

int main() {
    int value = calculate(5, 3);  // 调用calculate函数
    return 0;
}
```

**调用栈示意:**
```
1. main函数被调用
   ├─ 调用calculate(5, 3)
   │  ├─ 调用add(5, 3)
   │  │  └─ 返回8
   │  └─ 返回16
   └─ value = 16
```

### 参数传递

#### 值传递(Pass by Value)

C语言函数参数默认是**值传递**:
- 传递给函数的是参数的副本
- 函数内部修改不影响原始变量

**示例:**
```c
void modify_value(int x) {
    x = 100;  // 只修改副本
    printf("函数内: x = %d\n", x);  // 100
}

int main() {
    int num = 10;
    modify_value(num);
    printf("函数外: num = %d\n", num);  // 仍然是10
    return 0;
}
```

#### 传递指针(模拟引用传递)

**通过指针可以修改原始变量:**
```c
void modify_value(int *x) {
    *x = 100;  // 修改指针指向的值
    printf("函数内: *x = %d\n", *x);  // 100
}

int main() {
    int num = 10;
    modify_value(&num);  // 传递地址
    printf("函数外: num = %d\n", num);  // 100
    return 0;
}
```

#### 传递数组

**数组名作为参数时,实际传递的是指针:**
```c
void modify_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = arr[i] * 2;  // 会修改原数组
    }
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    modify_array(numbers, size);

    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);  // 2 4 6 8 10
    }
    return 0;
}
```

> [!important] 数组传递的本质
> - 数组名衰减为指针
> - 函数内无法使用sizeof获取数组大小
> - 需要额外传递数组大小参数

#### 实际应用示例

**1. 交换两个变量**
```c
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 10, y = 20;
    printf("交换前: x=%d, y=%d\n", x, y);
    swap(&x, &y);
    printf("交换后: x=%d, y=%d\n", x, y);
    return 0;
}
```

**2. 计算数组的和与平均值**
```c
int array_sum(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

double array_average(int arr[], int size) {
    int sum = array_sum(arr, size);
    return (double)sum / size;
}

int main() {
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    int sum = array_sum(numbers, size);
    double avg = array_average(numbers, size);

    printf("和: %d\n", sum);        // 150
    printf("平均值: %.2f\n", avg);  // 30.00
    return 0;
}
```

### 返回值

#### return语句

**作用:**
1. 结束函数执行
2. 返回结果给调用者

**语法:**
```c
return 表达式;
```

**示例:**

**1. 返回计算结果**
```c
int square(int num) {
    return num * num;
}
```

**2. 多个return语句**
```c
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// 更简洁的写法
int max_v2(int a, int b) {
    return (a > b) ? a : b;
}
```

**3. void函数的return**
```c
void print_positive(int num) {
    if (num <= 0) {
        return;  // 提前退出
    }
    printf("%d是正数\n", num);
}
```

#### 返回指针

```c
int* get_array_address(int arr[]) {
    return arr;  // 返回数组地址
}

int* create_array(int size) {
    // 注意: 不能返回局部数组的地址!
    // int arr[size];  // 错误!
    // return arr;

    // 正确做法: 使用动态内存分配
    int *arr = (int*)malloc(size * sizeof(int));
    return arr;
}
```

> [!warning] 返回值陷阱
> - 不要返回局部变量的地址
> - 不要返回栈上分配的数组地址
> - 返回动态分配的内存记得释放

### 变量的作用域

#### 局部变量

**定义:** 在函数内部声明的变量

**特点:**
- 只在函数内部可见
- 函数调用时创建,结束时销毁
- 不同函数可以有同名局部变量

```c
void func1() {
    int x = 10;  // 局部变量
    printf("func1: x = %d\n", x);
}

void func2() {
    int x = 20;  // 另一个局部变量
    printf("func2: x = %d\n", x);
}

int main() {
    func1();  // 输出: func1: x = 10
    func2();  // 输出: func2: x = 20
    return 0;
}
```

#### 全局变量

**定义:** 在函数外部声明的变量

**特点:**
- 整个程序都可见
- 程序启动时创建,结束时销毁
- 慎用,容易产生副作用

```c
#include <stdio.h>

int global_var = 100;  // 全局变量

void modify() {
    global_var = 200;
}

int main() {
    printf("修改前: %d\n", global_var);  // 100
    modify();
    printf("修改后: %d\n", global_var);  // 200
    return 0;
}
```

#### 静态变量(static)

**特点:**
- 保持值在函数调用之间不变
- 只初始化一次

```c
void counter() {
    static int count = 0;  // 静态局部变量
    count++;
    printf("函数被调用了 %d 次\n", count);
}

int main() {
    counter();  // 1
    counter();  // 2
    counter();  // 3
    return 0;
}
```

#### 作用域总结

| 变量类型 | 声明位置 | 作用域 | 生命周期 | 默认初始值 |
|----------|----------|--------|----------|------------|
| **局部变量** | 函数内 | 当前函数 | 函数调用期间 | 未定义(随机值) |
| **全局变量** | 函数外 | 整个程序 | 程序运行期间 | 0 |
| **静态局部变量** | 函数内+static | 当前函数 | 程序运行期间 | 0 |
| **静态全局变量** | 函数外+static | 当前文件 | 程序运行期间 | 0 |

### 递归函数

#### 什么是递归?

**递归** 是函数直接或间接调用自己的过程。

**递归的两个关键要素:**
1. **基础情况(Base Case)**: 递归的终止条件
2. **递归情况(Recursive Case)**: 问题规模缩小的递归调用

#### 经典示例

**1. 阶乘**
```c
// n! = n × (n-1)!
int factorial(int n) {
    // 基础情况
    if (n == 0 || n == 1) {
        return 1;
    }
    // 递归情况
    return n * factorial(n - 1);
}

int main() {
    printf("5! = %d\n", factorial(5));  // 120
    return 0;
}
```

**递归过程:**
```
factorial(5)
= 5 * factorial(4)
= 5 * (4 * factorial(3))
= 5 * (4 * (3 * factorial(2)))
= 5 * (4 * (3 * (2 * factorial(1))))
= 5 * (4 * (3 * (2 * 1)))
= 5 * (4 * (3 * 2))
= 5 * (4 * 6)
= 5 * 24
= 120
```

**2. 斐波那契数列**
```c
// F(n) = F(n-1) + F(n-2)
int fibonacci(int n) {
    // 基础情况
    if (n == 0) return 0;
    if (n == 1) return 1;
    // 递归情况
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    for (int i = 0; i < 10; i++) {
        printf("%d ", fibonacci(i));
    }
    // 输出: 0 1 1 2 3 5 8 13 21 34
    return 0;
}
```

**3. 幂运算**
```c
// x^n = x × x^(n-1)
int power(int x, int n) {
    // 基础情况
    if (n == 0) return 1;
    // 递归情况
    return x * power(x, n - 1);
}

int main() {
    printf("2^10 = %d\n", power(2, 10));  // 1024
    return 0;
}
```

**4. 最大公约数(GCD)**
```c
// gcd(a, b) = gcd(b, a % b)
int gcd(int a, int b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}

int main() {
    printf("gcd(48, 18) = %d\n", gcd(48, 18));  // 6
    return 0;
}
```

**5. 数组求和**
```c
int array_sum(int arr[], int size) {
    // 基础情况
    if (size == 0) {
        return 0;
    }
    // 递归情况
    return arr[size - 1] + array_sum(arr, size - 1);
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    printf("和: %d\n", array_sum(numbers, size));  // 15
    return 0;
}
```

#### 递归 vs 迭代

| 特性 | 递归 | 迭代 |
|------|------|------|
| **代码** | 简洁优雅 | 可能冗长 |
| **效率** | 较低(函数调用开销) | 较高 |
| **内存** | 栈空间(可能溢出) | 少量内存 |
| **适用** | 树、图等递归结构 | 简单循环 |

**迭代版本的阶乘:**
```c
int factorial_iterative(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}
```

> [!tip] 何时使用递归?
> - 问题本身具有递归性质(如树遍历)
> - 代码简洁性优先于性能
> - 递归深度可控(不会栈溢出)
>
> 其他情况优先考虑迭代。

### 函数指针(入门)

#### 基本概念

**函数指针** 是指向函数的指针变量。

**语法:**
```c
返回类型 (*指针名)(参数类型列表);
```

**示例:**
```c
// 普通函数
int add(int a, int b) {
    return a + b;
}

int main() {
    // 声明函数指针
    int (*func_ptr)(int, int);

    // 指向add函数
    func_ptr = add;  // 或 func_ptr = &add;

    // 通过函数指针调用函数
    int result = func_ptr(5, 3);  // 或 (*func_ptr)(5, 3);
    printf("5 + 3 = %d\n", result);  // 8

    return 0;
}
```

#### 函数指针作为参数

```c
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }

// 接受函数指针作为参数
int calculate(int a, int b, int (*operation)(int, int)) {
    return operation(a, b);
}

int main() {
    printf("5 + 3 = %d\n", calculate(5, 3, add));       // 8
    printf("5 - 3 = %d\n", calculate(5, 3, subtract));  // 2
    printf("5 * 3 = %d\n", calculate(5, 3, multiply));  // 15
    return 0;
}
```

> [!note] 更多内容
> 函数指针的高级应用请参考 [[C语言进阶 - 指针详解]]

### 常见陷阱和错误

#### 陷阱1: 函数声明与定义不一致
```c
// 声明
int add(int a, int b);

// 定义 - 参数类型不一致!
float add(float a, float b) {  // 错误!
    return a + b;
}
```

#### 陷阱2: 返回局部变量的地址
```c
// 危险!返回栈上局部变量的地址
int* create_array() {
    int arr[10] = {1, 2, 3};  // 局部变量
    return arr;  // 函数结束后arr被销毁!
}

// 正确做法:返回动态分配的内存
int* create_array_safe() {
    int *arr = (int*)malloc(10 * sizeof(int));
    return arr;  // 调用者需要free
}
```

#### 陷阱3: 修改const参数
```c
void process(const int *arr, int size) {
    // arr[0] = 10;  // 错误!不能修改const数据
    printf("%d\n", arr[0]);  // OK
}
```

#### 陷阱4: 数组参数的sizeof
```c
void print_size(int arr[]) {
    // sizeof(arr)返回指针大小,不是数组大小!
    printf("%zu\n", sizeof(arr));  // 输出4或8(指针大小)
}

int main() {
    int numbers[10];
    printf("%zu\n", sizeof(numbers));  // 输出40(数组大小)
    print_size(numbers);
    return 0;
}
```

#### 陷阱5: 递归没有终止条件
```c
// 危险!无限递归导致栈溢出
int bad_factorial(int n) {
    return n * bad_factorial(n - 1);  // 没有终止条件!
}

// 正确
int factorial(int n) {
    if (n <= 1) {  // 终止条件
        return 1;
    }
    return n * factorial(n - 1);
}
```

### 最佳实践

#### 1. 函数应该只做一件事
```c
// 不推荐:函数做太多事
void process_and_print_and_save(int *arr, int size) {
    // 处理数据
    // 打印数据
    // 保存到文件
}

// 推荐:拆分为多个函数
void process_data(int *arr, int size) { }
void print_data(int *arr, int size) { }
void save_data(int *arr, int size) { }
```

#### 2. 使用const保护只读参数
```c
// 表明函数不会修改数组
int array_sum(const int *arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}
```

#### 3. 检查指针参数
```c
void process(int *data) {
    if (data == NULL) {  // 防御性检查
        return;
    }
    // 处理数据
}
```

#### 4. 函数名应该清晰表达意图
```c
// 不推荐
int calc(int a, int b);

// 推荐
int calculate_area(int width, int height);
int find_maximum(int a, int b);
```

#### 5. 限制函数参数数量
```c
// 不推荐:参数太多
void create_window(int x, int y, int width, int height,
                   int r, int g, int b, int border,
                   int style, int flags);

// 推荐:使用结构体
typedef struct {
    int x, y;
    int width, height;
    int r, g, b;
    int border, style, flags;
} WindowConfig;

void create_window(const WindowConfig *config);
```

### 高级函数技巧

#### 可变参数函数
```c
#include <stdarg.h>
#include <stdio.h>

// 求多个整数的和
int sum(int count, ...) {
    va_list args;
    va_start(args, count);

    int total = 0;
    for (int i = 0; i < count; i++) {
        total += va_arg(args, int);
    }

    va_end(args);
    return total;
}

int main() {
    printf("%d\n", sum(3, 1, 2, 3));      // 6
    printf("%d\n", sum(5, 1, 2, 3, 4, 5)); // 15
    return 0;
}
```

#### 回调函数模式
```c
#include <stdio.h>

// 回调函数类型
typedef void (*callback_t)(int);

// 执行操作并调用回调
void process_numbers(int *arr, int size, callback_t callback) {
    for (int i = 0; i < size; i++) {
        callback(arr[i]);
    }
}

// 回调函数实现
void print_number(int n) {
    printf("%d ", n);
}

void print_square(int n) {
    printf("%d ", n * n);
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("原数字: ");
    process_numbers(numbers, size, print_number);

    printf("\n平方: ");
    process_numbers(numbers, size, print_square);
    printf("\n");

    return 0;
}
```

### 实战项目示例

#### 项目1: 字符串处理工具库
```c
#include <stdio.h>
#include <ctype.h>
#include <string.h>

// 去除字符串两端空白
char* trim(char *str) {
    if (str == NULL) return NULL;

    // 去除开头空白
    while (isspace(*str)) {
        str++;
    }

    if (*str == '\0') {
        return str;
    }

    // 去除末尾空白
    char *end = str + strlen(str) - 1;
    while (end > str && isspace(*end)) {
        end--;
    }
    *(end + 1) = '\0';

    return str;
}

// 字符串反转
void reverse_string(char *str) {
    if (str == NULL) return;

    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

// 统计单词数
int count_words(const char *str) {
    if (str == NULL) return 0;

    int count = 0;
    int in_word = 0;

    while (*str) {
        if (isspace(*str)) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            count++;
        }
        str++;
    }

    return count;
}

// 转换为大写
void to_uppercase(char *str) {
    while (*str) {
        *str = toupper(*str);
        str++;
    }
}

// 测试
int main() {
    char str1[] = "   hello world   ";
    printf("原字符串: '%s'\n", str1);
    printf("去除空白: '%s'\n", trim(str1));

    char str2[] = "Hello";
    reverse_string(str2);
    printf("反转: %s\n", str2);

    char str3[] = "The quick brown fox";
    printf("单词数: %d\n", count_words(str3));

    char str4[] = "hello";
    to_uppercase(str4);
    printf("大写: %s\n", str4);

    return 0;
}
```

#### 项目2: 数学工具库
```c
#include <stdio.h>
#include <math.h>

// 判断素数
int is_prime(int n) {
    if (n <= 1) return 0;
    if (n <= 3) return 1;
    if (n % 2 == 0 || n % 3 == 0) return 0;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return 0;
        }
    }
    return 1;
}

// 最大公约数(欧几里得算法)
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// 最小公倍数
int lcm(int a, int b) {
    return (a * b) / gcd(a, b);
}

// 阶乘
long long factorial(int n) {
    if (n <= 1) return 1;
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// 组合数C(n,k)
long long combination(int n, int k) {
    if (k > n) return 0;
    if (k == 0 || k == n) return 1;

    k = (k < n - k) ? k : n - k;  // 优化

    long long result = 1;
    for (int i = 0; i < k; i++) {
        result *= (n - i);
        result /= (i + 1);
    }
    return result;
}

// 检查完美数
int is_perfect(int n) {
    if (n <= 1) return 0;

    int sum = 1;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            sum += i;
            if (i != n / i) {
                sum += n / i;
            }
        }
    }
    return sum == n;
}

int main() {
    printf("29是素数: %d\n", is_prime(29));
    printf("gcd(48, 18) = %d\n", gcd(48, 18));
    printf("lcm(12, 18) = %d\n", lcm(12, 18));
    printf("5! = %lld\n", factorial(5));
    printf("C(5,2) = %lld\n", combination(5, 2));
    printf("28是完美数: %d\n", is_perfect(28));

    return 0;
}
```

#### 项目3: 数组排序与查找库
```c
#include <stdio.h>

// 冒泡排序
void bubble_sort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < size - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = 1;
            }
        }
        if (!swapped) break;  // 优化:已排序
    }
}

// 选择排序
void selection_sort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < size; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            int temp = arr[i];
            arr[i] = arr[min_idx];
            arr[min_idx] = temp;
        }
    }
}

// 二分查找(要求数组已排序)
int binary_search(const int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;  // 找到
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;  // 未找到
}

// 线性查找
int linear_search(const int arr[], int size, int target) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

// 查找最大值索引
int find_max_index(const int arr[], int size) {
    if (size <= 0) return -1;

    int max_idx = 0;
    for (int i = 1; i < size; i++) {
        if (arr[i] > arr[max_idx]) {
            max_idx = i;
        }
    }
    return max_idx;
}

// 打印数组
void print_array(const int arr[], int size) {
    printf("[");
    for (int i = 0; i < size; i++) {
        printf("%d", arr[i]);
        if (i < size - 1) printf(", ");
    }
    printf("]\n");
}

int main() {
    int arr1[] = {64, 34, 25, 12, 22, 11, 90};
    int size1 = sizeof(arr1) / sizeof(arr1[0]);

    printf("原数组: ");
    print_array(arr1, size1);

    bubble_sort(arr1, size1);
    printf("排序后: ");
    print_array(arr1, size1);

    int target = 25;
    int index = binary_search(arr1, size1, target);
    printf("查找%d: 索引=%d\n", target, index);

    int max_idx = find_max_index(arr1, size1);
    printf("最大值: %d (索引=%d)\n", arr1[max_idx], max_idx);

    return 0;
}
```

---

## 🤔 Q&A

### Q1: 函数声明和函数定义有什么区别?
**A**:
- **声明**: 告诉编译器函数的存在,包括返回类型、名称、参数
- **定义**: 实际实现函数的功能代码
- 可以多次声明,但只能定义一次

```c
int add(int, int);  // 声明(原型)

int add(int a, int b) {  // 定义
    return a + b;
}
```

### Q2: 为什么修改函数参数不影响原变量?
**A**: 因为C语言使用**值传递**,传递的是参数的副本。如果想修改原变量,需要传递指针:
```c
void modify(int *x) {
    *x = 100;
}
int num = 10;
modify(&num);  // 现在num变成100
```

### Q3: 什么时候使用递归,什么时候使用循环?
**A**:
- **递归**: 问题本身具有递归性质(树、分治算法)、代码简洁性优先
- **循环**: 简单重复任务、性能要求高、递归深度不确定

一般来说,能用循环的就用循环,性能更好。

### Q4: 函数可以返回数组吗?
**A**: 不能直接返回数组,但可以:
1. 返回指向动态分配数组的指针
2. 使用指针参数接收结果
3. 使用结构体包装数组

```c
// 方法1: 返回指针
int* create_array(int size) {
    int *arr = (int*)malloc(size * sizeof(int));
    return arr;
}

// 方法2: 通过参数
void fill_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = i;
    }
}
```

### Q5: 局部变量和全局变量如何选择?
**A**:
- **优先使用局部变量**: 作用域小,不易出错
- **谨慎使用全局变量**: 容易产生副作用,难以调试
- 如果多个函数需要共享数据,考虑通过参数传递或使用结构体

## 🚀 Tasks

### 基础练习
- [ ] 编写一个函数判断一个数是否为素数
- [ ] 实现一个递归函数计算字符串长度
- [ ] 编写函数实现冒泡排序
- [ ] 实现最大公约数和最小公倍数函数
- [ ] 编写函数计算数组的和与平均值

### 递归练习
- [ ] 使用递归实现汉诺塔问题
- [ ] 递归实现数组求和
- [ ] 递归实现字符串反转
- [ ] 递归实现快速排序
- [ ] 递归实现二叉树遍历(了解)

### 高级练习
- [ ] 实现可变参数函数(printf风格)
- [ ] 编写使用函数指针的回调机制
- [ ] 实现通用的排序函数(使用比较函数指针)

### 实战项目
- [x] 字符串处理工具库
- [x] 数学工具库
- [x] 数组排序与查找库
- [ ] 文件操作封装库
- [ ] 简单的JSON解析器
- [ ] 表达式求值器

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C和指针 - Kenneth A. Reek

## 🕸️ Relation
* [[C 语言知识地图]] - C语言知识体系
* [[C语言基础 - 数据类型与变量]] - 函数需要使用变量
* [[C语言基础 - 控制流]] - 函数内部使用控制流
* [[C语言基础 - 数组]] - 函数常用于处理数组
* [[C语言进阶 - 指针详解]] - 深入理解函数指针和指针参数
