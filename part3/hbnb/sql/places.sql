CREATE TABLE IF NOT EXISTS places(
	id CHAR(36),
	title VARCHAR(255),
	description TEXT,
	price DECIMAL(10, 2),
	latitude FLOAT,
	longitude FLOAT,
	owner_id CHAR(36),
	FOREIGN KEY (owner_id) REFERENCES users(id),
	PRIMARY KEY(id)
)
