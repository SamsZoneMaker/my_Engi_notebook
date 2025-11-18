---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/intermediate"
  - "#lang/c"
status: 完善中
complexity: 中级
notetype: 学习笔记
resource: C Primer Plus、C和指针
related:
  - "[[00_C_MOC]]"
  - "[[C语言基础 - 数组]]"
  - "[[C语言进阶 - 指针详解]]"
created: 2025-11-18 22:00:00
modified: 2025-11-18 22:00:00
---
# C语言进阶 - 字符串

> [!abstract] 摘要
> 本笔记深入介绍C语言字符串处理,包括字符串的本质、string.h标准库函数、字符串常见操作、内存安全问题以及高效的字符串处理技巧。

## 🎯 Target
- [ ] 深入理解字符串的本质和内存布局
- [ ] 熟练掌握string.h库函数的使用
- [ ] 了解字符串常见的安全问题
- [ ] 掌握字符串的高级操作技巧
- [ ] 能够实现自定义字符串处理函数

## 📝 Core

### 字符串的本质

#### 什么是C字符串?

**C字符串** 是以空字符`'\0'`(ASCII码0)结尾的字符数组。

**关键特性:**
- ✅ 字符数组
- ✅ 以`'\0'`结尾
- ✅ `'\0'`不计入字符串长度
- ✅ 不是独立的数据类型(不像C++的string类)

```c
char str[] = "Hello";
// 内存布局: ['H']['e']['l']['l']['o']['\0']
// 数组大小: 6字节
// 字符串长度: 5 (strlen)
```

#### 字符串的定义方式

**方式1: 字符数组初始化**
```c
char str1[] = "Hello";  // 推荐: 自动计算大小
char str2[10] = "Hello";  // 指定大小
char str3[] = {'H', 'e', 'l', 'l', 'o', '\0'};  // 逐字符初始化
```

**方式2: 字符指针**
```c
char *str4 = "Hello";  // 指向字符串字面量
const char *str5 = "Hello";  // 推荐: 使用const
```

> [!warning] 字符数组 vs 字符指针
> ```c
> char arr[] = "Hello";   // 可修改,在栈上
> char *ptr = "Hello";    // 不可修改,在只读区
>
> arr[0] = 'h';  // ✅ 合法
> ptr[0] = 'h';  // ❌ 运行时错误! 修改只读内存
> ```

#### 字符串的内存布局

**示例:**
```c
char name[] = "Alice";
```

**内存示意:**
```
地址        值       说明
0x1000:    'A'     name[0]
0x1001:    'l'     name[1]
0x1002:    'i'     name[2]
0x1003:    'c'     name[3]
0x1004:    'e'     name[4]
0x1005:    '\0'    name[5] - 字符串结束标志
```

**字符串字面量:**
```c
char *str = "Hello";
```

```
只读数据区:
  "Hello\0"  ← str指向这里

栈区:
  str (指针变量)
```

### 字符串输入输出

#### 输出字符串

**1. printf**
```c
char name[] = "Alice";
printf("%s\n", name);  // Alice

// 控制宽度
printf("%10s\n", name);   // "     Alice" (右对齐)
printf("%-10s\n", name);  // "Alice     " (左对齐)

// 限制长度
printf("%.3s\n", name);  // "Ali" (只打印3个字符)
```

**2. puts**
```c
char msg[] = "Hello, World!";
puts(msg);  // 自动添加换行
```

**3. putchar(逐字符输出)**
```c
char str[] = "Hello";
for (int i = 0; str[i] != '\0'; i++) {
    putchar(str[i]);
}
putchar('\n');
```

#### 输入字符串

**1. scanf(不推荐)**
```c
char name[50];
printf("输入姓名: ");
scanf("%s", name);  // 遇到空格停止
```

**问题:**
- ❌ 无法读取包含空格的字符串
- ❌ 不检查数组越界(缓冲区溢出)

**改进:**
```c
scanf("%49s", name);  // 限制最多读49个字符
```

**2. fgets(推荐)**
```c
char line[100];
printf("输入一行: ");
fgets(line, sizeof(line), stdin);

// 去除末尾换行符
line[strcspn(line, "\n")] = '\0';

printf("你输入了: %s\n", line);
```

**fgets的特点:**
- ✅ 可以读取空格
- ✅ 指定最大长度,安全
- ✅ 保留换行符(可能需要手动去除)

**3. gets(已废弃,永远不要用!)**
```c
gets(str);  // 危险! 没有边界检查,容易导致缓冲区溢出
```

#### 输入整行并处理

