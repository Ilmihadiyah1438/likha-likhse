#-*-coding:utf8;-*-
#qpy:2
#qpy:console
import re, codecs
data = codecs.open('/sdcard/words.csv','rw+','utf-8')
da = [d.replace('"','').split(',') for d in data]
print da[0]
words = {k[1].replace('\n',''):k[0] for k in da}
print words[u'جماعة']
hard_vowels = [
[u'aa', u'a'],
[u'ee', u'i', u'y'],
[u'oo', u'u']
]
madd_leen=[
[u'au', u'aw'],
[u'ay', u'ai']
]
soft_vowels = [
[u'a'],
[u'e'],
[u'i'],
[u'o'],
[u'u']
]
letters = {
u"ا":[u'a', hard_vowels[0], soft_vowels],
u'أ':[soft_vowels[0], soft_vowels[3:4]],
u'إ':soft_vowels[1:2],
u'آ':hard_vowels[0],
u'ٱ':hard_vowels[0],
u"ب":u'b',
u"ت":u't',
u"ث":u'th',
u"ج":u'j',
u"ح":u'h',
u"خ":u'kh',
u"د":u'd',
u"ذ":u'z',
u"ر":u'r',
u"ز":u'z',
u"س":u's',
u"ش":u'sh',
u"ص":u's',
u"ض":u'd',
u"ط":u't',
u"ظ":u'z',
u"ع":u'`',
u'غ':u'gh',
u'ف':u'f',
u'ق':u'q',
u'ك':u'k',
u'ل':u'l',
u'م':u'm',
u'ن':u'n', 
u'و':[u'v', u'w', hard_vowels[1]],
u'ه':u'h',
u'ء':u"'a",
u'ؤ':u"'u",
u"ئ":u"'i",
u'ى':hard_vowels[0],
u"ي":[u'y', hard_vowels[2]],
u'ئ':soft_vowels[2:3],
u"پ":u'p',
u"چ":u'ch',
u'گ':u'g',
u'ڑ':u'r',
u'ڈ':u'd',
u'ٹ':u't',
u'ں':u'n',
u'ے':soft_vowels[1],
u'ة':[u'h',u't']
}
iraab = {
u'َ':soft_vowels[0],
u'ِ':soft_vowels[1:2],
u'ُ':soft_vowels[3:4],
u'ٰ':hard_vowels[0],
u'ٖ':hard_vowels[1],
u'ٗ':hard_vowels[2],
u'ً':u'an',
u'ٍ':u'in',
u'ٌ':u'un',
u'ْ':u'**sukun',
u'ّ':u'**tashdeed'
}
def ara_eng(inp_ara):
    out_eng = inp_ara.replace(u'\u0640','')
    if inp_ara in words.keys():
        print 'db\t', words[inp_ara]
        return words[inp_ara]
    for a in letters.keys():
        repl_a = letters[a]
        while type(repl_a) == type([]):
            repl_a = repl_a[0]
        out_eng = out_eng.replace(a, repl_a)
    for b in iraab.keys():
        repl_b = iraab[b]
        while type(repl_b) == type([]):
            repl_b = repl_b[0]
        out_eng = out_eng.replace(b,
        	repl_b)   	
    return out_eng
def eng_ara(inp_eng):
    
inp_name = raw_input(str("araFile name: "))
in2_file = raw_input(str("engFile name: "))
inp_file0 = codecs.open(inp_name, 'r', 'utf-8')
inp_file1 = codecs.open(in2_file, 'r', 'utf-8')
ara = ''.join([l for l in inp_file0]).split()
eng = ''.join([l for l in inp_file1]).split()
print ara[0].encode('utf-8')
tran = [basic(a) for a in ara]
tran2 = []
print "progr \t hand"
add = {}
for a,b,c in zip(tran, eng, ara):
    if a != b.lower():
        print a, '\t', b.lower(), c.encode('utf-8')
        if ara not in add.keys():
            add[c] = b.lower()
data = codecs.open('/sdcard/words.csv','a','utf-8')
for i in add.keys():
    data.write('\n')
    r = u'"{1}","{0}"'.format(i,add[i])
    data.write(r)

