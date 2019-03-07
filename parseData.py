import glob
import sys
import re
import os
from plumbum import local
#from plumbum.cmd import grep


myPATH = 'D:/' #input("Folder Path: ")

#print(glob.glob(myPATH+'/*.txt'))
myFILES =glob.glob(myPATH+'/*.mdf') #List of all mdf files in myPATH folder
searchPattern =['http','https']

strings = local["C:/"] #loc of my strings.exe
grep = local["C:/"]

files_count = len(myFILES)
print('Number of files to parse: ' + str(files_count))

suc_count =0
err_count =0

for myfile in myFILES: #for each file in the folder
    fn = os.path.basename(myfile)
    print("Processing through "+fn+"...")
    for search in searchPattern: #for each search word in searchPattern
        command = strings[myfile] | grep[search] #command to cmd
        s = re.sub(r'[^A-Za-z]+','', search) #strips all non alphabet from search
        myfName = 'C:/.../results/'+fn+'_'+s+'.txt'
        while True:
            try:
                (command > myfName)() #execute command; output to [filename][search word].txt 
                suc_count +=1
                break
            except KeyboardInterrupt:
                raise StopIteration
            except: #all exceptions
                err_count +=1          
                err = str(sys.exc_info()[0])
                with open(myfName, 'w+') as errf:
                    errf.write(err +'\nNo Match was found')
                print ('No Match Found.') 
                break #break when error

print('Finished. Out of '+str(files_count)+':\n Match Found: '+str(suc_count)+'\n Errors(No Match): '+str(err_count))


        
