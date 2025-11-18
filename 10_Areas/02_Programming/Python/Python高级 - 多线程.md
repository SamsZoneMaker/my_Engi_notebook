---
tags:
  - "#domain/programming"
  - "#type/knowledge"
  - "#level/advanced"
  - "#lang/python"
status: 完善中
complexity: 高级
notetype: 学习笔记
resource: Python Threading Documentation
related:
  - "[[🐍 00_Python_MOC]]"
  - "[[Python基础 - 类与面向对象]]"
created: 2025-11-18 21:46:54
modified: 2025-11-18 21:46:54
---
# Python高级 - 多线程

> [!abstract] 摘要
> 本笔记详细介绍Python中的多线程编程,包括threading模块的使用、线程同步机制和线程队列的实现方法。

## 🎯 Target
- [ ] 理解多线程的概念和优势
- [ ] 掌握threading模块的基本使用
- [ ] 熟练使用线程同步机制(锁)
- [ ] 学会使用Queue实现线程间通信
- [ ] 了解多线程的最佳实践

## 📝 Core

### 多线程基础

#### 概念
多线程类似于同时执行多个不同的程序,每个线程代表程序中的一个独立执行流。

#### 多线程的优点
- 把占用时间长的程序放在后台运行
- 程序整体的运行速度可以加快
- 在一些需要等待用户输入、文件读写等情况下,线程可以释放一些珍贵的资源(内存占用等)

#### 线程 vs 进程
- **进程**: 每个独立的进程有一个程序运行的入口、顺序执行序列和程序的出口
- **线程**: 线程不能够独立执行,必须依存在应用程序中,由应用程序提供多个线程执行控制

### Threading库

#### 标准库
Python通过两个标准库支持线程:
- `_thread`: 提供了低级别的、原始的线程以及一个简单的锁
- `threading`: 建立在`_thread`模块之上,提供了更高级、更易用的线程管理接口(推荐使用)

#### 常用方法
```python
import threading

# 模块级函数
threading.currentThread()  # 返回当前的线程对象
threading.enumerate()      # 返回一个包含正在运行的线程的list
threading.activeCount()    # 返回正在运行的线程数量

# Thread类方法
thread.start()      # 启动线程活动
thread.join([time]) # 等待至线程中止
thread.run()        # 线程执行的代码
thread.isAlive()    # 返回线程是否活动
thread.getName()    # 返回线程名
thread.setName()    # 设置线程名
```

### 创建线程

#### 方法1: 使用函数创建线程

```python
import threading
import time

def print_numbers():
    """打印数字的函数"""
    for i in range(5):
        print(f"Number: {i}")
        time.sleep(1)

def print_letters():
    """打印字母的函数"""
    for letter in ['a', 'b', 'c', 'd', 'e']:
        print(f"Letter: {letter}")
        time.sleep(1)

# 创建线程
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("All threads completed!")
```

**步骤总结:**
1. 导入`threading`模块
2. 定义一个函数作为线程的执行体
3. 创建`threading.Thread`对象,将定义的函数作为`target`参数
4. 调用线程对象的`start()`方法启动线程
5. (可选)调用线程对象的`join()`方法等待线程执行完毕

#### 方法2: 继承Thread类创建线程

```python
import threading
import time

class MyThread(threading.Thread):
    """自定义线程类"""

    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)  # 调用父类初始化
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        """重写run方法,线程启动时会自动调用"""
        print(f"Starting {self.name}")
        print_time(self.name, self.counter, 5)
        print(f"Exiting {self.name}")

def print_time(thread_name, delay, counter):
    """打印时间的辅助函数"""
    while counter:
        time.sleep(delay)
        print(f"{thread_name}: {time.ctime(time.time())}")
        counter -= 1

# 创建新线程
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# 开启线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()

print("Exiting Main Thread")
```

**步骤总结:**
1. 导入`threading`模块
2. 定义一个新的类,继承自`threading.Thread`
3. 重写父类的`__init__()`方法(务必调用`super().__init__()`)
4. 重写父类的`run()`方法,将线程要执行的代码放在其中
5. 创建该子类的实例
6. 调用实例的`start()`方法启动线程(`start()`会自动调用`run()`)
7. (可选)调用实例的`join()`方法等待完成

### 线程同步

#### 为什么需要同步?
如果多个线程共同对某个数据进行修改,可能会产生不可预料的结果(数据竞争)。因此多个线程之间需要进行同步。

#### 锁的概念
锁有两种状态:
- **锁定(Locked)**: 资源被占用
- **未锁定(Unlocked)**: 资源空闲

#### 使用Lock实现同步
```python
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print(f"Starting {self.name}")
        # 获得锁,成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        thread_lock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        thread_lock.release()

def print_time(thread_name, delay, counter):
    while counter:
        time.sleep(delay)
        print(f"{thread_name}: {time.ctime(time.time())}")
        counter -= 1

# 创建锁
thread_lock = threading.Lock()
threads = []

# 创建新线程
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()

print("Exiting Main Thread")
```

#### 锁的工作原理
1. 线程A要访问共享数据时,先获得锁定(`acquire()`)
2. 如果线程B也要访问,但锁已被线程A占用,线程B就会阻塞等待
3. 线程A访问完毕后释放锁(`release()`)
4. 线程B获得锁,继续执行

> [!tip] 上下文管理器
> 推荐使用`with`语句自动管理锁:
> ```python
> with thread_lock:
>     print_time(self.name, self.counter, 3)
> # 自动释放锁,即使发生异常
> ```

### 线程队列(Queue)

#### 概念
Queue模块提供了线程安全的队列,可以实现线程间的安全数据传递。常见的队列类型:
- **FIFO队列**: 先进先出
- **LIFO队列**: 后进先出(栈)
- **优先级队列**: 按优先级排序

