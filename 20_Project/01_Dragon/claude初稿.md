# 日志模块重构设计方案

## 文档版本控制

```
版本日期作者修改说明
v1.02024-11-17[Your Name]初始版本
```

## 1. 项目背景与目标

### 1.1 当前问题分析

当前系统使用的`str_mode`日志模块存在以下问题:

1. **代码空间占用过大**
   - 每个日志点都需要存储完整的格式化字符串
   - 典型的日志字符串占用50-100字节
   - 如果项目中有500个日志点,仅字符串就占用25KB-50KB
   - printf家族函数的链接会引入额外的库代码(约5-10KB)

1. **RAM占用问题**
   - 格式化字符串处理需要栈空间
   - 每次日志调用可能需要100-200字节的栈空间

1. **可扩展性差**
   - 字符串模式下难以实现日志的持久化存储
   - 无法有效实现日志的统计分析功能

### 1.2 项目目标

1. **主要目标**
   - 将代码空间占用减少60%-80%
   - 将运行时RAM占用减少50%以上
   - 保持完整的日志信息追溯能力

1. **次要目标**
   - 提供统一的日志接口,支持模式切换
   - 支持编译时和运行时的日志开关
   - 支持多种输出目标(UART/RAM/外部存储)
   - 提供配套的日志解析工具

### 1.3 设计约束

1. **兼容性约束**
   - 必须保持现有日志调用接口不变
   - 两种模式只能选择其一编译,不能同时存在

1. **资源约束**
   - RAM缓冲区大小可配置,默认建议64-128条
   - 外部存储(如果使用)容量有限,需要考虑磨损均衡

1. **性能约束**
   - 单次日志记录操作不应超过100微秒
   - 临界区保护时间应尽可能短

## 2. 总体架构设计

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                       应用层代码                              │
│  (使用统一的日志宏: TEST_LOG_XXX_MSG)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   日志接口层 (ww_log.h)                       │
│  - 统一的日志宏定义                                           │
│  - 编译时模式选择                                             │
│  - 静态开关控制                                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│  str_mode     │   │  encode_mode     │
│  实现层       │   │  实现层          │
└───────┬───────┘   └────────┬─────────┘
        │                    │
        │                    ▼
        │           ┌─────────────────┐
        │           │  编码模块        │
        │           │  - 文件ID映射    │
        │           │  - 位置编码      │
        │           └────────┬─────────┘
        │                    │
        └────────┬───────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    输出管理层                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐              │
│  │  UART    │  │   RAM    │  │  外部存储    │              │
│  │  输出    │  │  缓冲区  │  │  (可选)      │              │
│  └──────────┘  └──────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────┘
                 ▲
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  RSDK接口    │  │  调试工具    │
│  (读取日志)  │  │  接口        │
└──────────────┘  └──────────────┘
```

### 2.2 模块划分

```
模块名称文件职责
日志接口层ww_log.h定义统一的日志宏,提供编译开关
文件ID管理log_file_id.h集中管理所有源文件的唯一编号
str_mode实现ww_log_str.c传统字符串日志的实现
encode_mode实现ww_log_encode.c编码日志的实现
RAM缓冲区管理ww_log_ram.c环形缓冲区的操作
外存管理(可选)ww_log_storage.c外部存储的读写操作
配置管理ww_log_config.h所有可配置参数的定义
RSDK接口ww_log_api.c提供给外部工具的读取接口
```

### 2.3 编译配置方案

通过宏定义控制编译选项:

c

```c
// ww_log_config.h

// ============ 模式选择 (二选一) ============
// #define CONFIG_WW_LOG_STR_MODE          // 字符串模式
#define CONFIG_WW_LOG_ENCODE_MODE       // 编码模式

// ============ 全局日志级别 ============
#define CONFIG_WW_LOG_LEVEL_DEFAULT     WW_LOG_LEVEL_ERR

// ============ 输出目标选择 ============
#define CONFIG_WW_LOG_OUTPUT_UART       // 输出到UART
#define CONFIG_WW_LOG_OUTPUT_RAM        // 保存到RAM
// #define CONFIG_WW_LOG_OUTPUT_FLASH   // 保存到Flash(可选)

// ============ RAM缓冲区配置 ============
#define CONFIG_WW_LOG_RAM_ENTRY_NUM     64    // 缓冲区条目数
#define CONFIG_WW_LOG_RAM_PERSISTENT    1     // 热重启后保留

// ============ 子模块静态开关 ============
#define CONFIG_WW_LOG_MOD_INIT_EN       // 使能INIT模块日志
#define CONFIG_WW_LOG_MOD_SENSOR_EN     // 使能SENSOR模块日志
// #define CONFIG_WW_LOG_MOD_MOTOR_EN   // 禁用MOTOR模块日志
```

## 3. 详细设计

### 3.1 文件编号管理方案

#### 3.1.1 设计思路

使用枚举集中管理所有源文件的唯一编号,确保全局唯一性和易维护性。

#### 3.1.2 实现细节

c

```c
// log_file_id.h
#ifndef LOG_FILE_ID_H
#define LOG_FILE_ID_H

/**
 * 文件编号枚举
 * 说明:
 * 1. 每个需要打印日志的.c文件都应该在此枚举中分配一个唯一ID
 * 2. 枚举值会自动递增,无需手动指定数值
 * 3. ID范围: 1-4095 (12位可表示)
 * 4. 添加新文件时,在对应分类下添加即可
 */
typedef enum {
    FILE_ID_INVALID = 0,
    
    /* 系统初始化模块 (1-50) */
    FILE_ID_MAIN,
    FILE_ID_SYSTEM_INIT,
    FILE_ID_CLOCK_CONFIG,
    FILE_ID_POWER_MANAGER,
    
    /* 驱动层模块 (51-150) */
    FILE_ID_I2C_DRIVER = 51,
    FILE_ID_SPI_DRIVER,
    FILE_ID_UART_DRIVER,
    FILE_ID_GPIO_DRIVER,
    FILE_ID_ADC_DRIVER,
    
    /* 传感器模块 (151-250) */
    FILE_ID_SENSOR_TEMPERATURE = 151,
    FILE_ID_SENSOR_PRESSURE,
    FILE_ID_SENSOR_HUMIDITY,
    
    /* 算法模块 (251-350) */
    FILE_ID_TEMP_CONTROL = 251,
    FILE_ID_PID_ALGORITHM,
    FILE_ID_FILTER_MODULE,
    
    /* 通信模块 (351-450) */
    FILE_ID_PROTOCOL_HANDLER = 351,
    FILE_ID_UART_COMM,
    FILE_ID_NETWORK_STACK,
    
    /* 应用层模块 (451-550) */
    FILE_ID_APP_MAIN = 451,
    FILE_ID_STATE_MACHINE,
    FILE_ID_ERROR_HANDLER,
    
    FILE_ID_MAX  // 边界值,用于检查
} LOG_FILE_ID_E;

/* 编译时检查文件ID是否超出12位范围 */
#if (FILE_ID_MAX > 4095)
#error "File ID exceeds 12-bit range (max 4095)"
#endif

#endif /* LOG_FILE_ID_H */
```

#### 3.1.3 使用方法

在每个需要打印日志的.c文件开头定义当前文件ID:

c

```c
// sensor_temperature.c
#include "log_file_id.h"
#include "ww_log.h"

// 定义当前文件的ID
#define CURRENT_FILE_ID  FILE_ID_SENSOR_TEMPERATURE

// 后续使用日志宏时会自动使用这个ID
void temp_sensor_init(void) {
    TEST_LOG_INFO_MSG("Temperature sensor initializing...");
    // ...
}
```

### 3.2 日志级别定义

c

```c
// ww_log.h

/**
 * 日志级别定义
 * 级别越低越重要,数值越小
 */
typedef enum {
    WW_LOG_LEVEL_OFF = 0,   // 关闭所有日志
    WW_LOG_LEVEL_ERR = 1,   // 错误:系统异常,需要立即关注
    WW_LOG_LEVEL_WRN = 2,   // 警告:潜在问题,建议关注
    WW_LOG_LEVEL_INF = 3,   // 信息:关键流程节点
    WW_LOG_LEVEL_DBG = 4,   // 调试:详细的调试信息
} WW_LOG_LEVEL_E;

// 级别字符串,用于str_mode输出
static const char* g_log_level_str[] = {
    "OFF",
    "ERR",
    "WRN", 
    "INF",
    "DBG"
};
```

### 3.3 统一日志接口设计

#### 3.3.1 基础日志宏

c

```c
// ww_log.h

