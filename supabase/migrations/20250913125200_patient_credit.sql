-- Створення бази даних для олімпійських даних
CREATE DATABASE IF NOT EXISTS olympic_dataset;

USE olympic_dataset;

-- Створення таблиці athlete_event_results з тестовими даними
CREATE TABLE IF NOT EXISTS athlete_event_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    athlete_name VARCHAR(255),
    event_name VARCHAR(255),
    medal VARCHAR(10),
    year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка тестових даних
INSERT INTO athlete_event_results (athlete_name, event_name, medal, year) VALUES
('John Smith', '100m Sprint', 'Gold', 2020),
('Jane Doe', '200m Sprint', 'Silver', 2020),
('Bob Johnson', 'Long Jump', 'Bronze', 2020),
('Alice Brown', 'High Jump', 'Gold', 2020),
('Charlie Wilson', 'Marathon', 'Silver', 2020),
('Diana Davis', 'Swimming 100m', 'Bronze', 2020),
('Eva Martinez', 'Swimming 200m', 'Gold', 2020),
('Frank Garcia', 'Cycling', 'Silver', 2020),
('Grace Lee', 'Tennis', 'Bronze', 2020),
('Henry Taylor', 'Basketball', 'Gold', 2020),
('Ivy Chen', 'Volleyball', 'Silver', 2020),
('Jack Anderson', 'Football', 'Bronze', 2020),
('Kate Miller', 'Gymnastics', 'Gold', 2020),
('Leo Rodriguez', 'Wrestling', 'Silver', 2020),
('Mia Thompson', 'Boxing', 'Bronze', 2020),
('Noah White', 'Weightlifting', 'Gold', 2020),
('Olivia Harris', 'Archery', 'Silver', 2020),
('Paul Clark', 'Shooting', 'Bronze', 2020),
('Quinn Lewis', 'Sailing', 'Gold', 2020),
('Ruby Walker', 'Equestrian', 'Silver', 2020);

-- Створення користувача для Airflow з правами доступу
CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON *.* TO 'airflow'@'%';
FLUSH PRIVILEGES;