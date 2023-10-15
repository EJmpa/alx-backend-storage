-- creates a stored procedure ComputeAverageScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Calculate the average score
    SELECT AVG(score)
    INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average score for the user
    IF avg_score IS NOT NULL THEN  -- Check if there are records for the user
        UPDATE users
        SET average_score = avg_score
        WHERE id = user_id;
    ELSE
        -- Handle the case where there are no records for the user
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;
END;
//
DELIMITER ;
