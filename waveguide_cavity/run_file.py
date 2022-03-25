import os

os.system('conda run -n mp python cavity.py')
os.system('conda deactivate')
os.system('h5topng cavity-eps-000000.00.h5')
os.system('h5topng -Zc dkbluered cavity')

