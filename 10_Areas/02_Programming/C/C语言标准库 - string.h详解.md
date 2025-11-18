---
tags:
  - "#domain/programming"
  - "#type/reference"
  - "#level/intermediate"
  - "#lang/c"
  - "#grain/stdlib"
  - "#tech/strings"
status: 完成
complexity: 中级
notetype: 技术参考
resource: C标准库文档
related:
  - "[[C语言进阶 - 字符串]]"
  - "[[C语言标准库 - stdio.h详解]]"
  - "[[C语言标准库 - stdlib.h详解]]"
  - "[[C语言进阶 - 指针详解]]"
created: 2025-11-18
modified: 2025-11-18
---

# C语言标准库 - string.h详解

## 📋 概述

`string.h` 是C标准库中专门处理字符串和内存操作的头文件，包含：
- **字符串复制** (strcpy, strncpy, memcpy, memmove)
- **字符串连接** (strcat, strncat)
- **字符串比较** (strcmp, strncmp, memcmp)
- **字符串搜索** (strchr, strstr, strpbrk, strcspn, strspn)
- **字符串分割** (strtok, strtok_r)
- **内存操作** (memset, memchr, memcmp)
- **其他工具** (strlen, strerror)

---

## 🎯 学习目标

- [ ] 掌握安全的字符串复制方法
- [ ] 理解strcpy和memcpy的区别
- [ ] 学会使用strncpy避免缓冲区溢出
- [ ] 掌握字符串搜索和分割技巧
- [ ] 理解strtok的状态管理和陷阱
- [ ] 掌握内存操作函数的使用
- [ ] 避免常见的字符串安全漏洞

---

## 📚 核心内容

### 重要宏和类型

```c
NULL        // 空指针常量
size_t      // 无符号整数类型，用于表示大小
```

---

## 🔧 函数详解

### 一、字符串长度

#### strlen() - 计算字符串长度 ⭐⭐⭐⭐⭐

```c
size_t strlen(const char *s);
```

**功能**：计算字符串的长度（不包括终止符'\0'）。

**参数**：
- `s`：以'\0'结尾的字符串

**返回值**：字符串中字符的个数（不含'\0'）

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str1[] = "Hello";
    char str2[] = "Hello World";
    char str3[] = "";

    printf("'%s' 长度: %zu\n", str1, strlen(str1));     // 5
    printf("'%s' 长度: %zu\n", str2, strlen(str2));     // 11
    printf("'%s' 长度: %zu\n", str3, strlen(str3));     // 0

    // ⚠️ 注意：strlen遍历字符串直到'\0'，时间复杂度O(n)
    // 在循环中避免重复调用

    // ❌ 低效
    for (size_t i = 0; i < strlen(str1); i++) {  // 每次迭代都计算长度！
        printf("%c ", str1[i]);
    }

    // ✅ 高效
    size_t len = strlen(str1);
    for (size_t i = 0; i < len; i++) {
        printf("%c ", str1[i]);
    }

    return 0;
}
```

**⚠️ 陷阱**：

```c
char str[10] = {'H', 'e', 'l', 'l', 'o'};  // 没有'\0'终止符
printf("%zu\n", strlen(str));  // 未定义行为！可能越界读取

// ✅ 正确初始化
char str[10] = "Hello";  // 自动添加'\0'
```

---

### 二、字符串复制

#### 1. strcpy() - 字符串复制

```c
char *strcpy(char *dest, const char *src);
```

**功能**：将src字符串（包括'\0'）复制到dest。

**参数**：
- `dest`：目标缓冲区
- `src`：源字符串

**返回值**：返回dest指针

**⚠️ 危险**：不检查dest大小，容易造成缓冲区溢出！

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char src[] = "Hello";
    char dest[20];

    strcpy(dest, src);
    printf("dest: %s\n", dest);  // Hello

    // ❌ 危险！缓冲区溢出
    char small[3];
    strcpy(small, "Hello");  // 溢出！src需要6字节（含'\0'），但small只有3字节

    return 0;
}
```

