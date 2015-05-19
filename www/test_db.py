# !/usr/bin/env python
# -*- coding:utf-8 -*-

from models import User, Blog, Comment
from transwarp import db

db.create_engine(user='root', password='root', database='awesomeblog')

# u = User(name='Test', email='test@126.com', password='abcdefghijklmn', image='about:blank')
# u.insert()
# print 'new user id:', u.id

# u1 = User.find_first('where email=?', 'test@126.com')
# print 'find user\'s name:', u1.name

# u1.delete()

# u2 = User.find_first('where email=?', 'test@126.com')
# print 'find user\'s name:', u2.name
# summary = '今天上午，魅族宣布将于6月2日在北京国家会议中心召开魅蓝新品发布会，如果不出什么意外花，新一代魅蓝系列手机就要跟我们见面了。下午，又有用户在微博上曝光了疑似魅蓝Note 2的真机照。谍照显示，虽然该机采用了实体Home键，但并不支持指纹识别功能。而现在，魅族副总裁李楠则在微博上确认了魅蓝新机即将发布的消息，而且他还表示，这款魅蓝确实会配备“腰圆”键，但并不支持指纹识别功能。'
# content = '那么，好端端取消小圆圈，换成Home键干啥呢？李楠表示这是来“革Android系统返回键命”的，看来魅族又要在操作方式上有所创新了。今天上午，魅族宣布将于6月2日在北京国家会议中心召开魅蓝新品发布会，如果不出什么意外花，新一代魅蓝系列手机就要跟我们见面了。下午，又有用户在微博上曝光了疑似魅蓝Note 2的真机照。谍照显示，虽然该机采用了实体Home键，但并不支持指纹识别功能。而现在，魅族副总裁李楠则在微博上确认了魅蓝新机即将发布的消息，而且他还表示，这款魅蓝确实会配备“腰圆”键，但并不支持指纹识别功能。'
# name = 'Meizu'
# user_name = 'Administrator'
# b = Blog(name=name, user_name=user_name, content=content, summary=summary)
# b.insert()

# summary = '小米已成立5年之久，旗下的智能手机以及平板电脑正在中国热销。现在，该公司打算进军欧美市场，但准备销售的产品并非国人熟知的手机和平板。周一夜间，小米针对美国消费者的在线商店正式上线，各种配件陈列其中，包括移动电源、售价为80美元的Mi耳机以及15美元的Mi Band健身追踪器。周二，该商店还将出现在英国、德国以及法国。'
# content = '此举意味着小米向进军西方市场迈出了关键一步。过去，小米一直以低价智能手机厂商的形象示人，在包括印度、马来西亚以及印度尼西亚在内的发展中国家销售自己的产品但小米的野心不仅止于此。小米全球副总裁雨果·巴拉（Hugo Barra）于三月表示，公司将自身定位为一个引领生活方式的品牌。去年12月，小米成为世界上最具价值的初创公司，在成功融得11亿美元之后，公司的估值达到450亿美元。小米对中国消费者产生了巨大的吸引力，使得人们经常将其拿来与苹果比较。小米创始人和CEO雷军的一举一动都受到已逝苹果CEO史蒂夫·乔布斯的影响。小米的新品通常在数分钟内即告售罄。例如，4月，200万台智能手机在12小时内便被消费者一扫而光。今年一季度，小米在中国市场售出1350万台智能手机，仅次于苹果，后者的数字为1450万台。而华为、联想以及三星则落在小米身后。'
# name = 'Xiaomi'
# user_name = 'Administrator'
# b = Blog(name=name, user_name=user_name, content=content, summary=summary)
# b.insert()

# summary = '在华为手机产品中，P系列一直定位于华为手机中的高端产品。2014年华为P7的推出经过了一年的市场论证，代表着国产机高端水平的P7在销量和用户认可度方面取得了一个不错的成绩。而一年后的今天，作为P7的后续机型华为P8在P7的基础上进行了全方面的升级，P8的体验到底怎样？P8还能否再续P7的成功传奇，下面我们就对它进行一个全方面的评测，一同来看它到底表现如何？'
# content = ''
# name = 'Huawei'
# user_name = 'Administrator'
# b = Blog(name=name, user_name=user_name, content=content, summary=summary)
# b.insert()

summary = '锤子科技创始人罗永浩今日在其个人微博上吐槽日本手机，称“设计糟糕、系统难用”。并表示出了要扩展日本市场的意愿。原微博指出：“在东京出差，到大型卖场看了看，发现到处都是设计糟糕、系统难用的手机…同事们聊了几句，想到要发布的不止一款优秀产品，决定“说干就干”：'
content = ''
name = '锤子'
user_name = 'Administrator'
b = Blog(name=name, user_name=user_name, content=content, summary=summary)
b.insert()

summary = '三星“一年双旗舰”的更新周期已经定型，在今年3月召开的MWC大展上公布Galaxy S6/S6 Edge之后另一款旗舰机型Galaxy Note 5也将于今年8月下旬9月上旬召开的IFA大会上亮相。但最新消息指出三星可能会跳出这传统的更新周期，来自韩媒报道称Galaxy Note 5及其弧形版本有望在今年7月底就会上架发售。'
content = ''
name = '三星'
user_name = 'Administrator'
b = Blog(name=name, user_name=user_name, content=content, summary=summary)
b.insert()