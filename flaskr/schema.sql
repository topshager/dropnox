DROP TABLE IF EXISTS user;


CREATE TABLE user(
  id INTEGER PRIMARY Key AUTOINCREMENT,
  username varchar(77) unique NOT  NULL,
  password varchar(55) NOT NULL
);
select * from user 
