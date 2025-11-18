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
# C语言进阶 - 结构体

> [!abstract] 摘要
> 本笔记深入介绍C语言结构体的定义、使用、内存布局、嵌套、位域、联合体以及链表等数据结构的实现,帮助你掌握复杂数据类型的设计。

## 🎯 Target
- [ ] 理解结构体的定义和使用
- [ ] 掌握结构体的内存布局和对齐规则
- [ ] 了解结构体指针和动态分配
- [ ] 掌握typedef和结构体的结合使用
- [ ] 理解联合体(union)和位域(bit field)
- [ ] 能够使用结构体实现链表等数据结构

## 📝 Core

### 结构体的基本概念

#### 什么是结构体?

**结构体(struct)** 是一种用户自定义的数据类型,可以将不同类型的数据组合在一起。

**为什么需要结构体?**
```c
// 不使用结构体
char name[50];
int age;
float score;

// 使用结构体 - 更有组织
struct Student {
    char name[50];
    int age;
    float score;
};
```

**结构体的特点:**
- ✅ 组合不同类型的数据
- ✅ 是值类型(复制时复制整个结构体)
- ✅ 可以作为函数参数和返回值
- ✅ 是实现抽象数据类型的基础

#### 结构体的定义

**基本语法:**
```c
struct 结构体名 {
    数据类型 成员1;
    数据类型 成员2;
    ...
};
```

**示例:**

**1. 简单结构体**
```c
struct Point {
    int x;
    int y;
};
```

**2. 复杂结构体**
```c
struct Student {
    char name[50];
    int id;
    int age;
    float score;
    char grade;
};
```

**3. 定义时声明变量**
```c
struct Point {
    int x;
    int y;
} p1, p2;  // 同时声明变量
```

**4. 匿名结构体**
```c
struct {
    int x;
    int y;
} point1, point2;  // 只能在这里声明变量
```

#### 结构体变量的声明和初始化

**声明:**
```c
struct Point p1;  // 声明一个Point类型的变量
```

**初始化:**

**方式1: 按顺序初始化**
```c
struct Point p1 = {10, 20};
```

**方式2: 指定成员初始化(C99)**
```c
struct Point p2 = {.x = 10, .y = 20};
struct Point p3 = {.y = 20, .x = 10};  // 顺序可以不同
```

**方式3: 部分初始化**
```c
struct Student s1 = {"Alice", 1001};  // 后面的成员为0/NULL
struct Student s2 = {.name = "Bob"};  // 其他成员为0/NULL
```

**完整示例:**
```c
struct Student {
    char name[50];
    int id;
    float score;
};

int main() {
    // 声明并初始化
    struct Student s1 = {"Alice", 1001, 95.5};

    // 指定成员
    struct Student s2 = {
        .name = "Bob",
        .id = 1002,
        .score = 88.0
    };

    // 部分初始化
    struct Student s3 = {.id = 1003};

    return 0;
}
```

#### 访问结构体成员

**使用点运算符(.):**
```c
struct Point {
    int x;
    int y;
};

int main() {
    struct Point p1 = {10, 20};

    // 读取成员
    printf("x = %d, y = %d\n", p1.x, p1.y);

    // 修改成员
    p1.x = 30;
    p1.y = 40;

    printf("x = %d, y = %d\n", p1.x, p1.y);

    return 0;
}
```

### typedef简化结构体定义

#### 基本用法

**方式1: 分步定义**
```c
struct Point {
    int x;
    int y;
};

typedef struct Point Point;  // 创建别名

// 使用
Point p1 = {10, 20};  // 无需写struct
```

**方式2: 同时定义(推荐)**
```c
typedef struct {
    int x;
    int y;
} Point;

// 使用
Point p1 = {10, 20};
```

**方式3: 命名结构体+typedef**
```c
typedef struct Point {
    int x;
    int y;
} Point;

// 可以使用struct Point或Point
```

**实际应用:**
```c
typedef struct {
    char name[50];
    int age;
    float score;
} Student;

int main() {
    Student s1 = {"Alice", 20, 95.5};
    Student s2;

    strcpy(s2.name, "Bob");
    s2.age = 21;
    s2.score = 88.0;

    printf("%s, %d岁, 分数%.1f\n", s1.name, s1.age, s1.score);

    return 0;
}
```

### 结构体指针

#### 定义和初始化

