CREATE TABLE "enBirds" (
	"id"	INTEGER,
	"bird_en"	TEXT,
	"desc_en"	TEXT,
	"size_en"	TEXT,
	"place_en"	TEXT,
	"bird_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
	FOREIGN KEY("bird_id") REFERENCES "classes"("id")
);