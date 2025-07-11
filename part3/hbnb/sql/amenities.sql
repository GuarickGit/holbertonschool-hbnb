CREATE TABLE IF NOT EXISTS amenities (
	id CHAR(36),
	name VARCHAR(255),
	PRIMARY KEY (id),
	UNIQUE (name)
)
