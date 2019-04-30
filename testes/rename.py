import os
import sys

print(sys.argv[0])

os.chdir(sys.argv[1])

arquivos = os.listdir()

for i in arquivos:

	os.rename(i, i[17:])

print(os.listdir())