/**
 * 通用日志宏
 * 根据编译配置自动选择str_mode或encode_mode
 */
#ifdef CONFIG_WW_LOG_ENCODE_MODE
    // ========== encode_mode实现 ==========
    #define TEST_LOG_ERR_MSG(fmt, ...) \
        LOG_ENCODE_WRITE(WW_LOG_LEVEL_ERR, fmt, ##__VA_ARGS__)
    
    #define TEST_LOG_WRN_MSG(fmt, ...) \
        LOG_ENCODE_WRITE(WW_LOG_LEVEL_WRN, fmt, ##__VA_ARGS__)
    
    #define TEST_LOG_INF_MSG(fmt, ...) \
        LOG_ENCODE_WRITE(WW_LOG_LEVEL_INF, fmt, ##__VA_ARGS__)
    
    #define TEST_LOG_DBG_MSG(fmt, ...) \
        LOG_ENCODE_WRITE(WW_LOG_LEVEL_DBG, fmt, ##__VA_ARGS__)

#else  // CONFIG_WW_LOG_STR_MODE
    // ========== str_mode实现 ==========
    #define TEST_LOG_ERR_MSG(fmt, ...) \
        LOG_STR_WRITE(WW_LOG_LEVEL_ERR, fmt, ##__VA_ARGS__)
    
    #define TEST_LOG_WRN_MSG(fmt, ...) \
        LOG_STR_WRITE(WW_LOG_LEVEL_WRN, fmt, ##__VA_ARGS__)
    
    #define TEST_LOG_INF_MSG(fmt, ...) \
        LOG_STR_WRITE(WW_LOG_LEVEL_INF, fmt, ##__VA_ARGS__)
    
    #define TEST_LOG_DBG_MSG(fmt, ...) \
        LOG_STR_WRITE(WW_LOG_LEVEL_DBG, fmt, ##__VA_ARGS__)
#endif
```

#### 3.3.2 带模块名的日志宏

支持为不同子模块定义专用的日志宏,方便分类管理:

c

```c
// ww_log.h

// INIT模块日志宏
#ifdef CONFIG_WW_LOG_MOD_INIT_EN
    #define WW_INIT_LOG_ERR(fmt, ...)  TEST_LOG_ERR_MSG(fmt, ##__VA_ARGS__)
    #define WW_INIT_LOG_WRN(fmt, ...)  TEST_LOG_WRN_MSG(fmt, ##__VA_ARGS__)
    #define WW_INIT_LOG_INF(fmt, ...)  TEST_LOG_INF_MSG(fmt, ##__VA_ARGS__)
    #define WW_INIT_LOG_DBG(fmt, ...)  TEST_LOG_DBG_MSG(fmt, ##__VA_ARGS__)
#else
    // 编译时关闭,宏定义为空
    #define WW_INIT_LOG_ERR(fmt, ...)
    #define WW_INIT_LOG_WRN(fmt, ...)
    #define WW_INIT_LOG_INF(fmt, ...)
    #define WW_INIT_LOG_DBG(fmt, ...)
#endif

// SENSOR模块日志宏
#ifdef CONFIG_WW_LOG_MOD_SENSOR_EN
    #define WW_SENSOR_LOG_ERR(fmt, ...) TEST_LOG_ERR_MSG(fmt, ##__VA_ARGS__)
    #define WW_SENSOR_LOG_WRN(fmt, ...) TEST_LOG_WRN_MSG(fmt, ##__VA_ARGS__)
    #define WW_SENSOR_LOG_INF(fmt, ...) TEST_LOG_INF_MSG(fmt, ##__VA_ARGS__)
    #define WW_SENSOR_LOG_DBG(fmt, ...) TEST_LOG_DBG_MSG(fmt, ##__VA_ARGS__)
#else
    #define WW_SENSOR_LOG_ERR(fmt, ...)
    #define WW_SENSOR_LOG_WRN(fmt, ...)
    #define WW_SENSOR_LOG_INF(fmt, ...)
    #define WW_SENSOR_LOG_DBG(fmt, ...)
#endif

// 可以继续添加其他模块...
```

### 3.4 encode_mode详细设计

#### 3.4.1 编码格式定义

使用32位整数编码日志信息,位域分配如下:

```
 31                    20 19                8 7       4 3      0
┌──────────────────────┬────────────────────┬─────────┬────────┐
│   File ID (12 bits)  │  Line No (12 bits) │Reserved │ Level  │
│      0-4095          │     0-4095         │ (4 bits)│(4 bits)│
└──────────────────────┴────────────────────┴─────────┴────────┘

说明:
- Bits [31:20]: 文件ID,取值范围0-4095
- Bits [19:8]:  行号,取值范围0-4095  
- Bits [7:4]:   保留位,可用于扩展(如时间戳压缩、任务ID等)
- Bits [3:0]:   日志级别,取值0-15
```

#### 3.4.2 编码宏定义

c

```c
// ww_log_encode.h

// 位域位置定义
#define LOG_ENCODE_FILE_ID_SHIFT    20
#define LOG_ENCODE_LINE_NUM_SHIFT   8
#define LOG_ENCODE_RESERVED_SHIFT   4
#define LOG_ENCODE_LEVEL_SHIFT      0

// 位域掩码
#define LOG_ENCODE_FILE_ID_MASK     0xFFF00000
#define LOG_ENCODE_LINE_NUM_MASK    0x000FFF00
#define LOG_ENCODE_RESERVED_MASK    0x000000F0
#define LOG_ENCODE_LEVEL_MASK       0x0000000F

/**
 * 编码宏:将文件ID、行号、级别组合成32位整数
 */
#define LOG_ENCODE_PACK(file_id, line, level) \
    ((((U32)(file_id) & 0xFFF) << LOG_ENCODE_FILE_ID_SHIFT) | \
     (((U32)(line) & 0xFFF) << LOG_ENCODE_LINE_NUM_SHIFT) | \
     ((U32)(level) & 0xF))

/**
 * 解码宏:从32位整数中提取各字段
 */
#define LOG_DECODE_FILE_ID(encoded)  (((encoded) >> LOG_ENCODE_FILE_ID_SHIFT) & 0xFFF)
#define LOG_DECODE_LINE_NUM(encoded) (((encoded) >> LOG_ENCODE_LINE_NUM_SHIFT) & 0xFFF)
#define LOG_DECODE_LEVEL(encoded)    ((encoded) & 0xF)
```

#### 3.4.3 encode_mode核心函数

c

```c
// ww_log_encode.c

/**
 * encode_mode日志写入函数
 * 
 * @param level    日志级别
 * @param param1   可选参数1 (如错误码)
 * @param param2   可选参数2
 * 
 * 说明:
 * - 此函数会被日志宏调用
 * - 根据配置输出到UART和/或保存到RAM
 */
void log_encode_write(U8 level, U32 param1, U32 param2) {
    U32 encoded_info;
    
    // 动态级别过滤
    if (level > CONFIG_WW_LOG_LEVEL_DEFAULT) {
        return;  // 级别不够,直接返回
    }
    
    // 编码位置信息
    encoded_info = LOG_ENCODE_PACK(CURRENT_FILE_ID, __LINE__, level);
    
    #ifdef CONFIG_WW_LOG_OUTPUT_UART
    // 输出到UART (以十六进制格式,便于调试)
    uart_printf("LOG: %08X", encoded_info);
    if (param1 != 0) {
        uart_printf(" %08X", param1);
    }
    if (param2 != 0) {
        uart_printf(" %08X", param2);
    }
    uart_printf("\n");
    #endif
    
    #ifdef CONFIG_WW_LOG_OUTPUT_RAM
    // 保存到RAM缓冲区
    log_ram_write_entry(encoded_info, param1, param2);
    #endif
}

/**
 * 日志写入宏的实际实现
 * 这个宏会在各个日志宏中被调用
 */
#define LOG_ENCODE_WRITE(level, fmt, ...) \
    do { \
        /* 编译时级别检查 */ \
        if ((level) <= CONFIG_WW_LOG_LEVEL_DEFAULT) { \
            /* 提取可变参数 */ \
            /* 注意:这里简化处理,实际可能需要更复杂的参数提取 */ \
            log_encode_write((level), ##__VA_ARGS__, 0, 0); \
        } \
    } while(0)
```

#### 3.4.4 带参数的日志接口

为了支持在encode_mode下传递参数(如错误码),需要提供专门的接口:

c

```c
// ww_log.h

#ifdef CONFIG_WW_LOG_ENCODE_MODE

/**
 * 仅记录位置,不带参数
 */
#define LOG_ONLY() \
    log_encode_write(WW_LOG_LEVEL_INF, 0, 0)

/**
 * 记录位置+1个参数
 * 常用于记录错误码、返回值等
 */
#define LOG_WITH_U32(param1) \
    log_encode_write(WW_LOG_LEVEL_ERR, (U32)(param1), 0)

/**
 * 记录位置+2个参数  
 * 常用于记录地址+数据、配置参数等
 */
#define LOG_WITH_2U32(param1, param2) \
    log_encode_write(WW_LOG_LEVEL_ERR, (U32)(param1), (U32)(param2))

/**
 * 记录位置+数据块
 * 用于记录缓冲区内容
 * 注意:这个会占用多个日志条目
 */
#define LOG_WITH_DATA(ptr, len) \
    log_encode_write_data(WW_LOG_LEVEL_ERR, (U8*)(ptr), (len))

#endif
```

### 3.5 str_mode详细设计

#### 3.5.1 str_mode实现

c

```c
// ww_log_str.c

/**
 * str_mode日志输出函数
 * 
 * @param file     源文件名
 * @param line     行号
 * @param func     函数名
 * @param level    日志级别
 * @param fmt      格式化字符串
 * @param ...      可变参数
 */
void log_str_write(const char* file, int line, const char* func, 
                   U8 level, const char* fmt, ...) {
    char buf[128];
    va_list args;
    int len;
    
    // 动态级别过滤
    if (level > CONFIG_WW_LOG_LEVEL_DEFAULT) {
        return;
    }
    
    // 格式化用户消息
    va_start(args, fmt);
    len = vsnprintf(buf, sizeof(buf), fmt, args);
    va_end(args);
    
    // 输出到UART
    #ifdef CONFIG_WW_LOG_OUTPUT_UART
    uart_printf("[%s] %s:%d:%s: %s\n", 
                g_log_level_str[level], file, line, func, buf);
    #endif
    
    // str_mode通常不保存到RAM,因为占用空间太大
    // 如果确实需要,可以保存格式化后的字符串
}

/**
 * 日志写入宏的实际实现
 */
#define LOG_STR_WRITE(level, fmt, ...) \
    do { \
        if ((level) <= CONFIG_WW_LOG_LEVEL_DEFAULT) { \
            log_str_write(__FILE__, __LINE__, __FUNCTION__, \
                         (level), fmt, ##__VA_ARGS__); \
        } \
    } while(0)
```

### 3.6 RAM缓冲区管理

#### 3.6.1 数据结构定义

c

```c
// ww_log_ram.h

/**
 * 单条日志条目结构
 * 说明:
 * - encode_mode下,每条日志可能包含1-3个U32数据
 * - entry[0]: 编码的位置信息(文件ID+行号+级别)
 * - entry[1]: 可选参数1
 * - entry[2]: 可选参数2
 */
typedef struct {
    U32 entry[3];       // 最多3个U32数据
    U8  entry_count;    // 实际有效的entry数量(1-3)
    U8  read_flag;      // 读取标志: 0=未读, 1=已读
    U16 reserved;       // 保留,用于对齐
} LOG_ENTRY_T;

/**
 * RAM日志缓冲区管理结构
 * 说明:
 * - 使用环形缓冲区管理
 * - 支持热重启保留(通过特殊链接脚本段配置)
 */
typedef struct {
    U32 magic_head;                              // 魔数头,用于校验(0x4C4F4748='LOGH')
    U16 entry_head;                              // 读指针(最老的日志位置)
    U16 entry_tail;                              // 写指针(下一条日志写入位置)
    U32 write_count;                             // 累计写入计数(用于生成序列号)
    U32 read_count;                              // 累计读取计数
    U32 overflow_count;                          // 溢出计数(缓冲区满导致的丢弃)
    LOG_ENTRY_T entries[CONFIG_WW_LOG_RAM_ENTRY_NUM];  // 日志条目数组
    U32 magic_tail;                              // 魔数尾,用于校验(0x4C4F4754='LOGT')
} WW_LOG_RAM_T;

/**
 * 全局日志缓冲区
 * 说明:
 * - 使用__attribute__((section(".noinit")))放到特殊段,热重启不清零
 * - 冷启动时需要检查magic数来判断是否有效
 */
#ifdef CONFIG_WW_LOG_RAM_PERSISTENT
__attribute__((section(".noinit"))) WW_LOG_RAM_T g_log_ram;
#else
WW_LOG_RAM_T g_log_ram;
#endif
```

#### 3.6.2 缓冲区初始化

c

```c
// ww_log_ram.c

/**
 * 日志缓冲区初始化
 * 
 * @param force_clear  是否强制清空: 1=清空, 0=尝试保留
 * 
 * 说明:
 * - 系统初始化时调用
 * - 如果检测到有效的魔数且force_clear=0,则保留现有日志
 * - 否则清空缓冲区
 */
void log_ram_init(U8 force_clear) {
    U8 valid = 0;
    
    #ifdef CONFIG_WW_LOG_RAM_PERSISTENT
    // 检查魔数是否有效
    if (g_log_ram.magic_head == 0x4C4F4748 && 
        g_log_ram.magic_tail == 0x4C4F4754 &&
        !force_clear) {
        // 魔数有效,且不强制清空,保留现有日志
        valid = 1;
    }
    #endif
    
    if (!valid) {
        // 清空缓冲区
        memset(&g_log_ram, 0, sizeof(g_log_ram));
        g_log_ram.magic_head = 0x4C4F4748;
        g_log_ram.magic_tail = 0x4C4F4754;
        g_log_ram.entry_head = 0;
        g_log_ram.entry_tail = 0;
    }
}

/**
 * 检查缓冲区是否为空
 */
static inline U8 log_ram_is_empty(void) {
    return (g_log_ram.entry_head == g_log_ram.entry_tail);
}

/**
 * 检查缓冲区是否已满
 */
static inline U8 log_ram_is_full(void) {
    U16 next_tail = (g_log_ram.entry_tail + 1) % CONFIG_WW_LOG_RAM_ENTRY_NUM;
    return (next_tail == g_log_ram.entry_head);
}

/**
 * 获取缓冲区中的日志条数
 */
U16 log_ram_get_count(void) {
    if (g_log_ram.entry_tail >= g_log_ram.entry_head) {
        return g_log_ram.entry_tail - g_log_ram.entry_head;
    } else {
        return CONFIG_WW_LOG_RAM_ENTRY_NUM - g_log_ram.entry_head + g_log_ram.entry_tail;
    }
}
```

#### 3.6.3 日志写入操作

c

```c
// ww_log_ram.c

/**
 * 向RAM缓冲区写入一条日志
 * 
 * @param entry0   编码的位置信息(必需)
 * @param entry1   参数1(可选,0表示无效)
 * @param entry2   参数2(可选,0表示无效)
 * 
 * @return 0=成功, -1=失败
 * 
 * 说明:
 * - 此函数需要临界区保护
 * - 如果缓冲区满,根据策略处理(覆盖或丢弃)
 */
int log_ram_write_entry(U32 entry0, U32 entry1, U32 entry2) {
    U16 next_tail;
    LOG_ENTRY_T *p_entry;
    U8 entry_count = 1;
    
    // 计算有效entry数量
    if (entry1 != 0) entry_count = 2;
    if (entry2 != 0) entry_count = 3;
    
    // 临界区保护开始
    ENTER_CRITICAL_SECTION();
    
    // 检查是否满
    if (log_ram_is_full()) {
        // 获取级别,判断是否为ERROR
        U8 level = LOG_DECODE_LEVEL(entry0);
        
        if (level == WW_LOG_LEVEL_ERR) {
            // ERROR级别日志,检查最老的日志是否已读
            if (g_log_ram.entries[g_log_ram.entry_head].read_flag == 0) {
                // 未读,不能覆盖,记录溢出
                g_log_ram.overflow_count++;
                EXIT_CRITICAL_SECTION();
                return -1;
            }
        }
        
        // 非ERROR或已读,可以覆盖,head前移
        g_log_ram.entry_head = (g_log_ram.entry_head + 1) % CONFIG_WW_LOG_RAM_ENTRY_NUM;
        g_log_ram.overflow_count++;
    }
    
    // 写入日志到tail位置
    p_entry = &g_log_ram.entries[g_log_ram.entry_tail];
    p_entry->entry[0] = entry0;
    p_entry->entry[1] = entry1;
    p_entry->entry[2] = entry2;
    p_entry->entry_count = entry_count;
    p_entry->read_flag = 0;  // 标记为未读
    
    // 更新tail指针
    next_tail = (g_log_ram.entry_tail + 1) % CONFIG_WW_LOG_RAM_ENTRY_NUM;
    g_log_ram.entry_tail = next_tail;
    
    // 更新写入计数
    g_log_ram.write_count++;
    
    // 临界区保护结束
    EXIT_CRITICAL_SECTION();
    
    return 0;
}
```

#### 3.6.4 日志读取操作

c

```c
// ww_log_ram.c

/**
 * 从RAM缓冲区读取一条日志
 * 
 * @param p_entry  输出参数,保存读取的日志条目
 * 
 * @return 0=成功, -1=缓冲区为空
 * 
 * 说明:
 * - 读取后不删除,只标记为已读
 * - 工具可以多次读取同一条日志
 */
int log_ram_read_entry(LOG_ENTRY_T *p_entry) {
    LOG_ENTRY_T *p_src;
    
    if (p_entry == NULL) {
        return -1;
    }
    
    ENTER_CRITICAL_SECTION();
    
    // 检查是否为空
    if (log_ram_is_empty()) {
        EXIT_CRITICAL_SECTION();
        return -1;
    }
    
    // 从head位置读取
    p_src = &g_log_ram.entries[g_log_ram.entry_head];
    
    // 复制数据
    memcpy(p_entry, p_src, sizeof(LOG_ENTRY_T));
    
    // 标记为已读
    p_src->read_flag = 1;
    
    // head指针前移
    g_log_ram.entry_head = (g_log_ram.entry_head + 1) % CONFIG_WW_LOG_RAM_ENTRY_NUM;
    
    // 更新读取计数
    g_log_ram.read_count++;
    
    EXIT_CRITICAL_SECTION();
    
    return 0;
}

/**
 * 清空RAM缓冲区
 * 
 * 说明:
 * - 仅清空日志数据,保留统计信息
 */
void log_ram_clear(void) {
    ENTER_CRITICAL_SECTION();
    
    g_log_ram.entry_head = 0;
    g_log_ram.entry_tail = 0;
    
    // 可选:清空所有条目的read_flag
    for (int i = 0; i < CONFIG_WW_LOG_RAM_ENTRY_NUM; i++) {
        g_log_ram.entries[i].read_flag = 0;
    }
    
    EXIT_CRITICAL_SECTION();
}
```

### 3.7 临界区保护实现

c

```c
// ww_log_critical.h

/**
 * 临界区保护的实现方式
 * 
 * 根据系统环境选择合适的保护方式:
 * 1. 裸机系统:使用关中断
 * 2. RTOS系统:使用互斥锁或关调度器
 */

#ifdef USE_RTOS
    // RTOS环境:使用互斥锁
    #include "cmsis_os.h"
    
    extern osMutexId_t g_log_mutex;
    
    #define ENTER_CRITICAL_SECTION()  osMutexAcquire(g_log_mutex, osWaitForever)
    #define EXIT_CRITICAL_SECTION()   osMutexRelease(g_log_mutex)
    
    // 初始化互斥锁
    #define INIT_CRITICAL_SECTION() \
        do { \
            g_log_mutex = osMutexNew(NULL); \
        } while(0)

#else
    // 裸机环境:使用关中断
    #define ENTER_CRITICAL_SECTION() \
        do { \
            __disable_irq(); \
        } while(0)
    
    #define EXIT_CRITICAL_SECTION() \
        do { \
            __enable_irq(); \
        } while(0)
    
    #define INIT_CRITICAL_SECTION()  // 裸机无需初始化
#endif

/**
 * 注意事项:
 * 1. 临界区代码应尽可能短,避免长时间关中断
 * 2. 在中断中不能使用互斥锁,只能关中断
 * 3. 如果在中断中需要写日志,建议使用单独的缓冲区或延迟写入机制
 */
```

### 3.8 RSDK接口设计

c

```c
// ww_log_api.h

/**
 * RSDK日志读取接口
 * 
 * 说明:
 * - 这些接口供外部工具(如RSDK)通过串口或其他方式调用
 * - 可以通过命令行方式实现,也可以通过二进制协议实现
 */

/**
 * 获取RAM缓冲区状态
 * 
 * @param p_info  输出参数,保存缓冲区信息
 */
typedef struct {
    U16 total_count;        // 缓冲区总容量
    U16 used_count;         // 当前使用的条目数
    U32 write_count;        // 累计写入次数
    U32 read_count;         // 累计读取次数
    U32 overflow_count;     // 溢出次数
} LOG_RAM_INFO_T;

void log_api_get_ram_info(LOG_RAM_INFO_T *p_info);

/**
 * 批量读取日志
 * 
 * @param buffer      输出缓冲区
 * @param max_count   最多读取的条目数
 * 
 * @return 实际读取的条目数
 * 
 * 说明:
 * - 读取后日志不会被删除,只是标记为已读
 * - 工具可以多次读取
 */
int log_api_read_entries(LOG_ENTRY_T *buffer, int max_count);

/**
 * 清空RAM缓冲区
 */
void log_api_clear_ram(void);

/**
 * 命令行接口示例
 * 
 * 工具可以通过串口发送命令:
 * - "log info"         : 获取缓冲区信息
 * - "log read <n>"     : 读取n条日志
 * - "log clear"        : 清空缓冲区
 * - "log level <n>"    : 动态设置日志级别
 */
void log_api_cmd_handler(const char *cmd);
```

c

```c
// ww_log_api.c

void log_api_get_ram_info(LOG_RAM_INFO_T *p_info) {
    if (p_info == NULL) return;
    
    ENTER_CRITICAL_SECTION();
    
    p_info->total_count = CONFIG_WW_LOG_RAM_ENTRY_NUM;
    p_info->used_count = log_ram_get_count();
    p_info->write_count = g_log_ram.write_count;
    p_info->read_count = g_log_ram.read_count;
    p_info->overflow_count = g_log_ram.overflow_count;
    
    EXIT_CRITICAL_SECTION();
}

int log_api_read_entries(LOG_ENTRY_T *buffer, int max_count) {
    int count = 0;
    
    if (buffer == NULL || max_count <= 0) {
        return 0;
    }
    
    while (count < max_count) {
        if (log_ram_read_entry(&buffer[count]) != 0) {
            break;  // 缓冲区已空
        }
        count++;
    }
    
    return count;
}

void log_api_clear_ram(void) {
    log_ram_clear();
}

/**
 * 简单的命令行解析实现
 */
void log_api_cmd_handler(const char *cmd) {
    if (strncmp(cmd, "log info", 8) == 0) {
        LOG_RAM_INFO_T info;
        log_api_get_ram_info(&info);
        uart_printf("Total: %d, Used: %d, Write: %u, Read: %u, Overflow: %u\n",
                   info.total_count, info.used_count, info.write_count,
                   info.read_count, info.overflow_count);
    }
    else if (strncmp(cmd, "log read", 8) == 0) {
        int n = atoi(cmd + 9);  // 提取数字
        LOG_ENTRY_T entries[10];
        int count = log_api_read_entries(entries, n < 10 ? n : 10);
        
        for (int i = 0; i < count; i++) {
            uart_printf("Entry %d: ", i);
            for (int j = 0; j < entries[i].entry_count; j++) {
                uart_printf("%08X ", entries[i].entry[j]);
            }
            uart_printf("\n");
        }
    }
    else if (strncmp(cmd, "log clear", 9) == 0) {
        log_api_clear_ram();
        uart_printf("Log cleared\n");
    }
    else if (strncmp(cmd, "log level", 9) == 0) {
        int level = atoi(cmd + 10);
        if (level >= 0 && level <= 4) {
            // 动态修改日志级别
            extern U8 g_log_level_runtime;
            g_log_level_runtime = level;
            uart_printf("Log level set to %d\n", level);
        }
    }
}
```

### 3.9 外部存储支持(可选功能)

c

```c
// ww_log_storage.h

/**
 * 外部存储配置
 * 
 * 说明:
 * - 外部存储用于长期保存关键日志
 * - 支持EEPROM或Flash
 * - 需要考虑擦写次数限制
 */

#ifdef CONFIG_WW_LOG_OUTPUT_FLASH

// 外存存储区域配置
#define LOG_STORAGE_BASE_ADDR    0x08040000  // Flash起始地址
#define LOG_STORAGE_SIZE         (32*1024)   // 32KB
#define LOG_STORAGE_SECTOR_SIZE  4096        // 扇区大小

/**
 * 外存日志结构
 * 说明:
 * - 采用类似FAT的管理方式
 * - 每个扇区保存一定数量的日志条目
 * - 维护一个分配表
 */
typedef struct {
    U32 magic;              // 魔数(0x4C4F4753='LOGS')
    U16 sector_count;       // 总扇区数
    U16 used_sectors;       // 已使用扇区数
    U32 total_entries;      // 总日志条目数
    U16 alloc_bitmap[64];   // 扇区分配位图(每bit表示一个扇区)
} LOG_STORAGE_HDR_T;

/**
 * 初始化外部存储
 */
int log_storage_init(void);

/**
 * 写入日志到外部存储
 * 
 * @param p_entry  要保存的日志条目
 * 
 * @return 0=成功, <0=失败
 * 
 * 说明:
 * - 通常在关键ERROR时调用
 * - 或者定期将RAM中的日志刷新到外存
 */
int log_storage_write(const LOG_ENTRY_T *p_entry);

/**
 * 从外部存储读取日志
 * 
 * @param buffer     输出缓冲区
 * @param offset     起始偏移(条目索引)
 * @param max_count  最多读取的条目数
 * 
 * @return 实际读取的条目数
 */
int log_storage_read(LOG_ENTRY_T *buffer, U32 offset, int max_count);

/**
 * 擦除外部存储的日志
 * 
 * 说明:
 * - 谨慎使用,会丢失所有历史日志
 */
int log_storage_erase(void);

#endif // CONFIG_WW_LOG_OUTPUT_FLASH
```

## 4. 日志解析工具设计

### 4.1 工具功能需求

日志解析工具是整个日志系统的重要组成部分,主要功能包括:

1. **编码日志解析**
   - 将32位编码还原为文件名、行号、级别
   - 支持批量解析
   - 生成可读的文本日志

1. **日志读取**
   - 通过串口从设备读取RAM中的日志
   - 支持实时监控模式
   - 支持历史日志导出

1. **映射表生成**
   - 从源代码自动生成文件ID到文件名的映射
   - 可选:生成行号到代码内容的映射

1. **日志分析**
   - 统计各级别日志数量
   - 按模块分类统计
   - 时间序列分析(如果日志包含时间戳)

### 4.2 映射表生成方案

映射表是解析工具的核心数据,需要在编译时生成。

#### 4.2.1 方法一:Python脚本扫描源代码

python

```python
# gen_log_map.py
"""
扫描log_file_id.h生成文件ID映射表
"""

import re
import json

def parse_file_id_enum(header_file):
    """
    解析log_file_id.h中的枚举定义
    
    返回字典: {file_id: file_name}
    """
    file_map = {}
    
    with open(header_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取枚举定义
    enum_pattern = r'typedef\s+enum\s*\{(.*?)\}\s*LOG_FILE_ID_E'
    match = re.search(enum_pattern, content, re.DOTALL)
    
    if not match:
        print("Error: Cannot find LOG_FILE_ID_E enum")
        return file_map
    
    enum_body = match.group(1)
    
    # 解析每一行
    lines = enum_body.split('\n')
    current_id = 0
    
    for line in lines:
        line = line.strip()
        
        # 跳过注释和空行
        if not line or line.startswith('/*') or line.startswith('//'):
            continue
        
        # 移除行尾注释
        if '//' in line:
            line = line[:line.index('//')]
        
        # 解析枚举项
        # 格式: FILE_ID_XXXX = 值, 或 FILE_ID_XXXX,
        match = re.match(r'FILE_ID_(\w+)\s*(?:=\s*(\d+))?\s*,?', line)
        if match:
            name = match.group(1)
            value = match.group(2)
            
            if name in ['INVALID', 'MAX']:
                continue
            
            if value:
                current_id = int(value)
            
            file_map[current_id] = name.lower()
            current_id += 1
    
    return file_map

def generate_json_map(file_map, output_file):
    """
    生成JSON格式的映射表
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(file_map, f, indent=4)
    
    print(f"Generated {output_file} with {len(file_map)} entries")

def generate_c_array(file_map, output_file):
    """
    生成C语言数组格式的映射表(可选)
    供嵌入式设备使用
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("// Auto-generated file, do not edit\n\n")
        f.write("#include \"log_file_id.h\"\n\n")
        f.write("const char* g_log_file_name_map[] = {\n")
        
        max_id = max(file_map.keys()) if file_map else 0
        for i in range(max_id + 1):
            if i in file_map:
                f.write(f'    "{file_map[i]}.c",\n')
            else:
                f.write('    "unknown",\n')
        
        f.write("};\n")
    
    print(f"Generated {output_file}")

if __name__ == "__main__":
    # 解析头文件
    file_map = parse_file_id_enum("../../inc/log_file_id.h")
    
    # 生成JSON映射表(供Python工具使用)
    generate_json_map(file_map, "log_file_map.json")
    
    # 生成C数组(可选,供嵌入式设备使用)
    generate_c_array(file_map, "log_file_map.c")
```

#### 4.2.2 方法二:编译时生成

在Makefile中添加规则,编译前自动生成映射表:

makefile

```makefile
# Makefile片段

LOG_MAP_SCRIPT := tools/gen_log_map.py
LOG_FILE_ID_H := inc/log_file_id.h
LOG_MAP_JSON := tools/log_file_map.json

# 生成日志映射表
$(LOG_MAP_JSON): $(LOG_FILE_ID_H) $(LOG_MAP_SCRIPT)
	@echo "Generating log file map..."
	@python3 $(LOG_MAP_SCRIPT)

# 确保编译前生成映射表
all: $(LOG_MAP_JSON)
	@echo "Building project..."
	# ... 编译命令
```

### 4.3 日志解析工具实现

python

```python
# log_parser.py
"""
日志解析工具
功能:
1. 解析编码的日志数据
2. 从设备读取日志
3. 生成可读的日志文件
"""

import serial
import json
import struct
import argparse
from datetime import datetime

class LogParser:
    """日志解析器"""
    
    # 日志级别映射
    LEVEL_MAP = {
        0: "OFF",
        1: "ERR",
        2: "WRN",
        3: "INF",
        4: "DBG"
    }
    
    def __init__(self, map_file):
        """
        初始化解析器
        
        Args:
            map_file: 文件ID映射表JSON文件路径
        """
        with open(map_file, 'r') as f:
            self.file_map = json.load(f)
        
        # 将key转换为整数
        self.file_map = {int(k): v for k, v in self.file_map.items()}
    
    def decode_entry(self, encoded):
        """
        解码单个日志条目
        
        Args:
            encoded: 32位编码值
            
        Returns:
            字典: {file_id, file_name, line, level}
        """
        # 提取各字段
        file_id = (encoded >> 20) & 0xFFF
        line = (encoded >> 8) & 0xFFF
        level = encoded & 0xF
        
        # 查找文件名
        file_name = self.file_map.get(file_id, f"unknown_{file_id}")
        
        return {
            'file_id': file_id,
            'file_name': file_name,
            'line': line,
            'level': level,
            'level_str': self.LEVEL_MAP.get(level, "UNK")
        }
    
    def format_log(self, decoded, params=None):
        """
        格式化日志输出
        
        Args:
            decoded: 解码后的字典
            params: 可选参数列表
            
        Returns:
            格式化的字符串
        """
        output = f"[{decoded['level_str']}] {decoded['file_name']}.c:{decoded['line']}"
        
        if params:
            param_str = ' '.join([f'0x{p:08X}' for p in params])
            output += f" | Params: {param_str}"
        
        return output
    
    def parse_file(self, input_file, output_file):
        """
        解析日志文件
        
        Args:
            input_file: 输入的二进制日志文件
            output_file: 输出的文本日志文件
        """
        with open(input_file, 'rb') as fin, \
             open(output_file, 'w', encoding='utf-8') as fout:
            
            # 写入文件头
            fout.write(f"Log parsed at {datetime.now()}\n")
            fout.write("=" * 80 + "\n\n")
            
            entry_count = 0
            
            while True:
                # 读取一个条目(假设格式: U32 encoded + U8 param_count + params)
                data = fin.read(5)  # 4字节encoded + 1字节param_count
                if len(data) < 5:
                    break
                
                encoded, param_count = struct.unpack('<IB', data)
                
                # 读取参数
                params = []
                if param_count > 0:
                    param_data = fin.read(param_count * 4)
                    params = list(struct.unpack(f'<{param_count}I', param_data))
                
                # 解码并格式化
                decoded = self.decode_entry(encoded)
                log_line = self.format_log(decoded, params)
                
                fout.write(f"{entry_count:04d}: {log_line}\n")
                entry_count += 1
            
            fout.write("\n" + "=" * 80 + "\n")
            fout.write(f"Total entries: {entry_count}\n")
        
        print(f"Parsed {entry_count} log entries")
        print(f"Output: {output_file}")

class SerialLogReader:
    """通过串口读取设备日志"""
    
    def __init__(self, port, baudrate=115200):
        """
        初始化串口连接
        
        Args:
            port: 串口名称(如'COM3'或'/dev/ttyUSB0')
            baudrate: 波特率
        """
        self.ser = serial.Serial(port, baudrate, timeout=1)
    
    def send_command(self, cmd):
        """
        发送命令到设备
        
        Args:
            cmd: 命令字符串
        """
        self.ser.write((cmd + '\n').encode())
    
    def read_logs(self, count):
        """
        读取指定数量的日志
        
        Args:
            count: 要读取的日志条数
            
        Returns:
            日志数据列表
        """
        logs = []
        
        # 发送读取命令
        self.send_command(f"log read {count}")
        
        # 读取响应
        for _ in range(count):
            line = self.ser.readline().decode().strip()
            if not line or not line.startswith("Entry"):
                break
            
            # 解析十六进制数据
            # 格式: "Entry 0: 00200F03 12345678"
            parts = line.split(':')
            if len(parts) >= 2:
                hex_values = parts[1].strip().split()
                entry = [int(h, 16) for h in hex_values]
                logs.append(entry)
        
        return logs
    
    def monitor_realtime(self, parser, duration=60):
        """
        实时监控模式
        
        Args:
            parser: LogParser实例
            duration: 监控时长(秒),0表示持续监控
        """
        print("Starting real-time log monitor...")
        print("Press Ctrl+C to stop")
        
        start_time = datetime.now()
        
        try:
            while True:
                line = self.ser.readline().decode().strip()
                
                # 检查是否是日志输出
                if line.startswith("LOG:"):
                    # 格式: "LOG: 00200F03"
                    hex_str = line[5:].strip().split()[0]
                    encoded = int(hex_str, 16)
                    
                    decoded = parser.decode_entry(encoded)
                    log_str = parser.format_log(decoded)
                    
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    print(f"[{timestamp}] {log_str}")
                
                # 检查是否超时
                if duration > 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    if elapsed >= duration:
                        break
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
    
    def close(self):
        """关闭串口"""
        self.ser.close()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Log Parser Tool')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # 解析文件命令
    parse_cmd = subparsers.add_parser('parse', help='Parse log file')
    parse_cmd.add_argument('input', help='Input binary log file')
    parse_cmd.add_argument('output', help='Output text log file')
    parse_cmd.add_argument('-m', '--map', default='log_file_map.json',
                          help='File ID map JSON')
    
    # 从设备读取命令
    read_cmd = subparsers.add_parser('read', help='Read logs from device')
    read_cmd.add_argument('port', help='Serial port (e.g., COM3 or /dev/ttyUSB0)')
    read_cmd.add_argument('-b', '--baudrate', type=int, default=115200,
                         help='Baud rate')
    read_cmd.add_argument('-n', '--count', type=int, default=10,
                         help='Number of logs to read')
    read_cmd.add_argument('-m', '--map', default='log_file_map.json',
                         help='File ID map JSON')
    read_cmd.add_argument('-o', '--output', help='Output file (optional)')
    
    # 实时监控命令
    monitor_cmd = subparsers.add_parser('monitor', help='Real-time log monitoring')
    monitor_cmd.add_argument('port', help='Serial port')
    monitor_cmd.add_argument('-b', '--baudrate', type=int, default=115200,
                            help='Baud rate')
    monitor_cmd.add_argument('-d', '--duration', type=int, default=0,
                            help='Monitor duration in seconds (0 = infinite)')
    monitor_cmd.add_argument('-m', '--map', default='log_file_map.json',
                            help='File ID map JSON')
    
    args = parser.parse_args()
    
    if args.command == 'parse':
        # 解析日志文件
        log_parser = LogParser(args.map)
        log_parser.parse_file(args.input, args.output)
    
    elif args.command == 'read':
        # 从设备读取日志
        log_parser = LogParser(args.map)
        reader = SerialLogReader(args.port, args.baudrate)
        
        logs = reader.read_logs(args.count)
        
        # 输出到终端或文件
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"Logs read at {datetime.now()}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, entry in enumerate(logs):
                    decoded = log_parser.decode_entry(entry[0])
                    params = entry[1:] if len(entry) > 1 else None
                    log_str = log_parser.format_log(decoded, params)
                    f.write(f"{i:04d}: {log_str}\n")
            
            print(f"Saved {len(logs)} logs to {args.output}")
        else:
            for i, entry in enumerate(logs):
                decoded = log_parser.decode_entry(entry[0])
                params = entry[1:] if len(entry) > 1 else None
                log_str = log_parser.format_log(decoded, params)
                print(f"{i:04d}: {log_str}")
        
        reader.close()
    
    elif args.command == 'monitor':
        # 实时监控
        log_parser = LogParser(args.map)
        reader = SerialLogReader(args.port, args.baudrate)
        reader.monitor_realtime(log_parser, args.duration)
        reader.close()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

### 4.4 工具使用示例

bash

```bash
# 1. 生成文件ID映射表
python3 tools/gen_log_map.py

# 2. 解析二进制日志文件
python3 tools/log_parser.py parse logs.bin logs.txt

# 3. 从设备读取日志(通过串口)
python3 tools/log_parser.py read COM3 -n 50 -o device_logs.txt

# 4. 实时监控日志
python3 tools/log_parser.py monitor /dev/ttyUSB0 -d 300

# 5. 使用自定义波特率
python3 tools/log_parser.py monitor COM3 -b 921600
```

## 5. 动态/静态开关实现

### 5.1 静态开关(编译时)

静态开关通过宏定义实现,在编译时决定某段代码是否包含。

c

```c
// ww_log_config.h

// ============ 全局日志开关 ============
#define CONFIG_WW_LOG_ENABLE  1  // 1=启用日志, 0=完全禁用

// ============ 子模块静态开关 ============
#define CONFIG_WW_LOG_MOD_INIT_EN      // 定义则启用
#define CONFIG_WW_LOG_MOD_SENSOR_EN    // 定义则启用
// #undef CONFIG_WW_LOG_MOD_MOTOR_EN   // 不定义则禁用
```

使用示例:

c

```c
// 在ww_log.h中

#if CONFIG_WW_LOG_ENABLE
    // 日志功能启用
    #ifdef CONFIG_WW_LOG_MOD_INIT_EN
        #define WW_INIT_LOG_ERR(fmt, ...)  TEST_LOG_ERR_MSG(fmt, ##__VA_ARGS__)
    #else
        #define WW_INIT_LOG_ERR(fmt, ...)  // 空实现,编译后无任何代码
    #endif
#else
    // 日志功能完全禁用,所有宏都为空
    #define WW_INIT_LOG_ERR(fmt, ...)
    #define TEST_LOG_ERR_MSG(fmt, ...)
    // ...
#endif
```

**静态开关的优势:**

- 编译后完全不占用代码空间
- 无运行时开销
- 适合长期不需要的日志

**静态开关的劣势:**

- 需要重新编译才能改变
- 不够灵活

### 5.2 动态开关(运行时)

动态开关通过运行时变量实现,可以在系统运行过程中改变日志行为。

#### 5.2.1 全局日志级别控制

c

```c
// ww_log.c

/**
 * 运行时日志级别
 * 说明:
 * - 初始值为配置的默认级别
 * - 可通过API或命令动态修改
 * - 优先级高于编译时配置
 */
volatile U8 g_log_level_runtime = CONFIG_WW_LOG_LEVEL_DEFAULT;

/**
 * 设置运行时日志级别
 * 
 * @param level  新的日志级别(0-4)
 * 
 * @return 0=成功, -1=参数错误
 */
int log_set_level(U8 level) {
    if (level > WW_LOG_LEVEL_DBG) {
        return -1;
    }
    
    g_log_level_runtime = level;
    return 0;
}

/**
 * 获取当前日志级别
 */
U8 log_get_level(void) {
    return g_log_level_runtime;
}
```

在日志宏中检查运行时级别:

c

```c
// ww_log_encode.c

void log_encode_write(U8 level, U32 param1, U32 param2) {
    // 运行时级别过滤
    if (level > g_log_level_runtime) {
        return;  // 级别不够,直接返回
    }
    
    // 后续处理...
}
```

#### 5.2.2 按模块控制

更细粒度的控制可以为每个模块单独设置级别:

c

```c
// ww_log_config.h

/**
 * 模块ID定义
 */
typedef enum {
    LOG_MOD_INIT = 0,
    LOG_MOD_SENSOR,
    LOG_MOD_MOTOR,
    LOG_MOD_COMM,
    LOG_MOD_MAX
} LOG_MODULE_E;

// ww_log.c

/**
 * 每个模块的日志级别
 * 说明:
 * - 数组索引对应LOG_MODULE_E
 * - 值为日志级别(0-4)
 * - 0xFF表示禁用该模块日志
 */
U8 g_log_module_level[LOG_MOD_MAX] = {
    WW_LOG_LEVEL_ERR,  // INIT模块
    WW_LOG_LEVEL_WRN,  // SENSOR模块
    WW_LOG_LEVEL_INF,  // MOTOR模块
    WW_LOG_LEVEL_DBG,  // COMM模块
};

/**
 * 设置指定模块的日志级别
 */
int log_set_module_level(LOG_MODULE_E module, U8 level) {
    if (module >= LOG_MOD_MAX || level > WW_LOG_LEVEL_DBG) {
        return -1;
    }
    
    g_log_module_level[module] = level;
    return 0;
}
```

带模块ID的日志宏:

c

```c
// ww_log.h

#define WW_INIT_LOG_ERR(fmt, ...) \
    LOG_WITH_MODULE(LOG_MOD_INIT, WW_LOG_LEVEL_ERR, fmt, ##__VA_ARGS__)

#define LOG_WITH_MODULE(mod, level, fmt, ...) \
    do { \
        extern U8 g_log_module_level[]; \
        if ((level) <= g_log_module_level[mod]) { \
            log_encode_write((level), ##__VA_ARGS__); \
        } \
    } while(0)
```

#### 5.2.3 通过命令行动态调整

c

```c
// 在log_api.c中添加命令处理

void log_api_cmd_handler(const char *cmd) {
    // ... 之前的命令处理
    
    // 动态调整全局级别
    // 命令: "log level 3"
    else if (strncmp(cmd, "log level", 9) == 0) {
        int level = atoi(cmd + 10);
        if (log_set_level(level) == 0) {
            uart_printf("Global log level set to %d\n", level);
        } else {
            uart_printf("Invalid level\n");
        }
    }
    
    // 动态调整模块级别  
    // 命令: "log modlevel 1 2"  (模块1设为级别2)
    else if (strncmp(cmd, "log modlevel", 12) == 0) {
        int mod, level;
        if (sscanf(cmd + 13, "%d %d", &mod, &level) == 2) {
            if (log_set_module_level(mod, level) == 0) {
                uart_printf("Module %d log level set to %d\n", mod, level);
            } else {
                uart_printf("Invalid module or level\n");
            }
        }
    }
}
```

### 5.3 静态开关与动态开关的结合

实际项目中通常结合使用:

```
静态开关(编译时) --> 决定代码是否存在
                ↓
            (存在)
                ↓
动态开关(运行时) --> 决定是否执行
```

示例:

c

```c
// 某个模块的日志宏

#ifdef CONFIG_WW_LOG_MOD_SENSOR_EN  // 静态开关:编译时决定
    #define WW_SENSOR_LOG_ERR(fmt, ...) \
        do { \
            /* 动态开关:运行时检查 */ \
            extern U8 g_log_module_level[]; \
            if (WW_LOG_LEVEL_ERR <= g_log_module_level[LOG_MOD_SENSOR]) { \
                log_encode_write(WW_LOG_LEVEL_ERR, ##__VA_ARGS__); \
            } \
        } while(0)
#else  // 静态禁用,宏为空
    #define WW_SENSOR_LOG_ERR(fmt, ...)
#endif
```

这样的设计:

1. 如果编译时禁用(`#undef CONFIG_WW_LOG_MOD_SENSOR_EN`),则完全没有代码生成
2. 如果编译时启用,运行时还可以通过级别控制是否实际输出

## 6. 断言和Panic支持

### 6.1 断言宏设计

断言用于检查不应该发生的错误条件,在调试阶段非常有用。

c

```c
// ww_log.h

/**
 * 断言宏
 * 
 * @param condition  断言条件,为假时触发
 * @param fmt        格式化字符串
 * @param ...        可变参数
 * 
 * 说明:
 * - 断言失败时先记录日志,然后触发调试断点
 * - Release版本可以通过宏关闭断言检查
 */
#ifdef CONFIG_WW_LOG_ASSERT_ENABLE
    #define WW_ASSERT(condition, fmt, ...) \
        do { \
            if (!(condition)) { \
                TEST_LOG_ERR_MSG("ASSERT FAILED: " fmt, ##__VA_ARGS__); \
                /* 触发调试断点 */ \
                __asm__ volatile("bkpt #0"); /* ARM Cortex */ \
                /* 或者调用系统重启 */ \
                /* NVIC_SystemReset(); */ \
            } \
        } while(0)
#else
    // Release版本:断言为空
    #define WW_ASSERT(condition, fmt, ...)
#endif

/**
 * 简化的断言宏(不带消息)
 */
#define WW_ASSERT_SIMPLE(condition) \
    WW_ASSERT(condition, "Condition: " #condition)

/**
 * Panic宏
 * 说明:
 * - 用于不可恢复的错误
 * - 记录错误后立即重启系统
 */
#define WW_PANIC(fmt, ...) \
    do { \
        TEST_LOG_ERR_MSG("PANIC: " fmt, ##__VA_ARGS__); \
        /* 延时确保日志输出完成 */ \
        for (volatile int i = 0; i < 100000; i++); \
        /* 系统重启 */ \
        NVIC_SystemReset(); \
    } while(0)
```

使用示例:

c

```c
// sensor_driver.c

int sensor_init(void) {
    int ret;
    
    // 检查指针有效性
    WW_ASSERT(g_sensor_config != NULL, "Sensor config is NULL");
    
    // 检查返回值
    ret = i2c_init();
    WW_ASSERT(ret == 0, "I2C init failed, ret=%d", ret);
    
    // 检查寄存器值
    U8 chip_id = sensor_read_reg(REG_CHIP_ID);
    WW_ASSERT_SIMPLE(chip_id == EXPECTED_CHIP_ID);
    
    return 0;
}

void critical_error_handler(int error_code) {
    // 不可恢复的错误,触发panic
    WW_PANIC("Critical error: code=%d", error_code);
    // 不会执行到这里
}
```

## 7. 链接脚本配置(热重启保留)

为了实现热重启后保留RAM中的日志,需要修改链接脚本。

### 7.1 链接脚本示例

ld

```ld
/* linker_script.ld */

MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 256K
    RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 64K
    NOINIT (rw) : ORIGIN = 0x2000F000, LENGTH = 4K  /* 专用于noinit段 */
}

SECTIONS
{
    /* ... 其他段定义 ... */
    
    /* 不初始化段(热重启保留) */
    .noinit (NOLOAD) :
    {
        . = ALIGN(4);
        _noinit_start = .;
        
        /* 日志缓冲区放在这里 */
        *(.noinit)
        *(.noinit.*)
        
        . = ALIGN(4);
        _noinit_end = .;
    } > NOINIT
    
    /* ... 其他段定义 ... */
}
```

### 7.2 在代码中使用noinit段

c

```c
// ww_log_ram.c

/**
 * 日志缓冲区定义
 * 
 * 说明:
 * - 使用__attribute__((section(".noinit")))放到特殊段
 * - 这个段在启动代码中不会被清零
 * - 需要在链接脚本中配置对应的内存区域
 */
#ifdef CONFIG_WW_LOG_RAM_PERSISTENT
    __attribute__((section(".noinit"))) WW_LOG_RAM_T g_log_ram;
#else
    WW_LOG_RAM_T g_log_ram;  // 普通全局变量,会被清零
#endif
```

### 7.3 启动代码修改

确保启动代码不清除noinit段:

c

```c
// startup.c

void Reset_Handler(void) {
    // 1. 复制data段从Flash到RAM
    memcpy(&_data_start, &_data_load, &_data_end - &_data_start);
    
    // 2. 清零bss段
    memset(&_bss_start, 0, &_bss_end - &_bss_start);
    
    // 3. 注意:不清零noinit段
    // memset(&_noinit_start, 0, &_noinit_end - &_noinit_start); // 不要这样做!
    
    // 4. 调用main函数
    main();
}
```

### 7.4 初始化时的检查逻辑

c

```c
// ww_log_ram.c

void log_ram_init(U8 force_clear) {
    U8 valid = 0;
    
    #ifdef CONFIG_WW_LOG_RAM_PERSISTENT
    // 检查魔数是否有效
    if (g_log_ram.magic_head == 0x4C4F4748 && 
        g_log_ram.magic_tail == 0x4C4F4754) {
        
        // 进一步检查数据一致性
        if (g_log_ram.entry_head < CONFIG_WW_LOG_RAM_ENTRY_NUM &&
            g_log_ram.entry_tail < CONFIG_WW_LOG_RAM_ENTRY_NUM) {
            
            if (!force_clear) {
                valid = 1;
                uart_printf("Log buffer preserved after warm reset\n");
                uart_printf("  Head: %d, Tail: %d, Count: %d\n",
                          g_log_ram.entry_head, g_log_ram.entry_tail,
                          log_ram_get_count());
            }
        }
    }
    #endif
    
    if (!valid) {
        // 魔数无效或强制清空,初始化缓冲区
        memset(&g_log_ram, 0, sizeof(g_log_ram));
        g_log_ram.magic_head = 0x4C4F4748;
        g_log_ram.magic_tail = 0x4C4F4754;
        g_log_ram.entry_head = 0;
        g_log_ram.entry_tail = 0;
        
        uart_printf("Log buffer initialized\n");
    }
}
```

## 8. 性能评估与优化

### 8.1 代码空间对比

以一个典型的嵌入式项目为例,假设有500个日志点:

```
项目str_modeencode_mode节省
字符串常量~40KB0KB40KB
printf库函数~8KB0KB8KB
日志处理代码~2KB~3KB-1KB
文件ID枚举0KB~0.5KB-0.5KB
总计~50KB~3.5KB~46.5KB (93%)
```

**说明:**

- str_mode每个日志点平均80字节字符串,500个约40KB
- encode_mode只需要枚举定义和编码函数,约3.5KB
- 节省了约93%的代码空间

### 8.2 RAM占用对比

单条日志的RAM占用:

```
项目str_modeencode_mode
格式化缓冲区128字节0字节
栈开销~200字节~50字节
环形缓冲区(64条)不适用64×12=768字节
```

**说明:**

- str_mode由于需要格式化字符串,栈开销较大
- encode_mode只需要简单的整数操作,栈开销小
- encode_mode的环形缓冲区虽然占用RAM,但是可控的

### 8.3 执行时间对比

在80MHz的ARM Cortex-M4上测试:

```
操作str_modeencode_mode
简单日志(无参数)~150μs~15μs
带参数日志(2个)~200μs~20μs
UART输出(115200波特率)~1ms~0.5ms
```

**说明:**

- str_mode需要格式化字符串,开销大
- encode_mode只是简单的位操作和赋值,开销小
- UART输出时间主要取决于波特率和数据量

### 8.4 优化建议

1. **减少日志频率**
   - 对于高频调用的函数,考虑降低日志级别或使用采样
   - 避免在中断中频繁打印日志

1. **优化临界区时间**
   - 临界区内只做最必要的操作
   - 考虑使用无锁数据结构(如果RTOS支持)

1. **使用DMA传输UART数据**
   - 如果UART支持DMA,可以异步传输日志数据
   - 减少CPU在UART传输上的等待时间

1. **分级存储**
   - ERROR级别的日志同时保存到RAM和外存
   - INFO/DEBUG级别的日志只输出到UART
   - 根据重要性分配资源

1. **压缩存储**
   - 如果外存空间紧张,考虑对日志进行简单压缩
   - 比如RLE(行程编码)或者差分编码

## 9. 测试计划

### 9.1 单元测试

#### 9.1.1 编码/解码测试

c

```c
// test_encode_decode.c

void test_encode_decode(void) {
    U32 encoded;
    U16 file_id, line;
    U8 level;
    
    // 测试用例1:基本编码解码
    encoded = LOG_ENCODE_PACK(123, 456, WW_LOG_LEVEL_ERR);
    file_id = LOG_DECODE_FILE_ID(encoded);
    line = LOG_DECODE_LINE_NUM(encoded);
    level = LOG_DECODE_LEVEL(encoded);
    
    WW_ASSERT(file_id == 123, "File ID decode failed");
    WW_ASSERT(line == 456, "Line decode failed");
    WW_ASSERT(level == WW_LOG_LEVEL_ERR, "Level decode failed");
    
    // 测试用例2:边界值
    encoded = LOG_ENCODE_PACK(4095, 4095, 15);
    file_id = LOG_DECODE_FILE_ID(encoded);
    line = LOG_DECODE_LINE_NUM(encoded);
    level = LOG_DECODE_LEVEL(encoded);
    
    WW_ASSERT(file_id == 4095, "Max file ID failed");
    WW_ASSERT(line == 4095, "Max line failed");
    WW_ASSERT(level == 15, "Max level failed");
    
    uart_printf("Encode/Decode test passed\n");
}
```

#### 9.1.2 环形缓冲区测试

c

```c
// test_ring_buffer.c

void test_ring_buffer(void) {
    LOG_ENTRY_T entry;
    int ret;
    
    // 初始化
    log_ram_init(1);  // 强制清空
    
    // 测试1:空状态读取
    ret = log_ram_read_entry(&entry);
    WW_ASSERT(ret == -1, "Empty read should fail");
    
    // 测试2:写入和读取
    log_ram_write_entry(0x12345678, 0xAABBCCDD, 0);
    ret = log_ram_read_entry(&entry);
    WW_ASSERT(ret == 0, "Read should succeed");
    WW_ASSERT(entry.entry[0] == 0x12345678, "Data mismatch");
    WW_ASSERT(entry.entry[1] == 0xAABBCCDD, "Param mismatch");
    
    // 测试3:填满缓冲区
    for (int i = 0; i < CONFIG_WW_LOG_RAM_ENTRY_NUM; i++) {
        log_ram_write_entry(i, 0, 0);
    }
    
    U16 count = log_ram_get_count();
    WW_ASSERT(count == CONFIG_WW_LOG_RAM_ENTRY_NUM - 1, "Buffer full count error");
    
    // 测试4:翻转
    log_ram_init(1);
    for (int i = 0; i < CONFIG_WW_LOG_RAM_ENTRY_NUM * 2; i++) {
        log_ram_write_entry(i, 0, 0);
    }
    
    // 读取所有数据,检查是否正确翻转
    for (int i = 0; i < CONFIG_WW_LOG_RAM_ENTRY_NUM - 1; i++) {
        ret = log_ram_read_entry(&entry);
        WW_ASSERT(ret == 0, "Wrap-around read failed");
    }
    
    uart_printf("Ring buffer test passed\n");
}
```

#### 9.1.3 级别过滤测试

c

```c
// test_level_filter.c

void test_level_filter(void) {
    // 设置全局级别为WRN
    log_set_level(WW_LOG_LEVEL_WRN);
    
    log_ram_init(1);  // 清空
    
    // 这些应该被记录
    TEST_LOG_ERR_MSG("Error message");
    TEST_LOG_WRN_MSG("Warning message");
    
    // 这些应该被过滤
    TEST_LOG_INF_MSG("Info message");
    TEST_LOG_DBG_MSG("Debug message");
    
    // 检查缓冲区中只有2条日志
    U16 count = log_ram_get_count();
    WW_ASSERT(count == 2, "Level filter failed, count=%d", count);
    
    uart_printf("Level filter test passed\n");
}
```

### 9.2 集成测试

#### 9.2.1 多任务并发测试

c

```c
// test_multithread.c (需要RTOS环境)

void log_task1(void *arg) {
    for (int i = 0; i < 100; i++) {
        TEST_LOG_INF_MSG("Task1: iteration %d", i);
        osDelay(10);
    }
}

void log_task2(void *arg) {
    for (int i = 0; i < 100; i++) {
        TEST_LOG_WRN_MSG("Task2: iteration %d", i);
        osDelay(10);
    }
}

void test_multithread(void) {
    log_ram_init(1);
    
    osThreadId_t tid1 = osThreadNew(log_task1, NULL, NULL);
    osThreadId_t tid2 = osThreadNew(log_task2, NULL, NULL);
    
    // 等待任务完成
    osDelay(2000);
    
    // 检查日志完整性
    U16 count = log_ram_get_count();
    uart_printf("Multithread test: %d logs recorded\n", count);
    
    // 检查是否有数据损坏
```