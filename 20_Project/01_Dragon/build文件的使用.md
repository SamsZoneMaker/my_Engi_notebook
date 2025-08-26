---
tags:
  - shell
  - projDragon
  - Linux
aliases:
create date: 2025-08-22 16:20:48
modify date: 2025-08-26  18:53:44
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
    L_SCRIPT_EXECUTED_DIR=$(pwd)                    # step1：保存当前工作目录
    if [ "$0" = "-bash" ]; then                     # step2：判断脚本执行方式
        cd "$(dirname "$BASH_SOURCE")"              # step3a：source执行时，切换到脚本所在目录
        L_SCRIPT_LOCATED_DIR=$(pwd)                 # step4a：获取脚本所在目录的绝对路径
        L_SCRIPT_NAME=$(basename "$BASH_SOURCE")    # step5a：获取脚本文件名
    else
        cd "$(dirname "$0")"                        # step3b：直接执行时，切换到$0所在目录
        L_SCRIPT_LOCATED_DIR=$(pwd)                 # step4b：获取脚本所在目录的绝对路径
        L_SCRIPT_NAME=$(basename "$0")              # step5b：获取脚本文件名
    fi
    cd ${L_SCRIPT_EXECUTED_DIR}                     # step6：恢复到原始工作目录
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
    f_trace "$1"    # step1：使用绿色输出显示即将执行的命令
    eval "$1"       # step2：使用eval执行传入的命令字符串
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
    if [ $# -lt 1 ]; then                                    # step1：检查参数数量
        f_exit "Path not exist: ${FUNCNAME[0]}"              # step2a：参数不足时报错退出
    fi

    if [ -e "$1" ]; then                                     # step3：检查路径是否存在
        :                                                    # step4a：路径存在，空操作继续
    else
        f_exit "Path not exist: $1"                         # step4b：路径不存在，报错退出
    fi
}
```

**说明**
1. `$#`获取参数个数，检查是否至少有1个参数
    
2. `${FUNCNAME[0]}`获取当前函数名用于错误信息
    
3. `-e "$1"`测试文件或目录是否存在
    
4. `:`是bash的空命令，相当于true但不做任何操作

#### f_get_abs_path
用于获取某个文件的绝对路径
```Shell
f_get_abs_path()
{
    if [ $# -lt 1 ]; then                                    # step1：验证参数
        f_exit "Get abs path failed: ${FUNCNAME[0]}"
    fi

    l_abs_path=$(realpath -qe $1 || true)                   # step2：获取绝对路径

    if [ -z ${l_abs_path} ]; then                           # step3：检查结果
        f_exit "Get abs path failed: $1"                    # step4a：失败时退出
    else
        echo "${l_abs_path}"                                # step4b：成功时输出路径
    fi
}
```

**说明**
- `realpath -qe`: -q静默模式，-e要求路径必须存在
    
- `|| true`: 防止realpath失败时整个命令失败
    
- 使用局部变量`l_abs_path`（小写l开头）
    
- 通过echo返回结果，调用者可用`$(f_get_abs_path path)`接收

#### f_exit_if_var_is_empty_or_not_exist
作用是检查变量是否为空
```Shell
f_exit_if_var_is_empty_or_not_exist()
{
    if [ -z $1 ]; then                                       # step1：检查第一个参数（变量名）
        f_exit "at least two para for f_exit_if_var_is_empty_or_not_exist"
    fi

    if [ -z "$2" ]; then                                     # step2：检查第二个参数（变量值）
        f_exit "$1 is empty or not exist"                   # step3：变量值为空时报错
    fi
}
```

**说明**
使用场景：`f_exit_if_var_is_empty_or_not_exist "--product" "${L_PARA_PRODUCT}"`

### 进程管理
#### f_wait_process_stop
该函数用于处理进程的启停，包括等待进程停止、强制停止应用程序
```Shell
f_wait_process_stop()
{
    local result time1 time2                                 # step1：声明局部变量

    time1=`date +%s`                                        # step2：获取当前时间戳（秒）
    time1=$((time1 + 5))                                    # step3：计算5秒后的时间戳

    while true; do                                          # step4：进入无限循环
        result=`pgrep -x "$1" || true`                      # step5：查找指定进程
        if [ "${result}" == "" ]; then                      # step6：检查进程是否存在
            break                                           # step7a：进程不存在，退出循环
        fi

        time2=`date +%s`                                    # step8：获取当前时间
        if (( time2 > time1 )); then                       # step9：检查是否超时
            f_exit "wait process $1 stop timeout"          # step10：超时报错退出
        fi
    done
}
```

**说明**
- `pgrep -x`: 精确匹配进程名
    
- `|| true`: 防止`pgrep`未找到进程时返回非0退出码
    
- `(( ))`: 算术运算语法
    
- 5秒超时机制防止无限等待

#### f_app_kill
用于停止进程
```Shell
f_app_kill()
{
    local l_cmd                                             # step1：声明局部变量

    if [ $# -lt 1 ]; then                                  # step2：检查参数
        f_exit "at least one para for f_app_kill"
    fi

    l_cmd="killall $1 2>/dev/null || true"                 # step3：构建killall命令
    f_execute_cmd "${l_cmd}"                               # step4：执行kill命令
    f_wait_process_stop $1                                 # step5：等待进程停止
}
```

**说明 （执行逻辑）**
1. `killall $1`: 杀死所有名为$1的进程
    
2. `2>/dev/null`: 抑制错误输出
    
3. `|| true`: 即使killall失败也继续执行
    
4. 调用wait函数确保进程真正停止

#### f_exit_if_process_is_not_running
```Shell
f_exit_if_process_is_not_running()
{
    if [ $# -lt 1 ]; then                                  # step1：参数检查
        f_exit "at least 1 para for f_exit_if_process_is_not_running"
    fi

    l_temp=$(ps -aux | grep [${1:0:1}]${1:1} | grep -v ${L_SCRIPT_NAME} || true)  # step2：查找进程
    if [ "${l_temp}" == "0" ]; then                        # step3：检查结果
        f_exit "$1 is not running"                         # step4a：进程不运行时退出
    else
        f_trace "$1 is running"                            # step4b：进程运行中，输出日志
    fi
}
```

**说明 (执行逻辑)**
- `${1:0:1}`: 获取第一个字符
    
- `${1:1}`: 获取除第一个字符外的所有字符
    
- `[字符]`: 正则表达式，避免grep匹配到自身
    
- 过滤掉脚本自身进程

