drop table if exists numbers;

-- create table
create table numbers (
    id   serial,
    data numeric
);

-- insert random values
insert into numbers
    select id, random()
    from generate_series(1, 10) AS id;
