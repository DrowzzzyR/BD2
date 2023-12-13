USE your_database_name;

-- Добавление начальных пользователей
INSERT INTO users (username, password_hash, role) VALUES
('admin', 'hashe_admin_password', 'admin'),
('operator1', 'hashed_operator1_password', 'operator'),
('viewer1', 'hashed_viewer1_password', 'viewer');

-- Добавление начальных товаров
INSERT INTO products (name, description, price) VALUES
('Product 1', 'Description for Product 1', 50.00),
('Product 2', 'Description for Product 2', 75.00);

-- Добавление начальных поставок
INSERT INTO supplies (product_id, quantity, supply_date) VALUES
(1, 100, '2023-01-01'),
(2, 50, '2023-01-02');
