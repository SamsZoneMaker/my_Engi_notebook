---
created: 2025-11-18
tags:
  - type/knowledge
  - topic/programming/c
---
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

### 常见陷阱和错误

#### 陷阱1: if语句后的分号
```c
int x = 10;

if (x > 5);  // 错误!空语句
{
    printf("x大于5\n");  // 总是执行!
}

// 正确写法
if (x > 5) {
    printf("x大于5\n");
}
```

#### 陷阱2: 赋值与比较混淆
```c
int x = 10;

if (x = 5) {  // 错误!这是赋值,不是比较
    printf("这总是执行\n");
}

// 正确写法
if (x == 5) {
    printf("x等于5\n");
}

// 防御性编程(Yoda条件)
if (5 == x) {  // 如果误写成5=x,编译器会报错
    printf("x等于5\n");
}
```

#### 陷阱3: 浮点数在循环条件中
```c
// 危险!可能无限循环
for (float f = 0.0f; f != 1.0f; f += 0.1f) {
    printf("%.10f\n", f);
}

// 正确做法:使用整数或<比较
for (float f = 0.0f; f < 1.0f; f += 0.1f) {
    printf("%.2f\n", f);
}
```

#### 陷阱4: switch缺少break
```c
int day = 2;

switch (day) {
    case 1:
        printf("Monday\n");
        // 缺少break,会继续执行
    case 2:
        printf("Tuesday\n");
        // 缺少break
    case 3:
        printf("Wednesday\n");
        break;
}
// 输出: Tuesday  Wednesday (两个都输出!)
```

#### 陷阱5: 逻辑运算符优先级
```c
int a = 5, b = 10, c = 15;

// 错误!优先级问题
if (a < b && b < c && c < 20)  // OK
if (a < b < c)  // 错误!(a < b)结果是0或1,然后与c比较

// 位运算与逻辑运算混淆
int x = 1, y = 2;
if (x & y) {  // 位AND
    printf("都是奇数\n");
}
if (x && y) {  // 逻辑AND
    printf("都非零\n");
}
```

#### 陷阱6: 循环变量的类型
```c
// 使用unsigned时要小心
for (unsigned int i = 10; i >= 0; i--) {  // 无限循环!
    printf("%u\n", i);
}
// 当i为0时,i--变成UINT_MAX

// 正确做法
for (int i = 10; i >= 0; i--) {
    printf("%d\n", i);
}
```

### 最佳实践

#### 1. 花括号的使用
```c
// 不推荐:单行不加花括号
if (condition)
    do_something();

// 推荐:总是加花括号
if (condition) {
    do_something();
}

// 原因:易于维护,避免错误
if (condition)
    do_something();
    do_another();  // 总是执行!
```

#### 2. 避免魔法数字
```c
// 不推荐
if (status == 1) {
    // ...
}

// 推荐:使用有意义的常量
#define STATUS_SUCCESS 1
#define STATUS_FAILURE 0

if (status == STATUS_SUCCESS) {
    // ...
}

// 或使用enum
enum Status {
    SUCCESS = 0,
    FAILURE = 1,
    PENDING = 2
};
```

#### 3. 提前返回,减少嵌套
```c
// 不推荐:深层嵌套
int process(int *data, int size) {
    if (data != NULL) {
        if (size > 0) {
            if (size <= MAX_SIZE) {
                // 实际处理
                return 1;
            } else {
                return -1;
            }
        } else {
            return -1;
        }
    } else {
        return -1;
    }
}

// 推荐:提前返回
int process_better(int *data, int size) {
    if (data == NULL) {
        return -1;
    }
    if (size <= 0 || size > MAX_SIZE) {
        return -1;
    }

    // 实际处理
    return 1;
}
```

#### 4. 循环不变式提取
```c
// 不推荐:重复计算
for (int i = 0; i < 1000; i++) {
    int limit = expensive_calculation();  // 每次都计算
    if (i < limit) {
        process(i);
    }
}

// 推荐:提取循环不变式
int limit = expensive_calculation();  // 只计算一次
for (int i = 0; i < 1000; i++) {
    if (i < limit) {
        process(i);
    }
}
```

#### 5. 条件表达式的可读性
```c
// 不推荐:复杂条件
if (!(!(a > b) || !(c < d))) {
    // ...
}

// 推荐:简化条件
if (a > b && c < d) {
    // ...
}

// 或提取为函数
int is_valid_range(int a, int b, int c, int d) {
    return a > b && c < d;
}

if (is_valid_range(a, b, c, d)) {
    // ...
}
```

### 实战项目示例

