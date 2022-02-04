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

insert into dartboard.winners_corner(player, win_count, game_type, bb_y_n)
  values ('Test Player', 0, 'Cricket', 'Y');

create table dartboard.player_profiles
(
  player_name varchar(100) not null,
  description varchar (350),
  win_count numeric not null,
  date_added timestamp default current_timestamp,
  primary key (player_name)
)
