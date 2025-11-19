---
tags:
  - "#domain/programming"
  - "#type/reference"
  - "#level/intermediate"
  - "#lang/c"
  - "#grain/stdlib"
status: 完善中
complexity: 中级
notetype: 参考手册
resource: C标准库文档
related:
  - "[[00_C_MOC]]"
  - "[[C语言标准库 - stdlib.h详解]]"
  - "[[C语言进阶 - 文件IO]]"
created: 2025-11-18 22:00:00
modified: 2025-11-18 22:00:00
---
# C语言标准库 - stdio.h详解

> [!abstract] 摘要
> stdio.h是C语言标准输入输出库,提供了文件操作、格式化输入输出、字符IO等核心功能。本笔记详细介绍stdio.h中所有重要函数的使用方法、参数说明和最佳实践。

## 🎯 Target
- [ ] 掌握stdio.h中的文件操作函数
- [ ] 熟练使用格式化输入输出函数
- [ ] 了解字符和字符串IO函数
- [ ] 理解文件指针和缓冲区机制
- [ ] 能够处理文件错误和异常情况

## 📝 Core

### stdio.h概述

**stdio.h** (Standard Input/Output Header) 是C语言标准库中最常用的头文件之一。

**核心功能:**
- 文件操作 (打开、关闭、读写)
- 格式化输入输出
- 字符和字符串IO
- 文件定位
- 错误处理

**包含方式:**
```c
#include <stdio.h>
```

### 重要类型和宏

#### FILE类型

```c
FILE *fp;  // 文件指针
```

**FILE** 是一个结构体类型,包含了:
- 文件描述符
- 缓冲区信息
- 当前读写位置
- 文件状态标志
- 错误指示

> [!note] 不透明类型
> FILE是不透明类型,我们不需要(也不应该)直接访问其内部成员,所有操作都通过stdio.h提供的函数完成。

#### 标准流

```c
stdin   // 标准输入 (通常是键盘)
stdout  // 标准输出 (通常是屏幕)
stderr  // 标准错误输出 (通常也是屏幕,但不带缓冲)
```

**示例:**
```c
fprintf(stdout, "This is standard output\n");
fprintf(stderr, "This is an error message\n");
```

#### 重要宏

```c
EOF       // End of File, 通常为-1
NULL      // 空指针
BUFSIZ    // 缓冲区大小 (通常是512或1024)
FILENAME_MAX  // 文件名最大长度
FOPEN_MAX     // 同时打开文件的最大数量
```

### 文件操作函数

#### fopen - 打开文件

**原型:**
```c
FILE *fopen(const char *filename, const char *mode);
```

**参数:**
- `filename`: 文件路径
- `mode`: 打开模式

**打开模式:**

| 模式 | 说明 | 文件不存在 | 文件存在 |
|------|------|------------|----------|
| **"r"** | 只读 | 失败 | 从头读取 |
| **"w"** | 只写 | 创建新文件 | 清空内容 |
| **"a"** | 追加写 | 创建新文件 | 追加到末尾 |
| **"r+"** | 读写 | 失败 | 从头读写 |
| **"w+"** | 读写 | 创建新文件 | 清空内容 |
| **"a+"** | 读写追加 | 创建新文件 | 追加写,可读 |

**二进制模式:** 在模式后加`b`,如`"rb"`, `"wb"`, `"ab"`

**返回值:**
- 成功: 返回FILE指针
- 失败: 返回NULL

**示例:**
```c
// 打开文本文件读取
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("无法打开文件");
    return -1;
}

// 打开二进制文件写入
FILE *fp_bin = fopen("data.bin", "wb");

// 打开文件追加
FILE *fp_append = fopen("log.txt", "a");
```

> [!warning] 安全提示
> - 总是检查fopen的返回值
> - 使用完文件后记得fclose
> - 避免使用固定路径,考虑跨平台兼容性

#### fclose - 关闭文件

**原型:**
```c
int fclose(FILE *stream);
```

**作用:**
- 刷新缓冲区
- 关闭文件
- 释放FILE结构

**返回值:**
- 成功: 0
- 失败: EOF

**示例:**
```c
FILE *fp = fopen("data.txt", "r");
if (fp != NULL) {
    // 使用文件...

    if (fclose(fp) != 0) {
        perror("关闭文件失败");
    }
}
```

