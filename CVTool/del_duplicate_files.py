'''
Delete duplicate files by MD5 and name
'''
import hashlib
import os
import util

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myHash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest()


ref_filedir =input("Dir use to reference: ").strip()
ref_filedir=str(ref_filedir.replace("'",""))

clean_filedir =input("Dir need to clean: ").strip()
clean_filedir=str(clean_filedir.replace("'",""))

print('Get infos from ref_filedir...')
ref_paths = util.Traversal(ref_filedir)
ref_infos = {}
ref_names = []
for path in ref_paths:
    ref_infos[GetFileMd5(path)] = path
    ref_names.append(os.path.split(path)[1])

print('Begin remove...')
clean_paths = util.Traversal(clean_filedir)
del_num = 0
for path in clean_paths:
    if GetFileMd5(path) in ref_infos or os.path.split(path)[1] in ref_names:
        print('Del: '+path)
        os.remove(path)
        del_num += 1
print('Finished! Del:',del_num)
