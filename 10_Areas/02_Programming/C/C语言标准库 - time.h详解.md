---
tags:
  - "#domain/programming"
  - "#type/reference"
  - "#level/intermediate"
  - "#language/c"
  - "#grain/stdlib"
  - "#tech/time"
status: 完成
complexity: 中级
notetype: 技术参考
resource: C标准库文档
related:
  - "[[C语言标准库 - stdlib.h详解]]"
  - "[[C语言标准库 - stdio.h详解]]"
created: 2025-11-18
modified: 2026-01-09  14:47:04
---

# C语言标准库 - time.h详解

## 📋 概述

`time.h` 提供了时间和日期相关的函数，包括：
- **获取当前时间** (time, clock)
- **时间转换** (localtime, gmtime, mktime)
- **时间格式化** (strftime, asctime, ctime)
- **时间计算** (difftime)
- **程序计时** (clock)

---

## 🎯 学习目标

- [ ] 掌握获取当前时间的方法
- [ ] 理解time_t和struct tm的关系
- [ ] 学会格式化时间输出
- [ ] 掌握时间计算和比较
- [ ] 了解如何测量程序执行时间
- [ ] 理解时区和UTC时间

---

## 📚 核心内容

### 重要类型定义

```c
time_t      // 时间类型（通常是秒数，从1970-01-01 00:00:00 UTC开始）
clock_t     // 时钟计数类型，用于测量CPU时间
size_t      // 无符号整数类型
struct tm   // 时间结构体，包含年月日时分秒等字段
```

### struct tm 结构体

```c
struct tm {
    int tm_sec;    // 秒 [0-60] (60用于闰秒)
    int tm_min;    // 分 [0-59]
    int tm_hour;   // 时 [0-23]
    int tm_mday;   // 日 [1-31]
    int tm_mon;    // 月 [0-11] (0表示1月)
    int tm_year;   // 年份减去1900
    int tm_wday;   // 星期几 [0-6] (0表示星期日)
    int tm_yday;   // 一年中的第几天 [0-365]
    int tm_isdst;  // 夏令时标志 (>0: 夏令时, 0: 非夏令时, <0: 未知)
};
```

**⚠️ 重要注意事项**：
- `tm_year`：实际年份 = tm_year + 1900
- `tm_mon`：实际月份 = tm_mon + 1
- `tm_wday`：0 = 星期日，1 = 星期一，...，6 = 星期六

### 重要宏定义

```c
CLOCKS_PER_SEC  // 每秒的时钟计数（用于将clock()的返回值转换为秒）
NULL            // 空指针常量
```

---

## 🔧 函数详解

### 一、获取当前时间

#### 1. time() - 获取当前时间 ⭐⭐⭐⭐⭐

```c
time_t time(time_t *timer);
```

**功能**：获取当前的日历时间（从1970-01-01 00:00:00 UTC到现在的秒数）。

**参数**：
- `timer`：如果不为NULL，时间值也会存储到*timer中

**返回值**：当前时间（time_t类型），失败返回-1

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    // 方法1: 直接获取返回值
    time_t current_time = time(NULL);
    printf("当前时间戳: %ld\n", (long)current_time);

    // 方法2: 通过指针获取
    time_t current_time2;
    time(&current_time2);
    printf("当前时间戳: %ld\n", (long)current_time2);

    // 时间戳表示从1970-01-01 00:00:00 UTC到现在的秒数
    // 例如: 1700000000 表示 2023-11-14 22:13:20 UTC

    return 0;
}
```

**实际应用 - 设置随机数种子**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // 使用当前时间作为随机数种子
    srand(time(NULL));

    // 生成随机数
    for (int i = 0; i < 5; i++) {
        printf("%d ", rand() % 100);
    }
    printf("\n");

    return 0;
}
```

#### 2. clock() - 测量CPU时间 ⭐⭐⭐⭐

```c
clock_t clock(void);
```

