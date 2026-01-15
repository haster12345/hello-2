CREATE OR REPLACE FUNCTION increment_review_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE restaurants
    SET review_count = COALESCE(review_count, 0) + 1
    WHERE restaurant_id = NEW.restaurant_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_increment_review_count
AFTER INSERT ON reviews
FOR EACH ROW
EXECUTE FUNCTION increment_review_count();

CREATE OR REPLACE FUNCTION decrement_review_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE restaurants
    SET review_count = GREATEST(COALESCE(review_count, 0) - 1, 0)
    WHERE restaurant_id = OLD.restaurant_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_decrement_review_count
AFTER DELETE ON reviews
FOR EACH ROW
EXECUTE FUNCTION decrement_review_count();
