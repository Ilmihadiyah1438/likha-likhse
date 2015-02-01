#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import re, codecs, brevity,pprint, citat
citation = []
def form_re(cite_type, order):
    dlmtr_name = raw_input(
    	str('name delimiter: '))
    dlmtr_authors = raw_input( 
     str('authors delimiter: '))
    dlmtr_publish = raw_input(
     str('publishing delimiter: '))
def verify(query = ''):
    v = raw_input(str('{0}'.format(query)))
    while v != ('y' or 'Y' or 'n' or 'N'):
        v = raw_input(str('{0} (Please enter y or n)'.format(query)))
    if v.lowercase() == 'y':
        b = True
    else b = False
    return b
def num_verify(query = ''):
    n = raw_input(str('{0} (if unknown, enter 0): '.format(query)))
    y = 'y'
    while y == 'y':
        try:
            n = int(n)
            y = 'n'
        except ValueError:
            n = raw_input(str('''Please enter only integers. {0}
(if unknown, enter 0): '''.format(query)))
    return n
        
def basic_query(typ = 'author', multi = 'y', what = 'name', form = ''):
    basic = []
    arabic = []
    english = []
    cont = 'y'
    if form is not True:
        if what == 'name':
            form = '''Title FirstName;LastName Suffix; (If information is not available, type only ';'
    (without quotes). '''
            if typ != 'saheb':
                form += 'For example: M. Abdeali;Jamali: '
            elif typ == 'saheb':
                form += 'For example: al-Dai al-Ajal Syedna Mohammed;Burhanuddin RA'
                multi = 'n'
        elif what == 'year':
            form = 'year'
            multi = 'n'
        elif what == 'title':
            form = 'title;subtitle (if title contains a semicolon, insert && in place of it)'
            multi = 'n'
        elif what == 'url':
            form = 'url (replace semicolons with &&)'
            multi = 'n'
        elif what == 'place':
            form = 'city;country'
            multi = 'n'
        elif what == 'date':
            form = 'dd;mm;yyyy (If info is not available, type only ; (ex. ;2;1966)'
    while cont == 'y':
        if what != 'url':
            if what == 'year' or 'date':
                basA = raw_input(str('Enter Hijri {0} of publication: (if available)'.format(what)))
                basE = raw_input(str('Enter Gregorian {0} of pub.: (if available)'.format(what)))
            basA = raw_input(str('''Enter name of {0} in Arabic script in this format:
{1}: '''.format(what, typ.replace(';','؛'))))
            basE = raw_input(str('''Enter name of {0} in Latin script in the form
mentioned above: '''.format(what, typ)))
        if basA != '':
            arabic.append([i.replace('&&',u'؛').rstrip() for i in basA.split('؛')])
        else:
            basA = ['' for i in basA.split(';')]
            arabic.append(basA)
        if basE != '':
            english.append([i.replace('&&',';').rstrip() for i in basE.split(';')])
        else:
            basE = ['' for i in basE.split(';')]
            english.append(basE)
        if multi == 'y':
            cont = verify(query = 'Are there more {1}s? y or n: '.format(typ))
    basic = (arabic,english)
    return basic
                          
def bookPrint_query():
    title = basic_query(typ = 'title', multi = 'n', what = 'title')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    e = verify(query = 'Any editors? (y or n)')
    if e: editor = basic_query(typ = 'editor')
    else: editor = [('',''),('','')]
    t = verify(query = 'Any translators? (y or n)')
    if t: translator = basic_query(typ = 'translator')
    else: translator = [('',''),('','')]
    publisher = basic_query(typ = 'publisher', multi = 'n')
    city = basic_query(typ = 'city of publishing', what = 'place', multi = 'n')
    year = basic_query(typ = 'year')
    pages = num_verify(query = 'Number of pages: ')
    b = citat.BookPrint(title = title, nameSaheb = saheb, nameAuthors = author,
                        nameEditors = editor, nameTranslators = translator,
                        pub = publisher, place = city, year = year, pages = pages,
                        fatemi = fatemi)
    return b
                     
def bookIS_query():
    title = basic_query(typ = 'title', multi = 'n', what = 'title')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]               
    else:
        author = basic_query(typ= 'author')
        saheb = [('',''),('','')]
    khizana = basic_query(typ = 'khizana', multi = 'n')
    location = basic_query(typ = 'location of khizana', multi = 'n', what = 'city')
    year = basic_query(typ = 'year of IS', what = 'year', multi = 'n')
    pages = num_verify(query = 'Number of pages: ')
    i = citat.BookIS(fatemi = fatemi, saheb = saheb, author = author,
                     khizana = khizana, location = location, year = year,
                     pages = pages)
    return i
    
