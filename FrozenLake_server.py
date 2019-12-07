import random
from socket import *
import numpy as np
import gym
from gym import register
import re


def frozen(num):
    register(
        id='FrozenLake-v3',
        entry_point='gym.envs.toy_text:FrozenLakeEnv',
        kwargs={
            'map_name': '4x4',
            'is_slippery': False
        }
    )

    env = gym.make("FrozenLake-v3")

    Q = np.zeros([env.observation_space.n, env.action_space.n])  # (16,4) : 4*4 map + 상하좌우 4개

    num_episodes = num
    rList = []
    successRate = []

    def rargmax(vector):
        m = np.amax(vector)  # Return the maximum of an array or maximum along an axis (0 아니면 1)
        indices = np.nonzero(vector == m)[0]  # np.nonzero(True/False vector) => 최대값인 요소들만 걸러내
        return random.choice(indices)  # 그 중 하나 랜덤으로 선택

    for i in range(num_episodes):  # 학습을 num_episodes 만큼 시키면서 업데이트
        state = env.reset()  # 리셋
        total_reward = 0  # 나중에 그래프를 그리기 위한 (성공하면 1, 실패하면 0)
        done = None
        while not done:
            action = rargmax(Q[state, :])
            new_state, reward, done, _ = env.step(action)
            Q[state, action] = reward + np.max(Q[new_state, :])
            total_reward += reward
            state = new_state
        rList.append(total_reward)  # 이번 게임에서 reward가 0인지 1인지
        successRate.append(sum(rList) / (i + 1))  # 지금까지의 성공률
    print("Final Q-Table")
    print(Q)
    print("Success Rate : ", successRate[-1])

    return successRate[-1]


def frozen2(num):
    register(
        id='FrozenLake-v3',
        entry_point='gym.envs.toy_text:FrozenLakeEnv',
        kwargs={
            'map_name': '8x8',
            'is_slippery': False
        }
    )

    env = gym.make("FrozenLake-v3")

    Q = np.zeros([env.observation_space.n, env.action_space.n])  # (16,4) : 4*4 map + 상하좌우 4개

    num_episodes = num
    rList = []
    successRate = []

    def rargmax(vector):
        m = np.amax(vector)  # Return the maximum of an array or maximum along an axis (0 아니면 1)
        indices = np.nonzero(vector == m)[0]  # np.nonzero(True/False vector) => 최대값인 요소들만 걸러내
        return random.choice(indices)  # 그 중 하나 랜덤으로 선택

    for i in range(num_episodes):  # 학습을 num_episodes 만큼 시키면서 업데이트
        state = env.reset()  # 리셋
        total_reward = 0  # 나중에 그래프를 그리기 위한 (성공하면 1, 실패하면 0)
        done = None
        while not done:
            action = rargmax(Q[state, :])
            new_state, reward, done, _ = env.step(action)
            Q[state, action] = reward + np.max(Q[new_state, :])
            total_reward += reward
            state = new_state
        rList.append(total_reward)  # 이번 게임에서 reward가 0인지 1인지
        successRate.append(sum(rList) / (i + 1))  # 지금까지의 성공률
    print("Final Q-Table")
    print(Q)
    print("Success Rate : ", successRate[-1])

    return successRate[-1]

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print("접속 대기중")
connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속이 확인되었습니다.')


data = connectionSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))
newdata = data.decode('utf-8')
list = newdata.split('a')
print(list)


if (list[1] == '1'):
    print("연산중입니다.")
    print(list)
    rate = frozen(int(list[0]))
    rateStr = str(rate)
    connectionSock.send(rateStr.encode('utf-8'))
else:
    print("연산중입니다.")
    print(list)
    rate = frozen2(int(list[0]))
    rateStr = str(rate)
    connectionSock.send(rateStr.encode('utf-8'))

    print('메시지를 보냈습니다.')