---
tags:
  - "#domain/programming"
  - "#type/reference"
  - "#level/advanced"
  - "#lang/c"
  - "#tech/linux"
  - "#tech/process"
  - "#grain/system-programming"
status: 完成
complexity: 高级
notetype: 技术参考
resource: Linux系统编程手册
related:
  - "[[Linux系统编程 - 文件IO]]"
  - "[[Linux系统编程 - 进程间通信]]"
  - "[[C语言标准库 - stdlib.h详解]]"
created: 2025-11-18
modified: 2025-11-18
---

# Linux系统编程 - 进程管理

## 📋 概述

进程是Linux系统中程序执行的实例。本文涵盖：
- **进程创建** (fork, vfork, clone)
- **程序执行** (exec系列函数)
- **进程终止** (exit, _exit)
- **进程等待** (wait, waitpid)
- **进程标识** (getpid, getppid)
- **进程环境** (环境变量、命令行参数)
- **守护进程** (Daemon)
- **信号** (signal, kill)

---

## 🎯 学习目标

- [ ] 理解进程的概念和生命周期
- [ ] 掌握fork创建子进程的机制
- [ ] 学会使用exec系列函数执行新程序
- [ ] 理解父子进程的关系
- [ ] 掌握僵尸进程和孤儿进程的处理
- [ ] 学会创建守护进程
- [ ] 理解信号机制和信号处理

---

## 📚 核心内容

### 进程概念

**进程**：运行中的程序实例，包含：
- 程序代码（文本段）
- 当前活动（程序计数器、寄存器值）
- 进程栈（临时数据，如函数参数、局部变量）
- 数据段（全局变量）
- 堆（动态分配的内存）

**进程ID (PID)**：
- 每个进程有唯一的非负整数标识
- PID 0：调度进程（交换进程）
- PID 1：init进程（所有进程的祖先）

---

## 🔧 函数详解

### 一、进程标识

#### getpid() / getppid() ⭐⭐⭐⭐

```c
#include <unistd.h>
pid_t getpid(void);   // 获取当前进程ID
pid_t getppid(void);  // 获取父进程ID
```

**示例**：

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    printf("当前进程ID: %d\n", getpid());
    printf("父进程ID: %d\n", getppid());

    return 0;
}
```

---

### 二、进程创建

#### fork() - 创建子进程 ⭐⭐⭐⭐⭐

```c
#include <unistd.h>
pid_t fork(void);
```

**功能**：创建一个新进程（子进程），它是当前进程（父进程）的副本。

**返回值**：
- **父进程中**：返回子进程的PID（>0）
- **子进程中**：返回0
- **失败**：返回-1

**⚠️ 重要特性**：
1. 子进程是父进程的副本（代码、数据、堆、栈）
2. 子进程有独立的地址空间（采用写时复制COW技术）
3. 父子进程并发执行，执行顺序不确定
4. fork后文件描述符被继承且共享文件偏移

**基本示例**：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid;

    printf("程序开始，当前PID: %d\n", getpid());

    pid = fork();

    if (pid < 0) {
        // fork失败
        perror("fork失败");
        return 1;
    } else if (pid == 0) {
        // 子进程
        printf("子进程: PID=%d, 父PID=%d\n", getpid(), getppid());
    } else {
        // 父进程
        printf("父进程: PID=%d, 子PID=%d\n", getpid(), pid);
    }

    printf("进程%d结束\n", getpid());

    return 0;
}
```

**输出示例**：
```
程序开始，当前PID: 12345
父进程: PID=12345, 子PID=12346
进程12345结束
子进程: PID=12346, 父PID=12345
进程12346结束
```

**fork的典型用法**：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    }

    if (pid == 0) {
        // 子进程执行的代码
        printf("子进程开始工作\n");
        sleep(2);
        printf("子进程完成工作\n");
        return 0;
    } else {
        // 父进程执行的代码
        printf("父进程等待子进程\n");
        wait(NULL);  // 等待子进程结束
        printf("父进程继续工作\n");
        return 0;
    }
}
```

**多进程示例**：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int n = 3;

    printf("创建%d个子进程\n", n);

    for (int i = 0; i < n; i++) {
        pid_t pid = fork();

        if (pid < 0) {
            perror("fork");
            return 1;
        }

        if (pid == 0) {
            // 子进程
            printf("子进程%d: PID=%d\n", i + 1, getpid());
            sleep(i + 1);
            printf("子进程%d完成\n", i + 1);
            return 0;  // 子进程退出
        }
    }

    // 父进程等待所有子进程
    for (int i = 0; i < n; i++) {
        wait(NULL);
    }

    printf("所有子进程已结束\n");
    return 0;
}
```

