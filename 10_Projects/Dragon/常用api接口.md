---
created: 2026-08-28
tags:
  - type/knowledge
---
> [!abstract] 核心结论
> 这个文档用于记录 Dragon_fw中常用到的通用与模块内用的api接口，方便速查


## 通用接口 api

### WW_CSR_RD
该api用于读取指定地址处的32位 CSR
```C
#define WW_CSR_RD  sys_read32(addr)
#define sys_read32(addr)  (*((volatile const uint32_t *)(ADDR)(addr)))
```

特别说明 `sys_read32` 的实现方式，实际的过程：
1. 将 `addr` 转换为一个 `uint32_t ` 类型的地址
	
2. `*` 从 `addr` 解引用一次
	
3. 读取 addr 地址上的32位数据

上述过程等价代码
```c
ADDR normalized_addr = (ADDR)(addr);

volatile const uint32_t *p =
    (volatile const uint32_t *)normalized_addr;

uint32_t value = *p;

```

调用方式：
```c
uint32_t value = WW_CSR_RD(CSR_ADDRESS);

uint32_t value = WW_CSR_RD(0xd0c00400);

// 实际等价于
uint32_t value =
    *(volatile const uint32_t *)(ADDR)(CSR_ADDRESS);
```
- `uint32_t`：每次读取 32 位。
- `const`：禁止通过这个指针写寄存器。
- `volatile`：要求编译器每次都真正访问该地址，不能缓存、合并或删除读取操作。
- `(ADDR)(addr)`：通常用于把输入地址规范化为平台的地址类型；具体含义取决于 `ADDR` 的定义

^WWCSRWR

### WW_CSR_WR
写入整个32位寄存器，用法类似
```c
WW_CSR_WR(REG_ADDR, 0x12345678u);
```


### WW_CSR_BITS_SET
用于将掩码对应位置 置1，用法
```c
WW_CSR_BITS_SET(REG_ADDR, 0x00000005u);
```


### WW_CSR_BITS_CLR
用于将掩码对应位置 置0，用法
```c
WW_CSR_BITS_CLR(REG_ADDR, 0x00000004u);
```


### WW_CSR_FIELD_RD
读取指定字段并右移到最低位，因为读出需要是最低那位
```c
mode = WW_CSR_FIELD_RD(REG_ADDR, MODE_MASK, MODE_OFFSET);
```


### WW_CSR_FIELD_WR
修改指定字段，其他位保持不变
```C
WW_CSR_FIELD_WR(REG_ADDR, MODE_MASK, MODE_OFFSET, 0x5u);
```
参数含义：
- `addr`：寄存器地址
- `mask`：字段在整个32位寄存器中的位置掩码
- `offset`：字段最低位距离 bit0 的位数
- `data`：要写入字段的原始值，无需提前左移

Example：
假设要修改的寄存器字段是 \[11:8]
```c
/*
31                          12 11       8 7          0
+-----------------------------+----------+------------+
|         其他字段             | 目标字段  |  其他字段   |
+-----------------------------+----------+------------+
*/


// 目标字段的宽度是4位，因此定义

#define FIELD_MASK    0x00000F00u
#define FIELD_OFFSET  8u

// `mask = 0x00000F00`：二进制的 bit11～bit8 为1。
// `offset = 8`：字段最低位是 bit8。

WW_CSR_FIELD_WR(REG_ADDR, 0x00000F00u, 8u, 0xAu);

/* Inertial flow */
0. 假设寄存器的原始值为：0x12345678
   目标的字段是 [11:8]，当前的值是 0x6

1. 读取整个寄存器  tmp = sys_read32(addr);  
   tmp = 0x12345678
   
2. 清除原字段  tmp &= ~mask;
   mask是0x00000f00
   ~mask是 0xfffff0ff
   所以tmp 与上 ~mask的结果是 0x12345078，清空了bit [11:8]
   

3. 把新数据移动到字段位置   (data << offset) & mask
   计算：
   data           = 0xA
   data << 8      = 0x00000A00
   & mask         = 0x00000A00


4. 合并到寄存器当中
   tmp |= ((data << offset) & mask);
   计算：
  0x12345078
| 0x00000A00
--------------
  0x12345A78


5. 写回寄存器
   sys_write32(addr, tmp);
```







## 速查表

| 宏                                         | 用法                                         | 作用             |
| ----------------------------------------- | ------------------------------------------ | -------------- |
| `WW_CSR_RD(addr)`                         | `value = WW_CSR_RD(addr);`                 | 读取整个32位寄存器     |
| `WW_CSR_WR(addr, data)`                   | `WW_CSR_WR(addr, data);`                   | 写入整个32位寄存器     |
| `WW_CSR_BITS_SET(addr, mask)`             | `WW_CSR_BITS_SET(addr, BIT(3));`           | 将掩码对应位置1       |
| `WW_CSR_BITS_CLR(addr, mask)`             | `WW_CSR_BITS_CLR(addr, BIT(3));`           | 将掩码对应位清0       |
| `WW_CSR_FIELD_RD(addr, mask, ofst)`       | `value = WW_CSR_FIELD_RD(addr, 0xF00, 8);` | 读取指定字段并右移到最低位  |
| `WW_CSR_FIELD_WR(addr, mask, ofst, data)` | `WW_CSR_FIELD_WR(addr, 0xF00, 8, 5);`      | 修改指定字段，其他位保持不变 |

