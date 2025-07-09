from tensorboard.backend.event_processing import event_accumulator
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# import PyQt5
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
    "temp/gpu",
    "temp/big",
    "temp/mid",
    "temp/little",
    "temp/battery",
    "cstate/big",
    "cstate/mid",
    "cstate/little",
    "cstate/gpu",
    "freq/big",
    "freq/mid",
    "freq/gpu",
    "freq/little",
]

expLi = ["iccadAblation"]

valuesLi1 = []
valuesLi2 = []
valuesLi3 = []
valuesLi4 = []

for exp in expLi:

    mydict = {}
    ppwDict = {}
    myfpsDict = {}
    tempDict = {}
    powerDict = {}
    tempDict2 = {}
    tempDict3 = {}

    freqDict1 = {}
    freqDict2 = {}
    freqDict3 = {}
    freqDict4 = {}


    for subdir, dirs, files in os.walk("selected/"+exp):
        a = subdir.split("/")


        if len(a) > 2:
            if len(a) > 2:
                if "def" in a[2].split("_")[2]:
                    mykey = a[2].split("_")[2][-9:] + a[2].split("_")[4]
                else:
                    mykey = a[2].split("_")[2][-9:] + a[2].split("_")[6]

            if mykey not in mydict:
                mydict[mykey] = []
                ppwDict[mykey] = []
                myfpsDict[mykey] = []
                tempDict[mykey] = []    
                powerDict[mykey] = []    
                tempDict2[mykey] = []    
                tempDict3[mykey] = []  
                
                
                freqDict1[mykey] = []  
                freqDict2[mykey] = []  
                freqDict3[mykey] = []  
                freqDict4[mykey] = []  




    for subdir, dirs, files in os.walk("selected/"+exp):
        # print(subdir)
        for file in files:

            a = subdir.split("/")
            if len(a) > 2:
                if "def" in a[2].split("_")[2]:
                    mykey = a[2].split("_")[2][-9:] + a[2].split("_")[4]
                else:
                    mykey = a[2].split("_")[2][-9:] + a[2].split("_")[6]

            filepath = subdir + os.sep + file
            if "events" in filepath:
                x = parse_tensorboard(filepath, scalars)
                print(subdir, x["perf/ppw"][-50:]["value"].mean())
                # print(subdir, x["perf/fps"][-10:]["value"].mean())

                mydict[mykey].append(x["perf/ppw"])
                powerDict[mykey].append(x["perf/power"])
                myfpsDict[mykey].append(x["perf/fps"])
                tempDict[mykey].append(x["temp/gpu"])
                
                
                freqDict1[mykey].append(x["freq/big"])
                freqDict2[mykey].append(x["freq/mid"])
                freqDict3[mykey].append(x["freq/little"])
                freqDict4[mykey].append(x["freq/gpu"])

                

                processtemp = x["temp/big"]
                processtemp["value"] += x["temp/mid"]["value"] + x["temp/little"]["value"] + x["temp/gpu"]["value"]
                processtemp["value"] /= 4
                tempDict2[mykey].append(processtemp)
            
                cstate = x["cstate/big"]
                cstate["value"] += x["cstate/mid"]["value"] + x["cstate/little"]["value"] + x["cstate/gpu"]["value"]
                tempDict3[mykey].append(cstate)

            # mydict[mykey] = 

    values1 = [
        [myfpsDict["FStrain1120.0"][0]["value"].mean(), myfpsDict["FStrain1130.0"][0]["value"].mean(), myfpsDict["FStrain1140.0"][0]["value"].mean()],  # Group 1
        [myfpsDict["Ablation220.0"][0]["value"].mean(), myfpsDict["Ablation230.0"][0]["value"].mean(), myfpsDict["Ablation240.0"][0]["value"].mean()],  # Group 1
        [myfpsDict["Ablation320.0"][0]["value"].mean(), myfpsDict["Ablation330.0"][0]["value"].mean(), myfpsDict["Ablation340.0"][0]["value"].mean()],  # Group 1
        [myfpsDict["blation4320.0"][0]["value"].mean(), myfpsDict["blation4330.0"][0]["value"].mean(), myfpsDict["blation4340.0"][0]["value"].mean()],  # Group 1
    ]
    values2 = [
        [mydict["FStrain1120.0"][0]["value"].mean(), mydict["FStrain1130.0"][0]["value"].mean(), mydict["FStrain1140.0"][0]["value"].mean()],  # Group 1
        [mydict["Ablation220.0"][0]["value"].mean(), mydict["Ablation230.0"][0]["value"].mean(), mydict["Ablation240.0"][0]["value"].mean()],  # Group 1
        [mydict["Ablation320.0"][0]["value"].mean(), mydict["Ablation330.0"][0]["value"].mean(), mydict["Ablation340.0"][0]["value"].mean()],  # Group 1
        [mydict["blation4320.0"][0]["value"].mean(), mydict["blation4330.0"][0]["value"].mean(), mydict["blation4340.0"][0]["value"].mean()],  # Group 1
    ]
    values3 = [
        [tempDict2["FStrain1120.0"][0]["value"].mean(), tempDict2["FStrain1130.0"][0]["value"].mean(), tempDict2["FStrain1140.0"][0]["value"].mean()],  # Group 1
        [tempDict2["Ablation220.0"][0]["value"].mean(), tempDict2["Ablation230.0"][0]["value"].mean(), tempDict2["Ablation240.0"][0]["value"].mean()],  # Group 1
        [tempDict2["Ablation320.0"][0]["value"].mean(), tempDict2["Ablation330.0"][0]["value"].mean(), tempDict2["Ablation340.0"][0]["value"].mean()],  # Group 1
        [tempDict2["blation4320.0"][0]["value"].mean(), tempDict2["blation4330.0"][0]["value"].mean(), tempDict2["blation4340.0"][0]["value"].mean()],  # Group 1
    ]
    values4 = [
        [tempDict3["FStrain1120.0"][0]["value"].mean(), tempDict3["FStrain1130.0"][0]["value"].mean(), tempDict3["FStrain1140.0"][0]["value"].mean()],  # Group 1
        [tempDict3["Ablation220.0"][0]["value"].mean(), tempDict3["Ablation230.0"][0]["value"].mean(), tempDict3["Ablation240.0"][0]["value"].mean()],  # Group 1
        [tempDict3["Ablation320.0"][0]["value"].mean(), tempDict3["Ablation330.0"][0]["value"].mean(), tempDict3["Ablation340.0"][0]["value"].mean()],  # Group 1
        [tempDict3["blation4320.0"][0]["value"].mean(), tempDict3["blation4330.0"][0]["value"].mean(), tempDict3["blation4340.0"][0]["value"].mean()],  # Group 1
    ]

    values1 = np.array(values1)
    values2 = np.array(values2)
    values3 = np.array(values3)
    values4 = np.array(values4)

    # v1 = np.array([myfpsDict["FStrain1120.0"][0]["value"].mean(), myfpsDict["FStrain1130.0"][0]["value"].mean(), myfpsDict["FStrain1140.0"][0]["value"].mean()])
    # v2 = np.array([mydict["FStrain1120.0"][0]["value"].mean(), mydict["FStrain1130.0"][0]["value"].mean(), mydict["FStrain1140.0"][0]["value"].mean()])
    # v3 = np.array([tempDict2["FStrain1120.0"][0].mean(), tempDict2["FStrain1130.0"][0].mean(), tempDict2["FStrain1140.0"][0].mean()])
    # v4 = np.array([tempDict3["FStrain1120.0"][0].mean(), tempDict3["FStrain1130.0"][0].mean(), tempDict3["FStrain1140.0"][0].mean()])

    # values1 = 100 * (values1 / v1) - 100
    # values2 = 100 * (values2 / v2) - 100
    # values3 = 100 * (values3 / v3) - 100
    # # values4 = 100 * (values4 / v4) - 100

    # values4 = (values4 - v4)

    values1 = np.array(values1).T
    values2 = np.array(values2).T
    values3 = np.array(values3).T
    values4 = np.array(values4).T

    valuesLi1.append(values1)
    valuesLi2.append(values2)
    valuesLi3.append(values3)
    valuesLi4.append(values4)

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



