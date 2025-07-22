CREATE TABLE IF NOT EXISTS place_amenities(
	place_id CHAR(36),
	amenity_id CHAR(36),
	FOREIGN KEY (place_id) REFERENCES places(id),
	FOREIGN KEY (amenity_id) REFERENCES amenities(id),
	PRIMARY KEY (place_id, amenity_id)
)
