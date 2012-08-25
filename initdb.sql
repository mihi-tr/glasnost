create user glasnost;
create database glasnost;
\c glasnost glasnost;
create table asn (asn int primary key, owner varchar(500));
create table client (id serial primary key , ip cidr not null, time
timestamp not null, asn integer, cc varchar(2), foreign key (asn)
references asn (asn));
create table test (id serial primary key, test varchar(200) not null, mode
varchar(10) not null, port integer not null, client_id integer, foreign key
(client_id) references client (id) on delete cascade);
create table result (id serial primary key, test_id integer, who
varchar(10), received bigint, transmitted bigint, seconds real, rxrate real,
txrate real, foreign key (test_id) references test (id) on delete cascade);
create table client_results(id integer not null, ip cidr not null, asn
integer not null, time timestamp not null, cc varchar(2) not null, test
varchar(50) not null, rating real not null);
create table country_results(cc varchar(2) not null, test varchar(50)
not null, total int not null, shaped int default 0);
create table provider_results(owner varchar(500), test varchar(50), total
int, shaped int);
