    import sys,os,file

    if os.path.exists("E:\leozheng"):
        file.delete_file_folder("E:\leozheng")
    if not os.path.exists("E:\leozheng"):
        os.makedirs("E:\leozheng")
    if not os.path.isfile("E:\leozheng\leozheng.pid"):
        file=open("E:\leozheng\leozheng.pid","w",encoding="utf-8" )