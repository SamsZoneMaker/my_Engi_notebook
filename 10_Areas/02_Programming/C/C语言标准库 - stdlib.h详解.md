---
tags:
  - "#domain/programming"
  - "#type/reference"
  - "#level/intermediate"
  - "#lang/c"
  - "#grain/stdlib"
  - "#tech/memory"
status: 完成
complexity: 中级
notetype: 技术参考
resource: C标准库文档
related:
  - "[[C语言标准库 - stdio.h详解]]"
  - "[[C语言标准库 - string.h详解]]"
  - "[[C语言进阶 - 指针详解]]"
created: 2025-11-18
modified: 2025-11-18
---

# C语言标准库 - stdlib.h详解

## 📋 概述

`stdlib.h` 是C标准库中最重要的头文件之一，提供了通用工具函数，包括：
- **动态内存管理** (malloc, calloc, realloc, free)
- **程序控制** (exit, abort, atexit)
- **字符串转换** (atoi, atof, strtol, strtod)
- **随机数生成** (rand, srand)
- **搜索和排序** (qsort, bsort)
- **环境访问** (getenv, system)
- **整数运算** (abs, labs, div)

---

## 🎯 学习目标

- [ ] 掌握动态内存分配和释放
- [ ] 理解内存泄漏和悬空指针的危险
- [ ] 学会使用字符串转换函数
- [ ] 掌握随机数生成
- [ ] 理解qsort通用排序算法
- [ ] 学会安全地调用系统命令

---

## 📚 核心内容

### 1. 重要宏定义

```c
NULL        // 空指针常量
EXIT_SUCCESS // 成功退出状态码 (通常为0)
EXIT_FAILURE // 失败退出状态码 (通常为1)
RAND_MAX    // rand()函数的最大返回值 (至少32767)
MB_CUR_MAX  // 当前locale的多字节字符最大字节数
```

### 2. 重要类型定义

```c
size_t      // 无符号整数类型，用于表示大小
div_t       // div()函数返回的结构体类型
ldiv_t      // ldiv()函数返回的结构体类型
```

---

## 🔧 函数详解

### 一、动态内存管理 ⭐⭐⭐⭐⭐

#### 1. malloc() - 分配内存

```c
void *malloc(size_t size);
```

**功能**：分配指定大小的内存块，返回指向该内存的指针。

**参数**：
- `size`：要分配的字节数

**返回值**：
- 成功：返回指向分配内存的指针（未初始化）
- 失败：返回 `NULL`

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 分配10个int的内存
    int *arr = (int *)malloc(10 * sizeof(int));

    if (arr == NULL) {
        fprintf(stderr, "内存分配失败\n");
        return EXIT_FAILURE;
    }

    // 使用内存
    for (int i = 0; i < 10; i++) {
        arr[i] = i * 2;
        printf("%d ", arr[i]);
    }
    printf("\n");

    // 释放内存
    free(arr);
    arr = NULL;  // 防止悬空指针

    return EXIT_SUCCESS;
}
```

**⚠️ 注意事项**：
- malloc不初始化内存，内容是未定义的
- 必须检查返回值是否为NULL
- 使用后必须调用free释放
- free后应将指针设为NULL

#### 2. calloc() - 分配并清零内存

```c
void *calloc(size_t nmemb, size_t size);
```

**功能**：分配内存并将所有字节初始化为0。

**参数**：
- `nmemb`：元素个数
- `size`：每个元素的字节数

**返回值**：同malloc

**示例**：

```c
// 分配并初始化为0
int *arr = (int *)calloc(10, sizeof(int));

if (arr == NULL) {
    fprintf(stderr, "内存分配失败\n");
    return EXIT_FAILURE;
}

// 所有元素已经是0
for (int i = 0; i < 10; i++) {
    printf("%d ", arr[i]);  // 输出: 0 0 0 0 0 0 0 0 0 0
}

free(arr);
```

**malloc vs calloc**：
```c
// 等价操作
int *p1 = (int *)malloc(10 * sizeof(int));

int *p2 = (int *)calloc(10, sizeof(int));