**功能**：返回程序从启动到现在所消耗的CPU时钟计数。

**返回值**：时钟计数（clock_t类型），失败返回-1

**用途**：测量程序执行时间（精确度高于time()）

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    clock_t start, end;
    double cpu_time_used;

    start = clock();

    // 执行一些耗时操作
    long sum = 0;
    for (long i = 0; i < 100000000; i++) {
        sum += i;
    }

    end = clock();

    // 计算执行时间（秒）
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("计算结果: %ld\n", sum);
    printf("执行时间: %.6f 秒\n", cpu_time_used);
    printf("CPU时钟计数: %ld\n", (long)(end - start));

    return 0;
}
```

**time() vs clock()**：

| 特性 | time() | clock() |
|------|--------|---------|
| 测量的时间 | 日历时间（墙上时钟） | CPU时间 |
| 精度 | 秒 | 高精度（毫秒或更高） |
| 用途 | 获取当前日期时间 | 测量程序性能 |
| 受系统影响 | 是（可能跳跃） | 否（只计CPU时间） |

```c
// time()测量的是实际经过的时间（包括等待时间）
// clock()只测量程序实际使用CPU的时间

#include <stdio.h>
#include <time.h>
#include <unistd.h>  // for sleep()

int main() {
    time_t time_start = time(NULL);
    clock_t clock_start = clock();

    sleep(2);  // 睡眠2秒

    time_t time_end = time(NULL);
    clock_t clock_end = clock();

    printf("time()测量: %ld 秒\n", (long)(time_end - time_start));  // 约2秒
    printf("clock()测量: %.6f 秒\n",
           (double)(clock_end - clock_start) / CLOCKS_PER_SEC);     // 接近0秒

    return 0;
}
```

---

### 二、时间转换

#### 1. localtime() - 转换为本地时间 ⭐⭐⭐⭐⭐

```c
struct tm *localtime(const time_t *timer);
```

**功能**：将time_t类型的时间转换为本地时间的struct tm结构。

**参数**：
- `timer`：指向time_t类型的指针

**返回值**：指向静态分配的struct tm的指针（每次调用会覆盖）

**⚠️ 注意**：返回的指针指向静态内存，不是线程安全的

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    time_t current_time = time(NULL);
    struct tm *local = localtime(&current_time);

    // 访问各个字段（注意tm_year和tm_mon的偏移）
    printf("年份: %d\n", local->tm_year + 1900);  // 实际年份
    printf("月份: %d\n", local->tm_mon + 1);      // 实际月份 (1-12)
    printf("日期: %d\n", local->tm_mday);
    printf("时: %d\n", local->tm_hour);
    printf("分: %d\n", local->tm_min);
    printf("秒: %d\n", local->tm_sec);

    // 星期几
    const char *weekdays[] = {"日", "一", "二", "三", "四", "五", "六"};
    printf("星期%s\n", weekdays[local->tm_wday]);

    // 一年中的第几天
    printf("今年的第 %d 天\n", local->tm_yday + 1);

    return 0;
}
```

**线程安全版本 - localtime_r() (POSIX)**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    time_t current_time = time(NULL);
    struct tm local;

    // 使用localtime_r将结果存储到指定的结构中
    localtime_r(&current_time, &local);

    printf("%d-%02d-%02d %02d:%02d:%02d\n",
           local.tm_year + 1900,
           local.tm_mon + 1,
           local.tm_mday,
           local.tm_hour,
           local.tm_min,
           local.tm_sec);

    return 0;
}
```

#### 2. gmtime() - 转换为UTC时间

```c
struct tm *gmtime(const time_t *timer);
```

**功能**：将time_t转换为UTC时间（格林威治标准时间）。

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    time_t current_time = time(NULL);

    struct tm *local = localtime(&current_time);
    struct tm *utc = gmtime(&current_time);

    printf("本地时间: %02d:%02d:%02d\n",
           local->tm_hour, local->tm_min, local->tm_sec);

    printf("UTC时间:  %02d:%02d:%02d\n",
           utc->tm_hour, utc->tm_min, utc->tm_sec);

    return 0;
}
```

