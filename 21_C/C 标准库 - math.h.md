---
created: 2025-11-18
tags:
  - type/reference
  - topic/programming/c
---
## 📋 概述

`math.h` 提供了标准数学函数，包括：
- **三角函数** (sin, cos, tan, asin, acos, atan)
- **指数和对数** (exp, log, log10, pow)
- **开方和幂运算** (sqrt, cbrt, pow)
- **取整函数** (ceil, floor, round, trunc)
- **浮点运算** (fabs, fmod, modf)
- **特殊函数** (hypot, erf)

⚠️ **编译时需要链接数学库**：`gcc program.c -lm`

---

## 🎯 学习目标

- [ ] 掌握基本三角函数的使用
- [ ] 理解弧度制和角度制的转换
- [ ] 掌握指数和对数运算
- [ ] 学会使用取整函数的区别
- [ ] 理解浮点数的特殊值（NaN, Infinity）
- [ ] 掌握实用数学函数的应用场景

---

## 📚 核心内容

### 重要宏定义

```c
M_PI        // π ≈ 3.14159265358979323846 (部分编译器，非标准)
M_E         // e ≈ 2.71828182845904523536 (部分编译器，非标准)
INFINITY    // 正无穷大 (C99)
NAN         // Not a Number (C99)
HUGE_VAL    // 表示正无穷大的double值
HUGE_VALF   // 表示正无穷大的float值 (C99)
HUGE_VALL   // 表示正无穷大的long double值 (C99)
```

**注意**：M_PI 和 M_E 不是C标准的一部分，需要定义 `_USE_MATH_DEFINES` 或手动定义：

```c
#define _USE_MATH_DEFINES
#include <math.h>

// 或者
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
```

---

## 🔧 函数详解

### 一、三角函数

#### 1. sin/cos/tan - 基本三角函数 ⭐⭐⭐⭐

```c
double sin(double x);
double cos(double x);
double tan(double x);
```

**功能**：计算三角函数值（输入为弧度）。

**参数**：
- `x`：角度（弧度制）

**返回值**：三角函数值

**示例**：

```c
#include <stdio.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

int main() {
    // 计算特殊角的三角函数值
    printf("sin(0°) = %.4f\n", sin(0));                    // 0.0000
    printf("sin(30°) = %.4f\n", sin(M_PI / 6));            // 0.5000
    printf("sin(45°) = %.4f\n", sin(M_PI / 4));            // 0.7071
    printf("sin(90°) = %.4f\n", sin(M_PI / 2));            // 1.0000

    printf("cos(0°) = %.4f\n", cos(0));                    // 1.0000
    printf("cos(60°) = %.4f\n", cos(M_PI / 3));            // 0.5000
    printf("cos(90°) = %.4f\n", cos(M_PI / 2));            // 0.0000

    printf("tan(0°) = %.4f\n", tan(0));                    // 0.0000
    printf("tan(45°) = %.4f\n", tan(M_PI / 4));            // 1.0000

    return 0;
}
```

**角度与弧度转换**：

```c
// 角度转弧度
double deg_to_rad(double degrees) {
    return degrees * M_PI / 180.0;
}

// 弧度转角度
double rad_to_deg(double radians) {
    return radians * 180.0 / M_PI;
}

// 使用
double angle_deg = 45.0;
double angle_rad = deg_to_rad(angle_deg);
printf("sin(45°) = %.4f\n", sin(angle_rad));  // 0.7071
```

#### 2. asin/acos/atan - 反三角函数

```c
double asin(double x);   // 返回范围: [-π/2, π/2]
double acos(double x);   // 返回范围: [0, π]
double atan(double x);   // 返回范围: (-π/2, π/2)
double atan2(double y, double x);  // 返回范围: [-π, π] (推荐使用)
```

