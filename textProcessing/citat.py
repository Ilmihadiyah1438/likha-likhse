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
    def __init__(self, uid = '', c_type = '', name = ('',''), nameSaheb = ('', ''),
                 nameAuthors = ([('','')],[('','')]), nameEditors = ([('','')],[('','')]),
                 nameTranslators = ([('','')]),pub = ('', ''), place = ('', ''),
                 year = ('', ''), pages = '', fatemi = 1):
        
        if uid:
            self.uid = uid
            #uid for citation
        else: 
            self.uid = uid, (name + str(random.random()))
        #names are 2-tuples (prefix+first, last+suffix)    
        self.authors = self.__names(nameAuthors)
        self.editors = self.__names(nameEditors)
        self.translators = self.__names(nameTranslators)
        
        self.c_type = c_type
        self.name = nameAra,nameEng #title of work
        self.saheb = nameSahebA, nameSahebE
        if fatemi:
            self.author = self.saheb
        else:
            self.author = self.authors
        self.publisher = pubA, pubE #for istinsakh - name of khizana
        self.pub_date = yearH, yearM #for istinsakh - date of IS
        self.pub_place = placeA, placeE # for istinsakh - place of khizana
        self.istinsakh = 0
        self.volumes = 0
        self.multivolume = 0
        if self.volumes > 1:
            self.multivolume = 1
        self.edited = 0
        self.translate = 0
        self.part = 0
        self.fatemi = fatemi # 1 or 0
        self.pages = pages   # num of pages
        self.notes = (u'-',u'-')
        self.partOf = (u'-',u'-')
    def fullnote(self,page, lang):
        n = {}
        if lang == 'ara':
            if self.fatemi:
                n['authors'] = self.saheb[0]
            else:
                author = [i[0] for i in self.authors]
                
            if len(author) > 1:
                if len(author) == 2:
                    n['authors'] = u'{0}، و، {1}'.format(self.lName_first(author[0]),
                                                     self.fName_first(author[1]))
                elif len(author) >= 3:
                    n['authors'] = u'{0}، مع غيره'.format(self.fName_first(author[0]))
            else:
                authors = u'{0}'.format(self.fName_first(author[0]))
            n['title'] = self.__title(lang = 'ara')
            n['publish'] = self.__publish(lang = 'ara')
            n['page'] = page
            note = u'{authors}،{title}،({publish})،{page}.'.format(**n)
        elif lang == 'eng':
            if self.fatemi:
                n['authors'] = self.saheb[1]
            else:
                author = [i[1] for i in self.authors]
                
            if len(author) > 1:
                if len(author) == 2:
                    n['authors'] = u'{0}, and {1}'.format(self.lName_first(author[0]),
                                                     self.fName_first(author[1]))
                elif len(author) >= 3:
                    n['authors'] = u'{0}, and others'.format(self.fName_first(author[0]))
            else:
                authors = u'{0}'.format(self.fName_first(author[0]))
            n['title'] = self.__title(lang = 'eng')
            n['publish'] = self.__publish(lang = 'eng')
            n['page'] = page
            note = u'{authors},{title},({publish})،{page}.'.format(**n)
        return note                          
                                    
    def shortnote(self,page, lang):
        if lang == 'ara':
            if self.fatemi:
                author = self.saheb[0]
            else:
                author = [i[0] for i in self.authors]
            if len(author) > 1:
                if len(author) == 2:
                    authors = u'{0}، و، {1}'.format(self.lName_first(author[0]),
                                                     self.fName_first(author[1]))
                elif len(author) >= 3:
                    authors = u'{0}، مع غيره'.format(self.fName_first(author[0]))
            else:
                authors = u'{0}'.format(self.fName_first(author[0]))
            note = u'{0}، {1}، {2}.'.format(authors, self.name[0], page)
        elif lang == 'eng':
            if self.fatemi:
                author = self.saheb[1]
            else:
                author = [i[1] for i in self.authors]
            if len(author) > 1:
                if len(author) == 2:
                    authors = u'{0}, and {1}'.format(self.lName_first(author[0]),
                                                     self.fName_first(author[1]))
                elif len(author) >= 3:
                    authors = u'{0}, and others'.format(self.fName_first(author[0]))
            else:
                authors = u'{0}'.format(self.fName_first(author[0]))
            note = u'{0}, {1}, {2}.'.format(authors, self.name[0], page)
        return note
                                                
    def biblio(self, auth = 1, lang = 'ara'):
        if lang == 'ara':
            if auth == 0:
                authors = u'---'
            else:
                if self.fatemi:
                    author = self.saheb[0]
                else:
                    author = [i[0] for i in self.authors]
                if len(author) > 1:
                    if len(author) == 2:
                        authors = u'{0}، و، {1}'.format(self.lName_first(author[0]),
                                                         self.fName_first(author[1])) 
                    elif len(author) >= 3:
                        authors = u'،'.join(self.fName_first(i) for i in author)
                else:
                    authors = u'{0}'.format(self.fName_first(author[0]))
            bib_base = u'{authors}.{title}. {publish}.'
            publish = self.__publisher(lang = 'ara')
            title = self.__title(lang = 'ara')
            
        elif lang == 'eng:
            if auth == 0:
                authors = u'---'
            else:
                if self.fatemi:
                    author = self.saheb[1]
                else:
                    author = [i[1] for i in self.authors]
                if len(author) > 1:
                    if len(author) == 2:
                        authors = u'{0}, and {1}'.format(self.lName_first(author[0]),
                                                         self.fName_first(author[1])) 
                    elif len(author) >= 3:
                        authors = u','.join(self.fName_first(i) for i in author)
                else:
                    authors = u'{0}'.format(self.fName_first(author[0]))
            bib_base = u'{authors}.{title}. {publish}.'
            publish = self.__publisher(lang = 'eng')
            title = self.__title(lang = 'eng')
        b= {'publish' = publish, 'authors' = authors, 'title' = title}
        biblio = bib_base.format(**b)
    def fName_first(self, name, lang):
        """for tuple"""
        title = name[0]
        firstname = name[1]
        lastname = name[2]
        name = u'{1} {2}'.format(firstname,lastname).rstrip()
        return name
    def lName_first(self, name, lang):
        """for tuple"""
        if lang == 'ara':
           comma = '،'
        if lang == 'eng':
           comma = ','
        title = name[0]
        firstname = name[1]
        lastname = name[2]
        name = u'{1} {3} {2}'.format(lastname,firstname, comma).rstrip()
        return name
    def __year(self, lang = 'ara'):
        if lang == 'ara':
            h = 'هـ'
            g = 'م'
            hijri_greg = '{0}\{1}'
            
        elif lang == 'eng':
            h = 'AH'
            g = 'C.E'
            hijri_greg = '{0}/{1}'
            
        hijri = '{0}{1}'.format(self.pub_date[0], h)
        greg = '{0}{1}'.format(self.pub_date[1],g)
        h_g = hijri_greg.format(hijri,greg)
        dates = [hijri, greg, h_g]
        
        if self.pub_date[0] and self.pub_date[1]:
            dates[3] = h_g
        elif self.pub_date[0] and self.pub_date[1] == False:
            dates[3] = hijri
        elif self.pub_date[1] and self.pub_date[0] == False:
            dates[3] = greg
        return dates
        
    def __publisher(self, lang = 'ara'):
        pub = {'date':self.__year(lang = lang}}
        if lang == 'ara':
            pub['publisher', 'place'] = self.publisher[0], self.pub_place[0]
            if self.istinsakh:
                publish = u'اس: {date}،{publisher}،{place}'
            if self.istinsakh is not:
                publish = u'{place}:{publisher}،{date}'
        elif lang == 'eng':
            pub['publisher', 'place'] = self.publisher[1], self.pub_place[1]
            if self.istinsakh:
                publish = u'Date of IS: {date}, {publisher}'
            if self.istinsakh is not:
                publish = u'{place}:{publisher},{date}'
        p = publish.format(**pub)
        return p
    def __title(self, lang = 'ara', d = '.', volumes = 0):
        title = u'{title}'
        if lang == 'ara':
            editors = ','.join(self.fName_first(i, lang = 'ara') for i in self.editors[0])
            translators = ','.join(self.fName_first(i, lang = 'ara') for i in self.translators[0])
            titl = {'title':self.name[0], 'source': self.partOf[0], 'd':d,
                     'editor': editors, 'translator': translators}
            if self.part:
                title = u'"{title}"'
                title += u'{d} المرجع في {source}'
            if self.edited:
                title += u'{d} تحقيق {editor}'
            if self.translate:
                title += u'{d} المترجم بـ {editor}'s
        elif lang == 'eng':
            titl = {'title':self.name[1], 'source': self.partOf[1], 'd':d,
                     'editor': editors, 'translator': translators}
            if self.part:
                title = u'"{title}"'
                title += u'{d} In {source}'
            if self.edited:
                if self.editors > 1:
                    title += u'{d} eds. {editor}'
                else:
                    title += u'{d} ed. {editor}'
            if self.translate:
                title += u'{d} Translated by {translator}'       
        t = title.format(**titl)
    def __names(self, names):
        variable = []
        if len(names[0]) is not len(names[1]):
            raise InputError('''
Arabic name list should be equal to english name list
If no equivalents available, an empty
3-tuple should be used as a placeholder
''')
        for a,e in zip(names[0],names[1]):
            if a[0:1] and e[0:1]:
                variable.append((a,e))
            elif a[0:] and e[0:] == False:
                variable.append((a,a))
            elif e[0:] and a[0:] == False:
                variable.append((e,e))
            elif a[0:] == False and e[0:] == False:
                variable.append(u'(-)',u'(-)')
            ###make sure input keeps this clean...no index errors!!!
        return variable
            
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
