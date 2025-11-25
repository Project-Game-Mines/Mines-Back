import os
import shutil

'''
limpar os pycaches do projeto
'''

for root, dirs, files in os.walk(".", topdown=False):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
            print(f"Removed: {os.path.join(root, d)}")