### 选择菜单system
#### f_choice_list_add_item
添加菜单项，避免重复
```Shell
f_choice_list_add_item()
{
    local new_item=$1                                       # step1：保存新项目到局部变量
    local c                                                 # step2：声明循环变量

    for c in ${L_CHOICE_MENU_ITEMS[@]}; do                 # step3：遍历现有菜单项
        if [ "$new_item" = "$c" ]; then                    # step4：检查是否重复
            return                                          # step5a：重复则直接返回
        fi
    done

    L_CHOICE_MENU_ITEMS=(${L_CHOICE_MENU_ITEMS[@]} "$new_item")  # step6：添加到数组末尾
}
```

**数组操作详解：**

- `${数组[@]}`: 展开数组所有元素
    
- `数组=(${原数组[@]} 新元素)`: 数组追加元素的标准方法

#### f_choice_build_list
通过命令来构建选择列表
```Shell
f_choice_build_list()
{
    local file                                              # step1：声明循环变量
    
    for file in `eval "$1"`                                # step2：执行命令获取文件列表
    do
        f_choice_list_add_item "$file"                     # step3：逐个添加到菜单
    done
}
```

**执行逻辑：**

- `eval "$1"`: 执行传入的命令字符串
    
- 反引号捕获命令输出，for循环遍历结果

#### f_choice_print_menu
显示菜单中的编号
```Shell
f_choice_print_menu()
{
    local i=1                                              # step1：初始化计数器
    local choice                                           # step2：声明循环变量

    for choice in ${L_CHOICE_MENU_ITEMS[@]}               # step3：遍历菜单项
    do
        echo "    $i. $choice"                            # step4：输出编号和选项
    done
    echo                                                  # step5：输出空行
}
```

#### f_choice
主要作用是获取用户的输入，是主选择函数
```Shell
f_choice()
{
    unset L_CHOICE_MENU_ITEMS                             # step1：清空菜单数组

    local answer                                          # step2：声明局部变量
    local result

    echo -e "\r\n  $2  \r\n"                            # step3：显示提示信息

    f_choice_build_list "$3"                             # step4：构建选项列表

    f_choice_print_menu                                  # step5：显示菜单

    echo -n "Which would you like? [${L_CHOICE_MENU_ITEMS[0]}]: "  # step6：显示提示并默认值
    read answer                                          # step7：读取用户输入

    if [ -z "$answer" ]; then                            # step8：处理空输入
        result=${L_CHOICE_MENU_ITEMS[0]}                 # step9a：使用默认值（第一项）
    elif (echo -n $answer | grep -q -e "^[0-9][0-9]*$"); then  # step9：检查是否为数字
        if [ $answer -le ${#L_CHOICE_MENU_ITEMS[@]} ] && [ $answer -gt 0 ]; then  # step10：验证数字范围
            result=${L_CHOICE_MENU_ITEMS[$((answer-1))]} # step11：获取对应项（数组从0开始）
        fi
    fi

    if [ -z "$result" ]; then                            # step12：验证结果
        f_exit "Invalid choice ${result}"                # step13：无效选择时退出
    fi

    eval $1=$result                                      # step14：将结果赋值给第一个参数指定的变量
}
```

### 参数解析
对于输入的参数，需要进行解析后分类对应到编译使用的不同参数，涵盖的参数大概有

#### f_parse_option
是该shell脚本里的核心函数，参数解析的核心函数，主要需要识别的参数有
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

```Shell
f_parse_option()
{
    while true; do                                              # 无限循环，直到所有参数处理完毕
        case "$1" in                                            # 对第一个参数进行模式匹配
            -p | -P | --product)
                L_PARA_PRODUCT=$2                               # step1: 将第2个参数赋值给产品变量
                f_exit_if_var_is_empty_or_not_exist $1 $2       # step2: 验证参数值非空
                shift 2                                         # step3: 移动参数位置，跳过选项名和值
                ;;                                              
            -t | -T | --target)
                L_PARA_TARGET=$2                                # 保存目标名称
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -a | -A | --archi)
                L_PARA_ARCH=$2                                  # 保存架构类型（如：andes, x86）
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -ec| -ec)                                           # 扩展配置文件
                L_PARA_TARGET_EXT_CONF_FILE=$2                  # 保存扩展配置文件路径
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -tc |--tc)                                          # 目标配置文件
                L_PARA_TARGET_CONF_FILE=$2                      # 保存目标配置文件路径
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -ld |--ld)                                          # 链接器脚本文件
                L_PARA_TARGET_LD_FILE=$2                        # 保存链接器脚本路径
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -bi |--bi)                                          # 构建信息文件
                L_PARA_BI_FILE=$2                               # 保存构建信息文件路径
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -o |-O | --option)                                  # 选项文件
                L_PARA_TARGET_OPTION_FILE=$2
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -d |-D )
                L_PARA_GCC_CFLAG+="-D$2 "                       # step1: 累加编译器定义到CFLAG
                f_exit_if_var_is_empty_or_not_exist $1 $2       # step2: 验证参数非空
                shift 2                                         # step3: 移动参数
                ;;
            -g |--G ) 
                L_PARA_TARGET_GCC_CFLAG+="$2 "                  # 累加编译标志
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -l |--L )
                L_PARA_GCC_LDFLAG+="$2 "                        # 累加链接标志
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -m |--M )
                export "$2"                                     # step1: 导出环境变量
                L_PARA_MAKE_VAR+="$2 "                          # step2: 累加到Make变量列表
                f_exit_if_var_is_empty_or_not_exist $1 $2
                shift 2
                ;;
            -c | -C | --clean)
                L_PARA_CLEAN="y"
                shift 1
                ;;
            "")                                               # 当$1为空时，说明参数处理完毕
                break                                         # 跳出循环
                ;;
            * )
                f_exit "unsupport option $1"
                ;;
        esac
    done
}
```

**执行示例：**

- 调用：`./build.sh -p retimer target1`
- 执行时：`$1="-p"`, `$2="retimer"`, `$3="target1"`
- 处理后：`$1="target1"`, `$2=""`（为下次循环准备）

**对于GCC编译器参数的追加效果示例**

- 第一次：`-d DEBUG` → `L_PARA_GCC_CFLAG="-DDEBUG "`
- 第二次：`-d VERBOSE` → `L_PARA_GCC_CFLAG="-DDEBUG -DVERBOSE "`
意思是在 `build.sh` 使用时多次使用 `-d` 参数会直接追加，而不是覆盖原有的值

