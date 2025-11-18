eq_delay_time 开发学习Record



## Basic

### `->` 操作符

- `->`在c中是一个结构体指针操作符，用于访问结构体的成员，即通过指向结构体的指针访问结构体的成员

- 用法

  ```c
  pointer -> member
  
  // pointer 是指向结构体的指针
  // member 是结构体的成员
  ```

- 区分开 `.` ，`.`是用于直接访问结构体变量的成员，`->` 是通过结构体指针来访问结构体的成员



### `static void rx_eq_state_handler(struct pma_rx_t *rx, const struct pma_rx_event_t *event)`

这行代码中：

* `struct pma_rx_t *rx` 是一个指向 `pma_rx_t ` 结构体的指针
* `const struct pma_rx_event_t *event` 是一个指向常量 `pma_rx_event_t` 结构体的指针。
* `switch (event->id)` 中，`id` 是结构体 `event` 的成员



### 向上溯源

往 `rx_eq_state_handler` 这个函数向上溯源之后，查到定义代码为：

```c
static const struct state_lut_entry_t state_lut[NUM_PMW_RX_STATES] = {
    ...
    {.state_handler = rx_eq_state_handler,}
    ...
};

```

- 这里的 `state_lut_entry_t` 前面 接有 结构体的标符，所以是一个结构体类型，其中包括状态处理函数 `state_handler` ,从下面括号内的内容可以理解为这个函数指针是指向一个函数来处理与当前状态相关的事件。
- `state_lut` 数组：数组的类型为 `state_lut_entry_t`， 大小是`NUM_PMW_RX_STATES`。每个数组元素包含一个 `state_handler`，用于处理与该状态相关的操作或事件。



### 状态查找表

是一种常见的用于实现状态机的技术，它通过一个表来存储与不同状态对应的行为或函数，简化了状态机的设计，避免了使用大量的 `if-else` 或 `switch` 语句。



#### 主要思想：

- **查找表** 是一个包含多个元素的数组或结构体，每个元素包含与某个状态相关的处理函数或数据。
- 根据当前状态，程序可以直接从查找表中找到与该状态相关的处理函数，然后执行。



### 状态机

**状态机**（State Machine）是一种用于建模和处理系统行为的数学模型。它通过在多个 **状态** 之间进行转换，根据输入事件或条件来决定系统的行为。状态机通常用于处理具有离散状态和状态之间转换的系统。



#### 基本组成：

1. **状态（State）**：系统在某一时刻所处的具体情形。每个状态表示系统的一个特定状态或行为。
2. **事件（Event）**：触发状态转换的条件或输入。事件可以是外部输入或内部变化。
3. **转换（Transition）**：当系统接收到某个事件时，它从一个状态转换到另一个状态。
4. **动作（Action）**：每次状态转换时，可能会执行的操作或任务。



#### 状态机的工作原理：

- 系统从一个初始状态开始，接收输入事件。
- 根据当前状态和输入事件的组合，系统执行一个状态转换到另一个状态。
- 在状态转换时，可能会执行某些动作（例如处理数据、发送信号等）。
- 系统根据不同的输入和状态，不断在状态之间切换，执行不同的操作。



#### 结合向上溯源的代码：

假设 `state_lut` 是一个状态查找表，每个元素都包含一个指向函数的指针（如 `rx_eq_state_handler`）。当状态机运行时，它会根据当前状态查找 `state_lut` 表，找到对应的状态处理函数，然后调用该函数来处理与该状态相关的事件。



示例代码：

```c
// 定义状态枚举
typedef enum {
    STATE_IDLE,
    STATE_RECEIVING,
    STATE_PROCESSING,
    NUM_PMW_RX_STATES // 状态数量
} state_t;

// 定义每个状态的处理函数
void rx_eq_state_handler(void) {
    // 处理接收状态的逻辑
    printf("Handling RX EQ state\n");
}

void idle_state_handler(void) {
    // 处理空闲状态的逻辑
    printf("Handling IDLE state\n");
}

// 定义状态查找表结构体
struct state_lut_entry_t {
    void (*state_handler)(void); // 状态处理函数指针
};

// 初始化状态查找表
static const struct state_lut_entry_t state_lut[NUM_PMW_RX_STATES] = {
    [STATE_IDLE] = {.state_handler = idle_state_handler},
    [STATE_RECEIVING] = {.state_handler = rx_eq_state_handler},
    // 其他状态的处理函数
};

// 状态机函数
void state_machine(state_t current_state) {
    // 查找表通过当前状态索引到对应的状态处理函数
    state_lut[current_state].state_handler();
}

int main() {
    // 假设当前状态为 STATE_RECEIVING
    state_machine(STATE_RECEIVING); // 调用 rx_eq_state_handler 处理接收状态
    return 0;
}

```

