---
tags:
  - shell
  - projDragon
  - Linux
aliases:
create date: 2025-08-22 16:20:48
modify date: 2025-08-25  18:11:30
---
# 📝 笔记内容

`build.sh` 文件位于仓库根目录下，其设计的思想是根据不同的构建对象、构建链生成不同的编译结果，等同于对dragon库的一次编译（一般只针对需要编译的部分）

## 分类
对象有四类
- boot
- app
- demo
- test
不同的类别对编译所需条件不同

### boot类
boot类通常需要指定的是 **target file**，通过参数 `-ld` 指定。
`-o` 为选择性的方案，非必须，选择的内容为 ==xxx.option==,用于定义target的额外编译和链接参数

### app/demo/test 类
与Boot类相比

## 代码解析

### 目录和脚本信息
#### f_determin_dir()
这个函数主要用于确定脚本的执行目录和所在的目录，并针对使用 `source` 执行脚本的特殊情况
```shell
f_determin_dir()
{
    L_SCRIPT_EXECUTED_DIR=$(pwd)                    # 步骤1：保存当前工作目录
    if [ "$0" = "-bash" ]; then                     # 步骤2：判断脚本执行方式
        cd "$(dirname "$BASH_SOURCE")"              # 步骤3a：source执行时，切换到脚本所在目录
        L_SCRIPT_LOCATED_DIR=$(pwd)                 # 步骤4a：获取脚本所在目录的绝对路径
        L_SCRIPT_NAME=$(basename "$BASH_SOURCE")    # 步骤5a：获取脚本文件名
    else
        cd "$(dirname "$0")"                        # 步骤3b：直接执行时，切换到$0所在目录
        L_SCRIPT_LOCATED_DIR=$(pwd)                 # 步骤4b：获取脚本所在目录的绝对路径
        L_SCRIPT_NAME=$(basename "$0")              # 步骤5b：获取脚本文件名
    fi
    cd ${L_SCRIPT_EXECUTED_DIR}                     # 步骤6：恢复到原始工作目录
}
```

**变量说明**
- `L_SCRIPT_EXECUTED_DIR`: 脚本被执行时的工作目录
	
- `L_SCRIPT_LOCATED_DIR`: 脚本文件实际所在的目录
    
- `L_SCRIPT_NAME`: 脚本文件名
    
- `$0`: 在直接执行时是脚本路径，source执行时是"-bash"
    
- `$BASH_SOURCE`: 始终指向当前脚本文件路径

### 输出格式化
#### f_print
基础输出，使用 `echo -e`
```Shell
f_print()
{
    echo -e "$@"    # 使用echo -e输出所有参数，支持转义字符解释
}
```

**说明**
-  接收所有传入参数（$@）
    
-  使用echo -e输出，-e参数启用转义字符解释（如\n, \t等）

#### f_trace
绿色输出，用于正常的日志信息
```Shell
f_trace()
{
    echo -e "\033[32m${L_PREFIX} $@\033[0m" >&1
}
```

**说明**
- 使用ANSI转义序列设置绿色文本 `\033[32m`
    
- 输出前缀变量`L_PREFIX` 
    
- 输出所有参数（$@）
    
- 重置颜色到默认（\033[0m）
    
- 输出到标准输出（>&1）

#### f_alert
紫色输出，用于警告信息
```Shell
f_alert()
{
    echo -e "\033[35m${L_PREFIX} $@\033[0m" >&2
}
```

**说明**
- 使用ANSI转义序列设置紫色文本（\033[35m）
    
- 输出前缀变量L_PREFIX和所有参数
    
- 重置颜色到默认
    
- 输出到标准错误（>&2）

#### f_exit: 
红色背景输出，用于错误信息并退出程序
```Shell
f_exit()
{
    echo -e "\033[41;37m${L_PREFIX}[error] $@\033[0m" >&2
    exit 1
}
```

**说明**
- 设置红色背景白色前景 `\033[41;37m`
    
- 输出前缀、`[error]`标识和错误信息
    
- 重置颜色
    
- 输出到标准错误
    
- 以退出码 `1` 终止脚本执行

### 命令执行和路径验证
#### f_execute_cmd
作用是先把要执行的命令显示出来，然后再执行
```Shell
f_execute_cmd()
{
    f_trace "$1"    # 步骤1：使用绿色输出显示即将执行的命令
    eval "$1"       # 步骤2：使用eval执行传入的命令字符串
}
```

**说明**
1. 先通过f_trace以绿色显示要执行的命令
    
2. 使用eval执行命令，eval允许执行包含变量展开的复杂命令

#### f_exit_if_path_not_exist
作用是检查路径是否存在，不存在则退出
```Shell
f_exit_if_path_not_exist()
{
    if [ $# -lt 1 ]; then                                    # 步骤1：检查参数数量
        f_exit "Path not exist: ${FUNCNAME[0]}"              # 步骤2a：参数不足时报错退出
    fi

    if [ -e "$1" ]; then                                     # 步骤3：检查路径是否存在
        :                                                    # 步骤4a：路径存在，空操作继续
    else
        f_exit "Path not exist: $1"                         # 步骤4b：路径不存在，报错退出
    fi
}
```

**说明**
1. `$#`获取参数个数，检查是否至少有1个参数
    
2. `${FUNCNAME[0]}`获取当前函数名用于错误信息
    
3. `-e "$1"`测试文件或目录是否存在
    
4. `:`是bash的空命令，相当于true但不做任何操作

#### f_get_abs_path
作用是获取绝对路径

#### f_exit_if_var_is_empty_or_not_exist
作用是检查变量是否为空

### 进程管理
#### f_wait_process_stop
该函数用于处理进程的启停，包括等待进程停止、强制停止应用程序

### 选择菜单system
#### f_choice_list_add_item
添加菜单项，避免重复

#### f_choice_build_list
通过命令来构建选择列表

#### f_choice_print_menu
显示菜单中的编号

#### f_choice
主要作用是获取用户的输入，是主选择函数

### 参数解析
对于输入的参数，需要进行解析后分类对应到编译使用的不同参数，涵盖的参数大概有

#### f_parse_option
参数解析的核心函数，主要需要识别的参数有
- `-p/--product`: 产品类型
- `-t/--target`: 目标名称
- `-a/--arch`: 架构类型
- `-ec`: 扩展配置文件
- `-tc`: 目标配置文件
- `-ld`: 链接器脚本文件
- `-bi`: 构建信息文件
- `-o/--option`: 选项文件
- `-d/-D`: GCC编译选项
- `-g`: GCC编译标志
- `-l`: GCC链接标志
- `-m`: Make变量
- `-c/--clean`: 清理构建

### 工具链的配置

主要涉及Andes工具链的准备，例如
- 检查工具链的MD5值判断是否需要重新解压
- 自动解压工具链tar包
- 设置交叉编译器前缀为 `riscv32-elf-`