**功能**：计算反三角函数值（返回弧度）。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    // asin - 反正弦
    printf("asin(0.5) = %.4f 弧度\n", asin(0.5));           // π/6
    printf("asin(0.5) = %.1f 度\n", rad_to_deg(asin(0.5))); // 30.0

    // acos - 反余弦
    printf("acos(0.5) = %.4f 弧度\n", acos(0.5));           // π/3
    printf("acos(0.5) = %.1f 度\n", rad_to_deg(acos(0.5))); // 60.0

    // atan - 反正切
    printf("atan(1) = %.4f 弧度\n", atan(1));               // π/4
    printf("atan(1) = %.1f 度\n", rad_to_deg(atan(1)));     // 45.0

    // atan2 - 两参数反正切（更强大）
    // 可以处理所有象限，避免除零错误
    double x = 1.0, y = 1.0;
    double angle = atan2(y, x);
    printf("atan2(1, 1) = %.4f 弧度 = %.1f 度\n",
           angle, rad_to_deg(angle));  // 45.0度

    // atan2的优势：处理所有象限
    printf("第一象限: atan2(1, 1) = %.1f°\n", rad_to_deg(atan2(1, 1)));     // 45°
    printf("第二象限: atan2(1, -1) = %.1f°\n", rad_to_deg(atan2(1, -1)));   // 135°
    printf("第三象限: atan2(-1, -1) = %.1f°\n", rad_to_deg(atan2(-1, -1))); // -135°
    printf("第四象限: atan2(-1, 1) = %.1f°\n", rad_to_deg(atan2(-1, 1)));   // -45°

    return 0;
}
```

**⚠️ 定义域限制**：

```c
// asin和acos的输入必须在[-1, 1]之间
double x = 2.0;
double result = asin(x);  // 返回NaN (Not a Number)

if (isnan(result)) {
    printf("输入超出范围\n");
}
```

#### 3. sinh/cosh/tanh - 双曲函数

```c
double sinh(double x);  // 双曲正弦
double cosh(double x);  // 双曲余弦
double tanh(double x);  // 双曲正切
```

**定义**：
- sinh(x) = (e^x - e^-x) / 2
- cosh(x) = (e^x + e^-x) / 2
- tanh(x) = sinh(x) / cosh(x)

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    double x = 1.0;

    printf("sinh(1) = %.4f\n", sinh(x));  // 1.1752
    printf("cosh(1) = %.4f\n", cosh(x));  // 1.5431
    printf("tanh(1) = %.4f\n", tanh(x));  // 0.7616

    // 验证恒等式: cosh²(x) - sinh²(x) = 1
    double s = sinh(x);
    double c = cosh(x);
    printf("cosh²(x) - sinh²(x) = %.4f\n", c*c - s*s);  // 1.0000

    return 0;
}
```

---

### 二、指数和对数

#### 1. exp() - 指数函数 ⭐⭐⭐⭐

```c
double exp(double x);   // 计算 e^x
double exp2(double x);  // 计算 2^x (C99)
```

**功能**：计算自然指数。

**示例**：

```c
#include <stdio.h>
#include <math.h>

#ifndef M_E
#define M_E 2.71828182845904523536
#endif

int main() {
    printf("e^0 = %.4f\n", exp(0));      // 1.0000
    printf("e^1 = %.4f\n", exp(1));      // 2.7183 (e)
    printf("e^2 = %.4f\n", exp(2));      // 7.3891
    printf("e^-1 = %.4f\n", exp(-1));    // 0.3679

    // 使用exp计算复利
    double principal = 1000.0;  // 本金
    double rate = 0.05;         // 利率5%
    double time = 10.0;         // 10年
    double amount = principal * exp(rate * time);
    printf("连续复利: %.2f元\n", amount);  // 1648.72元

    return 0;
}
```

#### 2. log() - 自然对数 ⭐⭐⭐⭐

```c
double log(double x);    // 自然对数 ln(x) (底数为e)
double log10(double x);  // 常用对数 log₁₀(x) (底数为10)
double log2(double x);   // 二进制对数 log₂(x) (底数为2) (C99)
```

