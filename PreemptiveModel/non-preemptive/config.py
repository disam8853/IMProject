import math

# nodes num
NODES_COUNT = 20 
NODES = [i for i in range(1, NODES_COUNT+1)]

# link num
LINKS_COUNT = 100 

# link service rate random.randint(minSvcRate,maxSvcRate)
maxSvcRate = 25
minSvcRate = 20

# O-D pair traffic
traffic = 1

# O-D pair delay tolerance d_w random.uniform(minDelayTol_w,maxDelayTol_w)
maxDelayTol_w = 1.5
minDelayTol_w = 1

#priority num
priorityNum = 3

# priority on link delay tolerance max d_lk
maxDelayTol_lk = 1

# d_lk之間差值
d_lk_gap = 0.1

# x_wp找可能路徑所經過的link數
routing_num = 3

# iteration limit
ITER_LIMIT = 10

# improve limit
IMPROVE_LIMIT = 50

# lower bound
LB = -math.inf

# The target gap
GAP_MINIMUM = 0.05

# Lambda （0 <= lambda <= 2)
lamda = 0.25