```c
#include <stdio.h>
#include <string.h>

int main() {
    char line[100];

    printf("输入一行文本: ");
    if (fgets(line, sizeof(line), stdin) != NULL) {
        // 去除末尾换行符
        line[strcspn(line, "\n")] = '\0';

        printf("你输入了: [%s]\n", line);
        printf("长度: %zu\n", strlen(line));
    }

    return 0;
}
```

### string.h标准库函数

#### 字符串长度 - strlen

**原型:**
```c
size_t strlen(const char *str);
```

**作用:** 返回字符串长度(不包括`'\0'`)

**示例:**
```c
char str[] = "Hello";
int len = strlen(str);  // 5

// 注意: 与sizeof的区别
printf("strlen: %d\n", strlen(str));    // 5
printf("sizeof: %zu\n", sizeof(str));   // 6
```

> [!note] strlen vs sizeof
> - `strlen(str)`: 运行时计算字符串长度(遍历到'\0')
> - `sizeof(str)`: 编译时确定数组大小(包括'\0')

#### 字符串复制 - strcpy/strncpy

**strcpy - 不安全**
```c
char *strcpy(char *dest, const char *src);
```

```c
char src[] = "Hello";
char dest[20];
strcpy(dest, src);
printf("%s\n", dest);  // Hello
```

**问题:** 不检查dest大小,可能溢出

**strncpy - 更安全**
```c
char *strncpy(char *dest, const char *src, size_t n);
```

```c
char src[] = "Hello";
char dest[10];
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';  // 确保以'\0'结尾
```

**安全复制函数(推荐):**
```c
void safe_strcpy(char *dest, const char *src, size_t dest_size) {
    if (dest_size > 0) {
        strncpy(dest, src, dest_size - 1);
        dest[dest_size - 1] = '\0';
    }
}

char dest[10];
safe_strcpy(dest, "Hello World", sizeof(dest));
printf("%s\n", dest);  // "Hello Wor"
```

#### 字符串连接 - strcat/strncat

**strcat - 不安全**
```c
char *strcat(char *dest, const char *src);
```

```c
char str1[20] = "Hello";
char str2[] = " World";
strcat(str1, str2);
printf("%s\n", str1);  // "Hello World"
```

**strncat - 更安全**
```c
char *strncat(char *dest, const char *src, size_t n);
```

```c
char str1[20] = "Hello";
char str2[] = " World";
strncat(str1, str2, sizeof(str1) - strlen(str1) - 1);
printf("%s\n", str1);  // "Hello World"
```

#### 字符串比较 - strcmp/strncmp

**strcmp**
```c
int strcmp(const char *str1, const char *str2);
```

**返回值:**
- `< 0`: str1 < str2
- `= 0`: str1 == str2
- `> 0`: str1 > str2

```c
char str1[] = "apple";
char str2[] = "banana";
char str3[] = "apple";

if (strcmp(str1, str2) < 0) {
    printf("apple < banana\n");
}

if (strcmp(str1, str3) == 0) {
    printf("apple == apple\n");
}

// 错误示范
if (str1 == str3) {  // ❌ 错误! 比较的是地址
    printf("这不会打印\n");
}
```

**strncmp - 比较前n个字符**
```c
int strncmp(const char *str1, const char *str2, size_t n);
```

```c
char str1[] = "Hello World";
char str2[] = "Hello C";

if (strncmp(str1, str2, 5) == 0) {
    printf("前5个字符相同\n");  // ✅ 会打印
}
```

#### 字符串查找

**strchr - 查找字符**
```c
char *strchr(const char *str, int c);
```

```c
char str[] = "Hello, World!";
char *ptr = strchr(str, 'W');

if (ptr != NULL) {
    printf("找到'W',位置: %ld\n", ptr - str);  // 7
    printf("从'W'开始: %s\n", ptr);  // "World!"
} else {
    printf("未找到\n");
}
```

**strrchr - 从右查找字符**
```c
char str[] = "hello";
char *ptr = strrchr(str, 'l');
printf("最后一个'l'的位置: %ld\n", ptr - str);  // 3
```

**strstr - 查找子串**
```c
char *strstr(const char *haystack, const char *needle);
```

```c
char str[] = "This is a test string";
char *ptr = strstr(str, "test");

if (ptr != NULL) {
    printf("找到'test': %s\n", ptr);  // "test string"
} else {
    printf("未找到\n");
}
```

**strpbrk - 查找字符集合中的任一字符**
```c
char str[] = "hello world";
char *ptr = strpbrk(str, "aeiou");
if (ptr) {
    printf("第一个元音: %c\n", *ptr);  // 'e'
}
```

#### 字符串分割 - strtok