**shift命令**
假设调用是 `./build.sh -p retimer -t app -d DEBUG`，在这个状态下 `$1="-p", $2="retimer", $3="-t", $4="app", $5="-d", $6="DEBUG"`
第一次的循环时，会处理 `-p retimer`，匹配完 -p 的分支后，执行 `shift 2`，执行完后的状态变为 `$1="-t", $2="app1", $3="-d", $4="DEBUG"`

### 工具链的配置

主要涉及Andes工具链的准备，例如
- 检查工具链的MD5值判断是否需要重新解压
- 自动解压工具链tar包
- 设置交叉编译器前缀为 `riscv32-elf-`

#### f_prepare_toolchain_andes

准备Andes工具链

```Shell
f_prepare_toolchain_andes()  
{  
 L_toolchain_root_dir=${L_DIR_ROOT}/toolchain           # step1：设置工具链根目录  
 L_toolchain_name=andes_n25                             # step2：设置工具链名称  
 L_toolchain_dir=${L_toolchain_root_dir}/${L_toolchain_name}  # step3：设置工具链目录  
 L_toolchain_tar_file=${L_toolchain_root_dir}/${L_toolchain_name}.tar.xz  # step4：设置压缩文件路径  
 L_toolchain_md5_file=${L_toolchain_root_dir}/md5sum_${L_toolchain_name}.txt  # step5：设置MD5文件路径  
​  
 L_toolchain_renew_flag=1                               # step6：默认需要更新标志  
 if [ -e ${L_toolchain_md5_file} ] && [ -d ${L_toolchain_dir} ]; then  # step7：检查文件和目录是否存在  
	 L_toolchain_md5_new=$(md5sum ${L_toolchain_tar_file} | awk '{print $1}')  # step8：计算新的MD5值  
	 L_toolchain_md5_old=$(cat ${L_toolchain_md5_file}) # step9：读取旧的MD5值  
	 if [ ${L_toolchain_md5_old} = ${L_toolchain_md5_new} ]; then  # step10：比较MD5值  
		 L_toolchain_renew_flag=0                      # step11：相同则不需要更新  
	 fi  
 fi  
​  
 if [ ${L_toolchain_renew_flag} == "1" ]; then         # step12：检查是否需要更新  
	 rm -rf ${L_toolchain_dir}                         # step13：删除旧目录  
	 tar -xf ${L_toolchain_tar_file} -C ${L_toolchain_root_dir}  # step14：解压新工具链  
	 md5sum ${L_toolchain_tar_file} | awk '{print $1}' > ${L_toolchain_md5_file}  # step15：保存新MD5值  
 fi  
​  
 if [ ! -d ${L_toolchain_dir} ] || [ ! -e ${L_toolchain_md5_file} ]; then  # step16：最终检查  
	 echo "fail to prepare andes toolchain ${L_toolchain_name}"  # step17a：失败提示  
	 exit 1                                             # step18a：退出  
 fi  
​  
 export PATH=${PATH}:${L_toolchain_dir}/bin            # step17b：添加到PATH环境变量  
 L_CROSS_COMPILE=riscv32-elf-                          # step18b：设置交叉编译前缀  
}
```


**说明**

- MD5校验机制确保工具链完整性
    
- 智能更新：只有工具链变化时才重新解压
    
- `awk '{print $1}'`: 提取MD5值的第一列
    
- `tar -xf file -C dir`: 解压到指定目录
    

#### f_prepare_toolchain

准备工具链（根据架构选择）

```Shell
f_prepare_toolchain()  
{  
 if [ "${L_PARA_ARCH}" == "x86" ]; then               # step1：检查架构类型  
	 L_CROSS_COMPILE=""                                # step2a：x86架构不需要交叉编译  
 elif [ "${L_PARA_ARCH}" == "andes" ]; then           # step2b：andes架构  
	 f_prepare_toolchain_andes                         # step3b：准备andes工具链  
 else  
	 f_exit "unsupport arch ${L_PARA_ARCH}"           # step3c：不支持的架构  
 fi  
}
```

**说明**

- 根据不同架构选择对应的工具链
    
- 支持x86本机编译和andes交叉编译
    

### 选项文件解析函数

#### f_parse_option_file_sub

解析选项文件的子函数

```Shell
f_parse_option_file_sub()  
{  
 while true; do                                         # step1：循环处理所有选项  
	 case "$1" in                                       # step2：根据选项类型处理  
		 -d | -D )                                      # step3a：宏定义选项  
			 L_PARA_GCC_CFLAG_O+="-D$2"               # step4a：添加到编译标志  
			 f_exit_if_var_is_empty_or_not_exist $1 $2  
			 shift 2  
			 ;;  
		 -g | -G )                                      # step3b：编译选项  
			 L_PARA_GCC_CFLAG_O+="$2"  
			 f_exit_if_var_is_empty_or_not_exist $1 $2  
			 shift 2  
			 ;;  
		 -l | -L )                                      # step3c：链接选项  
			 L_PARA_GCC_LDFLAG_O+="$2"  
			 f_exit_if_var_is_empty_or_not_exist $1 $2  
			 shift 2  
			 ;;  
		 -m | -M )                                      # step3d：Make变量  
			 export "$2"  
			 L_PARA_MAKE_VAR_O+="$2"  
			 f_exit_if_var_is_empty_or_not_exist $1 $2  
			 shift 2  
			 ;;  
		 "" )                                           # step3e：参数为空  
			 break                                      # step4e：退出循环  
			 ;;  
		 * )                                            # step3f：未知选项  
			 f_exit "unknown option $1"                # step4f：报错退出  
			 ;;  
	 esac  
 done  
}
```

**说明**

- 与主选项解析类似，但用于处理选项文件内容
    
- 变量名带_O后缀表示来自选项文件

#### f_parse_option_file

解析选项文件

```Shell
f_parse_option_file()  
{  
 L_option_list=""                                       # step1：初始化选项列表  
 if [ "${L_PARA_TARGET_OPTION_FILE}" == "" ]; then     # step2：检查选项文件是否存在  
	 return                                             # step3a：不存在则直接返回  
 fi  
 if [ -f $1 ]; then                                    # step3b：检查文件是否存在  
	 dos2unix $1 2>/dev/null                          # step4：转换行结束符  
	 L_option_list=$(cat $1 | tr -s '\n' ' ')         # step5：读取文件内容并转换换行为空格  
 fi  
 eval f_parse_option_file_sub ${L_option_list}         # step6：调用子函数解析选项  
}
```

**说明**

- `dos2unix`: 转换Windows换行符为Unix格式
    
- `tr -s '\n' ' '`: 将换行符替换为空格，-s压缩连续字符
    