**fork的COW (Copy-On-Write) 机制**：

```c
#include <stdio.h>
#include <unistd.h>

int global_var = 10;

int main() {
    int local_var = 20;

    printf("fork前: global=%d, local=%d\n", global_var, local_var);

    pid_t pid = fork();

    if (pid == 0) {
        // 子进程修改变量（触发COW，创建独立副本）
        global_var = 100;
        local_var = 200;
        printf("子进程: global=%d, local=%d\n", global_var, local_var);
    } else {
        sleep(1);  // 确保子进程先执行
        // 父进程的变量不受影响
        printf("父进程: global=%d, local=%d\n", global_var, local_var);
    }

    return 0;
}
```

---

### 三、程序执行

#### exec系列函数 ⭐⭐⭐⭐⭐

```c
#include <unistd.h>

int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execle(const char *path, const char *arg, ..., char *const envp[]);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execve(const char *path, char *const argv[], char *const envp[]);
```

**功能**：用新程序替换当前进程的映像。

**⚠️ 重要特性**：
- exec成功后，不会返回（当前程序被完全替换）
- exec失败才返回-1
- 进程ID不变
- 打开的文件描述符保持打开（除非设置了FD_CLOEXEC）

**命名规则**：
- `l`：参数列表（list）
- `v`：参数数组（vector）
- `p`：搜索PATH环境变量
- `e`：指定环境变量

**execl() 示例**：

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    printf("执行ls命令:\n");

    // 执行 /bin/ls -l -a
    execl("/bin/ls", "ls", "-l", "-a", NULL);

    // 如果execl成功，下面的代码不会执行
    perror("execl失败");
    return 1;
}
```

**execlp() 示例**：

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    // 搜索PATH中的ls命令
    execlp("ls", "ls", "-l", NULL);

    perror("execlp失败");
    return 1;
}
```

**execv() 示例**：

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    char *args[] = {"ls", "-l", "-a", NULL};

    execv("/bin/ls", args);

    perror("execv失败");
    return 1;
}
```

**fork + exec 典型模式**：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    }

    if (pid == 0) {
        // 子进程：执行新程序
        printf("子进程：准备执行ls\n");
        execlp("ls", "ls", "-l", NULL);

        // 如果exec失败才会执行到这里
        perror("exec失败");
        return 1;
    } else {
        // 父进程：等待子进程
        printf("父进程：等待子进程执行ls\n");
        wait(NULL);
        printf("父进程：子进程已结束\n");
    }

    return 0;
}
```

**实现简单shell**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_LINE 1024
#define MAX_ARGS 64

int main() {
    char line[MAX_LINE];
    char *args[MAX_ARGS];

    while (1) {
        printf("myshell> ");
        fflush(stdout);

        if (fgets(line, sizeof(line), stdin) == NULL) {
            break;
        }

        // 去除换行符
        line[strcspn(line, "\n")] = 0;

        // 解析命令
        int argc = 0;
        char *token = strtok(line, " \t");
        while (token != NULL && argc < MAX_ARGS - 1) {
            args[argc++] = token;
            token = strtok(NULL, " \t");
        }
        args[argc] = NULL;

        if (argc == 0) continue;

        // 内置命令：exit
        if (strcmp(args[0], "exit") == 0) {
            break;
        }

        // 内置命令：cd
        if (strcmp(args[0], "cd") == 0) {
            if (argc > 1) {
                if (chdir(args[1]) != 0) {
                    perror("cd");
                }
            }
            continue;
        }

        // 执行外部命令
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            continue;
        }

        if (pid == 0) {
            // 子进程
            if (execvp(args[0], args) == -1) {
                perror(args[0]);
                exit(1);
            }
        } else {
            // 父进程
            wait(NULL);
        }
    }

    printf("Shell退出\n");
    return 0;
}
```

---

### 四、进程等待

#### wait() / waitpid() ⭐⭐⭐⭐⭐

```c
#include <sys/wait.h>

pid_t wait(int *status);
pid_t waitpid(pid_t pid, int *status, int options);
```

**功能**：等待子进程结束并获取其终止状态。

**wait() 参数**：
- `status`：存储子进程退出状态（可以为NULL）

**waitpid() 参数**：
- `pid`：
  - `> 0`：等待指定PID的子进程
  - `0`：等待同组的任一子进程
  - `-1`：等待任一子进程（等同wait）
  - `< -1`：等待进程组ID等于pid绝对值的任一子进程
- `status`：存储退出状态
- `options`：
  - `0`：阻塞等待
  - `WNOHANG`：非阻塞，没有子进程结束立即返回0
  - `WUNTRACED`：报告已停止的子进程

**返回值**：
- 成功：已结束子进程的PID
- 失败：-1
- WNOHANG且无子进程结束：0

**状态宏**：

```c
WIFEXITED(status)    // 子进程正常退出，返回true
WEXITSTATUS(status)  // 获取退出状态码