#### 3. mktime() - struct tm转time_t ⭐⭐⭐⭐

```c
time_t mktime(struct tm *timeptr);
```

**功能**：将struct tm结构转换为time_t（可用于时间计算）。

**参数**：
- `timeptr`：指向struct tm的指针（会被规范化）

**返回值**：time_t值，失败返回-1

**特性**：自动规范化时间（如13月会变成次年1月）

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    struct tm future_time = {0};

    // 设置时间：2025年1月1日 00:00:00
    future_time.tm_year = 2025 - 1900;  // 2025
    future_time.tm_mon = 0;             // 1月
    future_time.tm_mday = 1;            // 1日
    future_time.tm_hour = 0;
    future_time.tm_min = 0;
    future_time.tm_sec = 0;
    future_time.tm_isdst = -1;          // 让系统决定是否夏令时

    // 转换为time_t
    time_t future = mktime(&future_time);

    printf("2025-01-01的时间戳: %ld\n", (long)future);

    // mktime会自动规范化
    struct tm test = {0};
    test.tm_year = 2024 - 1900;
    test.tm_mon = 12;  // 第13个月（不存在）
    test.tm_mday = 1;
    test.tm_isdst = -1;

    mktime(&test);  // 自动规范化
    printf("2024年第13月被规范化为: %d年%d月\n",
           test.tm_year + 1900, test.tm_mon + 1);  // 2025年1月

    return 0;
}
```

---

### 三、时间格式化

#### 1. strftime() - 自定义格式化 ⭐⭐⭐⭐⭐

```c
size_t strftime(char *s, size_t maxsize, const char *format,
                const struct tm *timeptr);
```

**功能**：按照指定格式将时间格式化为字符串。

**参数**：
- `s`：输出缓冲区
- `maxsize`：缓冲区大小
- `format`：格式化字符串
- `timeptr`：时间结构指针

**返回值**：写入的字符数（不含'\0'），失败返回0

**常用格式说明符**：

| 格式 | 含义 | 示例 |
|------|------|------|
| `%Y` | 四位年份 | 2025 |
| `%y` | 两位年份 | 25 |
| `%m` | 月份(01-12) | 01 |
| `%B` | 月份全名 | January |
| `%b` | 月份缩写 | Jan |
| `%d` | 日期(01-31) | 15 |
| `%H` | 小时(00-23) | 14 |
| `%I` | 小时(01-12) | 02 |
| `%M` | 分钟(00-59) | 30 |
| `%S` | 秒(00-60) | 45 |
| `%p` | AM/PM | PM |
| `%A` | 星期全名 | Monday |
| `%a` | 星期缩写 | Mon |
| `%w` | 星期几(0-6) | 1 |
| `%j` | 一年中第几天(001-366) | 045 |
| `%U` | 周数(00-53, 周日开始) | 07 |
| `%W` | 周数(00-53, 周一开始) | 07 |
| `%c` | 完整日期时间 | Mon Jan 15 14:30:45 2025 |
| `%x` | 日期 | 01/15/25 |
| `%X` | 时间 | 14:30:45 |
| `%Z` | 时区名称 | CST |
| `%%` | 百分号 | % |

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    time_t current_time = time(NULL);
    struct tm *local = localtime(&current_time);
    char buffer[100];

    // 标准格式
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", local);
    printf("标准格式: %s\n", buffer);

    // ISO 8601格式
    strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%S", local);
    printf("ISO 8601: %s\n", buffer);

    // 中文格式
    strftime(buffer, sizeof(buffer), "%Y年%m月%d日 %H时%M分%S秒", local);
    printf("中文格式: %s\n", buffer);

    // 带星期
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %A", local);
    printf("带星期: %s\n", buffer);

    // 12小时制
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %I:%M:%S %p", local);
    printf("12小时制: %s\n", buffer);

    // 完整信息
    strftime(buffer, sizeof(buffer),
             "今天是%Y年的第%j天，本周的星期%w，现在是%H:%M:%S", local);
    printf("%s\n", buffer);

    return 0;
}
```

