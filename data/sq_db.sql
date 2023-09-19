CREATE TABLE "users" (
	"id"	INTEGER,
	"username"	text NOT NULL UNIQUE,
	"password"	text NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "posts" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"full_text"	TEXT NOT NULL,
	"author"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);