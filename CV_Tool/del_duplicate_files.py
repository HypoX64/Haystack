'''
Delete duplicate files bt MD5
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
for path in ref_paths:
    ref_infos[GetFileMd5(path)] = path

print('Begin remove...')
clean_paths = util.Traversal(clean_filedir)
del_num = 0
for path in clean_paths:
    if GetFileMd5(path) in ref_infos:
        print('Del: '+path)
        os.remove(path)
        del_num += 1
print('Finished! Del:',del_num)
