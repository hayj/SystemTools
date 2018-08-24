

# print("aaaaaaaaaa bbbbbbbbbb")

# # print(chr(27) + "[2J")

import os
import sys
from enum import Enum
import signal


print(getOutputType())
exit()



# import os
# os.system('cls' if os.name == 'nt' else 'clear')

size = os.get_terminal_size()

print(size[0])


if signal.getsignal(signal.SIGHUP) == signal.SIG_DFL:  # default action
    print("No SIGHUP handler")
else:
    print("In nohup mode")


import time
for x in range (0,5):  
    b = "Loading" + "." * x
    print (b, end="\r")
    time.sleep(1)



import sys
print("FAILED...")
sys.stdout.write("\033[F") #back to previous line
time.sleep(1)
sys.stdout.write("\033[K") #clear line
print("SUCCESS!")