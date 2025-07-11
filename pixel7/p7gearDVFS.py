import os
import os.path as path
import csv
import json
import time
import datetime
import pickle
import numpy as np
import pandas as pd

import torch
from torch import nn
import torch.nn.functional as F
import torch.utils.data
import subprocess

from p7utils import *
from time import sleep

import os,sys
import math
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from p7gearDVFSmodel import DQN_v0, ReplayMemory, DQN_AB

from torch.utils.tensorboard import SummaryWriter

from typing import Optional

"""
RL Agents are responsible for train/inference
Available Agents:
1. Vanilla Agent
2. Agent with Action Branching
"""

def save_checkpoint(state, savepath, flag=True):
    """Save for general purpose (e.g., resume training)"""
    if not os.path.isdir(savepath):
        os.makedirs(savepath, 0o777)
    # timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    if flag:
        filename = os.path.join(savepath, "best_ckpt.pth.tar")
    else:
        filename = os.path.join(savepath, "newest_ckpt.pth.tar")
    torch.save(state, filename)


def load_checkpoint(savepath, flag=True):
    """Load for general purpose (e.g., resume training)"""
    if flag:
        filename = os.path.join(savepath, "best_ckpt.pth.tar")
    else:
        filename = os.path.join(savepath, "newest_ckpt.pth.tar")
    if not os.path.isfile(filename):
        return None
    state = torch.load(filename)
    return state

# Agent with action branching without time context
class DQN_AGENT_AB():
	def __init__(self, s_dim, h_dim, branches, buffer_size, params):
		"""
		s_dim是输入向量的维度
		h_dim是隐藏层的温度
		branches是一个列表内的每一个数字代表该分支的Actions大小。
		"""
  		
		self.eps = 0.8
		self.actions = [np.arange(i) for i in branches]
		# Experience Replay(requires belief state and observations)
		self.mem = ReplayMemory(buffer_size)
		# Initi networks
		self.policy_net = DQN_AB(s_dim, h_dim, branches)
		self.target_net = DQN_AB(s_dim, h_dim, branches)
		
		# self.weights = params["policy_net"]
		self.target_net.load_state_dict(self.policy_net.state_dict())
		self.target_net.eval()

		self.optimizer = torch.optim.RMSprop(self.policy_net.parameters())
		self.criterion = nn.SmoothL1Loss() # Huber loss
		
	def max_action(self, state):
		# actions for multidomains
		max_actions = []
		with torch.no_grad():
			# Inference using policy_net given (domain, batch, dim)
			q_values = self.policy_net(state)
			for i in range(len(q_values)):
				domain = q_values[i].max(dim=1).indices
				max_actions.append(self.actions[i][domain])
		return max_actions

	def e_gready_action(self, actions, eps):
		# Epsilon-Gready for exploration
		final_actions = []
		for i in range(len(actions)):
			p = np.random.random()
			if isinstance(actions[i],np.ndarray):
				if p < 1- eps:
					final_actions.append(actions[i])
				else:
					# randint in (0, domain_num), for batchsize
					final_actions.append(np.random.randint(len(self.actions[i]),size=len(actions[i])))
			else:
				if p < 1- eps:
					final_actions.append(actions[i])
				else:
					final_actions.append(np.random.choice(self.actions[i]))
		final_actions = [int(i) for i in final_actions]
		return final_actions

	def select_action(self, state):
		return self.e_gready_action(self.max_action(state),self.eps)

	def train(self, n_round, n_update, n_batch):
		# Train on policy_net
		losses = []
		self.target_net.train()
		train_loader = torch.utils.data.DataLoader(
			self.mem, batch_size=n_batch, shuffle=True, drop_last=True)
		length = len(train_loader.dataset)
		GAMMA = 1.0
	
		# Calcuate loss for each branch and then simply sum up
		for i, trans in enumerate(train_loader):
			loss = 0.0 # initialize loss at the beginning of each batch
			states, actions, next_states, rewards = trans
			with torch.no_grad():
				target_result = self.target_net(next_states)
			policy_result = self.policy_net(states)
			# Loop through each action domain
			for j in range(len(self.actions)):
				next_state_values = target_result[j].max(dim=1)[0].detach()
				expected_state_action_values = (next_state_values*GAMMA) + rewards.float()
				# Gather action-values that have been taken
				branch_actions = actions[j].long()
				state_action_values = policy_result[j].gather(1, branch_actions.unsqueeze(1))
				loss += self.criterion(state_action_values, expected_state_action_values.unsqueeze(1))
			losses.append(loss.item())
			self.optimizer.zero_grad()
			loss.backward()
			if i>n_update:
				break

			self.optimizer.step()
		return losses

	def save_model(self, n_round, savepath):
		save_checkpoint({'epoch': n_round, 'model_state_dict':self.target_net.state_dict(),
	        'optimizer_state_dict':self.optimizer.state_dict()}, savepath)
		f = open(os.path.join(savepath,"memory"), 'wb')
		pickle.dump(self.mem,f)
		f.close()

	def load_model(self, loadpath):
		if not os.path.isdir(loadpath): os.makedirs(loadpath)
		checkpoint = load_checkpoint(loadpath)
		if checkpoint is not None:
			self.policy_net.load_state_dict(checkpoint['model_state_dict'])
			self.target_net.load_state_dict(checkpoint['model_state_dict'])
			self.target_net.eval()
		if os.path.exists(os.path.join(loadpath,"memory")):
			f = open(os.path.join(loadpath,"memory"),'rb')
			self.mem = pickle.load(f)
			f.close()

	def sync_model(self):
		self.target_net.load_state_dict(self.policy_net.state_dict())