#### 2. strncpy() - 限制长度的字符串复制 ⭐⭐⭐

```c
char *strncpy(char *dest, const char *src, size_t n);
```

**功能**：最多复制n个字符从src到dest。

**参数**：
- `dest`：目标缓冲区
- `src`：源字符串
- `n`：最多复制的字符数

**返回值**：返回dest指针

**⚠️ 陷阱**：
1. 如果src长度 < n，dest剩余部分会用'\0'填充
2. 如果src长度 >= n，**不会自动添加'\0'终止符**！

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char dest[10];

    // 情况1: src短于n
    strncpy(dest, "Hi", 10);
    // dest = "Hi\0\0\0\0\0\0\0\0" (剩余用'\0'填充)

    // 情况2: src长于或等于n
    strncpy(dest, "HelloWorld", 5);
    // dest = "Hello" (没有'\0'终止符！)
    dest[5] = '\0';  // 必须手动添加！

    printf("%s\n", dest);  // Hello

    return 0;
}
```

**✅ 安全的strncpy用法**：

```c
char dest[20];
strncpy(dest, src, sizeof(dest) - 1);  // 留一个字节给'\0'
dest[sizeof(dest) - 1] = '\0';          // 确保终止符

// 或者封装成安全函数
void safe_strcpy(char *dest, const char *src, size_t dest_size) {
    if (dest_size > 0) {
        strncpy(dest, src, dest_size - 1);
        dest[dest_size - 1] = '\0';
    }
}

char dest[20];
safe_strcpy(dest, src, sizeof(dest));
```

#### 3. memcpy() - 内存复制 ⭐⭐⭐⭐

```c
void *memcpy(void *dest, const void *src, size_t n);
```

**功能**：复制n个字节从src到dest。

**参数**：
- `dest`：目标内存
- `src`：源内存
- `n`：复制的字节数

**返回值**：返回dest指针

**⚠️ 前提条件**：dest和src不能重叠！

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    // 复制字符串
    char src[] = "Hello";
    char dest[20];
    memcpy(dest, src, strlen(src) + 1);  // +1包括'\0'
    printf("%s\n", dest);  // Hello

    // 复制数组
    int arr1[] = {1, 2, 3, 4, 5};
    int arr2[5];
    memcpy(arr2, arr1, sizeof(arr1));

    for (int i = 0; i < 5; i++) {
        printf("%d ", arr2[i]);  // 1 2 3 4 5
    }
    printf("\n");

    // 复制结构体
    struct Point {
        int x, y;
    };
    struct Point p1 = {10, 20};
    struct Point p2;
    memcpy(&p2, &p1, sizeof(struct Point));
    printf("p2: (%d, %d)\n", p2.x, p2.y);  // (10, 20)

    return 0;
}
```

**strcpy vs memcpy**：

| 特性 | strcpy | memcpy |
|------|--------|--------|
| 停止条件 | 遇到'\0' | 复制n字节 |
| 用途 | 仅字符串 | 任意内存 |
| 需要指定长度 | ❌ 否 | ✅ 是 |
| 处理二进制数据 | ❌ 否 | ✅ 是 |

```c
// memcpy可以复制包含'\0'的数据
char data[] = {'A', '\0', 'B', 'C'};
char dest[4];

strcpy(dest, data);   // 只复制'A'和'\0'
memcpy(dest, data, 4); // 复制全部4字节
```

#### 4. memmove() - 安全的内存复制 ⭐⭐⭐⭐

```c
void *memmove(void *dest, const void *src, size_t n);
```

**功能**：复制n个字节，即使dest和src重叠也安全。

**参数**：同memcpy

**返回值**：返回dest指针

