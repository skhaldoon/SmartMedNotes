/*Database Creation*/
/*CREATE DATABASE SmartMedNotes;*/

USE SmartMedNotes;
/*Users Table Creation*/
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),users
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(50),
    date_registered DATETIME
);