**功能**：计算对数。

**⚠️ 定义域**：x > 0

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    // 自然对数
    printf("ln(1) = %.4f\n", log(1));      // 0.0000
    printf("ln(e) = %.4f\n", log(M_E));    // 1.0000
    printf("ln(10) = %.4f\n", log(10));    // 2.3026

    // 常用对数
    printf("log₁₀(1) = %.4f\n", log10(1));     // 0.0000
    printf("log₁₀(10) = %.4f\n", log10(10));   // 1.0000
    printf("log₁₀(100) = %.4f\n", log10(100)); // 2.0000

    // 二进制对数
    printf("log₂(2) = %.4f\n", log2(2));    // 1.0000
    printf("log₂(8) = %.4f\n", log2(8));    // 3.0000
    printf("log₂(1024) = %.4f\n", log2(1024));  // 10.0000

    // 换底公式：log_a(x) = ln(x) / ln(a)
    double log_base_5 = log(25) / log(5);
    printf("log₅(25) = %.4f\n", log_base_5);  // 2.0000

    // ⚠️ 错误输入
    double result = log(-1);  // 返回NaN
    if (isnan(result)) {
        printf("log(-1) 未定义\n");
    }

    return 0;
}
```

**实际应用**：

```c
// 计算增长倍数
double initial = 100.0;
double final = 500.0;
double growth = final / initial;
printf("增长了 %.2f 倍\n", growth);  // 5.00倍

// 计算需要多少个周期才能达到目标（每周期增长r）
double target_growth = 10.0;
double rate_per_period = 0.05;  // 每期增长5%
double periods = log(target_growth) / log(1 + rate_per_period);
printf("需要 %.1f 个周期\n", periods);  // 约47.2个周期
```

#### 3. pow() - 幂运算 ⭐⭐⭐⭐⭐

```c
double pow(double base, double exponent);
```

**功能**：计算 base^exponent。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    // 整数幂
    printf("2^10 = %.0f\n", pow(2, 10));         // 1024
    printf("10^3 = %.0f\n", pow(10, 3));         // 1000

    // 小数幂
    printf("2^0.5 = %.4f\n", pow(2, 0.5));       // 1.4142 (√2)
    printf("8^(1/3) = %.4f\n", pow(8, 1.0/3));   // 2.0000 (∛8)

    // 负数幂
    printf("2^-1 = %.4f\n", pow(2, -1));         // 0.5000
    printf("10^-3 = %.6f\n", pow(10, -3));       // 0.000001

    // 特殊情况
    printf("0^0 = %.0f\n", pow(0, 0));           // 1 (按约定)
    printf("任何数^0 = %.0f\n", pow(123.456, 0)); // 1

    // ⚠️ 负数的非整数幂未定义
    double result = pow(-2, 0.5);
    if (isnan(result)) {
        printf("(-2)^0.5 未定义（复数）\n");
    }

    return 0;
}
```

**性能优化**：

```c
// ❌ 低效：对于小整数幂使用pow
double x = 5.0;
double result = pow(x, 3);  // 调用复杂的函数

// ✅ 高效：直接乘法
double result = x * x * x;  // 更快

// 对于平方，使用乘法
double square_pow = pow(x, 2);  // 慢
double square_mul = x * x;      // 快

// 对于立方根，使用cbrt
double cbrt_pow = pow(x, 1.0/3);  // 慢
double cbrt_func = cbrt(x);       // 快且更精确
```

---

### 三、开方运算

#### 1. sqrt() - 平方根 ⭐⭐⭐⭐⭐

```c
double sqrt(double x);
```

**功能**：计算平方根。

