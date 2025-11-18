swpedia_keyword: [vscode]

author: [ cheng.jiang@wisewavetech.com]   [ zhengquan.lin@wisewavetech.com] [desen.li@wisewavetech.com]

---

开源的代码编辑器, 以丰富的插件及灵活的配置著称。

# 1 安装

```
1. windows绿色版
	VSCode-win32-x64-1.67.2.zip
```

# 2 插件移植

```
1. windows插件默认位置
	C:\Users\cheng.jiang\.vscode\extensions
2. linux版插件默认位置
	~/.vscode/extensions
3. windows和linux插件通用, 拷贝即可
```

# 3 常用配置

#### **手动挂载远程目录**

1. SSHFS+WINFSP工具 红区提取目录：

   ```
   \\wisewave.local\fs\rd\Engineering\Firmware\Eevelopment Environment\tools
   ```

2. 右键此电脑-映射网络驱动器
3. \\sshfs\username@ipaddress(映射baikal服务器：\\sshfs\xxx.xx@10.1.3.228)
4. 输入登录的账号密码后，即可用vscode打开远程服务器上的代码。

# 4 常用插件

#### **Remote-SSH**

可以直接在 VS Code 中打开远程服务器(Baikal)上的文件夹

#### 步骤：

1. **安装 Remote - SSH 插件**：

   - 在 VS Code 中，打开扩展市场（快捷键：`Ctrl + Shift + X` 或点击左侧扩展图标）。
   - 搜索 **Remote - SSH** 并安装它。

2. **通过 SSH 连接到服务器**：

   - 按下快捷键 `Ctrl + Shift + P`（Windows/Linux）或 `Cmd + Shift + P`（Mac），打开命令面板。

   - 输入并选择 **Remote-SSH: Connect to Host**。

   - 在弹出的输入框中，输入你的服务器 SSH 地址：

     ```
     user@10.1.3.228
     ```

     其中user是服务器的用户名(例如: zhengquan.lin)，10.1.3.228是baikal服务器的 IP 地址。

   - 如果是首次连接，会提示你添加 SSH 主机到配置文件中，确认即可。

3. **选择代码文件夹**：

   - 连接到服务器后，VS Code 界面会切换到远程工作状态。
   - 在左侧的资源管理器中，点击 **Open Folder**，导航到服务器上你从 Git 拉下来的代码所在文件夹并打开它。

4. **开始编辑远程代码**

   

#### Markdown PDF

1. **搜索并下载Markdown PDF**
该插件允许你直接将 Markdown 文档转换为 PDF、HTML 等格式。

2. **按下快捷键 Ctrl+Shift+P（Windows/Linux），调出命令面板。**

3. **输入并选择：**

  ```
  Markdown PDF: Export (pdf)
  ```

4. **插件会自动将你的 Markdown 文件转换为 PDF，并保存到与你 Markdown 文件相同的目录下。**



# 5 常用快捷键

### 代码编辑类

| Shortcut                  | Function                       |
| ------------------------- | ------------------------------ |
| Alt + up/down             | 将当前行代码移动上下行             |
| Shift + Alt + up/down     | 将当前行代码复制到上下行           |
| Ctrl + Shift + Enter      | 在当前行上插入新行                |
| Ctrl + ] / [          | 行缩进                         |
| Ctrl + Shift + \      | 匹配花括号的闭合处，跳转功能   |
| Ctrl + Shift + K      | 整行删除                       |
| Ctrl + up/down        | 滚轮功能                       |
| PgUp/PgDown           | 光标在当页头尾切换，再按则翻页 |
| Alt + PgUp/PgDown     | 屏视图切页                     |
| Ctrl + Shift + [ or ] | 折叠or展开区域代码             |
| Ctrl + K Ctrl + [     | 折叠所有子区域代码             |
| Ctrl + k Ctrl + ]     | 展开所有折叠的子区域代码       |
| Ctrl + K Ctrl + 0     | 折叠所有区域代码               |
| Ctrl + K Ctrl + J     | 展开所有折叠区域代码           |
| Ctrl + /              | 添加关闭行注释                 |
| Ctrl + K Ctrl + C     | 添加行注释                     |
| Ctrl + K Ctrl + U     | 删除行注释                     |
| Ctrl + H              | 替换                           |
| Ctrl + L              | 选中当前行                     |
| Shift + Alt + right   | 从光标处扩展选中全行           |
| Shift + Alt + left    | 收缩选择区域                   |
| Ctrl + .              | 快速修复部分可以修复的语法错误 |
| Shift + Alt + F       | 代码格式自动化规整             |



### 开发常用类

| Shortcut              | Function                                   |
| --------------------- | ------------------------------ |
| Ctrl + G | 跳转行 |
| Ctrl + P | 跳转文件 |
| Ctrl + T | 列出所有符号 |
| Ctrl + Shift + O | 跳转到符号处 |
| Alt + Left / Right | 跳转光标位置 |
| Ctrl + Shift + M | 打开问题面板 |
| F8 | 跳转到下一个错误或者警告 |
| Shift + F8 | 跳转到上一个错误或者警告 |
| Ctrl + D | 移动当前选择到下个匹配选择的位置(光标选定) |
| F12 | 跳转到定义处或使用处 |
| Alt + F12 | 显示代码段定义 |
| Ctrl + K F12 | 打开另一窗口显示定义处 |
| Shift + F12 | 显示所有引用 |
| F2 | 重命名符号 |
| Ctrl + \ | 切割编辑窗口 |
| Ctrl + 1/2/3 | 切换焦点在不同的切割窗口 |
| Ctrl + K Left / Right | 切割窗口位置调换 |

### 终端

| Shortcut              | Function             |
| --------------------- | -------------------- |
| Ctrl + `              | 打开集成终端         |
| Ctrl + Shift + `      | 创建一个新的终端     |
| Ctrl + Shift + C      | 复制所选             |
| Ctrl + Shift + V      | 复制到当前激活的终端 |
| Shift + PgUp / PgDown | 页面上下翻屏         |
| Ctrl + Home / End     | 滚动到页面头部或尾部 |
