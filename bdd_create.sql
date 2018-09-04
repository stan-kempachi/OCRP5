DROP DATABASE IF EXISTS openfoodfacts;

CREATE DATABASE openfoodfacts CHARACTER SET 'utf8';

USE openfoodfacts;

CREATE TABLE IF NOT EXISTS Food(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(150) NOT NULL,
	categories_id VARCHAR(400) NOT NULL,
	nutri_score CHAR(1),
	url VARCHAR(150),
	stores VARCHAR(150),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;
	
CREATE TABLE IF NOT EXISTS Categories(
	id VARCHAR(400) NOT NULL,
	name VARCHAR(100) NOT NULL,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Backup(
	id INT UNSIGNED AUTO_INCREMENT,
	product_id INT UNSIGNED NOT NULL,
	substitute_id INT UNSIGNED NOT NULL,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;
	
	
