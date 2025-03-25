## Linux

### 一、远程连接Linux系统

### 二、指令系统

1. 命令基础格式：command [-options] [parameter]

   一定要记住linux指令的三要素：指令，选项，参数

2. ls 指令

   ```bash
   ls [-a -h -l] [linux路径]
   ```

   -a 是all的意思，表示列出所有的选项，包括隐藏文件。

   -l 是list的意思，表示以列表排列像是竖向展示文件。

   上述两种可以同时使用。

   -h 是human的意思，表示以人类易于阅读的形式显示信息。

   -h必须和-l一起使用，否则不会有特殊作用。

   ls -l 显示的结果中，d表示目录（文件夹），l表示链接，-表示普通文件，b表示块设备文件，c表示字符设备文件。

3. cd 指令不使用参数，则直接回到用户的home目录。

4. pwd 指令：print work director **打印工作目录**。

5. ~是特殊路径符，表示home目录。

   cd .. ：切换上一级目录。

   cd ../.. ：切换上二级目录。

6. mkdir 指令

   ```bash
   mkdir [-p] linux路径
   ```

   -p 是parents的意思，表示可以**创建多层路径**。如果没有-p选项的话，只能**创建一个文件夹**。

   mkdir 指令需要权限，没有权限创建不了。

7. 文件操作指令：touch-cat-more

   touch 指令

   ```bash
   touch linux路径
   ```

   `touch`指令具有**创建文件**的作用。

   cat 指令

   `cat`指令是`concatenate`的缩写，意思是 “连接”“串联”，可以用来**查看文件内容**。

   more 指令

   和cat指令相同的功能，只不过more指令支持翻页。按空格翻页，按q退出。

8. 文件操作命令：cp-mv-rm

   cp 指令

   ```bash
   cp [-r] 参数1 参数2
   ```

   用来**复制**文件，前者源路径，后者目的路径。

   mv 指令

   ```bash
   mv 参数1 参数2
   ```

   用来**移动文件或文件夹**，如果参数2是不存在的路径，则就有改名效果。

   rm 指令

   ```bash
   rm [-r -f] 参数1 参数2 ...... 参数N
   ```

   -r用来**删除文件夹**，-f用来强制删除。

   rm可以使用通配符*，用来做模糊匹配：

   *test，test\*，\*test\*分别表示test结尾、开头、包含的内容。

9. su - root 切换到管理员用户，exit 退出。

10. 查找指令：which-find

   which 指令：

   ```bash
   which 要查找的指令
   ```

   用于**查找指令文件所在的位置**。

   find 指令：

   ```bash
   find 起始路径 -name "被查找文件名"
   find 起始路径 -size +|-n[kMG]
   ```

   查找小于10KB的文件：-10k

   查找大于100MB的文件：+100M

   查找大于1GB的文件：+1G

11. grep 指令（global regular expression print）

    ```bash
    grep [-n] 关键字 文件路径（内容输入端口）
    ```

    grep 指令用来进行文件内容的过滤。

    关键字用""包围。

    -n表示显示过滤出来的行号。

12. wc 指令（word count）

    ```bash
    wc [-c -m -l -w] 文件路径
    ```

    wc 指令用来统计文件的行数、单词数量等。

    -c 统计字节数量

    -m 统计字符数量

    -l 统计行数

    -w 统计单词数量

13. 管道符：将管道符左边的结果作为右边的输入。

