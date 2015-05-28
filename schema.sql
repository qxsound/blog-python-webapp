-- schema.sql

drop database if exists awesomeblog;

create database awesomeblog;

use awesomeblog;

grant select, insert, update, delete on awesomeblog.* to 'root'@'localhost' identified by 'root';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;




insert into users (`id`, `email`, `password`, `admin`, `name`, `image`, `created_at`) values ('0010018336417540987fff4508f43fbaed718e263442526000', 'admin@example.com', '5f4dcc3b5aa765d61d8327deb882cf99', 1, 'Administrator', 'about:{}', 1402909113.628);
insert into users (`id`, `email`, `password`, `admin`, `name`, `image`, `created_at`) values ('1010018336417540987fff4508f43fbaed718e263442526000', 'Jon@example.com', '5f4dcc3b5aa765d61d8327deb882cf99', 1, 'Administrator', 'about:{}', 1402909113.628);
insert into users (`id`, `email`, `password`, `admin`, `name`, `image`, `created_at`) values ('2010018336417540987fff4508f43fbaed718e263442526000', 'Jason@example.com', '5f4dcc3b5aa765d61d8327deb882cf99', 1, 'Administrator', 'about:{}', 1402909113.628);
insert into users (`id`, `email`, `password`, `admin`, `name`, `image`, `created_at`) values ('1110018336417540987fff4508f43fbaed718e263442526000', 'Jimmy@example.com', 'e10adc3949ba59abbe56e057f20f883e', 1, 'Administrator', 'about:{}', 1402909113.628);