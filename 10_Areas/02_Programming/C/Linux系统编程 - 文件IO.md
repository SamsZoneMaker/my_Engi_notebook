---
tags:
  - "#domain/programming"
  - "#type/reference"
  - "#level/advanced"
  - "#language/c"
  - "#tech/linux"
  - "#tech/syscall"
  - "#grain/system-programming"
status: 完成
complexity: 高级
notetype: 技术参考
resource: Linux系统编程手册
related:
  - "[[C语言标准库 - stdio.h详解]]"
  - "[[Linux系统编程 - 进程管理]]"
  - "[[C语言进阶 - 指针详解]]"
created: 2025-11-18
modified: 2026-01-09  14:47:04
---

# Linux系统编程 - 文件IO

## 📋 概述

Linux系统提供了两套文件IO接口：
1. **标准IO库** (stdio.h) - 带缓冲的高级IO，如fopen, fread, fwrite
2. **系统调用** (unistd.h, fcntl.h) - 无缓冲的底层IO，如open, read, write

本文重点讲解Linux系统调用级别的文件IO操作，包括：
- **文件描述符** (File Descriptors)
- **基本IO操作** (open, close, read, write)
- **文件偏移** (lseek)
- **文件控制** (fcntl, ioctl)
- **文件属性** (stat, chmod, chown)
- **目录操作** (opendir, readdir)
- **高级IO** (select, poll, epoll)

---

## 🎯 学习目标

- [ ] 理解文件描述符的概念
- [ ] 掌握系统调用与标准IO的区别
- [ ] 学会使用open/read/write/close进行文件操作
- [ ] 理解文件偏移和lseek的使用
- [ ] 掌握文件属性和权限管理
- [ ] 了解目录操作和遍历
- [ ] 理解阻塞IO和非阻塞IO
- [ ] 掌握IO多路复用（select/poll/epoll）

---

## 📚 核心内容

### 文件描述符 (File Descriptor)

文件描述符是一个非负整数，用于标识打开的文件。每个进程都有自己的文件描述符表。

**标准文件描述符**：

```c
#define STDIN_FILENO   0  // 标准输入
#define STDOUT_FILENO  1  // 标准输出
#define STDERR_FILENO  2  // 标准错误
```

**特点**：
- 文件描述符从0开始，依次递增
- 每个进程最多可以打开的文件数有限（通过ulimit -n查看）
- 文件描述符在进程间不共享（除了fork后）

---

## 🔧 函数详解

### 一、基本文件操作

#### 1. open() - 打开文件 ⭐⭐⭐⭐⭐

```c
#include <fcntl.h>
int open(const char *pathname, int flags);
int open(const char *pathname, int flags, mode_t mode);
```

**功能**：打开或创建文件，返回文件描述符。

**参数**：
- `pathname`：文件路径
- `flags`：打开标志（必须包含以下之一）
  - `O_RDONLY`：只读
  - `O_WRONLY`：只写
  - `O_RDWR`：读写
- `mode`：文件权限（当创建新文件时需要，八进制表示）

**可选标志**（可通过 | 组合）：
- `O_CREAT`：文件不存在则创建
- `O_EXCL`：与O_CREAT一起使用，文件存在则失败
- `O_TRUNC`：截断文件为0长度
- `O_APPEND`：追加模式，写入总是在末尾
- `O_NONBLOCK`：非阻塞模式
- `O_SYNC`：同步IO，写入立即同步到磁盘

**返回值**：
- 成功：文件描述符（非负整数）
- 失败：-1，并设置errno

