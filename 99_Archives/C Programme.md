---
modify date: 2025-08-19  18:03:19
modified: 2025-11-18  21:48:31
---
# C Programme

## C 基本格式

1. system是一种函数调用，功能是运行windows命令。

   system（“pause”）；让程序停在cmd画面，造成程序输入任意键之前不会结束

   system（“color 3”）；让cmd字体颜色改变

2. Int main（）解释
             main是程序的入口，操作系统启动一个程序，先找整个exe文件中main出现的位置；main是函数名称，加上括号（）才算函数；
             int是和末尾return0配套的，int是操作系统启动一个程序让程序干活，干完之后return0给操作系统一个交代。
             一般函数调用返回给操作系统，正常返回都是0（正数），程序出错了一般会返回负数。

3. {}是上一个函数管辖的范围

4. Int main后面一定要return0，如果用了void main则后面不需要反馈交代，不需要return0 

5. 循环中的另一种形式 

      ```c
      if  () {}
      else if (){}
      else {}
      ```

6. ```c
   switch（）{
    Case 0：
    case 1： 
    break;
    Case 2:
    case 3:
    break；}
   default :...break;
   ```
   
   * 在Switch语句中,没有break语句时,程序会继续执行下一条case的语句
   * 当判断结果与任何一个case都不相符时,直接执行default
   
7. do-while

   ```c
   do{
       ...
   }while(继续条件);    
   ```

   ```c
   do{
       ...
   }while(!终止条件);
   ```

8. 实现无限循环的方法

   ```c
   while(1){}
   ```

   ```c
   for( ; ; ){}
   ```

```c
printf("why no header?");

```






## C 基础知识（整型、循环...）

- 程序变量包括类型、变量名、变量值。（int num=1）变量名不以数字开头。
- 占位符 %d，代表在输出的地方占一个位，其输出的值取决于逗号后面的变量名里的变量值。
- 记得在printf后加\n；
- scanf双引号中除了占位符尽量不要写其他东西，否则输入时很有可能会产生错误
- 占位符只是代表从键盘中输入一个数，输入要比输出多了一个地址的约束，也就是加一个&
- 当连续输入多个变量时，最好分开写scanf
          或者写成scanf（“%d%d”, &num1, &num2)；的形式
- If     else语句表示如果…否则…  要在if和else后面加{} 不然只会运行if else的那一句话
- 用while循环先定义一个循环变量， while（1）{循环变量+1；循环内容；给出循环的种终止条件（用break；跳出}
- 一般在使用while的时候会将大括号内的内容进行缩进
- for（初始条件，控制条件（当不满足此情况时，不执行for循环体）， 条件变化）    常见for（i=0， i<=10 , i++)
- 用for构造一个死循环的方法  for（ ， ，）{ 循环体}
- Do while 和while的区别在于dowhile至少有一次执行，但while一旦为0则一次都不执行。
- 不同类型数据进行运算时，比如两个整数相除，必须将除数或者被除数强制转换成小数，否则小数点后面的数据会被忽略。
- float为单精度的小数值
- &&表示和  ||表示或  !a表示取非
- `%3d`表示输出3位整型数,不够3位则右对齐.`%9.2f` 表示输出为9的浮点数, 其中小数位为2, 整数位为7,小数点占一位, 不够9位右对齐
- 终止函数的形式是`return x;`,因此即便在函数中用了`while(1)`作为循环条件,遇到return也会直接跳出函数返回主函数中
- `const`类型修饰符,在函数声明接收数组的形参时应该使用const,确保函数中不能改写数组的元素值`(const int v[  ],int n)`此为一般形式





## 函数

1. 操作系统是找到程序中第一个main运行的，即便在main前面定义函数，操作系统也是会从后面的第一个main开始运行；

2. **什么是函数？**
   函数是一个功能模块，它把实现某个功能的代码块包含起来，并起一个函数名供别人调用，如printf、system函数等等，是程序运行当中包装起来的一个步骤。