cmap = plt.get_cmap("tab20c")
fig, axes = plt.subplots(2, 4, figsize=(14.5, 3.5))


index1 = 'FStrain1130.0'
index2 = 'blation4330.0'
index2 = 'Ablation330.0'

(1 - myfpsDict[index2][0]["value"].mean()/myfpsDict[index1][0]["value"].mean()) *100
(1 - mydict[index2][0]["value"].mean()/mydict[index1][0]["value"].mean()) *100
(1 - tempDict2[index2][0]["value"].mean()/tempDict2[index1][0]["value"].mean()) *100

deft = myfpsDict[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][0].plot(deft2, deft3, color = cmap(12))


deft = myfpsDict[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][0].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[0][0].set_xticks([])
axes[0][0].set_xlabel("Frame rates (fps)")

deft = mydict[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4 * 1000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][0].plot(deft2, deft3, color = cmap(12))

deft = mydict[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4 * 1000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][0].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][0].set_xticks([])
axes[1][0].set_xlabel("Power efficiency (PPW)")


deft = freqDict1[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][1].plot(deft2, deft3, color = cmap(12))

deft = freqDict1[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][1].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[0][1].set_xticks([])
axes[0][1].set_xlabel("Big freq. (Ghz)")

deft = freqDict2[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][1].plot(deft2, deft3, color = cmap(12))

