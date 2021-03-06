#-*-coding:utf8-*
#qpy:2
#qpy:console
#786
#bihi wa bi waliyyihi wa bi daihi Syedna Aali Qadr Mufaddal Saifuddin TUS
#asta'eeno fi jamee' il umoor
import re, codecs, citat, sqlite3
from operator import itemgetter
from os.path import dirname,join
from getdir import curdir
print curdir
citation = []
def form_re(cite_type, order):
    dlmtr_name = raw_input(
    	str('name delimiter: '))
    dlmtr_authors = raw_input( 
     str('authors delimiter: '))
    dlmtr_publish = raw_input(
     str('publishing delimiter: '))
def verify(query = ''):
    v = raw_input(str(u'{0}'.format(query)))
    while v.lower() != u'y' and v.lower() != u'n':
        v = raw_input(str(u'{0} (Please enter y or n)'.format(query)))
    
    if v.lower() == u'y':
        b = 1
    else: b = 0
    return b
def num_verify(query = ''):
    n = raw_input(str(u'{0} (if unknown, enter 0): '.format(query)))
    y = 'y'
    while y is 'y':
        try:
            n = int(n)
            y = 'n'
        except ValueError:
            n = raw_input(str(u'''Please enter only integers. {0}
(if unknown, enter 0): '''.format(query)))
    return n