WIFSIGNALED(status)  // 子进程被信号终止，返回true
WTERMSIG(status)     // 获取终止信号编号

WIFSTOPPED(status)   // 子进程被停止，返回true
WSTOPSIG(status)     // 获取停止信号编号
```

**wait() 示例**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 子进程
        printf("子进程开始\n");
        sleep(2);
        printf("子进程结束\n");
        exit(42);  // 返回状态码42
    } else {
        // 父进程
        int status;
        printf("父进程等待子进程\n");

        pid_t child_pid = wait(&status);

        if (WIFEXITED(status)) {
            printf("子进程%d正常退出，状态码=%d\n",
                   child_pid, WEXITSTATUS(status));
        }
    }

    return 0;
}
```

**waitpid() 示例 - 非阻塞等待**：

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 子进程工作3秒
        sleep(3);
        exit(0);
    } else {
        // 父进程每秒检查一次
        int status;
        pid_t result;

        while (1) {
            result = waitpid(pid, &status, WNOHANG);

            if (result == 0) {
                // 子进程还在运行
                printf("子进程还在运行...\n");
                sleep(1);
            } else if (result == pid) {
                // 子进程已结束
                printf("子进程已结束\n");
                break;
            } else {
                perror("waitpid");
                break;
            }
        }
    }

    return 0;
}
```

**等待多个子进程**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int n = 5;

    // 创建n个子进程
    for (int i = 0; i < n; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            printf("子进程%d (PID=%d) 开始\n", i, getpid());
            sleep(rand() % 5 + 1);
            printf("子进程%d 结束\n", i);
            exit(i);
        }
    }

    // 等待所有子进程
    pid_t pid;
    int status;

    while ((pid = wait(&status)) > 0) {
        if (WIFEXITED(status)) {
            printf("进程%d退出，状态码=%d\n", pid, WEXITSTATUS(status));
        }
    }

    printf("所有子进程已结束\n");
    return 0;
}
```

---

### 五、进程终止

#### exit() vs _exit() ⭐⭐⭐⭐

```c
#include <stdlib.h>
void exit(int status);

#include <unistd.h>
void _exit(int status);
```

**区别**：

| 特性 | exit() | _exit() |
|------|--------|---------|
| 头文件 | stdlib.h | unistd.h |
| 调用atexit | ✅ 是 | ❌ 否 |
| 刷新缓冲区 | ✅ 是 | ❌ 否 |
| 关闭流 | ✅ 是 | ❌ 否 |
| 用途 | 正常退出 | fork子进程快速退出 |

**示例**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void cleanup() {
    printf("清理函数被调用\n");
}

int main() {
    atexit(cleanup);

    printf("使用exit()退出：");
    // exit(0);  // 会调用cleanup，会刷新缓冲区

    printf("使用_exit()退出：");
    _exit(0);  // 不会调用cleanup，不会刷新缓冲区（看不到这行输出）
}
```

**fork后在子进程中应使用_exit()**：

```c
pid_t pid = fork();

if (pid == 0) {
    // 子进程
    // 执行工作...

    _exit(0);  // 推荐：不会刷新父进程的缓冲区
    // exit(0); // 不推荐：可能导致父子进程的缓冲区被刷新两次
}
```

---

### 六、僵尸进程和孤儿进程

#### 僵尸进程 (Zombie Process)

**定义**：子进程已终止，但父进程还未调用wait/waitpid回收其资源。

**危害**：
- 占用进程表项
- 浪费系统资源
- 达到最大进程数限制后无法创建新进程

**产生僵尸进程**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("子进程退出\n");
        exit(0);
    } else {
        printf("父进程睡眠（不调用wait）\n");
        sleep(30);  // 这段时间子进程是僵尸进程
        // 使用 ps aux | grep Z 可以看到僵尸进程
    }

    return 0;
}
```

**避免僵尸进程**：

方法1：父进程调用wait/waitpid

```c
pid_t pid = fork();
if (pid == 0) {
    exit(0);
} else {
    wait(NULL);  // 回收子进程
}
```

方法2：忽略SIGCHLD信号