**与memcpy的区别**：memmove可以处理重叠的内存区域。

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str[] = "Hello World";

    // ❌ memcpy在重叠时未定义行为
    // memcpy(str + 2, str, 5);  // 危险！

    // ✅ memmove处理重叠安全
    memmove(str + 2, str, 5);
    printf("%s\n", str);  // HeHello rld

    // 另一个例子：删除数组元素
    int arr[] = {1, 2, 3, 4, 5};
    // 删除索引2的元素（值为3）
    memmove(&arr[2], &arr[3], 2 * sizeof(int));
    // arr = {1, 2, 4, 5, 5}

    for (int i = 0; i < 4; i++) {
        printf("%d ", arr[i]);  // 1 2 4 5
    }
    printf("\n");

    return 0;
}
```

**性能考虑**：
- memmove比memcpy稍慢（因为要检测重叠）
- 如果确定不重叠，使用memcpy更高效
- 如果不确定，安全起见使用memmove

---

### 三、字符串连接

#### 1. strcat() - 字符串连接

```c
char *strcat(char *dest, const char *src);
```

**功能**：将src追加到dest末尾。

**参数**：
- `dest`：目标字符串（必须有足够空间）
- `src`：源字符串

**返回值**：返回dest指针

**⚠️ 危险**：不检查dest大小，容易溢出！

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char dest[20] = "Hello";
    char src[] = " World";

    strcat(dest, src);
    printf("%s\n", dest);  // Hello World

    // ❌ 缓冲区溢出
    char small[10] = "Hello";
    strcat(small, " World!");  // 溢出！

    return 0;
}
```

#### 2. strncat() - 限制长度的字符串连接 ⭐⭐⭐

```c
char *strncat(char *dest, const char *src, size_t n);
```

**功能**：最多追加src的n个字符到dest末尾，**总是添加'\0'**。

**参数**：
- `dest`：目标字符串
- `src`：源字符串
- `n`：最多追加的字符数

**返回值**：返回dest指针

**✅ 与strncpy不同**：strncat总是添加'\0'终止符！

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char dest[20] = "Hello";

    // 追加最多5个字符
    strncat(dest, " World!", 5);
    printf("%s\n", dest);  // Hello Worl (自动添加'\0')

    // ✅ 安全用法
    char buffer[20] = "Hi";
    size_t remaining = sizeof(buffer) - strlen(buffer) - 1;
    strncat(buffer, " there friend", remaining);
    printf("%s\n", buffer);

    return 0;
}
```

**strcat vs strncat**：

```c
char dest[20] = "Hello";

// strcat - 不安全
strcat(dest, src);  // 可能溢出

// strncat - 更安全
strncat(dest, src, sizeof(dest) - strlen(dest) - 1);  // 限制追加长度
```

---

### 四、字符串比较

#### 1. strcmp() - 字符串比较 ⭐⭐⭐⭐⭐

```c
int strcmp(const char *s1, const char *s2);
```

**功能**：按字典序比较两个字符串。

**返回值**：
- 0：s1 == s2
- <0：s1 < s2
- \>0：s1 > s2

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    printf("%d\n", strcmp("apple", "apple"));   // 0 (相等)
    printf("%d\n", strcmp("apple", "banana"));  // <0 (a < b)
    printf("%d\n", strcmp("banana", "apple"));  // >0 (b > a)
    printf("%d\n", strcmp("Apple", "apple"));   // <0 (A < a, ASCII值比较)

    // ❌ 错误用法 - 不要用==比较字符串
    char *s1 = "hello";
    char *s2 = "hello";
    if (s1 == s2) {  // 比较的是指针地址，不是内容！
        printf("这个可能不会执行\n");
    }

    // ✅ 正确用法
    if (strcmp(s1, s2) == 0) {
        printf("字符串相等\n");
    }

    return 0;
}
```

**实际应用**：

```c
// 排序字符串数组
int compare_strings(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

char *names[] = {"Charlie", "Alice", "Bob"};
qsort(names, 3, sizeof(char *), compare_strings);
// 结果: Alice, Bob, Charlie

// 忽略大小写比较（需要自己实现或使用strcasecmp - POSIX）
int strcasecmp_custom(const char *s1, const char *s2) {
    while (*s1 && *s2) {
        char c1 = tolower(*s1);
        char c2 = tolower(*s2);
        if (c1 != c2) return c1 - c2;
        s1++;
        s2++;
    }
    return *s1 - *s2;
}
```

