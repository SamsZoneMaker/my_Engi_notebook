---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/basic"
  - "#language/c"
status: 完善中
complexity: 基础
notetype: 学习笔记
resource: C Primer Plus、C程序设计语言
related:
  - "[[00_C_MOC]]"
  - "[[C语言基础 - 函数]]"
  - "[[C语言基础 - 控制流]]"
  - "[[C语言进阶 - 指针详解]]"
created: 2025-11-18 22:00:00
modified: 2026-01-09  14:47:03
---
# C语言基础 - 数组

> [!abstract] 摘要
> 本笔记详细介绍C语言数组的定义、初始化、访问、多维数组以及数组与指针的关系,帮助你掌握批量数据处理的基础。

## 🎯 Target
- [ ] 理解数组的概念和内存布局
- [ ] 掌握一维数组的定义、初始化和访问
- [ ] 掌握二维数组和多维数组的使用
- [ ] 了解数组与指针的关系
- [ ] 能够编写处理数组的函数
- [ ] 掌握字符数组和字符串的基本操作

## 📝 Core

### 数组的基本概念

#### 什么是数组?

**数组** 是一组相同类型数据的集合,在内存中连续存储。

**特点:**
- ✅ **相同类型**: 数组中所有元素类型相同
- ✅ **连续存储**: 元素在内存中连续排列
- ✅ **固定大小**: 数组大小在声明时确定,不能改变
- ✅ **索引访问**: 通过下标快速访问任意元素

**为什么需要数组?**
```c
// 不使用数组
int score1, score2, score3, score4, score5;

// 使用数组
int scores[5];  // 更简洁
```

#### 数组的内存布局

```c
int arr[5] = {10, 20, 30, 40, 50};
```

**内存示意图:**
```
内存地址    值
0x1000:    10  ← arr[0]
0x1004:    20  ← arr[1]
0x1008:    30  ← arr[2]
0x100C:    40  ← arr[3]
0x1010:    50  ← arr[4]
```

> [!note] 数组下标从0开始
> - 第一个元素: `arr[0]`
> - 最后一个元素: `arr[size-1]`
> - 访问`arr[size]`会越界!

### 一维数组

#### 定义与初始化

**语法:**
```c
数据类型 数组名[数组大小];
```

**示例:**

**1. 声明不初始化**
```c
int numbers[5];  // 包含5个int元素,值未定义(随机值)
```

**2. 完全初始化**
```c
int numbers[5] = {10, 20, 30, 40, 50};
```

**3. 部分初始化**
```c
int numbers[5] = {10, 20};  // {10, 20, 0, 0, 0}
// 未初始化的元素自动设为0
```

**4. 自动推导大小**
```c
int numbers[] = {10, 20, 30, 40, 50};
// 编译器自动推导大小为5
```

**5. 全部初始化为0**
```c
int numbers[100] = {0};  // 全部初始化为0
```

**6. 指定位置初始化(C99)**
```c
int arr[10] = {[0]=1, [4]=5, [9]=10};
// {1, 0, 0, 0, 5, 0, 0, 0, 0, 10}
```

#### 访问数组元素

**语法:**
```c
数组名[索引]
```

**示例:**
```c
int scores[5] = {85, 90, 78, 92, 88};

// 读取元素
printf("第一个分数: %d\n", scores[0]);  // 85
printf("最后一个分数: %d\n", scores[4]);  // 88

// 修改元素
scores[2] = 95;
printf("修改后的第三个分数: %d\n", scores[2]);  // 95
```

> [!warning] 数组越界
> C语言不检查数组越界,访问`arr[10]`(当数组大小为5)会导致:
> - 读取随机数据
> - 程序崩溃
> - 安全漏洞
>
> **程序员必须自己确保索引在有效范围内!**

#### 遍历数组

**使用for循环:**
```c
int numbers[] = {10, 20, 30, 40, 50};
int size = sizeof(numbers) / sizeof(numbers[0]);

for (int i = 0; i < size; i++) {
    printf("numbers[%d] = %d\n", i, numbers[i]);
}
```

> [!tip] 获取数组大小
> ```c
> int size = sizeof(数组名) / sizeof(数组名[0]);
> ```
> - `sizeof(numbers)`: 数组总字节数
> - `sizeof(numbers[0])`: 单个元素字节数
> - 结果: 元素个数

