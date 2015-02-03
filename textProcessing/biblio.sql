CREATE TABLE kitabs(
	uid TEXT UNIQUE,
	fatemi INTEGER,
	titleAra TEXT,
	titleEng TEXT,
	type TEXT,
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
	partOf TEXT REFERENCES kitabs (uid));
CREATE TABLE authors(
	id INTEGER AUTOINCREMENT PRIMARY KEY,
	nameAra TEXT,
	nameEng TEXT,
	fatemi INTEGER);
CREATE TABLE editors(
	id INTEGER AUTOINCREMENT PRIMARY KEY,
	nameAra TEXT,
	nameEng TEXT);
CREATE TABLE translators(
	id INTEGER AUTOINCREMENT PRIMARY KEY,
	nameAra TEXT,
	nameEng TEXT);
CREATE TABLE booktoauthors(
	kit REFERENCES kitabs(uid),
	aut REFERENCES authors(id),
	aut_index INTEGER,
	edi REFERENCES editors(id),
	edi_index INTEGER,
	tra REFERENCES translators(id),
	tra_index INTEGER);
CREATE TABLE chapters(
	id INTEGER PRIMARY KEY,
	kit REFERENCES kitabs(uid),
	chapterAra TEXT,
	chapterEng TEXT,
	chapter_index INTEGER);
	
	
	
