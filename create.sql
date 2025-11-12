CREATE DATABASE IF NOT EXISTS college;
USE college;

CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(15)
);

CREATE TABLE Parcels (
    parcel_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_name VARCHAR(100) NOT NULL,
    destination VARCHAR(255),
    weight DECIMAL(10,2),
    FOREIGN KEY (sender_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    delivery_date DATE NOT NULL,
    status VARCHAR(50),
    FOREIGN KEY (parcel_id) REFERENCES Parcels(parcel_id)
);

CREATE TABLE Offices (
    office_id INT AUTO_INCREMENT PRIMARY KEY,
    office_name VARCHAR(100) NOT NULL,
    location VARCHAR(255)
);
