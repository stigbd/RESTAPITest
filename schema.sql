drop table if exists request;
create table request (
  id integer primary key autoincrement,
  verb text not null,
  url text not null
);

drop table if exists response;
create table response (
  id integer primary key autoincrement,
  fk_request_id integer not null,
  status_code text not null,
  body text
);

drop table if exists request_header;
create table request_header (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists response_header;
create table response_header (
  id integer primary key autoincrement,
  name text not null
);
