---
created: 2025-11-18
tags:
  - type/reference
  - topic/programming/c
---
## 📋 概述

状态机（State Machine）是一种强大的设计模式，广泛应用于嵌入式系统、协议处理、游戏开发等领域。本文详细介绍如何在C语言中实现状态机。

**适用场景**：
- 协议状态管理（TCP/IP协议栈）
- 设备状态控制（电源管理）
- UI界面切换
- 游戏角色状态
- 工作流引擎

---

## 🎯 学习目标

- [ ] 理解状态机的基本概念
- [ ] 掌握函数指针的使用
- [ ] 学会使用查找表实现状态机
- [ ] 理解状态机的优缺点
- [ ] 能够设计实用的状态机系统

---

## 📚 核心概念

### 状态机基本组成

**状态机**（State Machine）由以下要素组成：

1. **状态（State）**：系统在某一时刻所处的具体情形
2. **事件（Event）**：触发状态转换的条件或输入
3. **转换（Transition）**：从一个状态转换到另一个状态
4. **动作（Action）**：状态转换时执行的操作

**工作原理**：
```
当前状态 + 输入事件 → 执行动作 + 新状态
```

### 状态机示意图

```
     [开始]
        ↓
    [状态A] --事件1--> [状态B]
        ↓               ↓
      事件2           事件3
        ↓               ↓
    [状态C] <--事件4-- [状态D]
```

---

## 🔧 实现方法

### 方法1：使用switch-case

**优点**：简单直观
**缺点**：代码冗长，难以维护

```c
#include <stdio.h>

// 定义状态枚举
typedef enum {
    STATE_IDLE,
    STATE_RUNNING,
    STATE_PAUSED,
    STATE_STOPPED
} State;

// 定义事件枚举
typedef enum {
    EVENT_START,
    EVENT_PAUSE,
    EVENT_RESUME,
    EVENT_STOP
} Event;

// 状态机结构
typedef struct {
    State current_state;
} StateMachine;

// 初始化状态机
void sm_init(StateMachine *sm) {
    sm->current_state = STATE_IDLE;
}

// 状态机处理函数
void sm_handle_event(StateMachine *sm, Event event) {
    switch (sm->current_state) {
        case STATE_IDLE:
            switch (event) {
                case EVENT_START:
                    printf("从空闲到运行\n");
                    sm->current_state = STATE_RUNNING;
                    break;
                default:
                    printf("空闲状态：无效事件\n");
                    break;
            }
            break;

        case STATE_RUNNING:
            switch (event) {
                case EVENT_PAUSE:
                    printf("从运行到暂停\n");
                    sm->current_state = STATE_PAUSED;
                    break;
                case EVENT_STOP:
                    printf("从运行到停止\n");
                    sm->current_state = STATE_STOPPED;
                    break;
                default:
                    printf("运行状态：无效事件\n");
                    break;
            }
            break;

        case STATE_PAUSED:
            switch (event) {
                case EVENT_RESUME:
                    printf("从暂停到运行\n");
                    sm->current_state = STATE_RUNNING;
                    break;
                case EVENT_STOP:
                    printf("从暂停到停止\n");
                    sm->current_state = STATE_STOPPED;
                    break;
                default:
                    printf("暂停状态：无效事件\n");
                    break;
            }
            break;

        case STATE_STOPPED:
            switch (event) {
                case EVENT_START:
                    printf("从停止到运行\n");
                    sm->current_state = STATE_RUNNING;
                    break;
                default:
                    printf("停止状态：无效事件\n");
                    break;
            }
            break;
    }
}

int main() {
    StateMachine sm;
    sm_init(&sm);

    sm_handle_event(&sm, EVENT_START);   // IDLE -> RUNNING
    sm_handle_event(&sm, EVENT_PAUSE);   // RUNNING -> PAUSED
    sm_handle_event(&sm, EVENT_RESUME);  // PAUSED -> RUNNING
    sm_handle_event(&sm, EVENT_STOP);    // RUNNING -> STOPPED

    return 0;
}
```

---

### 方法2：状态查找表（推荐）⭐⭐⭐⭐⭐

**优点**：代码简洁，易于扩展
**缺点**：需要理解函数指针

#### 函数指针基础

```c
// 函数指针语法
返回类型 (*指针名)(参数列表);

// 示例
int add(int a, int b) {
    return a + b;
}

int (*func_ptr)(int, int);  // 声明函数指针
func_ptr = add;             // 指向函数
int result = func_ptr(3, 5); // 调用函数，result = 8
```

#### 状态处理函数指针

