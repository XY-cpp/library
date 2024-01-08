-- 
--  创建用户表
-- 

drop table if exists `user`;
create table `user` (
  `id` int auto_increment primary key ,
  `username` char(128) not null unique,
  `password` char(128) not null,
  `name` char(15) default null,
  `phone` char(11) default null,
  `email` char(128) default null,
  `admin` tinyint(3) unsigned not null default '0' comment '0为普通用户,1为管理员',
  `last_login_time` datetime default null
);

--
-- 导入用户数据
--

lock tables `user` write;
insert into `user` (`username`,`password`,`name`,`phone`,`email`,`admin`) 
values 
  ('admin','123456',null,'15700169452','user@example.com',1),
  ('user1','123456','张三','15700169452','user@example.com',0),
  ('user2','123456','李四','15700169452','user@example.com',0),
  ('user3','123456','王五','15700169452','user@example.com',0),
  ('user4','123456','赵六','15700169452','user@example.com',0);
unlock tables;