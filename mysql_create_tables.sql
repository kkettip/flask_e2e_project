create database `all_patients`;
use `all_patients`;

CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE
);

CREATE TABLE conditions (
    condition_id INT PRIMARY KEY AUTO_INCREMENT,
    condition_name VARCHAR(100) NOT NULL
);

CREATE TABLE patient_conditions (
    patient_condition_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    condition_id INT,
    intake_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (condition_id) REFERENCES conditions(condition_id)
);