#### 2. strncmp() - 限制长度的字符串比较

```c
int strncmp(const char *s1, const char *s2, size_t n);
```

**功能**：最多比较前n个字符。

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char *s1 = "Hello World";
    char *s2 = "Hello There";

    printf("%d\n", strcmp(s1, s2));      // >0 (W > T)
    printf("%d\n", strncmp(s1, s2, 5));  // 0 (前5个字符相同)

    // 用途：检查前缀
    if (strncmp(s1, "Hello", 5) == 0) {
        printf("s1以'Hello'开头\n");
    }

    return 0;
}
```

#### 3. memcmp() - 内存比较

```c
int memcmp(const void *s1, const void *s2, size_t n);
```

**功能**：按字节比较两块内存。

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    // 比较字符串（包括'\0'后的内容）
    char str1[] = "Hello\0XXX";
    char str2[] = "Hello\0YYY";

    printf("%d\n", strcmp(str1, str2));         // 0 (strcmp在'\0'处停止)
    printf("%d\n", memcmp(str1, str2, 9));      // <0 (memcmp比较全部9字节)

    // 比较结构体
    struct Data {
        int x;
        char c;
    };

    struct Data d1 = {10, 'A'};
    struct Data d2 = {10, 'A'};

    if (memcmp(&d1, &d2, sizeof(struct Data)) == 0) {
        printf("结构体相等\n");
    }

    // ⚠️ 注意：结构体填充字节可能导致不相等
    // 即使所有成员相同，padding可能不同

    return 0;
}
```

---

### 五、字符串搜索

#### 1. strchr() - 查找字符 ⭐⭐⭐⭐

```c
char *strchr(const char *s, int c);
char *strrchr(const char *s, int c);  // 从右往左找
```

**功能**：在字符串中查找第一个（或最后一个）字符c。

**返回值**：
- 找到：返回指向该字符的指针
- 未找到：返回NULL

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char *str = "Hello World";

    // 查找字符'o'
    char *p = strchr(str, 'o');
    if (p != NULL) {
        printf("找到'o'在位置: %ld\n", p - str);  // 4
        printf("从'o'开始: %s\n", p);             // o World
    }

    // 查找最后一个'o'
    p = strrchr(str, 'o');
    if (p != NULL) {
        printf("最后的'o'在位置: %ld\n", p - str);  // 7
        printf("从最后'o'开始: %s\n", p);           // orld
    }

    // 查找不存在的字符
    p = strchr(str, 'x');
    if (p == NULL) {
        printf("未找到'x'\n");
    }

    // 实用：提取文件扩展名
    char *filename = "document.txt";
    char *ext = strrchr(filename, '.');
    if (ext != NULL) {
        printf("扩展名: %s\n", ext + 1);  // txt
    }

    return 0;
}
```

**实际应用 - 路径解析**：

```c
// 提取文件名
char *get_filename(char *path) {
    char *p = strrchr(path, '/');
    if (p == NULL) p = strrchr(path, '\\');  // Windows路径
    return (p == NULL) ? path : p + 1;
}

char *path = "/home/user/file.txt";
printf("文件名: %s\n", get_filename(path));  // file.txt
```

#### 2. strstr() - 查找子字符串 ⭐⭐⭐⭐⭐

```c
char *strstr(const char *haystack, const char *needle);
```

**功能**：在haystack中查找第一次出现的needle子字符串。

**返回值**：
- 找到：返回指向子字符串的指针
- 未找到：返回NULL

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char *text = "The quick brown fox jumps over the lazy dog";

    // 查找子字符串
    char *p = strstr(text, "brown");
    if (p != NULL) {
        printf("找到'brown'在位置: %ld\n", p - text);  // 10
        printf("从'brown'开始: %s\n", p);              // brown fox jumps...
    }

    // 查找所有出现位置
    char *str = "one two one three one";
    char *search = "one";
    char *pos = str;

    printf("'%s'出现在: ", search);
    while ((pos = strstr(pos, search)) != NULL) {
        printf("%ld ", pos - str);  // 0 8 18
        pos += strlen(search);      // 移动到下一个可能的位置
    }
    printf("\n");

    return 0;
}
```

