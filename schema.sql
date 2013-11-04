drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  verb text not null,
  url text not null,
  body text
);