**⚠️ 定义域**：x >= 0

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("√4 = %.2f\n", sqrt(4));       // 2.00
    printf("√2 = %.4f\n", sqrt(2));       // 1.4142
    printf("√100 = %.2f\n", sqrt(100));   // 10.00

    // 勾股定理：计算斜边长度
    double a = 3.0, b = 4.0;
    double c = sqrt(a*a + b*b);
    printf("斜边长度: %.2f\n", c);  // 5.00

    // ⚠️ 负数输入
    double result = sqrt(-1);
    if (isnan(result)) {
        printf("√(-1) 未定义（实数域）\n");
    }

    return 0;
}
```

#### 2. cbrt() - 立方根 (C99)

```c
double cbrt(double x);
```

**功能**：计算立方根。

**特点**：可以计算负数的立方根。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("∛8 = %.2f\n", cbrt(8));       // 2.00
    printf("∛27 = %.2f\n", cbrt(27));     // 3.00
    printf("∛-8 = %.2f\n", cbrt(-8));     // -2.00 (可以处理负数)

    // 对比pow
    printf("8^(1/3) using pow = %.4f\n", pow(8, 1.0/3));   // 2.0000
    printf("8^(1/3) using cbrt = %.4f\n", cbrt(8));        // 2.0000 (更精确)

    return 0;
}
```

#### 3. hypot() - 计算斜边 (C99)

```c
double hypot(double x, double y);
```

**功能**：计算 √(x² + y²)，避免溢出。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    double a = 3.0, b = 4.0;

    // 方法1: 直接计算（可能溢出）
    double c1 = sqrt(a*a + b*b);
    printf("直接计算: %.2f\n", c1);  // 5.00

    // 方法2: 使用hypot（更安全）
    double c2 = hypot(a, b);
    printf("hypot: %.2f\n", c2);     // 5.00

    // hypot的优势：防止中间计算溢出
    double large = 1e200;
    // sqrt(large*large + large*large) 会溢出
    // hypot(large, large) 安全
    printf("hypot(1e200, 1e200) = %.2e\n", hypot(large, large));

    return 0;
}
```

---

### 四、取整函数

#### 1. ceil() - 向上取整 ⭐⭐⭐⭐

```c
double ceil(double x);
```

**功能**：返回不小于x的最小整数。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("ceil(2.3) = %.1f\n", ceil(2.3));     // 3.0
    printf("ceil(2.9) = %.1f\n", ceil(2.9));     // 3.0
    printf("ceil(-2.3) = %.1f\n", ceil(-2.3));   // -2.0
    printf("ceil(-2.9) = %.1f\n", ceil(-2.9));   // -2.0

    // 实际应用：计算需要多少页
    int items = 23;
    int items_per_page = 10;
    int pages = (int)ceil((double)items / items_per_page);
    printf("需要 %d 页\n", pages);  // 3页

    return 0;
}
```

#### 2. floor() - 向下取整 ⭐⭐⭐⭐

```c
double floor(double x);
```

**功能**：返回不大于x的最大整数。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("floor(2.3) = %.1f\n", floor(2.3));     // 2.0
    printf("floor(2.9) = %.1f\n", floor(2.9));     // 2.0
    printf("floor(-2.3) = %.1f\n", floor(-2.3));   // -3.0
    printf("floor(-2.9) = %.1f\n", floor(-2.9));   // -3.0

    return 0;
}
```

#### 3. round() - 四舍五入 (C99) ⭐⭐⭐⭐

```c
double round(double x);
long lround(double x);
long long llround(double x);
```

**功能**：四舍五入到最接近的整数。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("round(2.3) = %.1f\n", round(2.3));     // 2.0
    printf("round(2.5) = %.1f\n", round(2.5));     // 3.0 (0.5向上舍入)
    printf("round(2.9) = %.1f\n", round(2.9));     // 3.0
    printf("round(-2.5) = %.1f\n", round(-2.5));   // -3.0

    // 返回long类型
    long rounded = lround(2.7);
    printf("lround(2.7) = %ld\n", rounded);  // 3

    return 0;
}
```

