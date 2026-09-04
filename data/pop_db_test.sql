INSERT INTO player(id_player, username, password, elo, email, pokemon_fan) VALUES
(999, 'admin',     '0000',  null,  'admin@project.io',      null),
(998, 'a',         'a',     1200,  'a@ensai.fr',           true),
(997, 'maurice',   '1234',  1000,  'maurice@ensai.fr',     true),
(996, 'batricia',  '9876',  1500,  'bat@project.io',       false),
(995, 'miguel',    'abcd',  1300,  'miguel@project.io',    true),
(994, 'gilbert',   'toto',  1100,  'gilbert@project.io',   false),
(993, 'junior',    'aaaa',  1200,  'junior@project.io',    true);

INSERT INTO game(id_game, id_player1, id_player2, game_mode, id_winner, detail) VALUES
(8888, 994, 993, 'coinflip', 994, 'Gilbert chose heads, result was heads'),
(8887, 997, 996, 'dice',     997, 'Maurice rolled 5, Batricia rolled 2'),
(8886, 997, 996, 'dice',     null, 'Maurice rolled 4, Batricia rolled 4'),
(8885, 996, 997, 'dice',     996, 'Batricia rolled 2, Maurice rolled 1'),
(8884, 997, 993, 'coinflip', 993, 'Maurice chose heads, result was tails');
