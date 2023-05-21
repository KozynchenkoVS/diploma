CREATE TABLE "ruBirds" (
	"id"	INTEGER,
	"bird_ru"	TEXT,
	"desc_ru"	TEXT,
	"size_ru"	TEXT,
	"place_ru"	TEXT,
	"bird_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
	FOREIGN KEY("bird_id") REFERENCES classes(id)
);