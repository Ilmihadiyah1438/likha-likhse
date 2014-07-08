#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import html2text, codecs, glob, re, brevity
'''this is a module to extract info from .html files
Here i used it for al-kanz'''
numbers = {u'الاول': 1,
u'الثاني' : 2,
u'الثالث' : 3,
u'الرابع' : 4,
u'الخامس' : 5,
u'السادس' : 6,
u'السابع' : 7,
u'الثامن' : 8,
u'التاسع' : 9,
u'العاشر' : 10,
}
    	
def get_info():
    file_name = raw_input(str('Filename: '))
    file_name = brevity.brevity(file_name, home = '', ext = '.html')#change to your home directory
    return file_name
           
def parse_html(f_name):
    h_file = codecs.open(f_name, 'r', 'utf-8')
    h_raw = ''.join(h_file.readlines())
    sections = re.split(ur'<br>', h_raw, flags = re.IGNORECASE)
    h_edited = html2text.html2text(sections[1])
    hdng_re = re.compile(
ur'(?P<year>\d+) (?P<majlis>\w+) (?P<maj_no>\w+)', re.U)
    hdng_raw = hdng_re.search(h_edited)
    hdng_dict = hdng_raw.groupdict()
    number = nmbrs[hdng_dict[u'maj_no']]    
    hdng_edit = u"mjls_{no}_{yr}".format(
    	no = number, 
    	yr = hdng_dict[u'year'])	
    return hdng_edit, h_edited
    
def extrctn(f_name = '', f_list = []):
    if f_name:
        ex = parse_html(f_name)
        out_name = brevity.brevity(f_name)
        out_file = codecs.open(out_name, 'w', 'utf-8')
        out_file.writelines(ex[1])
    if f_list:
        edit = {}
        for f in f_list:
            ex = parse_html(f)
            if ex[0] not in edit.keys():
                edit[ex[0]] = []
                edit[ex[0]].append(''.join(ex[1]))
            elif ex[0] in edit.keys():
                edit[ex[0]].append(ex[1])
        for e in edit.keys():
            ind = 1
            for fi in edit[e]:
                out_name = '/sdcard/extracted/'+e+u'_'+unicode(ind)+'.txt'
                out_file = codecs.open(
                	out_name, 'w', 'utf-8')
                out_file.writelines(fi)
                ind += 1
            
if __name__='__main__':
    #kanz_docs = glob.glob('/sdcard/ikanz/kanz*.html')
    #extrctn(f_list=kanz_docs)
    f = get_info()
    extrctn(f_name=f)