```c
#include <signal.h>

signal(SIGCHLD, SIG_IGN);  // 子进程退出时自动回收

pid_t pid = fork();
if (pid == 0) {
    exit(0);
}
// 不需要wait
```

方法3：捕获SIGCHLD信号

```c
#include <signal.h>
#include <sys/wait.h>

void sigchld_handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0);  // 回收所有已结束的子进程
}

int main() {
    signal(SIGCHLD, sigchld_handler);

    // 创建子进程...
}
```

#### 孤儿进程 (Orphan Process)

**定义**：父进程先于子进程结束，子进程被init进程(PID=1)收养。

**特点**：
- 不会造成资源泄漏（init会自动回收）
- 不是问题，是正常现象

**示例**：

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 子进程
        sleep(2);
        printf("子进程：我的父进程PID=%d\n", getppid());  // 将是1（init）
    } else {
        // 父进程立即退出
        printf("父进程退出\n");
    }

    return 0;
}
```

---

### 七、守护进程 (Daemon)

**守护进程**：在后台运行的特殊进程，不依附于任何终端。

**特点**：
- 生命周期长（通常从系统启动运行到关闭）
- 在后台运行
- 没有控制终端
- 父进程通常是init

**创建守护进程的步骤**：

1. fork创建子进程，父进程退出
2. 子进程调用setsid()创建新会话
3. 再次fork，父进程退出（防止获取控制终端）
4. 改变工作目录到根目录
5. 重置文件权限掩码
6. 关闭不需要的文件描述符

**完整示例**：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <syslog.h>

void daemonize() {
    pid_t pid;

    // 1. fork并退出父进程
    pid = fork();
    if (pid < 0) {
        exit(1);
    }
    if (pid > 0) {
        exit(0);  // 父进程退出
    }

    // 2. 创建新会话
    if (setsid() < 0) {
        exit(1);
    }

    // 3. 再次fork
    pid = fork();
    if (pid < 0) {
        exit(1);
    }
    if (pid > 0) {
        exit(0);  // 第一个子进程退出
    }

    // 4. 改变工作目录
    chdir("/");

    // 5. 重置文件权限掩码
    umask(0);

    // 6. 关闭文件描述符
    for (int fd = 0; fd < sysconf(_SC_OPEN_MAX); fd++) {
        close(fd);
    }

    // 7. 重定向标准输入输出到/dev/null
    int fd = open("/dev/null", O_RDWR);
    dup2(fd, STDIN_FILENO);
    dup2(fd, STDOUT_FILENO);
    dup2(fd, STDERR_FILENO);
    if (fd > STDERR_FILENO) {
        close(fd);
    }
}

int main() {
    daemonize();

    // 使用syslog记录日志
    openlog("mydaemon", LOG_PID, LOG_DAEMON);
    syslog(LOG_INFO, "守护进程启动");

    // 守护进程的工作循环
    while (1) {
        syslog(LOG_INFO, "守护进程运行中");
        sleep(60);
    }

    closelog();
    return 0;
}
```

**查看守护进程**：

```bash
ps aux | grep mydaemon
# 或
ps -ef | grep mydaemon
```

---

### 八、信号基础

#### signal() - 信号处理 ⭐⭐⭐⭐

```c
#include <signal.h>
typedef void (*sighandler_t)(int);
sighandler_t signal(int signum, sighandler_t handler);
```

**功能**：设置信号处理函数。

**handler参数**：
- `SIG_DFL`：默认处理
- `SIG_IGN`：忽略信号
- 自定义函数指针

**常见信号**：

| 信号 | 值 | 默认行为 | 描述 |
|------|-----|----------|------|
| SIGHUP | 1 | 终止 | 终端挂起 |
| SIGINT | 2 | 终止 | 中断(Ctrl+C) |
| SIGQUIT | 3 | 终止+core | 退出(Ctrl+\\) |
| SIGKILL | 9 | 终止 | 强制杀死（不可捕获） |
| SIGSEGV | 11 | 终止+core | 段错误 |
| SIGTERM | 15 | 终止 | 终止信号 |
| SIGCHLD | 17 | 忽略 | 子进程状态改变 |
| SIGSTOP | 19 | 停止 | 停止进程（不可捕获） |
| SIGCONT | 18 | 继续 | 继续进程 |

**示例 - 捕获Ctrl+C**：

```c
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void sigint_handler(int sig) {
    printf("\n捕获到信号%d (SIGINT)\n", sig);
    printf("按Ctrl+C无法退出，使用Ctrl+\\ 或 kill命令\n");
}

int main() {
    signal(SIGINT, sigint_handler);

    printf("程序运行中，按Ctrl+C测试\n");

    while (1) {
        printf("工作中...\n");
        sleep(2);
    }

    return 0;
}
```

