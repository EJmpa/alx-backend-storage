-- Create a trigger to update item quantity after adding a new order
DELIMITER //
CREATE TRIGGER update_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item_quantity INT;
    
    -- Get the current quantity of the item
    SELECT quantity INTO item_quantity
    FROM items
    WHERE name = NEW.item_name;
    
    -- Update the item quantity after subtracting the number of items in the order
    UPDATE items
    SET quantity = GREATEST(item_quantity - NEW.number, 0)
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;

