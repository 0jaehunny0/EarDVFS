python pixel7/p7zTT.py --total_timesteps 4501 --experiment 2 --temperature 10 --initSleep 10 --timeOut 1800 --latency 0 --tempSet 20 --targetTemp 65
python pixel7/p7OURS4.py --total_timesteps 4501 --experiment 2 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20 --learning_starts 10 --q_lr 5.0e-4
python pixel7/p7gearDVFS.py --total_timesteps 4501 --experiment 2 --temperature 10 --initSleep 10 --timeOut 1800 --latency 0 --tempSet 20 --targetTemp 60 --targetUtil 0.0
python pixel7/p7defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20

python pixel7/p7screenoff.py
exit 1 

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 12 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
exit 1 

python DVFS/zTT.py --total_timesteps 4501 --experiment 12 --temperature 20 --initSleep 10 --timeOut 1800 --latency 0 --tempSet 30.0 --targetTemp 65
python DVFS/screenoff.py
exit 1 



python DVFS/gearDVFS.py --total_timesteps 4501 --experiment 12 --temperature 20 --initSleep 10 --timeOut 1800 --latency 0 --tempSet 30.0 --targetTemp 60 --targetUtil 0.0
python DVFS/screenoff.py
exit 1 


python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 12 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
exit 1 

python DVFS/OURS4.py --total_timesteps 4501 --experiment 12 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 






python DVFS/defaultDVFStempChange.py --total_timesteps 4501 --experiment 12 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
exit 1 

python DVFS/gearDVFS.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --latency 0 --tempSet 30.0 --targetTemp 60 --targetUtil 0.0
python DVFS/screenoff.py
exit 1 

python DVFS/zTT.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --latency 0 --tempSet 30.0 --targetTemp 65
python DVFS/screenoff.py
exit 1 





python DVFS/defaultDVFSmonitorTemp.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 20.0
python DVFS/screenoff.py
exit 1 


python DVFS/freqFixedwaitTempAll.py --total_timesteps 9001 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet 40.0 --big 500000 --gpu 151000
python DVFS/screenoff.py

python DVFS/freqFixedwaitTempAll.py --total_timesteps 9001 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet 50.0 --big 500000 --gpu 151000
python DVFS/screenoff.py

exit 1 

python DVFS/OURS4.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 



python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 

python DVFS/defaultDVFSmonitorTemp.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 20.0
python DVFS/screenoff.py

python DVFS/defaultDVFSmonitorTemp.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
exit 1 

python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 





python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 10 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4.py --total_timesteps 4501 --experiment 10 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 10 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0
python DVFS/screenoff.py
exit 1 




python DVFS/freqFixed.py --total_timesteps 9001 --experiment 2 --temperature 20 --initSleep 10 --timeOut 3600 --tempSet 30.0 --big 500000 --gpu 151000
python DVFS/screenoff.py
exit 1 


python DVFS/freqFixed.py --total_timesteps 9001 --experiment 2 --temperature 30 --initSleep 10 --timeOut 3600 --tempSet 40.0 --big 500000 --gpu 151000
python DVFS/screenoff.py
exit 1 


python DVFS/freqFixed.py --total_timesteps 9001 --experiment 2 --temperature 10 --initSleep 10 --timeOut 3600 --tempSet 20.0 --big 500000 --gpu 151000
python DVFS/screenoff.py
exit 1 

python DVFS/freqFixed.py --total_timesteps 9001 --experiment 2 --temperature 10 --initSleep 10 --timeOut 3600 --tempSet 20.0 --big 1826000 --gpu 471000
python DVFS/screenoff.py
exit 1 


python DVFS/freqFixed.py --total_timesteps 9001 --experiment 2 --temperature 30 --initSleep 10 --timeOut 3600 --tempSet 40.0 --big 1826000 --gpu 471000
python DVFS/screenoff.py
exit 1 


python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet 20.0
python DVFS/screenoff.py
exit 1 

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 12 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0
python DVFS/screenoff.py
exit 1 

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet 20.0
python DVFS/screenoff.py
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet -1.0
python DVFS/screenoff.py
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet -1.0
python DVFS/screenoff.py
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 600 --tempSet -1.0
python DVFS/screenoff.py

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0


python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
sleep 300
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet -1.0

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
sleep 300
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet -1.0

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
sleep 300
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet -1.0

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0
python DVFS/screenoff.py
sleep 300
python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 2 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet -1.0


python DVFS/screenoff.py
exit 1 

python DVFS/defaultDVFS.py --total_timesteps 4501 --experiment 10 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0
python DVFS/screenoff.py
exit 1 

python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 10 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4.py --total_timesteps 4501 --experiment 10 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4.py --total_timesteps 4501 --experiment 10 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/screenoff.py
exit 1 


python DVFS/OURS4ablation44.py --total_timesteps 4501 --experiment 1 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation44.py --total_timesteps 4501 --experiment 1 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation44.py --total_timesteps 4501 --experiment 1 --temperature 20 --initSleep 10 --timeOut 1800 --tempSet 30.0 --learning_starts 10 --q_lr 5.0e-4

python DVFS/screenoff.py
exit 1 



python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation3.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation42.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation43.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation3.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation42.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation43.py --total_timesteps 4501 --experiment 1 --temperature 30 --initSleep 10 --timeOut 1800 --tempSet 40.0 --learning_starts 10 --q_lr 5.0e-4


python DVFS/screenoff.py
exit 1 




python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation3.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation42.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation43.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation2.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation3.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation42.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4
python DVFS/OURS4ablation43.py --total_timesteps 4501 --experiment 1 --temperature 10 --initSleep 10 --timeOut 1800 --tempSet 20.0 --learning_starts 10 --q_lr 5.0e-4


python DVFS/screenoff.py
exit 1 