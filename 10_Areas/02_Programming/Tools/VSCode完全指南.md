---
tags:
  - "#domain/tools"
  - "#type/reference"
  - "#tech/editor"
  - "#grain/guide"
  - "#level/basic"
aliases:
  - VSCode使用指南
  - Visual Studio Code
create_date: 2025-11-19
notetype: 开发工具指南
---

# VSCode完全指南

Visual Studio Code 是微软推出的开源代码编辑器，以丰富的插件生态系统和灵活的配置能力著称。本指南涵盖VSCode的安装、配置、插件使用和常用快捷键。

## 目录

1. [[#安装与部署]]
2. [[#插件管理]]
3. [[#远程开发配置]]
4. [[#常用插件详解]]
5. [[#快捷键速查]]
6. [[#高级配置]]

---

## 安装与部署

### Windows 绿色版安装

推荐使用绿色版（Portable）以便于跨机器使用和版本控制：

```
下载: VSCode-win32-x64-1.67.2.zip (或最新版本)
解压到目标目录即可使用
```

**优势**：
- 无需管理员权限
- 配置和插件可随文件夹迁移
- 多版本并存

### Linux 安装

```bash
# Debian/Ubuntu
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# 或者下载 .deb/.rpm 包手动安装
```

---

## 插件管理

### 插件目录位置

不同系统的默认插件目录：

| 系统 | 插件路径 |
|------|----------|
| **Windows** | `C:\Users\<username>\.vscode\extensions` |
| **Linux** | `~/.vscode/extensions` |
| **macOS** | `~/.vscode/extensions` |

### 插件迁移

**Windows 和 Linux 插件通用**，可以直接拷贝：

```bash
# 从 Windows 迁移到 Linux
# 1. 打包 Windows 插件
tar -czf vscode-extensions.tar.gz -C "C:\Users\<username>\.vscode\extensions" .

# 2. 在 Linux 上解压
tar -xzf vscode-extensions.tar.gz -C ~/.vscode/extensions/
```

### 推荐插件列表

#### 语言支持
- **C/C++** (Microsoft)
- **Python** (Microsoft)
- **Go** (Go Team at Google)
- **Rust Analyzer**
- **CMake** / **CMake Tools**

#### 远程开发
- **Remote - SSH**：远程服务器开发
- **Remote - Containers**：Docker 容器开发
- **Remote - WSL**：Windows Subsystem for Linux

#### 代码质量
- **ESLint** / **Pylint**：代码检查
- **Prettier**：代码格式化
- **SonarLint**：代码质量分析

#### 版本控制
- **GitLens**：增强 Git 功能
- **Git Graph**：可视化分支图
- **Git History**：文件历史查看

#### 效率工具
- **Bracket Pair Colorizer 2**：括号配对着色
- **Path Intellisense**：路径自动补全
- **Auto Rename Tag**：自动重命名配对标签
- **Todo Tree**：TODO 注释管理

---

## 远程开发配置

### 方法一：Remote-SSH（推荐）

**Remote-SSH** 插件允许直接在 VSCode 中打开远程服务器文件夹，是最流畅的远程开发方案。

#### 配置步骤

**1. 安装插件**

- 打开扩展市场：`Ctrl + Shift + X`
- 搜索 **Remote - SSH** 并安装

**2. 配置 SSH 连接**

按 `Ctrl + Shift + P` 打开命令面板，选择 **Remote-SSH: Open SSH Configuration File**，编辑配置：

```ssh-config
Host baikal-server
    HostName 10.1.3.228
    User zhengquan.lin
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
    ServerAliveInterval 60
```

**3. 连接到服务器**

- 按 `Ctrl + Shift + P`
- 选择 **Remote-SSH: Connect to Host**
- 选择配置好的主机名（如 `baikal-server`）
- 首次连接会提示添加指纹，确认即可

**4. 打开远程文件夹**

连接成功后，VSCode 界面左下角会显示远程主机信息：

- 点击左侧 **Explorer** → **Open Folder**
- 导航到代码目录（如 `/home/zhengquan.lin/projects/firmware`）
- 开始编辑

#### Remote-SSH 优势

✅ **性能优异**：插件和语言服务器运行在远程，本地只负责渲染
✅ **完整体验**：支持终端、调试、Git 等所有功能
✅ **安全可靠**：基于 SSH 协议，支持密钥认证

#### 常见问题

**Q: 连接后提示无法安装 VSCode Server**

A: 可能是服务器磁盘空间不足或网络问题，检查 `~/.vscode-server/` 目录权限。

**Q: 连接速度慢**

A:
- 在 SSH 配置中添加 `Compression yes`
- 配置 `ControlMaster` 复用连接：
```ssh-config
ControlMaster auto
ControlPath ~/.ssh/sockets/%r@%h-%p
ControlPersist 600
```

**Q: 每次都要输入密码**

A: 使用 SSH 密钥对：
```bash
ssh-keygen -t rsa -b 4096
ssh-copy-id user@10.1.3.228
```

### 方法二：手动挂载远程目录（Windows）

使用 **SSHFS + WinFSP** 将远程目录映射为本地网络驱动器。

#### 配置步骤

**1. 安装工具**

从共享路径获取：
```
\\wisewave.local\fs\rd\Engineering\Firmware\Development Environment\tools
```

**2. 映射网络驱动器**

- 右键"此电脑" → "映射网络驱动器"
- 输入路径：
  ```
  \\sshfs\username@10.1.3.228
  ```
- 输入 SSH 用户名和密码
- 映射后可用 VSCode 直接打开

#### 对比 Remote-SSH

| 特性 | Remote-SSH | SSHFS 挂载 |
|------|-----------|-----------|
| **配置复杂度** | 低（一键安装插件） | 中（需要额外工具） |
| **性能** | 优秀 | 较慢（网络IO） |
| **功能完整性** | 完整 | 部分受限 |
| **适用场景** | 日常开发 | 临时访问 |

---

## 常用插件详解

### Markdown PDF

将 Markdown 文档转换为 PDF、HTML 等格式。

#### 使用步骤

1. **安装插件**：在扩展市场搜索 **Markdown PDF**

2. **转换文档**：
   - 打开 Markdown 文件
   - 按 `Ctrl + Shift + P`
   - 选择：`Markdown PDF: Export (pdf)`

3. **输出位置**：PDF 文件会生成在源文件同目录

#### 配置选项

在 `settings.json` 中自定义：

```json
{
  "markdown-pdf.outputDirectory": "./output",
  "markdown-pdf.format": "A4",
  "markdown-pdf.displayHeaderFooter": true,
  "markdown-pdf.headerTemplate": "<div style='font-size:10px;width:100%;text-align:center;'>Document Title</div>",
  "markdown-pdf.footerTemplate": "<div style='font-size:10px;width:100%;text-align:center;'>Page <span class='pageNumber'></span> of <span class='totalPages'></span></div>"
}
```

### C/C++ 插件（Microsoft）

提供 IntelliSense、调试、代码导航等核心功能。

#### 配置 `c_cpp_properties.json`

```json
{
  "configurations": [
    {
      "name": "Linux",
      "includePath": [
        "${workspaceFolder}/**",
        "/usr/include",
        "/usr/local/include"
      ],
      "defines": [],
      "compilerPath": "/usr/bin/gcc",
      "cStandard": "c11",
      "cppStandard": "c++17",
      "intelliSenseMode": "gcc-x64"
    }
  ],
  "version": 4
}
```

#### 调试配置 `launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "C/C++ Debug",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/myapp",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ],
      "preLaunchTask": "build",
      "miDebuggerPath": "/usr/bin/gdb"
    }
  ]
}
```

### GitLens

增强 Git 功能，提供行级别的 Git 信息。

#### 核心功能

- **Blame 注释**：每行代码显示最后修改者和时间
- **文件历史**：可视化查看文件变更历史
- **分支比较**：对比不同分支的差异
- **提交搜索**：按作者、消息、文件搜索提交

#### 常用命令

| 命令 | 功能 |
|------|------|
| `GitLens: Toggle File Blame` | 切换文件 Blame 注释 |
| `GitLens: Show File History` | 查看文件历史 |
| `GitLens: Compare with Branch` | 与分支比较 |
| `GitLens: Search Commits` | 搜索提交 |

---

## 快捷键速查

### 代码编辑类

| 快捷键 | 功能 |
|--------|------|
| `Alt + ↑/↓` | 移动当前行代码 |
| `Shift + Alt + ↑/↓` | 复制当前行到上/下行 |
| `Ctrl + Shift + Enter` | 在当前行上方插入新行 |
| `Ctrl + Enter` | 在当前行下方插入新行 |
| `Ctrl + ]` / `[` | 增加/减少缩进 |
| `Ctrl + Shift + \` | 跳转到匹配的括号 |
| `Ctrl + Shift + K` | 删除整行 |
| `Ctrl + ↑/↓` | 滚动视图（光标不动） |
| `PgUp/PgDown` | 翻页 |
| `Alt + PgUp/PgDown` | 切换编辑器标签页 |
| `Ctrl + /` | 切换行注释 |
| `Shift + Alt + A` | 切换块注释 |
| `Ctrl + H` | 查找替换 |
| `Ctrl + L` | 选中当前行 |
| `Shift + Alt + →` | 从光标处扩展选中 |
| `Shift + Alt + ←` | 收缩选择区域 |
| `Ctrl + .` | 快速修复 |
| `Shift + Alt + F` | 格式化文档 |
| `Ctrl + K Ctrl + F` | 格式化选中区域 |

### 代码折叠

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + Shift + [` | 折叠当前区域 |
| `Ctrl + Shift + ]` | 展开当前区域 |
| `Ctrl + K Ctrl + [` | 折叠所有子区域 |
| `Ctrl + K Ctrl + ]` | 展开所有子区域 |
| `Ctrl + K Ctrl + 0` | 折叠所有区域 |
| `Ctrl + K Ctrl + J` | 展开所有区域 |

### 开发导航类

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + G` | 跳转到指定行 |
| `Ctrl + P` | 快速打开文件 |
| `Ctrl + T` | 搜索所有符号 |
| `Ctrl + Shift + O` | 跳转到当前文件符号 |
| `Alt + ←/→` | 前进/后退光标位置 |
| `Ctrl + Shift + M` | 打开问题面板 |
| `F8` | 跳转到下一个错误/警告 |
| `Shift + F8` | 跳转到上一个错误/警告 |
| `Ctrl + D` | 多光标选择下一个匹配项 |
| `Ctrl + Shift + L` | 多光标选择所有匹配项 |
| `F12` | 跳转到定义 |
| `Alt + F12` | 查看定义（Peek） |
| `Ctrl + K F12` | 在侧边打开定义 |
| `Shift + F12` | 查找所有引用 |
| `F2` | 重命名符号 |

### 多窗口管理

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + \` | 拆分编辑器 |
| `Ctrl + 1/2/3` | 聚焦到第 1/2/3 编辑器组 |
| `Ctrl + K Ctrl + ←/→` | 移动编辑器组位置 |
| `Ctrl + W` | 关闭当前编辑器 |
| `Ctrl + K W` | 关闭所有编辑器 |
| `Ctrl + Tab` | 切换最近打开的文件 |

### 集成终端

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + ` ` | 打开/关闭集成终端 |
| `Ctrl + Shift + ` ` | 创建新终端 |
| `Ctrl + Shift + C` | 复制选中内容 |
| `Ctrl + Shift + V` | 粘贴到终端 |
| `Shift + PgUp/PgDown` | 终端翻页 |
| `Ctrl + Home/End` | 滚动到顶部/底部 |

### 调试快捷键

| 快捷键 | 功能 |
|--------|------|
| `F5` | 开始调试 / 继续 |
| `Shift + F5` | 停止调试 |
| `Ctrl + Shift + F5` | 重启调试 |
| `F9` | 切换断点 |
| `F10` | 单步跳过 (Step Over) |
| `F11` | 单步进入 (Step Into) |
| `Shift + F11` | 单步跳出 (Step Out) |
| `Ctrl + K Ctrl + I` | 显示悬停信息 |

---

## 高级配置

### 用户设置 vs 工作区设置

- **用户设置**：`~/.config/Code/User/settings.json`（全局）
- **工作区设置**：`.vscode/settings.json`（项目级）

工作区设置优先级更高，适合团队共享。

### 推荐配置

```json
{
  // 编辑器
  "editor.fontSize": 14,
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": true,
  "editor.rulers": [80, 120],
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,

  // 文件
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/.svn": true,
    "**/*.o": true,
    "**/build": true
  },

  // 终端
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.shell.linux": "/bin/bash",

  // C/C++
  "C_Cpp.clang_format_style": "{ BasedOnStyle: Google, IndentWidth: 4 }",
  "C_Cpp.default.cStandard": "c11",
  "C_Cpp.default.cppStandard": "c++17",

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,

  // 远程开发
  "remote.SSH.remotePlatform": {
    "baikal-server": "linux"
  },
  "remote.SSH.enableRemoteCommand": true
}
```

### 任务配置 `tasks.json`

自动化构建和测试：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "type": "shell",
      "command": "make",
      "args": ["-j4"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": ["$gcc"],
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    },
    {
      "label": "clean",
      "type": "shell",
      "command": "make clean",
      "group": "build"
    },
    {
      "label": "test",
      "type": "shell",
      "command": "./run_tests.sh",
      "group": "test"
    }
  ]
}
```

运行任务：`Ctrl + Shift + B`（默认构建任务）

### 代码片段（Snippets）

创建自定义代码片段以提高效率。

**打开片段编辑器**：`Ctrl + Shift + P` → `Snippets: Configure User Snippets`

**示例：C 语言头文件保护**

```json
{
  "Header Guard": {
    "prefix": "hguard",
    "body": [
      "#ifndef ${1:${TM_FILENAME_BASE/(.*)/${1:/upcase}/}_H}",
      "#define $1",
      "",
      "$0",
      "",
      "#endif // $1"
    ],
    "description": "Insert header guard"
  }
}
```

**使用**：在 `.h` 文件中输入 `hguard` 并按 `Tab`，自动生成头文件保护宏。

---

## 常见问题

### Q1: 如何同步设置到多台机器？

**方案 1：使用 Settings Sync（内置）**

- 登录 Microsoft 或 GitHub 账号
- 点击左下角齿轮图标 → **Turn on Settings Sync**
- 选择要同步的内容（设置、快捷键、插件等）

**方案 2：手动同步**

- 将 `settings.json` 和 `.vscode/extensions` 放入 Git 仓库
- 在新机器上拉取并恢复

### Q2: 插件过多导致启动缓慢

**诊断**：`Ctrl + Shift + P` → `Developer: Show Running Extensions`

**优化**：
- 禁用不常用的插件
- 为特定语言设置推荐插件（`.vscode/extensions.json`）
- 使用工作区禁用全局插件

### Q3: C/C++ IntelliSense 不工作

**检查步骤**：
1. 确认 `c_cpp_properties.json` 配置正确
2. 检查 `compilerPath` 是否有效
3. 查看 **C/C++ Output** 面板的错误信息
4. 重启 C/C++ 扩展：`Ctrl + Shift + P` → `C/C++: Restart IntelliSense`

---

## 相关资源

- [[Makefile完全指南]]：构建系统配置
- [[Git使用手册]]：版本控制最佳实践
- [[GDB调试技巧]]：命令行调试工具

## 参考链接

- [VSCode 官方文档](https://code.visualstudio.com/docs)
- [Remote-SSH 配置指南](https://code.visualstudio.com/docs/remote/ssh)
- [快捷键速查表 (PDF)](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)

---

**最后更新**: 2025-11-19
