from pathlib import Path
import os
import streamlit as st

st.set_page_config(page_title="File Manager", layout="centered")

st.title("📂 File Handling CRUD App")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create File",
        "Read File",
        "Update File",
        "Delete File",
        "Rename File",
        "Create Folder",
        "Delete Folder"
    ]
)

# Show existing files/folders
st.subheader("Existing Files & Folders")
items = list(Path(".").rglob("*"))

for item in items:
    st.write(item)

# CREATE FILE
if menu == "Create File":
    st.header("Create File")

    filename = st.text_input("Enter file name")
    content = st.text_area("Enter file content")

    if st.button("Create"):
        p = Path(filename)

        if p.exists():
            st.error("File already exists!")
        else:
            with open(filename, "w") as file:
                file.write(content)

            st.success("File created successfully!")

# READ FILE
elif menu == "Read File":
    st.header("Read File")

    filename = st.text_input("Enter file name")

    if st.button("Read"):
        p = Path(filename)

        if p.exists():
            with open(filename, "r") as file:
                st.text(file.read())
        else:
            st.error("File does not exist!")

# UPDATE FILE
elif menu == "Update File":
    st.header("Update File")

    filename = st.text_input("Enter file name")

    option = st.radio(
        "Choose option",
        ["Overwrite", "Append"]
    )

    content = st.text_area("Enter content")

    if st.button("Update"):
        p = Path(filename)

        if p.exists():

            mode = "w" if option == "Overwrite" else "a"

            with open(filename, mode) as file:
                file.write(content)

            st.success("File updated!")
        else:
            st.error("File does not exist!")

# DELETE FILE
elif menu == "Delete File":
    st.header("Delete File")

    filename = st.text_input("Enter file name")

    if st.button("Delete"):
        p = Path(filename)

        if p.exists():
            os.remove(p)
            st.success("File deleted!")
        else:
            st.error("File does not exist!")

# RENAME FILE
elif menu == "Rename File":
    st.header("Rename File")

    filename = st.text_input("Old file name")
    new_name = st.text_input("New file name")

    if st.button("Rename"):
        p = Path(filename)

        if p.exists():
            p.rename(new_name)
            st.success("File renamed!")
        else:
            st.error("File does not exist!")

# CREATE FOLDER
elif menu == "Create Folder":
    st.header("Create Folder")

    folder_name = st.text_input("Folder name")

    if st.button("Create Folder"):
        p = Path(folder_name)

        if p.exists():
            st.error("Folder already exists!")
        else:
            p.mkdir()
            st.success("Folder created!")

# DELETE FOLDER
elif menu == "Delete Folder":
    st.header("Delete Folder")

    folder_name = st.text_input("Folder name")

    if st.button("Delete Folder"):
        p = Path(folder_name)

        if p.exists():
            p.rmdir()
            st.success("Folder deleted!")
        else:
            st.error("Folder does not exist!")