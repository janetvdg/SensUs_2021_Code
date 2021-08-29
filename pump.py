"""
ALL.py
~~~~~~~~~~~~~~~~~
This program shows how to connect to to the LSPone (laboratory syringe pump) using python and do the General cleaning procedure.
It should be done at the beginning and end of the day.
:author: SenSwiss 2021

Cleaning procedure: 
Do the steps 2x using 1% chlorine bleach and deionized water
Do the steps 2x using detergent
Do the steps 1x using 70% ethanol
Do the steps 2x using PBS
Do the steps 2x with air
"""

# include python libraries
import sys
import serial
import time



stop_pandp = False

#%% Functions
def initialise_LSPone(lsp):
    #Initialise LSPone
    lsp.write(b"/1Z3R\r")
    time.sleep(20)
    print("LSP one ready")

def general_cleaning_procedure(lsp):
    # 2: PBS, 3: Air, 4: Ethanol
    lsp.write(b"/1V200M200B2M1000A1500M1000B6M1000A0M1000B3M1000A1500M1000B6M1000A0M1000B4M1000A1500M1000B6M1000A0M1000B3M1000A3000M1000B6M1000A0M1000B3M1000A3000M1000B6M1000A0M1000R\r")


def pick_BB(lsp):
    lsp.write(b"/1V5M200B6M1000A480M1000V300M200B3M1000A510M1000B6M1000V5M200R\r")
    time.sleep(105)
    beep.beep(8)

def push_pull_sample(lsp, n_times):
    if n_times == 1:
        lsp.write(b"/1V5M1000A660M1000A510M1000R\r")
    elif n_times == 2:
        lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000R\r")
    elif n_times == 3:
        lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000R\r")
    elif n_times == 4:
        lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000R\r")


#%% Open serial connection -> check COM port on your device
lsp = serial.Serial('COM5', 9600, timeout=1000)
print('LSPone connected on ',lsp.name)
#%% Initialise LSPone normally already done
initialise_LSPone(lsp)

#%% 0. General Cleaning # this were i start
# 2: PBS, 3: Air, 4: Ethanol
lsp.write(b"/1V200M200B2M1000A1500M1000B6M1000A0M1000B3M1000A1500M1000B6M1000A0M1000B4M1000A1500M1000B6M1000A0M1000B3M1000A3000M1000B6M1000A0M1000B3M1000A3000M1000B6M1000A0M1000R\r")

#%% 1. Sippin part 1 (26/08)
# Sucking BB at 50 ul/min
pick_BB(lsp)

#%% 2. Sippin part 2
# 2x Push and pull at 50 ul/min
lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000R\r")
time.sleep(138)
beep.beep(8)

#%% 3x Push and pull at 50 ul/min
lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000R\r")
time.sleep(207)
beep.beep(8)

#%% 4x Push and pull at 50 ul/min
lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000R\r")
time.sleep(276)
beep.beep(8)

#%% 3. Push & pull (10 times)
lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000R\r")
# Print time in minutes after instruction is sent
for i in range(1, 11):
        time.sleep(69)
        print(i)
beep.beep(8)
#%% 3. Push & pull (20 times)
lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000R\r")
# Print time in minutes after instruction is sent
for i in range(1, 21):
        time.sleep(60)
        print(i)
#%% Empty syringe in trash
#to make sure te syrine is fully pused out
lsp.write(b"/1V150B1M1000A0M1000R\r")

#%% Push & pull (2 times)
n = 2
push_pull_sample_n_times(lsp, n)
stop_pandp = False
#Each push and pull takes exactly 70s

#%% Push & pull (3 times)
n = 3
push_pull_sample_n_times(lsp, n)
stop_pandp = False
#Each push and pull takes exactly 70s

#%% Push & pull (4 times)
n = 4
push_pull_sample_n_times(lsp, n)
stop_pandp = False
#Each push and pull takes exactly 70s

#%% Push & pull (8 times)
lsp.write(b"/1V5M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000A660M1000A510M1000R\r")
# Print time in minutes after instruction is sent
for i in range(1, 9):
        time.sleep(60)
        print(i)
#%% Air Cleanin
lsp.write(b"/1V300B3M1000A1000M1000B6M1000A0M1000R\r")

#%% IN CASE BB IS NOT MOVING
# Start picking BB again at 100 ul/min 
#Empty syringe 
lsp.write(b"/1V150B1M1000A0M1000R\r")
# Pick at 100 ul/min
lsp.write(b"/1V5M200B6M1000A240M1000R\r")

#%% Sucking 80 ul BB at 100 ul/min 
lsp.write(b"/1V10M200B6M1000A480M1000R\r")
#%%  Put in position A480 to do sample 
lsp.write(b"/1V100M200B3M1000A480M1000R\r")

#%% 2. Sippin part 2
# 1x Push and pull at 200 ul/min
lsp.write(b"/1V20M1000A660M1000A510M1000R\r")
print(0)


#%%
#Finishing the script 
sys.exit(0)

#%% 
def willy():
    beep.beep(7)

    threading.Thread(target=willy).start()
    time.sleep(0.1)
    
        
threading.Thread(target=willy).start()
