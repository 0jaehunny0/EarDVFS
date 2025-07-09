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
littleFreqDict = {}

# for subdir, dirs, files in os.walk("selected/fluctuation2"):
for subdir, dirs, files in os.walk("selected/tempChange"):
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
            littleFreqDict[mykey] = []    
 


# for subdir, dirs, files in os.walk("selected/fluctuation2"):
for subdir, dirs, files in os.walk("selected/tempChange"):
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

            littleFreqDict[mykey].append(x["freq/little"])

            cstate = x["cstate/big"]
            cstate["value"] = cstate["value"] + x["cstate/mid"]["value"]
            cstate["value"] = cstate["value"] + x["cstate/little"]["value"]
            cstate["value"] = cstate["value"] + x["cstate/gpu"]["value"]

            cputemp = x["temp/gpu"]
            cputemp1 = x["temp/big"]
            cputemp2 = x["temp/mid"]
            cputemp3 = x["temp/little"]

            cputemp["value"] = (cputemp["value"] + cputemp1["value"] + cputemp2["value"] + cputemp3["value"]) / 4

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








########################

kkey = 'defaulttemp20'
deft = littleFreqDict[kkey][0]
np.where(deft["wall_time"] - deft["wall_time"][0] > 600)
deft["value"][:45].mean()

kkey = 'DVFStrain11temp20'
deft = littleFreqDict[kkey][0]
np.where(deft["wall_time"] - deft["wall_time"][0] > 600)
deft["value"][:86].mean()



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



fig, axes = plt.subplots(1, 1, figsize=(14.5, 4))




kkey = 'defaulttemp20'
deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(0), linestyle = "--")

kkey = 'zTT2target65'
deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(4), linestyle = "-.")

kkey = 'gearDVFStargetUtil0.0'
deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(8), linestyle = ":")


kkey = 'DVFStrain11temp20'
deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(12))



axes.set_xticks([0, 300, 600, 900, 1200, 1500, 1800])



axes.grid(axis='both',linestyle='--')  
axes.set_axisbelow(True)


axes.set_ylabel("Frame rates (fps)")
axes.set_xlabel("Time (s)")


axes.axvline(0, color='black', linewidth=2)
axes.axvline(600, color='black', linewidth=2)
axes.axvline(1200, color='black', linewidth=2)
axes.axvline(1800, color='black', linewidth=2)


axes.text(300, 40, "20 °C", ha='center', va='bottom')
axes.text(900, 40, "30 °C", ha='center', va='bottom')
axes.text(1500, 40, "10 °C", ha='center', va='bottom')

axes.annotate(
    '', 
    xy=(0.045, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.351, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes.annotate(
    '', 
    xy=(0.352, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.658, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes.annotate(
    '', 
    xy=(0.659, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.965, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

fig.legend(["Deft", "zTT", "Gear", "Ear"], loc='upper center', ncol=4, bbox_to_anchor=(0.5,1.03), borderpad=0.25, fontsize=22, columnspacing = 1.2, handlelength = 1.6)

# plt.tight_layout(pad = 0.05, rect = (0,0,1,0.92))
plt.tight_layout(pad = 0.05, rect = (0,0,1,0.88))

# plt.tight_layout(pad = 0.1)
plt.show()






#########################


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

# myfpsDict["DVFStrain11temp10"][0]["value"].mean()
# myfpsDict["DVFStrainAblation2temp10"][0]["value"].mean()


(1 - myfpsDict["DVFStrainAblation2temp20"][0]["value"].mean() / myfpsDict["DVFStrain11temp20"][0]["value"].mean()) * 100

(1 - mydict["DVFStrainAblation2temp20"][0]["value"].mean() / mydict["DVFStrain11temp20"][0]["value"].mean())*100


kkey = 'DVFStrain11temp10'
kkey = 'DVFStrain11temp20'


fig, axes = plt.subplots(1, 1, figsize=(13.5, 4))


deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(12))

kkey = 'DVFStrainAblation2temp10'
kkey = 'DVFStrainAblation2temp20'
deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(16), linestyle = "--")



axes.set_xticks([0, 300, 600, 900, 1200, 1500, 1800])



axes.grid(axis='both',linestyle='--')  
axes.set_axisbelow(True)


axes.set_ylabel("Frame rates (fps)")
axes.set_xlabel("Time (s)")

2.5
axes.axvline(0, color='black', linewidth=2)
axes.axvline(600, color='black', linewidth=2)
axes.axvline(1200, color='black', linewidth=2)
axes.axvline(1800, color='black', linewidth=2)


axes.text(300, 51, "20 °C", ha='center', va='bottom')
axes.text(900, 51, "30 °C", ha='center', va='bottom')
axes.text(1500, 51, "10 °C", ha='center', va='bottom')

axes.annotate(
    '', 
    xy=(0.045, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.351, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes.annotate(
    '', 
    xy=(0.352, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.658, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes.annotate(
    '', 
    xy=(0.659, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.965, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

fig.legend(["Ear", "Ablation2"], loc='lower right',  ncol = 2, bbox_to_anchor=(0.667,0.675), borderpad=0.3, fontsize=22, columnspacing = 1.2, handlelength = 1)
# plt.tight_layout(pad = 0.05, rect = (0,0,1,0.92))
plt.tight_layout(pad = 0.05, rect = (0,0,1,0.995))


# plt.tight_layout(pad = 0.1)
plt.show()





#########################




cmap = plt.get_cmap("tab20c")


cmap = plt.get_cmap("Set1")



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


kkey = 'defaulttemp10'

fig, axes = plt.subplots(2, 1, figsize=(12, 5.8))


deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %1 == 0:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-0:i+1]) / 1)
axes[0].plot(deft2, deft3, color = cmap(0))
axes[0].set_ylim(20, 44)
axes[0].set_yticks([20, 28, 36, 44])

ax2 = axes[0].twinx()

deft = tempDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %1 == 0:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-0:i+1]) / 1)
ax2.plot(deft2, deft3, color = cmap(1))
ax2.set_ylim(0, 36)
ax2.set_yticks([0, 12, 24, 36])



deft = batteryDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %1 == 0:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-0:i+1]) / 1)
axes[1].plot(deft2, deft3, color = cmap(3))
axes[1].set_ylim(20, 44)
axes[1].set_yticks([20, 28, 36, 44])


ax3 = axes[1].twinx()

deft = cpuDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %1 == 0:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-0:i+1]) / 1)
ax3.plot(deft2, deft3, color = cmap(6))
ax3.set_ylim(70, 85)
ax3.set_yticks([70, 75, 80, 85])