// 或者用malloc + memset
int *p3 = (int *)malloc(10 * sizeof(int));
memset(p3, 0, 10 * sizeof(int));
```

#### 3. realloc() - 重新分配内存

```c
void *realloc(void *ptr, size_t size);
```

**功能**：改变已分配内存块的大小。

**参数**：
- `ptr`：原内存块指针（如果为NULL，行为等同malloc）
- `size`：新的大小（如果为0，行为等同free）

**返回值**：
- 成功：返回新内存块的指针（可能与原指针不同）
- 失败：返回NULL，原内存块不变

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 初始分配5个int
    int *arr = (int *)malloc(5 * sizeof(int));
    if (arr == NULL) return EXIT_FAILURE;

    // 初始化
    for (int i = 0; i < 5; i++) {
        arr[i] = i;
    }

    // 扩展到10个int
    int *temp = (int *)realloc(arr, 10 * sizeof(int));
    if (temp == NULL) {
        // realloc失败，原内存仍然有效
        free(arr);
        return EXIT_FAILURE;
    }

    arr = temp;  // 更新指针

    // 初始化新增部分
    for (int i = 5; i < 10; i++) {
        arr[i] = i;
    }

    // 打印所有元素
    for (int i = 0; i < 10; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    free(arr);
    return EXIT_SUCCESS;
}
```

**⚠️ realloc陷阱**：

```c
// ❌ 错误用法 - 可能导致内存泄漏
arr = (int *)realloc(arr, new_size);
// 如果realloc失败，arr变成NULL，原内存丢失

// ✅ 正确用法
int *temp = (int *)realloc(arr, new_size);
if (temp == NULL) {
    // 处理错误，arr仍然有效
    free(arr);
    return EXIT_FAILURE;
}
arr = temp;
```

#### 4. free() - 释放内存

```c
void free(void *ptr);
```

**功能**：释放之前通过malloc/calloc/realloc分配的内存。

**参数**：
- `ptr`：要释放的内存指针（可以是NULL，此时不执行任何操作）

**返回值**：无

**示例**：

```c
int *p = (int *)malloc(sizeof(int));
if (p != NULL) {
    *p = 42;
    free(p);
    p = NULL;  // 良好习惯：防止悬空指针
}

free(NULL);  // 安全，不会有任何问题
```

**⚠️ 常见内存错误**：

```c
// 1. 内存泄漏 - 忘记释放
void memory_leak() {
    int *p = (int *)malloc(100 * sizeof(int));
    // 忘记free(p)
    return;  // 内存泄漏！
}

// 2. 悬空指针 - 使用已释放的内存
int *p = (int *)malloc(sizeof(int));
free(p);
*p = 10;  // ❌ 未定义行为！

// 3. 重复释放
free(p);
free(p);  // ❌ 未定义行为！

// 4. 释放非堆内存
int x = 10;
free(&x);  // ❌ 严重错误！
```

**✅ 最佳实践**：

```c
// 封装安全的free
#define SAFE_FREE(p) do { free(p); (p) = NULL; } while(0)

int *p = (int *)malloc(sizeof(int));
SAFE_FREE(p);
SAFE_FREE(p);  // 第二次调用安全（free(NULL)）
```

---

### 二、程序控制

#### 1. exit() - 正常终止程序

```c
void exit(int status);
```

**功能**：正常终止程序执行。

**参数**：
- `status`：退出状态码（0或EXIT_SUCCESS表示成功，非0或EXIT_FAILURE表示失败）

**行为**：
1. 调用所有通过atexit注册的函数（后进先出顺序）
2. 刷新所有打开的缓冲流
3. 关闭所有打开的流
4. 删除tmpfile创建的临时文件
5. 返回状态码给操作系统

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp = fopen("data.txt", "r");

    if (fp == NULL) {
        fprintf(stderr, "无法打开文件\n");
        exit(EXIT_FAILURE);  // 退出程序，返回失败状态
    }

    // 处理文件...

    fclose(fp);
    exit(EXIT_SUCCESS);  // 正常退出
}
```

#### 2. atexit() - 注册退出处理函数

```c
int atexit(void (*function)(void));
```

**功能**：注册在程序正常终止时调用的函数。

**参数**：
- `function`：要注册的函数指针（无参数，无返回值）

**返回值**：
- 成功：0
- 失败：非0

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

void cleanup1(void) {
    printf("清理函数1被调用\n");
}

void cleanup2(void) {
    printf("清理函数2被调用\n");
}

void cleanup3(void) {
    printf("清理函数3被调用\n");
}

int main() {
    // 注册多个清理函数
    atexit(cleanup1);
    atexit(cleanup2);
    atexit(cleanup3);

    printf("主程序运行\n");

    return 0;  // 或者 exit(0)

    // 输出顺序（后进先出）：
    // 主程序运行
    // 清理函数3被调用
    // 清理函数2被调用
    // 清理函数1被调用
}
```

