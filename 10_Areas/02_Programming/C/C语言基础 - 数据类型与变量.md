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

#### 整型家族完整表

C语言提供了丰富的整型类型,满足不同场景的需求:

| 类型 | 典型大小(字节) | 范围(有符号) | 范围(无符号) | 格式说明符 |
|------|--------------|--------------|--------------|-----------|
| `char` | 1 | -128 ~ 127 | 0 ~ 255 | `%c` (字符), `%d` (整数) |
| `signed char` | 1 | -128 ~ 127 | - | `%d` |
| `unsigned char` | 1 | - | 0 ~ 255 | `%u` |
| `short` | 2 | -32,768 ~ 32,767 | - | `%hd` |
| `unsigned short` | 2 | - | 0 ~ 65,535 | `%hu` |
| `int` | 4 | -2,147,483,648 ~ 2,147,483,647 | - | `%d` |
| `unsigned int` | 4 | - | 0 ~ 4,294,967,295 | `%u` |
| `long` | 4/8 | 平台相关 | - | `%ld` |
| `unsigned long` | 4/8 | - | 平台相关 | `%lu` |
| `long long` | 8 | -9,223,372,036,854,775,808 ~ 9,223,372,036,854,775,807 | - | `%lld` |
| `unsigned long long` | 8 | - | 0 ~ 18,446,744,073,709,551,615 | `%llu` |

**完整示例:**
```c
#include <stdio.h>

int main() {
    // 各种整型的声明和使用
    char c = 'A';                          // 字符型
    signed char sc = -100;                 // 有符号字符
    unsigned char uc = 200;                // 无符号字符

    short s = 32000;                       // 短整型
    unsigned short us = 65000;             // 无符号短整型

    int i = 2000000000;                    // 整型
    unsigned int ui = 4000000000U;         // 无符号整型

    long l = 100000L;                      // 长整型
    unsigned long ul = 200000UL;           // 无符号长整型

    long long ll = 9000000000000000000LL;  // 长长整型
    unsigned long long ull = 18000000000000000000ULL;

    // 输出各种类型
    printf("char: %c (as int: %d)\n", c, c);
    printf("signed char: %d\n", sc);
    printf("unsigned char: %u\n", uc);
    printf("short: %hd\n", s);
    printf("unsigned short: %hu\n", us);
    printf("int: %d\n", i);
    printf("unsigned int: %u\n", ui);
    printf("long: %ld\n", l);
    printf("unsigned long: %lu\n", ul);
    printf("long long: %lld\n", ll);
    printf("unsigned long long: %llu\n", ull);

    return 0;
}
```

#### 不同平台下的大小差异

**C标准只规定了最小大小要求:**
- `char`: 至少8位
- `short`: 至少16位
- `int`: 至少16位
- `long`: 至少32位
- `long long`: 至少64位

**满足的关系:**
```
sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)
```

**常见平台差异:**

| 平台 | int | long | long long | 指针 |
|------|-----|------|-----------|------|
| **32位Linux/Windows** | 4字节 | 4字节 | 8字节 | 4字节 |
| **64位Linux (LP64)** | 4字节 | 8字节 | 8字节 | 8字节 |
| **64位Windows (LLP64)** | 4字节 | 4字节 | 8字节 | 8字节 |

**检测平台的代码:**
```c
#include <stdio.h>

int main() {
    printf("=== 数据类型大小 ===\n");
    printf("char:           %zu 字节\n", sizeof(char));
    printf("short:          %zu 字节\n", sizeof(short));
    printf("int:            %zu 字节\n", sizeof(int));
    printf("long:           %zu 字节\n", sizeof(long));
    printf("long long:      %zu 字节\n", sizeof(long long));
    printf("float:          %zu 字节\n", sizeof(float));
    printf("double:         %zu 字节\n", sizeof(double));
    printf("long double:    %zu 字节\n", sizeof(long double));
    printf("void*:          %zu 字节\n", sizeof(void*));

    printf("\n=== 平台信息 ===\n");
    #if defined(__LP64__) || defined(_WIN64)
        printf("64位平台\n");
    #else
        printf("32位平台\n");
    #endif

    return 0;
}
```

> [!tip] 可移植性建议
> 不要假设特定类型的大小,总是使用sizeof检查。如果需要固定大小的类型,使用stdint.h。

#### 固定宽度整型 (stdint.h)

为了解决跨平台的整型大小问题,C99引入了`<stdint.h>`,提供了固定宽度的整型:

**精确宽度整型 (Exact-width integer types):**
```c
#include <stdint.h>
#include <stdio.h>

int main() {
    // 精确宽度类型 - 保证特定位数
    int8_t   i8  = -128;           // 8位有符号整数
    uint8_t  u8  = 255;            // 8位无符号整数
    int16_t  i16 = -32768;         // 16位有符号整数
    uint16_t u16 = 65535;          // 16位无符号整数
    int32_t  i32 = -2147483648;    // 32位有符号整数
    uint32_t u32 = 4294967295U;    // 32位无符号整数
    int64_t  i64 = -9223372036854775807LL; // 64位有符号整数
    uint64_t u64 = 18446744073709551615ULL; // 64位无符号整数

    // 使用PRId宏打印(需要inttypes.h)
    printf("int8_t:   %" PRId8 "\n", i8);
    printf("uint8_t:  %" PRIu8 "\n", u8);
    printf("int16_t:  %" PRId16 "\n", i16);
    printf("uint16_t: %" PRIu16 "\n", u16);
    printf("int32_t:  %" PRId32 "\n", i32);
    printf("uint32_t: %" PRIu32 "\n", u32);
    printf("int64_t:  %" PRId64 "\n", i64);
    printf("uint64_t: %" PRIu64 "\n", u64);

    // 或者使用更简单的强制转换
    printf("\nint32_t:  %d\n", (int)i32);
    printf("uint32_t: %u\n", (unsigned)u32);

    return 0;
}
```

