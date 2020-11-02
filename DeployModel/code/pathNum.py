import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib


# Delay demand
primal1 = [167790, 329938, 588923]
primal2 = [167790, 315022, 579120]
primal3 = [167790, 331410, 591060]
LB = [165227.312, 317489, 578023]
UP = [167790, 331410, 591060]
# data = np.array([primal1, primal2, primal3, LB, UP])
# x = [3, 8, 14]
index = ["2-3", "2-8", "2-14"]
x = np.arange(len(index))
# width = 0.15
figure, ax = plt.subplots(figsize = (10,4), dpi=100)

# 折線圖
# ax.plot(x, primal1, label="NLS", color="sandybrown", marker="o", linewidth=2)
# ax.plot(x, primal2, label="LRPS", color="darkseagreen", marker="^", linewidth=2)
# ax.plot(x, primal3, label="TS", color="cadetblue", marker="s", linewidth=2)
# ax.plot(x, LB, label="Lower Bound", color="gold", marker="*", linewidth=2)
# ax.plot(x, UP, label="UP", color="tomato", marker="^", linewidth=2, linestyle=":")

# 長條圖
ax.bar(x-0.2, primal1, width=0.1, facecolor="sandybrown", edgecolor="white", label="NLS")
ax.bar(x-0.1, UP, width=0.1, facecolor="tomato", edgecolor="white", label="UP")
ax.bar(x, primal2, width=0.1, facecolor="darkseagreen", edgecolor="white", label="LRPS")
ax.bar(x+0.1, LB, width=0.1, facecolor="gold", edgecolor="white", label="Lower Bound")
ax.bar(x+0.2, primal3, width=0.1, facecolor="cadetblue", edgecolor="white", label="TS")

ax.set_title("Deployment Cost with Increasing Range of Path Number")
ax.set_xlabel("Number of Paths")
ax.set_ylabel("Objective Value")
ax.set_xticks(x)
ax.set_xticklabels(index)
ax.legend(loc="upper left")
figure.tight_layout()
plt.savefig("path_number_v3.png")
plt.show()