#### Queue常用方法
```python
import queue

# 创建队列
work_queue = queue.Queue(maxsize=10)

# 常用方法
work_queue.qsize()              # 返回队列的大小
work_queue.empty()              # 如果队列为空,返回True
work_queue.full()               # 如果队列满了,返回True
work_queue.put(item)            # 写入队列
work_queue.get()                # 获取队列元素
work_queue.get_nowait()         # 相当于get(False)
work_queue.put_nowait(item)     # 相当于put(item, False)
work_queue.task_done()          # 向队列发送任务完成信号
work_queue.join()               # 等待队列为空
```

#### 使用Queue的示例
```python
import queue
import threading
import time

exit_flag = 0

class MyThread(threading.Thread):
    def __init__(self, thread_id, name, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.q = q

    def run(self):
        print(f"Starting {self.name}")
        process_data(self.name, self.q)
        print(f"Exiting {self.name}")

def process_data(thread_name, q):
    while not exit_flag:
        queue_lock.acquire()
        if not work_queue.empty():
            data = q.get()
            queue_lock.release()
            print(f"{thread_name} processing {data}")
        else:
            queue_lock.release()
        time.sleep(1)

thread_list = ["Thread-1", "Thread-2", "Thread-3"]
name_list = ["One", "Two", "Three", "Four", "Five"]
queue_lock = threading.Lock()
work_queue = queue.Queue(10)
threads = []
thread_id = 1

# 创建新线程
for t_name in thread_list:
    thread = MyThread(thread_id, t_name, work_queue)
    thread.start()
    threads.append(thread)
    thread_id += 1

# 填充队列
queue_lock.acquire()
for word in name_list:
    work_queue.put(word)
queue_lock.release()

# 等待队列清空
while not work_queue.empty():
    pass

# 通知线程是时候退出
exit_flag = 1

# 等待所有线程完成
for t in threads:
    t.join()

print("Exiting Main Thread")
```

### 实际应用场景

#### 1. 并发下载
```python
import threading
import requests

def download_file(url):
    """下载单个文件"""
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

urls = [
    'http://example.com/file1.pdf',
    'http://example.com/file2.pdf',
    'http://example.com/file3.pdf',
]

threads = []
for url in urls:
    thread = threading.Thread(target=download_file, args=(url,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("All downloads completed!")
```

#### 2. 生产者-消费者模式
```python
import threading
import queue
import time
import random

def producer(q):
    """生产者"""
    for i in range(5):
        item = f"Item-{i}"
        q.put(item)
        print(f"Produced {item}")
        time.sleep(random.random())

def consumer(q):
    """消费者"""
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumed {item}")
        time.sleep(random.random())
        q.task_done()

# 创建队列
q = queue.Queue()

# 创建生产者线程
producer_thread = threading.Thread(target=producer, args=(q,))
producer_thread.start()

# 创建消费者线程
consumer_thread = threading.Thread(target=consumer, args=(q,))
consumer_thread.start()

# 等待生产者完成
producer_thread.join()

# 发送终止信号给消费者
q.put(None)

# 等待消费者完成
consumer_thread.join()

print("All tasks completed!")
```

### 注意事项和最佳实践

> [!warning] 重要提示
> - **避免使用`-i`标志**: 不要使用需要交互式输入的git命令(如`git rebase -i`或`git add -i`)
> - **GIL限制**: Python的全局解释器锁(GIL)意味着同一时刻只有一个线程在执行Python字节码,因此多线程不适合CPU密集型任务
> - **适用场景**: 多线程适合I/O密集型任务(网络请求、文件读写等)
> - **资源竞争**: 始终使用锁来保护共享资源
> - **死锁风险**: 注意避免死锁(两个线程互相等待对方释放锁)

> [!tip] 最佳实践
> 1. **优先使用`with`语句管理锁**: 自动释放,避免忘记
> 2. **使用`join()`等待线程完成**: 确保主程序不会过早退出
> 3. **使用`Queue`进行线程间通信**: 比使用共享变量更安全
> 4. **为线程命名**: 便于调试和日志记录
> 5. **CPU密集型任务使用多进程**: 使用`multiprocessing`模块代替

---
## 🤔 Q&A

### Q1: 什么时候使用多线程,什么时候使用多进程?
**A**:
- **多线程**: I/O密集型任务(网络请求、文件读写),因为GIL在I/O操作时会释放
- **多进程**: CPU密集型任务(大量计算),可以真正利用多核CPU

### Q2: 为什么Python有GIL还要使用多线程?
**A**: 虽然GIL限制了CPU密集型任务的并行,但对于I/O密集型任务,当一个线程在等待I/O时,其他线程仍可以运行,因此多线程仍然有效。

### Q3: 什么是死锁,如何避免?
**A**: 死锁是指两个或多个线程互相等待对方释放资源。避免方法:
- 按固定顺序获取锁
- 使用超时机制
- 使用`RLock`(可重入锁)

### Q4: join()方法的作用是什么?
**A**: `join()`会阻塞主线程,直到被调用线程执行完毕。这确保了主程序不会在子线程完成前退出。

## 🚀 Tasks
- [ ] 编写一个多线程文件下载程序
- [ ] 实现生产者-消费者模式练习队列使用
- [ ] 练习使用锁保护共享资源
- [ ] 对比多线程和多进程的性能差异

## 📚 Reference
* Python官方文档 - threading
* Python官方文档 - queue
* Threading in Python: The Complete Guide

## 🕸️ Relation
* 这篇笔记是[[🐍 00_Python_MOC|Python知识体系]]的高级部分
* [[Python基础 - 类与面向对象]]是理解线程类的基础
* [[Python高级 - 异常处理]]在多线程中同样重要