14. echo 指令

    ```bash
    echo [-e] 要输出的内容
    ```

    -e 表示要输出的内容中有转义符号。（\n 换行符；\c 清除echo结尾的换行）

    输出指令，直接输出echo后面的东西，如果害怕混淆那就用双引号括起来。

    反引号（飘号）括起来就表示输出里面的内容，例如echo \`pwd\`就表示输出当前工作目录。

15. tail 指令

    ```bash
    tail [-f -num] Linux路径
    ```

    -f 表示持续追踪输出尾部内容，程序一直运行直到程序员控制结束。

    -num 这一项应该写具体的数字，例如-5表示输出5行。

16. 重定向符：> 将左侧命令的结果**覆盖**到右侧指向的文件中；>> 将左侧命令的记过**追加**到右侧指向的文件中。

17. vi/vim编辑器

    - 命令模式

      ![image-20241225232122980](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241225232122980.png)
      ![image-20241225232412831](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241225232412831.png)
      ![image-20241225232429914](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241225232429914.png)

    - 输入模式

    - 底线命令模式

      ![image-20241225232500812](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241225232500812.png)

18. 切换用户

    ```bash
    su [-] [用户名]
    ```

    \- 表示是否在切换用户后加载环境变量。可以使用exit指令退回上一个用户，也可使用ctrl+d。

    root到普通用户无需密码，普通用户到root需要密码。

    也可使用sudo语句临时赋权。

19. - 创建用户组

       ```bash
       groupadd 用户组名
       ```

    - 删除用户组

      ```bash
      groupdel 用户组名
      ```

    - 创建用户

      ```bash
      useradd [-g -d] 用户名
      ```

      -g 指定用户的组，不指定 -g，会创建同名组并自动加入，指定 -g 需要组已经存在，如已存在同名组，必须使用-g。

      -d 指定用户HOME路径，不指定，HOME目录默认在：/home/用户名。

    - 删除用户

      ```bash
      userdel [-r] 用户名
      ```

      -r 删除用户的HOME目录，不使用 -r，删除用户时，HOME目录保留。

    - 查看用户所属组

      ```bash
      id [选项] [用户名]
      ```

      参数：用户名，被查看的用户，如果不提供则查看自身。

      选项：

      - **-u**：只显示用户 ID（UID）。例如，`id -u` 会输出当前用户的 UID。这个选项在脚本中很有用，比如判断当前用户是否为具有特定 UID 的用户（如`root`用户的 UID 为 0）。
      - **-g**：只显示用户所属主组的组 ID（GID）。它可以帮助你快速确定用户的主要组身份相关的 GID。
      - **-G**：显示用户所属的所有组的组 ID。这在需要了解用户的所有组归属情况时很有用，因为一个用户可以属于多个组。
      - **-n**：与 `-u`、`-g`、`-G` 等选项一起使用时，不显示数字 ID，而是显示对应的名称。例如，`id -un` 显示当前用户名，`id -Gn` 显示当前用户所属的所有组的名称。
      - **-r**：显示实际的 UID、GID 或组名，而不是映射后的结果。这在处理一些特殊的用户或组映射场景（如通过 NIS 或 LDAP 等）时可能会用到。

    - 修改用户所属组

      ```bash
      usermod -aG 用户组 用户名
      ```

    - 查看系统中所有用户

      ```bash
      getent passwd
      ```

      输出的结果对应：用户名:密码(x):用户ID:组ID:描述信息(无用):HOME目录:执行终端(默认bash)。

    - 查看系统中所有用户组

      ```bash
      getent group
      ```

      输出的结果对应：组名称:组认证(显示为x):组ID。

20. 权限信息

    ![image-20241226012003698](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226012003698.png)

    r 读取文件/查看目录中的文件和子目录的名称；

    w 修改文件内容/在目录中创建新的文件或子目录；

    x 执行文件/允许用户进入目录（可以更改工作目录到此文件夹）。

21. 修改权限

    ```bash
    chmod [-R] 权限 文件或文件夹
    chmod -R u=rwx,g=rx,o=x test
    chmod 751 hello.txt
    ```

    选项 -R 表示对文件夹内所有的内容全部都应用相同的操作。

    u表示user，g表示group，o表示other。

    751表示user/group/other分别取7(111,rwx)，5(101,r-x)，1(001,--x)。

22. 修改文件、文件夹所属用户组

    ```bash
    chown [-R] [用户][:][用户组] 文件或文件夹
    ```

    此指令只适用于root用户。

    选项-R表示对文件夹内所有的内容全部都应用相同的操作。

### 三、实用操作

1. 常用快捷键

   ctrl+c 强制停止

   ctrl+d 退出当前账户，包括用户、python环境等等都可以退出

   history 指令：查看历史命令

   历史命令搜索：

   1. !命令前缀，自动执行上一次匹配前缀的指令。
   2. ctrl+r，输入命令去匹配历史命令

   ctrl+a，跳到命令开头
   ctrl+e，跳到命令结尾
   ctrl+键盘左键，向左跳一个单词
   ctrl+键盘右键，向右跳一个单词

   清屏：ctrl+l 或者clear指令

2. 软件安装

   ```bash
   yum [-y] [install|remove|search] 软件名称
   apt [-y] [install|remove|search] 软件名称
   ```

   -y 是自动确认的意思，无需手动确认安装或卸载过程

   该指令需要联网和root权限。

3. systemctl 指令控制软件启动和关闭

   ```bash
   systemctl start|stop|status|enable|disable 服务名
   ```

   enable是开机自启的意思。

4. ln 指令创建软链接

   ```bash
   ln -s 参数1 参数2
   ```

   -s，创建软链接。

   参数1：被链接的文件或文件夹

   参数2：要链接去的目的地

5. 日期、时区

   ```bash
   date [-d] [+格式化字符串]
   date "+%Y-%m-%d %H:%M:%S"
   date -d "+1 day" "+%Y-%m-%d %H:%M:%S"
   2024-12-26 13:16:26
   2024-12-27 13:16:26
   ```

   字符串中的空格如果不想被理解为新参数，那就用双引号括起来。

   -d 选项是日期计算。支持year/month/day/hour/minute/second

   ![image-20241226133926246](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226133926246.png)

   修改时区到东八区：

   ```bash
   rm -f /etc/localtime
   sudo ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
   ```

   ntp 程序

   安装运行：

   ```bash
   yum -y install ntp
   systemctl start ntpd
   systemctl enable ntpd
   ```

   手动校准：

   ```bash
   ntpdate -u ntp.aliyun.com
   ```

6. 固定IP地址

   配置固定IP需要2个大步骤：

   1. 在VMware Workstation（或Fusion）中配置IP地址网关和网段（IP地址的范围）

   2. 在Linux系统中手动修改配置文件，固定IP

   具体操作：

   ![image-20241226160845649](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226160845649.png)

   ![image-20241226160920958](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226160920958.png)

   再修改配置：

   ```bash
   vim /etc/sysconfig/network-scripts/ifcfg-ens33
   ```

   在配置文件中加入如下四行：

   ```bash
   IPADDR="192.168.88.130"
   NETMASK="255.255.255.0”
   GATEWAY="192.168.88.2"
   DNS1="192.168.88.2”
   ```

   重启服务：

   ```bash
   systemctl restart network
   ```

7. 网络请求和下载

   - ping 指令

     ```bash
     ping [-c num] ip或主机名
     ```

     -c是检查的次数，不使用-c，则无限检查。

     该指令用于检查该IP地址是否可以连通。

   - wget 指令

     ```bash
     wget [-b] url
     ```

     -b是后台下载的意思。

     该指令用来下载文件。

   - curl 指令

     ```bash
     curl [-O] url
     ```

     -O用于下载文件，当url是下载链接时，可以使用此选项保存文件。

     该指令用来发起网络请求，用于下载文件、获取信息等。

8. 端口

   网络端口的概念（略）

   查看端口占用情况：

   - 使用nmap命令，查看本机端口占用情况：

     ```bash
     yum install nmap
     nmap 127.0.0.1
     ```

   - 使用netstat命令，查看指定端口的占用情况：

     ```bash
     yum -y install net-tools
     netstat -anp | grep 端口号
     ```

9. 进程管理

   - 查看系统进程信息：

     ```bash
     ps [-e -f]
     ps -ef
     ```

     -e 表示显示出全部的进程。

     -f 以完全格式化的形式展示信息（展示全部信息）。

     ![image-20241226171609731](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226171609731.png)

   - 关闭进程

     ```bash
     kill [-9] 进程ID
     ```

     -9表示强制关闭进程。

10. 主机状态监控（面试常用）

    ```bash
    top
    ```

    默认每5s刷新一次。

    ![image-20241226172113481](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226172113481.png)

    ![image-20241226174855817](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226174855817.png)

    ![image-20241226174947242](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226174947242.png)

    ![image-20241226185615329](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226185615329.png)

11. 磁盘信息监控

    ```bash
    df [-h]
    iostat [-x] [num1][num2]
    ```

    -h：以人性化单位显示。

    -x：显示更多信息。

    num1：数字，刷新间隔；num2：数字，刷新几次。

    ![image-20241226190251220](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226190251220.png)

12. 网络情况监控

    ```bash
    sar -n DEV num1 num2
    ```

    -n表示查看网络，DEV表示查看网络接口。

    num1：刷新间隔（不填就查看一次结束），num2：查看次数（不填就无限次数）。

    ![image-20241226191000031](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226191000031.png)

13. 环境变量

    查看当前系统环境变量：

    ```bash
    env
    ```

    $ 用于取“变量”的值。

    ```bash
    echo $PATH
    echo $PWD
    echo ${PATH}ABC
    ```

    临时设置变量：

    ```bash
    export 变量名=变量值
    ```

    永久生效变量

    ```bash
    # 对本用户生效：~/.bashrc文件中
    vim ~/.bashrc
    
    # 在文件中加入
    export 变量名=变量值
    
    # 之后回到终端，使用sourse
    sourse .bashrc
    
    
    # 对所有用户生效：/etc/profile文件中
    vim /etc/profile
    
    # 在文件中加入
    export 变量名=变量值
    
    # 之后回到终端，使用sourse
    sourse /etc/profile
    
    # 在配置文件中还有一种常见写法
    # 表示在原有的PATH后追加一个路径
    export PATH=$PATH:/root/myenv
    ```

14. 文件的上传和下载

    ```bash
    yum -y install lrzsz
    ```

    rz上传，sz下载。

15. 文件的压缩和解压

    - 文件压缩的两种格式：

      .tar：归档文件，简单的将文件组装到一个文件中，并没有太多文件体积的减少。

      .gz：gzip压缩算法将文件压缩到一个文件内，极大压缩文件的体积。

    - 指令：

      ```bash
      tar [-c -v -x -f -z -C] 参数1 参数2 ...... 参数N
      ```

      -c，创建压缩文件，用于压缩模式

      -v，显示压缩、解压过程，用于查看进度

      -x，解压模式

      -f，要创建的文件，或要解压的文件，-f选项必须在所有选中位置处于最后一个

      -z，gzip模式，不使用-z就是普通的tarball格式

      -C，选择解压的目的地，用于解压模式

    - 压缩的两种格式：

      ![image-20241226205308761](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226205308761.png)

    - 解压的三种格式：

      ![image-20241226205729829](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241226205729829.png)

    - zip命令压缩文件

      ```bash
      zip [-r] 参数1 参数2 ... 参数N
      zip test.zip a.txt b.txt c.txt
      zip -r test.zip test itheima a.txt
      ```

      -r，被压缩的包含文件夹的时候，需要使用-r选项,和rm、cp等命令的-r效果一致。

    - unzip命令解压文件

      ```bash
      unzip [-d] 参数
      unzip test.zip -d /home/myhome
      ```

      解压出来的文件会覆盖目录中已有的同名文件。

### 四、Shell编程基础知识

1. shell介绍：shell命令发送给linux内核去执行，操作就是计算机硬件，所以Shell是用户操作计算机硬件的桥梁。

2. shell解析器

   ```bash
   cat /etc/shells
   ```

3. shell解析器类型

   | 解析器类型    | 介绍                         |
   | ------------- | ---------------------------- |
   | /bin/sh       | UNIX最初使用的shell          |
   | /bin/bash     | sh的扩展，LinuxOS的默认shell |
   | /sbin/nologin | 不需要登录                   |
   | /bin/dash     | 需要较少空间，但交互性较差   |
   | /bin/csh      | C语言风格shell               |
   | /bin/tcsh     | C Shell的一个扩展版本        |

   查看本机shell环境的指令：

   ```bash
   echo $SHELL
   ```

4. shell脚本编写规范

   1. 文件后缀名：`.sh`

   2. 首行格式：`#!/bin/bash`，用来设置shell解析器类型。

   3. 注释方式

      1. 单行注释

         ```bash
         # 注释内容
         ```

      2. 多行注释

         ```bash
         :<<!
         # 注释内容
         !
         ```

   4. 变量声明方式：`set`

