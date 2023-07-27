# converts entrties pasted from https://keisan.casio.com/exec/system/1329114617 on stdin to a (non-formatted) python file on stdout
# stop with Ctrl+D

import sys

print("[")
print("{")
for line in sys.stdin:
    line = line.strip()
    if line == "":
        print("\n},{")
        continue
    print(line.replace("\t", ":"), end=",")
print("}")
print("]")