```c
#include <stdio.h>
#include <stddef.h>

// 前置声明
typedef struct StateMachine StateMachine;
typedef struct Event Event;

// 定义状态处理函数类型
typedef void (*StateHandler)(StateMachine *sm, const Event *event);

// 事件结构
typedef struct Event {
    int id;
    void *data;
} Event;

// 状态机结构
typedef struct StateMachine {
    int current_state;
    void *context;  // 状态机上下文数据
} StateMachine;

// 状态查找表项
typedef struct {
    StateHandler handler;  // 状态处理函数指针
} StateLutEntry;

// 状态枚举
enum {
    STATE_IDLE,
    STATE_RUNNING,
    STATE_PAUSED,
    NUM_STATES
};

// 事件ID枚举
enum {
    EVENT_START,
    EVENT_PAUSE,
    EVENT_RESUME,
    EVENT_STOP
};

// ========== 状态处理函数 ==========

// 空闲状态处理
void idle_state_handler(StateMachine *sm, const Event *event) {
    switch (event->id) {
        case EVENT_START:
            printf("[IDLE] 收到START事件 -> 切换到RUNNING\n");
            sm->current_state = STATE_RUNNING;
            break;
        default:
            printf("[IDLE] 未知事件: %d\n", event->id);
            break;
    }
}

// 运行状态处理
void running_state_handler(StateMachine *sm, const Event *event) {
    switch (event->id) {
        case EVENT_PAUSE:
            printf("[RUNNING] 收到PAUSE事件 -> 切换到PAUSED\n");
            sm->current_state = STATE_PAUSED;
            break;
        case EVENT_STOP:
            printf("[RUNNING] 收到STOP事件 -> 切换到IDLE\n");
            sm->current_state = STATE_IDLE;
            break;
        default:
            printf("[RUNNING] 未知事件: %d\n", event->id);
            break;
    }
}

// 暂停状态处理
void paused_state_handler(StateMachine *sm, const Event *event) {
    switch (event->id) {
        case EVENT_RESUME:
            printf("[PAUSED] 收到RESUME事件 -> 切换到RUNNING\n");
            sm->current_state = STATE_RUNNING;
            break;
        case EVENT_STOP:
            printf("[PAUSED] 收到STOP事件 -> 切换到IDLE\n");
            sm->current_state = STATE_IDLE;
            break;
        default:
            printf("[PAUSED] 未知事件: %d\n", event->id);
            break;
    }
}

// ========== 状态查找表 ==========

static const StateLutEntry state_lut[NUM_STATES] = {
    [STATE_IDLE]    = {.handler = idle_state_handler},
    [STATE_RUNNING] = {.handler = running_state_handler},
    [STATE_PAUSED]  = {.handler = paused_state_handler}
};

// ========== 状态机API ==========

void sm_init(StateMachine *sm) {
    sm->current_state = STATE_IDLE;
    sm->context = NULL;
}

void sm_dispatch_event(StateMachine *sm, const Event *event) {
    if (sm->current_state < NUM_STATES) {
        StateHandler handler = state_lut[sm->current_state].handler;
        if (handler != NULL) {
            handler(sm, event);
        }
    }
}

// ========== 测试代码 ==========

int main() {
    StateMachine sm;
    Event event;

    sm_init(&sm);

    // 测试状态转换
    event.id = EVENT_START;
    sm_dispatch_event(&sm, &event);

    event.id = EVENT_PAUSE;
    sm_dispatch_event(&sm, &event);

    event.id = EVENT_RESUME;
    sm_dispatch_event(&sm, &event);

    event.id = EVENT_STOP;
    sm_dispatch_event(&sm, &event);

    return 0;
}
```

**输出**：
```
[IDLE] 收到START事件 -> 切换到RUNNING
[RUNNING] 收到PAUSE事件 -> 切换到PAUSED
[PAUSED] 收到RESUME事件 -> 切换到RUNNING
[RUNNING] 收到STOP事件 -> 切换到IDLE
```

---

## 📝 实战示例

### 示例1：TCP连接状态机