5. 脚本文件执行方式

   1. sh解析器执行：`sh 脚本文件`
   2. bash解析器执行：`bash 脚本文件`
   3. 仅路径执行（需要可执行权限）：`./脚本文件`

6. 常用系统环境变量

   ![image-20241227001714431](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227001714431.png)

7. 变量定义规则

   1. 变量名称可以有字母,数字和下划线组成,但是不能以数字开头
   2. 等号两侧不能有空格
   3. 在bash环境中,变量的默认类型都是字符串类型,无法直接进行数值运算
   4. 变量的值如果有空格,必须使用双引号括起来
   5. 不能使用Shel的关键字作为变量名称

8. 自定义局部变量值定义、查询、删除语法

   定义语法：

   ```bash
   var_name=value
   ```

   查询语法：

   ```bash
   $var_name
   ${var_name}
   两者的区别在于花括号适合拼接字符串
   ```

   删除语法：

   ```bash
   unset var_name
   ```

9. 自定义常量值定义、查询、删除语法

   定义语法：

   ```bash
   readonly var_name
   ```

   这个语法可以把原本的变量转变成常量。

   查询语法：

   ```bash
   $var_name
   ${var_name}
   两者的区别在于花括号适合拼接字符串
   ```

   删除语法：

   ```bash
   unset var_name
   ```