- `eval`: 动态执行包含选项的字符串

## 外部库准备函数

### f_prepare_extlib

准备外部库

```Shell
f_prepare_extlib()  
{  
 L_extlib_target=$1                                     # step1：获取外部库目标名称  
 case "${L_extlib_target}" in                          # step2：根据目标类型处理  
	 googletest )                                       # step3a：googletest库  
		 L_extlib_target_dir=${L_DIR_EXTLIB}/$1        # step4a：设置目标目录  
		 f_exit_if_path_not_exist ${L_extlib_target_dir}/build.sh  # step5a：检查构建脚本  
		 if [ ! -e "${L_extlib_target_dir}/output/lib/libgtest.a" ]; then  # step6a：检查库文件是否存在  
			 ${L_extlib_target_dir}/build.sh 1>/dev/null  # step7a：构建库（静默输出）  
		 fi  
		 ;;  
	 * )                                                # step3b：不支持的库  
		 f_exit "unsupport extlib ${L_extlib_target}"  # step4b：报错退出  
		 ;;  
 esac  
}
```

**说明**

- 按需构建外部库，避免重复构建
    
- `1>/dev/null`: 重定向stdout到/dev/null，静默执行
    
- 检查库文件是否已存在，提高构建效率

## 构建配置文件确定函数

### f_build_determin_target_ext_conf_file

确定目标扩展配置文件

```Shell
f_build_determin_target_ext_conf_file()  
{  
 local L_search_dir                                     # step1：声明搜索目录变量  
 L_search_dir=$1                                        # step2：获取搜索目录参数  
 if [ "${L_PARA_TARGET_EXT_CONF_FILE}" == "" ]; then   # step3：检查是否未指定配置文件  
	 L_PARA_TARGET_EXT_CONF_FILE=${L_DIR_ROOT}/utility/build_tool/null.conf  # step4a：使用默认null配置  
 elif [ "${L_PARA_TARGET_EXT_CONF_FILE}" == "new" ]; then  # step4b：用户要求交互选择  
	 f_choice L_PARA_TARGET_EXT_CONF_FILE "select target extend conf file:" "ls ${L_search_dir}/*.conf 2>/dev/null | xargs -n 1 basename"  # step5b：交互选择  
	 L_PARA_TARGET_EXT_CONF_FILE=${L_search_dir}/${L_PARA_TARGET_EXT_CONF_FILE}  # step6b：构建完整路径  
 else                                                   # step4c：用户指定了文件  
	 if [ -f ${L_PARA_TARGET_EXT_CONF_FILE} ]; then    # step5c：检查是否为完整路径  
		 L_PARA_TARGET_EXT_CONF_FILE=$(f_get_abs_path ${L_PARA_TARGET_EXT_CONF_FILE})  # step6c：获取绝对路径  
	 else                                               # step6d：相对路径  
		 L_PARA_TARGET_EXT_CONF_FILE=${L_search_dir}/${L_PARA_TARGET_EXT_CONF_FILE}  # step7d：构建完整路径  
	 fi  
 fi  
 f_exit_if_path_not_exist ${L_PARA_TARGET_EXT_CONF_FILE}  # step7：验证文件存在  
}
```

**说明**

- `xargs -n 1 basename`: 每行一个文件名，提取基础名
    
- `2>/dev/null`: 抑制ls的错误输出
    
- 支持三种模式：默认、交互选择、用户指定
    

### f_build_determin_target_conf_file

确定目标配置文件

```Shell
f_build_determin_target_conf_file()  
{  
 local L_search_dir                                     # step1：声明搜索目录变量  
 L_search_dir=$1                                        # step2：获取搜索目录参数  
 if [ "${L_PARA_TARGET_CONF_FILE}" == "" ]; then       # step3：检查是否未指定配置文件  
	 L_PARA_TARGET_CONF_FILE=${L_search_dir}/${L_PARA_TARGET}.conf  # step4a：使用默认命名规则  
 elif [ "${L_PARA_TARGET_CONF_FILE}" == "new" ]; then  # step4b：用户要求交互选择  
	 f_choice L_PARA_TARGET_CONF_FILE "select target conf file:" "ls ${L_search_dir}/*.conf 2>/dev/null | xargs -n 1 basename"  # step5b：交互选择  
	 L_PARA_TARGET_CONF_FILE=${L_search_dir}/${L_PARA_TARGET_CONF_FILE}  # step6b：构建完整路径  
 else                                                   # step4c：用户指定了文件  
	 if [ -f ${L_PARA_TARGET_CONF_FILE} ]; then        # step5c：检查是否为完整路径  
		 L_PARA_TARGET_CONF_FILE=$(f_get_abs_path ${L_PARA_TARGET_CONF_FILE})  # step6c：获取绝对路径  
	 else                                               # step6d：相对路径  
		 L_PARA_TARGET_CONF_FILE=${L_search_dir}/${L_PARA_TARGET_CONF_FILE}  # step7d：构建完整路径  
	 fi  
 fi  
 f_exit_if_path_not_exist ${L_PARA_TARGET_CONF_FILE}   # step7：验证文件存在  
}
```

**说明**

- 默认使用"目标名.conf"作为配置文件名
    
- 与扩展配置文件处理逻辑相同
    

### f_build_determin_target_ld_file

确定目标链接脚本文件

```Shell
f_build_determin_target_ld_file()  
{  
 local L_search_dir_1                                   # step1：声明第一个搜索目录  
 local L_search_dir_2                                   # step2：声明第二个搜索目录  
 L_search_dir_1=$1                                      # step3：获取第一个搜索目录  
 L_search_dir_2=$2                                      # step4：获取第二个搜索目录  
 if [ "${L_PARA_TARGET_LD_FILE}" == "" ]; then         # step5：检查是否未指定链接文件  
	 L_PARA_TARGET_LD_FILE=${L_search_dir_1}/${L_PARA_TARGET}.ld  # step6a：尝试使用目标名.ld  
	 if [ ! -f ${L_PARA_TARGET_LD_FILE} ]; then        # step7a：检查文件是否存在  
		 L_PARA_TARGET_LD_FILE=${L_search_dir_2}/${L_PARA_PRODUCT}.ld  # step8a：尝试使用产品名.ld  
	 fi  
 elif [ "${L_PARA_TARGET_LD_FILE}" == "new" ]; then    # step6b：用户要求交互选择  
	 echo "ls ${L_search_dir_1}/*.ld 2>/dev/null | xargs -n 1 basename"  # step7b：显示命令（调试用）  
	 f_choice L_PARA_TARGET_LD_FILE "select target ld file:" "ls ${L_search_dir_1}/*.ld 2>/dev/null | xargs -n 1 basename"  # step8b：交互选择  
	 L_PARA_TARGET_LD_FILE=${L_search_dir_1}/${L_PARA_TARGET_LD_FILE}  # step9b：构建完整路径  
 else                                                   # step6c：用户指定了文件  
	 if [ -f ${L_PARA_TARGET_LD_FILE} ]; then          # step7c：检查是否为完整路径  
		 L_PARA_TARGET_LD_FILE=$(f_get_abs_path ${L_PARA_TARGET_LD_FILE})  # step8c：获取绝对路径  
	 else                                               # step8d：相对路径  
		 L_PARA_TARGET_LD_FILE=${L_search_dir}/${L_PARA_TARGET_LD_FILE}  # step9d：构建完整路径（注意这里有个bug，应该是L_search_dir_1）  
	 fi  
 fi  
 f_exit_if_path_not_exist ${L_PARA_TARGET_LD_FILE}     # step9：验证文件存在  
}

```

