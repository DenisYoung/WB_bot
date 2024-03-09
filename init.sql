CREATE TABLE users_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INT,
    article INT,
    sub_status BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp
);