#### 数组作为函数参数

**方式1: 使用数组符号**
```c
void print_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    print_array(numbers, size);
    return 0;
}
```

**方式2: 使用指针**
```c
void print_array(int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
```

> [!important] 数组参数的本质
> - 数组名作为参数时,实际传递的是指针
> - 函数内无法用sizeof获取数组大小
> - 必须额外传递size参数

**示例: 计算数组和**
```c
int array_sum(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    int sum = array_sum(numbers, size);
    printf("数组元素之和: %d\n", sum);  // 150
    return 0;
}
```

#### 常见数组操作

**1. 查找最大值和最小值**
```c
void find_min_max(int arr[], int size, int *min, int *max) {
    *min = arr[0];
    *max = arr[0];

    for (int i = 1; i < size; i++) {
        if (arr[i] < *min) {
            *min = arr[i];
        }
        if (arr[i] > *max) {
            *max = arr[i];
        }
    }
}

int main() {
    int numbers[] = {45, 23, 67, 12, 89, 34};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    int min, max;

    find_min_max(numbers, size, &min, &max);
    printf("最小值: %d\n", min);  // 12
    printf("最大值: %d\n", max);  // 89
    return 0;
}
```

**2. 反转数组**
```c
void reverse_array(int arr[], int size) {
    for (int i = 0; i < size / 2; i++) {
        int temp = arr[i];
        arr[i] = arr[size - 1 - i];
        arr[size - 1 - i] = temp;
    }
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("反转前: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }

    reverse_array(numbers, size);

    printf("\n反转后: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    // 输出: 5 4 3 2 1
    return 0;
}
```

**3. 复制数组**
```c
void copy_array(int source[], int dest[], int size) {
    for (int i = 0; i < size; i++) {
        dest[i] = source[i];
    }
}

int main() {
    int src[] = {1, 2, 3, 4, 5};
    int size = sizeof(src) / sizeof(src[0]);
    int dest[5];

    copy_array(src, dest, size);

    printf("复制后的数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", dest[i]);
    }
    return 0;
}
```

**4. 查找元素**
```c
int find_element(int arr[], int size, int target) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            return i;  // 返回索引
        }
    }
    return -1;  // 未找到
}

int main() {
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    int index = find_element(numbers, size, 30);
    if (index != -1) {
        printf("找到30,位置: %d\n", index);  // 2
    } else {
        printf("未找到\n");
    }
    return 0;
}
```

**5. 冒泡排序**
```c
void bubble_sort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                // 交换
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int numbers[] = {64, 34, 25, 12, 22, 11, 90};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("排序前: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }

    bubble_sort(numbers, size);

    printf("\n排序后: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    return 0;
}
```

### 二维数组

#### 定义与初始化

**语法:**
```c
数据类型 数组名[行数][列数];
```

**示例:**

**1. 声明不初始化**
```c
int matrix[3][4];  // 3行4列
```

**2. 完全初始化**
```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};
```

**3. 按行初始化**
```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6},          // {5, 6, 0, 0}
    {9}              // {9, 0, 0, 0}
};
```

**4. 连续初始化**
```c
int matrix[3][4] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
// 按行依次填充
```

**5. 省略第一维**
```c
int matrix[][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};
// 编译器自动推导行数为3
```

#### 访问二维数组元素

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// 访问元素: matrix[行][列]
printf("%d\n", matrix[0][0]);  // 1
printf("%d\n", matrix[1][2]);  // 7
printf("%d\n", matrix[2][3]);  // 12

// 修改元素
matrix[1][1] = 100;
printf("%d\n", matrix[1][1]);  // 100
```

#### 遍历二维数组

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

int rows = sizeof(matrix) / sizeof(matrix[0]);
int cols = sizeof(matrix[0]) / sizeof(matrix[0][0]);

// 双重循环遍历
for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        printf("%3d ", matrix[i][j]);
    }
    printf("\n");
}
```

**输出:**
```
  1   2   3   4
  5   6   7   8
  9  10  11  12
```

#### 二维数组作为函数参数

**必须指定列数:**
```c
void print_matrix(int matrix[][4], int rows) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < 4; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int m[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    print_matrix(m, 3);
    return 0;
}
```