**原型:**
```c
char *strtok(char *str, const char *delim);
```

**特点:**
- 会修改原字符串(将分隔符替换为'\0')
- 第一次调用传入字符串,后续传入NULL
- 线程不安全

**示例:**
```c
char str[] = "one,two,three,four";
char *token = strtok(str, ",");

while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",");
}
// 输出:
// one
// two
// three
// four
```

**分割空格分隔的单词:**
```c
char sentence[] = "This is a test";
char *word = strtok(sentence, " ");

while (word != NULL) {
    printf("[%s] ", word);
    word = strtok(NULL, " ");
}
// 输出: [This] [is] [a] [test]
```

> [!warning] strtok的问题
> - 修改原字符串
> - 不可重入(线程不安全)
> - 替代方案: `strtok_r`(POSIX) 或自己实现

#### 其他有用的函数

**strcspn - 计算不包含字符集的长度**
```c
char str[] = "Hello, World!";
size_t len = strcspn(str, ",");
printf("%zu\n", len);  // 5 ("Hello"的长度)

// 常用于去除换行符
char line[100] = "Hello\n";
line[strcspn(line, "\n")] = '\0';
```

**strspn - 计算只包含字符集的长度**
```c
char str[] = "12345abc";
size_t len = strspn(str, "0123456789");
printf("%zu\n", len);  // 5
```

**strdup - 复制字符串(动态分配)**
```c
char *strdup(const char *str);  // POSIX标准,非C标准
```

```c
char *copy = strdup("Hello");
if (copy != NULL) {
    printf("%s\n", copy);
    free(copy);  // 记得释放!
}
```

### 字符串常见操作

#### 1. 字符串反转

**方法1: 使用临时变量**
```c
void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

int main() {
    char str[] = "Hello";
    reverse_string(str);
    printf("%s\n", str);  // "olleH"
    return 0;
}
```

**方法2: 使用指针**
```c
void reverse_string_ptr(char *str) {
    char *start = str;
    char *end = str + strlen(str) - 1;

    while (start < end) {
        char temp = *start;
        *start = *end;
        *end = temp;
        start++;
        end--;
    }
}
```

#### 2. 字符串转大写/小写

```c
#include <ctype.h>

void to_uppercase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = toupper(str[i]);
    }
}

void to_lowercase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

int main() {
    char str1[] = "Hello World";
    char str2[] = "HELLO WORLD";

    to_uppercase(str1);
    printf("%s\n", str1);  // "HELLO WORLD"

    to_lowercase(str2);
    printf("%s\n", str2);  // "hello world"

    return 0;
}
```

#### 3. 去除首尾空格

```c
#include <ctype.h>

char* trim(char *str) {
    // 去除开头空格
    while (isspace(*str)) {
        str++;
    }

    // 如果全是空格
    if (*str == '\0') {
        return str;
    }

    // 去除结尾空格
    char *end = str + strlen(str) - 1;
    while (end > str && isspace(*end)) {
        end--;
    }
    *(end + 1) = '\0';

    return str;
}

int main() {
    char str[] = "   Hello World   ";
    char *trimmed = trim(str);
    printf("[%s]\n", trimmed);  // "[Hello World]"
    return 0;
}
```

#### 4. 字符串分割(不修改原串)

```c
#include <stdio.h>
#include <string.h>

void split_string(const char *str, char delim) {
    const char *start = str;
    const char *end;

    while ((end = strchr(start, delim)) != NULL) {
        // 打印从start到end的子串
        printf("%.*s\n", (int)(end - start), start);
        start = end + 1;
    }

    // 打印最后一段
    printf("%s\n", start);
}

int main() {
    split_string("one,two,three,four", ',');
    return 0;
}
```

#### 5. 统计字符出现次数

```c
void count_characters(const char *str) {
    int count[256] = {0};  // ASCII字符

    // 统计
    for (int i = 0; str[i]; i++) {
        count[(unsigned char)str[i]]++;
    }

    // 输出
    for (int i = 0; i < 256; i++) {
        if (count[i] > 0) {
            if (isprint(i)) {
                printf("'%c': %d次\n", i, count[i]);
            } else {
                printf("\\x%02X: %d次\n", i, count[i]);
            }
        }
    }
}

int main() {
    count_characters("Hello World");
    return 0;
}
```

#### 6. 检查回文字符串

```c
int is_palindrome(const char *str) {
    int left = 0;
    int right = strlen(str) - 1;

    while (left < right) {
        if (str[left] != str[right]) {
            return 0;  // 不是回文
        }
        left++;
        right--;
    }

    return 1;  // 是回文
}

int main() {
    printf("%d\n", is_palindrome("level"));  // 1
    printf("%d\n", is_palindrome("hello"));  // 0
    return 0;
}
```

