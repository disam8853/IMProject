import numpy as np
from matplotlib import pyplot as plt
import matplotlib

# Delay demand
# NLS = [588923, 794922]
NLS = [52629, 224629, 588923, 794922, 1174930]
# NLS = [23578, 52629, 224629, 588923, 794922, 1174930]
# NLS = [33240, 191310, 1099500, 1790160, 2239320, 3704820]

# LRPS = [579120, 786700]
LRPS = [50580, 221130, 579120, 786700, 1152098]
# LRPS = [21750, 50580, 221130, 579120, 786700, 1152098]
# LRPS = [28020, 83250, 262860, 381450, 498030, 643200]

# TS = [591060, 808050]
TS = [54990, 225780, 591060, 808050, 1182450]
# TS = [24990, 54990, 225780, 591060, 808050, 1182450]
# TS = [37740, 345420, 2145030, 4176600, 5447070, 8770440]

# UP = [591060, 808050]
UP = [54990, 225780, 591060, 808050, 1182450]
# UP = [24990, 54990, 225780, 591060, 808050, 1182450]
# UP = [37740, 206760, 1192950, 2078610, 2861520, 4648620]

# LB = [578032, 786698]
LB = [49622.013, 220865.1787, 578032, 786698, 1151995]
# LB = [21734.472, 49622.013, 220865.1787, 578032, 786698, 1151995]
# LB = [27512.1102, 82345.9859, 237447.7018, 375402.2868, 494131.3, 634117.7132]
# user_pair = [30, 40]
user_pair = [10, 20, 30, 40, 50]


figure, ax = plt.subplots(figsize = (8,4), dpi=100)
# ax.plot(user_pair, NLS, label="NLS", color="darkorange", marker="o", linewidth=2)
ax.plot(user_pair, NLS, label="NLS", color="darkorange", marker="o", linewidth=2)
ax.plot(user_pair, LRPS, label="LRPS", color="olive", marker="^", linewidth=2)
# ax.plot(user_pair, LRPS, label="LRPS", color="darkseagreen", marker="^", linewidth=2, linestyle="-")
ax.plot(user_pair, TS, label="TS", color="lightslategrey", marker="s", linewidth=2)
# ax.plot(user_pair, TS, label="TS", color="cadetblue", marker="s", linewidth=2)
ax.plot(user_pair, UP, label="UP", color="tomato", marker="^", linewidth=2, linestyle=":")
# ax.plot(user_pair, UP, label="UP", color="lightcoral", marker="^", linewidth=2, linestyle=":")
# ax.plot(user_pair, LB, label="Lower Bound", color="gold", marker=".", linewidth=2, linestyle="--")
ax.plot(user_pair, LB, label="Lower Bound", color="gold", marker=".", linewidth=2, linestyle="--")
#major_tricks = np.arange(0, upper_bound+1000, 10000) 
#ax.set_xtricks(major_tricks)
ax.legend(loc="upper left")
ax.set_title("Deployment Cost with Increasing User Pair")
ax.set_xlabel("Number of User Pair")
# ax.set_xlim([0, 5])
ax.set_ylabel("Objective Value")
# ax.set_xticklabels("%.1f" %i for i in range(6))
figure.tight_layout()
plt.savefig("demand_exp_v4.png")
plt.show()