#### 项目1: 菜单驱动的学生成绩管理系统
```c
#include <stdio.h>
#include <stdlib.h>

#define MAX_STUDENTS 50

typedef struct {
    int id;
    char name[50];
    float score;
} Student;

Student students[MAX_STUDENTS];
int student_count = 0;

void add_student() {
    if (student_count >= MAX_STUDENTS) {
        printf("错误: 学生数已达上限\n");
        return;
    }

    Student *s = &students[student_count];
    printf("输入学号: ");
    scanf("%d", &s->id);
    printf("输入姓名: ");
    scanf("%s", s->name);
    printf("输入成绩: ");
    scanf("%f", &s->score);

    student_count++;
    printf("添加成功!\n");
}

void display_all() {
    if (student_count == 0) {
        printf("没有学生记录\n");
        return;
    }

    printf("\n%-10s %-20s %-10s %-10s\n", "学号", "姓名", "成绩", "等级");
    printf("----------------------------------------------------------\n");

    for (int i = 0; i < student_count; i++) {
        Student *s = &students[i];
        char grade;

        if (s->score >= 90) {
            grade = 'A';
        } else if (s->score >= 80) {
            grade = 'B';
        } else if (s->score >= 70) {
            grade = 'C';
        } else if (s->score >= 60) {
            grade = 'D';
        } else {
            grade = 'F';
        }

        printf("%-10d %-20s %-10.2f %-10c\n", s->id, s->name, s->score, grade);
    }
}

void calculate_statistics() {
    if (student_count == 0) {
        printf("没有学生记录\n");
        return;
    }

    float sum = 0;
    float max = students[0].score;
    float min = students[0].score;
    int pass_count = 0;

    for (int i = 0; i < student_count; i++) {
        sum += students[i].score;

        if (students[i].score > max) {
            max = students[i].score;
        }
        if (students[i].score < min) {
            min = students[i].score;
        }
        if (students[i].score >= 60) {
            pass_count++;
        }
    }

    printf("\n=== 统计信息 ===\n");
    printf("总人数: %d\n", student_count);
    printf("平均分: %.2f\n", sum / student_count);
    printf("最高分: %.2f\n", max);
    printf("最低分: %.2f\n", min);
    printf("及格人数: %d\n", pass_count);
    printf("及格率: %.2f%%\n", (float)pass_count / student_count * 100);
}

void search_student() {
    int id;
    printf("输入要查找的学号: ");
    scanf("%d", &id);

    for (int i = 0; i < student_count; i++) {
        if (students[i].id == id) {
            printf("\n找到学生:\n");
            printf("学号: %d\n", students[i].id);
            printf("姓名: %s\n", students[i].name);
            printf("成绩: %.2f\n", students[i].score);
            return;
        }
    }

    printf("未找到学号为%d的学生\n", id);
}

int main() {
    int choice;

    while (1) {
        printf("\n=== 学生成绩管理系统 ===\n");
        printf("1. 添加学生\n");
        printf("2. 显示所有学生\n");
        printf("3. 查找学生\n");
        printf("4. 统计信息\n");
        printf("0. 退出\n");
        printf("请选择: ");

        if (scanf("%d", &choice) != 1) {
            printf("输入错误!\n");
            while (getchar() != '\n');  // 清空缓冲区
            continue;
        }

        switch (choice) {
            case 1:
                add_student();
                break;
            case 2:
                display_all();
                break;
            case 3:
                search_student();
                break;
            case 4:
                calculate_statistics();
                break;
            case 0:
                printf("感谢使用,再见!\n");
                return 0;
            default:
                printf("无效选择,请重试\n");
        }
    }

    return 0;
}
```

#### 项目2: 数字猜谜游戏
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void play_game() {
    int secret = rand() % 100 + 1;  // 1-100
    int guess;
    int attempts = 0;
    int max_attempts = 7;

    printf("\n我想了一个1-100之间的数字,你有%d次机会猜!\n", max_attempts);

    while (attempts < max_attempts) {
        printf("\n第%d次猜测: ", attempts + 1);

        if (scanf("%d", &guess) != 1) {
            printf("请输入有效的数字!\n");
            while (getchar() != '\n');
            continue;
        }

        if (guess < 1 || guess > 100) {
            printf("数字必须在1-100之间!\n");
            continue;
        }

        attempts++;

        if (guess == secret) {
            printf("恭喜!你猜对了!用了%d次\n", attempts);
            return;
        } else if (guess < secret) {
            printf("太小了!还有%d次机会\n", max_attempts - attempts);
        } else {
            printf("太大了!还有%d次机会\n", max_attempts - attempts);
        }

        // 给提示
        if (attempts == max_attempts / 2) {
            if (secret % 2 == 0) {
                printf("提示: 这是一个偶数\n");
            } else {
                printf("提示: 这是一个奇数\n");
            }
        }
    }

    printf("\n游戏结束!正确答案是: %d\n", secret);
}

