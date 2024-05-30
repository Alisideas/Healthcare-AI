CREATE DATABASE healthcare_assistance;

USE healthcare_assistance;

CREATE TABLE chat_log (
    id INT PRIMARY KEY,
    user_input TEXT NOT NULL,
    assistant_reply TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