```c
#include <stdio.h>
#include <string.h>

// TCP状态
typedef enum {
    TCP_CLOSED,
    TCP_LISTEN,
    TCP_SYN_SENT,
    TCP_SYN_RECEIVED,
    TCP_ESTABLISHED,
    TCP_FIN_WAIT_1,
    TCP_FIN_WAIT_2,
    TCP_CLOSE_WAIT,
    TCP_CLOSING,
    TCP_LAST_ACK,
    TCP_TIME_WAIT,
    TCP_NUM_STATES
} TcpState;

// TCP事件
typedef enum {
    TCP_EVENT_PASSIVE_OPEN,
    TCP_EVENT_ACTIVE_OPEN,
    TCP_EVENT_SYN,
    TCP_EVENT_SYN_ACK,
    TCP_EVENT_ACK,
    TCP_EVENT_FIN,
    TCP_EVENT_CLOSE,
    TCP_EVENT_TIMEOUT
} TcpEvent;

// TCP连接
typedef struct {
    TcpState state;
    char remote_ip[16];
    int remote_port;
} TcpConnection;

// 状态名称
const char *state_names[] = {
    "CLOSED", "LISTEN", "SYN_SENT", "SYN_RECEIVED",
    "ESTABLISHED", "FIN_WAIT_1", "FIN_WAIT_2",
    "CLOSE_WAIT", "CLOSING", "LAST_ACK", "TIME_WAIT"
};

// 状态处理函数
typedef void (*TcpStateHandler)(TcpConnection *conn, TcpEvent event);

// CLOSED状态处理
void tcp_closed_handler(TcpConnection *conn, TcpEvent event) {
    switch (event) {
        case TCP_EVENT_PASSIVE_OPEN:
            printf("  被动打开 -> LISTEN\n");
            conn->state = TCP_LISTEN;
            break;
        case TCP_EVENT_ACTIVE_OPEN:
            printf("  主动打开，发送SYN -> SYN_SENT\n");
            conn->state = TCP_SYN_SENT;
            break;
        default:
            printf("  CLOSED: 忽略事件\n");
            break;
    }
}

// LISTEN状态处理
void tcp_listen_handler(TcpConnection *conn, TcpEvent event) {
    switch (event) {
        case TCP_EVENT_SYN:
            printf("  收到SYN，发送SYN-ACK -> SYN_RECEIVED\n");
            conn->state = TCP_SYN_RECEIVED;
            break;
        case TCP_EVENT_CLOSE:
            printf("  关闭监听 -> CLOSED\n");
            conn->state = TCP_CLOSED;
            break;
        default:
            printf("  LISTEN: 忽略事件\n");
            break;
    }
}

// SYN_SENT状态处理
void tcp_syn_sent_handler(TcpConnection *conn, TcpEvent event) {
    switch (event) {
        case TCP_EVENT_SYN_ACK:
            printf("  收到SYN-ACK，发送ACK -> ESTABLISHED\n");
            conn->state = TCP_ESTABLISHED;
            break;
        case TCP_EVENT_CLOSE:
            printf("  关闭连接 -> CLOSED\n");
            conn->state = TCP_CLOSED;
            break;
        default:
            printf("  SYN_SENT: 忽略事件\n");
            break;
    }
}

// SYN_RECEIVED状态处理
void tcp_syn_received_handler(TcpConnection *conn, TcpEvent event) {
    switch (event) {
        case TCP_EVENT_ACK:
            printf("  收到ACK -> ESTABLISHED\n");
            conn->state = TCP_ESTABLISHED;
            break;
        case TCP_EVENT_CLOSE:
            printf("  关闭连接，发送FIN -> FIN_WAIT_1\n");
            conn->state = TCP_FIN_WAIT_1;
            break;
        default:
            printf("  SYN_RECEIVED: 忽略事件\n");
            break;
    }
}

// ESTABLISHED状态处理
void tcp_established_handler(TcpConnection *conn, TcpEvent event) {
    switch (event) {
        case TCP_EVENT_FIN:
            printf("  收到FIN，发送ACK -> CLOSE_WAIT\n");
            conn->state = TCP_CLOSE_WAIT;
            break;
        case TCP_EVENT_CLOSE:
            printf("  主动关闭，发送FIN -> FIN_WAIT_1\n");
            conn->state = TCP_FIN_WAIT_1;
            break;
        default:
            printf("  ESTABLISHED: 数据传输中\n");
            break;
    }
}

// 状态查找表
static const TcpStateHandler tcp_state_handlers[TCP_NUM_STATES] = {
    [TCP_CLOSED]       = tcp_closed_handler,
    [TCP_LISTEN]       = tcp_listen_handler,
    [TCP_SYN_SENT]     = tcp_syn_sent_handler,
    [TCP_SYN_RECEIVED] = tcp_syn_received_handler,
    [TCP_ESTABLISHED]  = tcp_established_handler,
    // 其他状态省略...
};

// 处理事件
void tcp_handle_event(TcpConnection *conn, TcpEvent event) {
    printf("当前状态: %s\n", state_names[conn->state]);

    if (conn->state < TCP_NUM_STATES && tcp_state_handlers[conn->state]) {
        tcp_state_handlers[conn->state](conn, event);
    }

    printf("新状态: %s\n\n", state_names[conn->state]);
}

int main() {
    TcpConnection conn = {0};
    conn.state = TCP_CLOSED;
    strcpy(conn.remote_ip, "192.168.1.1");
    conn.remote_port = 8080;

    printf("=== TCP三次握手 ===\n");
    tcp_handle_event(&conn, TCP_EVENT_ACTIVE_OPEN);  // CLOSED -> SYN_SENT
    tcp_handle_event(&conn, TCP_EVENT_SYN_ACK);      // SYN_SENT -> ESTABLISHED

    printf("=== 数据传输 ===\n");
    tcp_handle_event(&conn, TCP_EVENT_ACK);          // 保持ESTABLISHED

    printf("=== TCP四次挥手 ===\n");
    tcp_handle_event(&conn, TCP_EVENT_CLOSE);        // ESTABLISHED -> FIN_WAIT_1

    return 0;
}
```