### 字符串与数字转换

#### 字符串转数字

**atoi - 转整数**
```c
int atoi(const char *str);
```

```c
char str1[] = "123";
char str2[] = "-456";
char str3[] = "12.34";  // 只转换整数部分

int num1 = atoi(str1);  // 123
int num2 = atoi(str2);  // -456
int num3 = atoi(str3);  // 12
```

**atof - 转浮点数**
```c
double atof(const char *str);
```

```c
char str[] = "3.14159";
double num = atof(str);  // 3.14159
```

**strtol/strtod - 更强大(推荐)**
```c
long strtol(const char *str, char **endptr, int base);
double strtod(const char *str, char **endptr);
```

```c
char str[] = "123abc";
char *end;
long num = strtol(str, &end, 10);

printf("数字: %ld\n", num);     // 123
printf("剩余: %s\n", end);      // "abc"

// 检测转换错误
if (end == str) {
    printf("转换失败\n");
}
```

#### 数字转字符串

**sprintf - 格式化输出到字符串**
```c
char str[50];
int num = 123;
double pi = 3.14159;

sprintf(str, "num = %d, pi = %.2f", num, pi);
printf("%s\n", str);  // "num = 123, pi = 3.14"
```

**snprintf - 更安全(推荐)**
```c
char str[10];
snprintf(str, sizeof(str), "%d", 12345678);
printf("%s\n", str);  // "123456789" (会截断)
```

### 内存安全问题

#### 缓冲区溢出

**危险代码:**
```c
char buffer[10];
strcpy(buffer, "This is too long!");  // 溢出!
```

**安全做法:**
```c
char buffer[10];
strncpy(buffer, "This is too long!", sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';
```

#### 空指针检查

```c
char *str = NULL;

// 危险
// printf("%s\n", str);  // 段错误!

// 安全
if (str != NULL) {
    printf("%s\n", str);
} else {
    printf("字符串为空\n");
}
```

#### 字符串字面量的修改

```c
char *str = "Hello";
// str[0] = 'h';  // ❌ 运行时错误! 修改只读内存

// 正确做法
char str[] = "Hello";  // 可修改的副本
str[0] = 'h';  // ✅ 合法
```

---

## 🤔 Q&A

### Q1: strlen和sizeof有什么区别?
**A**:
- `strlen`: 运行时计算字符串长度(到'\0'),不包括'\0'
- `sizeof`: 编译时确定数组/类型大小(字节数),包括'\0'

```c
char str[] = "Hello";
strlen(str);   // 5
sizeof(str);   // 6
```

### Q2: 为什么不能用==比较字符串?
**A**: 因为==比较的是指针地址,不是字符串内容:
```c
char str1[] = "hello";
char str2[] = "hello";

if (str1 == str2) {  // ❌ 比较地址,永远不相等
    printf("相等\n");
}

if (strcmp(str1, str2) == 0) {  // ✅ 正确
    printf("相等\n");
}
```

### Q3: 如何安全地复制字符串?
**A**: 使用strncpy并确保末尾有'\0':
```c
char dest[10];
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
```

### Q4: char *str = "Hello" 和 char str[] = "Hello" 有什么区别?
**A**:
- `char *str = "Hello"`: 指向只读字符串字面量,不可修改
- `char str[] = "Hello"`: 字符数组,在栈上,可修改

### Q5: 如何实现一个安全的字符串拼接?
**A**:
```c
void safe_strcat(char *dest, const char *src, size_t dest_size) {
    size_t dest_len = strlen(dest);
    size_t remaining = dest_size - dest_len - 1;
    if (remaining > 0) {
        strncat(dest, src, remaining);
    }
}
```

## 🚀 Tasks
- [ ] 实现一个函数检查字符串是否包含另一个字符串(不使用strstr)
- [ ] 编写程序统计字符串中单词的数量
- [ ] 实现一个函数将字符串中的连续空格压缩为一个
- [ ] 编写程序实现简单的字符串加密(Caesar cipher)
- [ ] 实现自己的strlen、strcpy、strcmp函数

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C和指针 - Kenneth A. Reek
* Secure Coding in C and C++ - Robert C. Seacord

## 🕸️ Relation
* [[00_C_MOC]] - C语言知识体系
* [[C语言基础 - 数组]] - 字符串是特殊的字符数组
* [[C语言进阶 - 指针详解]] - 字符串与指针密切相关
* [[C语言进阶 - 结构体]] - 字符串常作为结构体成员
