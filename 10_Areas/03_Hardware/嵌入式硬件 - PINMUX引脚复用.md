---
tags:
  - "#domain/hardware"
  - "#type/concept"
  - "#tech/embedded"
  - "#grain/system-design"
  - "#level/basic"
aliases:
  - Pin Multiplexing
  - PINMUX
  - 引脚复用
create_date: 2025-11-19
notetype: 硬件概念
---

# 嵌入式硬件 - PINMUX引脚复用

## 概述

**PINMUX**，全称是 **Pin Multiplexing**，中文常译为"**引脚复用**"或"**管脚复用**"。它的核心思想非常简单：

> **让一个物理引脚（Pin）在不同的时间或配置下，可以拥有多种不同的功能。**

---

## 为什么需要PINMUX？

### 芯片集成度的挑战

现代芯片（如微控制器MCU、片上系统SoC）内部集成了大量功能模块：

| 功能模块 | 用途 |
|---------|------|
| **GPIO** (General Purpose I/O) | 通用输入输出 - 控制LED、读取按键 |
| **UART** (Universal Asynchronous Receiver/Transmitter) | 串行通信 - 与电脑或其他设备通信 |
| **I2C** (Inter-Integrated Circuit) | 两线式串行总线 - 连接传感器、OLED屏幕 |
| **SPI** (Serial Peripheral Interface) | 高速串行总线 - 连接Flash存储、SD卡 |
| **PWM** (Pulse Width Modulation) | 脉宽调制 - 控制电机转速、调节LED亮度 |
| **ADC** (Analog-to-Digital Converter) | 模数转换器 - 读取模拟传感器值 |
| **CAN** | 控制器局域网 - 汽车电子通信 |
| **I2S** | 音频数据传输 - 音频codec |
| **USB** | 通用串行总线 - 设备连接 |
| **Ethernet** | 以太网接口 - 网络连接 |
| **JTAG/SWD** | 调试接口 - 程序下载和调试 |

### 物理限制

**问题**：
- 假设一个芯片有100个引脚
- 但内部功能模块需要200+个引脚才能全部引出
- **物理上不可能为每个功能分配独立的引脚**

**解决方案**：
- 通过**PINMUX引脚复用技术**，让一个物理引脚可以配置为多种功能之一
- 用户根据实际需求选择需要的功能

---

## PINMUX工作原理

### 基本概念

每个物理引脚连接到一个**多路选择器（Multiplexer）**，该选择器可以将引脚连接到不同的内部功能模块。

```
物理引脚 PA0
    │
    ├───[MUX]─┬─→ 功能0: GPIO (默认)
              ├─→ 功能1: UART0_TX (串口发送)
              ├─→ 功能2: SPI0_MOSI (SPI主出从入)
              └─→ 功能3: TIM0_CH1 (定时器通道1)
```

通过**配置寄存器**选择具体功能：

```c
// 伪代码：将 PA0 配置为 UART0_TX
PINMUX_CONFIG[PA0] = FUNCTION_UART0_TX;
```

### 典型PINMUX配置流程

1. **查阅芯片数据手册**：确定引脚支持的所有复用功能
2. **根据需求选择功能**：例如需要UART通信，选择UART功能
3. **配置PINMUX寄存器**：通过软件设置引脚功能
4. **配置外设参数**：设置波特率、数据位等外设相关参数
5. **启用外设**：使能对应的功能模块

---

## 实际示例

### 示例1：STM32F4 的GPIOA Pin 9

STM32F4系列芯片的 PA9 引脚可以复用为以下功能：

| 功能选择 | 功能名称 | 描述 |
|---------|---------|------|
| **AF0** | GPIO | 通用输入/输出 |
| **AF1** | TIM1_CH2 | 定时器1通道2 |
| **AF7** | USART1_TX | 串口1发送引脚 |
| **AF8** | I2C3_SMBA | I2C3总线管理 |
| **AF12** | OTG_FS_VBUS | USB OTG VBUS检测 |

**配置代码**（将PA9配置为USART1_TX）：

```c
#include "stm32f4xx.h"

void configure_pa9_as_uart_tx(void) {
    // 1. 使能GPIOA时钟
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    // 2. 配置PA9为复用功能模式
    GPIOA->MODER &= ~(3U << (9 * 2));  // 清除原配置
    GPIOA->MODER |= (2U << (9 * 2));   // 设置为复用功能模式

    // 3. 选择复用功能AF7 (USART1)
    GPIOA->AFR[1] &= ~(0xF << ((9 - 8) * 4));  // 清除AF配置
    GPIOA->AFR[1] |= (7U << ((9 - 8) * 4));    // 设置为AF7

    // 4. 配置输出类型（推挽输出）
    GPIOA->OTYPER &= ~(1U << 9);

    // 5. 配置输出速度（高速）
    GPIOA->OSPEEDR |= (3U << (9 * 2));

    // 6. 配置上拉/下拉（上拉）
    GPIOA->PUPDR &= ~(3U << (9 * 2));
    GPIOA->PUPDR |= (1U << (9 * 2));
}
```

---

### 示例2：Linux设备树中的PINMUX配置

