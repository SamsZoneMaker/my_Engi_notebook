---
created: 2025-11-18
tags:
  - type/reference
  - topic/tools
---
## 📋 概述

Makefile 是用于自动化构建和管理项目依赖关系的强大工具。

**核心价值**：
- **自动化编译**：一条`make`命令完成整个工程编译
- **增量编译**：只重编修改过的文件，提升效率
- **依赖管理**：自动处理文件间的依赖关系
- **跨平台**：Unix/Linux/macOS/Windows广泛支持

---

## 🎯 学习目标

- [ ] 理解Make的工作原理
- [ ] 掌握基本规则语法
- [ ] 学会使用变量和函数
- [ ] 掌握隐式规则
- [ ] 能够编写实用的Makefile
- [ ] 理解模式规则和静态模式
- [ ] 掌握嵌套make和多目录构建

---

## 📚 核心内容

### Makefile基本结构

```makefile
targets: prerequisites
	command
	command
```

**组成部分**：

| 部分 | 说明 | 示例 |
|------|------|------|
| 目标(Target) | 要生成的文件或操作 | `main.o`, `clean` |
| 依赖(Prerequisites) | 目标依赖的文件 | `main.c`, `utils.h` |
| 命令(Command) | 生成目标的Shell命令 | `gcc -c main.c` |

**⚠️ 重要规则**：
- 命令行必须以 **Tab键** 开头（不是空格！）
- 依赖文件比目标新时，命令会被执行
- Make 默认执行第一个目标

---

## 🔧 基础使用

### 1. 简单示例

```makefile
# 最简单的Makefile
hello: hello.c
	gcc hello.c -o hello

clean:
	rm -f hello
```

**执行**：
```bash
make        # 编译hello
make clean  # 清理
```

### 2. 多文件项目

```makefile
# 编译多个源文件
program: main.o utils.o
	gcc main.o utils.o -o program

main.o: main.c utils.h
	gcc -c main.c

utils.o: utils.c utils.h
	gcc -c utils.c

clean:
	rm -f program main.o utils.o
```

### 3. 使用变量

```makefile
CC = gcc
CFLAGS = -Wall -g
OBJS = main.o utils.o helper.o

program: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o program

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f program $(OBJS)
```

---

## 📝 Make工作流程

### 执行过程

1. **读取Makefile**：查找当前目录下的 `Makefile` 或 `makefile`
2. **找到第一个目标**：作为最终目标
3. **检查依赖**：递归检查目标的所有依赖
4. **判断是否更新**：
   - 目标不存在 → 执行命令
   - 依赖比目标新 → 执行命令
   - 依赖无变化 → 跳过
5. **执行命令**：按顺序执行规则中的命令

**依赖树示例**：

```
program
  ├─ main.o
  │    ├─ main.c
  │    └─ defs.h
  ├─ utils.o
  │    ├─ utils.c
  │    └─ defs.h
  └─ helper.o
       ├─ helper.c
       └─ helper.h
```

---

## 🎨 变量

### 变量定义

```makefile
# 递归变量（延迟展开）
VAR = value

# 简单变量（立即展开）
VAR := value

# 追加变量
VAR += more

# 条件赋值（未定义时才赋值）
VAR ?= default

# 示例
CC = gcc
CFLAGS = -Wall
CFLAGS += -g -O2
TARGET ?= program
```

### 变量引用

```makefile
$(VAR)   # 推荐
${VAR}   # 也可以
$V       # 单字符变量（不推荐）
```

### 常用内置变量

```makefile
CC       # C编译器 (默认: cc)
CXX      # C++编译器 (默认: g++)
CFLAGS   # C编译选项
CXXFLAGS # C++编译选项
LDFLAGS  # 链接选项
AR       # 打包工具 (默认: ar)
```

### 自动变量 ⭐⭐⭐⭐⭐

