#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import re, codecs, brevity,pprint, random
class Citation(object):
    def __init__(self, 
     uid = '', c_type = '',
     nameAra = '',nameEng = '',
     nameSahebA = '', nameSahebE = '',
     nameAuthorsA = [('','','')],
     nameAuthorsE = [('','','')], 
     pubA = '', pubE = '', 
     placeA = '', placeE = '',
     yearH = '', yearM = '', 
     pages = '', fatemi = 1):
        if uid:
            self.uid = uid 
            #uid for citation
        else: 
            self.uid = name + str(
                       random.random())
        self.c_type = c_type 
        #type of citation
        self.name = (nameAra,nameEng)
        self.saheb = (nameSahebA,
                      nameSahebE)
        self.authors = []
        for a,e in zip(nameAuthorsA,
                       nameAuthorsE):
            self.authors.append((a,e))
            ###make sure input keeps this clean...no index errors!!!
        self.publisher = (pubA, pubE)
        self.pub_date = (yearH, yearM)
        self.pub_place = (placeA,
                          placeE)
        self.fatemi = fatemi # 1 or 0
        self.pages = pages   # num of pages
    def longAra(self):
        if self.fatemi:
            pass
        else:
            pass
    def shortAra(self):
        pass
    def longEng(self):
        pass
    def shortEng(self):
        pass
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
              authors += author.format(
                           i[0],i[1])
        out = s.format(
          uid = self.uid,
          c_type = self.c_type,
          name = self.name[1],
          nameAra = self.name[0],
          authors = authors, 
          city = self.pub_place[1],
          pblshr = self.publisher[1],
          date = self.pub_date[1], 
          pgs = self.pages
          f = self.fatemi)
        print out.encode('utf-8')    
class Journal(Citation):
    pass
class Qasida(Citation):
    pass
class Website(Citation):
    pass
class BookPrint(Citation):
    pass
class BookIS(Citation):
    pass
class Living(Citation):
    pass