CREATE TABLE kitabs(
	k_uid TEXT UNIQUE,
	fatemi INTEGER,
	titleAra TEXT,
	titleEng TEXT,
	c_type TEXT,
	istinsakh INTEGER,
	publisherAra TEXT,
	publisherEng TEXT,
	pub_dateH TEXT,
	pub_dateG TEXT,
	pub_placeAra TEXT,
	pub_placeEng TEXT,
	volumes INTEGER,
	pages TEXT,
	notesAra TEXT,
	notesEng TEXT,
	partOf TEXT REFERENCES kitabs (k_uid));

CREATE TABLE names(
id INTEGER AUTOINCREMENT PRIMARY KEY,
firstnameAra TEXT,
lastnameAra TEXT,
firstnameEng TEXT,
lastnameEng TEXT,
position INTEGER,
chrono INTEGER
);

CREATE TABLE names_fatemi(
id INTEGER PRIMARY KEY,
firstnameAra TEXT,
lastnameAra TEXT,
firstnameEng TEXT,
lastnameEng TEXT,
position INTEGER,
chrono INTEGER);

CREATE TABLE booktoauthors(
	kit TEXT,
	name INTEGER,
	name_fatemi INTEGER,
	position INTEGER,
	p_index INTEGER);

CREATE TABLE chapters(
	id INTEGER PRIMARY KEY,
	kit REFERENCES kitabs(k_uid),
	chapterAra TEXT,
	chapterEng TEXT,
	chapter_index INTEGER);


	
	