**说明**

- 双重搜索策略：先找目标名.ld，再找产品名.ld
    
- 链接脚本用于指定程序在内存中的布局
    
- 代码中第9dstep存在bug，应该使用L_search_dir_1
    

### f_build_determin_target_option_file

确定目标选项文件

```Shell
f_build_determin_target_option_file()  
{  
 local L_search_dir                                     # step1：声明搜索目录变量  
 L_search_dir=$1                                        # step2：获取搜索目录参数  
 if [ "${L_PARA_TARGET_OPTION_FILE}" == "" ]; then     # step3：检查是否未指定选项文件  
	 if [ "${L_PARA_TARGET_OPTION_FILE}" == "new" ]; then  # step4a：用户要求交互选择（注意：这个条件永远不会满足，因为上面已经检查为空）  
		 f_choice L_PARA_TARGET_OPTION_FILE "select target option file:" "ls ${L_search_dir}/*.option 2>/dev/null | xargs -n 1 basename"  # step5a：交互选择  
		 L_PARA_TARGET_OPTION_FILE=${L_search_dir}/${L_PARA_TARGET_OPTION_FILE}  # step6a：构建完整路径  
	 else                                               # step4b：用户指定了文件  
		 if [ -f ${L_PARA_TARGET_OPTION_FILE} ]; then  # step5b：检查是否为完整路径  
			 L_PARA_TARGET_OPTION_FILE=$(f_get_abs_path ${L_PARA_TARGET_OPTION_FILE})  # step6b：获取绝对路径  
		 else                                           # step6c：相对路径  
			 L_PARA_TARGET_OPTION_FILE=${L_search_dir}/${L_PARA_TARGET_OPTION_FILE}  # step7c：构建完整路径  
		 fi  
	 fi  
	 f_exit_if_path_not_exist ${L_PARA_TARGET_OPTION_FILE}  # step7：验证文件存在  
	 f_parse_option_file ${L_PARA_TARGET_OPTION_FILE}  # step8：解析选项文件  
 else                                                   # step4d：未指定选项文件，使用默认  
	 L_PARA_TARGET_OPTION_FILE=${L_search_dir}/${L_PARA_TARGET}.option  # step5d：构建默认选项文件路径  
	 if [ -f ${L_PARA_TARGET_OPTION_FILE} ]; then      # step6d：检查默认文件是否存在  
		 f_parse_option_file ${L_PARA_TARGET_OPTION_FILE}  # step7d：解析选项文件  
	 else                                               # step7e：默认文件不存在  
		 L_PARA_TARGET_OPTION_FILE=""                  # step8e：清空选项文件变量  
	 fi  
 fi  
}
```

**说明**

- 这个函数有逻辑错误：第4astep的条件永远不会满足
    
- 默认使用"目标名.option"作为选项文件名
    
- 选项文件不是必须的，不存在时不报错

## 主构建函数

### f_build_system

主要的系统构建函数