**示例**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main() {
    int fd;

    // 1. 只读打开现有文件
    fd = open("test.txt", O_RDONLY);
    if (fd == -1) {
        perror("打开文件失败");
        return 1;
    }
    printf("文件描述符: %d\n", fd);
    close(fd);

    // 2. 创建新文件并写入（权限：rw-r--r--）
    fd = open("new.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("创建文件失败");
        return 1;
    }
    printf("创建文件，fd = %d\n", fd);
    close(fd);

    // 3. 追加模式打开
    fd = open("log.txt", O_WRONLY | O_CREAT | O_APPEND, 0644);
    if (fd == -1) {
        perror("打开日志文件失败");
        return 1;
    }
    close(fd);

    // 4. 独占创建（文件存在则失败）
    fd = open("unique.txt", O_WRONLY | O_CREAT | O_EXCL, 0644);
    if (fd == -1) {
        if (errno == EEXIST) {
            printf("文件已存在\n");
        } else {
            perror("创建失败");
        }
        return 1;
    }
    close(fd);

    return 0;
}
```

**文件权限说明**：

```c
// 权限位（mode参数，八进制）
0400  // 用户可读
0200  // 用户可写
0100  // 用户可执行
0040  // 组可读
0020  // 组可写
0010  // 组可执行
0004  // 其他可读
0002  // 其他可写
0001  // 其他可执行

// 常用组合
0644  // rw-r--r-- (用户读写，组和其他只读)
0755  // rwxr-xr-x (用户全部，组和其他读+执行)
0600  // rw------- (仅用户读写)
```

#### 2. creat() - 创建文件

```c
int creat(const char *pathname, mode_t mode);
```

**功能**：创建新文件（等同于 `open(pathname, O_WRONLY | O_CREAT | O_TRUNC, mode)`）。

**示例**：

```c
int fd = creat("file.txt", 0644);
// 等同于
int fd = open("file.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
```

#### 3. read() - 读取数据 ⭐⭐⭐⭐⭐

```c
#include <unistd.h>
ssize_t read(int fd, void *buf, size_t count);
```

**功能**：从文件描述符读取数据。

**参数**：
- `fd`：文件描述符
- `buf`：数据缓冲区
- `count`：要读取的字节数

**返回值**：
- >0：实际读取的字节数
- 0：文件结束（EOF）
- -1：错误，设置errno

**⚠️ 重要特性**：
- 返回值可能小于count（不是错误，可能是文件剩余字节不足）
- 非阻塞模式下，如果没有数据可读，返回-1且errno=EAGAIN

**示例**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    int fd = open("test.txt", O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    char buffer[1024];
    ssize_t bytes_read;

    // 读取数据
    bytes_read = read(fd, buffer, sizeof(buffer) - 1);

    if (bytes_read == -1) {
        perror("read");
        close(fd);
        return 1;
    }

    if (bytes_read == 0) {
        printf("文件为空\n");
    } else {
        buffer[bytes_read] = '\0';  // 添加终止符
        printf("读取了 %zd 字节:\n%s\n", bytes_read, buffer);
    }

    close(fd);
    return 0;
}
```

**完整读取文件**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

#define BUFFER_SIZE 4096

int main() {
    int fd = open("file.txt", O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    char buffer[BUFFER_SIZE];
    ssize_t bytes_read;
    ssize_t total = 0;

    // 循环读取直到EOF
    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
        // 处理数据（这里直接写到标准输出）
        write(STDOUT_FILENO, buffer, bytes_read);
        total += bytes_read;
    }

    if (bytes_read == -1) {
        perror("read");
        close(fd);
        return 1;
    }

    printf("\n总共读取 %zd 字节\n", total);
    close(fd);
    return 0;
}
```

#### 4. write() - 写入数据 ⭐⭐⭐⭐⭐

```c
ssize_t write(int fd, const void *buf, size_t count);
```

**功能**：向文件描述符写入数据。

**参数**：
- `fd`：文件描述符
- `buf`：数据缓冲区
- `count`：要写入的字节数

**返回值**：
- >=0：实际写入的字节数
- -1：错误，设置errno

**⚠️ 注意**：
- 返回值可能小于count（磁盘满、信号中断等）
- 需要循环写入确保所有数据写完

**示例**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main() {
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    const char *text = "Hello, Linux File I/O!\n";
    ssize_t bytes_written = write(fd, text, strlen(text));

    if (bytes_written == -1) {
        perror("write");
        close(fd);
        return 1;
    }

    printf("写入了 %zd 字节\n", bytes_written);
    close(fd);
    return 0;
}
```

**完整写入函数**：

```c
#include <unistd.h>
#include <errno.h>

// 确保写入所有数据
ssize_t write_all(int fd, const void *buf, size_t count) {
    size_t total_written = 0;
    const char *p = (const char *)buf;

    while (total_written < count) {
        ssize_t written = write(fd, p + total_written, count - total_written);

        if (written == -1) {
            if (errno == EINTR) {
                continue;  // 被信号中断，重试
            }
            return -1;  // 真正的错误
        }

        total_written += written;
    }

    return total_written;
}

int main() {
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    const char *data = "This is important data that must be fully written.";
    if (write_all(fd, data, strlen(data)) == -1) {
        perror("write_all");
        close(fd);
        return 1;
    }

    close(fd);
    return 0;
}
```

#### 5. close() - 关闭文件 ⭐⭐⭐⭐⭐

```c
int close(int fd);
```

**功能**：关闭文件描述符。

**返回值**：
- 0：成功
- -1：失败

**⚠️ 重要**：
- 关闭后文件描述符会被回收，可被重新使用
- 进程结束时，所有文件描述符会自动关闭
- 应该检查close的返回值（某些文件系统可能延迟写入错误）

**示例**：

```c
int fd = open("file.txt", O_RDONLY);
if (fd == -1) {
    perror("open");
    return 1;
}

// 使用文件...

if (close(fd) == -1) {
    perror("close");
    return 1;
}
```

---

### 二、文件偏移和定位

#### lseek() - 文件定位 ⭐⭐⭐⭐

```c
#include <unistd.h>
off_t lseek(int fd, off_t offset, int whence);
```

**功能**：设置文件偏移量（读写位置）。

**参数**：
- `fd`：文件描述符
- `offset`：偏移量（可以是负数）
- `whence`：偏移基准
  - `SEEK_SET`：文件开头
  - `SEEK_CUR`：当前位置
  - `SEEK_END`：文件末尾

**返回值**：
- 成功：新的文件偏移量
- 失败：-1

**示例**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    int fd = open("test.txt", O_RDWR);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    // 1. 移动到文件开头
    lseek(fd, 0, SEEK_SET);

    // 2. 移动到文件末尾
    off_t file_size = lseek(fd, 0, SEEK_END);
    printf("文件大小: %ld 字节\n", (long)file_size);

    // 3. 回到开头
    lseek(fd, 0, SEEK_SET);

    // 4. 向前移动100字节
    lseek(fd, 100, SEEK_CUR);

    // 5. 从末尾向前10字节
    lseek(fd, -10, SEEK_END);

    // 6. 获取当前位置
    off_t current_pos = lseek(fd, 0, SEEK_CUR);
    printf("当前位置: %ld\n", (long)current_pos);

    close(fd);
    return 0;
}
```

**创建空洞文件**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    int fd = open("sparse.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    // 写入数据
    write(fd, "START", 5);

    // 跳过1MB（创建空洞）
    lseek(fd, 1024 * 1024, SEEK_CUR);

    // 在空洞后写入数据
    write(fd, "END", 3);

    close(fd);

    // 文件逻辑大小为1MB+8字节，但实际磁盘占用很小
    printf("空洞文件创建完成\n");

    return 0;
}
```