#### 4. trunc() - 截断小数 (C99)

```c
double trunc(double x);
```

**功能**：截断小数部分，向零方向取整。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("trunc(2.3) = %.1f\n", trunc(2.3));     // 2.0
    printf("trunc(2.9) = %.1f\n", trunc(2.9));     // 2.0
    printf("trunc(-2.3) = %.1f\n", trunc(-2.3));   // -2.0
    printf("trunc(-2.9) = %.1f\n", trunc(-2.9));   // -2.0

    return 0;
}
```

**取整函数对比**：

| 函数 | 2.3 | 2.9 | -2.3 | -2.9 | 说明 |
|------|-----|-----|------|------|------|
| ceil | 3 | 3 | -2 | -2 | 向正无穷 |
| floor | 2 | 2 | -3 | -3 | 向负无穷 |
| round | 2 | 3 | -2 | -3 | 四舍五入 |
| trunc | 2 | 2 | -2 | -2 | 向零 |

---

### 五、浮点运算

#### 1. fabs() - 绝对值 ⭐⭐⭐⭐⭐

```c
double fabs(double x);
float fabsf(float x);
long double fabsl(long double x);
```

**功能**：计算浮点数的绝对值。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("|2.5| = %.2f\n", fabs(2.5));     // 2.50
    printf("|-3.7| = %.2f\n", fabs(-3.7));   // 3.70
    printf("|0| = %.2f\n", fabs(0));         // 0.00

    // 注意：stdlib.h中的abs()只能处理整数
    // math.h中的fabs()处理浮点数

    return 0;
}
```

#### 2. fmod() - 浮点取模 ⭐⭐⭐⭐

```c
double fmod(double x, double y);
```

**功能**：计算 x 除以 y 的余数。

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    printf("5.3 %% 2 = %.2f\n", fmod(5.3, 2));      // 1.30
    printf("7.5 %% 2.5 = %.2f\n", fmod(7.5, 2.5));  // 0.00
    printf("-5.3 %% 2 = %.2f\n", fmod(-5.3, 2));    // -1.30

    // 实际应用：限制角度在[0, 360)范围
    double angle = 450.0;
    double normalized = fmod(angle, 360.0);
    if (normalized < 0) normalized += 360.0;
    printf("450° 归一化为 %.1f°\n", normalized);  // 90.0°

    return 0;
}
```

#### 3. modf() - 分离整数和小数部分

```c
double modf(double x, double *iptr);
```

**功能**：将x分离为整数和小数部分。

**参数**：
- `x`：输入值
- `iptr`：存储整数部分的指针

**返回值**：小数部分

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    double intpart;
    double x = 3.14159;

    double fracpart = modf(x, &intpart);

    printf("%.5f 的整数部分: %.0f\n", x, intpart);  // 3
    printf("%.5f 的小数部分: %.5f\n", x, fracpart); // 0.14159

    // 负数
    x = -2.718;
    fracpart = modf(x, &intpart);
    printf("%.3f = %.0f + %.3f\n", x, intpart, fracpart);  // -2.718 = -2 + -0.718

    return 0;
}
```

---

### 六、特殊值检测 (C99)

#### isnan() / isinf() / isfinite()

```c
int isnan(double x);      // 检查是否为NaN
int isinf(double x);      // 检查是否为无穷大
int isfinite(double x);   // 检查是否为有限值
int isnormal(double x);   // 检查是否为正常值（非零、非无穷、非NaN）
```

**示例**：