```Shell
f_build_system()  
{  
 L_class_dir=$1                                         # step1：获取类别目录参数  
 # ---------- to select target if not defined  
 if [ "${L_PARA_TARGET}" == "new" ] && [ "${L_PARA_TARGET}" == "" ]; then  # step2：检查目标选择（逻辑错误：条件永远不满足）  
	 f_choice L_PARA_TARGET "select ${basename ${L_class_dir}}:" "ls -l ${L_class_dir} | grep '^d' | awk '{print \$NF}'"  # step3：交互选择目标  
 fi  
 # ---------- to determin target name and dir  
 f_exit_if_var_is_empty_or_not_exist L_PARA_TARGET ${L_PARA_TARGET}  # step4：检查目标变量不为空  
 L_PARA_TARGET='basename ${L_PARA_TARGET}'             # step5：获取目标基础名（注意：这里应该是$(basename...)）  
 L_target_dir=${L_class_dir}/${L_PARA_TARGET}          # step6：构建目标目录路径  
 f_exit_if_path_not_exist ${L_target_dir}              # step7：验证目标目录存在  
 # ---------- to determin out dir  
 L_app_out_dir=${L_DIR_OUT}/${L_PARA_CLASS}/${L_PARA_TARGET}  # step8：构建输出目录路径  
 mkdir -p ${L_app_out_dir}                             # step9：创建输出目录  
 # ---------- to determin product dir  
 f_exit_if_var_is_empty_or_not_exist L_PARA_PRODUCT ${L_PARA_PRODUCT}  # step10：检查产品变量不为空  
 if [ "${L_PARA_PRODUCT}" == "new" ]; then            # step11：检查是否需要交互选择产品  
	 f_choice L_PARA_PRODUCT "select product:" "ls -l ${L_DIR_SOC} | grep '^d' | awk '{print \$NF}'"  # step12：交互选择产品  
	 L_PARA_PRODUCT='basename ${L_PARA_PRODUCT}'       # step13：获取产品基础名（同样的语法错误）  
 fi  
 L_product_dir=${L_DIR_SOC}/${L_PARA_PRODUCT}          # step14：构建产品目录路径  
 f_exit_if_path_not_exist ${L_product_dir}             # step15：验证产品目录存在  
 # ---------- to determin base_config_file  
 f_build_determin_target_ext_conf_file ${L_target_dir}  # step16：确定扩展配置文件  
 # ---------- to determin target_config_file  
 f_build_determin_target_conf_file ${L_target_dir}     # step17：确定目标配置文件  
 # ---------- to determin ld_file  
 f_build_determin_target_ld_file ${L_target_dir} ${L_product_dir}  # step18：确定链接脚本文件  
 # ---------- to handle option_file  
 f_build_determin_target_option_file ${L_target_dir}   # step19：确定和处理选项文件  
 f_print "L=\"\n"                                      # step20：打印分隔符（可能是打错了）  
 L_compile_tool=gcc                                     # step21：设置默认编译工具  
 f_trace "build start"                                 # step22：输出构建开始信息  
 if [ "${L_PARA_CLASS}" == "test" ]; then             # step23：检查是否为测试构建  
	 if [ "${L_PARA_TARGET}" == "svc_test" ] || [ "${L_PARA_TARGET}" == "bflash_test" ] || [ "${L_PARA_TARGET}" == "prog_test" ] ||  
		[ "${L_PARA_TARGET}" == "demo_test" ]; then    # step24：检查是否为需要googletest的测试  
		 f_prepare_extlib googletest                    # step25：准备googletest库  
		 L_compile_tool="g++"                          # step26：切换到C++编译器  
	 fi  
 fi  
 f_trace "build $*"                                    # step27：输出构建参数  
 f_check_build_para ${L_app_out_dir}                   # step28：检查构建参数变化  
 # ---------- to determin build info file  
 if [ "${L_PARA_BI_FILE}" == "" ]; then               # step29：检查是否指定了构建信息文件  
	 ${L_TOOL_GEN_BUILD_INFO} 0 0 0 > ${L_app_out_dir}/version.h  # step30a：生成版本信息文件  
	 L_PARA_BI_FILE=${L_app_out_dir}/version.h        # step31a：设置构建信息文件路径  
 else                                                   # step30b：使用指定的构建信息文件  
	 f_exit_if_path_not_exist ${L_PARA_BI_FILE}       # step31b：验证文件存在  
	 cp ${L_PARA_BI_FILE} ${L_app_out_dir}/version.h  # step32b：复制文件到输出目录  
 fi  
 # ---------- to export var for makefile  
 if [ "${L_CROSS_COMPILE}" != "" ]; then              # step33：检查是否使用交叉编译  
	 L_PARA_GCC_LDFLAG_O+="-T ${L_PARA_TARGET_LD_FILE}"  # step34：添加链接脚本到链接标志  
 fi  
 export G_DIR_ROOT=${L_DIR_ROOT}                       # step35：导出根目录变量  
 export G_TARGET_DIR=${L_target_dir}                   # step36：导出目标目录变量  
 export G_TARGET_OUT_DIR=${L_app_out_dir}              # step37：导出输出目录变量  
 export G_PRODUCT=${L_PARA_PRODUCT}                    # step38：导出产品变量  
 export G_COMPILE_TOOL=${L_compile_tool}               # step39：导出编译工具变量  
 export G_GCC_CFLAG="${L_PARA_GCC_CFLAG}${L_PARA_GCC_CFLAG_O}"  # step40：导出编译标志  
 export G_GCC_LDFLAG="${L_PARA_GCC_LDFLAG}${L_PARA_GCC_LDFLAG_O}"  # step41：导出链接标志  
 export G_CROSS_COMPILE=${L_CROSS_COMPILE}             # step42：导出交叉编译前缀  
 export G_EXTEND_CONF_FILE=${L_PARA_TARGET_EXT_CONF_FILE}  # step43：导出扩展配置文件  
 export G_TARGET_CONF_FILE=${L_PARA_TARGET_CONF_FILE}  # step44：导出目标配置文件  
 export G_BI_FILE=${L_app_out_dir}/version.h           # step45：导出构建信息文件  
 f_show_build_cmd                                       # step46：显示构建命令信息  
 # ---------- to create .config, autoconf.h, version.h  
 f_trace "generate file"                               # step47：输出生成文件信息  
 make -C ${L_DIR_SYSTEM} generate_file -s              # step48：执行make生成配置文件  
 f_trace "generate file done"                          # step49：输出生成文件完成信息  
 # ---------- to build target  
 f_trace "build ${L_PARA_CLASS} ${L_PARA_TARGET}"     # step50：输出构建目标信息  
 make -C ${L_DIR_SYSTEM} -s                            # step51：执行主构建命令  
 f_trace "build done"                                  # step52：输出构建完成信息  
}
```

**说明**

- 这是整个脚本的核心函数，协调所有构建step
    
- 包含多个语法错误和逻辑错误需要修复
    
- `-s`: make的静默模式，减少输出信息
    

## 清理和检查函数

### f_clean_sub

清理子目录函数

```Shell
f_clean_sub()  
{  
 f_clean_sub ${L_out_dir}                              # step1：递归调用自身（这里有错误，应该传入$1）  
}
```


**说明**

- 这个函数实现有误，会导致无限递归
    
- 应该实际执行清理操作，如rm -rf $1
    

### f_check_build_para

检查构建参数是否变化

```Shell
f_check_build_para()  
{  
 local L_build_para_curr                               # step1：声明当前参数变量  
 local L_build_para_last                               # step2：声明上次参数变量  
 L_build_para_curr="${L_PARA_CLASS} -> ${L_PARA_TARGET} -a ${L_PARA_ARCH} ${L_PARA_GCC_CFLAG}${L_PARA_GCC_CFLAG_O} ${L_PARA_GCC_LDFLAG}${L_PARA_GCC_LDFLAG_O}"  # step3：构建当前参数字符串  
 if [ "${L_PARA_PRODUCT}" != "" ]; then               # step4：检查产品参数是否存在  
	 L_build_para_curr+=" -p ${L_PARA_PRODUCT}"       # step5：添加产品参数到字符串  
 fi  
 L_LAST_BUILD_PARA_FILE=$1/last_build_para            # step6：设置参数文件路径  
 if [ -f ${L_LAST_BUILD_PARA_FILE} ]; then            # step7：检查参数文件是否存在  
	 L_build_para_last='cat ${L_LAST_BUILD_PARA_FILE}' # step8：读取上次构建参数（语法错误，应该是$()）  
 fi  
 if [ "${L_build_para_curr}" != "${L_build_para_last}" ]; then  # step9：比较参数是否相同  
	 rm -rf $1/*                                       # step10a：清理输出目录  
	 echo "${L_build_para_curr}" > ${L_LAST_BUILD_PARA_FILE}  # step11a：保存新参数  
 fi  
}
```


**说明**

- 通过比较构建参数决定是否需要完全重新构建
    
- 参数变化时清理输出目录，确保构建一致性
    
- 第8步有语法错误，应该使用$(cat ...)
    

