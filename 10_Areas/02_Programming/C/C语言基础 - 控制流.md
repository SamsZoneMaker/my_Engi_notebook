---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/basic"
  - "#lang/c"
status: 完善中
complexity: 基础
notetype: 学习笔记
resource: C Primer Plus、C程序设计语言
related:
  - "[[00_C_MOC]]"
  - "[[C语言基础 - 函数]]"
  - "[[C语言基础 - 数组]]"
created: 2025-11-18 22:00:00
modified: 2025-11-18 22:00:00
---
# C语言基础 - 控制流

> [!abstract] 摘要
> 本笔记详细介绍C语言的控制流语句,包括条件判断(if-else、switch)、循环结构(for、while、do-while)以及跳转语句(break、continue、goto),帮助你掌握程序逻辑控制的核心技术。

## 🎯 Target
- [ ] 掌握if-else条件判断的使用
- [ ] 理解switch-case多分支选择
- [ ] 熟练使用for、while、do-while三种循环
- [ ] 了解break、continue、goto的作用和使用场景
- [ ] 能够编写包含复杂逻辑的程序

## 📝 Core

### 条件判断 - if语句

#### 基本语法

**1. 简单if语句**
```c
if (条件表达式) {
    // 条件为真时执行的代码
}
```

**示例:**
```c
int age = 20;
if (age >= 18) {
    printf("你已经成年了\n");
}
```

**2. if-else语句**
```c
if (条件表达式) {
    // 条件为真时执行
} else {
    // 条件为假时执行
}
```

**示例:**
```c
int score = 75;
if (score >= 60) {
    printf("及格\n");
} else {
    printf("不及格\n");
}
```

**3. if-else if-else多分支**
```c
if (条件1) {
    // 条件1为真
} else if (条件2) {
    // 条件2为真
} else if (条件3) {
    // 条件3为真
} else {
    // 所有条件都不满足
}
```

**示例:**
```c
int score = 85;
if (score >= 90) {
    printf("优秀\n");
} else if (score >= 80) {
    printf("良好\n");
} else if (score >= 70) {
    printf("中等\n");
} else if (score >= 60) {
    printf("及格\n");
} else {
    printf("不及格\n");
}
```

#### 条件表达式

**关系运算符:**
```c
==  // 等于
!=  // 不等于
>   // 大于
<   // 小于
>=  // 大于等于
<=  // 小于等于
```

**逻辑运算符:**
```c
&&  // 逻辑与 (AND)
||  // 逻辑或 (OR)
!   // 逻辑非 (NOT)
```

**示例:**
```c
int age = 25;
int has_license = 1;

// 逻辑与
if (age >= 18 && has_license) {
    printf("可以开车\n");
}

// 逻辑或
if (age < 18 || age > 70) {
    printf("不建议开车\n");
}

// 逻辑非
if (!has_license) {
    printf("不能开车\n");
}
```

#### 嵌套if语句

```c
int year = 2024;

if (year % 4 == 0) {
    if (year % 100 == 0) {
        if (year % 400 == 0) {
            printf("%d是闰年\n", year);
        } else {
            printf("%d不是闰年\n", year);
        }
    } else {
        printf("%d是闰年\n", year);
    }
} else {
    printf("%d不是闰年\n", year);
}
```

> [!tip] 最佳实践
> - 对于复杂的嵌套if,考虑提取为独立函数
> - 使用花括号`{}`即使只有一条语句,提高可读性
> - 避免过深的嵌套(超过3层考虑重构)

#### 三元运算符

三元运算符是if-else的简化形式:

**语法:**
```c
条件 ? 表达式1 : 表达式2
```

**示例:**
```c
int a = 10, b = 20;
int max = (a > b) ? a : b;  // max = 20

// 等价于
int max;
if (a > b) {
    max = a;
} else {
    max = b;
}
```

### 多分支选择 - switch语句

#### 基本语法

```c
switch (表达式) {
    case 常量1:
        语句1;
        break;
    case 常量2:
        语句2;
        break;
    case 常量3:
        语句3;
        break;
    default:
        默认语句;
        break;
}
```

#### 示例

**1. 简单switch**
```c
int day = 3;

switch (day) {
    case 1:
        printf("星期一\n");
        break;
    case 2:
        printf("星期二\n");
        break;
    case 3:
        printf("星期三\n");
        break;
    case 4:
        printf("星期四\n");
        break;
    case 5:
        printf("星期五\n");
        break;
    case 6:
        printf("星期六\n");
        break;
    case 7:
        printf("星期日\n");
        break;
    default:
        printf("无效的日期\n");
        break;
}
```