#### 2. asctime() - 转换为ASCII字符串

```c
char *asctime(const struct tm *timeptr);
```

**功能**：将struct tm转换为固定格式的字符串。

**格式**：`"Www Mmm dd hh:mm:ss yyyy\n"`（例如："Mon Jan 15 14:30:45 2025\n"）

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    time_t current_time = time(NULL);
    struct tm *local = localtime(&current_time);

    char *time_str = asctime(local);
    printf("asctime: %s", time_str);  // 已包含换行符

    return 0;
}
```

#### 3. ctime() - time_t直接转ASCII

```c
char *ctime(const time_t *timer);
```

**功能**：将time_t直接转换为ASCII字符串（等同于asctime(localtime(timer))）。

**示例**：

```c
#include <stdio.h>
#include <time.h>

int main() {
    time_t current_time = time(NULL);

    // 方法1: 两步转换
    char *str1 = asctime(localtime(&current_time));

    // 方法2: 直接转换
    char *str2 = ctime(&current_time);

    printf("方法1: %s", str1);
    printf("方法2: %s", str2);

    return 0;
}
```

---

### 四、时间计算

#### difftime() - 计算时间差 ⭐⭐⭐⭐

```c
double difftime(time_t time1, time_t time0);
```

**功能**：计算time1 - time0的秒数差。

**返回值**：时间差（秒），双精度浮点数

**示例**：

```c
#include <stdio.h>
#include <time.h>
#include <unistd.h>

int main() {
    time_t start = time(NULL);

    // 执行一些操作
    printf("执行中...\n");
    sleep(3);

    time_t end = time(NULL);

    // 计算时间差
    double elapsed = difftime(end, start);
    printf("经过了 %.0f 秒\n", elapsed);

    return 0;
}
```

**时间计算示例**：

```c
#include <stdio.h>
#include <time.h>

// 计算两个日期之间相差多少天
int days_between_dates(int y1, int m1, int d1, int y2, int m2, int d2) {
    struct tm date1 = {0}, date2 = {0};

    date1.tm_year = y1 - 1900;
    date1.tm_mon = m1 - 1;
    date1.tm_mday = d1;
    date1.tm_isdst = -1;

    date2.tm_year = y2 - 1900;
    date2.tm_mon = m2 - 1;
    date2.tm_mday = d2;
    date2.tm_isdst = -1;

    time_t t1 = mktime(&date1);
    time_t t2 = mktime(&date2);

    double seconds = difftime(t2, t1);
    return (int)(seconds / (60 * 60 * 24));
}

int main() {
    // 计算2024-01-01到2025-01-01相差多少天
    int days = days_between_dates(2024, 1, 1, 2025, 1, 1);
    printf("相差天数: %d\n", days);  // 366天（2024是闰年）

    // 计算距离某个日期还有多少天
    time_t now = time(NULL);
    struct tm *current = localtime(&now);

    struct tm future = {0};
    future.tm_year = 2025 - 1900;
    future.tm_mon = 11;  // 12月
    future.tm_mday = 31;
    future.tm_isdst = -1;

    time_t future_time = mktime(&future);
    double diff = difftime(future_time, now);
    int days_until = (int)(diff / (60 * 60 * 24));

    printf("距离2025-12-31还有 %d 天\n", days_until);

    return 0;
}
```

---

## 📝 实战示例

### 示例1：日志时间戳

```c
#include <stdio.h>
#include <time.h>
#include <stdarg.h>

void log_message(const char *level, const char *format, ...) {
    time_t now = time(NULL);
    struct tm *local = localtime(&now);
    char timestamp[64];

    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", local);

    printf("[%s] [%s] ", timestamp, level);

    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);

    printf("\n");
}

