-- 
--  创建用户表
-- 

drop table if exists `user`;
create table `user` (
  `id` int(11) not null,
  `pwd` char(128) not null,
  `name` char(15) default null,
  `class` char(15) default null,
  `status` tinyint(3) unsigned not null default '1' comment '0为挂失,1为正常',
  `admin` tinyint(3) unsigned not null default '0' comment '0为普通用户,1为管理员',
  `last_login_time` datetime default null,
  primary key (`id`)
);

--
-- 导入用户数据
--

lock tables `user` write;
insert into `user` values 
  (10000,'123456',null,null,1,1,'2022-11-01 13:57:33'),
  (10001,'123456','张三','初级一班',1,0,'2022-11-01 13:55:16'),
  (10002,'123456','李四','初级二班',1,0,null),
  (10003,'123456','王五','初级三班',1,0,null),
  (10004,'123456','赵六','高级一班',1,0,null),
  (10005,'123456','王二麻子','班主任',0,0,null);
unlock tables;