> [!tip] 最佳实践
> ```c
> FILE *fp = fopen("data.txt", "r");
> if (fp == NULL) {
>     // 错误处理
>     return -1;
> }
>
> // 使用文件
>
> // 总是检查fclose的返回值
> if (fclose(fp) != 0) {
>     perror("fclose");
> }
> ```

### 字符输入输出

#### fgetc/getc - 读取单个字符

**原型:**
```c
int fgetc(FILE *stream);
int getc(FILE *stream);  // 宏版本,可能更快
```

**返回值:**
- 成功: 读取的字符 (as unsigned char, cast to int)
- 失败或EOF: EOF

**示例:**
```c
FILE *fp = fopen("data.txt", "r");
int ch;

while ((ch = fgetc(fp)) != EOF) {
    putchar(ch);
}

if (ferror(fp)) {
    fprintf(stderr, "读取错误\n");
} else if (feof(fp)) {
    fprintf(stderr, "到达文件末尾\n");
}

fclose(fp);
```

> [!important] 为什么返回int而不是char?
> 因为需要区分EOF(-1)和有效字符。如果返回char,无法表示所有可能的值。

#### fputc/putc - 写入单个字符

**原型:**
```c
int fputc(int c, FILE *stream);
int putc(int c, FILE *stream);  // 宏版本
```

**返回值:**
- 成功: 写入的字符
- 失败: EOF

**示例:**
```c
FILE *fp = fopen("output.txt", "w");

for (char c = 'A'; c <= 'Z'; c++) {
    if (fputc(c, fp) == EOF) {
        perror("写入失败");
        break;
    }
}

fclose(fp);
```

#### getchar/putchar - 标准输入输出

```c
int getchar(void);      // 等价于 getc(stdin)
int putchar(int c);     // 等价于 putc(c, stdout)
```

**示例:**
```c
printf("请输入一个字符: ");
int ch = getchar();
printf("你输入了: ");
putchar(ch);
putchar('\n');
```

#### ungetc - 退回字符

**原型:**
```c
int ungetc(int c, FILE *stream);
```

**作用:** 将字符退回输入流,下次读取时会重新读到

**用途:** 需要"偷看"下一个字符但不消费它

**示例:**
```c
int ch = fgetc(fp);
if (ch == '#') {
    // 这是注释行,退回'#'字符
    ungetc(ch, fp);
    skip_comment_line(fp);
} else {
    // 处理普通字符
    process_char(ch);
}
```

> [!note] 限制
> - 只能退回一个字符
> - 不能退回EOF

### 字符串输入输出

#### fgets - 读取一行

**原型:**
```c
char *fgets(char *str, int n, FILE *stream);
```

**参数:**
- `str`: 目标缓冲区
- `n`: 最多读取n-1个字符(留一个给'\0')
- `stream`: 文件指针

**行为:**
- 读取到换行符'\n'停止(保留'\n')
- 读取n-1个字符停止
- 遇到EOF停止
- 总是添加'\0'结尾

**返回值:**
- 成功: 返回str
- 失败或EOF: 返回NULL

**示例:**
```c
char line[256];
FILE *fp = fopen("data.txt", "r");

while (fgets(line, sizeof(line), fp) != NULL) {
    // 去除末尾换行符
    line[strcspn(line, "\n")] = '\0';
    printf("读取行: %s\n", line);
}

fclose(fp);
```

> [!tip] fgets vs gets
> - **永远不要使用gets()!** 它已被废弃,不安全
> - gets不检查缓冲区大小,容易导致缓冲区溢出
> - fgets是安全的替代方案

#### fputs - 写入字符串

**原型:**
```c
int fputs(const char *str, FILE *stream);
```

**行为:**
- 写入字符串,但不自动添加换行符
- 不会写入'\0'

**返回值:**
- 成功: 非负数
- 失败: EOF

**示例:**
```c
FILE *fp = fopen("output.txt", "w");

fputs("第一行\n", fp);
fputs("第二行\n", fp);

fclose(fp);
```

#### gets/puts - 标准输入输出(不推荐gets)

```c
char *gets(char *str);      // 危险! 已废弃
int puts(const char *str);  // 安全,自动添加换行
```