**实际应用**：

```c
#include <stdio.h>
#include <stdlib.h>

FILE *log_file = NULL;

void close_log(void) {
    if (log_file != NULL) {
        fprintf(log_file, "程序正常退出\n");
        fclose(log_file);
        printf("日志文件已关闭\n");
    }
}

int main() {
    log_file = fopen("app.log", "a");
    if (log_file == NULL) {
        return EXIT_FAILURE;
    }

    // 注册退出时自动关闭日志文件
    atexit(close_log);

    fprintf(log_file, "程序启动\n");

    // 程序的其他逻辑...

    return EXIT_SUCCESS;  // close_log会自动被调用
}
```

#### 3. abort() - 异常终止程序

```c
void abort(void);
```

**功能**：异常终止程序，不执行清理工作。

**特点**：
- 不调用atexit注册的函数
- 不刷新缓冲区
- 发送SIGABRT信号
- 生成core dump（如果系统配置允许）

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

void critical_error(const char *msg) {
    fprintf(stderr, "致命错误: %s\n", msg);
    abort();  // 立即终止
}

int main() {
    int *p = (int *)malloc(1000000000000);  // 巨大的分配

    if (p == NULL) {
        critical_error("无法分配内存");
    }

    free(p);
    return 0;
}
```

**exit vs abort**：

| 特性 | exit() | abort() |
|------|--------|---------|
| 调用atexit函数 | ✅ 是 | ❌ 否 |
| 刷新缓冲区 | ✅ 是 | ❌ 否 |
| 关闭文件 | ✅ 是 | ❌ 否 |
| 生成core dump | ❌ 否 | ✅ 是 |
| 用途 | 正常退出 | 异常退出 |

---

### 三、字符串转换

#### 1. atoi/atol/atoll - 字符串转整数

```c
int atoi(const char *nptr);
long atol(const char *nptr);
long long atoll(const char *nptr);  // C99
```

**功能**：将字符串转换为整数。

**参数**：
- `nptr`：要转换的字符串

**返回值**：
- 转换后的整数
- 转换失败返回0（⚠️ 无法区分真正的0和错误）

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    char *str1 = "12345";
    char *str2 = "-6789";
    char *str3 = "  42  ";      // 前导空格会被忽略
    char *str4 = "123abc";      // 只转换数字部分
    char *str5 = "abc123";      // 返回0

    printf("%d\n", atoi(str1));  // 12345
    printf("%d\n", atoi(str2));  // -6789
    printf("%d\n", atoi(str3));  // 42
    printf("%d\n", atoi(str4));  // 123
    printf("%d\n", atoi(str5));  // 0 (无法区分是错误还是真的0)

    return 0;
}
```

**⚠️ atoi的问题**：
- 无法检测转换错误
- 溢出时行为未定义
- 不推荐在新代码中使用

#### 2. strtol/strtoll - 安全的字符串转整数 ⭐⭐⭐

```c
long strtol(const char *nptr, char **endptr, int base);
long long strtoll(const char *nptr, char **endptr, int base);
unsigned long strtoul(const char *nptr, char **endptr, int base);
```

**功能**：将字符串转换为整数，提供错误检测。

**参数**：
- `nptr`：要转换的字符串
- `endptr`：存储第一个无法转换字符的位置（可以为NULL）
- `base`：进制数（0表示自动检测，2-36为具体进制）

