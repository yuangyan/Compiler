### 任务一 词法分析

#### 一 设计思路

##### 1.1 词法设计

**1.1.1NFA设计**

在词法分析程序中，为分析器设计的文法NFA如图所示：

![image-20220415204531251](C:\Users\13692\AppData\Roaming\Typora\typora-user-images\image-20220415204531251.png)

其中可接受状态为`IDENTIFIER`，`STRING`，`DOUBLE`，`COMPLEX`，分别为标识符，字符串，浮点数，复数

转换边解释：

`i`：字母i

`e/E`：小写字母e或大写字母E

`char`：其他字母字符

`d+`：1-9的数字字符

`0`：字符0

`+/-`：字符+或字符-

`ε`：空输入

在处理前先对所有字符进行分类，简化了NFA的复杂程度

 

**1.1.2 关键词，操作符，限定符设置**

关键词：`for`, `while`, `if`, `else`, `return`, `break`, `continue`, `def`, `class`, `int`, `double`

赋值操作符：`+=`，`-=`，`*=`，`/=`，`*=`， `//=`，`%=`，`=`

二元运算符：`and`，`or`，`xor`，`==`，`**`，`+`，`-`，`*`，`/`，`//`，`%`，`in`，`<`，`>`，`<=`，`>=`

单目运算符：`！`，`not`

限定符：`.` `:` ,` ; `[` `]` {` `}` `(` `)`



##### 1.2 数据结构的设计

本程序的NFA使用python的字典，是一种索引数据结构.

设一条正规产生式为f(A, t) = Z

具体格式为NFA[(A, t)] = Z. A, t作为键，Z作为值存储，方便查找，降低算法复杂度。由于NFA中f(A, t)可能有不止一种的状态，Z用set类保存所有f(A,t)的状态

而DFA中f(A, t)只有一种状态，因此Z不再用set保存，直接赋值。

 

##### 1.3 ε-closure的计算

算法流程图如下：

![closure](C:\Users\13692\Desktop\code\Compiler\pics&charts\closure.png )