### 示例2：电梯控制系统

```c
#include <stdio.h>
#include <stdbool.h>

// 电梯状态
typedef enum {
    ELEVATOR_IDLE,
    ELEVATOR_MOVING_UP,
    ELEVATOR_MOVING_DOWN,
    ELEVATOR_DOOR_OPENING,
    ELEVATOR_DOOR_CLOSING,
    ELEVATOR_NUM_STATES
} ElevatorState;

// 电梯事件
typedef enum {
    EVENT_CALL_UP,
    EVENT_CALL_DOWN,
    EVENT_ARRIVED,
    EVENT_DOOR_OPEN_COMPLETE,
    EVENT_DOOR_CLOSE_COMPLETE
} ElevatorEvent;

// 电梯系统
typedef struct {
    ElevatorState state;
    int current_floor;
    int target_floor;
    bool door_open;
} Elevator;

// 状态处理函数声明
typedef void (*ElevatorHandler)(Elevator *elev, ElevatorEvent event);

// 空闲状态
void elevator_idle_handler(Elevator *elev, ElevatorEvent event) {
    switch (event) {
        case EVENT_CALL_UP:
            if (elev->target_floor > elev->current_floor) {
                printf("  开始上行 %d -> %d\n",
                       elev->current_floor, elev->target_floor);
                elev->state = ELEVATOR_MOVING_UP;
            }
            break;
        case EVENT_CALL_DOWN:
            if (elev->target_floor < elev->current_floor) {
                printf("  开始下行 %d -> %d\n",
                       elev->current_floor, elev->target_floor);
                elev->state = ELEVATOR_MOVING_DOWN;
            }
            break;
        default:
            break;
    }
}

// 上行状态
void elevator_moving_up_handler(Elevator *elev, ElevatorEvent event) {
    if (event == EVENT_ARRIVED) {
        elev->current_floor++;
        printf("  到达 %d 楼\n", elev->current_floor);

        if (elev->current_floor == elev->target_floor) {
            printf("  到达目标楼层，开门\n");
            elev->state = ELEVATOR_DOOR_OPENING;
        }
    }
}

// 下行状态
void elevator_moving_down_handler(Elevator *elev, ElevatorEvent event) {
    if (event == EVENT_ARRIVED) {
        elev->current_floor--;
        printf("  到达 %d 楼\n", elev->current_floor);

        if (elev->current_floor == elev->target_floor) {
            printf("  到达目标楼层，开门\n");
            elev->state = ELEVATOR_DOOR_OPENING;
        }
    }
}

// 开门状态
void elevator_door_opening_handler(Elevator *elev, ElevatorEvent event) {
    if (event == EVENT_DOOR_OPEN_COMPLETE) {
        printf("  门已打开\n");
        elev->door_open = true;
        elev->state = ELEVATOR_DOOR_CLOSING;
    }
}

// 关门状态
void elevator_door_closing_handler(Elevator *elev, ElevatorEvent event) {
    if (event == EVENT_DOOR_CLOSE_COMPLETE) {
        printf("  门已关闭\n");
        elev->door_open = false;
        elev->state = ELEVATOR_IDLE;
    }
}

// 状态处理表
static const ElevatorHandler elevator_handlers[ELEVATOR_NUM_STATES] = {
    [ELEVATOR_IDLE]          = elevator_idle_handler,
    [ELEVATOR_MOVING_UP]     = elevator_moving_up_handler,
    [ELEVATOR_MOVING_DOWN]   = elevator_moving_down_handler,
    [ELEVATOR_DOOR_OPENING]  = elevator_door_opening_handler,
    [ELEVATOR_DOOR_CLOSING]  = elevator_door_closing_handler
};

// 处理事件
void elevator_handle_event(Elevator *elev, ElevatorEvent event) {
    if (elev->state < ELEVATOR_NUM_STATES && elevator_handlers[elev->state]) {
        elevator_handlers[elev->state](elev, event);
    }
}

int main() {
    Elevator elev = {
        .state = ELEVATOR_IDLE,
        .current_floor = 1,
        .target_floor = 5,
        .door_open = false
    };

    printf("电梯初始位置: %d楼\n\n", elev.current_floor);

    // 模拟从1楼到5楼
    printf("=== 按下5楼按钮 ===\n");
    elevator_handle_event(&elev, EVENT_CALL_UP);

    for (int i = 0; i < 4; i++) {
        elevator_handle_event(&elev, EVENT_ARRIVED);
    }

    elevator_handle_event(&elev, EVENT_DOOR_OPEN_COMPLETE);
    elevator_handle_event(&elev, EVENT_DOOR_CLOSE_COMPLETE);

    printf("\n当前状态: IDLE, 当前楼层: %d\n", elev.current_floor);

    return 0;
}
```