**最小宽度整型 (Minimum-width integer types):**
```c
int_least8_t   il8;   // 至少8位的最小有符号整型
uint_least8_t  ul8;   // 至少8位的最小无符号整型
int_least16_t  il16;  // 至少16位
int_least32_t  il32;  // 至少32位
int_least64_t  il64;  // 至少64位
```

**最快整型 (Fastest minimum-width integer types):**
```c
int_fast8_t   if8;    // 至少8位的最快整型
int_fast16_t  if16;   // 至少16位的最快整型
int_fast32_t  if32;   // 至少32位的最快整型
int_fast64_t  if64;   // 至少64位的最快整型
```

**指针大小整型:**
```c
intptr_t  iptr;       // 可以容纳指针的有符号整型
uintptr_t uptr;       // 可以容纳指针的无符号整型
```

**最大整型:**
```c
intmax_t  imax;       // 系统支持的最大有符号整型
uintmax_t umax;       // 系统支持的最大无符号整型
```

**实际应用示例:**
```c
#include <stdint.h>
#include <stdio.h>

// 网络协议中使用固定大小类型
struct packet_header {
    uint16_t packet_id;      // 2字节包ID
    uint32_t timestamp;      // 4字节时间戳
    uint64_t session_id;     // 8字节会话ID
};

// 文件格式中使用固定大小
struct bmp_header {
    uint16_t signature;      // 文件标识 "BM"
    uint32_t file_size;      // 文件大小
    uint32_t reserved;       // 保留字段
    uint32_t data_offset;    // 像素数据偏移
};

int main() {
    struct packet_header pkt;
    pkt.packet_id = 12345;
    pkt.timestamp = 1234567890;
    pkt.session_id = 9876543210123456789ULL;

    printf("包大小: %zu 字节\n", sizeof(pkt));
    printf("保证在所有平台上都是: 2 + 4 + 8 = 14 字节\n");

    return 0;
}
```

> [!tip] 何时使用固定宽度整型?
> - 文件格式定义
> - 网络协议实现
> - 跨平台数据交换
> - 位操作和硬件接口
> - 加密算法实现

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
long double ld = 3.141592653589793238L;  // 扩展精度浮点数
```

**浮点类型对比:**

| 类型 | 大小(字节) | 精度(十进制位) | 范围 | 格式说明符 |
|------|-----------|--------------|------|-----------|
| `float` | 4 | ~6-7位 | ±3.4E±38 | `%f`, `%e`, `%g` |
| `double` | 8 | ~15-16位 | ±1.7E±308 | `%lf`, `%le`, `%lg` |
| `long double` | 8/12/16 | 平台相关 | 平台相关 | `%Lf`, `%Le`, `%Lg` |

**注意事项:**
- `float`为单精度的小数值
- 不同类型数据进行运算时,比如两个整数相除,必须将除数或被除数强制转换成小数,否则小数点后面的数据会被忽略

```c
int a = 5, b = 2;
float result = (float)a / b;  // 强制类型转换
```

**浮点数使用示例:**
```c
#include <stdio.h>
#include <float.h>  // 浮点数极限值

int main() {
    float f = 3.14159265358979f;      // 声明float时加f后缀
    double d = 3.14159265358979;      // double是默认浮点类型
    long double ld = 3.14159265358979L; // 声明long double加L后缀

    // 不同格式输出
    printf("float:       %.10f\n", f);   // 精度丢失,约6-7位
    printf("double:      %.20lf\n", d);  // 精度更高,约15-16位
    printf("long double: %.20Lf\n", ld);

    // 科学计数法
    printf("\n科学计数法:\n");
    printf("%e\n", 12345.6789);    // 1.234568e+04
    printf("%E\n", 0.0001234);     // 1.234000E-04

    // 浮点数的范围
    printf("\n=== float范围 ===\n");
    printf("FLT_MIN:  %e\n", FLT_MIN);    // 最小正数
    printf("FLT_MAX:  %e\n", FLT_MAX);    // 最大值
    printf("FLT_EPSILON: %e\n", FLT_EPSILON); // 精度

    printf("\n=== double范围 ===\n");
    printf("DBL_MIN:  %e\n", DBL_MIN);
    printf("DBL_MAX:  %e\n", DBL_MAX);
    printf("DBL_EPSILON: %e\n", DBL_EPSILON);

    return 0;
}
```

#### 浮点数内部表示 (IEEE 754简介)

大多数现代计算机使用**IEEE 754标准**表示浮点数。

**float (32位) 的存储格式:**
```
符号位(1位) | 指数位(8位) | 尾数位(23位)
   S       |     E      |      M
```

**示例: 5.75的float表示**
```
5.75 = 101.11₂ = 1.0111₂ × 2²

符号位 S = 0 (正数)
指数位 E = 2 + 127 = 129 = 10000001₂  (偏移127)
尾数位 M = 0111... (省略前导1)

最终: 0 10000001 01110000000000000000000
```

**double (64位) 的存储格式:**
```
符号位(1位) | 指数位(11位) | 尾数位(52位)
   S       |     E       |      M
```

**特殊值:**
```c
#include <stdio.h>
#include <math.h>

int main() {
    // 正无穷
    double pos_inf = 1.0 / 0.0;  // +∞
    printf("正无穷: %f (isinf: %d)\n", pos_inf, isinf(pos_inf));

    // 负无穷
    double neg_inf = -1.0 / 0.0; // -∞
    printf("负无穷: %f\n", neg_inf);

    // NaN (Not a Number)
    double nan_val = 0.0 / 0.0;
    printf("NaN: %f (isnan: %d)\n", nan_val, isnan(nan_val));

    // 负零
    double neg_zero = -0.0;
    printf("负零: %f\n", neg_zero);

    // NaN的特性: NaN != NaN
    if (nan_val != nan_val) {
        printf("NaN不等于自己!\n");
    }

    return 0;
}
```

**浮点数精度问题:**
```c
#include <stdio.h>

