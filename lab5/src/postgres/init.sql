GRANT ALL PRIVILEGES ON DATABASE pg_db TO my_admin;

CREATE TABLE init_table (
    id serial PRIMARY KEY,
    message_body VARCHAR(200)
);

-- INSERT INTO init_table (message_body) VALUES ('hey'), ('you');