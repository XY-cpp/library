import toml
import os, sys
from library import app
from library.model import *
import random

config = toml.load("config.toml")

app.config["host"] = config["db"]["host"]
app.config["port"] = config["db"]["port"]
app.config["username"] = config["db"]["username"]
app.config["password"] = config["db"]["password"]
app.config["database"] = config["db"]["database"]


def init_user():
    model = Model()
    model.update("drop table if exists `user`;")
    model.update(
        "create table `user` ( \
        `id` int auto_increment primary key, \
        `username` char(128) not null unique, \
        `password` char(128) not null, \
        `name` char(15) default null, \
        `phone` char(11) default null, \
        `email` char(128) default null, \
        `admin` tinyint(3) unsigned not null default '0' comment '0为普通用户,1为管理员', \
        `last_login_time` datetime default null );"
    )
    infos = (
        ("10001", "123456", "甲", "15700169452", "admin@example.com", 1),
        ("10002", "123456", "乙", "15700169452", "admin@example.com", 1),
        ("10003", "123456", "丙", "15700169452", "admin@example.com", 1),
        ("user1", "123456", "张三", "15700169452", "user@example.com", 0),
        ("user2", "123456", "李四", "15700169452", "user@example.com", 0),
        ("user3", "123456", "王五", "15700169452", "user@example.com", 0),
        ("user4", "123456", "赵六", "15700169452", "user@example.com", 0),
    )
    for info in infos:
        model.update(
            "insert into user (`username`,`password`,`name`,`phone`,`email`,`admin`) "
            "values (%s,%s,%s,%s,%s,%s)",
            info,
        )


def init_icp():
    model = Model()
    model.update("drop table if exists `icp`;")
    model.update(
        "create table `icp`( \
        `id` int auto_increment primary key, \
        `name` char(128) not null, \
        `author` char(128) default null, \
        `press` char(128) default null, \
        `isbn` bigint unique not null, \
        `press_time` char(128), \
        `number` int not null, \
        `manager` int not null \
        ); "
    )
    infos = (
        ("追风筝的人", "[美]卡勒德·胡赛尼", "上海人民出版社", "9787208061644", "2006-5"),
        ("解忧杂货店", "[日]东野圭吾", "南海出版公司", "9787544270878", "2014-5"),
        ("小王子", "[法]圣埃克苏佩里", "人民文学出版社", "9787020042494", "2003-8"),
        ("白夜行", "[日]东野圭吾", "南海出版公司", "9787544242516", "2008-9"),
        ("围城", "钱钟书", "人民文学出版社", "9787020024759", "1991-2"),
        ("三体", "刘慈欣", "重庆出版社", "9787536692930", "2008-1"),
        ("挪威的森林", "[日]村上春树", "上海译文出版社", "9787532725694", "2001-2"),
        ("嫌疑人X的献身", "[日]东野圭吾", "南海出版公司", "9787544241694", "2008-9"),
        ("活着", "余华", "南海出版公司", "9787544210966", "1998-5"),
        ("红楼梦", "中国古典文学读本丛书", "人民文学出版社", "9787020002207", "1996-12"),
        ("百年孤独", "[哥伦比亚]加西亚·马尔克斯", "南海出版公司", "9787544253994", "2011-6"),
        ("看见", "柴静", "广西师范大学出版社", "9787549529322", "2013-1-1"),
        ("不能承受的生命之轻", "[捷克]米兰·昆德拉", "上海译文出版社", "9787532731077", "2003-7"),
        ("达·芬奇密码", "[美]丹·布朗", "上海人民出版社", "9787208050037", "2004-2"),
        ("平凡的世界（全三部）", "路遥", "人民文学出版社", "9787020049295", "2005-1"),
        ("三体Ⅱ", "刘慈欣", "重庆出版社", "9787536693968", "2008-5"),
        ("三体Ⅲ", "科幻世界·中国科幻基石丛书", "重庆出版社", "9787229030933", "2010-11"),
        ("简爱（英文全本）", "[英]夏洛蒂·勃朗特", "世界图书出版公司", "9787506261579", "2003-11"),
        ("哈利·波特与魔法石", "[英]J·K·罗琳", "人民文学出版社", "9787020033430", "2000-9"),
        ("天才在左 疯子在右", "高铭", "武汉大学出版社", "9787307075429", "2010-2"),
    )
    for info in infos:
        model.update(
            "insert into `icp` (`name`,`author`,`press`,`isbn`,`press_time`,`number`,`manager`) \
            values (%s,%s,%s,%s,%s,%s,%s)",
            (
                info[0],
                info[1],
                info[2],
                info[3],
                info[4],
                random.randint(1, 6),
                random.randint(1, 4),
            ),
        )


def init_item():
    model = Model()
    model.update("drop table if exists `item`;")
    model.update(
        "create table `item`( \
        `id` int auto_increment primary key, \
        `isbn` char(128) not null, \
        `location` char(128), \
        `status` tinyint not null default 0 comment '0未借出,1不外借,2已预约,3已借出' \
        );"
    )
    id_list = Icp.get_id_list()
    for id in id_list:
        icp = Icp(id)
        model = Model()
        for i in range(0, icp.number):
            model.update(
                "insert into item (isbn, location, status) \
                values (%s,%s,%s)",
                (
                    icp.isbn,
                    random.choice(["流通室", "阅览室", "典藏室"]),
                    random.choices([0, 1], [0.9, 0.1]),
                ),
            )


def init_borrow():
    model = Model()
    model.update("drop table if exists `borrow`;")
    model.update(
        "create table `borrow`( \
            `id` int auto_increment primary key, \
            `book_id` int not null, \
            `user_id` int not null, \
            `start` date default null, \
            `end` date default null \
        );"
    )

    id_list = Item.get_id_list()
    for i in range(0, 40):
        user_id = random.choice([4, 5, 6, 7])
        book_id = random.choice(id_list)
        id_list.remove(book_id)
        opt = random.choices([0, 1], [0.5, 0.5])[0]
        if opt == 0:
            start = datetime.date(2023, 11, 1)
            end = datetime.date(2023, 11, 2)
            opt1 = random.choice([1, 2, 3])
            if opt1 == 1:  # 借了没还
                Borrow.borrow(book_id, user_id, start)
            elif opt == 2:  # 借了已经还了
                Borrow.borrow(book_id, user_id, start, end)
            else:  # 今天借的
                Borrow.borrow(book_id, user_id)
        else:
            Borrow.reserve(book_id, user_id)


if __name__ == "__main__":
    init_user()
    init_icp()
    init_item()
    init_borrow()