**返回值**：
- 成功：转换后的整数
- 溢出：LONG_MAX或LONG_MIN，并设置errno为ERANGE
- 无法转换：返回0

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int main() {
    char *str = "12345abc";
    char *endptr;

    // 基本转换
    long num = strtol(str, &endptr, 10);
    printf("转换结果: %ld\n", num);           // 12345
    printf("剩余字符: %s\n", endptr);         // abc

    // 检查是否完全转换
    if (*endptr != '\0') {
        printf("警告: 字符串未完全转换\n");
    }

    // 不同进制
    printf("二进制'1010': %ld\n", strtol("1010", NULL, 2));    // 10
    printf("八进制'755': %ld\n", strtol("755", NULL, 8));      // 493
    printf("十六进制'FF': %ld\n", strtol("FF", NULL, 16));     // 255
    printf("自动检测'0xFF': %ld\n", strtol("0xFF", NULL, 0));  // 255

    // 错误检测
    errno = 0;
    char *overflow_str = "99999999999999999999";
    long overflow_num = strtol(overflow_str, NULL, 10);

    if (errno == ERANGE) {
        printf("溢出检测: 数值超出范围\n");
        printf("返回值: %ld (LONG_MAX)\n", overflow_num);
    }

    return 0;
}
```

**✅ 最佳实践 - 完整错误检查**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int safe_strtol(const char *str, long *result) {
    char *endptr;
    errno = 0;

    long val = strtol(str, &endptr, 10);

    // 检查各种错误情况
    if (endptr == str) {
        fprintf(stderr, "错误: 没有数字可转换\n");
        return -1;
    }

    if (*endptr != '\0') {
        fprintf(stderr, "错误: 字符串包含非数字字符: %s\n", endptr);
        return -1;
    }

    if (errno == ERANGE && (val == LONG_MAX || val == LONG_MIN)) {
        fprintf(stderr, "错误: 数值溢出\n");
        return -1;
    }

    *result = val;
    return 0;  // 成功
}

int main() {
    long num;

    if (safe_strtol("12345", &num) == 0) {
        printf("成功: %ld\n", num);
    }

    if (safe_strtol("abc", &num) != 0) {
        printf("转换失败\n");
    }

    return 0;
}
```

#### 3. atof/strtod - 字符串转浮点数

```c
double atof(const char *nptr);
double strtod(const char *nptr, char **endptr);
float strtof(const char *nptr, char **endptr);  // C99
```

**功能**：将字符串转换为浮点数。

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // atof - 简单但不安全
    printf("%f\n", atof("3.14159"));        // 3.141590
    printf("%f\n", atof("-2.5e3"));         // -2500.000000
    printf("%f\n", atof("  1.23  "));       // 1.230000

    // strtod - 安全，带错误检测
    char *str = "123.45abc";
    char *endptr;
    double num = strtod(str, &endptr);

    printf("转换结果: %f\n", num);          // 123.450000
    printf("剩余字符: %s\n", endptr);       // abc

    // 科学计数法
    printf("%f\n", strtod("1.5e-3", NULL)); // 0.001500

    return 0;
}
```

---

### 四、随机数生成

#### 1. rand() - 生成伪随机数

```c
int rand(void);
```

**功能**：生成0到RAND_MAX之间的伪随机数。

**返回值**：0到RAND_MAX之间的整数（RAND_MAX至少为32767）

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 生成10个随机数
    for (int i = 0; i < 10; i++) {
        printf("%d ", rand());
    }
    printf("\n");

    // 生成0-9的随机数
    for (int i = 0; i < 10; i++) {
        printf("%d ", rand() % 10);
    }
    printf("\n");

    // 生成1-100的随机数
    for (int i = 0; i < 10; i++) {
        printf("%d ", rand() % 100 + 1);
    }
    printf("\n");

    return 0;
}
```

**⚠️ 注意**：每次运行程序，rand()生成的序列相同！

#### 2. srand() - 设置随机数种子

```c
void srand(unsigned int seed);
```

**功能**：设置rand()的种子，使每次运行产生不同的随机序列。