int main() {
    // 问题1: 精度损失
    float f1 = 0.1f;
    float f2 = 0.2f;
    float sum = f1 + f2;
    printf("0.1 + 0.2 = %.20f\n", sum);  // 不是精确的0.3!

    // 问题2: 比较浮点数
    double a = 0.1 + 0.2;
    double b = 0.3;
    if (a == b) {  // 不推荐!
        printf("相等\n");
    } else {
        printf("不相等! a=%.20lf, b=%.20lf\n", a, b);
    }

    // 正确做法: 使用epsilon比较
    #define EPSILON 1e-9
    if (fabs(a - b) < EPSILON) {
        printf("在误差范围内相等\n");
    }

    // 问题3: 大数吃小数
    float big = 1e20f;
    float small = 1.0f;
    printf("1e20 + 1 = %.0f\n", big + small);  // 结果还是1e20!

    // 问题4: 累加误差
    float sum2 = 0.0f;
    for (int i = 0; i < 10000000; i++) {
        sum2 += 0.1f;
    }
    printf("0.1累加1000万次 = %.2f\n", sum2);  // 不是1000000!

    return 0;
}
```

> [!warning] 浮点数注意事项
> 1. **永远不要用 == 比较浮点数**,使用epsilon容差比较
> 2. **不要在循环条件中使用浮点数**,如`for(float f=0; f!=1.0; f+=0.1)`可能死循环
> 3. **避免大数和小数相加**,精度会丢失
> 4. **金融计算不要用float/double**,使用整数(分)或专门的十进制库
> 5. **了解精度限制**: float约7位有效数字,double约16位

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

### 类型转换详解

#### 隐式类型转换(自动类型转换)

**发生时机:**
- 混合类型运算
- 赋值操作
- 函数参数传递
- 函数返回值

**转换规则 - 算术转换(Usual Arithmetic Conversions):**
```
低精度 → 高精度

char/short → int → unsigned int → long → unsigned long →
long long → unsigned long long → float → double → long double
```

**示例:**
```c
#include <stdio.h>

int main() {
    // 1. 整型提升
    char c = 100;
    int i = c;  // char自动转换为int
    printf("char转int: %d\n", i);

    // 2. 混合运算
    int a = 10;
    double b = 3.5;
    double result = a + b;  // a自动转换为double,结果为13.5
    printf("int + double = %.1lf\n", result);

    // 3. 赋值转换
    double d = 9.8;
    int j = d;  // 小数部分被截断!
    printf("double转int: %d (丢失小数)\n", j);  // 9

    // 4. 有符号和无符号混合(危险!)
    int signed_val = -1;
    unsigned int unsigned_val = 1;
    if (signed_val < unsigned_val) {  // -1转为无符号大数!
        printf("预期: -1 < 1\n");
    } else {
        printf("实际: %d被转换为无符号%u!\n", signed_val, (unsigned)signed_val);
    }

    return 0;
}
```

#### 整型提升 (Integer Promotion)

**规则:** 在表达式中,`char`和`short`类型会自动提升为`int`

```c
#include <stdio.h>

int main() {
    char c1 = 100;
    char c2 = 50;

    // c1和c2都提升为int再运算
    int result = c1 + c2;  // 以int精度计算
    printf("100 + 50 = %d\n", result);

    // 验证提升
    printf("sizeof(c1 + c2) = %zu\n", sizeof(c1 + c2));  // 4 (int的大小)
    printf("sizeof(c1) = %zu\n", sizeof(c1));            // 1 (char的大小)

    // 位运算中的整型提升
    unsigned char uc = 0xFF;
    unsigned int result2 = ~uc;  // uc提升为int再取反
    printf("~0xFF = 0x%X (期望0x00,实际0xFFFFFF00)\n", result2);

    // 正确做法
    unsigned int result3 = ~uc & 0xFF;
    printf("正确结果: 0x%X\n", result3);  // 0x00

    return 0;
}
```

#### 显式类型转换(强制类型转换)

**语法:**
```c
(目标类型) 表达式
```

**常见用途:**
```c
#include <stdio.h>

int main() {
    // 1. 整数除法转浮点除法
    int a = 5, b = 2;
    double result1 = a / b;              // 2.0 (整数除法后转double)
    double result2 = (double)a / b;      // 2.5 (正确!)
    printf("5/2 = %.1lf (错误), (double)5/2 = %.1lf (正确)\n", result1, result2);

    // 2. 防止整数溢出
    int x = 100000;
    int y = 100000;
    long long product = (long long)x * y;  // 先转long long再乘
    printf("100000 * 100000 = %lld\n", product);

    // 错误示例
    long long wrong = x * y;  // 先以int计算(溢出),再转long long
    printf("错误结果: %lld\n", wrong);

    // 3. 指针类型转换
    int num = 0x12345678;
    unsigned char *ptr = (unsigned char*)&num;
    printf("字节序: ");
    for (int i = 0; i < sizeof(num); i++) {
        printf("%02X ", ptr[i]);
    }
    printf("\n");

    // 4. void指针转换
    void *vp = &num;
    int *ip = (int*)vp;
    printf("通过void*访问: 0x%X\n", *ip);

    return 0;
}
```

#### 常见类型转换陷阱

**陷阱1: 有符号和无符号混合运算**
```c
#include <stdio.h>

int main() {
    // 问题: -1与unsigned比较
    int a = -1;
    unsigned int b = 1;

    if (a < b) {
        printf("正常: -1 < 1\n");
    } else {
        printf("异常: a=%d 转为unsigned后 a=%u > b=%u\n", a, (unsigned)a, b);
    }

    // 问题: 数组索引
    unsigned int size = 10;
    for (int i = size - 11; i < size; i++) {  // i=-1转为超大正数!
        printf("i = %d\n", i);  // 可能死循环或越界
    }

    // 正确做法
    for (int i = 0; i < (int)size; i++) {
        // 安全
    }

    return 0;
}
```

**陷阱2: 窄化转换丢失数据**
```c
#include <stdio.h>

