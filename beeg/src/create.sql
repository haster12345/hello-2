-- USERS
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USER  FOLLOWINGS
CREATE TABLE IF NOT EXISTS user_following (
    user_id TEXT NOT NULL REFERENCES users(user_id),
    follows_id TEXT NOT NULL REFERENCES users(user_id)
);

-- RESTAURANTS
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id TEXT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    stars DECIMAL(2,1),
    review_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORIES
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- RESTAURANT CATEGORIES
CREATE TABLE IF NOT EXISTS restaurant_categories (
    restaurant_id TEXT NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (restaurant_id, category_id)
);

-- REVIEWS
CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    restaurant_id TEXT NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    rating DECIMAL(1,1) NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- VISITS
CREATE TABLE IF NOT EXISTS visits (
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    restaurant_id TEXT NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    ranking INTEGER,
    date_visited TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, restaurant_id, date_visited)
);

-- REVIEW LIKES
CREATE TABLE IF NOT EXISTS review_likes (
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    review_id TEXT NOT NULL REFERENCES reviews(review_id) ON DELETE CASCADE,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, review_id)
);

-- REVIEW PHOTOS
CREATE TABLE IF NOT EXISTS review_photos (
    review_id TEXT NOT NULL REFERENCES reviews(review_id) ON DELETE CASCADE,
    photo_url VARCHAR(500) NOT NULL,
    photo_sequence INTEGER NOT NULL,
    PRIMARY KEY (review_id, photo_sequence)
);

-- OPENING HOURS
CREATE TABLE IF NOT EXISTS opening_hours (
    restaurant_id TEXT NOT NULL REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 1 AND 7), -- 1=Monday, 7=Sunday
    open_time TEXT NOT NULL,
    close_time TEXT NOT NULL,
    PRIMARY KEY (restaurant_id, weekday)
);

-- Basic rating queries
CREATE INDEX IF NOT EXISTS idx_reviews_rating
ON reviews(rating);

-- Restaurant + rating
CREATE INDEX IF NOT EXISTS idx_reviews_restaurant_rating
ON reviews(restaurant_id, rating);

-- Restaurant + rating + time
CREATE INDEX IF NOT EXISTS idx_reviews_restaurant_rating_date
ON reviews(restaurant_id, rating, created_at);

-- User rating patterns
CREATE INDEX IF NOT EXISTS idx_reviews_user_rating
ON reviews(user_id, rating);

-- Recent high-rated reviews
CREATE INDEX IF NOT EXISTS idx_reviews_rating_date
ON reviews(rating, created_at DESC);