**参数**：
- `seed`：随机数种子（通常使用time(NULL)）

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // 使用当前时间作为种子
    srand(time(NULL));

    // 现在每次运行产生不同的序列
    for (int i = 0; i < 10; i++) {
        printf("%d ", rand() % 100);
    }
    printf("\n");

    return 0;
}
```

**✅ 生成指定范围随机数的最佳实践**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// 生成[min, max]范围的随机整数
int random_range(int min, int max) {
    return min + rand() % (max - min + 1);
}

// 生成[0, 1]范围的随机浮点数
double random_double() {
    return (double)rand() / (double)RAND_MAX;
}

// 生成[min, max]范围的随机浮点数
double random_double_range(double min, double max) {
    return min + (max - min) * random_double();
}

int main() {
    srand(time(NULL));

    // 生成1-100的随机整数
    printf("随机整数(1-100): %d\n", random_range(1, 100));

    // 生成0-1的随机浮点数
    printf("随机浮点数(0-1): %f\n", random_double());

    // 生成-5.0到5.0的随机浮点数
    printf("随机浮点数(-5.0到5.0): %f\n", random_double_range(-5.0, 5.0));

    return 0;
}
```

**⚠️ rand()的模运算偏差问题**：

```c
// ❌ 有偏差的方法（当RAND_MAX不是范围的整数倍时）
int biased = rand() % 10;

// ✅ 无偏差的方法（拒绝-重采样）
int unbiased_random(int max) {
    int divisor = RAND_MAX / (max + 1);
    int result;

    do {
        result = rand() / divisor;
    } while (result > max);

    return result;
}
```

---

### 五、搜索和排序

#### 1. qsort() - 快速排序 ⭐⭐⭐⭐

```c
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void *, const void *));
```

**功能**：对数组进行排序（使用快速排序算法）。

**参数**：
- `base`：数组首地址
- `nmemb`：元素个数
- `size`：每个元素的大小
- `compar`：比较函数指针

**比较函数**：
- 返回负数：第一个元素小于第二个
- 返回0：两个元素相等
- 返回正数：第一个元素大于第二个

**示例1 - 整数排序**：

```c
#include <stdio.h>
#include <stdlib.h>

// 升序比较函数
int compare_int_asc(const void *a, const void *b) {
    int arg1 = *(const int *)a;
    int arg2 = *(const int *)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;

    // 或简化为：
    // return arg1 - arg2;  // 注意溢出风险！
}

// 降序比较函数
int compare_int_desc(const void *a, const void *b) {
    return compare_int_asc(b, a);  // 反向比较
}

int main() {
    int arr[] = {5, 2, 9, 1, 5, 6};
    int n = sizeof(arr) / sizeof(arr[0]);

    // 升序排序
    qsort(arr, n, sizeof(int), compare_int_asc);

    printf("升序: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");  // 输出: 1 2 5 5 6 9

    // 降序排序
    qsort(arr, n, sizeof(int), compare_int_desc);

    printf("降序: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");  // 输出: 9 6 5 5 2 1

    return 0;
}
```

**示例2 - 字符串排序**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 字符串比较函数
int compare_string(const void *a, const void *b) {
    // a和b是指向char*的指针
    const char *str1 = *(const char **)a;
    const char *str2 = *(const char **)b;
    return strcmp(str1, str2);
}

int main() {
    char *fruits[] = {"banana", "apple", "orange", "grape", "mango"};
    int n = sizeof(fruits) / sizeof(fruits[0]);

    qsort(fruits, n, sizeof(char *), compare_string);

    printf("排序后的水果:\n");
    for (int i = 0; i < n; i++) {
        printf("%s\n", fruits[i]);
    }
    // 输出:
    // apple
    // banana
    // grape
    // mango
    // orange

    return 0;
}
```

**示例3 - 结构体排序**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[50];
    int age;
    double score;
} Student;

// 按年龄排序
int compare_by_age(const void *a, const void *b) {
    const Student *s1 = (const Student *)a;
    const Student *s2 = (const Student *)b;
    return s1->age - s2->age;
}

// 按成绩排序（降序）
int compare_by_score(const void *a, const void *b) {
    const Student *s1 = (const Student *)a;
    const Student *s2 = (const Student *)b;

    if (s1->score < s2->score) return 1;
    if (s1->score > s2->score) return -1;
    return 0;
}

// 按姓名排序
int compare_by_name(const void *a, const void *b) {
    const Student *s1 = (const Student *)a;
    const Student *s2 = (const Student *)b;
    return strcmp(s1->name, s2->name);
}

void print_students(Student *students, int n) {
    for (int i = 0; i < n; i++) {
        printf("%-10s  年龄:%2d  成绩:%.1f\n",
               students[i].name, students[i].age, students[i].score);
    }
    printf("\n");
}

int main() {
    Student students[] = {
        {"Alice", 20, 85.5},
        {"Bob", 19, 92.0},
        {"Charlie", 21, 78.5},
        {"David", 20, 88.0}
    };
    int n = sizeof(students) / sizeof(students[0]);

    printf("原始数据:\n");
    print_students(students, n);

    // 按年龄排序
    qsort(students, n, sizeof(Student), compare_by_age);
    printf("按年龄排序:\n");
    print_students(students, n);

    // 按成绩排序
    qsort(students, n, sizeof(Student), compare_by_score);
    printf("按成绩排序(降序):\n");
    print_students(students, n);

    // 按姓名排序
    qsort(students, n, sizeof(Student), compare_by_name);
    printf("按姓名排序:\n");
    print_students(students, n);

    return 0;
}
```