int main() {
    // long long → int
    long long big = 10000000000LL;  // 100亿
    int small = big;  // 溢出!
    printf("100亿转int: %d (数据丢失)\n", small);

    // double → float
    double d = 3.141592653589793;
    float f = d;  // 精度丢失
    printf("double: %.15lf\n", d);
    printf("float:  %.15f\n", f);

    // int → char
    int large = 300;
    char c = large;  // 只保留低8位
    printf("300转char: %d (溢出)\n", c);

    return 0;
}
```

**陷阱3: 浮点数转整数截断**
```c
#include <stdio.h>
#include <math.h>

int main() {
    double values[] = {1.2, 1.5, 1.8, -1.2, -1.5, -1.8};

    printf("直接转换(截断):\n");
    for (int i = 0; i < 6; i++) {
        printf("%.1lf → %d\n", values[i], (int)values[i]);
    }

    printf("\n四舍五入(正确):\n");
    for (int i = 0; i < 6; i++) {
        printf("%.1lf → %d\n", values[i], (int)round(values[i]));
    }

    printf("\n向上取整:\n");
    for (int i = 0; i < 6; i++) {
        printf("%.1lf → %d\n", values[i], (int)ceil(values[i]));
    }

    printf("\n向下取整:\n");
    for (int i = 0; i < 6; i++) {
        printf("%.1lf → %d\n", values[i], (int)floor(values[i]));
    }

    return 0;
}
```

**类型转换最佳实践:**

| 场景 | 推荐做法 | 避免 |
|------|---------|------|
| 整数除法保留小数 | `(double)a / b` | `a / b` |
| 防止整数溢出 | `(long long)a * b` | `a * b` 后转换 |
| 有无符号混合 | 统一类型 | 直接比较 |
| 指针转换 | 明确类型转换 | 隐式转换 |
| 浮点数取整 | `round()`/`ceil()`/`floor()` | 直接转int |

### 变量作用域和生命周期

#### 局部变量

**定义:** 在函数或代码块内声明的变量

**特点:**
- 作用域: 声明位置到代码块结束
- 生命周期: 进入代码块时创建,退出时销毁
- 存储位置: 栈(stack)
- 默认值: 未初始化(随机值)

```c
#include <stdio.h>

void func() {
    int local = 10;  // 局部变量
    printf("func中的local: %d\n", local);
}  // local在这里被销毁

int main() {
    int local = 20;  // 另一个局部变量
    printf("main中的local: %d\n", local);

    {
        int local = 30;  // 代码块内的局部变量(覆盖外层)
        printf("代码块中的local: %d\n", local);
    }  // 这个local被销毁

    printf("代码块后的local: %d\n", local);  // 20

    func();

    // printf("%d\n", local);  // 错误!func中的local不可见

    return 0;
}
```

**未初始化的危险:**
```c
#include <stdio.h>

int main() {
    int uninitialized;  // 未初始化,值不确定!
    printf("未初始化的值: %d (随机!)\n", uninitialized);

    // 正确做法: 总是初始化
    int initialized = 0;
    printf("已初始化的值: %d\n", initialized);

    return 0;
}
```

#### 全局变量

**定义:** 在所有函数外部声明的变量

**特点:**
- 作用域: 整个程序
- 生命周期: 程序开始到结束
- 存储位置: 数据段(data segment)
- 默认值: 自动初始化为0

```c
#include <stdio.h>

int global_var = 100;  // 全局变量,所有函数可见

void modify_global() {
    global_var = 200;  // 可以修改全局变量
    printf("modify_global中: %d\n", global_var);
}

int another_global;  // 未显式初始化,自动为0

int main() {
    printf("main中: %d\n", global_var);
    modify_global();
    printf("修改后: %d\n", global_var);
    printf("another_global自动初始化为: %d\n", another_global);

    return 0;
}
```

**全局变量的危害:**
```c
// 文件1: module1.c
int shared_counter = 0;  // 全局变量

void increment() {
    shared_counter++;  // 副作用!
}

// 文件2: module2.c
extern int shared_counter;

void reset() {
    shared_counter = 0;  // 另一个副作用!
}

// 问题: shared_counter的值难以追踪,任何函数都能修改它
```

> [!warning] 避免滥用全局变量
> - 破坏封装性
> - 难以调试和维护
> - 线程不安全
> - 命名冲突风险
>
> 推荐:使用局部变量+参数传递,或使用static限制作用域

#### 静态变量 (static)

**静态局部变量:**
```c
#include <stdio.h>

void counter() {
    static int count = 0;  // 静态局部变量,只初始化一次
    count++;
    printf("count = %d\n", count);
}

int main() {
    counter();  // count = 1
    counter();  // count = 2
    counter();  // count = 3
    counter();  // count = 4

    // printf("%d\n", count);  // 错误!count作用域仅在counter内

    return 0;
}
```

**特点:**
- 作用域: 声明所在的函数/代码块
- 生命周期: 程序开始到结束
- 只初始化一次
- 保持值在函数调用之间

**静态全局变量:**
```c
// file1.c
static int file_scope_var = 10;  // 只在file1.c中可见

void func1() {
    printf("%d\n", file_scope_var);  // 可以访问
}

// file2.c
// extern int file_scope_var;  // 错误!无法访问static全局变量
```

**用途: 模块内私有变量**

#### 存储类别关键字

**auto (自动变量,很少用)**
```c
void func() {
    auto int x = 10;  // 等价于 int x = 10;
    // auto是默认的局部变量存储类别
}
```

**register (寄存器变量)**
```c
void fast_loop() {
    register int i;  // 建议编译器将i放在寄存器中
    for (i = 0; i < 1000000; i++) {
        // 快速访问i
    }
    // 注意: 不能对register变量取地址
    // int *ptr = &i;  // 错误!
}
```

**static (静态变量)**
- 局部static: 保持值,局部作用域
- 全局static: 限制在文件内

**extern (外部变量)**
```c
// file1.c
int shared_var = 100;  // 定义