```c
#include <stdio.h>
#include <math.h>

int main() {
    double nan_val = 0.0 / 0.0;        // NaN
    double inf_val = 1.0 / 0.0;        // Infinity
    double normal_val = 3.14;

    printf("0.0/0.0 是NaN? %s\n", isnan(nan_val) ? "是" : "否");      // 是
    printf("1.0/0.0 是无穷? %s\n", isinf(inf_val) ? "是" : "否");     // 是
    printf("3.14 是有限值? %s\n", isfinite(normal_val) ? "是" : "否"); // 是

    // 实际应用：安全的数学计算
    double result = sqrt(-1);
    if (isnan(result)) {
        printf("计算结果无效\n");
    }

    // 检查除法结果
    double a = 10.0, b = 0.0;
    double div_result = a / b;
    if (isinf(div_result)) {
        printf("除零错误\n");
    }

    return 0;
}
```

---

## 📝 实战示例

### 示例1：几何计算

```c
#include <stdio.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// 计算圆的面积和周长
void circle_properties(double radius) {
    double area = M_PI * radius * radius;
    double circumference = 2 * M_PI * radius;

    printf("圆的半径: %.2f\n", radius);
    printf("圆的面积: %.2f\n", area);
    printf("圆的周长: %.2f\n", circumference);
}

// 计算两点之间的距离
double distance_2d(double x1, double y1, double x2, double y2) {
    return hypot(x2 - x1, y2 - y1);
}

// 计算三角形面积（海伦公式）
double triangle_area(double a, double b, double c) {
    double s = (a + b + c) / 2.0;  // 半周长
    return sqrt(s * (s - a) * (s - b) * (s - c));
}

int main() {
    circle_properties(5.0);
    printf("\n");

    printf("点(0,0)到点(3,4)的距离: %.2f\n", distance_2d(0, 0, 3, 4));
    printf("\n");

    printf("边长为3,4,5的三角形面积: %.2f\n", triangle_area(3, 4, 5));

    return 0;
}
```

### 示例2：科学计算

```c
#include <stdio.h>
#include <math.h>

// 计算标准差
double std_deviation(double data[], int n) {
    // 计算平均值
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += data[i];
    }
    double mean = sum / n;

    // 计算方差
    double variance = 0.0;
    for (int i = 0; i < n; i++) {
        variance += pow(data[i] - mean, 2);
    }
    variance /= n;

    // 标准差是方差的平方根
    return sqrt(variance);
}

// 复利计算
double compound_interest(double principal, double rate, int years, int n) {
    // A = P(1 + r/n)^(nt)
    // principal: 本金, rate: 年利率, years: 年数, n: 每年复利次数
    return principal * pow(1 + rate / n, n * years);
}

// 人口增长模型（指数增长）
double population_growth(double P0, double r, double t) {
    // P(t) = P0 * e^(rt)
    // P0: 初始人口, r: 增长率, t: 时间
    return P0 * exp(r * t);
}

int main() {
    // 标准差计算
    double data[] = {2, 4, 4, 4, 5, 5, 7, 9};
    int n = sizeof(data) / sizeof(data[0]);
    printf("数据的标准差: %.4f\n\n", std_deviation(data, n));

    // 复利计算
    double amount = compound_interest(1000, 0.05, 10, 12);
    printf("1000元，年利率5%%，每月复利，10年后: %.2f元\n\n", amount);

    // 人口增长
    double future_pop = population_growth(1000000, 0.02, 20);
    printf("初始人口100万，年增长率2%%，20年后: %.0f\n", future_pop);

    return 0;
}
```

### 示例3：物理模拟

