#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This is console module"

import sys,getopt, codecs
words = []
punctuation = [u'.', u',', u"'",u'!',
u';',u'-',u'_',u'?', u'"', u'،', u'؛', 
u'؟']
if __name__ == "__main__":
    docu = codecs.open(sys.argv[1],'r','utf-8')
    out = codecs.open(sys.argv[2],'w','utf-8')
else:
    d_file = raw_input(str('File: '))
    o_file = raw_input(str('Out: '))
    docu = codecs.open(docu,'r','utf-8')
    out = codecs.open(o_file,'w','utf-8')
words = []
for line in docu:
   word = ''.join(ch for ch in line
   	    if ch not in punctuation)
   words.append(word)
out.writelines(words)
out.close