### f_show_build_cmd

显示构建命令和参数

```Shell
f_show_build_cmd()  
{  
 local L_cmd_option                                     # step1：声明命令选项变量  
 f_trace "parameter:"                                   # step2：输出参数标题  
 f_trace "L_PARA_CLASS:              ${L_PARA_CLASS}"  # step3：输出构建类别  
 f_trace "L_PARA_PRODUCT:            ${L_PARA_PRODUCT}"  # step4：输出产品信息  
 f_trace "L_PARA_TARGET:             ${L_PARA_TARGET}"  # step5：输出目标信息  
 f_trace "L_PARA_TARGET_CONF_FILE:   ${L_PARA_TARGET_CONF_FILE}"  # step6：输出配置文件  
 f_trace "L_PARA_TARGET_EXT_CONF_FILE: ${L_PARA_TARGET_EXT_CONF_FILE}"  # step7：输出扩展配置文件  
 f_trace "L_PARA_TARGET_LD_FILE:     ${L_PARA_TARGET_LD_FILE}"  # step8：输出链接脚本文件  
 f_trace "L_PARA_TARGET_OPTION_FILE: ${L_PARA_TARGET_OPTION_FILE}"  # step9：输出选项文件  
 f_trace "L_PARA_BI_FILE:            ${L_PARA_BI_FILE}"  # step10：输出构建信息文件  
 f_trace "L_PARA_GCC_CFLAG:          ${L_PARA_GCC_CFLAG}"  # step11：输出编译标志  
 f_trace "L_PARA_GCC_LDFLAG:         ${L_PARA_GCC_LDFLAG}"  # step12：输出链接标志  
 f_trace "L_PARA_MAKE_VAR:           ${L_PARA_MAKE_VAR}"  # step13：输出Make变量  
 f_trace "L_PARA_ARCH:               ${L_PARA_ARCH}"   # step14：输出架构信息  
 f_trace "\r\n\r\n"                                    # step15：输出分隔符  
 L_cmd_option="${L_PARA_CLASS} -> ${L_PARA_TARGET} -a ${L_PARA_ARCH}"  # step16：构建命令选项字符串  
 if [ "${L_PARA_PRODUCT}" != "" ]; then               # step17：检查产品参数  
	 L_cmd_option+=" -p ${L_PARA_PRODUCT}"             # step18：添加产品参数  
 fi  
 if [ "${L_PARA_TARGET_CONF_FILE}" != "" ]; then      # step19：检查配置文件参数  
	 L_cmd_option+=" -tc ${L_PARA_TARGET_CONF_FILE}"   # step20：添加配置文件参数  
 fi  
 if [ "${L_PARA_TARGET_EXT_CONF_FILE}" != "" ]; then  # step21：检查扩展配置文件参数  
	 L_cmd_option+=" -ec ${L_PARA_TARGET_EXT_CONF_FILE}"  # step22：添加扩展配置文件参数  
 fi  
 if [ "${L_PARA_TARGET_LD_FILE}" != "" ]; then        # step23：检查链接文件参数  
	 L_cmd_option+=" -ld ${L_PARA_TARGET_LD_FILE}"     # step24：添加链接文件参数  
 fi  
 if [ "${L_PARA_TARGET_OPTION_FILE}" != "" ]; then    # step25：检查选项文件参数  
	 L_cmd_option+=" -o ${L_PARA_TARGET_OPTION_FILE}"  # step26：添加选项文件参数  
 fi  
 if [ "${L_PARA_GCC_CFLAG}" != "" ]; then             # step27：检查编译标志  
	 L_cmd_option+=" -g \"${L_PARA_GCC_CFLAG}\""      # step28：添加编译标志参数  
 fi  
 if [ "${L_PARA_GCC_LDFLAG}" != "" ]; then            # step29：检查链接标志  
	 L_cmd_option+=" -l \"${L_PARA_GCC_LDFLAG}\""     # step30：添加链接标志参数  
 fi  
 if [ "${L_PARA_MAKE_VAR}" != "" ]; then              # step31：检查Make变量  
	 L_cmd_option+=" -m ${L_PARA_MAKE_VAR}"            # step32：添加Make变量参数  
 fi  
 f_trace "./${L_SCRIPT_NAME} ${L_cmd_option}\r\n"     # step33：输出完整构建命令  
 echo ${L_cmd_option} > ${L_LAST_BUILD_CMD_FILE}      # step34：保存构建命令到文件  
}
```


**说明**

- 详细输出所有构建参数，便于调试和记录
    
- 重构完整的命令行，便于复现构建
    
- 保存命令到文件供下次无参数调用时使用
    

### f_clean

清理构建输出

```Shell
f_clean()  
{  
 f_clean_sub ${L_out_dir}                              # step1：调用清理子函数  
 return                                                 # step2：返回  
}
```


**说明**

- 简单的清理函数封装
    
- 由于f_clean_sub实现有误，这个函数也无法正常工作

## 主程序流程控制

### 主程序开始部分

```Shell
L_out_dir=${L_DIR_OUT}/${L_PARA_CLASS}                   # step1：设置输出目录路径  
if [ "${L_PARA_CLASS}" == "boot" ]; then                 # step2：检查是否为boot构建  
 if [ "${L_PARA_TARGET}" != "" ]; then                # step3：检查是否指定了目标  
	 L_target_name='basename ${L_PARA_TARGET}'         # step4：获取目标基础名（语法错误）  
	 L_out_dir=${L_out_dir}/${L_target_name}           # step5：更新输出目录路径  
 fi  
 f_clean_sub ${L_out_dir}                              # step6：清理输出目录  
 return                                                 # step7：返回  
fi  
```
                                                 

### 主程序初始化部分

```Shell
set -e                                                 # step0：启用错误时退出模式
# ---------- main process ----------  
L_PREFIX=build                                            # step1：设置输出前缀  
if [ "${L_PREFIX}" != "" ]; then                         # step2：检查前缀是否非空  
 L_PREFIX="[${L_PREFIX}]"                             # step3：格式化前缀  
fi  
f_determin_dir $0                                         # step4：确定脚本目录  
# ---------- to define the already existed path  
L_DIR_ROOT=${L_SCRIPT_LOCATED_DIR}                       # step5：设置根目录  
L_DIR_SW=${L_DIR_ROOT}/sw                                # step6：设置软件目录  
L_DIR_SYSTEM=${L_DIR_SW}/system                          # step7：设置系统目录  
L_DIR_BOOT=${L_DIR_SW}/boot                              # step8：设置启动目录  
L_DIR_APP=${L_DIR_SYSTEM}/app                            # step9：设置应用程序目录  
L_DIR_TEST=${L_DIR_SYSTEM}/test                          # step10：设置测试目录  
L_DIR_DEMO=${L_DIR_SYSTEM}/demo                          # step11：设置演示目录  
L_DIR_SOC=${L_DIR_SYSTEM}/soc                            # step12：设置SOC目录  
L_DIR_EXTLIB=${L_DIR_SW}/extlib                          # step13：设置外部库目录  
L_DIR_OUT=${L_DIR_ROOT}/output                           # step14：设置输出目录  
L_TOOL_GEN_BUILD_INFO=${L_DIR_ROOT}/utility/build_tool/gen_build_info.py  # step15：设置构建信息生成工具路径
```


