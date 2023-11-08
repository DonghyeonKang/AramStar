-- db table 의 스키마이다.
-- er-diagram 이 수정되어 스키마를 변경해야하면 이 파일도 수정해준다. 

CREATE TABLE `menudata`(
    `id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `menu` varchar(50) UNIQUE,
    `score` INT(10) default 0,
    `reviewcount` INT(10) default 0
);

CREATE TABLE `dinner`(
    `day` varchar(2) NOT NULL,
    `course` varchar(50),
    `menu` varchar(50) NOT NULL
);


CREATE TABLE `lunch`(
    `day` varchar(2) NOT NULL,
    `course` varchar(50),
    `menu` varchar(50) NOT NULL
);

CREATE TABLE `morning`(
    `day` varchar(2) NOT NULL,
    `course` varchar(50),
    `menu` varchar(100) NOT NULL
);

CREATE TABLE `week`(
    `day` varchar(2) NOT NULL PRIMARY KEY, --키
    `date` varchar(11) NOT NULL --값
);

CREATE TABLE `users` (
    `id` INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` varchar(50) NOT NULL,
    `user_pw` TEXT NOT NULL
);

CREATE TABLE `views` (
    `views` BIGINT(5) default 0
);