#### 2. bsearch() - 二分查找

```c
void *bsearch(const void *key, const void *base, size_t nmemb,
              size_t size, int (*compar)(const void *, const void *));
```

**功能**：在已排序数组中进行二分查找。

**参数**：
- `key`：要查找的键值
- `base`：数组首地址
- `nmemb`：元素个数
- `size`：每个元素的大小
- `compar`：比较函数（与qsort使用相同的比较函数）

**返回值**：
- 找到：返回指向匹配元素的指针
- 未找到：返回NULL

**⚠️ 前提条件**：数组必须已经排序！

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int compare_int(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

int main() {
    int arr[] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
    int n = sizeof(arr) / sizeof(arr[0]);

    // 查找元素7
    int key = 7;
    int *result = (int *)bsearch(&key, arr, n, sizeof(int), compare_int);

    if (result != NULL) {
        printf("找到元素 %d, 位置: %ld\n", *result, result - arr);
    } else {
        printf("未找到元素 %d\n", key);
    }

    // 查找不存在的元素
    key = 8;
    result = (int *)bsearch(&key, arr, n, sizeof(int), compare_int);

    if (result == NULL) {
        printf("未找到元素 %d\n", key);
    }

    return 0;
}
```

---

### 六、环境访问

#### 1. getenv() - 获取环境变量

```c
char *getenv(const char *name);
```

**功能**：获取环境变量的值。

**参数**：
- `name`：环境变量名

**返回值**：
- 成功：指向环境变量值的指针
- 失败：NULL

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 获取常见环境变量
    char *path = getenv("PATH");
    if (path != NULL) {
        printf("PATH = %s\n", path);
    }

    char *home = getenv("HOME");
    if (home != NULL) {
        printf("HOME = %s\n", home);
    }

    char *user = getenv("USER");
    if (user != NULL) {
        printf("USER = %s\n", user);
    }

    // 检查不存在的环境变量
    char *custom = getenv("MY_CUSTOM_VAR");
    if (custom == NULL) {
        printf("MY_CUSTOM_VAR 未设置\n");
    }

    return 0;
}
```

**⚠️ 注意**：
- 返回的字符串不应被修改
- 返回的指针可能在下次调用getenv或程序修改环境时失效

#### 2. system() - 执行系统命令

```c
int system(const char *command);
```

**功能**：执行shell命令。

**参数**：
- `command`：要执行的命令字符串（NULL时检查shell是否可用）

**返回值**：
- command为NULL：shell可用返回非0，不可用返回0
- command非NULL：命令的退出状态

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 检查shell是否可用
    if (system(NULL)) {
        printf("命令处理器可用\n");
    } else {
        printf("命令处理器不可用\n");
        return EXIT_FAILURE;
    }

    // 执行简单命令
    printf("列出当前目录:\n");
    system("ls -l");

    // 执行多个命令
    system("echo '开始备份' && cp file.txt file.bak && echo '备份完成'");

    // 检查命令执行状态
    int ret = system("gcc program.c -o program");
    if (ret == 0) {
        printf("编译成功\n");
    } else {
        printf("编译失败，返回值: %d\n", ret);
    }

    return 0;
}
```

**⚠️ 安全警告**：

```c
// ❌ 危险！容易受到命令注入攻击
char filename[100];
char command[200];
scanf("%s", filename);
sprintf(command, "rm %s", filename);
system(command);  // 如果用户输入 "file.txt; rm -rf /", 后果严重！