| 变量 | 含义 | 示例 |
|------|------|------|
| `$@` | 目标文件名 | `main.o` |
| `$<` | 第一个依赖文件名 | `main.c` |
| `$^` | 所有依赖文件（去重） | `main.c utils.h` |
| `$?` | 比目标新的依赖文件 | `utils.h` |
| `$*` | 模式匹配的部分 | `main` (from `%.o: %.c`) |
| `$(@D)` | 目标的目录部分 | `dir/` |
| `$(@F)` | 目标的文件名部分 | `main.o` |

**实例**：

```makefile
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
	# $< = xxx.c
	# $@ = xxx.o

program: main.o utils.o
	$(CC) $^ -o $@
	# $^ = main.o utils.o
	# $@ = program
```

---

## 🎯 伪目标

伪目标不是实际文件，只是一个标签。

```makefile
.PHONY: clean all install

all: program

clean:
	rm -f *.o program

install: program
	cp program /usr/local/bin/
```

**常用伪目标**：

| 目标 | 用途 |
|------|------|
| `all` | 编译所有目标 |
| `clean` | 清理生成文件 |
| `install` | 安装程序 |
| `test` | 运行测试 |
| `dist` | 打包分发 |

---

## 🔄 模式规则

### 基本模式

```makefile
# % 通配符匹配任意字符串
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```

**示例**：

```makefile
# 编译C文件
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

# 编译C++文件
%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $< -o $@

# 生成依赖文件
%.d: %.c
	$(CC) -M $< > $@
```

### 静态模式规则

```makefile
objs = foo.o bar.o baz.o

$(objs): %.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@
```

**与普通模式的区别**：
- 静态模式：明确指定目标列表
- 普通模式：匹配所有符合的文件

---

## 🔀 函数

### 字符串函数

```makefile
# 1. subst - 字符串替换
$(subst .c,.o,main.c utils.c)  # → main.o utils.o

# 2. patsubst - 模式替换
$(patsubst %.c,%.o,main.c utils.c)  # → main.o utils.o

# 3. strip - 去除空格
$(strip "  hello   world  ")  # → "hello world"

# 4. findstring - 查找字符串
$(findstring main,main.c utils.c)  # → main

# 5. filter - 过滤
$(filter %.c,main.c utils.o test.c)  # → main.c test.c

# 6. filter-out - 反向过滤
$(filter-out %.c,main.c utils.o)  # → utils.o
```

### 文件名函数

```makefile
FILES = src/main.c include/utils.h

# dir - 提取目录
$(dir $(FILES))  # → src/ include/

# notdir - 提取文件名
$(notdir $(FILES))  # → main.c utils.h

# suffix - 提取后缀
$(suffix $(FILES))  # → .c .h

# basename - 去除后缀
$(basename $(FILES))  # → src/main include/utils

# addprefix - 添加前缀
$(addprefix build/,$(FILES))  # → build/src/main.c build/include/utils.h

# addsuffix - 添加后缀
$(addsuffix .o,main utils)  # → main.o utils.o
```

### 其他实用函数

```makefile
# wildcard - 获取文件列表
SRCS = $(wildcard *.c)  # 获取所有.c文件

# shell - 执行shell命令
DATE = $(shell date +%Y%m%d)

# foreach - 循环
DIRS = src include lib
ALL_FILES = $(foreach dir,$(DIRS),$(wildcard $(dir)/*.c))

# if - 条件判断
RESULT = $(if $(DEBUG),-g,-O2)
```

---

## 📂 实战示例

### 示例1：完整的C项目Makefile

