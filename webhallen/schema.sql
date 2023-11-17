CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    json TEXT
);

INSERT INTO Products (id, json) VALUES (1, '{"name": "Product 1", "price": 100}');