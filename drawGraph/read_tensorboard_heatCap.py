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


sensor_list = [
    "BIG", "ISP", "MID",   "disp_therm",
    "maxfg", "pca9468-mains",  "qi_therm", "rf1_therm",  "usb_pwr_therm", 
    "G3D", "LITTLE", "TPU", "battery",
    "gnss_tcxo_therm", "neutral_therm", "quiet_therm",
      "usb_pwr_therm2",
]

sensorDict = {}

scalars = [
]
for i in sensor_list:
    scalars.append("tempAll/"+i)

for i in scalars:
    sensorDict[i] = {}

for subdir, dirs, files in os.walk("selected/heatCap"):
# for subdir, dirs, files in os.walk("selected/iccadFluctuation2"):
    a = subdir.split("/")


    if len(a) > 2:
        if len(a) > 2:
            if "def" in a[2].split("_")[2]:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]
            else:
                mykey = a[2].split("_")[2] + a[2].split("_")[-1]
            for i in scalars:
                sensorDict[i][mykey] = []


for subdir, dirs, files in os.walk("selected/heatCap"):
# for subdir, dirs, files in os.walk("selected/iccadFluctuation2"):
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

            for asdf in  scalars:
                sensorDict[asdf][mykey].append(x[asdf])

            

############ figure 1

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






#########################

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


fig, axes = plt.subplots(1, 1, figsize=(4.8, 3.3))


deft = sensorDict["tempAll/disp_therm"][mykey][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %2 == 1:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-1:i+1]) / 2 / 1000)
# axes.plot(deft2, deft3, color = "C0", label = "ISP")
axes.plot(deft2, deft3, color = "C0", label = "Display")

# deft = sensorDict["tempAll/disp_therm"][mykey][0]
# deft2, deft3 = [], []
# firstTime = deft["wall_time"][0]
# for i in range(len(deft["step"])):
#     if i %2 == 1:
#         deft2.append(deft["wall_time"][i] - firstTime)
#         deft3.append(sum(deft["value"][i-1:i+1]) / 2/ 1000)
# axes.plot(deft2, deft3, color = "C1", label= "display")

deft = sensorDict["tempAll/battery"][mykey][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %2 == 1:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-1:i+1]) / 2/ 1000)
axes.plot(deft2, deft3, color = "C2", label = "Battery")


deft = sensorDict["tempAll/gnss_tcxo_therm"][mykey][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %2 == 1:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-1:i+1]) / 2/ 1000)
axes.plot(deft2, deft3, color = "C3", label = "GNSS")


deft = sensorDict["tempAll/pca9468-mains"][mykey][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %2 == 1:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-1:i+1]) / 2 * 10/ 1000)
axes.plot(deft2, deft3, color = "C4", label = "PMIC")

# deft = sensorDict["tempAll/qi_therm"][mykey][0]
# deft2, deft3 = [], []
# firstTime = deft["wall_time"][0]
# for i in range(len(deft["step"])):
#     if i %2 == 1:
#         deft2.append(deft["wall_time"][i] - firstTime)
#         deft3.append(sum(deft["value"][i-1:i+1]) / 2 / 1000)
# axes.plot(deft2, deft3, color = "C5", label = "remote charger")

# deft = sensorDict["tempAll/usb_pwr_therm"][mykey][0]
# deft2, deft3 = [], []
# firstTime = deft["wall_time"][0]
# for i in range(len(deft["step"])):
#     if i %2 == 1:
#         deft2.append(deft["wall_time"][i] - firstTime)
#         deft3.append(sum(deft["value"][i-1:i+1]) / 2 / 1000)
# axes.plot(deft2, deft3, color = "C6", label = "usb")


deft = sensorDict["tempAll/G3D"][mykey][0]
deft2, deft3 = [], []
firstTime = deft["wall_time"][0]
for i in range(len(deft["step"])):
    if i %2 == 1:
        deft2.append(deft["wall_time"][i] - firstTime)
        deft3.append(sum(deft["value"][i-1:i+1]) / 2/ 1000)
axes.plot(deft2, deft3, color = "C7", label = "GPU")


defta = sensorDict["tempAll/BIG"][mykey][0]
deftb = sensorDict["tempAll/MID"][mykey][0]
deftc = sensorDict["tempAll/LITTLE"][mykey][0]
deft2, deft3 = [], []
firstTime = defta["wall_time"][0]
for i in range(len(defta["step"])):
    if i %2 == 1:
        deft2.append(defta["wall_time"][i] - firstTime)
        deft3.append((sum(defta["value"][i-1:i+1]) + sum(deftb["value"][i-1:i+1]) + sum(deftc["value"][i-1:i+1]))/3 / 2 / 1000)
axes.plot(deft2, deft3, color = "C8", label = "CPU")

axes.grid(axis='both',linestyle='--')  
axes.set_axisbelow(True)

axes.set_xlabel("Time (s)")
axes.set_ylabel("Temp. (°C)")
axes.set_xticks([0, 600, 1200, 1800])


# plt.legend()
# plt.tight_layout(pad=0.1)

fig.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.047),frameon=False, borderpad=0.1, fontsize=22, columnspacing = 0.4, handlelength=1)
plt.tight_layout(pad = 0.05, rect = (0,0,1,0.75))

plt.show()