```makefile
# 项目配置
PROJECT = myapp
VERSION = 1.0

# 编译器设置
CC = gcc
CFLAGS = -Wall -Wextra -std=c11
DEBUG_FLAGS = -g -DDEBUG
RELEASE_FLAGS = -O2 -DNDEBUG

# 目录设置
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build
BIN_DIR = bin

# 源文件和目标文件
SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SRCS))
DEPS = $(OBJS:.o=.d)

# 目标程序
TARGET = $(BIN_DIR)/$(PROJECT)

# 默认为Debug模式
DEBUG ?= 1
ifeq ($(DEBUG),1)
    CFLAGS += $(DEBUG_FLAGS)
else
    CFLAGS += $(RELEASE_FLAGS)
endif

# 默认目标
.PHONY: all
all: $(TARGET)

# 链接
$(TARGET): $(OBJS) | $(BIN_DIR)
	$(CC) $(CFLAGS) $^ -o $@
	@echo "Build complete: $@"

# 编译
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -I$(INC_DIR) -MMD -MP -c $< -o $@

# 创建目录
$(BUILD_DIR) $(BIN_DIR):
	mkdir -p $@

# 包含依赖文件
-include $(DEPS)

# 清理
.PHONY: clean
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)

# 运行
.PHONY: run
run: $(TARGET)
	./$(TARGET)

# Release构建
.PHONY: release
release:
	$(MAKE) DEBUG=0

# 安装
.PHONY: install
install: release
	install -m 755 $(TARGET) /usr/local/bin/

# 显示信息
.PHONY: info
info:
	@echo "Project: $(PROJECT) v$(VERSION)"
	@echo "Sources: $(SRCS)"
	@echo "Objects: $(OBJS)"
	@echo "Target:  $(TARGET)"
```

### 示例2：多目录项目

```makefile
PROJECT = server

# 子目录
SUBDIRS = network database utils

# 默认目标
.PHONY: all
all:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir; \
	done
	$(CC) -o $(PROJECT) $(wildcard */build/*.o)

# 清理
.PHONY: clean
clean:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean; \
	done
	rm -f $(PROJECT)

# 子目录Makefile示例 (network/Makefile)
# CC = gcc
# CFLAGS = -Wall -I../include
# BUILD_DIR = build
# SRCS = $(wildcard *.c)
# OBJS = $(patsubst %.c,$(BUILD_DIR)/%.o,$(SRCS))
#
# all: $(OBJS)
#
# $(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
#     $(CC) $(CFLAGS) -c $< -o $@
#
# $(BUILD_DIR):
#     mkdir -p $@
#
# clean:
#     rm -rf $(BUILD_DIR)
```

### 示例3：库文件构建

```makefile
LIB_NAME = mylib
LIB_STATIC = lib$(LIB_NAME).a
LIB_SHARED = lib$(LIB_NAME).so

SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)

# 构建静态库
$(LIB_STATIC): $(OBJS)
	ar rcs $@ $^

# 构建动态库
$(LIB_SHARED): $(OBJS)
	$(CC) -shared -fPIC $^ -o $@

# 编译位置无关代码
%.o: %.c
	$(CC) -c -fPIC $(CFLAGS) $< -o $@

.PHONY: all
all: $(LIB_STATIC) $(LIB_SHARED)

.PHONY: install
install: all
	install -m 644 $(LIB_STATIC) /usr/local/lib/
	install -m 755 $(LIB_SHARED) /usr/local/lib/
	ldconfig
```

---

## 🔍 高级技巧

### 1. 自动生成依赖

```makefile
# 方法1：使用gcc -M
%.d: %.c
	@set -e; rm -f $@; \
	$(CC) -M $(CFLAGS) $< > $@.tmp; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.tmp > $@; \
	rm -f $@.tmp

-include $(OBJS:.o=.d)

# 方法2：使用gcc -MMD（推荐）
%.o: %.c
	$(CC) -MMD -MP -c $(CFLAGS) $< -o $@

-include $(OBJS:.o=.d)
```

### 2. 条件判断

```makefile
# 系统判断
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    LDFLAGS += -lpthread
endif
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -framework CoreFoundation
endif

# 变量判断
ifdef DEBUG
    CFLAGS += -g
else
    CFLAGS += -O2
endif

# 值比较
ifeq ($(CC),gcc)
    CFLAGS += -fno-strict-aliasing
endif
```

### 3. 嵌套Make

