# SerDes Arch Training

## 20250328

代码架构：

boot有3个方案  <BOOTMODE.docx>

现有芯片有两个内核  Andes-RSIC-V



内核：

链接地址linker.ld(系统的链接地址  运行在ILM上)  链接地址0x80000000



\> 重定向到flash



start.S (n25f) 是RISC-V的启动代码



c语言遵循abi（？）的标准  汇编的压栈和入栈



在soc firmware中  FreeRtos有3套体系  



小空间基本都是固定空间 不会经常 malloc()  和 free()

不考虑内存碎片



bootrom 允许下载 2.解决了只能从0地址启动 做了双分区的概念



Kernal的优先级 看启动顺序（n25f_reset.c ———extern main）





ctle是把高频boost起来

vga设置摆幅

greycode是CDR用的

tia光转电
