<%*
// 获取所有文件夹
const folders = app.vault.getAllLoadedFiles()
    .filter(file => file.children)
    .map(folder => folder.path)
    .filter(path => path !== "")
    .sort();

// 添加根目录选项
folders.unshift("根目录 (Root)");

// 选择文件夹
const selectedFolder = await tp.system.suggester(
    folders.map(folder => folder === "根目录 (Root)" ? "📁 " + folder : "📁 " + folder),
    folders
);

if (!selectedFolder) {
    new Notice("已取消创建笔记");
    return;
}

// 输入笔记名称
const noteName = await tp.system.prompt("请输入笔记名称:");
if (!noteName) {
    new Notice("已取消创建笔记");
    return;
}

// 确定最终路径
const finalFolder = selectedFolder === "根目录 (Root)" ? "" : selectedFolder;
const fullPath = finalFolder ? `${finalFolder}/${noteName}` : `${noteName}`;

// 移动文件到指定位置
await tp.file.move(fullPath);
_%>
---
tags: 
aliases: 
create date: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %>
modify date: 
---
# 📝 笔记内容