// ✅ 更安全的方法：验证输入
#include <ctype.h>

int is_safe_filename(const char *name) {
    for (int i = 0; name[i]; i++) {
        if (!isalnum(name[i]) && name[i] != '.' && name[i] != '_' && name[i] != '-') {
            return 0;
        }
    }
    return 1;
}

char filename[100];
scanf("%s", filename);

if (!is_safe_filename(filename)) {
    fprintf(stderr, "非法文件名\n");
    return EXIT_FAILURE;
}

char command[200];
snprintf(command, sizeof(command), "rm %s", filename);
system(command);
```

**最佳实践**：尽量避免使用system()，优先使用专门的系统调用（如fork/exec）。

---

### 七、整数运算

#### 1. abs/labs/llabs - 绝对值

```c
int abs(int x);
long labs(long x);
long long llabs(long long x);  // C99
```

**功能**：计算整数的绝对值。

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("%d\n", abs(-42));      // 42
    printf("%ld\n", labs(-123L));  // 123
    printf("%d\n", abs(10));       // 10

    // ⚠️ 注意溢出
    int min_int = -2147483648;  // INT_MIN on 32-bit
    printf("%d\n", abs(min_int));  // 未定义行为！溢出

    return 0;
}
```

#### 2. div/ldiv - 除法运算

```c
div_t div(int numer, int denom);
ldiv_t ldiv(long numer, long denom);

typedef struct {
    int quot;  // 商
    int rem;   // 余数
} div_t;
```

**功能**：同时计算商和余数。

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    div_t result = div(17, 5);

    printf("17 / 5 = %d 余 %d\n", result.quot, result.rem);
    // 输出: 17 / 5 = 3 余 2

    // 负数除法
    result = div(-17, 5);
    printf("-17 / 5 = %d 余 %d\n", result.quot, result.rem);
    // 输出: -17 / 5 = -3 余 -2

    result = div(17, -5);
    printf("17 / -5 = %d 余 %d\n", result.quot, result.rem);
    // 输出: 17 / -5 = -3 余 2

    return 0;
}
```

---

## 📝 实战示例

### 示例1：动态数组实现

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} DynamicArray;

// 创建动态数组
DynamicArray *create_array(size_t initial_capacity) {
    DynamicArray *arr = (DynamicArray *)malloc(sizeof(DynamicArray));
    if (arr == NULL) return NULL;

    arr->data = (int *)malloc(initial_capacity * sizeof(int));
    if (arr->data == NULL) {
        free(arr);
        return NULL;
    }

    arr->size = 0;
    arr->capacity = initial_capacity;

    return arr;
}

// 添加元素
int push_back(DynamicArray *arr, int value) {
    if (arr->size >= arr->capacity) {
        // 扩容（容量翻倍）
        size_t new_capacity = arr->capacity * 2;
        int *new_data = (int *)realloc(arr->data, new_capacity * sizeof(int));

        if (new_data == NULL) {
            return -1;  // 扩容失败
        }

        arr->data = new_data;
        arr->capacity = new_capacity;
        printf("扩容: %zu -> %zu\n", arr->capacity / 2, arr->capacity);
    }

    arr->data[arr->size++] = value;
    return 0;
}

// 销毁数组
void destroy_array(DynamicArray *arr) {
    if (arr != NULL) {
        free(arr->data);
        free(arr);
    }
}

// 打印数组
void print_array(DynamicArray *arr) {
    printf("Array (size=%zu, capacity=%zu): ", arr->size, arr->capacity);
    for (size_t i = 0; i < arr->size; i++) {
        printf("%d ", arr->data[i]);
    }
    printf("\n");
}

int main() {
    DynamicArray *arr = create_array(2);
    if (arr == NULL) {
        fprintf(stderr, "创建数组失败\n");
        return EXIT_FAILURE;
    }

    // 添加元素触发自动扩容
    for (int i = 0; i < 10; i++) {
        push_back(arr, i * 10);
        print_array(arr);
    }

    destroy_array(arr);
    return EXIT_SUCCESS;
}
```

### 示例2：配置文件解析器

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 256

typedef struct {
    char *server;
    int port;
    int timeout;
} Config;