**示例:**
```c
char buffer[100];

// 不要用gets!
// gets(buffer);  // 危险!

// 使用fgets代替
fgets(buffer, sizeof(buffer), stdin);
buffer[strcspn(buffer, "\n")] = '\0';  // 去除换行符

// puts是安全的
puts("Hello, World!");  // 自动添加换行
```

### 格式化输入输出

#### printf系列

**printf - 格式化输出到stdout**
```c
int printf(const char *format, ...);
```

**fprintf - 格式化输出到文件**
```c
int fprintf(FILE *stream, const char *format, ...);
```

**sprintf - 格式化输出到字符串**
```c
int sprintf(char *str, const char *format, ...);
```

**snprintf - 安全的sprintf(推荐)**
```c
int snprintf(char *str, size_t size, const char *format, ...);
```

**格式说明符:**

| 说明符 | 类型 | 示例 |
|--------|------|------|
| **%d, %i** | int | 123 |
| **%u** | unsigned int | 456 |
| **%ld** | long | 123456L |
| **%lld** | long long | 123456789LL |
| **%f** | double | 3.14 |
| **%lf** | double (scanf中) | - |
| **%e, %E** | 科学计数法 | 1.23e+2 |
| **%g, %G** | 自动选择%f或%e | - |
| **%c** | char | 'A' |
| **%s** | char* | "Hello" |
| **%p** | void* | 0x7fff5fbff |
| **%x, %X** | 十六进制 | ff, FF |
| **%o** | 八进制 | 377 |
| **%%** | 字面% | % |

**修饰符:**

```c
// 宽度
printf("%5d", 42);      // "   42"
printf("%-5d", 42);     // "42   " (左对齐)

// 精度
printf("%.2f", 3.14159);    // "3.14"
printf("%.5s", "Hello");    // "Hello"

// 0填充
printf("%05d", 42);     // "00042"

// 符号
printf("%+d", 42);      // "+42"
printf("% d", 42);      // " 42"

// #修饰
printf("%#x", 255);     // "0xff"
printf("%#o", 64);      // "0100"
```

**示例:**
```c
// printf
int num = 42;
printf("数字: %d\n", num);

// fprintf到文件
FILE *fp = fopen("log.txt", "w");
fprintf(fp, "日志: %s, 值: %d\n", "test", 100);
fclose(fp);

// sprintf (不安全)
char buffer[100];
sprintf(buffer, "结果: %d", 42);

// snprintf (安全,推荐)
char safe_buffer[20];
int len = snprintf(safe_buffer, sizeof(safe_buffer),
                   "这是一个很长的字符串: %d", 12345);
if (len >= sizeof(safe_buffer)) {
    fprintf(stderr, "字符串被截断\n");
}
```

#### scanf系列

**scanf - 从stdin格式化输入**
```c
int scanf(const char *format, ...);
```

**fscanf - 从文件格式化输入**
```c
int fscanf(FILE *stream, const char *format, ...);
```

**sscanf - 从字符串格式化输入**
```c
int sscanf(const char *str, const char *format, ...);
```

**返回值:** 成功赋值的项目数,EOF表示失败

**示例:**
```c
// scanf
int num;
printf("输入一个数字: ");
if (scanf("%d", &num) == 1) {
    printf("你输入了: %d\n", num);
} else {
    fprintf(stderr, "输入错误\n");
}

// 清空输入缓冲区
int c;
while ((c = getchar()) != '\n' && c != EOF);

// fscanf从文件
FILE *fp = fopen("data.txt", "r");
int x, y;
while (fscanf(fp, "%d %d", &x, &y) == 2) {
    printf("读取: %d, %d\n", x, y);
}
fclose(fp);

// sscanf从字符串
char str[] = "123 456";
int a, b;
if (sscanf(str, "%d %d", &a, &b) == 2) {
    printf("解析: %d, %d\n", a, b);
}
```

> [!warning] scanf的问题
> - 不检查缓冲区大小
> - 容易留下垃圾在输入缓冲区
> - 错误处理复杂
>
> **推荐:** 使用fgets+sscanf的组合更安全

**更安全的输入方式:**
```c
char line[100];
int num;

printf("输入一个数字: ");
if (fgets(line, sizeof(line), stdin) != NULL) {
    if (sscanf(line, "%d", &num) == 1) {
        printf("你输入了: %d\n", num);
    } else {
        fprintf(stderr, "格式错误\n");
    }
}
```