int main() {
    char play_again;

    srand(time(NULL));  // 初始化随机数种子

    printf("=== 猜数字游戏 ===\n");

    do {
        play_game();

        printf("\n要再玩一次吗? (y/n): ");
        scanf(" %c", &play_again);
    } while (play_again == 'y' || play_again == 'Y');

    printf("感谢游玩,再见!\n");
    return 0;
}
```

#### 项目3: 简单的ATM模拟器
```c
#include <stdio.h>

#define PIN 1234
#define MAX_ATTEMPTS 3

double balance = 1000.0;

int verify_pin() {
    int pin;
    int attempts = 0;

    while (attempts < MAX_ATTEMPTS) {
        printf("请输入PIN码: ");
        scanf("%d", &pin);

        if (pin == PIN) {
            return 1;  // 验证成功
        }

        attempts++;
        printf("PIN码错误!还有%d次机会\n", MAX_ATTEMPTS - attempts);
    }

    return 0;  // 验证失败
}

void check_balance() {
    printf("\n当前余额: $%.2f\n", balance);
}

void deposit() {
    double amount;

    printf("\n输入存款金额: $");
    scanf("%lf", &amount);

    if (amount <= 0) {
        printf("金额必须大于0\n");
        return;
    }

    balance += amount;
    printf("存款成功!新余额: $%.2f\n", balance);
}

void withdraw() {
    double amount;

    printf("\n输入取款金额: $");
    scanf("%lf", &amount);

    if (amount <= 0) {
        printf("金额必须大于0\n");
        return;
    }

    if (amount > balance) {
        printf("余额不足!当前余额: $%.2f\n", balance);
        return;
    }

    balance -= amount;
    printf("取款成功!新余额: $%.2f\n", balance);
}

int main() {
    int choice;

    printf("=== ATM系统 ===\n");

    if (!verify_pin()) {
        printf("验证失败!卡已被锁定\n");
        return 1;
    }

    printf("验证成功!欢迎使用\n");

    while (1) {
        printf("\n=== 主菜单 ===\n");
        printf("1. 查询余额\n");
        printf("2. 存款\n");
        printf("3. 取款\n");
        printf("0. 退出\n");
        printf("请选择: ");

        if (scanf("%d", &choice) != 1) {
            printf("无效输入\n");
            while (getchar() != '\n');
            continue;
        }

        switch (choice) {
            case 1:
                check_balance();
                break;
            case 2:
                deposit();
                break;
            case 3:
                withdraw();
                break;
            case 0:
                printf("感谢使用,再见!\n");
                return 0;
            default:
                printf("无效选择\n");
        }
    }

    return 0;
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

### 基础练习
- [ ] 编写程序判断一个年份是否为闰年
- [ ] 实现一个简单的计算器(使用switch)
- [ ] 打印九九乘法表(使用嵌套for循环)
- [ ] 编写程序找出数组中的最大值和最小值
- [ ] 实现数字金字塔打印程序

### 循环练习
- [ ] 计算1到100的和(for、while、do-while三种方式)
- [ ] 打印斐波那契数列前n项
- [ ] 找出所有100以内的素数
- [ ] 实现数字反转程序
- [ ] 计算最大公约数和最小公倍数

### 控制流综合练习
- [ ] 编写程序检查一个数是否为完美数
- [ ] 实现数字阶乘计算(迭代和递归)
- [ ] 编写程序打印星号图案(菱形、三角形)
- [ ] 实现简单的进制转换(十进制转二进制/八进制/十六进制)

### 实战项目
- [x] 学生成绩管理系统(菜单驱动)
- [x] 数字猜谜游戏(带提示)
- [x] ATM模拟器(PIN验证+余额管理)
- [ ] 简单的文本冒险游戏
- [ ] 日历打印程序(任意年月)
- [ ] Rock-Paper-Scissors游戏
- [ ] 简易通讯录管理系统

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C语言程序设计现代方法 - K. N. King

## 🕸️ Relation
* [[C 语言知识地图]] - C语言知识体系
* [[C语言基础 - 数据类型与变量]] - 控制流中需要使用变量和运算符
* [[C语言基础 - 函数]] - 复杂的控制流逻辑通常封装为函数
* [[C语言基础 - 数组]] - 循环常用于遍历数组