**实际应用 - 字符串替换**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *str_replace(const char *str, const char *old, const char *new) {
    size_t old_len = strlen(old);
    size_t new_len = strlen(new);

    // 计算需要的缓冲区大小
    int count = 0;
    const char *p = str;
    while ((p = strstr(p, old)) != NULL) {
        count++;
        p += old_len;
    }

    size_t result_len = strlen(str) + count * (new_len - old_len);
    char *result = malloc(result_len + 1);
    if (result == NULL) return NULL;

    char *dst = result;
    const char *src = str;

    while ((p = strstr(src, old)) != NULL) {
        size_t prefix_len = p - src;
        memcpy(dst, src, prefix_len);
        dst += prefix_len;

        memcpy(dst, new, new_len);
        dst += new_len;

        src = p + old_len;
    }

    strcpy(dst, src);
    return result;
}

int main() {
    char *text = "Hello World, World!";
    char *result = str_replace(text, "World", "Universe");

    printf("原字符串: %s\n", text);
    printf("替换后: %s\n", result);  // Hello Universe, Universe!

    free(result);
    return 0;
}
```

#### 3. strpbrk() - 查找字符集中的任意字符

```c
char *strpbrk(const char *s, const char *accept);
```

**功能**：在s中查找accept中任意字符的第一次出现。

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char *text = "Hello, World!";

    // 查找第一个标点符号
    char *p = strpbrk(text, ",.!?;:");
    if (p != NULL) {
        printf("找到标点: '%c' 在位置 %ld\n", *p, p - text);  // ',' 在位置5
    }

    // 查找数字
    char *str = "abc123def";
    p = strpbrk(str, "0123456789");
    if (p != NULL) {
        printf("第一个数字: %c\n", *p);  // 1
    }

    return 0;
}
```

#### 4. strcspn() 和 strspn() - 计算区间长度

```c
size_t strcspn(const char *s, const char *reject);  // 计算不包含reject的前缀长度
size_t strspn(const char *s, const char *accept);   // 计算只包含accept的前缀长度
```

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char *text = "hello123world";

    // strcspn: 计算到第一个数字的长度
    size_t len = strcspn(text, "0123456789");
    printf("前%zu个字符是字母: %.*s\n", len, (int)len, text);  // hello

    // strspn: 计算开头字母的长度
    len = strspn(text, "abcdefghijklmnopqrstuvwxyz");
    printf("前%zu个字符是小写字母: %.*s\n", len, (int)len, text);  // hello

    // 实用：去除前导空格
    char *str = "   Hello";
    size_t spaces = strspn(str, " \t\n");
    printf("去除空格: '%s'\n", str + spaces);  // 'Hello'

    return 0;
}
```

---

### 六、字符串分割

#### strtok() - 字符串分割 ⭐⭐⭐⭐

```c
char *strtok(char *str, const char *delim);
```

**功能**：将字符串按分隔符分割成多个token。

**参数**：
- `str`：第一次调用时传入要分割的字符串，后续调用传NULL
- `delim`：分隔符字符集

**返回值**：
- 找到token：返回指向token的指针
- 没有更多token：返回NULL

**⚠️ 重要特性**：
1. **修改原字符串**：将分隔符替换为'\0'
2. **内部状态**：使用静态变量保存状态，**不是线程安全的**
3. 第一次调用传字符串，后续调用传NULL

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str[] = "apple,banana,orange,grape";
    char *token;

    // 第一次调用传原字符串
    token = strtok(str, ",");
    while (token != NULL) {
        printf("Token: %s\n", token);
        token = strtok(NULL, ",");  // 后续调用传NULL
    }
    // 输出:
    // Token: apple
    // Token: banana
    // Token: orange
    // Token: grape

    // ⚠️ 注意：原字符串被修改了
    // str = "apple\0banana\0orange\0grape"

    return 0;
}
```

**多个分隔符**：