```c
#include <stdio.h>
#include <math.h>

#define G 9.81  // 重力加速度 m/s²

// 抛体运动
typedef struct {
    double max_height;    // 最大高度
    double time_to_peak;  // 到达最高点时间
    double total_time;    // 总飞行时间
    double range;         // 射程
} ProjectileMotion;

ProjectileMotion calculate_projectile(double v0, double angle_deg) {
    double angle_rad = angle_deg * M_PI / 180.0;
    double v0x = v0 * cos(angle_rad);
    double v0y = v0 * sin(angle_rad);

    ProjectileMotion result;
    result.max_height = (v0y * v0y) / (2 * G);
    result.time_to_peak = v0y / G;
    result.total_time = 2 * result.time_to_peak;
    result.range = v0x * result.total_time;

    return result;
}

// 简谐运动
double simple_harmonic_motion(double A, double omega, double t, double phi) {
    // x(t) = A * cos(ωt + φ)
    // A: 振幅, omega: 角频率, t: 时间, phi: 初相位
    return A * cos(omega * t + phi);
}

int main() {
    // 抛体运动：初速度20m/s，发射角度45°
    ProjectileMotion proj = calculate_projectile(20.0, 45.0);
    printf("抛体运动（v0=20m/s, θ=45°）:\n");
    printf("  最大高度: %.2f m\n", proj.max_height);
    printf("  到达最高点时间: %.2f s\n", proj.time_to_peak);
    printf("  总飞行时间: %.2f s\n", proj.total_time);
    printf("  射程: %.2f m\n\n", proj.range);

    // 简谐运动：振幅2m，角频率π rad/s
    printf("简谐运动（A=2m, ω=π rad/s）:\n");
    for (double t = 0; t <= 2.0; t += 0.5) {
        double x = simple_harmonic_motion(2.0, M_PI, t, 0);
        printf("  t=%.1fs: x=%.3fm\n", t, x);
    }

    return 0;
}
```

---

## ⚠️ 常见陷阱

### 1. 角度与弧度混淆

```c
// ❌ 错误：直接使用角度
double result = sin(30);  // 计算的是sin(30弧度)，不是sin(30°)

// ✅ 正确：转换为弧度
double result = sin(30 * M_PI / 180);
```

### 2. 整数除法问题

```c
// ❌ 错误：整数除法
double x = pow(8, 1/3);  // 1/3 = 0 (整数除法)，结果是8^0 = 1

// ✅ 正确：浮点除法
double x = pow(8, 1.0/3);  // 或使用 cbrt(8)
```

### 3. 比较浮点数

```c
// ❌ 不精确：直接比较
if (sqrt(2) * sqrt(2) == 2.0) {  // 可能失败！
    printf("相等\n");
}

// ✅ 使用epsilon比较
#define EPSILON 1e-9
if (fabs(sqrt(2) * sqrt(2) - 2.0) < EPSILON) {
    printf("近似相等\n");
}
```

### 4. 忘记链接数学库

```bash
# ❌ 编译错误：undefined reference to `sin'
gcc program.c

# ✅ 正确：链接数学库
gcc program.c -lm
```

### 5. 域错误未检查

```c
// ❌ 未检查输入范围
double x = sqrt(-1);  // 返回NaN
printf("%.2f\n", x);  // 输出nan

// ✅ 检查输入
double input = -1.0;
if (input < 0) {
    fprintf(stderr, "输入必须非负\n");
} else {
    double result = sqrt(input);
    printf("%.2f\n", result);
}
```

---

## 🔗 相关链接

- [[C 标准库 - stdlib.h]] - 数值转换、随机数
- [[C - 数据类型与变量]] - 浮点类型
- [[MOC - C]] - C语言知识地图

---

## 相关资源

- [[MOC - C]] - C语言知识体系
- [[C 标准库 - stdlib.h]] - 数值转换和随机数
- [[C 标准库 - stdio.h]] - 数学结果的格式化输出

---

## 📚 参考资料

- C Math Library Reference
- IEEE 754 Floating Point Standard
- https://en.cppreference.com/w/c/numeric/math

---

## ✅ 学习检查清单

- [ ] 掌握三角函数及角度弧度转换
- [ ] 理解exp和log的关系
- [ ] 掌握pow函数的使用和注意事项
- [ ] 了解各种取整函数的区别
- [ ] 会使用hypot计算距离
- [ ] 理解浮点数特殊值（NaN, Infinity）
- [ ] 能够进行基本的科学计算
- [ ] 记得编译时链接数学库 -lm

---

*最后更新: 2025-11-18*
