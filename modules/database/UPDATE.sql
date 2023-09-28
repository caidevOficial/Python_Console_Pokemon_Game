-- SQLite
UPDATE `trainer_scores`
SET `score` = 0
WHERE `score` < 0;