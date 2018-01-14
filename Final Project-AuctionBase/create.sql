drop table if exists Items;
drop table if exists Categories;
drop table if exists Users;
drop table if exists Bids;
drop table if exists CurrentTime;


create table Items (
item_id INTEGER PRIMARY KEY,
name VARCHAR(100),
currently MONEY,
buy_price MONEY,
first_bid MONEY,
started DAYTIME,
ends DAYTIME,
seller_id VARCHAR(100),
number_of_bids INTEGER,
description VARCHAR(10000000),
FOREIGN KEY (seller_id) REFERENCES User(user_id) DEFERRABLE INITIALLY DEFERRED,
CHECK (ends>started)
);

create table Categories (
item_id INTEGER,
category VARCHAR(100),
PRIMARY KEY (category, item_id),
FOREIGN KEY (item_id) REFERENCES Items(item_id) DEFERRABLE INITIALLY DEFERRED
);

create table Users(
user_id VARCHAR(100) PRIMARY KEY,
rating INTEGER,
location VARCHAR(50),
country VARCHAR(50)
);


create table Bids(
item_id INTEGER,
user_id VARCHAR(100),
time DATETIME,
amount INTEGER,
UNIQUE (item_id,time),
PRIMARY KEY (item_id, user_id, amount),
FOREIGN KEY (item_id) REFERENCES Items(item_id) DEFERRABLE INITIALLY DEFERRED,
FOREIGN KEY (user_id) REFERENCES Users(user_id) DEFERRABLE INITIALLY DEFERRED
);

create table CurrentTime (
time DAYTIME
);
INSERT into CurrentTime values ('2001-12-20 00:00:01');
SELECT time from CurrentTime;


