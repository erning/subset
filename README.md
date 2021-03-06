
[![Build Status](https://travis-ci.org/erning/subset.png)](https://travis-ci.org/erning/subset)

## Quick Start

```text
$ git clone git://github.com/erning/subset.git
$ cd subset
$ script/bootstrap
```

### Run it
```text
$ .bootstrap/ve subset 'age>21' 'age>20'

"age>21" is subset of "age>20"
"age>20" is NOT subset of "age>21"
```

### Tests
```
$ .bootstrap/ve python tests.py

..........
----------------------------------------------------------------------
Ran 10 tests in 0.044s

OK
```

## 原始问题

请写一个算法，判断一个查询表达式是不是另外一个查询表达式的子集。

稍微加一点解释

就拿SQL语句为例，如果查询A是

    age > 21

查询B是

    age > 20

我们知道，A所代表的集合是B所代表的集合的子集。凡是满足A的条件的记录，也一定满足B的条件。我需要一个算法，在给出任意两个表达式以后，判断一个是不是另外一个的子集。

    if($queryA->isSubSet($queryB)) { echo(“A is subset of B”);}
    
为了简单起见，只需要实现最简单的AND, OR逻辑操作，大于，等于，小于三种比较操作就好。最好用PHP，其他语言，比如Java也没问题。

这有什么用呢？

这是个我们不到10人的技术团队日常典型需要解决的问题。给个例子：百姓网为了应付更大的搜索数据量，把搜索分布在多个城市的多台服务器上。系统管理员可以根据数据的使用频度等规律，配置几个不同的数据库（MySQL的，和Solr的）。这样，当有一个新的广告出来后，子集算法根据搜索库的配置查询就可以决定，它更新到哪一个或多个库里面。

查询的时候，如果确认给定的查询条件是以前配置的一个库的子集，就可以只从那个库里查询了。这可以让我们轻松地配置几十个搜索库，而不用改一行代码。

http://blog.baixing.com/?p=9
