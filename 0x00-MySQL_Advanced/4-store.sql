-- create trigger after an order has been made
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMITER $$
CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
FOR EACH Row
BEGIN
	UPDATE items
		SET quantity = quantity - NEW.number
		WHERE name = NEW.item_name;
END $$
DELIMITER ;
