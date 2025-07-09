from tensorboard.backend.event_processing import event_accumulator
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# import PyQt5
# import matplotlib
# matplotlib.use('Qt5Agg')

def parse_tensorboard(path, scalars):
    """returns a dictionary of pandas dataframes for each requested scalar"""
    ea = event_accumulator.EventAccumulator(
        path,
        size_guidance={event_accumulator.SCALARS: 0},
    )
    _absorb_print = ea.Reload()
    # make sure the scalars are in the event accumulator tags
    assert all(
        s in ea.Tags()["scalars"] for s in scalars
    ), "some scalars were not found in the event accumulator"
    return {k: pd.DataFrame(ea.Scalars(k)) for k in scalars}




scalars = [
    "perf/fps",
    "perf/ppw",
    "perf/power",
    "cstate/big",
    "cstate/mid",
    "cstate/little",
    "cstate/gpu",
    "temp/battery",
    "temp/big",
    "temp/mid",
    "temp/little",
    "temp/gpu",
    "freq/big",
    "freq/mid",
    "freq/little",
    "freq/gpu",
    "util/gu",
]

mydict = {}
ppwDict = {}
myfpsDict = {}
tempDict = {}
batteryDict = {}
powerDict = {}
cpuDict = {}
cpuDict1 = {}
cpuDict2 = {}
cpuDict3 = {}

bigD = {}
midD = {}
litD = {}
gpuD = {}
utilD = {}

# for subdir, dirs, files in os.walk("selected/fluctuation2"):
for subdir, dirs, files in os.walk("selected/iccadCmp"):
    a = subdir.split("/")


    if len(a) > 2:
        if len(a) > 2:
            if "def" in a[2].split("_")[2]:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]
            else:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]

        if mykey not in mydict:
            mydict[mykey] = []
            ppwDict[mykey] = []
            myfpsDict[mykey] = []
            tempDict[mykey] = []    
            batteryDict[mykey] = []    
            powerDict[mykey] = []    
            cpuDict[mykey] = []   
            cpuDict1[mykey] = []   
            cpuDict2[mykey] = []   
            cpuDict3[mykey] = []   
                        
            bigD[mykey] = []    
            midD[mykey] = []    
            litD[mykey] = []    
            gpuD[mykey] = []    
            utilD[mykey] = []    
 


# for subdir, dirs, files in os.walk("selected/fluctuation2"):
for subdir, dirs, files in os.walk("selected/iccadCmp"):
    # print(subdir)
    for file in files:

        a = subdir.split("/")
        if len(a) > 2:
            if "def" in a[2].split("_")[2]:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]
            else:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]

        filepath = subdir + os.sep + file
        if "events" in filepath:
            x = parse_tensorboard(filepath, scalars)
            print(subdir, x["perf/ppw"][-50:]["value"].mean())
            # print(subdir, x["perf/fps"][-10:]["value"].mean())

            mydict[mykey].append(x["perf/ppw"])
            
            myfpsDict[mykey].append(x["perf/fps"])

            batteryDict[mykey].append(x["temp/battery"])
            
            powerDict[mykey].append(x["perf/power"])

            cstate = x["cstate/big"]
            cstate["value"] = cstate["value"] + x["cstate/mid"]["value"]
            cstate["value"] = cstate["value"] + x["cstate/little"]["value"]
            cstate["value"] = cstate["value"] + x["cstate/gpu"]["value"]

            cputemp = x["temp/gpu"]
            cputemp1 = x["temp/big"]
            cputemp2 = x["temp/mid"]
            cputemp3 = x["temp/little"]
            # cputemp["value"] = cputemp["value"] + x["temp/mid"]["value"]
            # cputemp["value"] = cputemp["value"] + x["temp/little"]["value"] + x["temp/gpu"]["value"]

            cpuDict[mykey].append(cputemp)
            cpuDict1[mykey].append(cputemp1)
            cpuDict2[mykey].append(cputemp2)
            cpuDict3[mykey].append(cputemp3)

            tempDict[mykey].append(cstate)

            bigD[mykey].append(x["freq/big"])
            midD[mykey].append(x["freq/mid"])
            litD[mykey].append(x["freq/little"])
            gpuD[mykey].append(x["freq/gpu"])
            utilD[mykey].append(x["util/gu"])


mydict.keys()








cmap = plt.get_cmap("tab20c")





import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib import font_manager
font_path = '/usr/share/fonts/truetype/msttcorefonts/arial.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()
matplotlib.rcParams.update({'font.size': 22})


fig, axes = plt.subplots(2, 1, figsize=(4.8, 3.3))