Config *parse_config(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("无法打开配置文件");
        return NULL;
    }

    Config *cfg = (Config *)calloc(1, sizeof(Config));
    if (cfg == NULL) {
        fclose(fp);
        return NULL;
    }

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), fp) != NULL) {
        // 跳过注释和空行
        if (line[0] == '#' || line[0] == '\n') continue;

        char key[50], value[200];
        if (sscanf(line, "%49[^=]=%199[^\n]", key, value) == 2) {
            if (strcmp(key, "server") == 0) {
                cfg->server = strdup(value);
            } else if (strcmp(key, "port") == 0) {
                cfg->port = atoi(value);
            } else if (strcmp(key, "timeout") == 0) {
                cfg->timeout = atoi(value);
            }
        }
    }

    fclose(fp);
    return cfg;
}

void free_config(Config *cfg) {
    if (cfg != NULL) {
        free(cfg->server);
        free(cfg);
    }
}

int main() {
    // 假设config.txt内容:
    // server=192.168.1.1
    // port=8080
    // timeout=30

    Config *cfg = parse_config("config.txt");
    if (cfg == NULL) {
        return EXIT_FAILURE;
    }

    printf("服务器: %s\n", cfg->server);
    printf("端口: %d\n", cfg->port);
    printf("超时: %d秒\n", cfg->timeout);

    free_config(cfg);
    return EXIT_SUCCESS;
}
```

---

## ⚠️ 常见陷阱

### 1. 内存泄漏

```c
// ❌ 内存泄漏
void leak_example() {
    char *p = malloc(100);
    if (some_condition) {
        return;  // 忘记free(p)
    }
    free(p);
}

// ✅ 正确做法
void no_leak_example() {
    char *p = malloc(100);
    if (p == NULL) return;

    if (some_condition) {
        free(p);
        return;
    }

    free(p);
}
```

### 2. 使用已释放的内存

```c
// ❌ 悬空指针
char *p = malloc(100);
free(p);
strcpy(p, "hello");  // 未定义行为！

// ✅ 释放后置NULL
char *p = malloc(100);
free(p);
p = NULL;
if (p != NULL) {
    strcpy(p, "hello");
}
```

### 3. atoi的错误检测问题

```c
// ❌ 无法区分错误和真正的0
int val = atoi(user_input);
if (val == 0) {
    // 是转换失败还是用户输入了"0"？
}

// ✅ 使用strtol
char *endptr;
long val = strtol(user_input, &endptr, 10);
if (endptr == user_input) {
    // 转换失败
}
```

### 4. system()的安全问题

```c
// ❌ 命令注入漏洞
char cmd[100];
sprintf(cmd, "rm %s", user_input);
system(cmd);

// ✅ 验证输入或使用专门的系统调用
```

---

## 🔗 相关链接

- [[C语言进阶 - 指针详解]] - 指针是动态内存管理的基础
- [[C语言标准库 - string.h详解]] - 字符串操作函数
- [[C语言标准库 - stdio.h详解]] - 文件和IO操作
- [[00_C_MOC]] - C语言知识地图

---

## 相关资源

- [[00_C_MOC]] - C语言知识体系
- [[C语言标准库 - stdio.h详解]] - 文件IO和格式化输入输出
- [[C语言标准库 - string.h详解]] - 字符串操作（配合malloc使用）
- [[C语言进阶 - 指针详解]] - 动态内存分配详解
- [[Linux系统编程 - 进程管理]] - 进程退出和环境变量

---

## 📚 参考资料

- C标准库官方文档
- The C Programming Language (K&R)
- C Standard Library Reference: https://en.cppreference.com/w/c/memory

---

## ✅ 学习检查清单

完成以下任务以巩固学习：

- [ ] 编写程序动态分配数组并正确释放
- [ ] 实现一个使用atexit的资源清理系统
- [ ] 使用strtol安全地解析用户输入
- [ ] 编写一个使用qsort排序结构体数组的程序
- [ ] 实现一个简单的动态字符串类型
- [ ] 理解malloc/calloc/realloc的区别
- [ ] 能够检测和避免内存泄漏
- [ ] 掌握随机数生成的正确方法

---

*最后更新: 2025-11-18*
