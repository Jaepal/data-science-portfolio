from os import rename, listdir 

files_platinum = listdir('.')
files_monster = listdir('.')
files_masque = listdir('.')

count = 0 
for name in files_platinum:
   
    new_name = name.replace(name, "platinum_%d.jpg" %count)
    rename(name,new_name)
    count += 1

count = 0
for name in files_monster:
   
    new_name = name.replace(name, "monster_%d.jpg" %count)
    rename(name,new_name)
    count += 1

count = 0
for name in files_masque:
   
    new_name = name.replace(name, "masque_%d.jpg" %count)
    rename(name,new_name)
    count += 1