#### kill() - 发送信号 ⭐⭐⭐⭐

```c
#include <signal.h>
int kill(pid_t pid, int sig);
```

**功能**：向进程发送信号。

**pid参数**：
- `> 0`：发送给指定PID的进程
- `0`：发送给同进程组的所有进程
- `-1`：发送给所有有权限的进程
- `< -1`：发送给进程组ID等于|pid|的所有进程

**示例**：

```c
#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 子进程
        printf("子进程等待信号\n");
        while (1) {
            sleep(1);
        }
    } else {
        // 父进程
        sleep(2);
        printf("父进程发送SIGTERM给子进程\n");
        kill(pid, SIGTERM);

        wait(NULL);
        printf("子进程已终止\n");
    }

    return 0;
}
```

---

## 📝 实战示例

### 示例1：并行执行任务

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

void do_task(int id, int seconds) {
    printf("任务%d开始 (PID=%d)\n", id, getpid());
    sleep(seconds);
    printf("任务%d完成\n", id);
}

int main() {
    int tasks[] = {3, 2, 4, 1, 5};  // 任务耗时(秒)
    int n = sizeof(tasks) / sizeof(tasks[0]);

    time_t start = time(NULL);

    // 创建子进程执行任务
    for (int i = 0; i < n; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            do_task(i + 1, tasks[i]);
            exit(0);
        }
    }

    // 等待所有任务完成
    for (int i = 0; i < n; i++) {
        wait(NULL);
    }

    time_t end = time(NULL);
    printf("所有任务完成，总耗时: %ld秒\n", (long)(end - start));
    // 并行执行，总耗时约等于最长任务的时间(5秒)

    return 0;
}
```

### 示例2：进程池

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#define WORKER_COUNT 4
#define TASK_COUNT 10

void worker(int id) {
    printf("Worker %d (PID=%d) 启动\n", id, getpid());

    while (1) {
        // 从任务队列获取任务（这里简化处理）
        sleep(rand() % 3 + 1);
        printf("Worker %d 完成一个任务\n", id);
    }
}

int main() {
    pid_t workers[WORKER_COUNT];

    // 创建工作进程池
    for (int i = 0; i < WORKER_COUNT; i++) {
        workers[i] = fork();

        if (workers[i] == 0) {
            worker(i);
            exit(0);
        }
    }

    // 主进程等待一段时间
    sleep(10);

    // 终止所有工作进程
    for (int i = 0; i < WORKER_COUNT; i++) {
        kill(workers[i], SIGTERM);
    }

    // 回收工作进程
    for (int i = 0; i < WORKER_COUNT; i++) {
        wait(NULL);
    }

    printf("进程池关闭\n");
    return 0;
}
```

---

## ⚠️ 常见陷阱

### 1. fork炸弹

```c
// ❌ 危险！会导致系统崩溃
while (1) {
    fork();  // 指数级增长，迅速耗尽系统资源
}
```

### 2. 忘记wait导致僵尸进程

```c
// ❌ 产生僵尸进程
for (int i = 0; i < 100; i++) {
    if (fork() == 0) {
        exit(0);
    }
    // 忘记wait
}
```

### 3. 文件描述符泄漏

```c
// ❌ 每个子进程都继承了fd，但没关闭
int fd = open("file.txt", O_RDONLY);
for (int i = 0; i < 10; i++) {
    if (fork() == 0) {
        // 子进程应该关闭不需要的fd
        // close(fd);
        exec...
    }
}
```

---

## 🔗 相关链接

- [[Linux系统编程 - 文件IO]] - 文件操作
- [[Linux系统编程 - 进程间通信]] - IPC机制
- [[C语言标准库 - stdlib.h详解]] - exit函数
- [[00_C_MOC]] - C语言知识地图

---

## 📚 参考资料

- Advanced Programming in the UNIX Environment (APUE)
- The Linux Programming Interface (TLPI)
- Linux man pages: fork(2), exec(3), wait(2), signal(7)

---

## ✅ 学习检查清单

- [ ] 理解进程的概念和生命周期
- [ ] 掌握fork的工作机制和COW
- [ ] 会使用exec执行新程序
- [ ] 掌握wait/waitpid回收子进程
- [ ] 理解僵尸进程和孤儿进程
- [ ] 能够创建守护进程
- [ ] 掌握基本的信号处理
- [ ] 实现简单的多进程程序

---

*最后更新: 2025-11-18*
