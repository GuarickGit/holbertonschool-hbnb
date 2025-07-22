CREATE TABLE IF NOT EXISTS users(
	id CHAR(36),
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	email VARCHAR(255),
	password VARCHAR(255),
	is_admin BOOLEAN DEFAULT FALSE,
	UNIQUE (email),
	PRIMARY KEY(id)
)
