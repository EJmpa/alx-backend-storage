-- creates a stored procedure ComputeAverageScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;

    -- Calculate the total score and the number of projects
    SELECT SUM(score), COUNT(DISTINCT project_id)
    INTO total_score, total_projects
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average score for the user
    IF total_projects > 0 THEN
        UPDATE users
        SET average_score = total_score / total_projects
        WHERE id = user_id;
    ELSE
        -- Handle the case where there are no projects
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;
END;
//
DELIMITER ;