```c
typedef struct {
    int x;
    int y;
} Point;

int main() {
    Point p1 = {10, 20};
    Point *ptr = &p1;  // 指向结构体的指针

    return 0;
}
```

#### 访问成员

**方式1: 使用箭头运算符(->)**
```c
ptr->x = 30;  // 推荐
ptr->y = 40;
```

**方式2: 解引用后使用点运算符**
```c
(*ptr).x = 30;  // 等价,但不推荐
(*ptr).y = 40;
```

**示例:**
```c
typedef struct {
    char name[50];
    int age;
} Person;

void print_person(Person *p) {
    printf("姓名: %s, 年龄: %d\n", p->name, p->age);
}

int main() {
    Person alice = {"Alice", 25};
    Person *ptr = &alice;

    printf("使用ptr->: %s\n", ptr->name);
    printf("使用(*ptr).: %s\n", (*ptr).name);

    print_person(&alice);

    return 0;
}
```

### 结构体作为函数参数

#### 传值(Pass by Value)

```c
typedef struct {
    int x;
    int y;
} Point;

void modify_point_value(Point p) {
    p.x = 100;
    p.y = 200;
}

int main() {
    Point p1 = {10, 20};
    modify_point_value(p1);
    printf("x = %d, y = %d\n", p1.x, p1.y);  // 10, 20 (未改变)
    return 0;
}
```

**特点:**
- 复制整个结构体
- 函数内修改不影响原结构体
- 大结构体效率低

#### 传指针(Pass by Pointer) - 推荐

```c
void modify_point_ptr(Point *p) {
    p->x = 100;
    p->y = 200;
}

int main() {
    Point p1 = {10, 20};
    modify_point_ptr(&p1);
    printf("x = %d, y = %d\n", p1.x, p1.y);  // 100, 200 (已改变)
    return 0;
}
```

**特点:**
- 只传递指针(4或8字节)
- 可以修改原结构体
- 效率高

#### const保护

```c
void print_point(const Point *p) {
    printf("x = %d, y = %d\n", p->x, p->y);
    // p->x = 100;  // 错误! 不能修改
}

int main() {
    Point p1 = {10, 20};
    print_point(&p1);
    return 0;
}
```

#### 返回结构体

**方式1: 返回值**
```c
Point create_point(int x, int y) {
    Point p = {x, y};
    return p;  // 返回副本
}

int main() {
    Point p1 = create_point(10, 20);
    printf("x = %d, y = %d\n", p1.x, p1.y);
    return 0;
}
```

**方式2: 返回指针(动态分配)**
```c
Point* create_point_dynamic(int x, int y) {
    Point *p = (Point*)malloc(sizeof(Point));
    if (p != NULL) {
        p->x = x;
        p->y = y;
    }
    return p;
}

int main() {
    Point *p1 = create_point_dynamic(10, 20);
    if (p1 != NULL) {
        printf("x = %d, y = %d\n", p1->x, p1->y);
        free(p1);  // 记得释放!
    }
    return 0;
}
```

> [!warning] 不要返回局部变量的地址
> ```c
> Point* bad_function() {
>     Point p = {10, 20};
>     return &p;  // 危险! 局部变量在函数结束后销毁
> }
> ```

### 结构体的内存布局

#### 内存对齐

**示例:**
```c
typedef struct {
    char a;    // 1字节
    int b;     // 4字节
    char c;    // 1字节
} Example;

printf("sizeof(Example) = %zu\n", sizeof(Example));
// 输出: 12 (不是6!)
```

**内存布局:**
```
地址    成员    说明
0x00:   a      1字节
0x01-03: [padding]  3字节填充(为了b对齐到4的倍数)
0x04-07: b      4字节
0x08:   c      1字节
0x09-0B: [padding]  3字节填充(结构体大小对齐到最大成员4的倍数)
```

**对齐规则:**
1. 每个成员按自身大小对齐
2. 结构体总大小是最大成员大小的倍数
3. 成员顺序影响总大小

**优化示例:**
```c
// 不优化 - 浪费空间
typedef struct {
    char a;    // 1字节
    int b;     // 4字节
    char c;    // 1字节
} Bad;  // sizeof = 12

// 优化 - 减少填充
typedef struct {
    int b;     // 4字节
    char a;    // 1字节
    char c;    // 1字节
    // [2字节填充]
} Good;  // sizeof = 8
```

#### 查看成员偏移量