---

### 三、文件复制示例

**系统调用版本**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

#define BUFFER_SIZE 4096

int copy_file(const char *src, const char *dest) {
    int fd_src, fd_dest;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read, bytes_written;

    // 打开源文件
    fd_src = open(src, O_RDONLY);
    if (fd_src == -1) {
        perror("打开源文件失败");
        return -1;
    }

    // 创建目标文件
    fd_dest = open(dest, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd_dest == -1) {
        perror("创建目标文件失败");
        close(fd_src);
        return -1;
    }

    // 复制数据
    while ((bytes_read = read(fd_src, buffer, sizeof(buffer))) > 0) {
        char *ptr = buffer;
        while (bytes_read > 0) {
            bytes_written = write(fd_dest, ptr, bytes_read);
            if (bytes_written == -1) {
                perror("写入失败");
                close(fd_src);
                close(fd_dest);
                return -1;
            }
            bytes_read -= bytes_written;
            ptr += bytes_written;
        }
    }

    if (bytes_read == -1) {
        perror("读取失败");
        close(fd_src);
        close(fd_dest);
        return -1;
    }

    close(fd_src);
    close(fd_dest);

    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "用法: %s <源文件> <目标文件>\n", argv[0]);
        return 1;
    }

    if (copy_file(argv[1], argv[2]) == 0) {
        printf("文件复制成功\n");
    } else {
        printf("文件复制失败\n");
        return 1;
    }

    return 0;
}
```

---

### 四、文件控制

#### fcntl() - 文件控制 ⭐⭐⭐⭐

```c
#include <fcntl.h>
int fcntl(int fd, int cmd, ... /* arg */);
```

**功能**：对已打开的文件描述符执行各种操作。

**常用命令**：
- `F_GETFL`：获取文件状态标志
- `F_SETFL`：设置文件状态标志
- `F_GETFD`：获取文件描述符标志
- `F_SETFD`：设置文件描述符标志
- `F_DUPFD`：复制文件描述符

**示例 - 设置非阻塞IO**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) {
        perror("fcntl F_GETFL");
        return -1;
    }

    flags |= O_NONBLOCK;

    if (fcntl(fd, F_SETFL, flags) == -1) {
        perror("fcntl F_SETFL");
        return -1;
    }

    return 0;
}

int main() {
    int fd = open("file.txt", O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    // 设置为非阻塞模式
    if (set_nonblocking(fd) == 0) {
        printf("文件描述符已设置为非阻塞模式\n");
    }

    close(fd);
    return 0;
}
```

