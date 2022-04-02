[toc]
# mysql
## 安装
### linux
```bash
# 安装
sudo apt-get install mysql-server
# 修改配置文件
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf #注释掉bind-address
# 本地管理员权限登录
sudo mysql -u root -p
# 查看目前用户
show databases;
use mysql;
select User,Host from user;
# 创建用户
create user hypo identified by '123.321';
flush privileges;
# 更新加密方式(MySQL 8.0以后，默认的密码加密方式是caching_sha2_password而不是mysql_native_password,但是很多api视乎还是使用的是mysql_native_password方式)
ALTER USER 'hypo' IDENTIFIED WITH mysql_native_password BY '123.321';
flush privileges;
# 创建数据库
CREATE DATABASE test
# 授权
grant all privileges on test.* to hypo@'%';
show grants for hypo@'%';
flush privileges;
# 重启mysql-server
service mysql restart
```
## 使用python远程操作数据库
### 安装mysql.connector
```bash
pip install mysql.connector
```
### [基本操作](https://www.runoob.com/python3/python-mysql-connector.html)
```python
import mysql.connector

# 连接mysql
mydb = mysql.connector.connect(
  host="172.31.76.17",
  user="hypo",
  passwd="123.321",  
  auth_plugin='mysql_native_password', #mysql 8.0 修改了默认连接方式为caching_sha2_password，注意匹配
  database="test"
)

# 创建游标，后续数据库的操作都将通过游标进行
mycursor = mydb.cursor()

# 所有命令都将通过execute传递，返回的数据会存在mycursor中

# -----------------创建数据库
# mycursor.execute("CREATE DATABASE runoob_db")

# -----------------查看数据库
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#   print(x)

# -----------------创建表
#mycursor.execute("CREATE TABLE people (name VARCHAR(255), age int)")

# # -----------------查看表
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)

# # -----------------插入数据
# mycursor.execute("INSERT INTO people(name, age) VALUES('hypo', 20);")
# mydb.commit()    # 数据表内容有更新，必须使用到该语句

# -----------------查询
mycursor.execute("select * from people")
data_list = mycursor.fetchall() #获取返回
print(data_list)

mydb.close()
```
## SQL基本语句用法
### 连接
```sql
-- 左连接
-- 是以左表为基础，根据ON后给出的两表的条件将两表连接起来。
SELECT * FROM A LEFT JOIN B  ON A.key = B.key;
```
### if 与case
```mysql
# 1, if(三目运算)
update salary
set sex = if(sex='m', 'f', 'm')

# 2. if
IF N < 0 THEN
  RETURN NULL;
Else
...
END IF
  
# 3, case
update salary
set sex = (case sex
                when 'm' then 'f'
                else 'm'
            end
            )
```
### 修改函数中传入参数的值
如果要修改mysql函数的传入值，必须在RETURN之前写
```mysql
-- [177] 第N高的薪水
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  set N = N-1;
  RETURN (
      # Write your MySQL query statement below.  
      select Salary from 
      (select * from Employee order by Salary desc) tmp
      limit N,1
  );
END
```
### 查询某一行(按索引)
这点SQL很蛇皮，在编程语言中最简单的操作被整得这么复杂
一般结合排序一起使用
```mysql
limit y -- 分句表示: 读取 y 条数据
limit x,y -- 分句表示: 跳过 x 条数据，读取 y 条数据
limit y offset x -- 分句表示: 跳过 x 条数据，读取 y 条数据
# eg.
select * from Employee order by Salary desc limit N,1
```

### 窗口函数
```mysql
-- rank()函数 跳跃排序；
-- 比如并列第1,则两行数据(这里为rank列)都标为1,下一位将是第3名.中间的2被直接跳过了。排名存在重复值。

-- dense_rank()函数 连续排序
-- 此排序方法进行排序时，相同的排序是一样的，但是后面名次不跳跃。比如两条并列第1,则两行数据(这里为rank列)都标为1,下一个排名将是第2名。

-- row_number()函数
-- 先查出的排名在前,没有重复值

-- 用法
select id, rank() over(partition by class order by score desc) from tabel

```


## 常见错误
### Every derived table must have its own alias
mysql要求每一个派生出来的表都必须有一个自己的别名，那我给派生表加上别名即可
```mysql
-- [596] 超过5名学生的课
select class from (
    select distinct * from courses
) tmp  group by class having count(class) >= 5
```
### You can't specify target table for update in FROM clause
不能先select出同一表中的某些值，再update这个表(在同一语句中), 再包一层给个新的名字即可
```mysql
-- [196] 删除重复的电子邮箱
delete from Person where Id not in (
    -- 外包一层 避免You can't specify target table for update in FROM clause
    select t.id from (select min(Id) id from Person group by Email) t
)
```