3. **如何定义一个函数**
   ①返回值；②形式参数；③函数名；④函数体（代码块）
             如： int     prepare（）；

4. **如何调用一个函数**         

    函数名（实际参数）； 或 函数名（）；

5. **为什么要调用函数**

   * 让程序更好看；
   * 容易定位问题；
   * 可复用；
   * 可将全部函数中每个函数分工做

6. void函数代表无返回值不需要return。或者说，void代表返回值的类型是无类型，return要写，但是return后面不加变量，直接写return；（这种情况不常用）

7. Void buyrice (int     kg) 中的kg是形式参数，意思类似变量定义，所以写法上也类似变量的定义， 如用到int等。与传参相关。

8. ①7代码中 kg是局部变量，同时它是一个形式参数，作用域仅限为该函数。

   ② 形式参数也是一个变量，局部变量，有自己的内存空间。其空间生存期为当函数被调用的时候申请了该内存空间，才有了这个变量。同时这个空间的数据被赋值成实际参数的值，函数调用吧实际参数的值拷贝一份给形式参数。

   ③当函数执行结束后，该内存管理单元自动回收（释放）。


9. 形式参数与局部变量的比较：

   形式参数也是局部变量的一种，作用仅限于该函数，决定了该变量的生效范围。且生存周期也类似。
    形式参数会更灵活，会根据main函数里传递过来的实参的值变而发生变化。

10. 看懂一个函数3步：
            ① 参数怎么传，参数的类型，参数的个数。
            ②函数的返回值，返回值的类型
            ③功能：一般用函数的名字来体现函数的功能

2. a++表示先使用a的值再+1，++a表示把现有的a的值+1后使用
3. 在函数末尾 return  xxx表示把函数执行的结果返回给调用者，输入什么类型的数其还函数就是一个什么类型的数，至于数值为多少取决于return后面的变量的值（相当于函数的结果等于return后面的值）
4. 在定义有返回值的函数时，要用int定义而void定义的是无返回值的函数。
5. main函数和定义函数内即便都有x，y等变量，但其实是不一样的。而调用函数的时候把x变量传过去传的是数值。 
6. char用来定义字符，定义方法类似于int等，用getchar（）吸收输入时的回车。
7. 当程序内有多个回车可能需要被吸收时可采用办法：定义一个变量=0，令其不为0时才吸收回车，并在程序后令变量加一，
             否则可能会在程序开始时就需要敲两次回车。语句：if（I ！=0）{}





## 数组

### 基础知识

1. 数组是数据的集合；

2. 数组的数据必须是同类型的，不能同时存在整型和浮点型的数；

3. 数组地址时连续的；

4. 数组是通过下标来引用当中的某个元素的

5. Array[0]表示的是第一个数，同理array[10]是第十一个数。也就是说是从0开始算的；

   1. 数组中的中括号[]只有在定义一个数组的时候，才表示数组的大小，其余任何情况，都表示用下标来访问数组`int array[10]`这里的10表示数组大小

