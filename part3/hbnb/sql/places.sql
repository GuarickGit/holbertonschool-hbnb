CREATE TABLE IF NOT EXISTS places(
	id CHAR(36) PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	description TEXT,
	price DECIMAL(10, 2) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	owner_id CHAR(36) NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES users(id)
)