### 二进制IO

#### fread - 读取二进制数据

**原型:**
```c
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
```

**参数:**
- `ptr`: 目标缓冲区
- `size`: 每个元素的字节数
- `nmemb`: 元素个数
- `stream`: 文件指针

**返回值:** 成功读取的元素个数(可能小于nmemb)

**示例:**
```c
// 读取结构体数组
typedef struct {
    char name[50];
    int age;
    float score;
} Student;

FILE *fp = fopen("students.dat", "rb");
Student students[100];

size_t count = fread(students, sizeof(Student), 100, fp);
printf("读取了 %zu 个学生记录\n", count);

fclose(fp);

// 读取整个文件到内存
FILE *fp2 = fopen("data.bin", "rb");

// 获取文件大小
fseek(fp2, 0, SEEK_END);
long file_size = ftell(fp2);
fseek(fp2, 0, SEEK_SET);

// 分配内存并读取
char *buffer = (char*)malloc(file_size);
size_t bytes_read = fread(buffer, 1, file_size, fp2);

fclose(fp2);
free(buffer);
```

#### fwrite - 写入二进制数据

**原型:**
```c
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
```

**示例:**
```c
typedef struct {
    int id;
    char name[50];
    double salary;
} Employee;

Employee emp = {1001, "Alice", 50000.0};

FILE *fp = fopen("employees.dat", "wb");

if (fwrite(&emp, sizeof(Employee), 1, fp) != 1) {
    perror("写入失败");
}

fclose(fp);
```

### 文件定位

#### fseek - 移动文件位置指针

**原型:**
```c
int fseek(FILE *stream, long offset, int whence);
```

**参数:**
- `offset`: 偏移量
- `whence`: 起始位置
  - `SEEK_SET`: 文件开头
  - `SEEK_CUR`: 当前位置
  - `SEEK_END`: 文件末尾

**返回值:**
- 成功: 0
- 失败: -1

**示例:**
```c
FILE *fp = fopen("data.bin", "rb");

// 移动到文件开头
fseek(fp, 0, SEEK_SET);

// 移动到文件末尾
fseek(fp, 0, SEEK_END);

// 获取文件大小
long size = ftell(fp);

// 回到开头
fseek(fp, 0, SEEK_SET);

// 跳过前10个字节
fseek(fp, 10, SEEK_SET);

// 向后移动5个字节
fseek(fp, -5, SEEK_CUR);

fclose(fp);
```

#### ftell - 获取当前位置

**原型:**
```c
long ftell(FILE *stream);
```

**返回值:** 当前位置,失败返回-1L

**示例:**
```c
FILE *fp = fopen("data.txt", "r");

char ch;
while ((ch = fgetc(fp)) != EOF) {
    long pos = ftell(fp);
    printf("位置 %ld: %c\n", pos, ch);
}

fclose(fp);
```

#### rewind - 回到文件开头

**原型:**
```c
void rewind(FILE *stream);
```

**等价于:**
```c
fseek(stream, 0, SEEK_SET);
clearerr(stream);  // 还会清除错误标志
```

### 错误处理

#### feof - 检测EOF

**原型:**
```c
int feof(FILE *stream);
```

**返回值:** 到达EOF返回非0,否则返回0

#### ferror - 检测错误

**原型:**
```c
int ferror(FILE *stream);
```

**返回值:** 有错误返回非0,否则返回0

#### clearerr - 清除错误和EOF标志

**原型:**
```c
void clearerr(FILE *stream);
```

#### perror - 打印错误信息

**原型:**
```c
void perror(const char *s);
```

**作用:** 打印errno对应的错误信息

**示例:**
```c
FILE *fp = fopen("nonexistent.txt", "r");
if (fp == NULL) {
    perror("fopen");  // 输出: fopen: No such file or directory
    return -1;
}
```

**完整错误处理示例:**
```c
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("无法打开文件");
    return -1;
}

int ch;
while ((ch = fgetc(fp)) != EOF) {
    putchar(ch);
}

if (ferror(fp)) {
    fprintf(stderr, "读取过程中发生错误\n");
    clearerr(fp);
} else if (feof(fp)) {
    printf("\n文件读取完毕\n");
}

fclose(fp);
```