def cal_cpu_reward(cpu_utils,cpu_temps,cluster_num):
    global targetUtil
    lambda_value = 0.15
    # for cpu
    cpu_u_max,cpu_u_min = 0.85+targetUtil,0.75+targetUtil
    cpu_u_g = 0.8+targetUtil
    u,v,w = -0.2,0.21,0.1
    # temp_thre = 60
    reward_value = 0.0
    cpu_t =cpu_temps[0]
    # print('cpu',end=': ')
    for cpu_u in cpu_utils:
        if cpu_t < temp_thre:
            w = 0.2 * math.tanh(temp_thre-cpu_t)
        else:
            w = -2
        if cpu_u < cpu_u_min and cpu_u > cpu_u_max:
            d =lambda_value
        else:
            d = u+v*math.exp(-(cpu_u-cpu_u_g)**2 / (w ** 2))
        reward_value += d
        # print(f"{d}",end=',')
    
    return reward_value/cluster_num
  
def cal_gpu_reward(gpu_utils,gpu_temps,num):
    global targetUtil
    lambda_value = 0.1
    # for cpu
    gpu_u_max,gpu_u_min = 0.85+targetUtil,0.75+targetUtil
    gpu_u_g = 0.8+targetUtil
    u,v,w = -0.05,0.051,0.1
    # temp_thre = 60
    reward_value = 0
    # print('gpu',end=': ')
    for gpu_u,gpu_t in zip(gpu_utils,gpu_temps):
        if gpu_t < temp_thre:
            w = 0.2 * math.tanh(temp_thre-gpu_t)
        else:
            w = -2
        if gpu_u < gpu_u_min and gpu_u > gpu_u_max:
            d =lambda_value
        else:
            d = u+v*math.exp(-(gpu_u-gpu_u_g)**2 / (w ** 2))
        reward_value += d
        # print(f"{d}",end=',')
    return reward_value/num 

def get_ob_phone(a, aa, qos_type: str, qos_time_prev: float, byte_prev: Optional[int], packet_prev: Optional[int]):
    # State Extraction and Reward Calculation

	global targetUtil
	t1a, t2a, littlea, mida, biga, gpua = aa

	c_states, temps, qos, t1b, t2b, littleb, midb, bigb, gpub, b, gpu_util, freqs, _, _, _ = get_states2(window, "fps", None, None, None)
	little_c, mid_c, big_c, gpu_c = c_states
	little_f, mid_f, big_f, gpu_f = freqs
	little_t, mid_t, big_t, gpu_t, qi_t, batt_t = temps

	bb = (t1b, t2b, littleb, midb, bigb, gpub)

	# cpu_util = get_cpu_util()
	# gpu_util = get_gpu_util()

	# little_f, mid_f, big_f, gpu_f = get_frequency()
	# little_t, mid_t, big_t, gpu_t, qi_t, batt_t = get_temperatures()

	gpu_freq = [gpu_f]
	cpu_freq = [little_f, mid_f, big_f]
	gpu_thremal= [gpu_t]
	cpu_thremal = np.array([(little_t + mid_t + big_t) / 3])
	

	# b = get_core_util()
	# t1b, t2b, littleb, midb, bigb, gpub = get_energy()

	cpu_util = list(cal_core_util(b,a))

	power = (littleb + midb + bigb - littlea - mida - biga)/(t1b-t1a) + (gpub-gpua)/(t2b-t2a)
	# power2 = get_battery_power()

	fps = qos

	qos_time_cur = None
	byte_cur = None
	packet_cur = None
	match qos_type:
		# case "fps":
		# 	qos = get_fps(window)
		case "byte":
			byte_cur = get_packet_info(window, qos_type)
			qos_time_cur = time.time()
			qos = cal_packet((byte_prev, byte_cur), (qos_time_prev, qos_time_cur))
			# print(byte_cur[1] - byte_prev[1], byte_cur[0] - byte_prev[0], qos_time_cur - qos_time_prev, qos)
			byte_prev = byte_cur
		case "packet":
			packet_cur = get_packet_info(window, qos_type)
			qos_time_cur = time.time()
			qos = cal_packet((packet_prev, packet_cur), (qos_time_prev, qos_time_cur))
			packet_prev = packet_cur

	util_li = np.concatenate([cpu_util, gpu_util])


	# 16个数据
	states = np.concatenate([gpu_util,cpu_util,gpu_freq,cpu_freq,gpu_thremal,cpu_freq,[power]]).astype(np.float32)

	reward = cal_cpu_reward(cpu_util,cpu_thremal,8)
	reward += cal_gpu_reward(gpu_util,gpu_thremal,1)
	# print()
	return c_states, states,reward, power, [little_t, mid_t, big_t, gpu_t, qi_t, batt_t], qos, util_li, qos_time_cur, byte_cur, packet_cur, b, bb

