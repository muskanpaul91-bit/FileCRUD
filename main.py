#Project -CRUD operations

from pathlib import Path
def readfilefolder():
    p=Path('')
    items =list(p.rglob('*'))
    for index, file in enumerate(items):
        print(f"{index+1}. {file}")

def create_file():
    readfilefolder()
    Fname=input("Enter your File name:-")
    p= Path(Fname)
    if p.exists():
        print("File Already exists.")
    else:
        with open(Fname,'w') as file:
            content=input("Enter your file content:-")
            file.write(content)
            print("File Added!")
            
def read_file():
    readfilefolder()
    fname=input('Enter file name:-')
    p= Path(fname)
    if p.exists():
        with open(fname,'r') as file:
            print(file.read())
    else:
        print("File not Found!!")
        

print("Press 1 for creating a file")
print("Press 2 for reading a file")
print("Press 3 for updating a file")
print("Press 4 for deleting a file")

option=int(input("Enter your choice:-"))
if option==1:
    create_file()
elif option==2:
    read_file()
    
    
    def create_file_in_folder():
    folder_name=input('Enter your folder nsme:-')
    file_name=input("Enter your file name.")
    p=Path(folder_name/file_name)
    if p.exists():
        print("FILE ALREADY EXISTS!!")
    else:
        content=input('Enter your content')
        with open(file_name,'w') as file:
            file.write(content)
            print('ADDED!!')
            