### 缓冲控制

#### setbuf - 设置缓冲区

**原型:**
```c
void setbuf(FILE *stream, char *buffer);
```

#### setvbuf - 高级缓冲区控制

**原型:**
```c
int setvbuf(FILE *stream, char *buffer, int mode, size_t size);
```

**模式:**
- `_IOFBF`: 全缓冲
- `_IOLBF`: 行缓冲
- `_IONBF`: 无缓冲

**示例:**
```c
// 设置无缓冲(立即输出)
setvbuf(stdout, NULL, _IONBF, 0);

// 设置全缓冲
char buffer[BUFSIZ];
setvbuf(stdout, buffer, _IOFBF, BUFSIZ);
```

#### fflush - 刷新缓冲区

**原型:**
```c
int fflush(FILE *stream);
```

**作用:** 将缓冲区中的数据立即写入文件

**示例:**
```c
printf("进度: ");
for (int i = 1; i <= 100; i++) {
    printf("%d%%", i);
    fflush(stdout);  // 立即显示进度
    usleep(100000);  // 延时
    printf("\r");    // 回到行首
}
printf("\n");
```

### 临时文件

#### tmpfile - 创建临时文件

**原型:**
```c
FILE *tmpfile(void);
```

**特点:**
- 以"wb+"模式打开
- 文件关闭或程序结束时自动删除

**示例:**
```c
FILE *temp = tmpfile();
if (temp == NULL) {
    perror("创建临时文件失败");
    return -1;
}

// 使用临时文件
fprintf(temp, "临时数据\n");
rewind(temp);

char line[100];
fgets(line, sizeof(line), temp);

fclose(temp);  // 自动删除
```

#### tmpnam - 生成临时文件名

**原型:**
```c
char *tmpnam(char *str);
```

**示例:**
```c
char temp_name[L_tmpnam];
if (tmpnam(temp_name) != NULL) {
    printf("临时文件名: %s\n", temp_name);
}
```

---

## 🤔 Q&A

### Q1: fopen失败了怎么办?
**A**: 总是检查返回值并使用perror打印错误信息:
```c
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("fopen");
    return -1;
}
```

### Q2: 什么时候用文本模式,什么时候用二进制模式?
**A**:
- **文本模式** ("r", "w"): 处理文本文件,会进行换行符转换
- **二进制模式** ("rb", "wb"): 处理二进制数据,不做任何转换

**建议:** 不确定时使用二进制模式更安全

### Q3: scanf为什么不安全?
**A**: scanf不检查缓冲区大小,容易导致缓冲区溢出。推荐使用fgets+sscanf:
```c
char line[100];
int num;
fgets(line, sizeof(line), stdin);
sscanf(line, "%d", &num);
```

### Q4: printf和fprintf有什么区别?
**A**:
- `printf`: 输出到stdout
- `fprintf`: 可以输出到任意文件

实际上`printf(...)`等价于`fprintf(stdout, ...)`

### Q5: 如何正确读取整个文件?
**A**:
```c
FILE *fp = fopen("data.txt", "rb");

fseek(fp, 0, SEEK_END);
long size = ftell(fp);
fseek(fp, 0, SEEK_SET);

char *content = (char*)malloc(size + 1);
fread(content, 1, size, fp);
content[size] = '\0';

fclose(fp);
// 使用content...
free(content);
```

## 🚀 Tasks
- [ ] 实现一个简单的文本编辑器(读写文件)
- [ ] 编写程序复制二进制文件
- [ ] 实现一个CSV文件解析器
- [ ] 编写日志系统(使用fprintf)
- [ ] 实现文件加密/解密程序

## 📚 Reference
* C标准库文档 (C11 Standard)
* The C Programming Language - K&R
* C Primer Plus - Stephen Prata

## 🕸️ Relation
* [[00_C_MOC]] - C语言知识体系
* [[C语言标准库 - stdlib.h详解]] - 内存管理、类型转换
* [[C语言标准库 - string.h详解]] - 字符串操作函数
* [[Linux系统编程 - 文件IO]] - 系统调用层文件操作（open/read/write）
* [[C语言进阶 - 字符串]] - 字符串处理详解
* [[Makefile完全指南]] - 构建包含stdio.h的项目
