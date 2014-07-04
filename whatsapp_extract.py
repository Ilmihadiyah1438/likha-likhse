#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import codecs, re, brevity
def get_info(name = 'Abdeali Jamali',
	files =[]):
    prompt1 = raw_input(str('Your name: '))
    prompt2 = raw_input(str('Filename: '))
    prompt3 = raw_input(str('Out file'))
    
    if prompt1 is True:
        name = prompt1
    else: pass
    in_file = brevity(prompt2)
    out_file = brevity(prompt3)
    return name, in_file, out_file
def main_loop(itern = 0):
    print itern  
    info = get_info()
    in_file = codecs.open(info[1], 
    	mode = 'r')
    out_file = codecs.open(info[2],
    mode = 'w')
    date = r'\w{3} \d{1,2}, \d{1,2}:\d{2}'
    for line in in_file:
        divi = re.split(':', line, maxsplit = 2)
        print re.search(date, line)
        if re.search(date, line):
            print 'hi'
            if info[0] in divi[1]:
               print info[0]
               out_file.write(divi[2])

cont = 'y'
i = 1
while cont != 'n':
    main_loop(i)
    i+= 1
    cont = raw_input(str('Continue? y or n: '))                