**示例 - 复制文件描述符**：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    int fd = open("test.txt", O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    // 复制文件描述符（获取>=10的最小可用fd）
    int new_fd = fcntl(fd, F_DUPFD, 10);
    if (new_fd == -1) {
        perror("fcntl F_DUPFD");
        close(fd);
        return 1;
    }

    printf("原fd: %d, 新fd: %d\n", fd, new_fd);

    // 两个fd指向同一个文件
    close(fd);
    close(new_fd);

    return 0;
}
```

---

### 五、文件属性

#### stat() / fstat() / lstat() - 获取文件信息 ⭐⭐⭐⭐

```c
#include <sys/stat.h>
int stat(const char *pathname, struct stat *statbuf);
int fstat(int fd, struct stat *statbuf);
int lstat(const char *pathname, struct stat *statbuf);
```

**功能**：获取文件元数据。

**区别**：
- `stat`：通过路径名获取
- `fstat`：通过文件描述符获取
- `lstat`：对于符号链接，返回链接本身的信息（不是目标文件）

**struct stat 结构**：

```c
struct stat {
    dev_t     st_dev;         // 设备ID
    ino_t     st_ino;         // inode号
    mode_t    st_mode;        // 文件类型和权限
    nlink_t   st_nlink;       // 硬链接数
    uid_t     st_uid;         // 用户ID
    gid_t     st_gid;         // 组ID
    dev_t     st_rdev;        // 特殊文件的设备ID
    off_t     st_size;        // 文件大小（字节）
    blksize_t st_blksize;     // IO块大小
    blkcnt_t  st_blocks;      // 分配的块数
    time_t    st_atime;       // 最后访问时间
    time_t    st_mtime;       // 最后修改时间
    time_t    st_ctime;       // 最后状态改变时间
};
```

**示例**：

```c
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>
#include <pwd.h>
#include <grp.h>

