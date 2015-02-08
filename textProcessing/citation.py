#-*-coding:utf8;-*-
#qpy:2
#qpy:console
#786
#bihi wa bi waliyyihi wa bi daihi Syedna Aali Qadr Mufaddal Saifuddin TUS
#asta'eeno fi jamee' il umoor
import re, codecs, brevity,pprint, citat, sqlite3
from operator import itemgetter
from os.path import dirname,join
citation = []
cur_dir = dirname(__file__)
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
    if v.lower() == 'y':
        b = True
    else: b = False
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
def opening_db(file_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute('select * from kitabs')
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
        cur = conn.cursor()
        cur.execute('''select * from booktoauthors
where booktoauthors.kit = "?";''', i[0])
        aet = cur.fetchall()
        for z in aet:
            cur.execute('''select * from authors where authors.id = "?";''', z[1])
            auth_info = cur.fetchall()
            f = auth_info[3]
            a = (auth_info[1],auth_info[2])
            ai = z[2]
            ac = auth_info[4]
            auth.append((a,ai,ac))
            cur.execute('''select * from editors where editors.id = "?";''', z[3])
            edi_info = cur.fetchall()
            e = (edi_info[1], edi_info[2])
            ei = z[4]
            edi.append((e,ei))
            cur.execute('''select * from translators where translators.id = "?";''',z[5])
            tra_info = cur.fetchall()
            t = (tra_info[6],tra_info[7])
            ti = z[6]
            tra.append((t,ti))
        c.authors = [at[0] for at in sorted(auth, key = itemgetter(1))]
        c.editors = [et[0] for et in sorted(edi, key = itemgetter(1))]
        c.translators = [tr[0] for tr in sorted(tra, key =  itemgetter(1))]
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
            if a == b:
               equal.append(a)
            elif a[0] == b[0]:
               diff1.append(a)
            elif a[1] == b[1]:
               diff2.append(a)
            elif (a[0] and a[1]) != (b[0] and b[1]):
               new.append(a)
               
    return equal,diff1,diff2,new     

def saving_db(file_name,cite_list):
    create = ''
    try:
        codecs.open(file_name)
    except IOError:
        create = codecs.open(join(cur_dir,'biblio.sql'),'r').read()
    conn = sqlite3.connect(file_name)
    if create:
        conn.execute(create)
    cur = conn.cursor()
    e = cur.execute('select * from kitabs')
    exist_cites = [c[0] for c in e.fetchall()]
    prog_cites = [c for c in cite_list]
    new_cites = [c for c in prog_cites if c.uid not in exist_cites]
    update_cites = [c for c in prog_cites if c.uid in exist_cites]
    e = cur.execute('select * from authors')
    exist_authors = [a[1:2] for a in e.fetchall()]
    prog_authors = [a.authors for a in cite_list]
    diff = compare(exist_authors, prog_authors)
    update_authors = diff[0:2]
    new_authors = diff[3]
    e = cur.execute('select * from editors')
    exist_editors = [a[1:2] for a in e.fetchall()]
    prog_editors = [a.editors for a in cite_list]
    diff = compare(exist_editors, prog_editors)
    update_editors = diff[0:2]
    new_editors = diff[3]
    e = cur.execute('select * from translators')
    exist_translators = [a[1:2] for a in e.fetchall()]
    prog_translators = [a.translators for a in cite_list]
    diff = compare(exist_translators, prog_translators)
    update_translators = diff[0:2]
    new_translators = diff[3]
    #USE UPDATE INSTEAD OF REPLACE
    for c in cite_list:
        k =[('uid',c.uid),('fatemi',c.fatemi),('titleAra',c.titleAra),
        ('titleEng',c.titleEng),('type',c.type),('istinsakh',c.istinsakh),
        ('publisherAra',c.publisherAra),('publisherEng',c.publisherEng),
        ('pub_dateH',c.pub_dateH),('pub_dateG',c.pub_dateG),
        ('pub_placeAra',c.pub_placeAra),('pub_placeEng',c.pub_placeEng),
        ('volumes',c.volumes),('pages',c.pages),('notesAra',c.notesAra),
        ('notesEng',c.notesEng),('partOf',c.partOf)]
        e = cur.execute('''SELECT * FROM kitabs WHERE uid = "?"''', c.uid)
        for at in c.authors:
            if at in new_authors:
                ins = 'INSERT INTO authors (nameAra = "{0}", nameEng = "{1}");'.format(
                            at[0],at[1])
                cur.execute(ins)
            elif at in update_authors[0]:
                upd = 'UPDATE authors SET nameAra = "{0}" WHERE nameEng = "{1}";'
            elif at in update_authors[1]:
                upd = 'UPDATE authors SET nameEng = "{1}" WHERE nameAra = "{0}";'
            upd = upd.format(at[0], at[1])
            cur.execute(upd)
                        
        for ed in c.editors:
            if ed in new_editors:
                ins = 'INSERT INTO editors (nameAra = "{0}", nameEng = "{1}");'.format(
                            ed[0],ed[1])
                cur.execute(ins)
            elif ed in update_editors[0]:
                upd = 'UPDATE editors SET nameAra = "{0}" WHERE nameEng = "{1}";'
            elif ed in update_editors[1]:
                upd = 'UPDATE editors SET nameEng = "{1}" WHERE nameAra = "{0}";'
            upd = upd.format(ed[0], ed[1])
            cur.execute(upd)

        for tr in c.translators:
            if tr in new_translators:
                ins = 'INSERT INTO translators (nameAra = "{0}", nameEng = "{1}");'.format(
                            tr[0],tr[1])
                cur.execute(ins)
            elif tr in update_translators[0]:
                upd = 'UPDATE translators SET nameAra = "{0}" WHERE nameEng = "{1}";'
            elif tr in update_translators[1]:
                upd = 'UPDATE translators SET nameEng = "{1}" WHERE nameAra = "{0}";'
            upd = upd.format(tr[0], tr[1])
            cur.execute(upd)
        if e.fetchall():
            for i in k[1:]:               
                kit = 'UPDATE kitabs SET {0} WHERE uid = "{1}";'
                entry = '"{0}" = "{1}"'.format(i[0], i[1])
                kit = kit.format(kit,c.uid)
                cur.execute(kit)
        else:    
            kit = 'INSERT INTO kitabs ({0});'
            entry = ''
            for i in k[:-1]:
                if i:
                    entry += '"{0}" = "{1}",'.format(i[0],i[1])
            if k[-1]:
                entry += '"{0}" = "{1}"'.format(k[-1][0],k[-1][0])
            kit = kit.format(entry)
            cur.execute(kit)
        
        def indices(person,abbv):
            au_index = 1
            index = cur.execute("""
SELECT ?_index FROM booktoauthors
WHERE kit ='?' ORDER BY ?_index;""", (abbv,c.uid,abbv))
            index = index.fetchall()
            ind_list = []
            for i in index:
                names = cur.execute(
'''SELECT nameAra, nameEng FROM ? WHERE id = ?;''',
(person, i))
                names = names.fetchall()
                ind_list.append(names)
            return ind_list
        
        a = indices('authors','aut')
        e = indices('editors', 'edi')
        t = indices('translators', 'tra')                
                
        if a == c.authors: pass
        else:
            ind = 0
            for auth in c.authors:
                if auth == a[ind]:
                    ind += 1
                else: 
                    a[ind] = auth
                    a_ind = cur.execute("""
SELECT id FROM authors where nameEng = '?';""",
auth[1]).fetchone()
                    cur.execute("""
INSERT INTO booktoauthors (kit,aut,aut_index)
VALUES (?,?,?);""",(c.uid,a_ind[0],ind+1))
                    ind += 1
        if e == c.editors: pass
        else:
            ind = 0
            for edi in c.editors:
                if edi == e[ind]:
                    ind += 1
                else: 
                    e[ind] = edi
                    e_ind = cur.execute("""
SELECT id FROM editors where nameEng = '?';""",
edi[1]).fetchone()
                    cur.execute("""
INSERT INTO booktoauthors (kit,edi,edi_index)
VALUES (?,?,?);""",(c.uid,e_ind[0],ind))
                    ind += 1
        if t == c.translators: pass
        else:
            ind = 0
            for tra in c.translators:
                if tra == t[ind]:
                    ind += 1
                else: 
                    t[ind] = tra
                    t_ind = cur.execute("""
SELECT id FROM translators where nameEng = '?';""",
auth[1]).fetchone()
                    cur.execute("""
INSERT INTO booktoauthors (kit,tra,tra_index)
VALUES (?,?,?);""",(c.uid,t_ind[0],ind))
                    ind += 1
    cur.commit()
        
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
            form = 'title,subtitle (if title contains a semicolon, insert && in place of it)'
            multi = 'n'
        elif what == 'url':
            form = 'url (replace semicolons with &&)'
            multi = 'n'
        elif what == 'place':
            form = 'city,country'
            multi = 'n'
        elif what == 'date':
            form = 'dd/mm/yyyy (If info is not available, type only what is available)'
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
    part = False
    partof = ''
    title = basic_query(typ = 'title', multi = 'n', what = 'title')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    p = verify(query = 'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = 'name of larger work', multi = 'n',
                               what = 'title')
        part = True
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
    b.partof = partof
    b.part = part
    return b
                     
def bookIS_query():
    part = False
    partof = ''
    title = basic_query(typ = 'title', multi = 'n', what = 'title')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]               
    else:
        author = basic_query(typ= 'author')
        saheb = [('',''),('','')]
    p = verify(query = 'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = 'name of larger work', multi = 'n',
                               what = 'title')
        part = True
    khizana = basic_query(typ = 'khizana', multi = 'n')
    location = basic_query(typ = 'location of khizana', multi = 'n', what = 'city')
    year = basic_query(typ = 'year of IS', what = 'year', multi = 'n')
    pages = num_verify(query = 'Number of pages: ')
    i = citat.BookIS(fatemi = fatemi, saheb = saheb, author = author,
                     khizana = khizana, location = location, year = year,
                     pages = pages)
    i.partof = partof
    i.part = part
    return i
    