在Linux系统中，PINMUX通常通过**设备树（Device Tree）** 配置。

**示例：Raspberry Pi GPIO复用配置**

```dts
&gpio {
    spi0_pins: spi0 {
        brcm,pins = <9 10 11>;      /* GPIO 9, 10, 11 */
        brcm,function = <4>;         /* 复用功能4: SPI0 */
    };

    uart0_pins: uart0 {
        brcm,pins = <14 15>;         /* GPIO 14, 15 */
        brcm,function = <4>;         /* 复用功能4: UART0 */
    };

    i2c1_pins: i2c1 {
        brcm,pins = <2 3>;           /* GPIO 2, 3 */
        brcm,function = <4>;         /* 复用功能4: I2C1 */
    };
};
```

**激活配置**：

```dts
&spi0 {
    pinctrl-names = "default";
    pinctrl-0 = <&spi0_pins>;
    status = "okay";
};

&uart0 {
    pinctrl-names = "default";
    pinctrl-0 = <&uart0_pins>;
    status = "okay";
};
```

---

### 示例3：RISC-V芯片 SiFive FE310

**引脚配置寄存器**：

```c
// FE310 的 IOF (I/O Function) 寄存器
#define IOF_SEL     (0x10012038)  // I/O Function Select
#define IOF_EN      (0x10012034)  // I/O Function Enable

// 将 GPIO17 配置为 SPI MOSI
void configure_gpio17_spi_mosi(void) {
    // 选择IOF0功能（SPI）
    *(volatile uint32_t*)IOF_SEL &= ~(1 << 17);

    // 使能IOF功能
    *(volatile uint32_t*)IOF_EN |= (1 << 17);
}

// 将 GPIO17 恢复为 GPIO
void configure_gpio17_as_gpio(void) {
    // 禁用IOF功能
    *(volatile uint32_t*)IOF_EN &= ~(1 << 17);
}
```

---

## PINMUX配置注意事项

### 1. 引脚功能冲突

**问题**：如果两个外设配置了相同的引脚，会发生冲突。

**示例**：
```c
// ❌ 错误：PA9 被配置为两种功能
configure_pin(PA9, UART_TX);  // UART发送
configure_pin(PA9, I2C_SDA);  // I2C数据线
// 结果：未定义行为，两个外设都无法正常工作
```

**解决**：
- 查阅引脚分配表（Pinout Diagram）
- 使用不同的引脚，或只启用一个功能

### 2. 上电默认状态

大多数芯片在**上电复位后**，引脚默认配置为：
- **GPIO输入模式**（高阻态）
- 部分引脚可能有默认复用功能（如调试接口JTAG/SWD）

**最佳实践**：
- 在初始化代码中明确配置所有使用的引脚
- 不要假设引脚的初始状态

### 3. 电气特性配置

配置PINMUX后，还需配置引脚的**电气特性**：

| 参数 | 选项 | 说明 |
|------|------|------|
| **输出类型** | 推挽 (Push-Pull) / 开漏 (Open-Drain) | 推挽用于普通输出，开漏用于I2C等总线 |
| **输出速度** | 低速 / 中速 / 高速 / 超高速 | 影响信号完整性和EMI |
| **上拉/下拉** | 上拉 / 下拉 / 浮空 | 确定输入悬空时的默认电平 |
| **施密特触发** | 使能 / 禁用 | 提高抗干扰能力 |

**示例：I2C需要开漏输出 + 外部上拉电阻**

```c
// 配置 PB6 为 I2C1_SCL (开漏输出)
GPIOB->MODER |= (2U << (6 * 2));    // 复用功能模式
GPIOB->AFR[0] |= (4U << (6 * 4));   // AF4: I2C1
GPIOB->OTYPER |= (1U << 6);         // 开漏输出 (Open-Drain)
GPIOB->PUPDR |= (1U << (6 * 2));    // 内部上拉（或使用外部上拉电阻）
```

### 4. 调试接口占用

许多芯片的**JTAG/SWD调试接口**会占用部分GPIO引脚。

**常见情况**：
- STM32F4：PA13 (SWDIO), PA14 (SWCLK)
- ESP32：GPIO12, GPIO13, GPIO14, GPIO15（部分用于boot模式选择）

**风险**：
- 如果禁用调试接口，可能无法再次烧录程序（需要芯片擦除）

**建议**：
- 开发阶段保留调试接口
- 量产版本可以禁用以释放引脚

---

## PINMUX配置工具

### 1. 图形化配置工具

| 工具 | 适用芯片 | 功能 |
|------|---------|------|
| **STM32CubeMX** | STM32系列 | 可视化配置PINMUX、时钟、外设，自动生成初始化代码 |
| **MCUXpresso Config Tools** | NXP i.MX, LPC系列 | 图形化引脚配置 |
| **Microchip MPLAB Harmony** | PIC32, SAM系列 | 全栈配置工具 |
| **Espressif IDF** | ESP32系列 | 命令行 + menuconfig配置 |

**STM32CubeMX 截图示例**：

