## 一、DDL





## 二、系统变量

使用指令：

```sql
show variables;
show variables like '%slow_query_log%';
set global slow_query_log = 1; 
```

可以查看所有的系统变量。

![image-20250108171352907](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250108171352907.png)

![image-20250108171438696](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250108171438696.png)

与`global`相对应的是`session`。当使用`set session`（或者`set @@session`）来设置变量时，是在设置会话变量。会话变量只对当前客户端连接（会话）有效。例如，`set session slow_query_log = 0`只会在当前会话中关闭慢查询日志功能，而不会影响其他会话和服务器的全局设置。会话变量的初始值通常是从对应的全局变量继承而来的。例如，当一个新的客户端连接到`MySQL`服务器时，其`slow_query_log`会话变量的值会默认等于全局`slow_query_log`变量的值。

`persist`用于设置持久化的全局变量。当使用`set persist`来设置变量时，不仅会改变当前运行的`MySQL`服务器的全局变量的值，还会将这个变量设置保存到`MySQL`的数据目录下的配置文件（如`mysqld-auto.cnf`）中。这样，下次启动`MySQL`服务器时，这个变量会自动加载设置的值。`persist_only`类似，但它只将变量设置保存到配置文件中，而不会立即改变当前服务器运行中的变量值。

![image-20250108171816729](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250108171816729.png)

## 三、数据库覆盖索引