void print_file_info(const char *path) {
    struct stat sb;

    if (stat(path, &sb) == -1) {
        perror("stat");
        return;
    }

    printf("文件: %s\n", path);

    // 文件类型
    printf("文件类型: ");
    if (S_ISREG(sb.st_mode))  printf("普通文件\n");
    else if (S_ISDIR(sb.st_mode))  printf("目录\n");
    else if (S_ISLNK(sb.st_mode))  printf("符号链接\n");
    else if (S_ISCHR(sb.st_mode))  printf("字符设备\n");
    else if (S_ISBLK(sb.st_mode))  printf("块设备\n");
    else if (S_ISFIFO(sb.st_mode)) printf("FIFO\n");
    else if (S_ISSOCK(sb.st_mode)) printf("套接字\n");
    else printf("未知类型\n");

    // 权限
    printf("权限: %o\n", sb.st_mode & 0777);

    // 大小
    printf("大小: %ld 字节\n", (long)sb.st_size);

    // inode
    printf("Inode: %ld\n", (long)sb.st_ino);

    // 链接数
    printf("硬链接数: %ld\n", (long)sb.st_nlink);

    // 所有者
    struct passwd *pw = getpwuid(sb.st_uid);
    struct group *gr = getgrgid(sb.st_gid);
    printf("所有者: %s (UID:%d)\n", pw ? pw->pw_name : "?", sb.st_uid);
    printf("组: %s (GID:%d)\n", gr ? gr->gr_name : "?", sb.st_gid);

    // 时间
    char timebuf[64];
    strftime(timebuf, sizeof(timebuf), "%Y-%m-%d %H:%M:%S",
             localtime(&sb.st_mtime));
    printf("最后修改时间: %s\n", timebuf);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "用法: %s <文件>\n", argv[0]);
        return 1;
    }

    print_file_info(argv[1]);
    return 0;
}
```

**检查文件类型和权限**：

```c
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "用法: %s <文件>\n", argv[0]);
        return 1;
    }

    struct stat sb;
    if (stat(argv[1], &sb) == -1) {
        perror("stat");
        return 1;
    }

    // 检查是否是普通文件
    if (S_ISREG(sb.st_mode)) {
        printf("这是一个普通文件\n");
    }

    // 检查是否是目录
    if (S_ISDIR(sb.st_mode)) {
        printf("这是一个目录\n");
    }

    // 检查权限
    printf("权限检查:\n");
    printf("  所有者可读: %s\n", (sb.st_mode & S_IRUSR) ? "是" : "否");
    printf("  所有者可写: %s\n", (sb.st_mode & S_IWUSR) ? "是" : "否");
    printf("  所有者可执行: %s\n", (sb.st_mode & S_IXUSR) ? "是" : "否");
    printf("  组可读: %s\n", (sb.st_mode & S_IRGRP) ? "是" : "否");
    printf("  其他可读: %s\n", (sb.st_mode & S_IROTH) ? "是" : "否");

    // 检查特殊权限位
    if (sb.st_mode & S_ISUID) printf("设置了SUID位\n");
    if (sb.st_mode & S_ISGID) printf("设置了SGID位\n");
    if (sb.st_mode & S_ISVTX) printf("设置了粘滞位\n");

    return 0;
}
```

#### access() - 检查文件访问权限

```c
#include <unistd.h>
int access(const char *pathname, int mode);
```

**功能**：检查文件是否存在及是否有指定权限。

**mode参数**：
- `F_OK`：文件是否存在
- `R_OK`：是否可读
- `W_OK`：是否可写
- `X_OK`：是否可执行

**返回值**：
- 0：有权限
- -1：无权限或文件不存在

**示例**：

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    const char *file = "test.txt";

    // 检查文件是否存在
    if (access(file, F_OK) == 0) {
        printf("%s 存在\n", file);
    } else {
        printf("%s 不存在\n", file);
        return 1;
    }

    // 检查权限
    if (access(file, R_OK) == 0) {
        printf("可读\n");
    }

    if (access(file, W_OK) == 0) {
        printf("可写\n");
    }

    if (access(file, X_OK) == 0) {
        printf("可执行\n");
    }

    return 0;
}
```

---

### 六、标准IO vs 系统调用

**对比**：

| 特性 | 标准IO (stdio.h) | 系统调用 (unistd.h) |
|------|------------------|---------------------|
| 接口函数 | fopen, fread, fwrite, fclose | open, read, write, close |
| 缓冲 | 有（用户态缓冲） | 无 |
| 效率 | 小量多次读写更高效 | 大块读写更高效 |
| 返回值 | FILE* | 文件描述符(int) |
| 移植性 | 更好（ANSI C） | 差（POSIX） |
| 灵活性 | 较低 | 较高 |
| 格式化IO | 支持（fprintf, fscanf） | 不支持 |