> [!important] 为什么必须指定列数?
> - 编译器需要知道列数才能计算元素地址
> - `matrix[i][j]` 的地址计算: `matrix + i * cols + j`
> - 如果不知道cols,无法计算

#### 二维数组应用示例

**1. 矩阵加法**
```c
void matrix_add(int a[][3], int b[][3], int result[][3], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

int main() {
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int b[2][3] = {{7, 8, 9}, {10, 11, 12}};
    int result[2][3];

    matrix_add(a, b, result, 2, 3);

    printf("结果矩阵:\n");
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%3d ", result[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

**2. 矩阵转置**
```c
void transpose(int matrix[][3], int result[][2], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[j][i] = matrix[i][j];
        }
    }
}

int main() {
    int m[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };
    int t[3][2];  // 转置后3x2

    transpose(m, t, 2, 3);

    printf("原矩阵:\n");
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%d ", m[i][j]);
        }
        printf("\n");
    }

    printf("\n转置后:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 2; j++) {
            printf("%d ", t[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

**3. 九九乘法表**
```c
int main() {
    int table[9][9];

    // 生成乘法表
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            table[i][j] = (i + 1) * (j + 1);
        }
    }

    // 打印乘法表
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j <= i; j++) {
            printf("%d×%d=%2d  ", j+1, i+1, table[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

### 字符数组与字符串

#### 字符数组

```c
char name[20];  // 可以存储最多19个字符(留一个给'\0')
```

#### 字符串

**在C语言中,字符串是以空字符`'\0'`结尾的字符数组。**

**初始化方式:**

**1. 字符数组初始化**
```c
char str1[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
```

**2. 字符串字面量初始化(推荐)**
```c
char str2[] = "Hello";  // 自动添加'\0',实际大小为6
```

**3. 指定大小**
```c
char str3[20] = "Hello";  // {'H','e','l','l','o','\0',0,...}
```

#### 字符串输入输出

**1. 使用scanf和printf**
```c
char name[50];
printf("请输入你的名字: ");
scanf("%s", name);  // 注意: name已经是地址,不需要&
printf("你好, %s!\n", name);
```

> [!warning] scanf的问题
> - `scanf("%s", name)` 遇到空格就停止
> - 无法读取包含空格的字符串
> - 不检查数组越界,可能导致缓冲区溢出

**2. 使用fgets(更安全)**
```c
char line[100];
printf("请输入一行文字: ");
fgets(line, sizeof(line), stdin);
printf("你输入了: %s", line);
```

**3. 使用puts**
```c
char msg[] = "Hello, World!";
puts(msg);  // 自动换行
```

#### 字符串函数(string.h)

需要包含头文件: `#include <string.h>`

**1. strlen - 获取字符串长度**
```c
char str[] = "Hello";
int len = strlen(str);  // 5 (不包括'\0')
```

**2. strcpy - 复制字符串**
```c
char src[] = "Hello";
char dest[20];
strcpy(dest, src);
printf("%s\n", dest);  // Hello
```

**3. strcat - 连接字符串**
```c
char str1[20] = "Hello";
char str2[] = " World";
strcat(str1, str2);
printf("%s\n", str1);  // Hello World
```

**4. strcmp - 比较字符串**
```c
char str1[] = "apple";
char str2[] = "banana";
int result = strcmp(str1, str2);
// result < 0: str1 < str2
// result == 0: str1 == str2
// result > 0: str1 > str2
```

**5. strchr - 查找字符**
```c
char str[] = "Hello, World!";
char *ptr = strchr(str, 'W');
if (ptr != NULL) {
    printf("找到'W',位置: %ld\n", ptr - str);  // 7
}
```

**6. strstr - 查找子串**
```c
char str[] = "Hello, World!";
char *ptr = strstr(str, "World");
if (ptr != NULL) {
    printf("找到子串: %s\n", ptr);  // World!
}
```

**安全版本(推荐):**
```c
// strncpy - 限制复制长度
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';  // 确保结尾

// strncat - 限制连接长度
strncat(str1, str2, sizeof(str1) - strlen(str1) - 1);
```

#### 字符串数组

```c
// 方式1: 二维字符数组
char names[3][20] = {
    "Alice",
    "Bob",
    "Charlie"
};

for (int i = 0; i < 3; i++) {
    printf("%s\n", names[i]);
}

// 方式2: 指针数组
char *names2[] = {
    "Alice",
    "Bob",
    "Charlie"
};

for (int i = 0; i < 3; i++) {
    printf("%s\n", names2[i]);
}
```

### 数组与指针

#### 数组名是指针

```c
int arr[] = {10, 20, 30, 40, 50};

// 数组名是指向第一个元素的指针
printf("%p\n", arr);      // 数组首地址
printf("%p\n", &arr[0]);  // 第一个元素的地址
// 两者相同

// 通过指针访问数组
int *ptr = arr;
for (int i = 0; i < 5; i++) {
    printf("%d ", *(ptr + i));  // 等价于arr[i]
}
```

#### 指针算术

```c
int arr[] = {10, 20, 30, 40, 50};
int *ptr = arr;

printf("%d\n", *ptr);       // 10
printf("%d\n", *(ptr + 1)); // 20
printf("%d\n", *(ptr + 2)); // 30

ptr++;  // 指向下一个元素
printf("%d\n", *ptr);  // 20
```

> [!note] 数组与指针的区别
> - 数组名是常量指针,不能修改
> - 指针变量可以改变指向
> ```c
> int arr[5];
> int *ptr = arr;
>
> ptr++;  // 合法
> arr++;  // 错误! 数组名不能自增
> ```

> [!tip] 更多内容
> 数组与指针的深入内容请参考 [[C语言进阶 - 指针详解]]

### 常见陷阱和错误

#### 陷阱1: 数组越界访问
```c
int arr[5] = {1, 2, 3, 4, 5};
printf("%d\n", arr[5]);   // 越界!未定义行为
printf("%d\n", arr[-1]);  // 越界!未定义行为

// C语言不检查数组边界!程序员必须自己确保
```

#### 陷阱2: 未初始化数组
```c
int arr[100];  // 未初始化,包含随机值!

// 正确做法
int arr[100] = {0};  // 全部初始化为0
```

#### 陷阱3: sizeof在函数参数中失效
```c
void print_size(int arr[]) {
    printf("%zu\n", sizeof(arr));  // 只返回指针大小!
}

int main() {
    int numbers[10];
    printf("%zu\n", sizeof(numbers));  // 40 (10 * 4)
    print_size(numbers);  // 8 (64位系统指针大小)
    return 0;
}
```

#### 陷阱4: 数组赋值
```c
int arr1[5] = {1, 2, 3, 4, 5};
int arr2[5];

// arr2 = arr1;  // 错误!数组名是常量,不能赋值

// 正确做法:逐元素复制
for (int i = 0; i < 5; i++) {
    arr2[i] = arr1[i];
}

// 或使用memcpy
memcpy(arr2, arr1, sizeof(arr1));
```

#### 陷阱5: 返回局部数组
```c
// 危险!
int* get_array() {
    int arr[10] = {1, 2, 3};
    return arr;  // 返回栈上数组地址,函数结束后失效!
}

// 正确做法1:静态数组
int* get_array_static() {
    static int arr[10] = {1, 2, 3};
    return arr;  // 静态数组生命周期是整个程序
}

// 正确做法2:动态分配
int* get_array_dynamic() {
    int *arr = (int*)malloc(10 * sizeof(int));
    // 初始化...
    return arr;  // 调用者需要free
}
```

### 最佳实践

#### 1. 总是传递数组大小
```c
void process_array(int arr[], int size) {  // 明确传递size
    for (int i = 0; i < size; i++) {
        // 处理arr[i]
    }
}
```

#### 2. 使用const保护只读数组
```c
int sum_array(const int arr[], int size) {
    // arr[0] = 10;  // 编译错误,不能修改
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];  // 只读访问OK
    }
    return sum;
}
```

#### 3. 检查数组边界
```c
int safe_get(int arr[], int size, int index) {
    if (index < 0 || index >= size) {
        fprintf(stderr, "索引越界: %d\n", index);
        return -1;  // 或返回错误码
    }
    return arr[index];
}
```

#### 4. 使用宏简化数组操作
```c
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

int numbers[] = {1, 2, 3, 4, 5};
int size = ARRAY_SIZE(numbers);  // 5
```

#### 5. 字符串安全操作
```c
// 不安全
char str[10];
strcpy(str, "This is a very long string");  // 缓冲区溢出!

// 安全
char str[10];
strncpy(str, "This is a very long string", sizeof(str) - 1);
str[sizeof(str) - 1] = '\0';  // 确保以\0结尾
```

### 高级数组技巧

#### 变长数组(C99)
```c
#include <stdio.h>

void print_matrix(int rows, int cols, int matrix[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int rows = 3, cols = 4;
    int matrix[rows][cols];  // VLA (Variable Length Array)

    // 初始化
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i * cols + j;
        }
    }

    print_matrix(rows, cols, matrix);
    return 0;
}
```

#### 数组与指针的等价性
```c
int arr[] = {10, 20, 30, 40, 50};

// 以下都是等价的
printf("%d\n", arr[2]);      // 30
printf("%d\n", *(arr + 2));  // 30
printf("%d\n", *(2 + arr));  // 30
printf("%d\n", 2[arr]);      // 30 (奇怪但合法!)
```

### 实战项目示例

#### 项目1: 动态数组实现
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int *data;
    int size;
    int capacity;
} DynamicArray;

// 初始化
DynamicArray* da_create(int initial_capacity) {
    DynamicArray *da = (DynamicArray*)malloc(sizeof(DynamicArray));
    da->data = (int*)malloc(initial_capacity * sizeof(int));
    da->size = 0;
    da->capacity = initial_capacity;
    return da;
}

// 添加元素
void da_push(DynamicArray *da, int value) {
    if (da->size >= da->capacity) {
        // 扩容(2倍)
        da->capacity *= 2;
        da->data = (int*)realloc(da->data, da->capacity * sizeof(int));
    }
    da->data[da->size++] = value;
}

// 获取元素
int da_get(DynamicArray *da, int index) {
    if (index < 0 || index >= da->size) {
        fprintf(stderr, "索引越界\n");
        return -1;
    }
    return da->data[index];
}

// 删除元素
void da_remove(DynamicArray *da, int index) {
    if (index < 0 || index >= da->size) {
        return;
    }

    // 移动元素
    for (int i = index; i < da->size - 1; i++) {
        da->data[i] = da->data[i + 1];
    }
    da->size--;
}

// 销毁
void da_destroy(DynamicArray *da) {
    free(da->data);
    free(da);
}

int main() {
    DynamicArray *da = da_create(2);

    // 添加元素
    for (int i = 0; i < 10; i++) {
        da_push(da, i * 10);
    }

    // 打印
    printf("元素: ");
    for (int i = 0; i < da->size; i++) {
        printf("%d ", da_get(da, i));
    }
    printf("\n");

    // 删除
    da_remove(da, 5);
    printf("删除后: ");
    for (int i = 0; i < da->size; i++) {
        printf("%d ", da_get(da, i));
    }
    printf("\n");

    da_destroy(da);
    return 0;
}
```

#### 项目2: 矩阵运算库
```c
#include <stdio.h>
#include <stdlib.h>

// 矩阵加法
void matrix_add(int rows, int cols,
                int a[rows][cols],
                int b[rows][cols],
                int result[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

// 矩阵乘法
void matrix_multiply(int m, int n, int p,
                     int a[m][n],
                     int b[n][p],
                     int result[m][p]) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            result[i][j] = 0;
            for (int k = 0; k < n; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

// 打印矩阵
void print_matrix(int rows, int cols, int matrix[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%4d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int b[3][2] = {{7, 8}, {9, 10}, {11, 12}};
    int result[2][2];

    printf("矩阵A (2x3):\n");
    print_matrix(2, 3, a);

    printf("\n矩阵B (3x2):\n");
    print_matrix(3, 2, b);

    matrix_multiply(2, 3, 2, a, b, result);

    printf("\nA × B (2x2):\n");
    print_matrix(2, 2, result);

    return 0;
}
```

#### 项目3: 简单的图像处理(灰度图)
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WIDTH 10
#define HEIGHT 10

typedef unsigned char Pixel;  // 0-255

// 创建图像
void image_create(Pixel image[HEIGHT][WIDTH], Pixel value) {
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            image[i][j] = value;
        }
    }
}

// 绘制矩形
void image_draw_rect(Pixel image[HEIGHT][WIDTH],
                     int x, int y, int w, int h, Pixel value) {
    for (int i = y; i < y + h && i < HEIGHT; i++) {
        for (int j = x; j < x + w && j < WIDTH; j++) {
            image[i][j] = value;
        }
    }
}

// 反转颜色
void image_invert(Pixel image[HEIGHT][WIDTH]) {
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            image[i][j] = 255 - image[i][j];
        }
    }
}

// 显示图像(ASCII)
void image_display(Pixel image[HEIGHT][WIDTH]) {
    const char *chars = " .:-=+*#%@";
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            int index = image[i][j] * 10 / 256;
            printf("%c", chars[index]);
        }
        printf("\n");
    }
}

int main() {
    Pixel image[HEIGHT][WIDTH];

    // 创建黑色图像
    image_create(image, 0);

    // 绘制矩形
    image_draw_rect(image, 2, 2, 6, 6, 128);
    image_draw_rect(image, 4, 4, 2, 2, 255);

    printf("原图像:\n");
    image_display(image);

    // 反转
    image_invert(image);

    printf("\n反转后:\n");
    image_display(image);

    return 0;
}
```

---

## 🤔 Q&A

### Q1: 数组下标为什么从0开始?
**A**: 历史和效率原因:
- `arr[i]` 实际上是 `*(arr + i)` 的语法糖
- `arr[0]` 就是 `*(arr + 0)`,即数组首地址
- 这样设计使得地址计算最简单高效

### Q2: 如何避免数组越界?
**A**:
1. 使用常量定义数组大小
2. 循环时使用`<`而不是`<=`
3. 使用`sizeof`计算数组大小
4. 启用编译器警告
5. 使用静态分析工具

```c
#define SIZE 10
int arr[SIZE];

for (int i = 0; i < SIZE; i++) {  // 正确
    arr[i] = i;
}
```

### Q3: 如何从函数返回数组?
**A**: C语言不能直接返回数组,但可以:
1. 返回指向动态分配数组的指针
2. 使用输出参数
3. 使用结构体包装数组

```c
// 方法1: 动态分配
int* create_array(int size) {
    int *arr = (int*)malloc(size * sizeof(int));
    return arr;
}

// 方法2: 输出参数
void fill_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = i;
    }
}
```

### Q4: 为什么传递数组需要同时传递大小?
**A**: 因为数组传递给函数时退化为指针,sizeof无法获取数组大小:
```c
void func(int arr[]) {
    // sizeof(arr) 得到的是指针大小(4或8字节)
    // 而不是数组大小
}
```

### Q5: 字符数组和字符指针有什么区别?
**A**:
```c
char arr[] = "Hello";   // 字符数组,可修改
char *ptr = "Hello";    // 指向字符串字面量,不可修改

arr[0] = 'h';  // 合法
ptr[0] = 'h';  // 运行时错误! 字符串字面量在只读内存
```

## 🚀 Tasks

### 基础练习
- [ ] 编写程序找出数组中的第二大值
- [ ] 实现选择排序和插入排序算法
- [ ] 数组元素的反转和旋转
- [ ] 统计数组中每个元素出现的次数
- [ ] 实现数组的合并和去重

### 二维数组练习
- [ ] 编写程序实现矩阵乘法
- [ ] 实现矩阵转置
- [ ] 打印螺旋矩阵
- [ ] 实现二维数组的查找算法
- [ ] 编写程序计算矩阵的行列式

### 字符串练习
- [ ] 实现一个函数统计字符串中各字符出现次数
- [ ] 编写字符串比较函数(不用strcmp)
- [ ] 实现字符串分割函数
- [ ] 回文字符串检测
- [ ] 最长公共子序列

### 实战项目
- [x] 动态数组实现(类似vector)
- [x] 矩阵运算库
- [x] 简单的图像处理
- [ ] 字符串处理工具集
- [ ] 简单的电子表格程序
- [ ] 文本编辑器缓冲区

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C和指针 - Kenneth A. Reek

## 🕸️ Relation
* [[00_C_MOC]] - C语言知识体系
* [[C语言基础 - 数据类型与变量]] - 数组是同类型数据的集合
* [[C语言基础 - 控制流]] - 循环用于遍历数组
* [[C语言基础 - 函数]] - 函数用于处理数组
* [[C语言进阶 - 指针详解]] - 深入理解数组与指针的关系
* [[C语言进阶 - 字符串]] - 字符串是特殊的字符数组
