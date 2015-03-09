'''
usage: load txt file to the mongodb database as such format we can see in file './data_sample.json'  
'''


import os,sys
print "sys code is:", sys.getdefaultencoding() 
code_type = 'utf-8'   #windows gb2312, osx utf-8



import json

HY_list = [] #global list to store kinds of hangye

files_path= os.path.join(os.path.abspath('.'), 'categories')
print "files's path is: %s" % files_path



txtfiles = [ x for x in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, x)) \
                and os.path.splitext(x)[1] == '.txt' ]
print txtfiles[1].decode(code_type)   #windows gb2312, osx utf-8
print '-------------------'
for x in txtfiles:
    global HY_list
    print x
    temp = {} #dict to record the specific hangye such as linye..
    temp['HY'] = x.split('.')[0] # {"HY": "linye", ...}
    f = open(os.path.join(files_path, x), 'r')
    for line in f.readlines():
        line = line.strip('\n')
        linelist = line.split()
        #print "%s" % linelist[1]
        lname = {}
        lname['name'] = linelist[1].decode('gbk').encode(code_type)
        #lname['name'] = linelist[1]  in windows, it is likely ok.
        temp[linelist[0]] = lname
    HY_list.append(temp) #add the dict record
    f.close()

#print HY_list[1]['sh600366']['name'].decode('gbk')  #utf8
#print HY_list[1]['sh600366']
f = open('HY_list.json', 'w')

str_json = json.dumps(HY_list, indent = 4, encoding = code_type)  #windows gb2312, osx utf-8
str_json = str_json.decode('raw_unicode_escape')
str_json = str_json.encode(code_type) #windows gb2312, osx utf-8
print str_json
f.write(str_json)
f.close()

'''
from pymongo import MongoClient
mClient=MongoClient('54.169.18.100', 27017)
db=mClient.test  #test database
hy=db.hy   #hy collection

f = open('HY_list.json', 'r')
string = f.read()   #string encoded as gb2312 in windows, utf-8 in osx 
print string
l = json.loads(string, encoding = code_type)

print l[1]
hy.insert(l)  #l contains all hy dict l=[hy1,hy2,...] hy1={'HY':..,'sz0001':{'name':.,..},..}

f.close()
'''



'''
f = open('HY_list.json', 'r')

d = json.loads(f.read())

f.close()

f = open('HY_list.json', 'w')
d[1]['sz000001'] = {'name' : 'test1'} #insert {"sz000001" : {"name":"test1"}} into d[1]

d[0]['sh600359']['name'] = 'change'  #change {"sh600359" : {"name":"..."}} into {"sh600359" : {"name":"change"}} in d[0]

str_json = json.dumps(d, indent = 4)
str_json = str_json.decode('raw_unicode_escape')
str_json = str_json.encode('utf-8')
print str_json.__class__
f.write(str_json)
f.close()
'''
