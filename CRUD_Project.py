from pathlib import Path
import os
def readfilefolder():
    try:
         p= Path(".")
         items=list(p.rglob('*'))
         for index, item in enumerate(items):
             print(f'{index+1}. {item}')
    except Exception as e:
        print(e)

def create_file():
    try:
        readfilefolder()
        filename=input("Enter your file name:-")
        p=Path(filename)
        if p.exists():
            print("FILE ALREADY EXISTS..")
        else:
            with open(filename,'w') as file:
                content=input("Enter content of your file:-")
                file.write(content)
                print("File Added!!")
    except Exception as e:
        print(e)        

def read_file():
    try:
        print("Here are the existing Files..")
        readfilefolder()
        choice=input("Enter your File name:-")
        p=Path(choice)
        if p.exists():
            with open(choice,'r') as file:
                print(file.read())
        else:
            print("File not exists, please first create your file!!")
    except Exception as e:
        print(e)
        
def update_file():
    try:
        print("Here are the existing Files..")
        readfilefolder()
        filename=input("Enter your file name:-")
        a=Path(filename)
        if a.exists():
            print('Press 1 to overwrite content')
            print('Press 2 to append new content')
            option =int(input('Enter your choice:-'))
            if option==2:
                content=input("Enter your content:-")
                with open(filename, 'a') as file:
                    file.write(content)
                    print('Done!')
            elif option==1:
                content=input("Enter your content:-")
                with open(filename,'w') as file:
                    file.write(content)
                    print('Done!')
            else:
                print('Invalid option')
        else:
            print("FILE DOES NOT EXISTS!!")
    except Exception as e:
        print(e)
        
def delete_file():
    try:
        readfilefolder()
        print("Here are the existing Files..") 
        filename=input("Enter your file name:-")
        p=Path(filename)
        if p.exists():
            os.remove(p) #os is removing your file completely from the system
            print('done')
        else:
            print("FILE DOES NOT EXISTS!!")
    except Exception as e:
        print(e)
        
def rename_file():
    try:
        readfilefolder()
        filename=input("Enter file name:-")
        p=Path(filename)
        if p.exists():
            new_name=input('Enter new name of file:-')
            p.rename(new_name)
            print('FILED RENAMED!!')
        else:
            print('FILE DOES NOT EXISTS!!')
    except Exception as e:
        print(e)
        
def create_folder():
    try:
        readfilefolder()
        folder_name=input('Enter your folder name:-')
        p=Path(folder_name)
        if p.exists ():
            print("FOLDER ALREADY EXISTS!!")
        else:
            p.mkdir()
            print('FOLDER CREATED!!')
    except Exception as e:
        print(e)

def delete_folder():
    try:
        readfilefolder()
        folder_name=input('Enter folder name:-')
        p=Path(folder_name)
        if p.exists():
            p.rmdir()
            print("FILE REMOVED!!")
        else:
            print('FILE DOES NOT EXISTS!!')
    except Exception as e:
        print(e)
        

       
while True:       
    print("Press 1 for creating a file.")
    print("Press 2 for reading a file. ")
    print("Press 3 for updating a file.")
    print("Press 4 for deleting a file.")
    print('Press 5 to rename your file')
    print('Press 6 to create a folder.')
    print('Press 7 to delete a folder')
    print('Press 0 to exist.')

    option=int(input("Enter your choice:-"))
    if option==1:
        create_file()  
    elif option==2:
        read_file()
    elif option ==3:
        update_file()
    elif option ==4:
        delete_file()
    elif option ==5:
        rename_file()
    elif option==6:
        create_folder()
    elif option==7:
        delete_folder()
    elif option ==0:
        print("Thanks for visiting..")
        break
    else:
        print('INVALID OPTION SELECTED!! PLEASE SELECT THE CORRECT OPTION..')
    