def journal_query():
    part = False
    partof = ''
    title = basic_query(typ = 'title', multi = 'n', what = 'title')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')                        
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    p = verify(query = 'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = 'name of larger work', multi = 'n',
                               what = 'title')
        part = True
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
    j.part = part
    j.partof = partof
    return j
    
def qasida_query():
    part = False
    partof = ''
    matlaa = basic_query(typ = 'matlaa', multi = 'n', form = 'matlaa')
    fatemi = verify(query = 'Is source Fatemi? (y or n): ')
    if fatemi:
        saheb = basic_query(typ = 'saheb', multi = 'n')
        author = [('',''),('','')]
    else:
        author = basic_query(typ = 'author')
        saheb = ('','')
    p = verify(query = 'Is this part of a larger work? (y or n)')
    if p:
        partof = basic_query(typ = 'name of larger work', multi = 'n',
                               what = 'title')
        part = True
    year = basic_query(typ = 'year of publication', what = 'year')
    verses = num_verify(query = 'Number of verses: ')
    q = citat.Qasida(fatemi = fatemi, matlaa = matlaa, year = year, verses = verses,
                     saheb = saheb, authors = author)
    q.part = part
    q.partof = partof
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
        NOTE:  Append capital I for istinsakh kutub
        NOTE2: All entries without quotes, so 'book' is actually
        book
    """
    elif cite_type == 'skip':
        x += 1
    elif ('book' or '1') in cite_type:
        if 'I' in cite_type:
            b = bookIS_query()
        else: b = bookPrint_query()
        x+=1
    elif ('qasida' or '2') in cite_type:
        b = qasida_query()
        x += 1
    elif ('living' or '3') in cite_type:
        print 'Not available at this moment\n'
        x += 1
    elif ('website' or '4') in cite_type:
        b = website_query()
        x += 1
    elif ('journal' or '5') in cite_type:
        b = journal_query()
        x += 1
    else:
        print "Choose an option"
        c = 0
    more = verify('Any more citations (y or n)')
    if more: c = 0
    else: c = 1
    return b,x,c     
   
if __name__ =='__main__':
    opening = verify(query = 'Is there a preexisting list of citations? (y or n): ')
    citations = ''
    cites = []
    c = 0
    x = 1
    if opening:
        cite_name = raw_input(str("Citation file: "))
        if '/' or '\\' not in cite_name:
            cite_name = join(cur_dir,cite_name)
        if cite_name[-2:] == 'db':
            cites=opening_db(cite_name)
        else:
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
        print i.encode('utf-8')
    save = verify(query = "Would you like to save these citations? (y or n)")
    if save:
        dest = raw_input(str('Enter destination file name: '))
        if '/' or '\\' not in dest:
            dest = join(cur_dir, dest)
        saving_db(dest,cites)
print 'Goodbye\n'