**2. case穿透(Fall Through)**
```c
char grade = 'B';

switch (grade) {
    case 'A':
    case 'a':
        printf("优秀\n");
        break;
    case 'B':
    case 'b':
        printf("良好\n");
        break;
    case 'C':
    case 'c':
        printf("中等\n");
        break;
    case 'D':
    case 'd':
        printf("及格\n");
        break;
    case 'F':
    case 'f':
        printf("不及格\n");
        break;
    default:
        printf("无效的等级\n");
}
```

**3. 计算器示例**
```c
char op;
double num1, num2, result;

printf("输入运算符 (+, -, *, /): ");
scanf(" %c", &op);
printf("输入两个数: ");
scanf("%lf %lf", &num1, &num2);

switch (op) {
    case '+':
        result = num1 + num2;
        printf("%.2lf + %.2lf = %.2lf\n", num1, num2, result);
        break;
    case '-':
        result = num1 - num2;
        printf("%.2lf - %.2lf = %.2lf\n", num1, num2, result);
        break;
    case '*':
        result = num1 * num2;
        printf("%.2lf * %.2lf = %.2lf\n", num1, num2, result);
        break;
    case '/':
        if (num2 != 0) {
            result = num1 / num2;
            printf("%.2lf / %.2lf = %.2lf\n", num1, num2, result);
        } else {
            printf("错误: 除数不能为0\n");
        }
        break;
    default:
        printf("错误: 无效的运算符\n");
}
```

> [!important] switch语句的限制
> - 表达式必须是整数类型(int、char、enum)
> - case标签必须是常量表达式
> - 不能使用浮点数或字符串
> - 必须使用break防止穿透(除非有意为之)

#### if-else vs switch

| 特性 | if-else | switch |
|------|---------|--------|
| **适用场景** | 范围判断、复杂条件 | 等值判断、多分支 |
| **条件类型** | 任何布尔表达式 | 仅整数/字符类型 |
| **可读性** | 灵活但可能复杂 | 清晰简洁 |
| **性能** | 逐个判断 | 跳转表(可能更快) |
| **扩展性** | 容易添加条件 | 容易添加case |

**选择建议:**
- **使用if-else**: 范围判断 (`if (x > 10 && x < 20)`)
- **使用switch**: 明确的离散值判断 (`switch (choice)`)

### 循环结构

#### for循环

**语法:**
```c
for (初始化; 条件; 更新) {
    循环体
}
```

**执行流程:**
1. 执行初始化(只执行一次)
2. 判断条件
3. 如果为真,执行循环体
4. 执行更新
5. 回到步骤2

**示例:**

**1. 基本for循环**
```c
// 打印1到10
for (int i = 1; i <= 10; i++) {
    printf("%d ", i);
}
// 输出: 1 2 3 4 5 6 7 8 9 10
```

**2. 计算阶乘**
```c
int n = 5;
int factorial = 1;

for (int i = 1; i <= n; i++) {
    factorial *= i;
}
printf("%d! = %d\n", n, factorial);  // 5! = 120
```

**3. 遍历数组**
```c
int arr[] = {10, 20, 30, 40, 50};
int size = sizeof(arr) / sizeof(arr[0]);

for (int i = 0; i < size; i++) {
    printf("arr[%d] = %d\n", i, arr[i]);
}
```

**4. 嵌套for循环 - 打印乘法表**
```c
for (int i = 1; i <= 9; i++) {
    for (int j = 1; j <= i; j++) {
        printf("%d×%d=%2d  ", j, i, i*j);
    }
    printf("\n");
}
```

**5. 灵活的for循环**
```c
// 倒序
for (int i = 10; i >= 1; i--) {
    printf("%d ", i);
}

// 步长为2
for (int i = 0; i <= 10; i += 2) {
    printf("%d ", i);  // 0 2 4 6 8 10
}

// 多个变量
for (int i = 0, j = 10; i < j; i++, j--) {
    printf("i=%d, j=%d\n", i, j);
}
```

#### while循环

**语法:**
```c
while (条件) {
    循环体
}
```

**特点:** 先判断条件,条件为真才执行循环体

**示例:**

**1. 基本while循环**
```c
int i = 1;
while (i <= 5) {
    printf("%d ", i);
    i++;
}
// 输出: 1 2 3 4 5
```

**2. 计算数字和**
```c
int sum = 0;
int num = 1;

while (num <= 100) {
    sum += num;
    num++;
}
printf("1到100的和 = %d\n", sum);  // 5050
```

**3. 输入验证**
```c
int password = 1234;
int input;

printf("请输入密码: ");
scanf("%d", &input);

while (input != password) {
    printf("密码错误,请重新输入: ");
    scanf("%d", &input);
}
printf("密码正确!\n");
```