def journal_query():
    title = basic_query(typ = 'title', multi = 'n', what = 'title')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')                        
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    e = verify(query = 'Any editors? (y or n)')
    if e: editor = basic_query(typ = 'editor')
    else: editor = [('',''),('','')]
    t = verify(query = 'Any translators? (y or n)')
    if t: translator = basic_query(typ = 'translator')
    else: translator = [('',''),('','')]
    college = basic_query(typ = 'name of college', multi = 'n', what = 'place',
                          form = 'college;city;country')
    url = basic_query(typ = 'static url', multi = 'n', what = 'url')
    year = basic_query(typ = 'year of publication', what = 'year', multi = 'n')
    pages = num_verify(query = 'Number of pages: ')
    j = citat.Journal(fatemi = fatemi, saheb = saheb, authors = author,
                      editors = editor, translators = translator,
                      college = college, url = url, year = year, pages = pages)
    return j
    
def qasida_query():
    matlaa = basic_query(typ = 'matlaa', multi = 'n', form = 'matlaa')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    year = basic_query(typ = 'year of publication', what = 'year')
    verses = num_verify(query = 'Number of verses: ')
    q = citat.Qasida(fatemi = fatemi, matlaa = matlaa, year = year, verses = verses,
                     saheb = saheb, authors = author)
    return q
    
def website_query():
    '''def __init__(self, uid = '', nameEng = '', nameAra = '', authors = [('','','')],
                 authorsAra = [('', '', '')], date = '', url = '', fatemi = 1)'''
    title = basic_query(typ = 'title of article', what = 'title')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    date = basic_query(typ = 'Accession date', multi = 'n')
    url = basic_query(typ = 'URL', multi = 'n', what = 'url')
    w = citat.Website(title = title, authors = author, saheb = saheb, date = date,
                      url = url)
    return w
def menu(x):
    cite_type = raw_input(str("Enter citation type> enter 'help' for options: "))          
    if cite_type == 'help':
        print """Options:
        'book'\t or 1:\t normal book
        'qasida'\t or 2:\t qasida
        'living'\t or 3:\t living source
        'website'\t or 4:\t website
        'journal'\t or 5:\t journal article (like JSTOR)
        'skip'\t or #:\t skip this entry
        'save and close'\t or 0:\t save and close
        'close w/o saving'\t or !: \t close without saving
        NOTE:  Append capital I for istinsakh kutub
        NOTE2: All entries without quotes, so 'book' is actually
        book
    """
    elif cite_type == 'skip':
        x += 1
        c = 1
    elif ('book' or '1') in cite_type:
        if 'I' in cite_type:
            b = bookIS_query()
        else: b = bookPrint_query()
        x+=1
        c = 1
    elif ('qasida' or '2') in cite_type:
        b = qasida_query()
        x += 1
        c = 1
    elif ('living' or '3') in cite_type:
        print 'Not available at this moment\n'
        x += 1
        c = 1
    elif ('website' or '4') in cite_type:
        b = website_query()
        x += 1
        c = 1
    elif ('journal' or '5') in cite_type:
        b = journal_query()
        x += 1
        c = 1
    elif ('save and close' or '0') in cite_type:
        print 'Goodbye, saving....\n'
        out_name = raw_input(str("Enter out file name: "))
        out = codecs.open(out_name, 'w', 'utf-8')
        out.write(citations)
    elif ('close w/o save' or '!') in cite_type:
        print 'Not saving, goodbye \n'
    else:
        print "Choose an option"
        c = 0
    return b,x,c
    
   
if __name__ =='__main__':
    opening = verify(query = 'Is there a preexisting list of citations? (y or n): ')
    citations = ''
    cites = []
    c = 0
    x = 1
    if opening:
        cite_name = raw_input(str("Citation file: "))
        cite_file = codecs.open(cite_name,'r', 'utf-8')
        cite_raw = cite_file.readlines()
        for c in cite_raw:
            print x, '\t', c.encode('utf-8')
            while c == 0:
                result = menu()
                cites.append(result[0])
                x = result[1]
                c = result[2]
    else:
       while c == 0:
           result = menu(x)
           cites.append(result[0])
           x = result[1]
           c = result[2]
                    
    for i in cites:
        print i            
            
            
            
            
            
            
            
            
            