```c
char str[] = "one,two;three:four";
char *token = strtok(str, ",:;");

while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",:;");
}
// 输出: one, two, three, four
```

**解析CSV**：

```c
#include <stdio.h>
#include <string.h>

void parse_csv_line(char *line) {
    char *token = strtok(line, ",");
    int column = 0;

    while (token != NULL) {
        printf("列%d: %s\n", column++, token);
        token = strtok(NULL, ",");
    }
}

int main() {
    char csv[] = "John,25,Engineer,50000";
    parse_csv_line(csv);
    // 输出:
    // 列0: John
    // 列1: 25
    // 列2: Engineer
    // 列3: 50000

    return 0;
}
```

**⚠️ strtok的陷阱**：

```c
// ❌ 问题1：不能同时分割两个字符串
char str1[] = "a,b,c";
char str2[] = "x,y,z";

char *t1 = strtok(str1, ",");  // a
char *t2 = strtok(str2, ",");  // ❌ 错误！strtok状态被覆盖
t1 = strtok(NULL, ",");        // 返回NULL或错误结果

// ❌ 问题2：修改原字符串
const char *str = "a,b,c";  // 常量字符串
strtok(str, ",");  // ❌ 未定义行为！尝试修改只读内存

// ✅ 解决方案1：使用strtok_r（POSIX，线程安全）
char str1[] = "a,b,c";
char str2[] = "x,y,z";
char *saveptr1, *saveptr2;

char *t1 = strtok_r(str1, ",", &saveptr1);
char *t2 = strtok_r(str2, ",", &saveptr2);
t1 = strtok_r(NULL, ",", &saveptr1);  // 正确

// ✅ 解决方案2：自己实现简单的分割
char *my_strtok(char *str, const char *delim, char **saveptr) {
    if (str == NULL) str = *saveptr;
    if (*str == '\0') return NULL;

    // 跳过前导分隔符
    str += strspn(str, delim);
    if (*str == '\0') return NULL;

    // 找到下一个分隔符
    char *end = str + strcspn(str, delim);
    if (*end == '\0') {
        *saveptr = end;
        return str;
    }

    *end = '\0';
    *saveptr = end + 1;
    return str;
}
```

**✅ 更安全的字符串分割**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 不修改原字符串的分割函数
char **split_string(const char *str, const char *delim, int *count) {
    // 复制字符串
    char *copy = strdup(str);
    if (copy == NULL) return NULL;

    // 计算token数量
    int num_tokens = 0;
    char *temp = strdup(str);
    char *token = strtok(temp, delim);
    while (token != NULL) {
        num_tokens++;
        token = strtok(NULL, delim);
    }
    free(temp);

    // 分配指针数组
    char **tokens = malloc((num_tokens + 1) * sizeof(char *));
    if (tokens == NULL) {
        free(copy);
        return NULL;
    }

    // 分割并存储
    int i = 0;
    token = strtok(copy, delim);
    while (token != NULL) {
        tokens[i] = strdup(token);
        i++;
        token = strtok(NULL, delim);
    }
    tokens[i] = NULL;

    free(copy);
    *count = num_tokens;
    return tokens;
}

void free_tokens(char **tokens) {
    if (tokens == NULL) return;
    for (int i = 0; tokens[i] != NULL; i++) {
        free(tokens[i]);
    }
    free(tokens);
}