**4. 读取未知数量的输入**
```c
int num;
int sum = 0;
int count = 0;

printf("输入整数(输入0结束): \n");
scanf("%d", &num);

while (num != 0) {
    sum += num;
    count++;
    scanf("%d", &num);
}

if (count > 0) {
    printf("平均值: %.2f\n", (double)sum / count);
}
```

#### do-while循环

**语法:**
```c
do {
    循环体
} while (条件);
```

**特点:** 先执行循环体,再判断条件(至少执行一次)

**示例:**

**1. 基本do-while**
```c
int i = 1;
do {
    printf("%d ", i);
    i++;
} while (i <= 5);
// 输出: 1 2 3 4 5
```

**2. 菜单系统**
```c
int choice;

do {
    printf("\n=== 菜单 ===\n");
    printf("1. 选项1\n");
    printf("2. 选项2\n");
    printf("3. 选项3\n");
    printf("0. 退出\n");
    printf("请选择: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            printf("你选择了选项1\n");
            break;
        case 2:
            printf("你选择了选项2\n");
            break;
        case 3:
            printf("你选择了选项3\n");
            break;
        case 0:
            printf("退出程序\n");
            break;
        default:
            printf("无效选择\n");
    }
} while (choice != 0);
```

**3. 输入验证(至少执行一次)**
```c
int age;

do {
    printf("请输入你的年龄(1-120): ");
    scanf("%d", &age);

    if (age < 1 || age > 120) {
        printf("年龄无效,请重新输入!\n");
    }
} while (age < 1 || age > 120);

printf("你的年龄是: %d\n", age);
```

#### for vs while vs do-while

| 循环类型 | 使用场景 | 特点 |
|----------|----------|------|
| **for** | 已知循环次数 | 结构紧凑,适合计数循环 |
| **while** | 未知循环次数,先判断后执行 | 灵活,条件驱动 |
| **do-while** | 未知循环次数,至少执行一次 | 保证至少执行一次 |

**选择建议:**
```c
// 已知次数 -> for
for (int i = 0; i < 10; i++) { }

// 条件驱动,可能不执行 -> while
while (condition) { }

// 至少执行一次 -> do-while
do { } while (condition);
```

### 跳转语句

#### break语句

**作用:** 立即退出当前循环或switch语句

**示例:**

**1. 在循环中使用break**
```c
// 找到第一个大于50的数就停止
int arr[] = {10, 25, 60, 75, 90};
int size = sizeof(arr) / sizeof(arr[0]);

for (int i = 0; i < size; i++) {
    if (arr[i] > 50) {
        printf("找到第一个大于50的数: %d\n", arr[i]);
        break;  // 退出循环
    }
}
```

**2. 在嵌套循环中break只退出当前循环**
```c
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) {
            break;  // 只退出内层循环
        }
        printf("i=%d, j=%d\n", i, j);
    }
}
// 输出:
// i=0, j=0
// i=1, j=0
// i=2, j=0
```

**3. 素数判断**
```c
int num = 29;
int is_prime = 1;

for (int i = 2; i <= num / 2; i++) {
    if (num % i == 0) {
        is_prime = 0;
        break;  // 发现能整除就退出
    }
}

if (is_prime && num > 1) {
    printf("%d是素数\n", num);
} else {
    printf("%d不是素数\n", num);
}
```

#### continue语句

**作用:** 跳过本次循环的剩余部分,直接进入下一次循环

**示例:**

**1. 跳过偶数**
```c
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) {
        continue;  // 跳过偶数
    }
    printf("%d ", i);
}
// 输出: 1 3 5 7 9
```

**2. 跳过负数和零**
```c
int arr[] = {5, -3, 0, 8, -1, 12, 0, 7};
int size = sizeof(arr) / sizeof(arr[0]);
int sum = 0;

for (int i = 0; i < size; i++) {
    if (arr[i] <= 0) {
        continue;  // 跳过非正数
    }
    sum += arr[i];
}
printf("正数之和: %d\n", sum);  // 32
```

**3. 过滤特定字符**
```c
char str[] = "Hello, World!";
printf("去除元音字母: ");

for (int i = 0; str[i] != '\0'; i++) {
    char ch = str[i];
    if (ch == 'a' || ch == 'e' || ch == 'i' ||
        ch == 'o' || ch == 'u' ||
        ch == 'A' || ch == 'E' || ch == 'I' ||
        ch == 'O' || ch == 'U') {
        continue;  // 跳过元音
    }
    printf("%c", ch);
}
// 输出: Hll, Wrld!
```

#### goto语句

**语法:**
```c
label:
    语句;

goto label;
```

**作用:** 无条件跳转到指定标签

> [!warning] 使用警告
> - goto会破坏程序结构,降低可读性
> - 容易产生"意大利面条代码"
> - 现代编程中应尽量避免使用
> - 仅在极少数情况下使用(如跳出多层嵌套)

**示例:**