deft = myfpsDict['defaulttemp20'][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[0].plot(deft2, deft3, color = "C0")


deft = myfpsDict['defaulttemp20'][1]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[0].plot(deft2, deft3, color = "C8", linestyle = "--")

deft = myfpsDict['defaulttemp20'][2]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[0].plot(deft2, deft3, color = "C9", linestyle = "-.")

axes[0].set_xlabel("Frame rates (fps)")
axes[0].set_xticks([])
axes[0].set_yticks([30, 35, 40])



deft = tempDict['defaulttemp20'][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[1].plot(deft2, deft3, color = "C0")


deft = tempDict['defaulttemp20'][1]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[1].plot(deft2, deft3, color = "C8", linestyle = "--")

deft = tempDict['defaulttemp20'][2]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[1].plot(deft2, deft3, color = "C9", linestyle = "-.")


axes[1].set_xlabel("Total cooling states")
axes[1].set_xticks([])
axes[1].set_yticks([0, 10, 20])

axes[0].grid(axis='y',linestyle='--')  
axes[0].set_axisbelow(True)

axes[1].grid(axis='y',linestyle='--')  
axes[1].set_axisbelow(True)



fig.legend(["1st", "2nd", "3rd"], loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.047),frameon=False, borderpad=0.1, fontsize=22, columnspacing = 1.2)
plt.tight_layout(pad = 0.05, rect = (0,0,1,0.92))

plt.subplots_adjust(wspace=0.15)

plt.show()






mydict = {}
ppwDict = {}
myfpsDict = {}
tempDict = {}
batteryDict = {}
powerDict = {}
cpuDict = {}
cpuDict1 = {}
cpuDict2 = {}
cpuDict3 = {}

bigD = {}
midD = {}
litD = {}
gpuD = {}
utilD = {}

# for subdir, dirs, files in os.walk("selected/fluctuation2"):
for subdir, dirs, files in os.walk("selected/iccadCmp2"):
    a = subdir.split("/")


    if len(a) > 2:
        if len(a) > 2:
            if "def" in a[2].split("_")[2]:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]
            else:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]

        if mykey not in mydict:
            mydict[mykey] = []
            ppwDict[mykey] = []
            myfpsDict[mykey] = []
            tempDict[mykey] = []    
            batteryDict[mykey] = []    
            powerDict[mykey] = []    
            cpuDict[mykey] = []   
            cpuDict1[mykey] = []   
            cpuDict2[mykey] = []   
            cpuDict3[mykey] = []   
                        
            bigD[mykey] = []    
            midD[mykey] = []    
            litD[mykey] = []    
            gpuD[mykey] = []    
            utilD[mykey] = []    
 


# for subdir, dirs, files in os.walk("selected/fluctuation2"):
for subdir, dirs, files in os.walk("selected/iccadCmp2"):
    # print(subdir)
    for file in files:

        a = subdir.split("/")
        if len(a) > 2:
            if "def" in a[2].split("_")[2]:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]
            else:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]

        filepath = subdir + os.sep + file
        if "events" in filepath:
            x = parse_tensorboard(filepath, scalars)
            print(subdir, x["perf/ppw"][-50:]["value"].mean())
            # print(subdir, x["perf/fps"][-10:]["value"].mean())

            mydict[mykey].append(x["perf/ppw"])
            
            myfpsDict[mykey].append(x["perf/fps"])

            batteryDict[mykey].append(x["temp/battery"])
            
            powerDict[mykey].append(x["perf/power"])

            cstate = x["cstate/big"]
            cstate["value"] = cstate["value"] + x["cstate/mid"]["value"]
            cstate["value"] = cstate["value"] + x["cstate/little"]["value"]
            cstate["value"] = cstate["value"] + x["cstate/gpu"]["value"]

            cputemp = x["temp/gpu"]
            cputemp1 = x["temp/big"]
            cputemp2 = x["temp/mid"]
            cputemp3 = x["temp/little"]
            # cputemp["value"] = cputemp["value"] + x["temp/mid"]["value"]
            # cputemp["value"] = cputemp["value"] + x["temp/little"]["value"] + x["temp/gpu"]["value"]

            cpuDict[mykey].append(cputemp)
            cpuDict1[mykey].append(cputemp1)
            cpuDict2[mykey].append(cputemp2)
            cpuDict3[mykey].append(cputemp3)

            tempDict[mykey].append(cstate)

            bigD[mykey].append(x["freq/big"])
            midD[mykey].append(x["freq/mid"])
            litD[mykey].append(x["freq/little"])
            gpuD[mykey].append(x["freq/gpu"])
            utilD[mykey].append(x["util/gu"])


mydict.keys()








cmap = plt.get_cmap("tab20c")





import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib import font_manager
font_path = '/usr/share/fonts/truetype/msttcorefonts/arial.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()
matplotlib.rcParams.update({'font.size': 22})


fig, axes = plt.subplots(2, 1, figsize=(4.8, 3.3))


deft = myfpsDict['defaulttemp20'][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[0].plot(deft2, deft3, color = "C0")


deft = myfpsDict['defaulttemp20'][1]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[0].plot(deft2, deft3, color = "C8", linestyle = "--")

deft = myfpsDict['defaulttemp20'][2]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[0].plot(deft2, deft3, color = "C9", linestyle = "-.")

axes[0].set_xlabel("Frame rates (fps)")
axes[0].set_xticks([])
axes[0].set_yticks([36, 38, 40])



deft = tempDict['defaulttemp20'][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[1].plot(deft2, deft3, color = "C0")


deft = tempDict['defaulttemp20'][1]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[1].plot(deft2, deft3, color = "C8", linestyle = "--")

deft = tempDict['defaulttemp20'][2]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes[1].plot(deft2, deft3, color = "C9", linestyle = "-.")


axes[1].set_xlabel("Total cooling states")
axes[1].set_xticks([])
axes[1].set_yticks([0, 10, 20])

axes[0].grid(axis='y',linestyle='--')  
axes[0].set_axisbelow(True)

axes[1].grid(axis='y',linestyle='--')  
axes[1].set_axisbelow(True)



fig.legend(["1st", "2nd", "3rd"], loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.047),frameon=False, borderpad=0.1, fontsize=22, columnspacing = 1.2)
plt.tight_layout(pad = 0.05, rect = (0,0,1,0.92))

plt.subplots_adjust(wspace=0.15)

plt.show()