**何时使用系统调用**：
- 需要精确控制IO操作
- 非阻塞IO或异步IO
- 网络编程
- 设备文件操作
- 需要使用文件描述符的高级功能

**何时使用标准IO**：
- 文本文件处理
- 需要格式化输入输出
- 跨平台程序
- 小量频繁读写

---

## 📝 实战示例

### 示例1：实现tail命令

```c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

#define BUFFER_SIZE 4096

void print_last_n_lines(const char *filename, int n) {
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        perror("open");
        return;
    }

    // 获取文件大小
    off_t file_size = lseek(fd, 0, SEEK_END);
    if (file_size == -1) {
        perror("lseek");
        close(fd);
        return;
    }

    // 从文件末尾向前读取
    char buffer[BUFFER_SIZE];
    off_t pos = file_size;
    int newline_count = 0;
    ssize_t bytes_read;

    while (pos > 0 && newline_count < n) {
        // 每次向前读取一块
        off_t read_size = (pos < BUFFER_SIZE) ? pos : BUFFER_SIZE;
        pos -= read_size;

        lseek(fd, pos, SEEK_SET);
        bytes_read = read(fd, buffer, read_size);
        if (bytes_read == -1) {
            perror("read");
            close(fd);
            return;
        }

        // 从后向前统计换行符
        for (ssize_t i = bytes_read - 1; i >= 0; i--) {
            if (buffer[i] == '\n') {
                newline_count++;
                if (newline_count >= n) {
                    pos += i + 1;
                    break;
                }
            }
        }
    }

    // 定位到起始位置并输出
    lseek(fd, pos, SEEK_SET);

    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {
        write(STDOUT_FILENO, buffer, bytes_read);
    }

    close(fd);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "用法: %s -n <行数> <文件>\n", argv[0]);
        return 1;
    }

    int lines = atoi(argv[2]);
    print_last_n_lines(argv[1], lines);

    return 0;
}
```

---

## ⚠️ 常见陷阱

### 1. 忘记检查返回值

```c
// ❌ 危险
int fd = open("file.txt", O_RDONLY);
read(fd, buffer, sizeof(buffer));  // fd可能是-1

// ✅ 正确
int fd = open("file.txt", O_RDONLY);
if (fd == -1) {
    perror("open");
    return -1;
}
```

### 2. 部分读写

```c
// ❌ 错误：假设一次read能读完
char buffer[1000];
read(fd, buffer, 1000);  // 可能只读取了部分数据

// ✅ 正确：循环读取
ssize_t total = 0;
while (total < 1000) {
    ssize_t n = read(fd, buffer + total, 1000 - total);
    if (n <= 0) break;
    total += n;
}
```

### 3. 忘记关闭文件描述符

```c
// ❌ 资源泄漏
for (int i = 0; i < 1000; i++) {
    int fd = open("file.txt", O_RDONLY);
    // ... 使用fd
    // 忘记close(fd)
}

// ✅ 正确
for (int i = 0; i < 1000; i++) {
    int fd = open("file.txt", O_RDONLY);
    // ... 使用fd
    close(fd);
}
```

---

## 🔗 相关链接

- [[C语言标准库 - stdio.h详解]] - 标准IO库
- [[Linux系统编程 - 进程管理]] - 进程相关系统调用
- [[C语言进阶 - 指针详解]] - 指针操作
- [[00_C_MOC]] - C语言知识地图

---

## 📚 参考资料

- The Linux Programming Interface (TLPI)
- Advanced Programming in the UNIX Environment (APUE)
- Linux man pages: open(2), read(2), write(2), stat(2)

---

## ✅ 学习检查清单

- [ ] 理解文件描述符的概念
- [ ] 掌握open/read/write/close基本操作
- [ ] 会使用lseek进行文件定位
- [ ] 理解标准IO与系统调用的区别
- [ ] 掌握文件属性获取（stat）
- [ ] 能够实现文件复制程序
- [ ] 理解阻塞和非阻塞IO
- [ ] 能够正确处理错误和部分读写

---

*最后更新: 2025-11-18*
