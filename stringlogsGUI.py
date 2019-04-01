'''
-parse through files in folder [V]
-search script, exe files, output folder in same directory as script [v]
-output in text [v]
-errors in text [v]
-get offset [-]
-parse using binary headers [-]
-avoid NOT RESPONDING [-]
'''

from tkinter import * 
from tkinter import filedialog
import tkinter.ttk as ttk
import os, glob, sys, re
from plumbum import local

class MyGUI:

    def __init__(self, master):             
        self.master = master
        master.title('Strings and Logs Search GUI')

        self.myLabel = Label(master, text='Chose your image(s):')
        self.myLabel.grid(pady=10, row=0) 

        self.radio_stat = IntVar()
        self.radioFolder = Radiobutton(master, text='All files in folder', variable=self.radio_stat, value=1, command=self.sel_folder)
        self.radioFolder.grid(padx=10, pady=2, row=0, column=1)

        self.radioFile = Radiobutton(master, text='Only one file', variable=self.radio_stat, value=2,command=self.sel_file)
        self.radioFile.grid(padx=10,pady=2, row=0, column=2)
      
        self._Label = Label(master, text='Your image(s) PATH:')
        self._Label.grid(pady=5, row=1)

        self.folderLabel = Label(master, text='...')
        self.folderLabel.grid(pady=5, row=1, column=1, columnspan=2)

        self._separator = ttk.Separator(master, orient='horizontal')
        self._separator.grid(row=2, columnspan=3, sticky=E+W)
        
        self.selectSearchScriptbutton = Button(master, text='Choose your search file:', command = self.get_searchkey)
        self.selectSearchScriptbutton.grid(pady=5,column=1, row=4, padx=10,columnspan =2,sticky=E+W)
        
        self.searchScriptLabel = Label(master, text='Click button to choose text file.')
        self.searchScriptLabel.grid(pady=5, row=4, sticky=W, ipadx=100)
        
        self._separator2 = ttk.Separator(master, orient='horizontal')
        self._separator2.grid(row=5, columnspan=3, sticky=E+W)

        self.beginSearchbutton = Button(master, text='Begin search', command = self.begin_search, fg='white',bg='indian red')
        self.beginSearchbutton.grid(row=7, columnspan =3,sticky=E+W, pady=5)

        self.processStatus = Label(master, text='OUTPUT STATUS')
        self.processStatus.grid(row=8, columnspan =3,sticky=E+W, pady=3)

        self.searchPattern =[]
        self.user_filepath = ''
        self.script_filepath = sys.path[0]
        self.new_path = os.path.join(self.script_filepath, "myOUTPUT")

 
    def sel_folder(self):
        currdir = os.getcwd()
        self.user_filepath = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        self.folderLabel.config(text=self.user_filepath)


    def sel_file(self):
        currdir = os.getcwd()
        self.user_filepath= filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
        self.folderLabel.config(text=self.user_filepath)

    def get_searchkey(self):
        tempfile = filedialog.askopenfilename(parent=root, initialdir=os.path.join(self.script_filepath, "searchScript"), title='Please select a text file', filetypes=[('text file','*.txt')])
        if tempfile:
            print(tempfile) 
            self.searchScriptLabel.config(text=tempfile)
            with open(tempfile) as sf:
                s = sf.read()
                self.searchPattern = [res.strip() for res in s.split(',')]
                print(self.searchPattern)

    def make_dir(self): #creates new folder with the name myOUTPUT
        if not (os.path.exists(self.new_path)):
            os.makedirs(self.new_path)

    def begin_search(self):
        myFiles = glob.glob(self.user_filepath+'/*.*')
        #print("Name of folder/files:"+str(myFiles))
        files_count = len(myFiles)
        print("num of files: "+str(files_count))
        err_count = 0
        suc_count = 0
        grep = local[os.path.join(self.script_filepath,"tools/grep.exe")]
        strings = local[os.path.join(self.script_filepath,"tools/strings.exe")]
        self.make_dir()
        for myfile in myFiles:
            #print(myfile)
            fn = os.path.basename(myfile)           
            print("Processing through "+fn+"...")
            for search in self.searchPattern:
                print("Looking for search word: "+search+"...")
                command = strings[myfile] | grep[search]
                #print("gave command: "+str(command))
                s = re.sub(r'[^A-Za-z0-9]+','', search) #strips all non alphabet from search
                myfName = self.new_path+'/'+fn+'_'+s+'.txt'            
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

        t3 = 'Finished. Out of '+str(files_count)+' file(s):\n Match Found: '+str(suc_count)+'\n Errors(No Match): '+str(err_count)
        self.processStatus.config(text=t3)

root = Tk()
my_gui = MyGUI(root)
root.mainloop()
