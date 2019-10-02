from os import rename, listdir 

files_platinum = listdir('.')

count = 0 
for name in files_platinum:
   
    new_name = name.replace(name, "platinum_%d.jpg" %count)
    rename(name,new_name)
    count += 1