```
[Pinout View]
┌─────────────────────────┐
│  PA0: GPIO_Input        │
│  PA1: TIM2_CH2          │
│  PA9: USART1_TX        │
│  PA10: USART1_RX        │
│  ...                    │
└─────────────────────────┘
```

**优势**：
- 可视化冲突检测
- 自动生成初始化代码
- 减少手动配置错误

### 2. 设备树（Device Tree）

Linux系统中使用**设备树（DTS/DTSI文件）** 描述硬件配置。

**查看当前引脚配置**：

```bash
# 查看GPIO引脚状态
$ cat /sys/kernel/debug/gpio

# 查看pinctrl配置
$ cat /sys/kernel/debug/pinctrl/pinctrl-maps
```

### 3. 寄存器直接配置

对于裸机开发，通过读写寄存器配置PINMUX：

```c
// 通用配置函数
void pinmux_config(uint8_t pin, uint8_t function) {
    volatile uint32_t *reg = PINMUX_BASE + (pin / 4);
    uint32_t shift = (pin % 4) * 8;

    *reg &= ~(0xFF << shift);    // 清除原配置
    *reg |= (function << shift);  // 设置新功能
}
```

---

## PINMUX与GPIO的关系

### 区别

| 特性 | GPIO | PINMUX |
|------|------|--------|
| **层次** | 功能层 | 配置层 |
| **作用** | 实现输入/输出功能 | 选择引脚连接到哪个功能模块 |
| **配置** | 方向（输入/输出）、电平 | 引脚复用功能选择 |

### 配置顺序

1. **PINMUX配置**：选择引脚功能（GPIO或其他外设）
2. **GPIO/外设配置**：如果选择了GPIO，配置输入/输出方向；如果选择了外设，配置外设参数

**示例**：

```c
// 1. PINMUX: 将 PA5 配置为 GPIO
pinmux_select(PA5, FUNCTION_GPIO);

// 2. GPIO: 配置为输出模式
gpio_set_direction(PA5, GPIO_OUTPUT);

// 3. 使用: 设置高电平
gpio_set(PA5, HIGH);
```

---

## 常见应用场景

### 1. 多功能开发板

开发板（如Arduino、Raspberry Pi）通过PINMUX实现引脚的灵活配置。

**Arduino Uno引脚复用**：

| 引脚 | 默认 | 复用功能 |
|------|------|---------|
| D0 | GPIO | RX (UART) |
| D1 | GPIO | TX (UART) |
| D3 | GPIO | PWM (OC2B) |
| D13 | GPIO | SCK (SPI) |
| A4 | Analog Input | SDA (I2C) |
| A5 | Analog Input | SCL (I2C) |

### 2. 产品设计优化

在产品设计中，根据实际需求选择引脚功能，最大化利用芯片资源。

**案例：智能温控器**

| 功能 | 引脚 | PINMUX配置 |
|------|------|----------|
| 温度传感器 (I2C) | PA9, PA10 | I2C_SCL, I2C_SDA |
| 显示屏 (SPI) | PB13-15 | SPI_SCK, SPI_MOSI, SPI_MISO |
| 按键输入 | PC0-3 | GPIO_Input |
| 继电器控制 | PD5 | GPIO_Output |
| 调试接口 (UART) | PA2, PA3 | USART_TX, USART_RX |

### 3. 动态功能切换

某些应用需要在运行时切换引脚功能。

**示例：共享引脚的UART调试和产品功能**

```c
// 启动阶段：使用UART调试
void boot_init(void) {
    pinmux_config(PA9, FUNCTION_UART_TX);
    uart_init();
    uart_print("Boot message\n");
}

// 运行阶段：切换为PWM控制LED
void runtime_init(void) {
    uart_deinit();
    pinmux_config(PA9, FUNCTION_PWM);
    pwm_init();
}
```

---

## 调试技巧

### 1. 检查引脚配置

**方法1：读取寄存器值**

```c
void print_pin_config(uint8_t pin) {
    uint32_t moder = (GPIOA->MODER >> (pin * 2)) & 0x3;
    uint32_t afr = (GPIOA->AFR[pin / 8] >> ((pin % 8) * 4)) & 0xF;

    printf("Pin PA%d - Mode: %lu, AF: %lu\n", pin, moder, afr);
}
```

**方法2：使用调试器查看寄存器**

在调试器中查看 GPIO 和 PINMUX 相关寄存器。

### 2. 示波器验证

使用示波器观察引脚的实际电平和波形，确认配置是否生效。

### 3. 逐步排查

1. 确认PINMUX配置正确
2. 确认外设初始化完成
3. 确认引脚电气特性配置（上拉/下拉、输出类型）
4. 确认外设使能

---

## 相关资源

- [[Linux系统编程 - 进程管理]]：Linux下的GPIO和PINMUX控制
- [[C语言标准库 - stdio.h详解]]：嵌入式调试输出
- [[Makefile完全指南]]：嵌入式项目构建

## 参考资料

- [STM32F4 Reference Manual](https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)
- [Linux GPIO Subsystem](https://www.kernel.org/doc/html/latest/driver-api/gpio/index.html)
- [Device Tree Bindings](https://www.devicetree.org/)

---

**最后更新**: 2025-11-19
