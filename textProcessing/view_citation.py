#-*-coding:utf8-*
#qpy:2
#qpy:console
#786
#bihi wa bi waliyyihi wa bi daihi Syedna Aali Qadr Mufaddal Saifuddin TUS
#asta'eeno fi jamee' il umoor
import re, codecs, citat, sqlite3
from import_citation import verify
from operator import itemgetter
from os.path import dirname,join
from getdir import curdir
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