**说明**

- `set -e`: bash选项，任何命令返回非零退出码时立即退出脚本
    
- 定义了完整的目录结构，为后续构建提供路径基础
    

### 帮助选项处理

```Shell
# ---------- to handle in high priority for option -h  
for L_op_item in $@                                       # step1：遍历所有命令行参数  
do  
 if [ ${L_op_item} == "-h" ] || [ ${L_op_item} == "--help" ]; then  # step2：检查帮助选项  
	 f_help                                            # step3：显示帮助信息  
	 exit 0                                            # step4：正常退出  
 fi  
done
```

**说明**

- 优先处理帮助选项，无论其在命令行中的位置
    
- 显示帮助后立即退出，不执行后续构建 

### 全局变量定义

```Shell
# ---------- to define file global var  
L_CROSS_COMPILE=""                                        # step1：交叉编译前缀  
L_PARA_CLASS=""                                           # step2：构建类别  
L_PARA_PRODUCT="retimer"                                  # step3：默认产品名  
L_PARA_TARGET=""                                          # step4：构建目标  
L_PARA_TARGET_EXT_CONF_FILE=""                           # step5：扩展配置文件  
L_PARA_TARGET_CONF_FILE=""                               # step6：目标配置文件  
L_PARA_TARGET_LD_FILE=""                                 # step7：链接脚本文件  
L_PARA_TARGET_OPTION_FILE=""                             # step8：选项文件  
# from -g, -g, -ld  
L_PARA_GCC_CFLAG_O=""                                    # step9：来自选项的编译标志  
# from option_file, gtest  
L_PARA_GCC_LDFLAG_O=""                                   # step10：来自选项的链接标志  
# from option_file, gtest, -ld  
L_PARA_MAKE_VAR_O=""                                     # step11：来自选项的Make变量  
# from option_file  
L_PARA_ARCH="andes"                                      # step12：默认架构  
L_PARA_CLEAN="n"                                         # step13：清理标志  
L_PARA_BI_FILE=""                                        # step14：构建信息文件  
L_LAST_BUILD_CMD_FILE=${L_DIR_ROOT}/last_build.cmd       # step15：上次构建命令文件路径
```

**说明**

- 初始化所有构建参数的默认值
    
- 注释说明了某些变量的来源
    
- 默认架构为"andes"，默认产品为"retimer"

### 无参数情况处理

```Shell
# ---------- to use last build cmd if no para provided  
if [[ $# == 0 ]]; then                                   # step1：检查是否没有提供参数  
 if [ -f ${L_LAST_BUILD_CMD_FILE} ]; then            # step2：检查上次构建命令文件是否存在  
	 L_last_build_cmd='cat ${L_LAST_BUILD_CMD_FILE}'  # step3：读取上次构建命令（语法错误）  
 fi  
 if [ "${L_last_build_cmd}" == "" ]; then            # step4：检查命令是否为空  
	 f_exit "no parameter provided"                   # step5：报错退出  
 fi  
 eval set -- ${L_last_build_cmd}                     # step6：设置命令行参数  
fi
```


**说明**

- `$#`: 命令行参数个数
    
- `[[ ]]`: bash扩展的条件测试语法
    
- `eval set --`: 重新设置位置参数
    
- 第3步有语法错误，应该使用$(cat ...)
- 
### 选项解析和清理处理

```Shell
# ---------- to get options  
eval f_parse_option ${L_OPTIONS}                         # step1：解析命令行选项（L_OPTIONS未定义，应该是$@）  
# ---------- to handle in high priority for option -c  
if [ "${L_PARA_CLASS}" == "-c" ] || [ "${L_PARA_CLASS}" == "-C" ] || [ "${L_PARA_CLASS}" == "--clean" ]; then  # step2：检查清理选项  
 L_PARA_CLASS=""                                       # step3：清空类别参数  
 L_PARA_CLEAN="y"                                      # step4：设置清理标志  
fi  
if [ ${L_PARA_CLEAN} == "y" ]; then                     # step5：检查是否需要清理  
 f_clean                                              # step6：执行清理  
 exit 0                                               # step7：正常退出  
fi
```

**说明**

- 第1步有错误，L_OPTIONS变量未定义，应该使用$@
    
- 支持将清理选项作为构建类别参数传入
    

### 工具链准备和参数存储

```Shell
# ---------- to prepare toolchain  
f_prepare_toolchain                                       # step1：准备工具链  
# ---------- to store parameter  
mkdir -p ${L_DIR_OUT}                                    # step2：创建输出目录  
L_parameter="${L_PARA_CLASS} ${L_OPTIONS}"               # step3：构建参数字符串（L_OPTIONS未定义）  
echo ${L_parameter} > ${L_LAST_BUILD_CMD_FILE}          # step4：保存参数到文件
```

**说明**

- 在实际构建前准备交叉编译工具链
    
- 第3步有错误，L_OPTIONS未定义

### 构建执行分派

```Shell
# ---------- to build  
case "${L_PARA_CLASS}" in                               # step1：根据构建类别分派  
 boot | app | test | demo )                           # step2：支持的构建类别  
	 f_build_system ${L_DIR_SYSTEM}/${L_PARA_CLASS}   # step3：调用构建函数  
	 ;;  
 * )                                                  # step4：不支持的类别  
	 f_exit "unsupport class ${L_PARA_CLASS}"        # step5：报错退出  
	 ;;  
esac
```

**说明**

- 支持四种构建类别：boot、app、test、demo
    
- 统一调用f_build_system函数处理

### 最终输出

```Shell
# ---------- to show parameter  
f_show_build_cmd                                         # step1：显示构建命令  
f_trace "success\r\n\r\n"                              # step2：输出成功信息
```

**说明**

- 构建完成后显示所有参数和构建命令
    
- 输出成功信息表示构建完成