// file2.c
extern int shared_var;  // 声明(不分配内存)

void use_shared() {
    printf("%d\n", shared_var);  // 使用file1.c中定义的变量
}
```

**存储类别总结:**

| 存储类别 | 位置 | 默认值 | 生命周期 | 作用域 |
|----------|------|--------|----------|--------|
| auto | 栈 | 随机 | 代码块 | 代码块 |
| register | 寄存器 | 随机 | 代码块 | 代码块 |
| static局部 | 数据段 | 0 | 程序运行期 | 代码块 |
| static全局 | 数据段 | 0 | 程序运行期 | 当前文件 |
| extern | 数据段 | 0 | 程序运行期 | 全局 |
| 全局 | 数据段 | 0 | 程序运行期 | 全局 |

**实战示例 - 计数器模块:**
```c
// counter.h
#ifndef COUNTER_H
#define COUNTER_H

void increment_counter(void);
void reset_counter(void);
int get_counter(void);

#endif

// counter.c
#include "counter.h"

static int counter = 0;  // 文件内私有,外部无法直接访问

void increment_counter(void) {
    counter++;
}

void reset_counter(void) {
    counter = 0;
}

int get_counter(void) {
    return counter;
}

// main.c
#include <stdio.h>
#include "counter.h"

int main() {
    increment_counter();
    increment_counter();
    printf("计数: %d\n", get_counter());  // 2

    reset_counter();
    printf("重置后: %d\n", get_counter());  // 0

    // counter = 100;  // 错误!counter不可见

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

### 格式化输入输出进阶

#### printf高级格式控制

**基本语法:**
```
%[flags][width][.precision][length]specifier
```

**标志 (flags):**
```c
#include <stdio.h>

int main() {
    int num = 42;
    double pi = 3.14159;

    // - : 左对齐
    printf("|%-10d|\n", num);      // |42        |
    printf("|%10d|\n", num);       // |        42|

    // + : 显示符号
    printf("%+d\n", num);          // +42
    printf("%+d\n", -num);         // -42

    // 空格 : 正数前加空格
    printf("% d\n", num);          //  42
    printf("% d\n", -num);         // -42

    // 0 : 零填充
    printf("%010d\n", num);        // 0000000042

    // # : 替代格式
    printf("%#x\n", 255);          // 0xff (十六进制前缀)
    printf("%#o\n", 64);           // 0100 (八进制前缀)
    printf("%#f\n", pi);           // 3.141590 (保证小数点)

    return 0;
}
```

**宽度和精度:**
```c
#include <stdio.h>

int main() {
    int num = 123;
    double pi = 3.14159265;
    char *str = "Hello";

    // 宽度控制
    printf("|%5d|\n", num);        // |  123|
    printf("|%10s|\n", str);       // |     Hello|

    // 精度控制
    printf("%.2f\n", pi);          // 3.14 (保留2位小数)
    printf("%.5f\n", pi);          // 3.14159
    printf("%.10f\n", pi);         // 3.1415926500

    // 字符串精度(最大字符数)
    printf("%.3s\n", str);         // Hel

    // 宽度+精度
    printf("|%10.2f|\n", pi);      // |      3.14|
    printf("|%10.5s|\n", str);     // |     Hello|

    // 动态宽度和精度
    int width = 10;
    int precision = 3;
    printf("|%*.*f|\n", width, precision, pi);  // |     3.142|

    return 0;
}
```

**长度修饰符:**
```c
#include <stdio.h>
#include <stdint.h>

int main() {
    // hh: char
    char c = 'A';
    printf("%hhd\n", c);           // 65

    // h: short
    short s = 32767;
    printf("%hd\n", s);

    // l: long
    long l = 1234567890L;
    printf("%ld\n", l);

    // ll: long long
    long long ll = 123456789012345LL;
    printf("%lld\n", ll);

    // z: size_t
    size_t sz = sizeof(int);
    printf("%zu\n", sz);

    // t: ptrdiff_t
    ptrdiff_t diff = 100;
    printf("%td\n", diff);

    return 0;
}
```

**实用技巧 - 对齐表格:**
```c
#include <stdio.h>

int main() {
    printf("%-10s %8s %10s\n", "Name", "Age", "Salary");
    printf("%-10s %8s %10s\n", "----------", "--------", "----------");
    printf("%-10s %8d %10.2f\n", "Alice", 30, 5000.50);
    printf("%-10s %8d %10.2f\n", "Bob", 25, 4500.00);
    printf("%-10s %8d %10.2f\n", "Charlie", 35, 6000.75);

    /*输出:
    Name            Age     Salary
    ----------  --------  ----------
    Alice             30     5000.50
    Bob               25     4500.00
    Charlie           35     6000.75
    */

    return 0;
}
```

#### scanf的常见陷阱和解决方案

**陷阱1: 缓冲区遗留的换行符**
```c
#include <stdio.h>

int main() {
    int age;
    char grade;

    printf("输入年龄: ");
    scanf("%d", &age);  // 输入"25\n",\n留在缓冲区

    printf("输入等级: ");
    scanf("%c", &grade);  // 直接读取\n!

    printf("年龄: %d, 等级: %c\n", age, grade);

    // 解决方案1: 在%c前加空格
    scanf(" %c", &grade);  // 空格会跳过空白字符

    // 解决方案2: 清空缓冲区
    while (getchar() != '\n');

    return 0;
}
```

**陷阱2: scanf无法读取空格**
```c
#include <stdio.h>

int main() {
    char name[50];

    printf("输入姓名: ");
    scanf("%s", name);  // 输入"John Doe",只读取"John"

    printf("姓名: %s\n", name);  // 输出: John

    // 解决方案: 使用fgets
    fgets(name, sizeof(name), stdin);

    // 或使用scanf的字符集
    scanf("%[^\n]", name);  // 读取直到换行

    return 0;
}
```

**陷阱3: 缓冲区溢出**
```c
#include <stdio.h>

int main() {
    char buffer[10];

    printf("输入字符串: ");
    scanf("%s", buffer);  // 危险!如果输入超过9个字符会溢出

    // 解决方案: 限制读取长度
    scanf("%9s", buffer);  // 最多读9个字符(留1个给\0)

    return 0;
}
```

**陷阱4: scanf返回值未检查**
```c
#include <stdio.h>

int main() {
    int num;
    int ret;

    printf("输入整数: ");
    ret = scanf("%d", &num);  // 输入非数字,scanf失败

    if (ret != 1) {
        printf("输入无效!\n");
        // 清空错误输入
        while (getchar() != '\n');
    } else {
        printf("输入: %d\n", num);
    }

    return 0;
}
```

#### 安全的输入处理

**推荐: 使用fgets + sscanf**
```c
#include <stdio.h>
#include <string.h>

int main() {
    char line[100];
    int age;
    char name[50];

    // 读取整行
    printf("输入年龄: ");
    if (fgets(line, sizeof(line), stdin) != NULL) {
        // 去除换行符
        line[strcspn(line, "\n")] = '\0';

        // 解析
        if (sscanf(line, "%d", &age) == 1) {
            printf("年龄: %d\n", age);
        } else {
            printf("无效输入\n");
        }
    }

    // 读取字符串(含空格)
    printf("输入姓名: ");
    if (fgets(name, sizeof(name), stdin) != NULL) {
        name[strcspn(name, "\n")] = '\0';
        printf("姓名: %s\n", name);
    }

    return 0;
}
```

**输入验证函数:**
```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

// 安全读取整数
int read_int(const char *prompt, int *value) {
    char line[100];

    printf("%s", prompt);
    if (fgets(line, sizeof(line), stdin) == NULL) {
        return 0;  // 读取失败
    }

    // 去除换行符
    line[strcspn(line, "\n")] = '\0';

    // 使用strtol转换
    char *endptr;
    errno = 0;
    long val = strtol(line, &endptr, 10);

    // 检查转换是否成功
    if (errno != 0 || *endptr != '\0' || endptr == line) {
        return 0;  // 转换失败
    }

    *value = (int)val;
    return 1;  // 成功
}

int main() {
    int age;

    while (1) {
        if (read_int("输入年龄 (1-120): ", &age)) {
            if (age >= 1 && age <= 120) {
                printf("年龄: %d\n", age);
                break;
            } else {
                printf("年龄必须在1-120之间\n");
            }
        } else {
            printf("输入无效,请输入整数\n");
        }
    }

    return 0;
}
```

### 常见陷阱

#### 1. 未初始化变量
```c
#include <stdio.h>

int main() {
    int x;  // 未初始化,值不确定!

    if (x == 0) {  // 未定义行为!
        printf("x是0\n");
    }

    // 正确做法
    int y = 0;  // 总是初始化!

    return 0;
}
```

#### 2. 整数溢出的危害
```c
#include <stdio.h>
#include <limits.h>

int main() {
    // 有符号整数溢出(未定义行为)
    int max = INT_MAX;  // 2147483647
    int overflow = max + 1;  // 溢出!结果未定义
    printf("INT_MAX + 1 = %d\n", overflow);  // 通常是INT_MIN

    // 无符号整数溢出(定义为回绕)
    unsigned int umax = UINT_MAX;
    unsigned int uwrap = umax + 1;  // 回绕到0
    printf("UINT_MAX + 1 = %u\n", uwrap);  // 0

    // 乘法溢出
    int a = 100000;
    int b = 100000;
    int product = a * b;  // 溢出!
    printf("100000 * 100000 = %d (错误)\n", product);

    // 正确做法
    long long correct = (long long)a * b;
    printf("正确结果: %lld\n", correct);

    // 检测溢出(加法)
    if (a > 0 && b > 0 && a > INT_MAX - b) {
        printf("加法会溢出!\n");
    }

    return 0;
}
```

#### 3. 符号扩展问题
```c
#include <stdio.h>

int main() {
    char c = 0xFF;  // -1 (如果char是signed)

    // 符号扩展
    int i = c;  // 提升为int时符号扩展为0xFFFFFFFF (-1)
    printf("char 0xFF as int: 0x%X\n", i);

    // 避免符号扩展
    unsigned char uc = 0xFF;
    int j = uc;  // 零扩展为0x000000FF (255)
    printf("unsigned char 0xFF as int: 0x%X\n", j);

    // 位掩码
    int k = c & 0xFF;  // 清除扩展的符号位
    printf("masked: 0x%X\n", k);

    return 0;
}
```

#### 4. 宏定义 vs const常量
```c
#include <stdio.h>

// 宏定义(文本替换)
#define MACRO_MAX 100
#define MACRO_SQUARE(x) ((x) * (x))  // 需要加括号!

// const常量
const int CONST_MAX = 100;

int main() {
    // 宏的问题1: 没有类型检查
    int arr1[MACRO_MAX];  // OK
    // int arr2[CONST_MAX];  // C89中错误(C99+可以)

    // 宏的问题2: 多次求值
    int x = 5;
    int result1 = MACRO_SQUARE(x++);  // ((x++) * (x++)) - 错误!
    printf("MACRO_SQUARE(x++): %d, x=%d\n", result1, x);

    // const的优点: 类型安全,作用域受限
    const int y = 10;
    // y = 20;  // 编译错误

    // const指针
    const int *ptr1 = &x;    // 指向const int
    // *ptr1 = 10;  // 错误
    ptr1 = &y;  // OK

    int *const ptr2 = &x;    // const指针
    *ptr2 = 10;  // OK
    // ptr2 = &y;  // 错误

    const int *const ptr3 = &x;  // const指针指向const int
    // *ptr3 = 10;  // 错误
    // ptr3 = &y;  // 错误

    return 0;
}
```

**宏 vs const对比:**

| 特性 | #define | const |
|------|---------|-------|
| 类型检查 | 无 | 有 |
| 调试 | 困难(已替换) | 容易(符号存在) |
| 作用域 | 文件范围 | 块作用域 |
| 内存 | 无(文本替换) | 占用内存 |
| 数组大小 | C89可用 | C99+可用 |
| 指针 | 不可取地址 | 可以 |

**建议:**
- 简单常量: 优先使用`const`
- 数组大小(C89): 使用`#define`或`enum`
- 宏函数: 谨慎使用,或改用inline函数(C99+)

### 实战示例

#### 示例1: 温度转换程序
```c
#include <stdio.h>

// 摄氏转华氏: F = C × 9/5 + 32
double celsius_to_fahrenheit(double celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

// 华氏转摄氏: C = (F - 32) × 5/9
double fahrenheit_to_celsius(double fahrenheit) {
    return (fahrenheit - 32.0) * 5.0 / 9.0;
}

int main() {
    int choice;
    double temp, result;

    printf("=== 温度转换器 ===\n");
    printf("1. 摄氏 → 华氏\n");
    printf("2. 华氏 → 摄氏\n");
    printf("请选择: ");
    scanf("%d", &choice);

    printf("输入温度: ");
    scanf("%lf", &temp);

    switch (choice) {
        case 1:
            result = celsius_to_fahrenheit(temp);
            printf("%.2lf°C = %.2lf°F\n", temp, result);
            break;
        case 2:
            result = fahrenheit_to_celsius(temp);
            printf("%.2lf°F = %.2lf°C\n", temp, result);
            break;
        default:
            printf("无效选择\n");
            return 1;
    }

    // 温度范围提示
    if (choice == 1) {
        if (result > 100) {
            printf("提示: 水的沸点是212°F\n");
        } else if (result < 32) {
            printf("提示: 水的冰点是32°F\n");
        }
    }

    return 0;
}
```

#### 示例2: 增强型计算器
```c
#include <stdio.h>
#include <math.h>

int main() {
    char op;
    double num1, num2, result;
    int valid = 1;

    printf("=== 计算器 ===\n");
    printf("支持: + - * / %% ^ (幂) s (平方根)\n");

    printf("输入运算符: ");
    scanf(" %c", &op);

    if (op == 's') {
        printf("输入数字: ");
        scanf("%lf", &num1);
        if (num1 < 0) {
            printf("错误: 不能对负数开平方根\n");
            return 1;
        }
        result = sqrt(num1);
        printf("√%.2lf = %.6lf\n", num1, result);
    } else {
        printf("输入两个数字: ");
        scanf("%lf %lf", &num1, &num2);

        switch (op) {
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '*':
                result = num1 * num2;
                break;
            case '/':
                if (num2 == 0.0) {
                    printf("错误: 除数不能为0\n");
                    valid = 0;
                } else {
                    result = num1 / num2;
                }
                break;
            case '%':
                if (num2 == 0.0) {
                    printf("错误: 除数不能为0\n");
                    valid = 0;
                } else {
                    result = fmod(num1, num2);
                }
                break;
            case '^':
                result = pow(num1, num2);
                break;
            default:
                printf("错误: 无效的运算符\n");
                valid = 0;
        }

        if (valid) {
            printf("%.2lf %c %.2lf = %.6lf\n", num1, op, num2, result);
        }
    }

    return 0;
}
```

#### 示例3: 数值范围检查工具
```c
#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <stdint.h>

void print_type_info(const char *type_name, long long min, unsigned long long max, int is_unsigned) {
    printf("%-20s ", type_name);
    if (is_unsigned) {
        printf("0 ~ %llu", max);
    } else {
        printf("%lld ~ %lld", min, (long long)max);
    }
    printf("\n");
}

int main() {
    printf("=== 整型范围 ===\n");
    print_type_info("char", CHAR_MIN, CHAR_MAX, 0);
    print_type_info("signed char", SCHAR_MIN, SCHAR_MAX, 0);
    print_type_info("unsigned char", 0, UCHAR_MAX, 1);
    print_type_info("short", SHRT_MIN, SHRT_MAX, 0);
    print_type_info("unsigned short", 0, USHRT_MAX, 1);
    print_type_info("int", INT_MIN, INT_MAX, 0);
    print_type_info("unsigned int", 0, UINT_MAX, 1);
    print_type_info("long", LONG_MIN, LONG_MAX, 0);
    print_type_info("unsigned long", 0, ULONG_MAX, 1);

    printf("\n=== 浮点型信息 ===\n");
    printf("%-20s 精度: %d位, 范围: %e ~ %e\n",
           "float", FLT_DIG, FLT_MIN, FLT_MAX);
    printf("%-20s 精度: %d位, 范围: %e ~ %e\n",
           "double", DBL_DIG, DBL_MIN, DBL_MAX);
    printf("%-20s epsilon: %e\n", "float", FLT_EPSILON);
    printf("%-20s epsilon: %e\n", "double", DBL_EPSILON);

    printf("\n=== 固定宽度整型 ===\n");
    printf("%-20s %zu字节\n", "int8_t", sizeof(int8_t));
    printf("%-20s %zu字节\n", "int16_t", sizeof(int16_t));
    printf("%-20s %zu字节\n", "int32_t", sizeof(int32_t));
    printf("%-20s %zu字节\n", "int64_t", sizeof(int64_t));

    // 检查用户输入的值是否在范围内
    printf("\n=== 范围检查 ===\n");
    long long value;
    printf("输入一个整数: ");
    scanf("%lld", &value);

    if (value >= CHAR_MIN && value <= CHAR_MAX) {
        printf("可以用 char 存储\n");
    }
    if (value >= 0 && value <= UCHAR_MAX) {
        printf("可以用 unsigned char 存储\n");
    }
    if (value >= SHRT_MIN && value <= SHRT_MAX) {
        printf("可以用 short 存储\n");
    }
    if (value >= INT_MIN && value <= INT_MAX) {
        printf("可以用 int 存储\n");
    }

    return 0;
}
```

**编译运行:**
```bash
gcc -o temp_converter temp_converter.c -lm
./temp_converter

gcc -o calculator calculator.c -lm
./calculator

gcc -o type_info type_info.c
./type_info
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
**注意**: 避免有符号和无符号混合运算,会导致意外的类型转换!

### Q3: sizeof返回的单位是什么?
**A**: `sizeof`返回的是字节数(bytes),类型是`size_t`。例如在大多数系统上,`sizeof(int)`返回4,表示int类型占用4个字节。

### Q4: 为什么scanf需要&符号?
**A**: `&`是取地址运算符,`scanf`需要知道变量的内存地址才能将输入的值存储到该位置。而数组名本身就是地址,所以不需要`&`。

### Q5: float和double如何选择?
**A**:
- **float**: 4字节,6-7位有效数字,用于对精度要求不高的场景(图形学坐标等)
- **double**: 8字节,15-16位有效数字,是浮点运算的默认类型
- **建议**: 除非内存非常紧张或有特殊性能需求,默认使用double

### Q6: 如何检测整数溢出?
**A**:
```c
// 加法溢出检测
if (a > 0 && b > 0 && a > INT_MAX - b) {
    // 溢出
}

// 乘法溢出检测
if (a > INT_MAX / b) {
    // 溢出
}

// 或使用更大的类型
long long result = (long long)a * b;
if (result > INT_MAX) {
    // 溢出
}
```

### Q7: 全局变量和static变量有什么区别?
**A**:
- **全局变量**: 整个程序可见,跨文件(extern)
- **static全局变量**: 只在当前文件可见
- **static局部变量**: 只在函数内可见,但生命周期是整个程序运行期

### Q8: 为什么不能用==比较浮点数?
**A**: 浮点数在计算机中用二进制表示,很多十进制小数无法精确表示。例如0.1+0.2不等于0.3。正确做法是使用误差范围比较:
```c
#define EPSILON 1e-9
if (fabs(a - b) < EPSILON) {
    // 认为相等
}
```

### Q9: char是有符号还是无符号?
**A**: **取决于编译器和平台**。某些平台char默认有符号,某些无符号。如果需要明确,使用`signed char`或`unsigned char`。处理二进制数据时务必使用`unsigned char`。

### Q10: 如何在32位和64位平台之间编写可移植代码?
**A**:
1. 使用`stdint.h`的固定宽度类型(`int32_t`等)
2. 使用`size_t`表示大小
3. 使用`intptr_t`/`uintptr_t`表示指针大小的整数
4. 不要假设`int`或`long`的大小
5. 使用`sizeof`而不是硬编码大小

## 🚀 Tasks

### 基础练习
- [ ] 编写程序测试各数据类型的大小和范围
- [ ] 实现所有整型家族的范围输出程序
- [ ] 练习使用各种占位符进行格式化输出(对齐表格)
- [ ] 演示浮点数精度问题和正确的比较方法

### 类型转换练习
- [ ] 实现一个程序,演示隐式类型转换的各种情况
- [ ] 编写代码展示整型提升的效果
- [ ] 实现安全的类型转换函数(带溢出检测)
- [ ] 演示有符号和无符号混合运算的陷阱

### 作用域练习
- [ ] 实现一个使用static局部变量的计数器
- [ ] 编写多文件程序,练习extern的使用
- [ ] 创建一个模块,使用static全局变量实现封装

### 输入输出练习
- [ ] 实现安全的输入验证函数(整数、浮点数、字符串)
- [ ] 编写格式化表格输出程序
- [ ] 使用fgets+sscanf实现健壮的输入处理

### 实战项目
- [x] 完成温度转换器(摄氏/华氏/开尔文)
- [x] 实现增强型计算器(基本运算+幂+开方)
- [x] 编写数值范围检查工具
- [ ] 实现单位转换器(长度/重量/体积)
- [ ] 编写BMI计算器(包含输入验证)
- [ ] 实现简单的数值类型转换工具

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C语言程序设计(谭浩强)
* <limits.h>头文件文档
* <stdint.h>头文件文档
* <float.h>头文件文档
* IEEE 754浮点数标准
* C标准: ISO/IEC 9899

## 🕸️ Relation
### C语言知识体系
* [[00_C_MOC|C语言知识体系]] - 本笔记是C语言的基础核心
* [[C语言基础 - 控制流]] - 控制流中会大量使用数据类型和变量
* [[C语言基础 - 函数]] - 函数参数和返回值涉及类型转换
* [[C语言基础 - 数组]] - 数组需要理解数据类型的概念
* [[C语言进阶 - 指针详解]] - 指针类型与数据类型密切相关

### 相关主题
* [[C标准库 - stdio.h详解]] - 格式化输入输出的详细说明
* [[C标准库 - limits.h与float.h]] - 数值极限的完整参考
* [[C标准库 - stdint.h详解]] - 固定宽度整型的完整说明
* [[C语言进阶 - 内存布局]] - 理解变量的存储位置
* [[C语言进阶 - 位操作详解]] - 整型的位级操作

### 系统编程应用
* [[Linux系统编程 - 数据类型]] - Linux特定的数据类型
* [[C语言实战 - 跨平台编程]] - 处理平台差异
* [[C语言安全编程]] - 避免溢出和类型转换陷阱
