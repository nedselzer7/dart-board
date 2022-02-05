insert into dartboard.winners_corner(player, win_count, game_type, bb_y_n)
  values ('Test Player', 0, 'Cricket', 'Y');

insert into dartboard.player_profiles(player_name, description, win_count)
  values ('Test Player', 'This is a test player with no name and no story', 0);

insert into dartboard.player_profiles(player_name, description, win_count)
  values ('Dummy Player', 'This is a dummy player with no name and no story', 2);

insert into dartboard.current_cricket_game(player_name, count_12, count_13,
  count_14, count_15, count_16, count_17, count_18, count_19, count_20, count_B)
  values ('Dummy Player', 0, 0, 1, 0, 2, 3, 2, 1, 0, 1);

insert into dartboard.current_cricket_game(player_name, count_12, count_13,
  count_14, count_15, count_16, count_17, count_18, count_19, count_20, count_B)
  values ('Test Player', 1, 1, 0, 2, 1, 0, 1, 3, 1, 2);
