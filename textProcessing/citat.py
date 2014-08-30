#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import re, codecs, brevity,pprint, random
class InputError(Exception):
    def __init__(self, msg):
        self.msg = str(msg)
    def __str__(self):
        return self.msg
class Citation(object):
    def __init__(self, uid = '', c_type = '', nameAra = '',nameEng = '',
     nameSahebA = '', nameSahebE = '', nameAuthorsA = [('','','')],
     nameAuthorsE = [('','','')], pubA = '', pubE = '', placeA = '',
     placeE = '', yearH = '', yearM = '', pages = '', fatemi = 1):
        if uid:
            self.uid = ('{uid}',(uid))
            #uid for citation
        else: 
            self.uid = ('{uid}', (name + str(random.random())))
        self.authors = []
        if len(nameAuthorsA) is not len(nameAuthorsE):
            raise InputError('''
Arabic author name list should be equal to english name list
If no equivalents available, an empty
3-tuple should be used as a placeholder
''')
        for a,e in zip(nameAuthorsA,nameAuthorsE):
            self.authors.append((a,e))
            ###make sure input keeps this clean...no index errors!!!
            
        self.c_type = ('{c_type}',c_type)
        self.name = ('{name}', (nameAra,nameEng))
        self.saheb = (nameSahebA, nameSahebE)
        if fatemi:
            self.author = ('{author}', self.saheb)
        else:
            self.author = ('{author}', self.authors)
        self.publisher = ('{publisher}',(pubA, pubE))
        self.pub_date = ('{year}',(yearH, yearM))
        self.pub_place = ('{place}', (placeA, placeE))
        self.fatemi = ('{fatemi}', fatemi) # 1 or 0
        self.pages = ('{pages}', pages)   # num of pages
        
    def fullnote_ara(self,page):
        if self.fatemi:
            author = self.author[0]
        else:
            author = [i[0] for i in
             self.author]
        if len(author) > 1:
            if len(author) == 2:
                pass
            elif len(author) >= 3:
                pass
        else:
            output = ''
            return output
    def shortnote_ara(self,page):
        if self.fatemi:
            author = self.author[0]
        else:
            author = [i[0] for i in
             self.author]
        if len(author) > 1:
            if len(author) == 2:
                pass
            elif len(author) >= 3:
                pass
        else:
            output = ''
            return output
    def biblio_ara(self):
        if self.fatemi:
            author = self.author[0]
        else:
            author = [i[0] for i in
             self.author]
        if len(author) > 1:
            if len(author) == 2:
                pass
            elif len(author) >= 3:
                pass
        else:
            output = ''
            return output
    def fullnote_eng(self,page):
        if self.fatemi:
            author = self.author[1]
        else:
            author = [i[1] for i in
             self.author]
        if len(author) > 1:
            if len(author) == 2:
                pass
            elif len(author) >= 3:
                pass
        else:
            output = ''
            return output
    def shortnote_eng(self,page):
        if self.fatemi:
            author = self.author[1]
        else:
            author = [i[1] for i in
             self.author]
        if len(author) > 1:
            if len(author) == 2:
                pass
            elif len(author) >= 3:
                pass
        else:
            output = ''
            return output
        
    def biblio_eng(self):
        if self.fatemi:
            author = self.author[1]
        else:
            author = [i[1] for i in
             self.author]
        if len(author) > 1:
            if len(author) == 2:
                pass
            elif len(author) >= 3:
                pass
        else:
            output = ''
            return output
    def __str__(self):
        s = u"""
{uid}, {c_type}, Fatemi: {f}
------------------------------------------
Name:\t {name} \t|\t {nameAra}
Author(s):\t {authors} 
Pub_detail:\t {city}: {publisher}, {date}
Pages: {pgs}

"""
        if self.fatemi:
            authors = self.saheb[1]
        else: 
            athrs = [i[1] for i in self.authors]
            authors = ''
            author = '{0}, {1}, '
            for i in athrs:
              authors += author.format(i[0],i[1])
        out = s.format(uid = self.uid, c_type = self.c_type,
            name = self.name[1], nameAra = self.name[0],
            authors = authors, city = self.pub_place[1],
            pblshr = self.publisher[1], date = self.pub_date[1], 
            pgs = self.pages, f = self.fatemi)
        print out.encode('utf-8')
        