def action_to_freq(action):

	little_min, little_max = little_available_frequencies[action[0]], little_available_frequencies[action[0]]
	mid_min, mid_max = mid_available_frequencies[action[1]], mid_available_frequencies[action[1]]
	big_min, big_max = big_available_frequencies[action[2]], big_available_frequencies[action[2]]
	gpu_min, gpu_max = gpu_available_frequencies[action[3]], gpu_available_frequencies[action[3]]

	return little_min, little_max, mid_min, mid_max, big_min, big_max, gpu_min, gpu_max

if __name__ == "__main__":
	

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--total_timesteps", type=int, default = 1001,
						help="total timesteps of the experiments")
	parser.add_argument("--experiment", type=int, default = 1,
						help="the type of experiment")
	parser.add_argument("--temperature", type=int, default = 20,
						help="the ouside temperature")
	parser.add_argument("--initSleep", type=int, default = 1,
						help="initial sleep time")
	parser.add_argument("--loadModel", type=str, default = "no",
						help="initial sleep time")
	parser.add_argument("--timeOut", type=int, default = 60*30,
                    help="end time")
	parser.add_argument("--qos", default="fps", choices=['fps', 'byte', 'packet'],
                    help="Quality of Service")
	parser.add_argument("--targetTemp", type = int, default=60,
                    help="target temperature")
	parser.add_argument("--latency", type = int, default=0,
					help="additional latency for adb communication (ms)")
	parser.add_argument("--interval", type = float, default=0.2,
					help="interval between DVFSs (s)")
	parser.add_argument("--tempSet", type = float, default=-1.0,
					help="initial temperature")
	parser.add_argument("--targetUtil", type = float, default=0.0,
                    help="target utilization")
	args = parser.parse_args()

	print(args)

	total_timesteps = args.total_timesteps
	experiment = args.experiment
	temperature = args.temperature
	initSleep = args.initSleep
	qos_type = args.qos
	temp_thre = args.targetTemp
	latency = args.latency/1000
	interval = args.interval

	targetUtil = args.targetUtil

	N_S, N_A, N_B = 5, 3, 11

	# Test/Train Demo for DQN_AB
	print("Test/Train Demo for DQN_AB")
	agent = DQN_AGENT_AB(N_S, 15, [3,5], 11, None)
	EPS_START = 0.99
	EPS_END = 0.2
	EPS_DECAY = 1000
	n_update, n_batch = 5,4
	SYNC_STEP = 30
	N_S,  N_BUFFER = 18, 36000
	agent = DQN_AGENT_AB(N_S,8,[11,15,16,11],N_BUFFER,None)
	prev_state, prev_action = [None]*2
	record_count, test_count, n_round, g_step = [0]*4
	seed = 1

	random.seed(seed)
	np.random.seed(seed)
	torch.manual_seed(seed)

	global_count = 0

	run_name = f"{int(time.time())}__p7gearDVFS__{seed}__{args.tempSet}__exp{args.experiment}__temp{args.temperature}__target{args.targetTemp}__targetUtil{args.targetUtil}"
	# run_name = "gearDVFS__" + str(int(time.time()))+"__exp"+str(experiment)+"__temp"+str(temperature)

	if len(args.loadModel) > 2:
		agent.policy_net.load_state_dict(torch.load("save/"+args.loadModel+"_policy_net.pt"))
		agent.target_net.load_state_dict(torch.load("save/"+args.loadModel+"_target_net.pt"))
		
	littleReal = []
	midReal = []
	bigReal = []
	gpuReal = []

	little = []
	mid = []
	big = []
	gpu = []
	ppw = []
	ts = []
	fpsLi = []
	bytesLi = []
	packetsLi = []
	rewardLi = []
	powerLi = []
	lossLi = []
	tempLi = []

	l1Li = []
	l2Li = []
	l3Li = []
	l4Li = []
	m1Li = []
	m2Li = []
	b1Li = []
	b2Li = []
	guLi = []

	little_c = []
	mid_c = []
	big_c = []
	gpu_c = []


	wait_temp(args.tempSet - 1)
	wait_temp(args.tempSet + 0.5)

	# adb root
	set_root()
	
	# turn_off_usb_charging()

	turn_off_screen()

	turn_on_screen()
	
	sleep(initSleep)

	turn_on_screen()

	set_brightness(158)

	sleep(5)

	window = get_window()

	unset_frequency()

	# unset_rate_limit_us()
	set_rate_limit_us(1000000000, 20)

	a = get_core_util()
	aa = get_energy()
	qos_time_prev = time.time()
	byte_prev = None
	packet_prev = None
	match qos_type:
		case "byte":
			byte_prev = get_packet_info(window, qos_type)
		case "packet":
			packet_prev = get_packet_info(window, qos_type)
	sleep(interval)

	writer = SummaryWriter(f"runs/{run_name}")

	start_time = time.time()

	little_past, mid_past, big_past, gpu_past = -1, -1, -1, -1

	while True:

		if time.time() - start_time > args.timeOut:
			break

		c_states, state, reward, power1, temps, qos, util_li, qos_time_cur, byte_cur, packet_cur, a, aa = get_ob_phone(a, aa, qos_type, qos_time_prev, byte_prev, packet_prev)

		little_c1, mid_c1, big_c1, gpu_c1 = c_states

		agent.eps = EPS_END + (EPS_START - EPS_END) * \
                math.exp(-1. * g_step / EPS_DECAY)
		action = agent.select_action(torch.from_numpy(state).unsqueeze(0))
		if record_count!=0:
			agent.mem.push(prev_state, prev_action, state, reward)
		prev_state, prev_action = state, action


		sleep(latency)
		# set dvfs
		little_min, little_max, mid_min, mid_max, big_min, big_max, gpu_min, gpu_max = action_to_freq(action)
		set_frequency(little_min, little_max, mid_min, mid_max, big_min, big_max, gpu_min, gpu_max)
		little_past, mid_past, big_past, gpu_past = little_min, mid_min, big_min, gpu_min

		# a = get_core_util()
		# aa = get_energy()

		qos_time_prev = qos_time_cur
		byte_prev = byte_cur
		packet_prev = packet_cur

		sleep(interval)
		sleep(latency)

		record_count+=1
		global_count += 1

		little1, mid1, big1, gpu1 = state[[-4, -3, -2, 9]]

		if little_past != -1:

			littleReal.append(little1)
			midReal.append(mid1)
			bigReal.append(big1)
			gpuReal.append(gpu1)

			little.append(little_past)
			mid.append(mid_past)
			big.append(big_past)
			gpu.append(gpu_past)
			ppw.append(qos/power1)
			match qos_type:
				case "fps":
					fpsLi.append(qos)
				case "byte":
					bytesLi.append(qos)
				case "packet":
					packetsLi.append(qos)	
			powerLi.append(power1)
			rewardLi.append(reward)
			tempLi.append(temps)

			l1Li.append(util_li[0])
			l2Li.append(util_li[1])
			l3Li.append(util_li[2])
			l4Li.append(util_li[3])
			m1Li.append(util_li[4])
			m2Li.append(util_li[5])
			b1Li.append(util_li[6])
			b2Li.append(util_li[7])
			guLi.append(util_li[8])

			little_c.append(little_c1)
			mid_c.append(mid_c1)
			big_c.append(big_c1)
			gpu_c.append(gpu_c1)

		if (record_count%5==0 and record_count!=0):

			# train loop
			losses = agent.train(n_round,n_update,n_batch)

			if global_count % 10 == 0 and global_count != 0:
				print(global_count, end = " ")
				writer.add_scalar("losses/loss", losses[-1], global_count)
				writer.add_scalar("freq/little", np.array(little)[-10:].mean(), global_count)
				writer.add_scalar("freq/mid", np.array(mid)[-10:].mean(), global_count)
				writer.add_scalar("freq/big", np.array(big)[-10:].mean(), global_count)
				writer.add_scalar("freq/gpu", np.array(gpu)[-10:].mean(), global_count)

				writer.add_scalar("real/little", np.array(littleReal)[-10:].mean(), global_count)
				writer.add_scalar("real/mid", np.array(midReal)[-10:].mean(), global_count)
				writer.add_scalar("real/big", np.array(bigReal)[-10:].mean(), global_count)
				writer.add_scalar("real/gpu", np.array(gpuReal)[-10:].mean(), global_count)

				writer.add_scalar("perf/ppw", np.array(ppw)[-10:].mean(), global_count)
				writer.add_scalar("perf/reward", np.array(rewardLi)[-10:].mean(), global_count)
				writer.add_scalar("perf/power", np.array(powerLi)[-10:].mean(), global_count)
				match qos_type:
					case "fps":
						writer.add_scalar("perf/fps", np.array(fpsLi)[-10:].mean(), global_count)
					case "byte":
						writer.add_scalar("perf/bytes", np.array(bytesLi)[-10:].mean(), global_count)
					case "packet":
						writer.add_scalar("perf/packets", np.array(packetsLi)[-10:].mean(), global_count)
				writer.add_scalar("temp/little", np.array(tempLi)[-10:, 0].mean(), global_count)
				writer.add_scalar("temp/mid", np.array(tempLi)[-10:, 1].mean(), global_count)
				writer.add_scalar("temp/big", np.array(tempLi)[-10:, 2].mean(), global_count)
				writer.add_scalar("temp/gpu", np.array(tempLi)[-10:, 3].mean(), global_count)
				writer.add_scalar("temp/qi", np.array(tempLi)[-10:, 4].mean(), global_count)
				writer.add_scalar("temp/battery", np.array(tempLi)[-10:, 5].mean(), global_count)


				writer.add_scalar("cstate/little", np.array(little_c)[-10:].mean(), global_count)
				writer.add_scalar("cstate/mid", np.array(mid_c)[-10:].mean(), global_count)
				writer.add_scalar("cstate/big", np.array(big_c)[-10:].mean(), global_count)
				writer.add_scalar("cstate/gpu", np.array(gpu_c)[-10:].mean(), global_count)


				writer.add_scalar("util/l1", np.array(l1Li)[-10:].mean(), global_count)
				writer.add_scalar("util/l2", np.array(l2Li)[-10:].mean(), global_count)
				writer.add_scalar("util/l3", np.array(l3Li)[-10:].mean(), global_count)
				writer.add_scalar("util/l4", np.array(l4Li)[-10:].mean(), global_count)
				writer.add_scalar("util/m1", np.array(m1Li)[-10:].mean(), global_count)
				writer.add_scalar("util/m2", np.array(m2Li)[-10:].mean(), global_count)
				writer.add_scalar("util/b1", np.array(b1Li)[-10:].mean(), global_count)
				writer.add_scalar("util/b2", np.array(b2Li)[-10:].mean(), global_count)
				writer.add_scalar("util/gu", np.array(guLi)[-10:].mean(), global_count)
				writer.add_scalar("util/little", (np.array(l1Li[-10:]).mean()+np.array(l2Li[-10:]).mean()+np.array(l3Li[-10:]).mean()+np.array(l4Li[-10:]).mean()) / 4, global_count)
				writer.add_scalar("util/mid", (np.array(m1Li[-10:]).mean()+np.array(m2Li[-10:]).mean()) / 2, global_count)
				writer.add_scalar("util/big", (np.array(b1Li[-10:]).mean()+np.array(b2Li[-10:]).mean()) / 2, global_count)


			# Reset initial states/actions to None
			prev_state,prev_action,record_count = None,None,0
			# save model
			n_round += 1
			if n_round % SYNC_STEP == 0: agent.sync_model()
		
		if global_count >= total_timesteps:
			turn_on_usb_charging()
			unset_rate_limit_us()
			turn_off_screen()
			unset_frequency()
			torch.save(agent.policy_net.state_dict(), "save/"+run_name+"_policy_net.pt")
			torch.save(agent.target_net.state_dict(), "save/"+run_name+"_target_net.pt")
			break

		"""
		torch.save(agent.policy_net.state_dict(), "asdf.pt")
		actor2.load_state_dict(torch.load("asdf.pt", map_location=device))
		agent.policy_net.state_dict()
		agent2.policy_net.state_dict()
		"""

	
	turn_on_usb_charging()
	unset_rate_limit_us()
	turn_off_screen()
	unset_frequency()