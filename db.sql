-- 
--  创建用户表
-- 
drop table if exists `user`;

create table `user` (
  `id` int auto_increment primary key,
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
insert into `user`
  (`username`,`password`,`name`,`phone`,`email`,`admin`)
values
  ('10001', '123456', '甲', '15700169452', 'admin@example.com', 1),
  ('10002', '123456', '乙', '15700169452', 'admin@example.com', 1),
  ('10003', '123456', '丙', '15700169452', 'admin@example.com', 1),
  ('user1', '123456', '张三', '15700169452', 'user@example.com', 0),
  ('user2', '123456', '李四', '15700169452', 'user@example.com', 0),
  ('user3', '123456', '王五', '15700169452', 'user@example.com', 0),
  ('user4', '123456', '赵六', '15700169452', 'user@example.com', 0);

-- 
-- 创建图书信息表
-- 
drop table if exists `icp`;

create table `icp`(
  `id` int auto_increment primary key,
  `name` char(128) not null,
  `author` char(128) default null,
  `press` char(128) default null,
  `isbn` bigint unique not null,
  `press_time` char(128),
  `number` int not null,
  `manager` int not null
);

-- 
-- 导入图书信息数据
-- 
insert into `icp` (`name`,`author`,`press`,`isbn`,`press_time`,`number`,`manager`)
values
  ("追风筝的人","[美]卡勒德·胡赛尼","上海人民出版社","9787208061644","2006-5",4,2),
  ("解忧杂货店","[日]东野圭吾","南海出版公司","9787544270878","2014-5",4,3),
  ("小王子","[法]圣埃克苏佩里","人民文学出版社","9787020042494","2003-8",4,3),
  ("白夜行","[日]东野圭吾","南海出版公司","9787544242516","2008-9",3,3),
  ("围城","钱钟书","人民文学出版社","9787020024759","1991-2",3,3),
  ("三体","刘慈欣","重庆出版社","9787536692930","2008-1",3,3),
  ("挪威的森林","[日]村上春树","上海译文出版社","9787532725694","2001-2",1,2),
  ("嫌疑人X的献身","[日]东野圭吾","南海出版公司","9787544241694","2008-9",4,3),
  ("活着","余华","南海出版公司","9787544210966","1998-5",4,1),
  ("红楼梦","中国古典文学读本丛书","人民文学出版社","9787020002207","1996-12",5,1),
  ("百年孤独","[哥伦比亚]加西亚·马尔克斯","南海出版公司","9787544253994","2011-6",5,1),
  ("看见","柴静","广西师范大学出版社","9787549529322","2013-1-1",4,3),
  ("不能承受的生命之轻","[捷克]米兰·昆德拉","上海译文出版社","9787532731077","2003-7",1,1),
  ("达·芬奇密码","[美]丹·布朗","上海人民出版社","9787208050037","2004-2",1,3),
  ("平凡的世界（全三部）","路遥","人民文学出版社","9787020049295","2005-1",4,1),
  ("三体Ⅱ","刘慈欣","重庆出版社","9787536693968","2008-5",1,3),
  ("三体Ⅲ","科幻世界·中国科幻基石丛书","重庆出版社","9787229030933","2010-11",4,1),
  ("简爱（英文全本）","[英]夏洛蒂·勃朗特","世界图书出版公司","9787506261579","2003-11",5,3),
  ("哈利·波特与魔法石","[英]J·K·罗琳","人民文学出版社","9787020033430","2000-9",2,1),
  ("天才在左 疯子在右","高铭","武汉大学出版社","9787307075429","2010-2",5,1);

-- 
-- 创建图书状态表
-- 
drop table if exists `book`;

create table `book`(
  `id` int auto_increment primary key,
  `isbn` char(128) not null,
  `location` char(128) ,
  `status` tinyint not null default 0 comment '0未借出,1已预约,2已借出,3不外借'
);

-- 
-- 导入图书状态数据
-- 
insert into `book` (`isbn`)
with recursive t(n) as (
  select 1
  union all
  select n+1 
  from t 
  where n<(
    select max(`number`)
    from `icp`
    lock in share mode 
  )
) 
select `isbn`
from `icp`
cross join t
where t.n <= `icp`.`number`;