create database dartboard;

create table dartboard.winners_corner
(
  player varchar(100) not null,
  win_count numeric not null,
  game_type varchar(50) not null,
  bb_y_n varchar(1) not null,
  last_updated timestamp default current_timestamp,
  primary key (player)
)

create table dartboard.player_profiles
(
  player_name varchar(100) not null,
  description varchar (350),
  win_count numeric not null,
  date_added timestamp default current_timestamp,
  primary key (player_name)
)

create table dartboard.current_cricket_game
(
  player_name varchar(100) not null,
  count_12 numeric,
  count_13 numeric,
  count_14 numeric,
  count_15 numeric,
  count_16 numeric,
  count_17 numeric,
  count_18 numeric,
  count_19 numeric,
  count_20 numeric,
  count_B numeric,
  primary key (player_name)
)