```makefile
# 主Makefile
export CC CFLAGS  # 导出变量

.PHONY: all
all:
	$(MAKE) -C subdir1
	$(MAKE) -C subdir2

# 或使用foreach
SUBDIRS = dir1 dir2 dir3

.PHONY: all
all:
	@for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir || exit 1; \
	done
```

### 4. 并行编译

```bash
# 使用-j指定并行任务数
make -j4      # 4个并行任务
make -j       # 自动检测CPU核心数
```

---

## 🛠️ 调试Makefile

### 调试选项

```bash
make -n        # 只显示命令，不执行
make -p        # 打印所有规则和变量
make -d        # 显示调试信息
make -w        # 显示工作目录
make --trace   # 显示执行跟踪
```

### 调试技巧

```makefile
# 1. 打印变量
$(info SRCS = $(SRCS))
$(info OBJS = $(OBJS))

# 2. 警告信息
$(warning This is a warning message)

# 3. 错误信息并停止
$(error Build failed: missing file)

# 4. 显示命令
%.o: %.c
	@echo "Compiling $<..."
	$(CC) -c $< -o $@
```

---

## ⚠️ 常见陷阱

### 1. Tab vs 空格

```makefile
# ❌ 错误：使用空格
target:
    gcc main.c  # 这会报错！

# ✅ 正确：使用Tab
target:
	gcc main.c
```

### 2. 变量展开时机

```makefile
# = 递归展开（延迟）
VAR = $(OTHER)
OTHER = value
# VAR 在使用时才展开为 "value"

# := 简单展开（立即）
VAR := $(OTHER)
OTHER = value
# VAR 立即展开，值为空
```

### 3. 忘记.PHONY

```makefile
# ❌ 如果存在名为clean的文件，make clean会失败
clean:
	rm -f *.o

# ✅ 声明为伪目标
.PHONY: clean
clean:
	rm -f *.o
```

### 4. 路径问题

```makefile
# ❌ 相对路径可能出错
include ../common.mk

# ✅ 使用CURDIR或绝对路径
include $(CURDIR)/../common.mk
```

---

## 📋 Make参数速查

| 参数 | 说明 |
|------|------|
| `-f <file>` | 指定Makefile文件 |
| `-C <dir>` | 切换到指定目录 |
| `-j [N]` | 并行编译（N个任务） |
| `-n` | 只显示命令，不执行 |
| `-B` | 强制重新编译所有目标 |
| `-k` | 出错后继续执行 |
| `-s` | 静默模式 |
| `-w` | 显示工作目录 |

---

## 🔗 相关链接

- [[Linux系统编程 - 文件IO]] - 文件操作
- [[Shell脚本编程基础]] - Shell命令
- [[C语言基础 - 数据类型与变量]] - C语言基础
- [[C 语言知识地图]] - C语言知识地图

---

## 📚 参考资料

- GNU Make Manual: https://www.gnu.org/software/make/manual/
- GCC Manual: https://gcc.gnu.org/onlinedocs/gcc/
- 陈皓《跟我一起写Makefile》

---

## ✅ 学习检查清单

- [ ] 理解Make的工作原理和依赖关系
- [ ] 掌握基本规则的编写
- [ ] 熟练使用变量和自动变量
- [ ] 会使用模式规则简化Makefile
- [ ] 掌握常用函数的使用
- [ ] 能够编写实用的项目Makefile
- [ ] 理解并使用隐式规则
- [ ] 会调试和优化Makefile

---

## 🎓 最佳实践

1. **使用变量**：提高可维护性
2. **声明伪目标**：避免与文件名冲突
3. **自动生成依赖**：使用`-MMD -MP`
4. **目录组织**：源文件、构建文件分离
5. **错误处理**：检查命令返回值
6. **文档注释**：添加必要的说明
7. **模式规则**：减少重复代码
8. **并行编译**：加速构建过程

---

*最后更新: 2025-11-18*

## 相关笔记

- [[Linux系统编程 - 文件IO]]
- [[C语言基础 - 数据类型与变量]]
- [[Shell脚本编程基础]]