deft = freqDict2[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][1].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][1].set_xticks([])
axes[1][1].set_xlabel("Mid freq. (Ghz)")




deft = freqDict3[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][2].plot(deft2, deft3, color = cmap(12))

deft = freqDict3[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4 / 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][2].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[0][2].set_xticks([])
axes[0][2].set_xlabel("Little freq. (Ghz)")

deft = freqDict4[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][2].plot(deft2, deft3, color = cmap(12))

deft = freqDict4[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][2].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][2].set_xticks([])
axes[1][2].set_xlabel("GPU freq. (Ghz)")


deft = tempDict2[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][3].plot(deft2, deft3, color = cmap(12))

deft = tempDict2[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][3].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][3].set_xticks([])
axes[1][3].set_xlabel("Avg. proc. temp (°C)")



axes[0][0].set_axisbelow(True)

axes[0][0].grid(axis='y',linestyle='--')  
axes[0][0].set_axisbelow(True)

axes[0][1].grid(axis='y',linestyle='--')  
axes[0][1].set_axisbelow(True)

axes[0][2].grid(axis='y',linestyle='--')  
axes[0][2].set_axisbelow(True)


axes[1][0].grid(axis='y',linestyle='--')  
axes[1][0].set_axisbelow(True)


axes[1][1].grid(axis='y',linestyle='--')  
axes[1][1].set_axisbelow(True)


axes[1][2].grid(axis='y',linestyle='--')  
axes[1][2].set_axisbelow(True)


axes[1][3].grid(axis='y',linestyle='--')  
axes[1][3].set_axisbelow(True)


axes[0][3].axis('off') 


fig.legend(["Ear", "Ablation1"], loc='upper right', ncol=1, bbox_to_anchor=(0.96, 0.975),frameon=True, fontsize=22, labelspacing=0.4)
plt.tight_layout(pad = 0.1, rect = (0,0,1,1))

plt.show()









###########################
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


cmap = plt.get_cmap("tab20c")

fig, ax = plt.subplots(1, 4, figsize=(14.5, 4), sharey=False)

labelLi = ["Ear", "Ablation2"]
# Number of groups per category
num_groups = 2
bar_width = 0.20  # Width of individual bars
categories = ['10°C', '20°C', '30°C']  # X-axis labels
x_positions = np.arange(len(categories))  # Position for each category

for i in range(num_groups):
    ax[0].bar(x_positions + i * bar_width, [row[i]*1000 for row in valuesLi2[0]], 
            width=bar_width, label=labelLi[i], color = cmap(12 + i*4), alpha = 0.95)
ax[0].set_xticks(x_positions + bar_width)
ax[0].set_xticklabels(categories) 
ax[0].set_xlabel("Power efficiency (PPW)")
ax[0].grid(axis='y',linestyle='--')  # Add grid to the second subplot
ax[0].set_axisbelow(True)



for i in range(num_groups):
    ax[1].bar(x_positions + i * bar_width, [row[i] for row in valuesLi1[0]], 
            width=bar_width, label=labelLi[i], color = cmap(12 + i*4), alpha = 0.95)
ax[1].set_xticks(x_positions + bar_width)
ax[1].set_xticklabels(categories) 
ax[1].set_xlabel("Frame rates (fps)")
# ax[1].legend(loc = "upper right", borderpad = 0.3, labelspacing=0.2, borderaxespad=0.3, handletextpad=0.4, handlelength=0.5)
ax[1].grid(axis='y',linestyle='--')  # Add grid to the second subplot
ax[1].set_axisbelow(True)


for i in range(num_groups):
    ax[2].bar(x_positions + i * bar_width, [row[i] for row in valuesLi3[0]], 
            width=bar_width, label=labelLi[i], color = cmap(12 + i*4), alpha = 0.95)