axes[0].set_xticks([0, 300, 600, 900, 1200, 1500, 1800])

axes[0].set_xticklabels([])
axes[1].set_xticks([0, 300, 600, 900, 1200, 1500, 1800])



axes[0].grid(axis='both',linestyle='--')  
axes[0].set_axisbelow(True)

axes[1].grid(axis='both',linestyle='--')  
axes[1].set_axisbelow(True)


axes[0].set_ylabel("Frame rates", color = cmap(0))
ax2.set_ylabel("Total cool. states", color = cmap(1))
axes[1].set_ylabel("Battery temp.", color = cmap(3))
ax3.set_ylabel("Avg. proc. temp.", color = cmap(6))


axes[0].tick_params(axis="y", labelcolor=cmap(0))
ax2.tick_params(axis="y", labelcolor=cmap(1))
axes[1].tick_params(axis="y", labelcolor=cmap(3))
ax3.tick_params(axis="y", labelcolor=cmap(6))


axes[1].set_xlabel("Time (s)")


axes[0].axvline(0, color='black', linewidth=2)
axes[0].axvline(600, color='black', linewidth=2)
axes[0].axvline(1200, color='black', linewidth=2)
axes[0].axvline(1800, color='black', linewidth=2)

axes[1].axvline(0, color='black', linewidth=2)
axes[1].axvline(600, color='black', linewidth=2)
axes[1].axvline(1200, color='black', linewidth=2)
axes[1].axvline(1800, color='black', linewidth=2)


axes[0].text(300, 45.5, "10 °C", ha='center', va='bottom')
axes[0].text(900, 45.5, "30 °C", ha='center', va='bottom')
axes[0].text(1500, 45.5, "10 °C", ha='center', va='bottom')

axes[0].annotate(
    '', 
    xy=(0.045, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.351, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes[0].annotate(
    '', 
    xy=(0.352, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.658, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes[0].annotate(
    '', 
    xy=(0.659, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.965, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

# fig.legend(["1st", "2nd", "3rd"], loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.047),frameon=False, borderpad=0.1, fontsize=22, columnspacing = 1.2)
# plt.tight_layout(pad = 0.05, rect = (0,0,1,0.92))
plt.tight_layout(pad = 0.05, rect = (0,0,1,0.99))

# plt.tight_layout(pad = 0.1)
plt.show()



########################


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

myfpsDict["DVFStrain11temp10"][0]["value"].mean()
myfpsDict["DVFStrainAblation2temp10"][0]["value"].mean()


1 - myfpsDict["DVFStrainAblation2temp10"][0]["value"].mean() / myfpsDict["DVFStrain11temp10"][0]["value"].mean()

1 - mydict["DVFStrainAblation2temp10"][0]["value"].mean() / mydict["DVFStrain11temp10"][0]["value"].mean()



kkey = 'DVFStrain11temp10'
kkey = 'DVFStrain11temp20'


fig, axes = plt.subplots(1, 1, figsize=(12, 3.3))


deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(12))

kkey = 'DVFStrainAblation2temp10'
kkey = 'DVFStrainAblation2temp20'
deft = myfpsDict[kkey][0]
deft2 = []
deft3 = []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
axes.plot(deft2, deft3, color = cmap(16), linestyle = "--")



axes.set_xticks([0, 300, 600, 900, 1200, 1500, 1800])



axes.grid(axis='both',linestyle='--')  
axes.set_axisbelow(True)


axes.set_ylabel("Frame rates (fps)")
axes.set_xlabel("Time (s)")


axes.axvline(0, color='black', linewidth=2)
axes.axvline(600, color='black', linewidth=2)
axes.axvline(1200, color='black', linewidth=2)
axes.axvline(1800, color='black', linewidth=2)


axes.text(300, 52.5, "10 °C", ha='center', va='bottom')
axes.text(900, 52.5, "30 °C", ha='center', va='bottom')
axes.text(1500, 52.5, "10 °C", ha='center', va='bottom')

axes.annotate(
    '', 
    xy=(0.045, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.351, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes.annotate(
    '', 
    xy=(0.352, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.658, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

axes.annotate(
    '', 
    xy=(0.659, 1.05),    # 화살표의 끝점 (axes 상대 좌표)
    xytext=(0.965, 1.05),  # 화살표의 시작점 (axes 상대 좌표)
    arrowprops=dict(arrowstyle='<->', linewidth=2, color='black'),
    xycoords='axes fraction', 
    textcoords='axes fraction'
)

fig.legend(["Ear", "Ablation"], loc='lower right',  bbox_to_anchor=(0.97,0.2), borderpad=0.3, fontsize=22, columnspacing = 1.2, handlelength = 1)
# plt.tight_layout(pad = 0.05, rect = (0,0,1,0.92))
plt.tight_layout(pad = 0.1, rect = (0,0,1,0.99))

# plt.tight_layout(pad = 0.1)
plt.show()