int main() {
    log_message("INFO", "程序启动");
    log_message("WARNING", "内存使用率: %d%%", 85);
    log_message("ERROR", "文件 %s 不存在", "config.txt");

    return 0;
}
```

### 示例2：性能计时器

```c
#include <stdio.h>
#include <time.h>

typedef struct {
    clock_t start;
    const char *name;
} Timer;

void timer_start(Timer *t, const char *name) {
    t->name = name;
    t->start = clock();
}

void timer_stop(Timer *t) {
    clock_t end = clock();
    double elapsed = (double)(end - t->start) / CLOCKS_PER_SEC;
    printf("[Timer] %s: %.6f 秒\n", t->name, elapsed);
}

// 快速排序
void quick_sort(int arr[], int low, int high) {
    if (low < high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        int pi = i + 1;
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

int main() {
    Timer t;
    int n = 100000;
    int arr[n];

    // 填充随机数组
    for (int i = 0; i < n; i++) {
        arr[i] = rand();
    }

    // 计时排序
    timer_start(&t, "快速排序100000个元素");
    quick_sort(arr, 0, n - 1);
    timer_stop(&t);

    return 0;
}
```

### 示例3：倒计时程序

```c
#include <stdio.h>
#include <time.h>
#include <unistd.h>

void countdown(int seconds) {
    time_t start = time(NULL);
    time_t end = start + seconds;

    while (1) {
        time_t now = time(NULL);
        int remaining = (int)difftime(end, now);

        if (remaining <= 0) {
            printf("\r时间到！            \n");
            break;
        }

        int hours = remaining / 3600;
        int minutes = (remaining % 3600) / 60;
        int secs = remaining % 60;

        printf("\r剩余时间: %02d:%02d:%02d", hours, minutes, secs);
        fflush(stdout);

        sleep(1);
    }
}

int main() {
    printf("10秒倒计时开始:\n");
    countdown(10);
    return 0;
}
```

### 示例4：简单日历

```c
#include <stdio.h>
#include <time.h>

void print_calendar(int year, int month) {
    struct tm first_day = {0};
    first_day.tm_year = year - 1900;
    first_day.tm_mon = month - 1;
    first_day.tm_mday = 1;
    first_day.tm_isdst = -1;

    mktime(&first_day);  // 规范化，填充tm_wday

    // 获取该月天数
    struct tm last_day = first_day;
    last_day.tm_mon++;
    last_day.tm_mday = 0;
    mktime(&last_day);
    int days_in_month = last_day.tm_mday;

    printf("\n      %d年%d月\n", year, month);
    printf("日 一 二 三 四 五 六\n");

    // 打印前导空格
    for (int i = 0; i < first_day.tm_wday; i++) {
        printf("   ");
    }

    // 打印日期
    for (int day = 1; day <= days_in_month; day++) {
        printf("%2d ", day);

        if ((first_day.tm_wday + day) % 7 == 0) {
            printf("\n");
        }
    }

    printf("\n\n");
}

int main() {
    time_t now = time(NULL);
    struct tm *current = localtime(&now);

    print_calendar(current->tm_year + 1900, current->tm_mon + 1);

    return 0;
}
```

### 示例5：年龄计算器

```c
#include <stdio.h>
#include <time.h>

typedef struct {
    int years;
    int months;
    int days;
} Age;

Age calculate_age(int birth_year, int birth_month, int birth_day) {
    time_t now = time(NULL);
    struct tm *current = localtime(&now);

    Age age;
    age.years = current->tm_year + 1900 - birth_year;
    age.months = current->tm_mon + 1 - birth_month;
    age.days = current->tm_mday - birth_day;

    // 调整负数
    if (age.days < 0) {
        age.months--;
        // 获取上个月的天数
        struct tm last_month = *current;
        last_month.tm_mday = 0;
        mktime(&last_month);
        age.days += last_month.tm_mday;
    }

    if (age.months < 0) {
        age.years--;
        age.months += 12;
    }

    return age;
}

int main() {
    // 示例：1990年5月15日出生
    Age age = calculate_age(1990, 5, 15);

    printf("年龄: %d岁%d个月%d天\n", age.years, age.months, age.days);

    // 计算总天数
    struct tm birth = {0}, now_tm;
    birth.tm_year = 1990 - 1900;
    birth.tm_mon = 5 - 1;
    birth.tm_mday = 15;
    birth.tm_isdst = -1;

    time_t birth_time = mktime(&birth);
    time_t now = time(NULL);

    double total_days = difftime(now, birth_time) / (60 * 60 * 24);
    printf("总共活了: %.0f 天\n", total_days);

    return 0;
}
```

---

## ⚠️ 常见陷阱

### 1. tm_year和tm_mon的偏移

```c
// ❌ 错误
struct tm t;
t.tm_year = 2025;  // 错误！应该是2025 - 1900
t.tm_mon = 1;      // 错误！这是2月，不是1月

// ✅ 正确
t.tm_year = 2025 - 1900;  // 125
t.tm_mon = 0;             // 1月
```

### 2. localtime返回静态指针

```c
// ❌ 危险：第二次调用会覆盖第一次的结果
time_t t1 = time(NULL);
time_t t2 = time(NULL) + 3600;

struct tm *tm1 = localtime(&t1);
struct tm *tm2 = localtime(&t2);  // tm1现在指向的内容被覆盖了！

// ✅ 正确：复制结构体
struct tm tm1_copy = *localtime(&t1);
struct tm tm2_copy = *localtime(&t2);

// 或使用线程安全版本
struct tm tm1_safe, tm2_safe;
localtime_r(&t1, &tm1_safe);
localtime_r(&t2, &tm2_safe);
```

### 3. strftime缓冲区大小

```c
// ❌ 缓冲区太小
char buffer[10];
strftime(buffer, sizeof(buffer),
         "%Y-%m-%d %H:%M:%S", localtime(&t));  // 可能溢出

// ✅ 合适的缓冲区
char buffer[64];
size_t written = strftime(buffer, sizeof(buffer),
                          "%Y-%m-%d %H:%M:%S", localtime(&t));
if (written == 0) {
    fprintf(stderr, "strftime失败：缓冲区太小\n");
}
```

### 4. 忘记设置tm_isdst

```c
// ❌ 未设置tm_isdst
struct tm t = {0};
t.tm_year = 2025 - 1900;
t.tm_mon = 0;
t.tm_mday = 1;
// t.tm_isdst未设置，可能导致mktime结果不正确

// ✅ 正确设置
t.tm_isdst = -1;  // 让系统自动决定
mktime(&t);
```

---

## 🔗 相关链接

- [[C语言标准库 - stdio.h详解]] - 文件操作
- [[C语言标准库 - stdlib.h详解]] - 实用工具
- [[C语言进阶 - 结构体]] - struct tm结构
- [[00_C_MOC]] - C语言知识地图

---

## 相关资源

- [[00_C_MOC]] - C语言知识体系
- [[C语言标准库 - stdio.h详解]] - 时间格式化输出
- [[C语言标准库 - stdlib.h详解]] - srand()随机数种子
- [[Linux系统编程 - 进程管理]] - 进程时间统计

---

## 📚 参考资料

- C Standard Library Reference
- POSIX Time Functions
- https://en.cppreference.com/w/c/chrono

---

## ✅ 学习检查清单

- [ ] 掌握time()和clock()的区别
- [ ] 理解struct tm结构及字段含义
- [ ] 会使用strftime格式化时间
- [ ] 掌握时间转换函数（localtime, gmtime, mktime）
- [ ] 能够计算时间差和日期间隔
- [ ] 了解时区和UTC的概念
- [ ] 会测量程序执行时间
- [ ] 注意线程安全问题

---

*最后更新: 2025-11-18*
