#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import re, codecs, brevity,pprint
citation = {
'kitab_id': {'name':['',''],
             'authors':[['','']],
             'publisher':['',''],
             'pub_date':['',''],
             'c_type':'',
             'pub_country':['',''],
             'pub_city':['',''],
             'fatemi': 0,
             'pages': ''
             }
            }
def form_re(cite_type, order):
    dlmtr_name = raw_input(
    	str('name delimiter: '))
    dlmtr_authors = raw_input( 
     str('authors delimiter: '))
    dlmtr_publish = raw_input(
     str('publishing delimiter: '))
def verify(inp):
    print inp
    answer = raw_input(str('Is this correct? 1 for yes, 0 for no: '))
    return int(answer)
   
if __name__ =='__main__':
    cite_name = raw_input(str("Citation file: "))
    cite_file = codecs.open(cite_name,'r', 'utf-8')
    cite_raw = cite_file.readlines()
    x = 1
    for c in cite_raw:
        print x, '\t', c.encode('utf-8')
        c = 0
        while c == 0:
            cite_type = raw_input(str("Enter citation type> enter 'help' for options: "))          
            if cite_type == 'help':
                print """Options:
                'book' or 1: normal book
                'qasida' or 2: qasida
                'living' or 3: living source
                'website' or 4: website
                'journal' or 5: journal article (like JSTOR)
                'same' or 7: same type, same format as the one before it
                'skip' or 0: skip this entry
                NOTE: Append capital F to end of option for 'Fatemi' sources
                      like 'bookF' or '2F'
                      Append capital A for arabic citations, E for english
                      Append capital I for istinsakh kutub
                NOTE2: All entries without quotes, so 'book' is actually
                book
            """
            elif cite_type == 'skip':
                x += 1
                c = 1
            elif ('book' or '1') in cite_type:
                if 'F' or 'f' in cite_type:
                    citation[x]['fatemi'] = 1
                print 'book'
                x+=1
                c = 1
            elif ('qasida' or '2') in cite_type:
                if 'F' or 'f' in cite_type:
                    citation[x]['fatemi'] = 1
                print 'qasida'
                x += 1
                c = 1
            elif ('living' or '3') in cite_type:
                if 'F' or 'f' in cite_type:
                    citation[x]['fatemi'] = 1
                print 'living'
                x += 1
                c = 1
            elif ('website' or '4') in cite_type:
                if 'F' or 'f' in cite_type:
                    citation[x]['fatemi'] = 1
                print 'website'
                x += 1
                c = 1
            elif ('journal' or '5') in cite_type:
                if 'F' or 'f' in cite_type:
                    citation[x]['fatemi'] = 1
                print 'journal'
                x += 1
                c = 1
            elif ('same' or '7') in cite_type:
                print 'same'
                try:
                    citation[x] = citation[x-1]
                    x += 1
                    c =1
                except KeyError:
                    print "You havent entered any info for the last one!"
                    
                
    citations = pprint.pprint(citation)
    v = verify(citations)
    if v:
        out_name = raw_input(str("Enter out file name: "))
        out = codecs.open(out_name, 'w', 'utf-8')
        out.write(citations)                            
            
            
            
            
            
            
            
            
            