def opening_db(file_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute(u'select * from kitabs')
    cites = []
    for i in cur.fetchall():
        c = citat.Citation()
        c.uid = i[0]
        c.fatemi = i[1]
        c.name = (i[2],i[3])
        c.c_type = i[4] #type in kitabs.type
        c.istinsakh = i[5]
        c.publisher = (i[6],i[7])
        c.pub_date = (i[8],i[9])
        c.pub_place = (i[10],i[11])
        c.volumes = i[12]
        c.pages = i[13]
        c.notes = (i[14], i[15])
        auth = []
        edi = []
        tra = []
        fatemi_indices = []
        cur = conn.cursor()
        name_query = u'''SELECT firstnameAra, lastnameAra,
firstnameEng, lastnameEng, chrono FROM ? WHERE id = ?'''
        aet_query = u'''select * from booktoauthors
where kit = ? and position = ?;'''
        auth_indices = cur.execute(aet_query, (i[0], 1)).fetchall()
        edi_indices = cur.execute(aet_query, (i[0], 2)).fetchall()
        tra_indices = cur.execute(aet_query, (i[0], 4)).fetchall()
        auth_indices = sorted(auth_indices, key = itemgetter(5))
        for a in auth_indices:
            if a[2]:
                fatemi_indices.append(a)
        edi_indices = sorted(edi_indices, key = itemgetter(5))
        tra_indices = sorted(tra_indices, key = itemgetter(5))
        auth_fatemi = cur.execute(name_query,('names_fatemi',fatemi_indices[2]).fetchone()[0:3]
        for a in auth_indices:
            auth.append(cur.execute(name_query,('names',a[1])).fetchone()[0:3])
        for e in edi_indices:
            edi.append(cur.execute(name_query,('names',e[1])).fetchone()[0:3])
        for t in tra_indices:
            tra.append(cur.execute(name_query,('names',t[1])).fetchone()[0:3])
        c.saheb = c.__names(auth_fatemi)
        c.authors = c.__names(auth)
        c.editors = c.__names(edi)
        c.translators = c.__names(tra)
        cites.append(c)
        
    conn.close()
    return cites

def compare(list1, list2):
    equal = []
    diff1 = []
    diff2 = []
    new = []
    for a in list1:
        for b in list2:
            if a is b:
               equal.append(a)
            elif a[0:1] == b[0:1]:
               diff1.append(a)
            elif a[2:3] == b[2:3]:
               diff2.append(a)
            elif (a[0:1] != b[0:1]) and (a[2:3] != b[2:3]):
               new.append(a)
               
    return equal,diff1,diff2,new     

def saving_db(file_name,cite_list):
    create = ''
    try:
        codecs.open(file_name)
    except IOError:
        create = codecs.open(join(curdir,u'biblio.sql'),u'r').read()
    conn = sqlite3.connect(file_name)
    if create:
        conn.executemany(create)
    cur = conn.cursor()
    e = cur.execute(u'select * from kitabs')
    exist_cites = [c[0] for c in e.fetchall()]
    prog_cites = [c for c in cite_list]
    new_cites = [c for c in prog_cites if c.uid not in exist_cites]
    update_cites = [c for c in prog_cites if c.uid in exist_cites]
    e = cur.execute(u'''select * from names
WHERE position = 1 OR 3 OR 5 OR 7;''')
    exist_authors = [a[1:4] for a in e.fetchall()]
    prog_authors = [a.authors for a in cite_list]
    diff = compare(exist_authors, prog_authors)
    update_authors = diff[0:2]
    new_authors = diff[3]
    e = cur.execute(u'''select * from names 
WHERE position = 2 OR 3 OR 6 OR 7;''')
    exist_editors = [a[1:4] for a in e.fetchall()]
    prog_editors = [a.editors for a in cite_list]
    diff = compare(exist_editors, prog_editors)
    update_editors = diff[0:2]
    new_editors = diff[3]
    e = cur.execute(u'''select * from names
WHERE position = 4 OR 5 OR 6 OR 7;''')
    exist_translators = [a[1:4] for a in e.fetchall()]
    prog_translators = [a.translators for a in cite_list]
    diff = compare(exist_translators, prog_translators)
    update_translators = diff[0:2]
    new_translators = diff[3]
    #USE UPDATE INSTEAD OF REPLACE
    for c in cite_list:
        k =[(u'uid',c.uid),(u'fatemi',c.fatemi),(u'titleAra',c.titleAra),
        (u'titleEng',c.titleEng),(u'type',c.type),(u'istinsakh',c.istinsakh),
        (u'publisherAra',c.publisherAra),(u'publisherEng',c.publisherEng),
        (u'pub_dateH',c.pub_dateH),(u'pub_dateG',c.pub_dateG),
        (u'pub_placeAra',c.pub_placeAra),(u'pub_placeEng',c.pub_placeEng),
        (u'volumes',c.volumes),(u'pages',c.pages),(u'notesAra',c.notesAra),
        (u'notesEng',c.notesEng),(u'partOf',c.partOf)]
        e = cur.execute(u'''SELECT * FROM kitabs WHERE uid = "?"''', c.uid)
        def sort_names(t_name,list1,list2,list3,posits):
            for ite in list1:
                if ite in list2:
                    cur.execute(u'''INSERT INTO ? 
(firstnameAra, lastnameAra, firstnameEng, lastnameEng) 
VALUES (?,?,?,?);''',([t_name]+at[0:3]))
                if ite in list3[0]:
                    upd = u'''UPDATE ?
 SET (firstnameAra = "{0}", lastnameAra = "{1}")
 WHERE firstnameEng = "{2}" AND lastnameEng = "{3}";'''
                elif ite in list3[1]:
                    upd = u'''UPDATE ?
 SET (firstnameEng = "{2}", lastnameEng = "{3}")
 WHERE firstnameAra = "{0}" AND lastnameAra = "{1}";'''
                upd = upd.format(([t_name]+at[0:3]))
                cur.execute(upd)
                cur.execute('''UPDATE ? SET position = (position +1)
WHERE (firstnameAra = ? AND lastnameAra = ? AND firstnameEng = ? AND lastnameEng = ?)
 AND (position != ? OR position != ? OR position != ? OR position !=?);''', (ite[0:3]+list(posits)))
        sort_name('names_fatemi',c.authors,exist_authors,new_authors,
                    update_authors,(1,3,5,7))
        sort_name('names',c.authors,exist_authors,new_authors,
                    update_authors,(1,3,5,7))
        sort_name('names',c.editors,exist_editors,prog_editors,
                    update_editors,(2,5,6,7))
        sort_name('names',c.translators,exist_translators,new_translators,
                    update_authors,(4,5,6,7))
        if e.fetchall():
            for i in k[1:]:               
                kit = u'UPDATE kitabs SET {0} WHERE uid = "{1}";'
                entry = u'"{0}" = "{1}"'.format(i[0], i[1])
                kit = kit.format(kit,c.uid)
                cur.execute(kit)
        else:    
            kit = u'INSERT INTO kitabs ({0}) VALUES ({1});'
            entry0 = ''
            entry1 = ''
            for i in k[:-1]:
                if i:
                    entry0 += u'"{0}",'.format(i[0])
                    entry1 += u'"{0}",'.format(i[1])
            if k[-1]:
                entry0 += u'"{0}"'.format(k[-1][0])
                entry1 += u'"{0}"'.format(k[-1][0])
            if entry0[-1] == u',': entry0 = entry0[:-1]
            if entry1[-1] == u',': entry1 = entry1[:-1]
            kit = kit.format(entry0,entry1)
            cur.execute(kit)    
        def names(n_type,person):
            au_index = 1
            index = cur.execute(u"""
SELECT ? from booktoauthors WHERE kit = ? AND position = ?
ORDER BY p_index;""", (n_type,c.uid,person))
            index = index.fetchall()
            name_list = []
            for i in index:
                name = cur.execute(
u'''SELECT firstnameAra, lastnameAra, firstnameEng, lastnameEng
 FROM names WHERE id = ?;''', i)
                names = name.fetchone()
                name_list.append([name,i])
            return name_list
        a_f = names('name_fatemi',1)
        a = names('name',1)
        e = names('name',2)
        t = names('name',4)                
        def add_names(list1, list2, t_name, posit, inst):
            ind = 0
            for ite in list1:
                if ite[0] == list2[ind][0]:
                    ind += 1
                else: 
                    list2[ind][0] = auth[0]
                    cur.execute('''INSERT INTO booktoauthors
 (kit,?,position,p_index) VALUES (?,?,?,?);''',
 (t_name, inst.uid, list2[ind][1],posit,ind))
                    ind += 1
        add_names(c.saheb,a_f,'name_fatemi',1,c)
        add_names(c.authors,a,'name',1,c)
        add_names(c.editors,e,'name',2,c)
        add_names(c.translators,t,'name',4,c)
    cur.commit()
        
def basic_query(typ = u'author', multi = u'y', what = u'name', form = u''):
    basic = []
    arabic = []
    english = []
    cont = u'y'
    form_suff = ''
    print typ
    if form == '':
        if what == u'name':
            if typ == u'publisher':
                form = u'Publisher'
            else: form = u'''Title FirstName;LastName Suffix (If information is not available, type only ';'
    (without quotes). '''
            if typ == u'name':
                form_suff += u'For example: M. Abdeali;Jamali: '
            elif typ == u'saheb':
                form_suff += u'For example: al-Dai al-Ajal Syedna Mohammed;Burhanuddin RA'
                multi = u'n'
        elif what == u'year':
            form = u'year'
            multi = u'n'
        elif what == u'title':
            form = u'title,subtitle (if title contains a semicolon, insert && in place of it)'
            multi = u'n'
        elif what == u'url':
            form = u'url (replace semicolons with &&)'
            multi = u'n'
        elif what == u'place':
            form = u'city,country'
            multi = u'n'
        elif what == u'date':
            form = u'dd/mm/yyyy (If info is not available, type only what is available)'
    while cont == u'y':
        err = True
        while err  == True:
            try:
                if what != u'url':
                    if what == u'year' or what == u'date':
                        basA = raw_input(u'Enter Hijri {0} of publication: (if available)'.format(what))
                        basE = raw_input(u'Enter Gregorian {0} of pub.: (if available)'.format(what))
                    else:
                        basA = raw_input(u'''Enter {0} of {1} in Arabic script in this format:{2}: '''.format(what, typ, form)).decode('utf-8')
                        print basA.encode('utf-8')
                        basE = raw_input(u'''Enter {0} of {1} in Latin script in the form
mentioned above: '''.format(what, typ)).decode('utf-8')
                elif what == u'url':
                    url = raw_input('Enter complete URL: ').decode('utf-8')
                    basA = url
                    basE = url
                err = False
            except UnicodeDecodeError:
                print 'There was an error, please try again.'
            
        if basA: ar = [i.replace(u'&&', u'؛') for i in basA.split(u'؛')]   
        else: ar = [u'' for i in form.split(u';')]
        if len(ar) == 1 and multi == u'n': arabic = ar[0]
        else: arabic = ar
        if basE: eng = [i.replace(u'&&',u';') for i in basE.split(u';')]
        else: eng = [u'' for i in form.split(u';')]
        if len(eng) == 1 and multi == u'n': english = eng[0]
        else: english = eng
        if multi == u'y':
            print typ
            cont = verify(query = 'Are there more {0}s? y or n: '.format(typ))
        else: cont = u'n'
    basic = (arabic,english)
    return basic
                          
def bookPrint_query():
    part = False
    partof = ''
    title = basic_query(typ = u'title', multi = u'n', what = u'title')
    fatemi = verify(query = u'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = u'saheb', multi = u'n')
        author = [(u'',u''),(u'',u'')]
    else:
        author = basic_query(typ = u'author')
        saheb = (u'',u'')
    print saheb
    p = verify(query = u'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = u'name of larger work', multi = u'n',
                               what = u'title')
        part = True
    e = verify(query = u'Any editors? (y or n)')
    if e: editor = basic_query(typ = u'editor')
    else: editor = [(u'',u''),(u'',u'')]
    t = verify(query = u'Any translators? (y or n)')
    if t: translator = basic_query(typ = u'translator')
    else: translator = [(u'',u''),(u'',u'')]
    publisher = basic_query(typ = u'publisher', multi = u'n')
    city = basic_query(typ = u'city of publishing', what = u'place', multi = u'n')
    year = basic_query(typ = u'year', what = u'year')
    pages = num_verify(query = u'Number of pages: ')
    print title
    b = citat.BookPrint(title = title, saheb = saheb, authors = author,
                        editors = editor, translators = translator,
                        publisher = publisher, place = city, year = year, pages = pages,
                        fatemi = fatemi)
    b.partof = partof
    b.part = part
    return b
                     
def bookIS_query():
    part = False
    partof = ''
    title = basic_query(typ = u'title', multi = u'n', what = u'title')
    fatemi = verify(query = u'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = u'saheb', multi = u'n')
        author = [(u'',u''),(u'',u'')]               
    else:
        author = basic_query(typ= u'author')
        saheb = [(u'',u''),(u'',u'')]
    p = verify(query = u'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = u'name of larger work', multi = u'n',
                               what = u'title')
        part = True
    khizana = basic_query(typ = u'khizana', multi = u'n')
    location = basic_query(typ = u'location of khizana', multi = u'n', what = u'city')
    year = basic_query(typ = u'year of IS', what = u'year', multi = u'n')
    pages = num_verify(query = u'Number of pages: ')
    i = citat.BookIS(fatemi = fatemi, saheb = saheb, authors = author,
                     khizana = khizana, location = location, year = year,
                     pages = pages)
    i.partof = partof
    i.part = part
    return i
    
def journal_query():
    part = False
    partof = ''
    title = basic_query(typ = u'title', multi = u'n', what = u'title')
    fatemi = verify(query = u'Is source Fatemi? (y or n): ')                        
    if fatemi:
        saheb = basic_query(typ = u'saheb', multi = u'n')
        author = [(u'',u''),(u'',u'')]
    else:
        author = basic_query(typ = u'author')
        saheb = (u'',u'')
    p = verify(query = u'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = u'name of larger work', multi = u'n',
                               what = u'title')
        part = True
    e = verify(query = u'Any editors? (y or n)')
    if e: editor = basic_query(typ = u'editor')
    else: editor = [(u'',u''),(u'',u'')]
    t = verify(query = u'Any translators? (y or n)')
    if t: translator = basic_query(typ = u'translator')
    else: translator = [(u'',u''),(u'',u'')]
    college = basic_query(typ = u'name of college', multi = u'n', what = u'place',
                          form = u'college;city;country')
    url = basic_query(typ = u'static url', multi = u'n', what = u'url')
    year = basic_query(typ = u'year of publication', what = 'year', multi = 'n')
    pages = num_verify(query = u'Number of pages: ')
    j = citat.Journal(fatemi = fatemi, saheb = saheb, authors = author,
                      editors = editor, translators = translator,
                      college = college, url = url, year = year, pages = pages)
    j.part = part
    j.partof = partof
    return j
    
def qasida_query():
    part = False
    partof = ''
    matlaa = basic_query(typ = u'matlaa', multi = u'n', form = u'matlaa')
    fatemi = verify(query = u'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = u'saheb', multi = u'n')
        author = [(u'',u''),(u'',u'')]
    else:
        author = basic_query(typ = u'author')
        saheb = (u'',u'')
    p = verify(query = u'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = u'name of larger work', multi = u'n',
                               what = u'title')
        part = True
    year = basic_query(typ = u'year of publication', what = u'year')
    verses = num_verify(query = u'Number of verses: ')
    q = citat.Qasida(fatemi = fatemi, matlaa = matlaa, year = year, verses = verses,
                     saheb = saheb, authors = author)
    q.part = part
    q.partof = partof
    return q
    
def website_query():
    '''def __init__(self, uid = '', nameEng = '', nameAra = '', authors = [('','','')],
                 authorsAra = [('', '', '')], date = '', url = '', fatemi = 1)'''
    title = basic_query(typ = u'title of article', what = u'title')
    if fatemi:
        saheb = basic_query(typ = u'saheb', multi = u'n')
        author = [(u'',u''),(u'',u'')]
    else:
        author = basic_query(typ = u'author')
        saheb = (u'',u'')
    date = basic_query(typ = u'Accession date', multi = u'n')
    url = basic_query(typ = u'URL', multi = u'n', what = u'url')
    w = citat.Website(title = title, authors = author, saheb = saheb, date = date,
                      url = url)
    return w
def menu(x):
    c = 0
    cite_type = raw_input(str(u"Enter citation type> enter 'help' for options: "))    
    while c == 0:    
        if cite_type == u'help':
            print u"""Options:
        'book'\t or 1:\t normal book
        'qasida'\t or 2:\t qasida
        'living'\t or 3:\t living source
        'website'\t or 4:\t website
        'journal'\t or 5:\t journal article (like JSTOR)
        'skip'\t or #:\t skip this entry
        NOTE:  Append capital I for istinsakh kutub
        NOTE2: All entries without quotes, so 'book' is actually
        book
    """
        if cite_type == u'skip':
            b = 0
            x += 1
            c = 1
        elif cite_type == u'1' or cite_type == u'book':
            if u'I' in cite_type:
                b = bookIS_query()
            else: b = bookPrint_query()
            x+=1
            c = 1
        elif cite_type == u'2' or cite_type == u'qasida':
            b = qasida_query()
            x += 1
            c = 1
        elif cite_type == u'3' or cite_type == u'living':
            print 'Not available at this moment\n'
            b = 0
            x += 1
            c = 1
        elif cite_type == u'4' or cite_type ==u'website':
            b = website_query()
            x += 1
            c = 1
        elif cite_type == u'5' or cite_type == u'journal':
            b = journal_query()
            x += 1
            c = 1
        else:
            print u"Choose an option"
            b = 0
            c = 0
    return b,x   
   
if __name__ =='__main__':
    opening = verify(query = u'Is there a preexisting list of citations? (y or n): ')
    citations = ''
    cites = []
    c = 1
    x = 0
    if opening:
        cite_name = raw_input(str(u"Citation file: "))
        cite_name = join(curdir,cite_name)
        if cite_name[-2:] == u'db':
            cites=opening_db(cite_name)
        else:
            cite_file = codecs.open(cite_name,'r', 'utf-8')
            cite_raw = cite_file.readlines()
            while c == 1:
                print x+1, '\t', cite_raw[x].encode('utf-8')
                result = menu(x)
                cites.append(result[0])
                x = result[1]
                c = verify(query='Any more citations? (y or n): ')
  
    else:
       while c == 1:
           result = menu(x)
           cites.append(result[0])
           x = result[1]
           c = verify(query='Any more citations? (y or n): ')
    if cites != [0]:                
        for i in cites:
            try:
                print i.encode('utf-8')
            except AttributeError:
                print i
    save = verify(query = u"Would you like to save these citations? (y or n)")
    if save:
        dest = raw_input(str(u'Enter destination file name: '))
        if '/' or '\\' not in dest:
            dest = join(curdir, dest)
        saving_db(dest,cites)
print 'Goodbye\n'
