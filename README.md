# hq
my code


比如一个group开了两个协程，每个协程各对应一个函数。group.join就需要等这两个协程都完成再处理
不同的组用来区别不同功能
每个组可以有自己的的上下文关系
如果没关系就可以分不同组
协程不管分不分组都是单核
threding是多线程，有几个核就可以起几个线程
---------------------------------------------------------
想要充分地使用多核CPU的资源，在python中大部分情况需要使用多进程
multiprocessing 对cpu的使用更充分
协程比线程高效，协程是迷你线程
可以用多进程和协程，协程是程序切换上下文，线程是系统切换，协程高效。