```c
#include <stddef.h>

typedef struct {
    char a;
    int b;
    char c;
} Example;

int main() {
    printf("offsetof(a) = %zu\n", offsetof(Example, a));  // 0
    printf("offsetof(b) = %zu\n", offsetof(Example, b));  // 4
    printf("offsetof(c) = %zu\n", offsetof(Example, c));  // 8
    return 0;
}
```

### 嵌套结构体

#### 定义嵌套结构体

```c
typedef struct {
    int year;
    int month;
    int day;
} Date;

typedef struct {
    char name[50];
    int id;
    Date birthday;  // 嵌套结构体
} Student;
```

#### 访问嵌套成员

```c
int main() {
    Student s1 = {
        .name = "Alice",
        .id = 1001,
        .birthday = {2000, 5, 15}
    };

    // 访问嵌套成员
    printf("姓名: %s\n", s1.name);
    printf("生日: %d-%d-%d\n",
           s1.birthday.year,
           s1.birthday.month,
           s1.birthday.day);

    // 修改嵌套成员
    s1.birthday.year = 2001;

    return 0;
}
```

#### 结构体数组

```c
typedef struct {
    char name[50];
    int age;
} Person;

int main() {
    Person people[3] = {
        {"Alice", 20},
        {"Bob", 25},
        {"Charlie", 30}
    };

    for (int i = 0; i < 3; i++) {
        printf("%s: %d岁\n", people[i].name, people[i].age);
    }

    return 0;
}
```

### 联合体(Union)

#### 基本概念

**联合体** 允许在同一内存位置存储不同类型的数据,但同一时间只能使用一个成员。

**定义:**
```c
typedef union {
    int i;
    float f;
    char c;
} Data;
```

**内存布局:**
```
所有成员共享同一块内存
大小 = 最大成员的大小
```

**示例:**
```c
int main() {
    Data d;

    d.i = 10;
    printf("d.i = %d\n", d.i);  // 10

    d.f = 3.14;
    printf("d.f = %.2f\n", d.f);  // 3.14
    printf("d.i = %d\n", d.i);    // 未定义(被覆盖)

    printf("sizeof(Data) = %zu\n", sizeof(Data));  // 4 (float的大小)

    return 0;
}
```

#### 实际应用 - 类型标记联合体

```c
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING
} DataType;

typedef struct {
    DataType type;
    union {
        int i;
        float f;
        char *s;
    } value;
} Variant;

void print_variant(Variant *v) {
    switch (v->type) {
        case TYPE_INT:
            printf("int: %d\n", v->value.i);
            break;
        case TYPE_FLOAT:
            printf("float: %.2f\n", v->value.f);
            break;
        case TYPE_STRING:
            printf("string: %s\n", v->value.s);
            break;
    }
}

int main() {
    Variant v1 = {TYPE_INT, {.i = 42}};
    Variant v2 = {TYPE_FLOAT, {.f = 3.14}};
    Variant v3 = {TYPE_STRING, {.s = "Hello"}};

    print_variant(&v1);
    print_variant(&v2);
    print_variant(&v3);

    return 0;
}
```

### 位域(Bit Field)

#### 基本概念

**位域** 允许以位为单位定义结构体成员,节省内存。

**语法:**
```c
struct {
    unsigned int field1 : 位数;
    unsigned int field2 : 位数;
};
```

**示例:**
```c
typedef struct {
    unsigned int flag1 : 1;  // 1位
    unsigned int flag2 : 1;  // 1位
    unsigned int value : 6;  // 6位
} Flags;

int main() {
    Flags f = {1, 0, 32};

    printf("sizeof(Flags) = %zu\n", sizeof(Flags));  // 4 (编译器可能填充)
    printf("flag1 = %u\n", f.flag1);
    printf("flag2 = %u\n", f.flag2);
    printf("value = %u\n", f.value);

    return 0;
}
```

#### 实际应用 - 寄存器配置

```c
typedef struct {
    unsigned int enable : 1;     // bit 0
    unsigned int mode : 2;       // bits 1-2
    unsigned int reserved : 5;   // bits 3-7
    unsigned int speed : 3;      // bits 8-10
    unsigned int : 5;            // 未命名位域(填充)
    unsigned int interrupt : 1;  // bit 16
} RegisterConfig;

int main() {
    RegisterConfig reg = {
        .enable = 1,
        .mode = 2,
        .speed = 5,
        .interrupt = 0
    };

    printf("enable = %u\n", reg.enable);
    printf("mode = %u\n", reg.mode);
    printf("speed = %u\n", reg.speed);

    return 0;
}
```