class Journal(Citation):
    def __init__(self, uid = '',  title = '', name = '',nameAra = '', 
                 authors = [('','','')], authorsAra = [('', '', '')],
                 collegeA = '', collegeE = '', url = '',
                 yearH = '', yearM = '', pages = '', fatemi = 1):
        super(Journal, self).__init__(uid = uid, c_type = 'journal',
                                      title = title , nameEng = name,
                            nameAra = nameAra, authors = [('','','')],
                            authorsAra = [('','','')], pubA = collegeA,
                            pubE = collegeE, placeE = url, yearH = yearH,
                            yearM = yearM, pages = pages, fatemi = fatemi)
        
        
class Qasida(Citation):
    def __init__(self, uid = '',
                 nameEng = '', nameAra = '', nameSahebA = '', nameSahebE = '',
                 authors = [('','','')], authorsAra = [('', '', '')],
                 pubA = '', pubE = '', placeA = '', placeE = '',
                 yearH = '', yearM = '', pages = '', fatemi = 0):
        super(Qasida, self).__init__(c_type = 'qasida', uid = uid,  title = '',
         nameEng = nameEng, nameAra = nameAra, authors = authors,
         authorsAra = authorsAra, nameSahebA = nameSahebA, nameSahebE = nameSahebE,
         pubA = pubA, pubE = pubE, placeA = placeA, placeE = placeE, yearH = yearH,
         yearM = yearM, pages = pages, fatemi = fatemi)
        
class Website(Citation):
    def __init__(self, uid = '', nameEng = '', nameAra = '', authors = [('','','')],
                 authorsAra = [('', '', '')], date = '', url = '', fatemi = 1):
        super(Website, self).__init__(uid = uid, c_type = 'website',
         nameEng = name, nameAuthorsA = [('','','')], nameAuthorsE = [('','','')], pubA = '',
         pubE = '', placeA = '', placeE = '', yearH = '', yearM = '',
         pages = '', fatemi = 1)
class BookPrint(Citation):
    def __init__(self, uid = '',  titleE = '', titleA = '', nameSahebE = '', nameSahebA = ''
                 authors = [('','','')], authorsAra = [('', '', '')],
                 pubA = '', pubE = '', placeA = '', placeE = '',
                 yearH = '', yearM = '', pages = '', fatemi = 1):
        super(BookPrint, self).__init__(uid = uid, c_type = 'bookPrnt', nameAra = titleA,
                                        nameEng = titleE, nameSahebE = nameSahebE, nameSahebA = nameSahebA,
                                        authors = authors, authorsAra = authorsAra,
                                        pubA = pubA, pubE = pubE, placeA = placeA, placeE = placeE,
                                        yearH = yearH, yearM = yearM, pages = pages, fatemi = fatemi)
class BookIS(Citation):
    def __init__(self, uid = '',  titleE = '', titleA = '', nameSahebE = '', nameSahebA = ''
                 authors = [('','','')], authorsAra = [('', '', '')],
                 pubA = '', pubE = '', placeA = '', placeE = '',
                 yearH = '', yearM = '', pages = '', fatemi = 1):
        super(BookPrint, self).__init__(uid = uid, c_type = 'bookPrnt', nameAra = titleA,
                                        nameEng = titleE, nameSahebE = nameSahebE, nameSahebA = nameSahebA,
                                        authors = authors, authorsAra = authorsAra,
                                        pubA = pubA, pubE = pubE, placeA = placeA, placeE = placeE,
                                        yearH = yearH, yearM = yearM, pages = pages, fatemi = fatemi)
class Living(Citation):
    def __init__(self, uid = '',  title = '', name = '',nameAra = '', 
                 authors = [('','','')], authorsAra = [('', '', '')],
                 pubA = '', pubE = '', placeA = '', placeE = '',
                 yearH = '', yearM = '', pages = '', fatemi = 1):
        pass
