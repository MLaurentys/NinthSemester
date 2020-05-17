import os
import codecs
def generate_file(doc, initial_string, r_str):
    file = doc
    nusp = initial_string

    if os.path.exists(file): os.remove(file)

    os.mknod(file)
    f = open(file, 'a')
    f.write(nusp)
    f.close()
    f = open(file, 'ab')
    f.write(r_str)
    f.close()