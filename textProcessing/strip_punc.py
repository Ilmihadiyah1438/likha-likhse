#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This is console module"

import sys,getopt, codecs
punctuation = [u'.', u',', u"'",u'!',
u';',u'-',u'_',u'?', u'"', u'،', u'؛', 
u'؟']
def strip(docu):
    word = ''
    if type(docu) == type([]):
        for line in docu:
           word += ''.join(
        ch for ch in line
   	     if ch not in punctuation)
    else: word = ''.join(ch for ch in docu if ch not in punctuation)
    return word
if __name__ == "__main__":
    try:
        docu = codecs.open(sys.argv[1],'r','utf-8')
        out = codecs.open(sys.argv[2],'w','utf-8')
    except IOError:
        d_file = raw_input(str('File: '))
        o_file = raw_input(str('Out: '))
        docu = codecs.open(docu,'r','utf-8')
        out = codecs.open(o_file,'w','utf-8')
    words = strip(docu)
    out.writelines(words)
    out.close