**1. 跳出多层嵌套循环**
```c
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 10; j++) {
        for (int k = 0; k < 10; k++) {
            if (某个条件) {
                goto end;  // 直接跳出所有循环
            }
        }
    }
}
end:
printf("跳出循环\n");
```

**2. 错误处理(C语言中的常见用法)**
```c
int open_files() {
    FILE *file1 = fopen("file1.txt", "r");
    if (file1 == NULL) {
        goto error;
    }

    FILE *file2 = fopen("file2.txt", "r");
    if (file2 == NULL) {
        goto cleanup_file1;
    }

    FILE *file3 = fopen("file3.txt", "r");
    if (file3 == NULL) {
        goto cleanup_file2;
    }

    // 正常处理
    fclose(file3);
cleanup_file2:
    fclose(file2);
cleanup_file1:
    fclose(file1);
    return 0;

error:
    return -1;
}
```

**更好的替代方案:**
```c
// 使用标志变量
int found = 0;
for (int i = 0; i < 10 && !found; i++) {
    for (int j = 0; j < 10 && !found; j++) {
        if (某个条件) {
            found = 1;
        }
    }
}

// 或者提取为函数,使用return
```

### 无限循环

#### 创建无限循环

```c
// 方法1: while
while (1) {
    // 循环体
}

// 方法2: for
for (;;) {
    // 循环体
}

// 方法3: do-while
do {
    // 循环体
} while (1);
```

#### 实际应用

**1. 嵌入式系统主循环**
```c
int main() {
    init_system();

    while (1) {
        read_sensors();
        process_data();
        control_actuators();
        delay_ms(100);
    }

    return 0;  // 永远不会执行
}
```

**2. 服务器循环**
```c
while (1) {
    connection = accept_connection();
    if (connection) {
        handle_request(connection);
    }
}
```

**3. 带退出条件的无限循环**
```c
while (1) {
    printf("输入命令 (q退出): ");
    char cmd;
    scanf(" %c", &cmd);

    if (cmd == 'q') {
        break;  // 退出循环
    }

    process_command(cmd);
}
```

---

## 🤔 Q&A

### Q1: 什么时候用if-else,什么时候用switch?
**A**:
- **if-else**: 适合范围判断 (`if (x > 10 && x < 20)`) 或复杂条件
- **switch**: 适合离散值的等值判断 (`switch (choice)`),代码更清晰
- 如果超过3个分支且是等值判断,优先考虑switch

### Q2: for、while、do-while如何选择?
**A**:
- **for**: 已知循环次数 (`for (int i = 0; i < 10; i++)`)
- **while**: 未知次数,先判断后执行 (`while (condition)`)
- **do-while**: 未知次数,但至少执行一次 (`do { } while (condition)`)

### Q3: break和continue有什么区别?
**A**:
- **break**: 立即退出整个循环
- **continue**: 跳过本次循环剩余代码,进入下一次循环
```c
for (int i = 1; i <= 5; i++) {
    if (i == 3) break;    // 输出: 1 2
    printf("%d ", i);
}

for (int i = 1; i <= 5; i++) {
    if (i == 3) continue; // 输出: 1 2 4 5
    printf("%d ", i);
}
```

### Q4: 可以在switch中使用字符串吗?
**A**: 不可以。switch只支持整数类型(int、char、enum)。如果需要匹配字符串,使用if-else配合strcmp:
```c
if (strcmp(str, "option1") == 0) {
    // ...
} else if (strcmp(str, "option2") == 0) {
    // ...
}
```

### Q5: 如何跳出多层嵌套循环?
**A**: 三种方法:
1. **使用标志变量**
2. **提取为函数,使用return**
3. **使用goto**(不推荐,但有时最简单)

```c
// 方法1: 标志变量
int found = 0;
for (int i = 0; i < 10 && !found; i++) {
    for (int j = 0; j < 10 && !found; j++) {
        if (condition) found = 1;
    }
}

// 方法2: 函数
int search() {
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            if (condition) return 1;
        }
    }
    return 0;
}
```

## 🚀 Tasks
- [ ] 编写程序判断一个年份是否为闰年
- [ ] 实现一个简单的计算器(使用switch)
- [ ] 打印九九乘法表(使用嵌套for循环)
- [ ] 编写程序找出数组中的最大值和最小值
- [ ] 实现一个猜数字游戏(使用while和if-else)

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C语言程序设计现代方法 - K. N. King

## 🕸️ Relation
* [[00_C_MOC]] - C语言知识体系
* [[C语言基础 - 数据类型与变量]] - 控制流中需要使用变量和运算符
* [[C语言基础 - 函数]] - 复杂的控制流逻辑通常封装为函数
* [[C语言基础 - 数组]] - 循环常用于遍历数组
