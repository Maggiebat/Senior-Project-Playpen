USE chessboard;

CREATE TABLE chess (
	`column` CHAR(1),
    `row` INT,
    piece CHAR(3),
	`empty` BOOLEAN
);

INSERT INTO chess(`column`, `row`, piece, `empty`) 
VALUES
('A', 1, 'WR1', FALSE),  -- White Rook 1
('B', 1, 'WN1', FALSE),  -- White Knight 1
('C', 1, 'WB1', FALSE),  -- White Bishop 1
('D', 1, 'WQ',  FALSE),  -- White Queen
('E', 1, 'WK',  FALSE),  -- White King
('F', 1, 'WB2', FALSE),  -- White Bishop 2
('G', 1, 'WN2', FALSE),  -- White Knight 2
('H', 1, 'WR2', FALSE),  -- White Rook 2
('A', 2, 'WP1', FALSE),  -- White Pawn 1
('B', 2, 'WP2', FALSE),  -- White Pawn 2
('C', 2, 'WP3', FALSE),  -- White Pawn 3
('D', 2, 'WP4', FALSE),  -- White Pawn 4
('E', 2, 'WP5', FALSE),  -- White Pawn 5
('F', 2, 'WP6', FALSE),  -- White Pawn 6
('G', 2, 'WP7', FALSE),  -- White Pawn 7
('H', 2, 'WP8', FALSE),  -- White Pawn 8
('A', 3, NULL, TRUE), 
('B', 3, NULL, TRUE), 
('C', 3, NULL, TRUE), 
('D', 3, NULL, TRUE), 
('E', 3, NULL, TRUE), 
('F', 3, NULL, TRUE), 
('G', 3, NULL, TRUE), 
('H', 3, NULL, TRUE),
('A', 4, NULL, TRUE), 
('B', 4, NULL, TRUE), 
('C', 4, NULL, TRUE), 
('D', 4, NULL, TRUE), 
('E', 4, NULL, TRUE), 
('F', 4, NULL, TRUE), 
('G', 4, NULL, TRUE), 
('H', 4, NULL, TRUE),
('A', 5, NULL, TRUE), 
('B', 5, NULL, TRUE), 
('C', 5, NULL, TRUE), 
('D', 5, NULL, TRUE), 
('E', 5, NULL, TRUE), 
('F', 5, NULL, TRUE), 
('G', 5, NULL, TRUE), 
('H', 5, NULL, TRUE),
('A', 6, NULL, TRUE), 
('B', 6, NULL, TRUE), 
('C', 6, NULL, TRUE), 
('D', 6, NULL, TRUE), 
('E', 6, NULL, TRUE), 
('F', 6, NULL, TRUE), 
('G', 6, NULL, TRUE), 
('H', 6, NULL, TRUE),
('A', 7, 'BP1', FALSE),  -- Black Pawn 1
('B', 7, 'BP2', FALSE),  -- Black Pawn 2
('C', 7, 'BP3', FALSE),  -- Black Pawn 3
('D', 7, 'BP4', FALSE),  -- Black Pawn 4
('E', 7, 'BP5', FALSE),  -- Black Pawn 5
('F', 7, 'BP6', FALSE),  -- Black Pawn 6
('G', 7, 'BP7', FALSE),  -- Black Pawn 7
('H', 7, 'BP8', FALSE),  -- Black Pawn 8
('A', 8, 'BR1', FALSE),  -- Black Rook 1
('B', 8, 'BN1', FALSE),  -- Black Knight 1
('C', 8, 'BB1', FALSE),  -- Black Bishop 1
('D', 8, 'BQ',  FALSE),  -- Black Queen
('E', 8, 'BK',  FALSE),  -- Black King
('F', 8, 'BB2', FALSE),  -- Black Bishop 2
('G', 8, 'BN2', FALSE),  -- Black Knight 2
('H', 8, 'BR2', FALSE);  -- Black Rook 2

SELECT `column`, `row`, piece, `empty` 
FROM chess 
ORDER BY `row`, `column`;

ALTER TABLE chess
ADD COLUMN visible BOOLEAN DEFAULT TRUE;