10. 自定义全局变量定义语法

    ```bash
    export var_name
    ```

    父子 Shell 环境：有2个 Shell 脚本文件，A.sh 和 B.sh，如果在 A.sh 脚本文件中执行了 B.sh 脚本文件,那么 A.sh 就是父Shell环境, B.sh 就是子 Shell 环境。

    在当前脚本文件中定义全局变量，这个全局变量可以在当前Shel环境与子Shell环境中都可以使用。

11. 变量类型除了系统环境变量、自定义变量，还有：

    特殊符号变量

    - $n

      用于接收脚本文件执行时传入的数据

      $1~$9，代表获取第一个参数到第九个参数，第10个参数以上格式为${数字}，$0用户获取当前脚本名称

      ```bash
      sh 脚本文件 输入参数1 输入参数2
      $1就代表输入参数1，$2代表输入参数2
      ```

    - $#

      用于获取所有输入参数的个数，常用${#}

    - $*和$@

      不使用双引号括起来，都是获取所有参数，格式一样。

      如果使用双引号，则"$*"是把所有参数都拼接成一个字符串，是一个整体；而"$@"是一组参数列表对象。

    - $?

      用于获取上一个shell命令的退出状态码，或者是函数的返回值。每一个shell命令的执行都有一个返回值，用于说明当前命令是否成功。一般来说，返回0，代表成功；非0，代表失败。

    - $\$

      用于获取当前shell环境的进程ID号

12. shell的配置文件

    - 全局配置文件

      /etc/profile

      /etc/profile.d/*.sh

      /etc/bashrc

    - 个人配置文件

      当前用户/.bash_profile

      当前用户/.bashrc

    - 创建环境变量的步骤

      1. 编辑`/etc/profile`全局配置文件

         在文件中定义变量：

         ```bash
         export ABC=VAR
         ```

      2. 重新配置文件

         ```bash
         sourse /etc/profile
         ```

      3. 在shell环境中读取系统级环境变量

         （快捷键G快速定位到末尾，gg快速定位到首行）

13. shell环境变量深入：加载流程原理

    - 交互式与非交互式shell

      交互式：与用户进行交互，用户输入，shell环境就立刻反应；

      非交互式：不需要用户参与就可以执行多个命令，比如脚本文件。

    - 登录shell与非登录shell环境

      - 登录环境：需要用户名/密码登录的shell环境；

      - 非登录环境：不需要用户名/密码进入的shell环境或执行脚本文件。加载方法就是直接输入指令：bash

      - 识别不同登录环境的方法：

        ```bash
        echo $0
        ```

        如果是-bash，表示是登录环境；如果是bash，表示是非登录环境。注意该指令不可在脚本文件中使用，因为在脚本文件中这个指令代表文件名。

        ![image-20241227171254239](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227171254239.png)

      - 不同登录环境的环境变量加载初始化流程：

        ![image-20241227170036882](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227170036882.png)

      - ```bash
        # 非登录环境
        su 用户名
        
        # 登录环境
        su 用户名 -login或-l
        ```

### 五、Shell编程语言知识

1. 字符串

   - 字符串的三种格式：

     1. 单引号方式：任何字符都是原样输出，在其中使用变量是无效的；
     2. 双引号方式（推荐）：会解析变量，但有些时候需要转义；
     3. 不用引号方式：会解析变量，但无法输入空格。

   - 获取字符串的长度

     ```bash
     ${#字符串变量名}
     ```

   - 字符串的拼接的三种方式

     1. 无符号拼接

        ```bash
        varl=abc
        var2="hello world"
        var3=${varl}${var2}
        echo $var3
        ```

     2. 双引号拼接

        ```bash
        varl=abc
        var2="hello world"
        var3="${varl}${var2}"
        echo $var3
        ```

     3. 混合拼接

        ```bash
        varl=abc
        var2="hello world"
        var3=${varl}"&"${var2}
        echo $var3
        ```

   - 字符串截取

     | 格式                       | 说明                                                         |
     | -------------------------- | ------------------------------------------------------------ |
     | **${变量名:start:length}** | start从0开始，截取length                                     |
     | **${变量名:start}**        | start从0开始，从start截取到最后                              |
     | ${变量名:0-start:length}   | start从1开始，截取length                                     |
     | ${变量名:0-start}          | start从1开始，从start截取到最后                              |
     | ${变量名#*chars}           | 从 string 字符串左边第一次出现 *chars 的位置开始，截取 *chars 右边的所有字符。 |
     | ${变量名##*chars}          | 从 string 字符串左边最后一次出现 *chars 的位置开始，截取 *chars 右边的所有字符。 |
     | ${变量名%chars*}           | 从 string 字符串右边第一次出现 *chars 的位置开始，截取 *chars 左边的所有字符。 |
     | &{变量名%%chars*}          | 从 string 字符串右边最后一次出现 *chars 的位置开始，截取 *chars 左边的所有字符。 |

     ![image-20241227173935596](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227173935596.png)

2. 数组

   1. 只支持一维数组，不支持多维数组。

   2. 定义数组的代码：

      ```bash
      array_name=(item1 item2 item3 ...)
      array_name=([索引下标1]=item1 [索引下标2]=item2 ...)
      ```

   3. 获取数组的代码：

      ```bash
      ${arr[index]}
      # 获取数组所有元素
      ${arr[*]}
      ${arr[@]}
      ```

      获取数组或某个元素长度或个数

      ```bash
      # 获取数组长度
      ${#arr[*]}
      ${#arr[@]}
      # 获取某个元素的长度
      ${#arr[index]}
      ```

      ![image-20241227183123106](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227183123106.png)

   4. 数组的拼接

      ```bash
      array_new=(${array[*]} ${array[*]} ...)
      ```

   5. 删除数组或数组元素

      ```bash
      unset array
      unset array[index]
      ```

3. 内置指令

   - 判断是否是内置指令的方法

     ```bash
     type 指令名称
     ```

     内置执行的快，脚本执行的慢。通常来说，内置命令会比外部命令执行得更快，执行外部命令时不但会触发磁盘 IO，还需要 fork 出一个单独的进程来执行，执行完成后再退出，而执行内置命令相当于调用当前 Shell进程的一个函数，还是在当前 Shell 环境进程内，减少了上下文切换。

   - 常用内置指令补充

     - alias 指令：用于给指令起别名。

       ```bash
       alias 别名="命令"
       ```

       删除别名（临时删除，永久删除需要进入配置文件删除）：

       ```bash
       unalias 别名
       unalias -a # 删除所有别名
       ```

     - read 指令：用于从标准输入中读取数据并赋值给变量。

       ```bash
       read [-options] [var1 var2 var3 ...]
       ```

       $REPLY 保存 read 最后一个读入命令的数据。

       ![image-20241227185421280](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227185421280.png)

       options参数：

       ![image-20241227185526218](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241227185526218.png)

       ```bash
       # read给多变量赋值
       read -p "请输入姓名，年龄，爱好:(20s内)" -n 3 -t 20 -s name age hobby
       ```

     - exit 指令

       exit 后面跟一个数字表示退出码，一般0表示正确，其他表示错误。

     - declare 指令

       ```bash
       declare [+/-][aArxif][变量名称=设置值]
       ```

       "-"可用来指定变量的属性，"+“则是取消变量所设的属性

       a：array，设置为普通索引数组

       A：Array，设置为 key-value 关联数组

       r：readonly，将变量设置为只读，也可以使用readonly

       x：exprot，设置变量成为全局变量，也可以使用export

       i：int，设置为整型变量

       f：function，设置为一个函数变量

4. 运算符

   1. 算术运算符

      \+ \- * / %

      expr 执行运算命令：

      ```bash
      expr $a + $b
      ```

   2. 比较运算符

      | 运算符 | 说明                                  |
      | ------ | ------------------------------------- |
      | -eq    | 等于返回1，不等返回0，[&a -eq &b]     |
      | -ne    | 等于返回0，不等返回1，[&a -ne &b]     |
      | -gt    | 大于返回1，不大返回0，[&a -gt &b]     |
      | -lt    | 小于返回1，不小返回0，[&a -lt &b]     |
      | -ge    | 大于等于返回1，小于返回0，[&a -ge &b] |
      | -le    | 小于等于返回1，大于返回0，[&a -le &b] |
      | <      | 两边没有空格，((&a<&b))               |
      | <=     | 两边没有空格，((&a<=&b))              |
      | >      | 两边没有空格，((&a>&b))               |
      | >=     | 两边没有空格，((&a>=&b))              |
      | ==     | 两边没有空格，((&a==&b))              |
      | !=     | 两边没有空格，((&a!=&b))              |

   3. 字符串比较运算符

      ![image-20241228211300811](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228211300811.png)
      ![image-20241228211241807](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228211241807.png)

      []和[[]]的区别：

      1. [[]]不会发生单词分割，直接进行比较。

         ![image-20241228211602420](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228211602420.png)

      2. []需要对<和>转义，格式为 [字符串1 \> 字符串2]。

   4. 布尔运算符

      取反符号 ：!

      ![image-20241228211953497](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228211953497.png)

      or 或运算：-o

      and 与运算：-a

      ![image-20241228212100021](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228212100021.png)

   5. 逻辑运算符

      ![image-20241228212214836](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228212214836.png)

   6. 文件测试运算符

      包括检测：文件是否存在/可读/可写/可执行/为空/是目录/是普通文件

      文件类型：-普通文件/d目录文件/l链接文件/b块设备文件/c字符设备文件/p管道文件

      ![image-20241228214048238](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228214048238.png)
      ![image-20241228214116945](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228214116945.png)
      ![image-20241228214208201](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228214208201.png)

   7. expr 命令

      ![image-20241228214904735](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228214904735.png)

   8. (()) 命令

      ![image-20241228215204231](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228215204231.png)

      括号内赋值：((变量名=整数表达式))
      括号外赋值：变量名=$((整数表达式))
      多表达式赋值：((变量名1=整数表达式1,变量名2=整数表达式2....)
      与if条件句配合使：if((整数表达式))

   9. let 指令

      let只能完成赋值，不能直接输出，不可与条件判断结合使用。

      ```bash
      let 变量名1=整数表达式1 变量名2=整数表达式2
      ```

   10. $[] 命令

       ```bash
       $[表达式]
       ```

       只对一个表达式进行计算和输出，方括号内不能赋值。

       ![image-20241228221032053](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228221032053.png)

   11. bc 命令

       `bc` 在 Linux 中是一个功能强大的任意精度计算器语言环境，主要用于执行高精度的数学计算以及进行一些简单的编程操作。

       ```bash
       bc [options] [参数]
       ```

       options

       | 选项 | 说明                                  |
       | ---- | ------------------------------------- |
       | -h   | help，帮助信息                        |
       | -v   | version，显示命令版本信息             |
       | -l   | mathlib，使用标准数学库，用到内置函数 |
       | -i   | interactive，强制交互                 |
       | -w   | warn，显示POSIX的警告信息             |
       | -s   | standard，使用POSIX标准来处理         |
       | -q   | quiet，不显示欢迎信息                 |

       内置变量：

       ![image-20241228223516494](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228223516494.png)

       scale代表小数位数；last或者.代表上次输出结果；obase规定输出数字的进制；ibase规定输入数字的进制。

       内置数学函数（需要-l参数）：

       ![image-20241228223754987](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228223754987.png)

       借助管道输出结果：

       ```bash
       echo "obase=2;7" | bc -l
       111
       ```

       通过重定向赋值多行表达式：

       ![image-20241228225123090](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228225123090.png)

       或

       ![image-20241228225244113](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241228225244113.png)

       注：得到的结果不是数组。

   12. 流程控制

       1. if-else语句

          ```bash
          if ((score<60))
          then
          	echo "不及格"
          elif ((score>=60 && score<70))
          then
          	echo "及格"
          elif ((score>=70 && score<80))
          then
          	echo "中等"
          elif ((score>=80 && score<90))
          then
          	echo "良好"
          elif ((score>=90 && score<=100))
          then
          	echo "优秀"
          else
          	echo "成绩不合法"
          fi
          ```

          如果语句不换行的话，则在条件和命令后面都加分号即可。
   
          * if语句的退出状态
   
            linux任何命令的的执行都会有一个退出状态，无论是内置命令还是外部文件命令，还是自定义的 Shell 函数，当它退出（运行结束）时，都会返回一个比较小的整数值给调用（使用）它的程序，这就是命令的退出状态。大多数命令状态0代表成功，非0代表失败，也有特殊的命令，比如 diff 命令用来比较两个文件的不同，对于"没有差别“的文件返回 0，对于“找到差别”的文件返回1，对无效文件名返回2。Shell 中，有多种方式取得命令的退出状态，其中 $? 是最常见的一种。
   
            逻辑运算就是根据命令的状态码来进行判断的。
   
       2. case 指令
   
          ```bash
          case $number in
          1)
          	echo "星期一"
          	;;
          2)
          	echo "星期二"
          	;;
          3)
          	echo "星期三"
          	;;
          4)
          	echo "星期四"
          	;;
          5)
          	echo "星期五"
          	;;
          6)
          	echo "星期六"
          	;;
          7)
          	echo "星期日"
          	;;
          *)
          	echo "输入的数字有问题"
          	;;
          esac
          ```
   
       3. while 指令
   
          ```bash
          while ((i<number))
          do
          	echo "hello${i}"
          	let i++
          	break;
          	continue;
          done
          ```
   
       4. until 指令
   
          ```bash
          until [[ $i < $number]]
          do
          	let i++
          	echo "hello${i}"
          done
          ```
   
       5. for 指令
   
          ```bash
          for var in item1 item2 item3
          do 
          	命令1
          	命令2
          	...
          done
          
          for var in {start..end}
          do
          	命令1
          	命令2
          	...
          done
          
          for((i=start;i<end;i++))
          do
          	命令
          done
          ```
   
   13. test 指令
   
       ![image-20241231160827939](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241231160827939.png)
   
       ![image-20241231160750806](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241231160750806.png)
   
   14. select 语句
   
       ```bash
       select hobby in "编程" "游戏" "篮球"
       do
       	echo $hobby
       	break
       done
       
       select hobby in "编程" "游戏" "篮球"
       do
       	case $hobby in
       		"编程")
       			echo "编程,多敲代码"
       			break
       			;;
       		"游戏")
       			echo "少玩游戏"
       			break
       			;;
       		"篮球"|"游泳")
       			echo "运动有利健康"
       			break
       			;;
       		*)
       			echo "输入错误，请重新输入"
       	esac
       done
       ```
   
   15. 系统函数
   
       - basename 函数
   
         ```bash
         basename [string/pathname] [suffix]
         ```
   
         suffix用于去掉指定的后缀名。
   
         ![image-20241231172320333](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241231172320333.png)
   
       - dirname 函数
   
         ```bash
         dirname 文件绝对路径
         ```
   
         从指定的文件绝对路径，去除文件名，返回剩下的前缀目录路。
   
   16. 自定义函数
   
       ```bash
       [function] funname ()
       {
       	命令
       	[return 返回值]
       }
       
       funname 传递参数1 传递参数2
       ```
   
       例如：
   
       ```bash
       sum()
       {
       	echo "求2个数的和"
       	read -p "请输入第一个数字:" n1
       	read -p "请输入第二个数字:" n2
       	echo "两个数字分别为 $n1 和 $n2 
       	return $(($n1+$n2))
       }
       ```
   
       有参函数：
   
       $n 来获取参数的值，$1 表示第一个参数，以此类推。
   
       ![image-20241231231247691](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241231231247691.png)
   
       ```bash
       #!/bin/bash
       funParam()
       {
       	echo "第一个参数为: $1 !"
       	echo "第二个参数为: $2 !"
       	echo "第十个参数为: ${10} !"
       	echo "参数总数有 $# 个!"
       	echo "获取所有参数作为一个字符串返回: $* !"
       # 调用函数
       funParam 1 2 3 4 5 6 7 8 9 10 22
       ```
   
       函数和shell程序比较相似，区别在于：
       Shell 程序（内置命令和外部脚本文件），外部脚本文件是在子Shel中运行，会开启独立的进程运行；
       Shell函数在当前Shell的进程中运行。
   
       验证方法：
   
       ```bash
       #!/bin/bash
       demo(){
       	echo "函数中打印当前进程ID:$$"
       	echo "当前脚本文件(she11程序)打印当前进程ID:$$"
       # 调用函数
       demo
       ```
   
   17. 重定向
   
       默认输入输出文件：
   
       每个Unix/Linux命令运行时都会打开三个文件：
   
       ![image-20241231233525607](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241231233525607.png)
   
       * 标准输入
   
         从键盘读取用户输入的数据，然后再把数据拿到Shell程序中使用。
   
         标准输入是数据默认从键盘流向程序，如果改变了它的方向，数据就从其它地方流入】这就是输入重定向。
   
       * 标准输出
   
         Shel程序产生的数据，这些数据一般都是呈现到显示器上供用户浏览查看。
   
         标准输出是数据默认从程序流向显示器，如果改变了它的方向，数据就流向其它地方，这就是输出重定向。
   
       ![image-20241231233422025](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20241231233422025.png)
   
       在输出重定向中，>代表的是覆盖输出，>>代表的是追加输出。
       fd 是文件描述符
       0 通常是标准输入（STDIN）
       1 是标准输出（STDOUT）
       2 是标准错误输出（STDERR）
       fd> 或 fd>> 中间不可以有空格。

### 六、Shell好用工具

1. cut 译为“剪切,切割”，是一个强大文本处理工具，它可以将文本按列进行划分的文本处理。cut命令逐行读入文
   本，然后按列划分字段并进行提取、输出等操作。

   ```
   cut [options] filename
   ```

   选项：

   ![image-20250104141543251](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104141543251.png)

   提取范围：

   ![image-20250104141615017](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104141615017.png)

   ![image-20250104141802753](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104141802753.png)

   ![image-20250104141932266](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104141932266.png)

   示例：切割提取bash进程的PID号

   ```bash
   ps -aux | grep bash | head -n 1 | cut -d " " -f 8
   ```

   示例：切割提取IP地址

   ```bash
   ifconfig | grep broadcast | cut -d " " -f 10
   ```

2. sed 指令

   使用sed编辑文件替换文件中的单词
   编写在文件中插入或修改行的sed程序
   使用sed作为过滤器来过滤管道数据命令

   处理数据原理：

   ![image-20250104143724560](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104143724560.png)

   ```bash
   sed [选项参数] [模式匹配/sed程序命令] [文件名]
   ```

   ![image-20250104143850545](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104143850545.png)

3. awk 指令

   ```bash
   awk 'pattern{action}' {filenames}
   ```

   ![image-20250104182024395](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104182024395.png)

   内置变量

   ![image-20250104182057071](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104182057071.png)

4. sort 指令

   ```bash
   sort (options) 参数
   ```

   ![image-20250104182508807](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250104182508807.png)

### 七、Shell常见面试题

1. 查空行
2. 求一列的和
3. 数字排序
4. 搜索指定目录下文件内容
5. 批量生成文件名
6. 批量改名
7. 批量创建用户
8. 筛选单词
9. 单词及字母去重排序
10. 扫描网络内存活主机
11. MySQL分库备份
12. MySQL数据库分库分表备份

### 八、Shell习题

1. 编写脚本判断当前用户是否为 root 用户，如果是，输出 “You are root”，若不是，输出 “You are a normal user”。

   ```bash
   #!/bin/bash
   user=$(id -un)
   if [ "$user"  == "root" ]
   then
           echo "root"
   else
           echo "nomal user"
   fi
   ```

   当使用 `$( )` 包裹一个命令时，Shell 会先执行括号内的命令，然后用该命令执行得到的结果来替换整个 `$( )` 部分。例如在 `user=$(id -un)` 中，`id -un` 这个命令会先被执行，它会返回当前用户名（以字符串形式），接着这个返回的字符串就会被赋值给变量 `user`。

   ```bash
   #!/bin/bash
   if [ "$(whoami)" == "root" ]; then
       echo "You are root"
   else
       echo "You are a normal user"
   fi
   ```

   `whoami`指令就是输出当前用户名的指令。

2. 使用 `for` 循环打印出 1 到 10 的数字，每个数字占一行。

   ```bash
   #!/bin/bash
   for((i=1;i<=10;i++))
   do
           echo $i
   done
   ```

   

