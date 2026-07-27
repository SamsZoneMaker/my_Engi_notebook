Training by: Jiangcheng

# FPGA调试Training  

了解FPGA

nandflash 不支持片上运行  spiflash支持寄存器的动态寻址，支持直接片上运行



Andes：外面做RSIC-V的公司

文档在tech/andes

软核是可以改的 FPGA，需要分清楚软核硬核的区别



spinor flash的驱动 driver在哪里？



openocd 是一个第三方应用程序，提供apb的访问接口 （弄清楚什么是apb接口）

非直接访问，ahb高速信号路线图中右边的红线



quartus 烧写sof （本质上是烧写FPGA）



第二种方法可以跳过andes的工具，用串口烧写

启动的方式有：spi启动和rom启动



nor flash驱动的源码



retimer vs. redriver

retimer 会重置信号，实际上肯定是比redriver好的

bmc的作用





jtag

tdi接tdi

tdo接tdo



时钟一次跳变一个bit，且低bit位lsb优先传输