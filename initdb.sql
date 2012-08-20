create user glasnost;
create database glasnost;
\c glasnost glasnost;
create table client (id serial primary key , ip cidr not null, time timestamp not null);
create table test (id serial primary key, test varchar(200) not null, mode
varchar(10) not null, port integer not null, client_id integer, foreign key
(client_id) references client (id) on delete cascade);
create table result (id serial primary key, test_id integer, who
varchar(10), received bigint, transmitted bigint, seconds real, rxrate real,
txrate real, foreign key (test_id) references test (id) on delete cascade);
