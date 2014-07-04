#*-* coding : utf-8 *-*
#qpy:console
import codecs
path_root = '/sdcard/'
docu_path = str(raw_input("file path here: "))
if docu_path[0] == '/':
    pass
else:
    docu_path = path_root + docu_path
docu = open(docu_path,mode ='r')
words = []
punctuation = ['.', ',', "'",'!',
';','-','_','?', '"',
'،','؟','؛']
print punctuation
print test2
for line in docu:
   wordlist = line.split()
   for word in wordlist:
       word = ''.join(ch for ch in word
       	if ch not in punctuation)
       words.append(word)
word_path = str(raw_input("enter word file (add extracted to the beginning of the source file): "))
if word_path[0] == '/':
    pass
else:
    word_path = path_root + word_path
word_file = codecs.open(word_path,'r+w',
	encoding = 'utf-8')
text = "".join(w.encode(encoding='utf-8') + '\n' for w in words)
word_file.writelines(words)
word_file.close()
docu.close()