---

## 💡 设计技巧

### 1. 使用枚举命名状态和事件

```c
// ✅ 好的做法
typedef enum {
    STATE_IDLE,
    STATE_ACTIVE,
    STATE_ERROR
} State;

// ❌ 不好的做法
#define STATE_IDLE 0
#define STATE_ACTIVE 1
#define STATE_ERROR 2
```

### 2. 使用结构体封装状态机

```c
typedef struct {
    State current_state;
    void *context;      // 上下文数据
    int error_count;    // 错误计数
    // 其他状态机属性...
} StateMachine;
```

### 3. 添加状态进入/退出回调

```c
typedef void (*StateEnterExit)(StateMachine *sm);

typedef struct {
    StateHandler handler;
    StateEnterExit on_enter;   // 进入状态时调用
    StateEnterExit on_exit;    // 退出状态时调用
} StateLutEntry;
```

### 4. 记录状态转换历史

```c
#define HISTORY_SIZE 10

typedef struct {
    State current_state;
    State history[HISTORY_SIZE];
    int history_index;
} StateMachine;

void sm_transition(StateMachine *sm, State new_state) {
    sm->history[sm->history_index] = sm->current_state;
    sm->history_index = (sm->history_index + 1) % HISTORY_SIZE;
    sm->current_state = new_state;
}
```

---

## ⚠️ 常见陷阱

### 1. 忘记初始化状态机

```c
// ❌ 错误
StateMachine sm;
sm_dispatch_event(&sm, &event);  // current_state未初始化！

// ✅ 正确
StateMachine sm;
sm_init(&sm);
sm_dispatch_event(&sm, &event);
```

### 2. 状态处理函数中直接修改状态

```c
// ⚠️ 可能有问题（取决于设计）
void handler(StateMachine *sm, Event *e) {
    sm->current_state = NEW_STATE;  // 直接修改
}

// ✅ 更好的做法
void handler(StateMachine *sm, Event *e) {
    sm_transition(sm, NEW_STATE);  // 使用转换函数
}
```

### 3. 未检查函数指针是否为NULL

```c
// ❌ 危险
state_lut[state].handler(sm, event);

// ✅ 安全
if (state_lut[state].handler != NULL) {
    state_lut[state].handler(sm, event);
}
```

---

## 🔗 相关链接

- [[C语言进阶 - 指针详解]] - 函数指针基础
- [[C语言进阶 - 结构体]] - 结构体应用
- [[Linux系统编程 - 进程管理]] - 进程状态机
- [[C 语言知识地图]] - C语言知识地图

---

## 📚 参考资料

- Design Patterns: Elements of Reusable Object-Oriented Software
- Embedded C Coding Standard

---

## ✅ 学习检查清单

- [ ] 理解状态机的基本概念
- [ ] 掌握函数指针的声明和使用
- [ ] 会使用查找表实现状态机
- [ ] 能够设计状态转换图
- [ ] 实现过至少一个完整的状态机
- [ ] 理解状态机的优缺点
- [ ] 知道何时使用状态机模式

---

*最后更新: 2025-11-18*

## 相关笔记

- [[C语言进阶 - 指针详解]]
- [[C语言进阶 - 结构体]]
- [[C语言基础 - 函数]]