7. 遍历数组的数组的时候可以用
             for（i=0；i<100; i++){
                 printf("第%d个数为%d", i+1,      array[i];
             }

8. Sum +=     array[i] 等同于 sum=     sum + array[i]；
             相当于将i个array[i]相加起来= sum

9. Putchar （'\n'）;输出一个字符， getchar（）获取一个字符的输入，过滤一个回车。

10. 数组和函数相结合的时候，数组名当作实际参数。

11. ==int     a[3]和 char b[3]两者的异同点？==
              一个整型数占用空间4个字节，3个占用12个字节
              一个char型占用空间1个字节，3个占用空间3个字节

12. 检验某数组或整数的空间大小可用语句 sizeof（a）（括号内为检验的内容） 

13. 如何计算数组中元素的个数：数组的总大小/一个类型的大小。

    例如：printf（“a数组有%d个元素\n“, sizeof(a)/ sizeof(a[0])）

    上句中的后半部分也可写成 sizeof（a） / sizeof（int）

    相应的char型数组也可以写成 sizeof（a） / sizeof（char）。

14. 函数调用的形式参数，虽然写的是一个数组的样子，但中括号内数组的大小是无效的，中括号内写任何值都不能代表形参数组的大小。
15. 调用函数中的中括号仅仅用来表示地址，windows中用4个字节表示地址；linux64中用8个字节表示地址。
16. 函数传参的时候不仅要把地址传过去也要把个数传过去。
17. 数组名= 数组的首地址 = 第一个元素的地址



### 定义数组的几种方式

1. Int array[100]; 没有初始化数据，仅仅申请了100个整型的内存空间，一般定义时最好写：int array[100] =     {0}
2. Int array[3] =     {1,2,3}; 有初始化的数组，该数组申请了三个整型数内存空间，并赋值1，2，3；
3. Int array[100] =     {1,2,3}; 有初始化的数组，但是不完整初始化，该数组申请了100个整型数内存，但赋值只有三个数1，2，3，放在数组的前三个位置，后面的数皆为0.



### Example

```c
void arrayPrint(int datas[],int cnt)  //这里的数组只是一个形参,中括号内无论数字写多少都是无效的,都不能代表形参数组的大小.此处中括号的作用仅在于区别整型.
```



## 指针

* 地址：scanf("%d",&xxx)中的&就是取地址

* 指针可以理解为地址,是存放地址的变量

* 变量的访问有两种方式

  * 变量名 
  * 地址

* 查找地址的方式`printf("%p",&a);`

* 用地址找到变量的方式`printf("%d",*(&a));` 这里的*是一个运算符,与+-类似 , *的功能室取出内存地址中数据的值(取内容)

* `int a`是整型变量,存放的是整数;

  `char c = 'c';`是字符变量,存放的是字符;

  `int array[];`是数组,存放的是一串数据

  三者都是变量,但是变量的类型不同

* 与上述三者不同的是存放地址的变量叫==**指针**==

* ==定义指针的方式== `int *p`或者`int* p`

* ==指针赋值的方式==`p = &a;`

* ==数组名本身就是一个地址==  取数组地址的时候可以不加&

* 指针可以强制把想要的数据储存到想要的地址,但地址需要转换`int* p1 = (int*)0x0060ff00`

* 指针数组定义方式:`int *p[5];`

* ==数组指针的定义方式==:`int(*p) []`,偏移的时候，偏移的是整个数组的大小

* ==**函数指针**的定义方式==：`void (*p)(参数可不加)` `int (*p)(char *pname参数可不加)`......

  * *表示指针
  * ( )表示是函数
  * 函数指针是专用的,格式要求很强(参数类型,个数,返回值),与数组指针类似

* ==函数指针的赋值方法==:`p=函数名;`

  * 函数(名)就是地址,跟数组一样

* ==通过函数指针调用函数==:

  * `p(参数)`这种为直接通过指针名字+()   ——较为常用一点
  * `(*p)(参数 );`这种为取内容的方式,(*指针名字)+( )
  
* ==无类型malloc==：`int *p = (int *) malloc(n  * sizeof(int) );`

  `pstr = (char *)malloc(128);`

  用这种方式定义自选数组的大小,malloc指开辟空间的大小

  其返回值是void无类型的,需要用(int *)强转成int *型的,才能定义同类型的指针

* 使用`malloc`的时候要注意是否开辟成功,一般都要加一段判断的程序

  ```c
  if(pstr == NULL){
      printf("Error!");
      exit(-1);
  }
  ```

  

* ==内存泄漏==：程序刚跑起来很顺畅，但若干时间后，程序崩溃

  * malloc申请（开辟）的空间，程序是不会主动释放的；linux中程序结束后，系统会直接回收这个空间
  * 避免的方式
    * 检查循环中有没有一直申请malloc
    * 及时合理释放掉。`free(p);`此时p会成为野指针,定义`p = NULL;`

* ### 定义总结

  * 定义整型变量  ` int a;`
  * 定义p为指向整型数据的指针变量`int *p;`
  * 定义整形数组a,有5个元素  `int a[5];`
  * 定义指针数组p,它由4个指向整型数据的指针元素组成 `int *p[4];`
  * p为指向包含4个元素的一堆数组的指针变量 `int (*p)[4];`
  * f为返回整型函数值的函数 `int f();`
  * p为返回一个指针的函数 ,该指针指向整型数据 `int *p();`
  * p为指向函数的指针,该函数返回一个整数值 `int(*p) ();`
  * p是一个指针变量,它指向一个指向整型数据的指针变量(二级指针)`int **p;`
  * p是一个指针变量,基类型为void,不指向具体的对象 `void *p;`



----------------------------------------



## 基本数据类型和数



### 查询数据类型范围

```c
#include<stdio.h>
#include<limits.h>

int main() {
	puts("该环境下各字符型,整型数值的范围");
	printf("char            :%d~%d\n", CHAR_MIN , CHAR_MAX);
	printf("signed char     :%d~%d\n", SCHAR_MIN, SCHAR_MAX);
	printf("unsigned char   :%d~%d\n",    0     , UCHAR_MAX);

	printf("short           :%d~%d\n", SHRT_MIN, SHRT_MAX);
	printf("long            :%ld~%ld\n", LONG_MIN, LONG_MAX);
	printf("int             :%d~%d\n", INT_MIN, INT_MAX);

	printf("unsigned short  :%u~%u\n", 0 , USHRT_MAX);
	printf("unsigned        :%u~%u\n", 0 , UINT_MAX);
	printf("unsigned long   :%u~%u\n", 0 , ULONG_MAX);

	return 0;
}
```



### 特殊运算符

#### 按位运算符

* `~`为计算反码的运算符
* `<<`位移运算符

`a << b` 将a左移b位.右边空出的位用0填充

`a >> b`将a右移b位



### 基本知识

- 负数- 10 不是整数字面量，而是对整数字面量１０使用的单目运算符－
- 无符号整型的运算中不会发生数据溢出，当运算结果超出最大值时，结果为＂数学运算结果％（该无符号整形能够表示的最大值+1）
- `sqrt`是求平方根的函数,它需要头函数`#include<math.h>`
- 

## 字符串

### 定义字符串的两种方式

```c
char str[] = "abfjslncoeknclskalskjf";
/* 遍历 */
for(i = 0;i< sizeof(str) / sizeof(str[0]);i++){
    printf("%c",str[i]);
}
```



```c
char *pstr = "afksjflkjnlcasji nfoasfjl jflsiafjsd";
/* 打印 */
printf("%s\n",pstr);  //字符串用格式占位符%s表示,不需要用i的下标遍历
```

这种指针的方式较为常用,但是使用时要注意,容易出错



* 字符串在内存中,除了有效字符以外,还会自动在后面补一个`'\0'`作为字符串的结束标识,所以系统分配大小的时候会比比有效字符多1.
* 真正计算有效字符的长度用 `strlen`
* 不能用`sizeof`计算字符串中的有效个数,要用`strlen`,它在计算字符串大小的时候,遇到`'\0'`时,就会结束计数
* ==下述提到的函数头文件都要加入`\#include <string.h>`==
* `gets(地址/指针)`意为把键盘获取到的内容,放到地址(指针)处,与`scanf`功能类似
* `memset(pstr, '\0', 128);`==初始化函数==

  * 三部分,第一部分pstr为初始化的对象,第二部分为初始化成什么字符,第三部分初始化的大小

###常见的几种字符串操作函数

 #### `strcpy`
 是复制标准函数

`char *strcpy(char *dest, const char *src) `

  ```c
  char *strcpy(char *dest, const char *src) 
  
  char strDest[128] = {'\0'};
  char *strSrc = "Hello world!";
  
  strcpy(strDest, strSrc);
  printf("%s\n",strDest);
  
  /* 第二种复制方式 */
  memset(strDest, '\0', sizeof(strDest)/sizeof(strDest[0]));
  strcpy(strDest, "Hello world!");
  puts(strDest);
  ```

  

####`strncpy`

是用于将指定长度的字符串复制到字符数组中的函数

`char *strncpy(char *destinin, char *source, int maxlen);`

* destinin：表示复制的目标字符数组；
* source：表示复制的源字符数组；
* maxlen：表示复制的字符串长度

```c
char *strncpy(char *destinin, char *source, int maxlen)

char *strDest;
strDest = (char*)malloc(128);
memset(strDest, '\0', 128);

strncpy(strDest, "Hello world!", 5); //输出结果为Hello
puts(strDest);
```



#### `strcat`

是将两个char型连接的函数

  `char *strcat(char *dest, const char *src);`

  ```c
  char *strcat(char *dest, const char *src);
  
  char *strDest = "Hello";
  char src[128] = "World!";
  
  strcat(strDest, src);
  puts(strDest);
  ```



#### `strcmp`

是用于比较两个字符串并根据比较结果返回整数的函数

  `int` `strcmp``(``const` `char` `*s1,``const` `char` `*s2);`

  ```c
  int strcmp(const char *s1,const char *s2);
  
  int res = 0;
  char *s1 = "123";
  char *s2 = "4567";
  res = strcmp(s1,s2);   //前大后小输出1,前小后大输出-1,相等输出0
  printf("%d", res);
  ```



#### `strchr`

是在参数**str**所指向的字符串中搜索第一次出现字符**c**（一个无符号字符）的位置的函数

  `char *strchr(const char *str, int c)`

  * **str**-- 要被检索的 C 字符串
  * **c**-- 在 str 中要搜索的字符
  * 返回一个指向该字符串中第一次出现的字符的指针，如果字符串中不包含该字符则返回NULL空指针 

  ```c
  char *strchr(const char *str, int c)
      
  char *str = "Hello world!";
  char c = 'o';
  
  char* p;
  p = strchr(str,c);
  if(p == NULL)
      printf("No");
  else{
      printf("Find it\n");
      puts(p);
  }
  ```



#### `strstr`

是返回字符串中首次出现子串的地址的函数,与`strchr`类似

  `char` `*``strstr``(``char` `*str1, ``const` `char` `*str2);`

  ```c
  char *strstr(char *str1, const char *str2);
  
  char *str = "Hello world!";
  char *c = "llo";
  
  char* p;
  p = strstr(str,c);
  if(p == NULL)
      printf("No");
  else{
      printf("Find it\n");
      puts(p);
  }
  ```

  

  #### `strlwr`

功能是将字符串中的S参数转换为小写形式

  `char *strlwr(char *s);`

```c
char *strlwr(char *s);

char s[] = "Hello World!"; //要注意这里的定义要为数组
puts(strlwr(s));
```



#### `strupr`

  功能是将字符串中的S参数转换为大写形式

`char *strupr(char *s);`

```c
char *strupr(char *s);

char s[] = "Hello World!"; //要注意这里的定义要为数组
puts(strupr(s));
```



####`strtok`

分解字符串为一组字符串

`char *strtok(char s[], const char *delim);`

```c
char *strtok(char s[], const char *delim);

char* p = NULL;
char s[] = "Hello,World,i,am,sam";
int i = 1;

p = strtok(s , ",");
if(p!=NULL)
    printf("第%d个串为%s\n",i,p);

while(1){
    i++;
    p = strtok(NULL,",");   //这里要注意第二个串开始,主串名改用NULL
    if(p!=NULL)
    	printf("第%d个串为%s\n",i,p);
	else{
    	printf("没串了\n");
    	break;
    }
} 
```

```c
char *strtok(char s[], const char *delim);
//指针修改版

char* p = NULL;
char s[] = "Hello,World,i,am,sam";
char *psubs[10];

int i = 1;

p = strtok(s , ",");
if(p!=NULL)
    psubs[i-1] = p;

while(1){
    i++;
    p = strtok(NULL,",");   //这里要注意第二个串开始,主串名改用NULL
    if(p!=NULL)
    	psubs[i-1] = p;
	else{
    	break;
    }
} 

int j;
for(j=0; j< i-1;j++){
    puts(psubs[j]);
}
printf("没串了\n");
```



## 结构体

* ==数组==是同一种类型数据的几何,==结构体==是多种类型的数据的集合

* 特点是:数据多,丰富,大

* ==定义结构体的方式==

  ```c
  struct Name{
      int xxxx;
      char xxx[];
      void (*p)(char *xxx);
  };     //记住末尾一定要加分号
  ```

  

* 赋值结构体的方式

  ```c
  int             a    =  10;
  struct Name     stu1 = {xx,"aaa"};
  
  printf("%d(%s)", stu1.xxx);
  
  //注意赋值字符时要用strcpy
  strcpy(test.name, "xxx");
  ```

  

* ```c
  struct Datas{
      char *p;   //这里定义到的是野指针,使用时一定要赋予它空间(malloc...)
  };//这种方式不可取
  
  struct Test{
    	char p[128];  
  };//前期最好用这种,出错的概率比较小
  ```

* 





# Linux

## 基本常识

* 嵌入式系统功耗、移动性等方面具有传统计算机所不具备的优点

* LInux内核支持x86、PowerPC、ARM等主流的CPU架构，移植性能好

* 嵌入式系统——用于控制、监视或者辅助操作机器和设备的装置

* 掌握Linux常用的shell命令，如ls、cd、cp、rm、cp、chmod、file、mv等。

* 熟练掌握Linux文件IO函数open()/read()/write()/lseek()/close()等应用方法。

* 掌握mmap()函数实现显存映射的方法。

* 熟悉智能家居系统的硬件框架。

*  线程和进程的区别在于,子进程和父进程有不同的代码和数据空间,而多个线程则共享数据空间,每个线程有自己的执行堆栈和程序计数器为其执行上下文.多线程主要是为了节约CPU时间,发挥利用,根据具体情况而定. 线程的运行中需要使用计算机的内存资源和CPU。

* IO程序设计，通过引脚，找到寄存器，寄存器是通过地址来访问的，每个寄存器都有自己的地址。

* 将一个引脚配置成IO功能

  ii.再该引脚的IO功能配置成输出

  输出----处理器控制外面的设备：如LED、BEEP

  输入----处理器检测外面设备的状态：KEY

  iii.引脚输出低电平，LED亮、引脚输出高电平,LED灭

* 驱动程序的设计流程

  设计module：module是Linux内核模块，Linux设备驱动程序是工作在Linux内核中的，驱动程序是放在module中的，每个驱动都需要一个module。

  一个硬件---一个驱动----放在一个module中--->安装到Linux内核。

  module相当于是一个盒子，里面放了驱动程序。

* ==按键的驱动程序设计==

  1、设计一个module

  2、使用struct cdev 定义一个变量

  3、给cdev申请设备号

  4、定义并初始化文件操作集---file_operations

  5、cdev的初始化

  gec6818_led_dev.owner = THIS_MODULE;

  cdev_init(&gec6818_led_dev, &gec6818_led_fops);

  6、将cdev加入内核 cdev_add()

  7、创建class： class_create()

  8、创建device  device_create()

  9、申请寄存器的物理地址作为一个资源（不是必需的）

  request_mem_region()

  10、得到寄存器物理地址对一个的虚拟地址

    寄存器的虚拟地址=ioremap(寄存器的物理地址)

  11、 通过虚拟地址访问寄存器

    1）将引脚配成IO（GPIOxALTFN0 和 GPIOxALTFN1）

    2）将IO配置成输入（GPIOxOUTENB）

    3）读取引脚输入的电平（GPIOxPAD）

* module的描述，设计一个cdev，给cdev申请设备号

* 获取设备号有两种方法：

  动态分配----由内核分配一个空闲的设备号

  静态注册----指定一个设备号，注册到内核

* 驱动程序的编译和调试方法

  裸机程序是与操作系统无关的、直接控制硬件的程序，所以不能直接用 arm-linux-gcc 编译，需要使用 Makefile 文件调用编译器、链接器和可执行程序转换工具进行程序编译和处理，最后生成*.bin 文件。中 0x40000000 地址是 GEC6818 平台的 DDR3 内存首地址，编译器将可执行程序定位到 0x40000000 地址；led.bin 文件下载地址和执行地址也是该地址。

  调试的时候可以借助U-Boot 工具。U-Boot 是一个嵌入式平台上广泛使用的 bootloader，类似于 PC 机的 BIOS， 主要完成硬件平台的初始化和嵌入式 Linux 内核的加载等功能。U-Boot 是一个直接在硬件平台上运行的裸机程序，提供了 U-Boot 环境变量配置、文件下载和运行等功能的小工具。编译好的 led.bin 裸机程序可以通过 U-Boot 下载并运行。 





## 目录

1. Linux发展过程
2. ARM体系结构特点、常见的ARM结构微处理器
3. Linux安装配置
4. Linux的基础操作，包括文件管理、用户管理以及网络管理等部分
5. Linux系统C语言的特点，如常用的头文件及编译环境变量的配置、c语言程序的设计过程、编译器GCC、调试器GDB的用法，工程管理器make的用法，ARM平台交叉编译环境的搭建
6. Linux系统移植，在嵌入式硬件上安装Linux操作系统的过程，分为内核引导程序Bootloader、Linux内核、文件系统等部分的移植
7. LInux并发程序设计，Linux多进程程序设计、进程之间的通信以及多线程程序设计
8. Linux网络编程
9. Linux文件编程，包含Linux文件的概念，文件的读写操作，加锁访问，文件的并行访问复用模型等
10. LInux设备驱动程序设计介绍了设备驱动模型、总线型的设备驱动程序开发，中断设备驱动程序、混杂型设备驱动程序开发



##基本指令

* `xrandr`调分辨率
* `ctrl + L`清屏

<img src="image-20210714153420476.png" alt="image-20210714153420476" style="zoom:150%;" />

### man函数的用法

man命令后面加数字是有特定意义的，比如常用的查询shell命令的帮助信息，实际上是man 1。

man 2表示查询的是系统内核可调用的函数；

man 3表示查询的是常用的函数与函数库（大部分是C函数库）

###open

* open的返回值是文件描述符(==很重要==)

#### 头文件及说明

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int open(const char *pathname, int flags);
int open(const char *pathname, int flags, mode_t mode);

int creat(const char *pathname, mode_t mode);

```



#### open的实例

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    int fd;
    char* buf = "the example of 'Write'";

    fd = open("./file1", O_RDWR);

    printf("fd = %d\n", fd);
    if (fd <= 0) {
        printf("open file failed");

        fd = open("./file1", O_RDWR | O_CREAT, 0600);
        if (fd > 0) {
            printf("creat and open successful\n");
            printf("fd = %d\n", fd);
        }
    }

    //ssize_t write(int fd, const void *buf, size_t count);
    write(fd,buf, strlen(buf));

    close(fd); //写完文件要记得关闭文件

    return 0;
}
```

`fd`为==文件描述符==

#### 程序中0600补充

r--可读 (4)  w--可写(2)  x--可执行(1)   0600中的6就是4+2  后面两个0分别代表同组和其他组



### write

```c
//ssize_t write(int fd, const void *buf, size_t count);

write(fd,buf, strlen(buf));
```

写入数据

#### lseek

```c
#include <sys/types.h>
#include <unistd.h>

off_t lseek(int fd, off_t offset, int whence);
```

