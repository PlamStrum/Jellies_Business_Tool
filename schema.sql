-- 1. Create the Jellies database (if it doesn't already exist)
CREATE DATABASE IF NOT EXISTS Jellies;
USE Jellies;

-- 2. CustomerData table
CREATE TABLE IF NOT EXISTS CustomerData (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_name VARCHAR(255) NOT NULL,
  client_address TEXT NOT NULL,
  city VARCHAR(100) NOT NULL
);

-- 3. Inventory table
CREATE TABLE IF NOT EXISTS Inventory (
  id INT AUTO_INCREMENT PRIMARY KEY,
  job_id INT NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  product_price DECIMAL(10,2) NOT NULL,
  shop_name VARCHAR(255) NOT NULL,
  purchase_date DATE NOT NULL,
  FOREIGN KEY (job_id) REFERENCES CustomerData(id)
);

-- 4. BusinessIndex table
CREATE TABLE IF NOT EXISTS BusinessIndex (
  id INT AUTO_INCREMENT PRIMARY KEY,
  job_id INT NOT NULL,
  transport_method VARCHAR(100) NOT NULL,
  employee_name VARCHAR(255) NOT NULL,
  geo_data TEXT,
  additional_notes TEXT,
  FOREIGN KEY (job_id) REFERENCES CustomerData(id)
);
