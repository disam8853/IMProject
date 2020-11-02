import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib



primal1 = [87935.138, 88021.142]
primal2 = [85540.013, 85973.927]
primal3 = [94593.177, 94601.781]
LB = [84336.5179, 83851.6419]
UP = [88537.248, 88741.317]
# data = np.array([primal1, primal2, primal3, LB, UP])
# x = [3, 8, 14]
index = ["Suurballe's Algo", "Yen's Algo"]
x = np.arange(len(index))
# width = 0.15
figure, ax = plt.subplots(figsize = (10,4), dpi=100)


# 長條圖
ax.bar(x-0.2, primal1, width=0.1, facecolor="sandybrown", edgecolor="white", label="NLS")
# ax.bar(x-0.1, UP, width=0.1, facecolor="tomato", edgecolor="white", label="UP")
ax.bar(x-0.1, primal2, width=0.1, facecolor="darkseagreen", edgecolor="white", label="LRPS")
ax.bar(x, LB, width=0.1, facecolor="gold", edgecolor="white", label="Lower Bound")
ax.bar(x+0.1, primal3, width=0.1, facecolor="cadetblue", edgecolor="white", label="TS")
ax.bar(x+0.2, UP, width=0.1, facecolor="tomato", edgecolor="white", label="UP")

ax.set_title("Deployment Cost When All Users Required 2 Paths")
ax.set_xlabel("Algorithm Used")
ax.set_ylabel("Objective Value")
ax.set_xticks(x)
ax.set_xticklabels(index)
ax.legend(loc="lower right")
figure.tight_layout()
plt.savefig("yen_vs_s_small_delay.png")
plt.show()