ax[2].set_xticks(x_positions + bar_width)
ax[2].set_xticklabels(categories) 
ax[2].set_xlabel("Avg. processor temp. (°C)")
# ax[2].legend(loc = "upper right", borderpad = 0.3, labelspacing=0.2, borderaxespad=0.3, handletextpad=0.4, handlelength=0.5)
ax[2].grid(axis='y',linestyle='--')  # Add grid to the second subplot
ax[2].set_axisbelow(True)


for i in range(num_groups):
    ax[3].bar(x_positions + i * bar_width, [row[i] for row in valuesLi4[0]], 
            width=bar_width, label=labelLi[i], color = cmap(12 + i*4), alpha = 0.95)
ax[3].set_xticks(x_positions + bar_width)
ax[3].set_xticklabels(categories) 
ax[3].set_xlabel("Total cool. states (#)")
# ax[3].legend(loc = "upper right", borderpad = 0.3, labelspacing=0.2, borderaxespad=0.3, handletextpad=0.4, handlelength=0.5)
ax[3].grid(axis='y',linestyle='--')  # Add grid to the second subplot
ax[3].set_axisbelow(True)
ax[3].xaxis.set_label_coords(0.45, -0.142)
ax[3].legend(loc = "upper left", borderpad = 0.25, labelspacing=0.2, borderaxespad=0.25, handletextpad=0.4, handlelength=0.5)


plt.tight_layout(pad=0.1)
plt.show()





###########################





###########################

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



cmap = plt.get_cmap("tab20c")
fig, axes = plt.subplots(2, 4, figsize=(14.5, 3.5))


index1 = 'FStrain1130.0'
index2 = 'blation4330.0'




deft = myfpsDict[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][0].plot(deft2, deft3, color = cmap(12))


deft = myfpsDict[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][0].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[0][0].set_xticks([])
axes[0][0].set_xlabel("Frame rates (fps)")

deft = mydict[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4 * 1000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][0].plot(deft2, deft3, color = cmap(12))

deft = mydict[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4 * 1000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][0].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][0].set_xticks([])
axes[1][0].set_xlabel("Power efficiency (PPW)")


deft = freqDict1[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][1].plot(deft2, deft3, color = cmap(12))

deft = freqDict1[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][1].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[0][1].set_xticks([])
axes[0][1].set_xlabel("Big freq. (Ghz)")

deft = freqDict2[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][1].plot(deft2, deft3, color = cmap(12))

deft = freqDict2[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][1].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][1].set_xticks([])
axes[1][1].set_xlabel("Mid freq. (Ghz)")




deft = freqDict3[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][2].plot(deft2, deft3, color = cmap(12))

deft = freqDict3[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4 / 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[0][2].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[0][2].set_xticks([])
axes[0][2].set_xlabel("Little freq. (Ghz)")

deft = freqDict4[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][2].plot(deft2, deft3, color = cmap(12))

deft = freqDict4[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4/ 1000000)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][2].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][2].set_xticks([])
axes[1][2].set_xlabel("GPU freq. (Ghz)")


deft = tempDict2[index1][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][3].plot(deft2, deft3, color = cmap(12))

deft = tempDict2[index2][0]
xx = deft2
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %4 == 3:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-3:i+1]) / 4)
first = np.where(np.array(deft2) > 1200)[0][0]
deft2 = deft2[first:]
deft3 = deft3[first:]
axes[1][3].plot(deft2, deft3, color = cmap(16), linestyle="--")
axes[1][3].set_xticks([])
axes[1][3].set_xlabel("Avg. proc. temp (°C)")



axes[0][0].set_axisbelow(True)

axes[0][0].grid(axis='y',linestyle='--')  
axes[0][0].set_axisbelow(True)

axes[0][1].grid(axis='y',linestyle='--')  
axes[0][1].set_axisbelow(True)

axes[0][2].grid(axis='y',linestyle='--')  
axes[0][2].set_axisbelow(True)


axes[1][0].grid(axis='y',linestyle='--')  
axes[1][0].set_axisbelow(True)


axes[1][1].grid(axis='y',linestyle='--')  
axes[1][1].set_axisbelow(True)


axes[1][2].grid(axis='y',linestyle='--')  
axes[1][2].set_axisbelow(True)


axes[1][3].grid(axis='y',linestyle='--')  
axes[1][3].set_axisbelow(True)


axes[0][3].axis('off') 


fig.legend(["Ear", "Ablation3"], loc='upper right', ncol=1, bbox_to_anchor=(0.96, 0.975),frameon=True, fontsize=22, labelspacing=0.4)
plt.tight_layout(pad = 0.1, rect = (0,0,1,1))

plt.show()