int main() {
    const char *str = "apple,banana,orange";
    int count;
    char **tokens = split_string(str, ",", &count);

    printf("原字符串: %s\n", str);  // 未修改
    printf("分割结果 (%d个):\n", count);
    for (int i = 0; i < count; i++) {
        printf("  %d: %s\n", i, tokens[i]);
    }

    free_tokens(tokens);
    return 0;
}
```

---

### 七、内存操作

#### 1. memset() - 内存填充 ⭐⭐⭐⭐⭐

```c
void *memset(void *s, int c, size_t n);
```

**功能**：将内存块的前n个字节设置为值c。

**参数**：
- `s`：内存起始地址
- `c`：要设置的值（会被转换为unsigned char）
- `n`：字节数

**返回值**：返回s指针

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    // 初始化数组为0
    int arr[10];
    memset(arr, 0, sizeof(arr));

    // 初始化字符数组
    char str[20];
    memset(str, 'A', 19);
    str[19] = '\0';
    printf("%s\n", str);  // AAAAAAAAAAAAAAAAAAA

    // 清空结构体
    struct Data {
        int x;
        double y;
        char name[20];
    };
    struct Data data;
    memset(&data, 0, sizeof(struct Data));

    // ⚠️ 只适合字节级操作！
    int nums[5];
    memset(nums, 1, sizeof(nums));  // ❌ nums不是{1,1,1,1,1}
    // 而是{0x01010101, 0x01010101, ...} = {16843009, ...}

    // ✅ 初始化int数组应该用循环
    for (int i = 0; 0; i < 5; i++) {
        nums[i] = 1;
    }

    return 0;
}
```

**常见用途**：

```c
// 1. 清空缓冲区
char buffer[256];
memset(buffer, 0, sizeof(buffer));

// 2. 清除敏感数据（如密码）
char password[64];
// ... 使用密码 ...
memset(password, 0, sizeof(password));  // 安全清除

// 3. 初始化结构体数组
struct Student students[100];
memset(students, 0, sizeof(students));
```

#### 2. memchr() - 内存搜索

```c
void *memchr(const void *s, int c, size_t n);
```

**功能**：在内存块的前n个字节中查找字符c。

**示例**：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char data[] = "Hello\0World";  // 包含'\0'的数据

    // strchr会在'\0'处停止
    char *p1 = strchr(data, 'W');  // NULL

    // memchr可以搜索'\0'之后的内容
    char *p2 = memchr(data, 'W', 11);  // 找到'W'
    if (p2 != NULL) {
        printf("找到'W'在位置: %ld\n", p2 - data);  // 6
    }

    // 搜索字节值
    unsigned char bytes[] = {0x01, 0x02, 0xFF, 0x04};
    unsigned char *p = memchr(bytes, 0xFF, 4);
    if (p != NULL) {
        printf("找到0xFF在位置: %ld\n", p - bytes);  // 2
    }

    return 0;
}
```

---

### 八、其他工具函数

#### strerror() - 错误信息

```c
char *strerror(int errnum);
```

**功能**：返回错误码对应的描述字符串。

**示例**：

```c
#include <stdio.h>
#include <string.h>
#include <errno.h>

int main() {
    FILE *fp = fopen("nonexistent.txt", "r");

    if (fp == NULL) {
        printf("错误码: %d\n", errno);
        printf("错误描述: %s\n", strerror(errno));
        // 或者使用perror
        perror("打开文件失败");
    }

    return 0;
}
```

---

## 📝 实战示例

### 示例1：安全的字符串操作封装

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 安全的字符串结构
typedef struct {
    char *data;
    size_t length;
    size_t capacity;
} SafeString;

// 创建字符串
SafeString *str_create(const char *init) {
    SafeString *s = malloc(sizeof(SafeString));
    if (s == NULL) return NULL;

    size_t len = strlen(init);
    s->capacity = len + 16;  // 预留空间
    s->data = malloc(s->capacity);
    if (s->data == NULL) {
        free(s);
        return NULL;
    }

    strcpy(s->data, init);
    s->length = len;

    return s;
}

// 追加字符串
int str_append(SafeString *s, const char *text) {
    size_t add_len = strlen(text);
    size_t new_len = s->length + add_len;

    if (new_len >= s->capacity) {
        // 扩容
        size_t new_cap = (new_len + 1) * 2;
        char *new_data = realloc(s->data, new_cap);
        if (new_data == NULL) return -1;

        s->data = new_data;
        s->capacity = new_cap;
    }

    strcat(s->data, text);
    s->length = new_len;

    return 0;
}

// 销毁字符串
void str_destroy(SafeString *s) {
    if (s != NULL) {
        free(s->data);
        free(s);
    }
}

// 打印字符串
void str_print(SafeString *s) {
    printf("字符串: '%s' (长度=%zu, 容量=%zu)\n",
           s->data, s->length, s->capacity);
}

int main() {
    SafeString *s = str_create("Hello");
    str_print(s);

    str_append(s, " World");
    str_print(s);

    str_append(s, "! This is a longer string to trigger reallocation.");
    str_print(s);

    str_destroy(s);
    return 0;
}
```