> [!warning] 位域的限制
> - 不能取地址
> - 移植性差(字节序、对齐等依赖编译器)
> - 只能用于整数类型

### 链表实现

#### 单向链表

**节点定义:**
```c
typedef struct Node {
    int data;
    struct Node *next;  // 指向下一个节点
} Node;
```

**创建节点:**
```c
Node* create_node(int data) {
    Node *new_node = (Node*)malloc(sizeof(Node));
    if (new_node != NULL) {
        new_node->data = data;
        new_node->next = NULL;
    }
    return new_node;
}
```

**插入节点(头部):**
```c
void insert_at_head(Node **head, int data) {
    Node *new_node = create_node(data);
    if (new_node != NULL) {
        new_node->next = *head;
        *head = new_node;
    }
}
```

**插入节点(尾部):**
```c
void insert_at_tail(Node **head, int data) {
    Node *new_node = create_node(data);
    if (new_node == NULL) return;

    if (*head == NULL) {
        *head = new_node;
        return;
    }

    Node *temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = new_node;
}
```

**删除节点:**
```c
void delete_node(Node **head, int data) {
    if (*head == NULL) return;

    // 删除头节点
    if ((*head)->data == data) {
        Node *temp = *head;
        *head = (*head)->next;
        free(temp);
        return;
    }

    // 删除中间或尾节点
    Node *current = *head;
    while (current->next != NULL && current->next->data != data) {
        current = current->next;
    }

    if (current->next != NULL) {
        Node *temp = current->next;
        current->next = temp->next;
        free(temp);
    }
}
```

**遍历链表:**
```c
void print_list(Node *head) {
    Node *temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}
```

**释放链表:**
```c
void free_list(Node **head) {
    Node *current = *head;
    while (current != NULL) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    *head = NULL;
}
```

**完整示例:**
```c
int main() {
    Node *head = NULL;

    insert_at_head(&head, 10);
    insert_at_head(&head, 20);
    insert_at_tail(&head, 5);
    insert_at_tail(&head, 15);

    print_list(head);  // 20 -> 10 -> 5 -> 15 -> NULL

    delete_node(&head, 10);
    print_list(head);  // 20 -> 5 -> 15 -> NULL

    free_list(&head);

    return 0;
}
```

---

## 🤔 Q&A

### Q1: 结构体和数组有什么区别?
**A**:
- **数组**: 相同类型元素的集合,通过索引访问
- **结构体**: 不同类型数据的组合,通过成员名访问

### Q2: 什么时候传值,什么时候传指针?
**A**:
- **传值**: 小结构体(≤16字节)、需要副本、不修改原结构体
- **传指针**: 大结构体、需要修改原结构体、性能优先

### Q3: typedef有什么好处?
**A**:
- 简化类型名(不用写struct)
- 提高代码可读性
- 易于修改类型定义

### Q4: 结构体可以包含自身吗?
**A**: 不能包含自身,但可以包含指向自身的指针:
```c
typedef struct Node {
    int data;
    struct Node *next;  // ✅ 正确
    // struct Node child;  // ❌ 错误! 无限递归
} Node;
```

### Q5: union和struct有什么区别?
**A**:
- **struct**: 每个成员有独立内存,大小=所有成员之和(+填充)
- **union**: 所有成员共享内存,大小=最大成员的大小

## 🚀 Tasks
- [ ] 实现一个通讯录程序(使用结构体数组)
- [ ] 编写程序使用链表实现栈
- [ ] 实现双向链表
- [ ] 编写程序实现二叉树
- [ ] 使用结构体实现一个简单的学生管理系统

## 📚 Reference
* C Primer Plus (第6版) - Stephen Prata
* C程序设计语言 (第2版) - Brian W. Kernighan, Dennis M. Ritchie
* C和指针 - Kenneth A. Reek
* 数据结构(C语言版) - 严蔚敏

## 🕸️ Relation
* [[00_C_MOC]] - C语言知识体系
* [[C语言基础 - 数组]] - 结构体数组
* [[C语言进阶 - 指针详解]] - 结构体指针、链表
* [[C语言进阶 - 字符串]] - 结构体中的字符串成员