### 示例2：URL解析器

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *protocol;
    char *host;
    int port;
    char *path;
} URL;

URL *parse_url(const char *url_str) {
    URL *url = calloc(1, sizeof(URL));
    if (url == NULL) return NULL;

    char *copy = strdup(url_str);
    char *p = copy;

    // 提取协议 (http://...)
    char *proto_end = strstr(p, "://");
    if (proto_end != NULL) {
        *proto_end = '\0';
        url->protocol = strdup(p);
        p = proto_end + 3;
    }

    // 提取主机和端口
    char *path_start = strchr(p, '/');
    char *port_start = strchr(p, ':');

    if (path_start != NULL) {
        *path_start = '\0';
        url->path = strdup(path_start + 1);
    }

    if (port_start != NULL && (path_start == NULL || port_start < path_start)) {
        *port_start = '\0';
        url->port = atoi(port_start + 1);
        url->host = strdup(p);
    } else {
        url->host = strdup(p);
        url->port = 80;  // 默认端口
    }

    free(copy);
    return url;
}

void free_url(URL *url) {
    if (url != NULL) {
        free(url->protocol);
        free(url->host);
        free(url->path);
        free(url);
    }
}

int main() {
    URL *url = parse_url("https://example.com:8080/path/to/page");

    if (url != NULL) {
        printf("协议: %s\n", url->protocol);
        printf("主机: %s\n", url->host);
        printf("端口: %d\n", url->port);
        printf("路径: %s\n", url->path);

        free_url(url);
    }

    return 0;
}
```

---

## ⚠️ 常见陷阱汇总

### 1. 缓冲区溢出

```c
// ❌ strcpy不检查大小
char dest[5];
strcpy(dest, "Hello World");  // 溢出！

// ✅ 使用strncpy
strncpy(dest, "Hello World", sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
```

### 2. strncpy不添加'\0'

```c
// ❌ 可能没有终止符
char dest[5];
strncpy(dest, "HelloWorld", 5);  // dest = "Hello" (无'\0')

// ✅ 手动添加
strncpy(dest, "HelloWorld", sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
```

### 3. strtok修改原字符串

```c
// ❌ 修改常量
const char *str = "a,b,c";
strtok(str, ",");  // 未定义行为

// ✅ 复制后再分割
char copy[100];
strcpy(copy, str);
strtok(copy, ",");
```

### 4. strcmp不能用于二进制数据

```c
// ❌ 包含'\0'的数据
char data1[] = {1, 2, 0, 3, 4};
char data2[] = {1, 2, 0, 5, 6};
strcmp(data1, data2);  // 只比较到第一个'\0'

// ✅ 使用memcmp
memcmp(data1, data2, 5);
```

---

## 🔗 相关链接

- [[C语言进阶 - 字符串]] - 字符串基础知识
- [[C语言进阶 - 指针详解]] - 指针操作
- [[C语言标准库 - stdlib.h详解]] - 其他实用函数
- [[00_C_MOC]] - C语言知识地图

---

## 📚 参考资料

- C Standard Library Reference
- Secure Coding in C and C++
- https://en.cppreference.com/w/c/string

---

## ✅ 学习检查清单

- [ ] 理解strcpy和memcpy的区别
- [ ] 掌握strncpy的正确用法和陷阱
- [ ] 能够安全地连接字符串
- [ ] 掌握strcmp系列函数
- [ ] 会使用strchr和strstr搜索
- [ ] 理解strtok的工作原理和限制
- [ ] 掌握memset的正确用法
- [ ] 能够避免缓冲区溢出漏洞
- [ ] 实现一个安全的字符串操作函数库

---

*最后更新: 2025-11-18*
