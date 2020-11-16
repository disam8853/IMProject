#%matplotlib inline
from Class import *
import numpy as np
import math
import sys
from matplotlib import pyplot as plt
import matplotlib
import time

class LR():
    def __init__(self, r_loc: LinkSet, o_loc: LinkSet, p_loc: LinkSet, q_loc: LinkSet, s_loc: LinkSet, ro: float, delay_toler: float, comm_links: LinkSet, pairset: UserpairSet):
        self.ro = ro     
        self.delay_toler = delay_toler
        self.comm_links = comm_links
        self.comm_link_num = self.comm_links.length()
        self.pairset = pairset
        self.userpair_num = self.pairset.length()
        self.gamma = self.pairset.get_all_traffic()
        self.r_loc = r_loc
        self.o_loc = o_loc
        self.p_loc = p_loc
        self.q_loc = q_loc
        self.s_loc = s_loc
        
        self.r_loc_num = r_loc.length()
        self.o_loc_num = o_loc.length()
        self.p_loc_num = p_loc.length()
        self.q_loc_num = q_loc.length()
        self.s_loc_num = s_loc.length()

        self.r_capacity_list = r_loc.get_link(0).capacity_list
        self.o_capacity_list = o_loc.get_link(0).capacity_list
        self.p_capacity_list = p_loc.get_link(0).capacity_list
        self.q_capacity_list = q_loc.get_link(0).capacity_list
        self.s_capacity_list = s_loc.get_link(0).capacity_list
        self.comm_capacity_list = self.comm_links.get_link(0).capacity_list

        self.r_cost_list = r_loc.get_link(0).cost_list
        self.o_cost_list = o_loc.get_link(0).cost_list
        self.p_cost_list = p_loc.get_link(0).cost_list
        self.q_cost_list = q_loc.get_link(0).cost_list
        self.s_cost_list = s_loc.get_link(0).cost_list
        self.comm_cost_list = self.comm_links.get_link(0).cost_list

        self.r_capacity_num = len(self.r_capacity_list)
        self.o_capacity_num = len(self.o_capacity_list)
        self.p_capacity_num = len(self.p_capacity_list)
        self.q_capacity_num = len(self.q_capacity_list)
        self.s_capacity_num = len(self.s_capacity_list)
        self.comm_capacity_num = len(self.comm_links.get_link(0).capacity_list)

    def initialize_decision_variables(self):
        self.alpha_r, self.palpha_r = np.zeros((self.r_loc_num, self.r_capacity_num)), np.zeros((self.r_loc_num, self.r_capacity_num))
        self.alpha_o, self.palpha_o = np.zeros((self.o_loc_num, self.o_capacity_num)), np.zeros((self.o_loc_num, self.o_capacity_num))
        self.alpha_p, self.palpha_p = np.zeros((self.p_loc_num, self.p_capacity_num)), np.zeros((self.p_loc_num, self.p_capacity_num))
        self.alpha_q, self.palpha_q = np.zeros((self.q_loc_num, self.q_capacity_num)), np.zeros((self.q_loc_num, self.q_capacity_num))
        self.alpha_s, self.palpha_s = np.zeros((self.s_loc_num, self.s_capacity_num)), np.zeros((self.s_loc_num, self.s_capacity_num))
        self.beta, self.pbeta = np.zeros((self.comm_link_num, self.comm_capacity_num)), np.zeros((self.comm_link_num, self.comm_capacity_num))
        self.g_r, self.pg_r = np.zeros(self.r_loc_num), np.zeros(self.r_loc_num)
        self.c_r, self.pc_r = np.zeros(self.r_loc_num), np.zeros(self.r_loc_num)
        self.g_o, self.pg_o = np.zeros(self.o_loc_num), np.zeros(self.o_loc_num)
        self.c_o, self.pc_o = np.zeros(self.o_loc_num), np.zeros(self.o_loc_num)
        self.g_p, self.pg_p = np.zeros(self.p_loc_num), np.zeros(self.p_loc_num)
        self.c_p, self.pc_p = np.zeros(self.p_loc_num), np.zeros(self.p_loc_num)
        self.g_s, self.pg_s = np.zeros(self.s_loc_num), np.zeros(self.s_loc_num)
        self.c_s, self.pc_s = np.zeros(self.s_loc_num), np.zeros(self.s_loc_num)
        self.g_q, self.pg_q = np.zeros(self.q_loc_num), np.zeros(self.q_loc_num)
        self.c_q, self.pc_q = np.zeros(self.q_loc_num), np.zeros(self.q_loc_num)
        self.f_c, self.pf_c = np.zeros(self.comm_link_num), np.zeros(self.comm_link_num)
        self.F_c, self.pF_c = np.zeros(self.comm_link_num), np.zeros(self.comm_link_num)
    
    def initialize_lr_multiplier(self):
        init_value = 0.1

        self.mu1 = np.full(self.r_loc_num, init_value, dtype='float16')
        self.mu2 = np.full(self.o_loc_num, init_value, dtype='float16')
        self.mu3 = np.full(self.p_loc_num, init_value, dtype='float16')
        self.mu4 = np.full(self.s_loc_num, init_value, dtype='float16')
        self.mu5 = np.full(self.q_loc_num, init_value, dtype='float16')
        self.mu6 = np.full(self.comm_link_num, init_value, dtype='float16')
        self.mu7 = np.full(self.r_loc_num, init_value, dtype='float16')
        self.mu8 = np.full(self.o_loc_num, init_value, dtype='float16')
        self.mu9 = np.full(self.p_loc_num, init_value, dtype='float16')
        self.mu10 = np.full(self.s_loc_num, init_value, dtype='float16')
        self.mu11 = np.full(self.q_loc_num, init_value, dtype='float16')
        self.mu12 = np.full(self.comm_link_num, init_value, dtype='float16')
        self.mu13 = np.full((self.o_loc_num+self.p_loc_num+self.q_loc_num+self.comm_link_num, self.userpair_num), init_value, dtype='float16')
        # mu13[o, p, q, comm][w]
        self.mu14 = init_value
        self.mu15 = init_value
        self.mu16 = init_value
        self.mu17 = init_value
        self.mu18 = init_value


    def solve_sub1(self):
        sub1_ans = 0
        for i in range(self.r_loc_num):
            coef = np.zeros(self.r_capacity_num)
            for j in range(self.r_capacity_num):
                coef[j] = self.r_cost_list[j] - self.mu7[i] * self.r_capacity_list[j]
            min_coef_idx = np.argmin(coef)
            min_coef_val = coef[min_coef_idx]
            self.alpha_r[i][min_coef_idx] = 1      # 因為 sum alpha = 1 找係數最小的 alpha 設為1，其餘為0
            #print(self.alpha_r[i])
            sub1_ans += coef[min_coef_idx] * self.alpha_r[i][min_coef_idx]   # mu7 無值域限制

        print("Subproblem 1 solved! value: ", sub1_ans) 
        return sub1_ans

    def solve_sub2(self):
        sub2_ans = 0
        # self.alpha_o.fill(0)

        for i in range(self.o_loc_num):
            coef = np.zeros(self.o_capacity_num)
            for j in range(self.o_capacity_num):
                coef[j] = self.o_cost_list[j] - self.mu8[i] * self.o_capacity_list[j] - self.mu14
            min_coef_idx = np.argmin(coef)
            min_coef_val = coef[min_coef_idx]
            self.alpha_o[i][min_coef_idx] = 1
            sub2_ans += coef[min_coef_idx] * self.alpha_o[i][min_coef_idx]
        
        print("Subproblem 2 solved! value: ", sub2_ans)
        return sub2_ans

    def solve_sub3(self):
        sub3_ans = 0
        #self.alpha_p.fill(0)
        
        for i in range(self.p_loc_num):
            coef = np.zeros(self.p_capacity_num)
            for j in range(self.p_capacity_num):
                coef[j] = self.p_cost_list[j] - self.mu9[i] * self.p_capacity_list[j] - self.mu15
            min_coef_idx = np.argmin(coef)
            min_coef_val = coef[min_coef_idx]
            self.alpha_p[i][min_coef_idx] = 1
            sub3_ans += coef[min_coef_idx] * self.alpha_p[i][min_coef_idx]
        
        print("Subproblem 3 solved! value: ", sub3_ans)
        return sub3_ans

    def solve_sub4(self):
        sub4_ans = 0
        #self.alpha_s.fill(0)

        for i in range(self.s_loc_num):
            coef = np.zeros(self.s_capacity_num)
            for j in range(self.s_capacity_num):
                coef[j] = self.s_cost_list[j] - self.mu10[i] * self.s_capacity_list[j] - self.mu16
            min_coef_idx = np.argmin(coef)
            min_coef_val = coef[min_coef_idx]
            self.alpha_s[i][min_coef_idx] = 1
            sub4_ans += coef[min_coef_idx] * self.alpha_s[i][min_coef_idx]
        
        print("Subproblem 4 solved! value: ", sub4_ans)
        return sub4_ans

    def solve_sub5(self):
        sub5_ans = 0
        #self.alpha_q.fill(0)

        for i in range(self.q_loc_num):
            coef = np.zeros(self.q_capacity_num)
            for j in range(self.q_capacity_num):
                coef[j] = self.q_cost_list[j] - self.mu11[i] * self.q_capacity_list[j] - self.mu17
            min_coef_idx = np.argmin(coef)
            min_coef_val = coef[min_coef_idx]
            self.alpha_q[i][min_coef_idx] = 1
            sub5_ans += coef[min_coef_idx] * self.alpha_q[i][min_coef_idx]

        print("Subproblem 5 solved! value: ", sub5_ans)
        return sub5_ans
    # g_r, C_r
    def solve_sub6(self):
        sub6_ans = 0
        # self.g_r.fill(0)
        # self.c_r.fill(0)

        for i in range(self.r_loc_num):
            coef = np.zeros(self.r_capacity_num)
            g = np.zeros(self.r_capacity_num)
            for j in range(self.r_capacity_num):
                capacity = self.r_capacity_list[j]
                if j == 0: # capacity 為 0 時, set c and g to 0   現在cpacity = 0時cost不為0
                    # g[j] = 0
                    # coef[j] = 0
                    continue
                if self.mu1[i] * self.gamma == 0:
                    g_value = 0
                else:
                    g_value = ((self.mu1[i] * self.gamma - self.mu18) * capacity) / (self.mu1[i] * self.gamma)
                if g_value >= 0 and g_value <= self.ro * capacity:
                    # coefficient
                    coef_0 = (-self.mu1[i]) * g_value + self.mu7[i] * capacity + ((self.mu18 * g_value) / (self.gamma * (capacity - g_value)))
                    # end point: g_value = 0
                    coef_p1 = self.mu7[i] * capacity
                    # end point: g_value = ro*capacity
                    coef_p2 = (-self.mu1[i] * self.ro + self.mu7[i]) * capacity + (self.mu18 * self.ro) / (self.gamma * (1 - self.ro))
                    coef_value = np.zeros(3)
                    coef_value[0] = coef_0
                    coef_value[1] = coef_p1
                    coef_value[2] = coef_p2
                    g_values = np.zeros(3)
                    g_values[0] = g_value
                    g_values[1] = 0
                    g_values[2] = self.ro * capacity
                    min_idx = np.argmin(coef_value)
                    coef[j] = coef_value[min_idx]
                    g[j] = g_values[min_idx]
                else:
                    # g_value = 0
                    coef_1 = self.mu7[i] * capacity
                    # g_value = ro*capacity
                    coef_2 = (-self.mu1[i] * self.ro + self.mu7[i]) * capacity + (self.mu18 * self.ro) / (self.gamma * (1 - self.ro))
                    if coef_1 < coef_2:
                        coef[j] = coef_1
                        g[j] = 0
                    else:
                        coef[j] = coef_2
                        g[j] = self.ro * capacity
            min_coef_idx = np.argmin(coef)
            self.c_r[i] = self.r_capacity_list[min_coef_idx]
            self.g_r[i] = g[min_coef_idx]
            sub6_ans += coef[min_coef_idx]
        # 常數項
        #sub6_ans -= self.mu18 * self.delay_toler 
        print("Subproblem 6 solved! value: ", sub6_ans)
        # print(self.c_r)
        return sub6_ans
    # g_o, C_o
    def solve_sub7(self):
        sub7_ans = 0
        # self.g_o.fill(0)
        # self.c_o.fill(0)

        for i in range(self.o_loc_num):
            coef = np.zeros(self.o_capacity_num)
            g = np.zeros(self.o_capacity_num)
            for j in range(self.o_capacity_num):
                capacity = self.o_capacity_list[j]
                if j == 0:
                    # g[j] = 0
                    # coef[j] = 0
                    continue
                if self.mu2[i] * self.gamma == 0:
                    g_value = 0
                else:
                    g_value = ((self.mu2[i] * self.gamma - self.mu18) * capacity) / (self.mu2[i] * self.gamma)
                if g_value >= 0 and g_value <= self.ro * capacity:
                    # coefficient
                    coef_0 = (-self.mu2[i]) * g_value + self.mu8[i] * capacity + ((self.mu18 * g_value) / (self.gamma * (capacity - g_value)))
                    # end point: g_value = 0
                    coef_p1 = self.mu8[i] * capacity
                    # end point: g_value = ro*capacity
                    coef_p2 = (-self.mu2[i] * self.ro + self.mu8[i]) * capacity + (self.mu18 * self.ro) / (self.gamma * (1 - self.ro))
                    coef_value = np.zeros(3)
                    coef_value[0] = coef_0
                    coef_value[1] = coef_p1
                    coef_value[2] = coef_p2
                    g_values = np.zeros(3)
                    g_values[0] = g_value
                    g_values[1] = 0
                    g_values[2] = self.ro * capacity
                    min_idx = np.argmin(coef_value)
                    coef[j] = coef_value[min_idx]
                    g[j] = g_values[min_idx]
                else:
                    # g_value = 0
                    coef_1 = self.mu8[i] * capacity
                    # g_value = ro * capacity
                    coef_2 = (-self.mu2[i] * self.ro + self.mu8[i]) * capacity + ((self.mu18 * self.ro) / (self.gamma * (1 - self.ro)))
                    if coef_1 < coef_2:
                        coef[j] = coef_1
                        g[j] = 0
                    else:
                        coef[j] = coef_2
                        g[j] = self.ro * capacity
            min_coef_idx = np.argmin(coef)
            self.c_o[i] = self.o_capacity_list[min_coef_idx]
            self.g_o[i] = g[min_coef_idx]
            sub7_ans += coef[min_coef_idx]
        # 常數項
        #sub7_ans -= self.mu18 * self.delay_toler
        print("subproblem 7 solved! value: ", sub7_ans)
        return sub7_ans 
    # g_p, c_p
    def solve_sub8(self):
        sub8_ans = 0
        # self.g_p.fill(0)
        # self.c_p.fill(0)

        for i in range(self.p_loc_num):
            coef = np.zeros(self.p_capacity_num)
            g = np.zeros(self.p_capacity_num)
            for j in range(self.p_capacity_num):
                capacity = self.p_capacity_list[j]
                if j == 0:
                    # g[j] = 0
                    # coef[j] = 0
                    continue
                if self.mu3[i] * self.gamma == 0:
                    g_value = 0
                else:
                    g_value = ((self.mu3[i] * self.gamma - self.mu18) * capacity) / (self.mu3[i] * self.gamma)
                if g_value >= 0 and g_value <= self.ro * capacity:
                    # coefficient
                    coef_0 = (-self.mu3[i]) * g_value + self.mu9[i] * capacity + ((self.mu18 * g_value) / (self.gamma * (capacity - g_value)))
                    # end point: g_value = 0
                    coef_p1 = self.mu9[i] * capacity
                    # end point: g_value = ro*capacity
                    coef_p2 = (-self.mu3[i] * self.ro + self.mu9[i]) * capacity + (self.mu18 * self.ro) / (self.gamma * (1 - self.ro))
                    coef_value = np.zeros(3)
                    coef_value[0] = coef_0
                    coef_value[1] = coef_p1
                    coef_value[2] = coef_p2
                    g_values = np.zeros(3)
                    g_values[0] = g_value
                    g_values[1] = 0
                    g_values[2] = self.ro * capacity
                    min_idx = np.argmin(coef_value)
                    coef[j] = coef_value[min_idx]
                    g[j] = g_values[min_idx]
                else:
                    # g_value = 0
                    coef_1 = self.mu9[i] * capacity
                    # g_value = ro * capacity
                    coef_2 = (-self.mu3[i] * self.ro + self.mu9[i]) * capacity + ((self.mu18 * self.ro) / (self.gamma * (1 - self.ro)))
                    if coef_1 < coef_2:
                        coef[j] = coef_1
                        g[j] = 0
                    else:
                        coef[j] = coef_2
                        g[j] = self.ro * capacity
            min_coef_idx = np.argmin(coef)
            self.c_p[i] = self.p_capacity_list[min_coef_idx]
            self.g_p[i] = g[min_coef_idx]
            sub8_ans += coef[min_coef_idx]
        #sub8_ans -= self.mu18 * self.delay_toler
        print("subproblem 8 solved! value: ", sub8_ans)
        return sub8_ans    
    # g_s, c_s
    def solve_sub9(self):
        sub9_ans = 0
        # self.g_s.fill(0)
        # self.c_s.fill(0)

        for i in range(self.s_loc_num):
            coef = np.zeros(self.s_capacity_num)
            g = np.zeros(self.s_capacity_num)
            for j in range(self.s_capacity_num):
                capacity = self.s_capacity_list[j]
                if j == 0:
                    # g[j] = 0
                    # coef[j] = 0
                    continue
                if self.mu4[i] * self.gamma == 0:
                    g_value = 0
                else:
                    g_value = ((self.mu4[i] * self.gamma - self.mu18) * capacity) / (self.mu4[i] * self.gamma)
                if g_value >= 0 and g_value <= self.ro * capacity:
                    # coefficient
                    coef_0 = (-self.mu4[i]) * g_value + self.mu10[i] * capacity + ((self.mu18 * g_value) / (self.gamma * (capacity - g_value)))
                    # end point: g_value = 0
                    coef_p1 = self.mu10[i] * capacity
                    # end point: g_value = ro*capacity
                    coef_p2 = (-self.mu4[i] * self.ro + self.mu10[i]) * capacity + (self.mu18 * self.ro) / (self.gamma * (1 - self.ro))
                    coef_value = np.zeros(3)
                    coef_value[0] = coef_0
                    coef_value[1] = coef_p1
                    coef_value[2] = coef_p2
                    g_values = np.zeros(3)
                    g_values[0] = g_value
                    g_values[1] = 0
                    g_values[2] = self.ro * capacity
                    min_idx = np.argmin(coef_value)
                    coef[j] = coef_value[min_idx]
                    g[j] = g_values[min_idx]
                else:
                    # g_value = 0
                    coef_1 = self.mu10[i] * capacity
                    # g_value = ro * capacity
                    coef_2 = (-self.mu4[i] * self.ro + self.mu10[i]) * capacity + ((self.mu18 * self.ro) / (self.gamma * (1 - self.ro)))
                    if coef_1 < coef_2:
                        coef[j] = coef_1
                        g[j] = 0
                    else:
                        coef[j] = coef_2
                        g[j] = self.ro * capacity
            min_coef_idx = np.argmin(coef)
            self.c_s[i] = self.s_capacity_list[min_coef_idx]
            self.g_s[i] = g[min_coef_idx]
            sub9_ans += coef[min_coef_idx]
        #sub9_ans -= self.mu18 * self.delay_toler
        print("subproblem 9 solved! value: ", sub9_ans)
        return sub9_ans    
    # g_q, c_q   
    def solve_sub10(self):
        sub10_ans = 0
        # self.g_q.fill(0)
        # self.c_q.fill(0)

        for i in range(self.q_loc_num):
            coef = np.zeros(self.q_capacity_num)
            g = np.zeros(self.q_capacity_num)
            for j in range(self.q_capacity_num):
                capacity = self.q_capacity_list[j]
                if j == 0:
                    # g[j] = 0
                    # coef[j] = 0
                    continue
                if self.mu5[i] * self.gamma == 0:
                    g_value = 0
                else:
                    g_value = ((self.mu5[i] * self.gamma - self.mu18) * capacity) / (self.mu5[i] * self.gamma)
                if g_value >= 0 and g_value <= self.ro * capacity:
                    # coefficient
                    coef_0 = (-self.mu5[i]) * g_value + self.mu11[i] * capacity + ((self.mu18 * g_value) / (self.gamma * (capacity - g_value)))
                    # end point: g_value = 0
                    coef_p1 = self.mu11[i] * capacity
                    # end point: g_value = ro*capacity
                    coef_p2 = (-self.mu5[i] * self.ro + self.mu11[i]) * capacity + (self.mu18 * self.ro) / (self.gamma * (1 - self.ro))
                    coef_value = np.zeros(3)
                    coef_value[0] = coef_0
                    coef_value[1] = coef_p1
                    coef_value[2] = coef_p2
                    g_values = np.zeros(3)
                    g_values[0] = g_value
                    g_values[1] = 0
                    g_values[2] = self.ro * capacity
                    min_idx = np.argmin(coef_value)
                    coef[j] = coef_value[min_idx]
                    g[j] = g_values[min_idx]
                else:
                    # g_value = 0
                    coef_1 = self.mu11[i] * capacity
                    # g_value = ro * capacity
                    coef_2 = (-self.mu5[i] * self.ro + self.mu11[i]) * capacity + ((self.mu18 * self.ro) / (self.gamma * (1 - self.ro)))
                    if coef_1 < coef_2:
                        coef[j] = coef_1
                        g[j] = 0
                    else:
                        coef[j] = coef_2
                        g[j] = self.ro * capacity
            min_coef_idx = np.argmin(coef)
            self.c_q[i] = self.q_capacity_list[min_coef_idx]
            self.g_q[i] = g[min_coef_idx]
            sub10_ans += coef[min_coef_idx]
        #sub10_ans -= self.mu18 * self.delay_toler
        print("subproblem 10 solved! value: ", sub10_ans)
        return sub10_ans    
    # beta_{mnk}
    def solve_sub11(self): 
        sub11_ans = 0
        #self.beta.fill(0)

        for i in range(self.comm_link_num):
            coef = np.zeros(self.comm_capacity_num)
            for j in range(self.comm_capacity_num):
                coef[j] = self.comm_cost_list[j] - self.mu12[i] * self.comm_capacity_list[j]
            min_coef_idx = np.argmin(coef)
            min_coef_val = coef[min_coef_idx]
            self.beta[i][min_coef_idx] = 1
            sub11_ans += coef[min_coef_idx] * self.beta[i][min_coef_idx]
        print("Subproblem 11 solved! value: ", sub11_ans)
        return sub11_ans    
    # f_c, F_c
    def solve_sub12(self):
        sub12_ans = 0
        # self.f_c.fill(0)
        # self.F_c.fill(0)

        for i in range(self.comm_link_num):
            coef = np.zeros(self.comm_capacity_num)
            f = np.zeros(self.comm_capacity_num)
            for j in range(self.comm_capacity_num):
                capacity = self.comm_capacity_list[j]
                if j == 0:
                    # f[j] = 0
                    # coef[j] = 0
                    continue
                if self.mu6[i] * self.gamma == 0:
                    f_value = 0
                else:
                    f_value = ((self.mu6[i] * self.gamma - self.mu18) * capacity) / (self.mu6[i] * self.gamma)
                if f_value >= 0 and f_value <= self.ro * capacity:
                    # coefficient
                    coef_0 = -self.mu6[i] * f_value + self.mu12[i] * capacity + ((self.mu18 * f_value) / (self.gamma * (capacity - f_value)))
                    # end point: g_value = 0
                    coef_p1 = self.mu12[i] * capacity
                    # end point: g_value = ro*capacity
                    coef_p2 = (-self.mu6[i] * self.ro + self.mu12[i]) * capacity + ((self.mu18 * self.ro) / (self.gamma * (1 - self.ro)))
                    coef_value = np.zeros(3)
                    coef_value[0] = coef_0
                    coef_value[1] = coef_p1
                    coef_value[2] = coef_p2
                    f_values = np.zeros(3)
                    f_values[0] = f_value
                    f_values[1] = 0
                    f_values[2] = self.ro * capacity
                    min_idx = np.argmin(coef_value)
                    coef[j] = coef_value[min_idx]
                    f[j] = f_values[min_idx]
                else:
                    # f_value = 0
                    coef_1 = self.mu12[i] * capacity
                    # f_value = ro * capacity
                    coef_2 = (-self.mu6[i] * self.ro + self.mu12[i]) * capacity + ((self.mu18 * self.ro) / (self.gamma * (1 - self.ro)))
                    if coef_1 < coef_2:
                        coef[j] = coef_1
                        f[j] = 0
                    else:
                        coef[j] = coef_2
                        f[j] = self.ro * capacity
            min_coef_idx = np.argmin(coef)
            self.F_c[i] = self.comm_capacity_list[min_coef_idx]
            self.f_c[i] = f[min_coef_idx]
            sub12_ans += coef[min_coef_idx]
        #sub12_ans -= self.mu18 * self.delay_toler
        print("subproblem 12 solved! value: ", sub12_ans)
        return sub12_ans
    # xp  
    def solve_sub13(self):
        sub13_ans = 0
        #coef = np.zeros(self.userpair_num)

        for w in range(self.userpair_num):
            traffic = self.pairset.get_pair(w).traffic
            path_number = self.pairset.get_pair(w).path_number
            for p in range(path_number):
                path = self.pairset.get_pair(w).path_set.get_path(p)
                for r in range(self.r_loc_num):    # mu1
                    if self.r_loc.get_link(r) in path.node_list:
                        sub13_ans += self.mu1[r] * traffic
                for o in range(self.o_loc_num):    # mu2
                    if self.o_loc.get_link(o) in path.node_list:
                        # coef[w] += self.mu2[o] * traffic
                        # coef[w] += self.mu13[o][w]
                        sub13_ans += self.mu2[o] * traffic
                        sub13_ans += self.mu13[o][w]
                for p in range(self.p_loc_num):    # mu3
                    if self.p_loc.get_link(p) in path.node_list:
                        # coef[w] += self.mu3[p] * traffic
                        # coef[w] += self.mu13[self.o_loc_num+p][w]
                        sub13_ans += self.mu3[p] * traffic
                        sub13_ans += self.mu13[self.o_loc_num+p][w]
                for s in range(self.s_loc_num):    # mu4
                    if self.s_loc.get_link(s) in path.node_list:
                        # coef[w] += self.mu4[s] * traffic
                        sub13_ans += self.mu4[s] * traffic
                for q in range(self.q_loc_num):    # mu5
                    if self.q_loc.get_link(q) in path.node_list:
                        # coef[w] += self.mu5[q] * traffic
                        # coef[w] += self.mu13[self.o_loc_num+self.p_loc_num+q][w]
                        sub13_ans += self.mu5[q] * traffic
                        sub13_ans += self.mu13[self.o_loc_num+self.p_loc_num+q][w]
                for c in range(self.comm_link_num):    # mu6
                    if self.comm_links.get_link(c) in path.link_list:
                        # coef[w] += self.mu6[c] * traffic
                        # coef[w] += self.mu13[self.o_loc_num + self.p_loc_num + self.q_loc_num + c][w]
                        sub13_ans += self.mu6[c] * traffic
                        sub13_ans += self.mu13[self.o_loc_num + self.p_loc_num + self.q_loc_num + c][w]

        print("Subproblem 13 solved! value: ", sub13_ans)
        print('\n')
        return sub13_ans
    
    def constant_value(self):
        value = 0
        for r in range(self.r_loc_num):
            for k in range(self.r_capacity_num):
                value += self.alpha_r[r][k] * self.r_capacity_list[k]
        for o in range(self.o_loc_num):
            for k in range(self.o_capacity_num):
                value += self.alpha_o[o][k] * self.o_capacity_list[k]
        for p in range(self.p_loc_num):
            for k in range(self.p_capacity_num):
                value += self.alpha_p[p][k] * self.p_capacity_list[k]
        for s in range(self.s_loc_num):
            for k in range(self.s_capacity_num):
                value += self.alpha_s[s][k] * self.s_capacity_list[k]
        for q in range(self.q_loc_num):
            for k in range(self.q_capacity_num):
                value += self.alpha_q[q][k] * self.q_capacity_list[k]
        for c in range(self.comm_link_num):
            for k in range(self.comm_capacity_num):
                value += self.beta[c][k] * self.comm_capacity_list[k]
        
        for w in range(self.userpair_num):
            for i in range(self.o_loc_num + self.p_loc_num + self.q_loc_num + self.comm_link_num):
                value -= self.mu13[i][w]

        value -= self.mu18 * self.delay_toler
        return value
    
    def initialize(self):    
        initialized_Z_star = 0

        # self.alpha_r[::, 1] = 1
        # self.alpha_o[::, 1] = 1
        # self.alpha_p[::, 1] = 1
        # self.alpha_q[::, 1] = 1
        # self.alpha_s[::, 1] = 1
        # self.beta[::, 1] = 1

        node_traffic = {}
        link_traffic = {}
        
        # Union all paths
        for userpair in self.pairset.pairs:
            for path in userpair.path_set.paths:
                for node in path.node_list:
                    if node not in node_traffic:
                        node_traffic[node] = userpair.traffic
                    else:
                        node_traffic[node] += userpair.traffic
                for link in path.link_list:
                    if link not in link_traffic:
                        link_traffic[link] = userpair.traffic
                    else:
                        link_traffic[link] += userpair.traffic

        for node in node_traffic.keys():
            if node.node1.type == 'r':
                node_id = self.r_loc.find_link(node)
                given_value = node_traffic[node]
                #print(given_value)
                capacity_value = min(filter(lambda x: x > given_value, self.r_capacity_list))
                idx = self.r_capacity_list.index(capacity_value)
                # self.alpha_r[node_id, ::] = 0
                self.alpha_r[node_id][idx] = 1
            elif node.node1.type == 'o':
                node_id = self.o_loc.find_link(node)
                given_value = node_traffic[node]
                #print(given_value)
                capacity_value = min(filter(lambda x: x > given_value, self.o_capacity_list))
                idx = self.o_capacity_list.index(capacity_value)
                # self.alpha_p[node_id, ::] = 0
                self.alpha_p[node_id][idx] = 1
            elif node.node1.type == 's':
                node_id = self.s_loc.find_link(node)
                given_value = node_traffic[node]
                #print(given_value)
                capacity_value = min(filter(lambda x: x > given_value, self.s_capacity_list))
                idx = self.s_capacity_list.index(capacity_value)
                # self.alpha_s[node_id, ::] = 0
                self.alpha_s[node_id][idx] = 1
            else:
                node_id = self.q_loc.find_link(node)
                given_value = node_traffic[node]
                capacity_value = min(filter(lambda x: x > given_value, self.q_capacity_list))
                idx = self.q_capacity_list.index(capacity_value)
                # self.alpha_q[node_id, ::] = 0
                self.alpha_q[node_id][idx] = 1

        for link in link_traffic.keys():
                link_id = self.comm_links.find_link(link)
                given_value = link_traffic[link]
                #print(given_value)
                capacity_value = min(filter(lambda x: x > given_value, self.comm_capacity_list))
                idx = self.comm_capacity_list.index(capacity_value)
                # self.beta[link_id, ::] = 0
                self.beta[link_id][idx] = 1
                       
        # compute initialize Z*
        for r in range(self.r_loc_num):
            for k in range(self.r_capacity_num):
                initialized_Z_star += self.alpha_r[r][k] * self.r_cost_list[k]
        for o in range(self.o_loc_num):
            for k in range(self.o_capacity_num):
                initialized_Z_star += self.alpha_o[o][k] * self.o_cost_list[k]
        for p in range(self.p_loc_num):
            for k in range(self.p_capacity_num):
                initialized_Z_star += self.alpha_p[p][k] * self.p_cost_list[k]
        for s in range(self.s_loc_num):
            for k in range(self.s_capacity_num):
                initialized_Z_star += self.alpha_s[s][k] * self.s_cost_list[k]
        for q in range(self.q_loc_num):
            for k in range(self.q_capacity_num):
                initialized_Z_star += self.alpha_q[q][k] * self.q_cost_list[k]
        for c in range(self.comm_link_num):
            for k in range(self.comm_capacity_num):
                initialized_Z_star += self.beta[c][k] * self.comm_cost_list[k]

        self.initialize_decision_variables()

        return initialized_Z_star   # Since dual problem is a MAXIMUM problem
    
    def primal(self):    
        primal_ans = 0

        node_traffic = {}
        link_traffic = {}
        deployed_node = []
        node_level = []
        deployed_link = []
        link_level = []

        for userpair in self.pairset.pairs:
            for path in userpair.path_set.paths:
                for node in path.node_list:
                    if node not in node_traffic:
                        node_traffic[node] = userpair.traffic
                    else:
                        node_traffic[node] += userpair.traffic
                for link in path.link_list:
                    if link not in link_traffic:
                        link_traffic[link] = userpair.traffic
                    else:
                        link_traffic[link] += userpair.traffic      
            
        for node in node_traffic.keys():
            if node.node1.type == 'r':
                node_id = self.r_loc.find_link(node)
                deployed_node.append(node.node1.id)
                given_value = node_traffic[node]
                capacity_value = min(filter(lambda x: x > given_value, self.r_capacity_list))
                idx = self.r_capacity_list.index(capacity_value)
                node_level.append(idx)
                self.palpha_r[node_id][idx] = 1
            elif node.node1.type == 'o':
                node_id = self.o_loc.find_link(node)
                deployed_node.append(node.node1.id)
                given_value = node_traffic[node]
                capacity_value = min(filter(lambda x: x > given_value, self.o_capacity_list))
                idx = self.o_capacity_list.index(capacity_value)
                node_level.append(idx)
                self.palpha_o[node_id][idx] = 1
            elif node.node1.type == 'p':
                node_id = self.p_loc.find_link(node)
                deployed_node.append(node.node1.id)
                given_value = node_traffic[node]
                capacity_value = min(filter(lambda x: x > given_value, self.p_capacity_list))
                idx = self.p_capacity_list.index(capacity_value)
                node_level.append(idx)
                self.palpha_p[node_id][idx] = 1
            elif node.node1.type == 's':
                node_id = self.s_loc.find_link(node)
                deployed_node.append(node.node1.id)
                given_value = node_traffic[node]
                capacity_value = min(filter(lambda x: x > given_value, self.s_capacity_list))
                idx = self.s_capacity_list.index(capacity_value)
                node_level.append(idx)
                self.palpha_s[node_id][idx] = 1
            else:
                node_id = self.q_loc.find_link(node)
                deployed_node.append(node.node1.id)
                given_value = node_traffic[node]
                capacity_value = min(filter(lambda x: x > given_value, self.q_capacity_list))
                idx = self.q_capacity_list.index(capacity_value)
                node_level.append(idx)
                self.palpha_q[node_id][idx] = 1

        for link in link_traffic.keys():
            link_id = self.comm_links.find_link(link)
            deployed_link.append(link_id)
            given_value = link_traffic[link]
            capacity_value = min(filter(lambda x: x > given_value, self.comm_capacity_list))
            idx = self.comm_capacity_list.index(capacity_value)
            link_level.append(idx)
            self.pbeta[link_id][idx] = 1
    
        for r in range(self.r_loc_num):
            for k in range(self.r_capacity_num):
                primal_ans += self.palpha_r[r][k] * self.r_cost_list[k]
        for o in range(self.o_loc_num):
            for k in range(self.o_capacity_num):
                primal_ans += self.palpha_o[o][k] * self.o_cost_list[k]
        for p in range(self.p_loc_num):
            for k in range(self.p_capacity_num):
                primal_ans += self.palpha_p[p][k] * self.p_cost_list[k]
        for s in range(self.s_loc_num):
            for k in range(self.s_capacity_num):
                primal_ans += self.palpha_s[s][k] * self.s_cost_list[k]
        for q in range(self.q_loc_num):
            for k in range(self.q_capacity_num):
                primal_ans += self.palpha_q[q][k] * self.q_cost_list[k]
        for c in range(self.comm_link_num):
            for k in range(self.comm_capacity_num):
                primal_ans += self.pbeta[c][k] * self.comm_cost_list[k]
        return primal_ans, deployed_node, deployed_link, node_level, link_level
 
    def adjust_multiplier(self, lambda_value, Z_star, Zd):    # prepare for denominator
        dominator = 0
        # tmp1
        for r in range(self.r_loc_num):
            node = self.r_loc.get_link(r)
            tmp1 = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp1 += traffic
            tmp1 -= self.g_r[r]
            dominator += math.pow(tmp1, 2)
        # tmp2
        for o in range(self.o_loc_num):
            node = self.o_loc.get_link(o)
            tmp2 = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp2 += traffic
            tmp2 -= self.g_o[o]
            dominator += math.pow(tmp2, 2)
        # tmp3
        for p_idx in range(self.p_loc_num):
            node = self.p_loc.get_link(p_idx)
            tmp3 = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp3 += traffic
            tmp3 -= self.g_p[p_idx]
            dominator += math.pow(tmp3, 2)
        # tmp4
        for s in range(self.s_loc_num):
            node = self.s_loc.get_link(s)
            tmp4 = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp4 += traffic
            tmp4 -= self.g_s[s]
            dominator += math.pow(tmp4, 2)
        # tmp5
        for q in range(self.q_loc_num):
            node = self.q_loc.get_link(q)
            tmp5 = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp5 += traffic
            tmp5 -= self.g_q[q]
            dominator += math.pow(tmp5, 2)
        # tmp6
        for c in range(self.comm_link_num):
            link = self.comm_links.get_link(c)
            tmp6 = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if link in userpair.path_set.get_path(p).link_list:
                        tmp6 += traffic
            tmp6 -= self.f_c[c]
            dominator += math.pow(tmp6, 2)
        # tmp7
        for r in range(self.r_loc_num):
            node = self.r_loc.get_link(r)
            tmp7 = 0
            tmp7 += self.c_r[r]
            for k in range(self.r_capacity_num):
                tmp7 -= self.alpha_r[r][k]*self.r_capacity_list[k]
            dominator += math.pow(tmp7, 2)
        # tmp8
        for o in range(self.o_loc_num):
            node = self.o_loc.get_link(o)
            tmp8 = 0
            tmp8 += self.c_o[o]
            for k in range(self.o_capacity_num):
                tmp8 -= self.alpha_o[o][k]*self.o_capacity_list[k]
            dominator += math.pow(tmp8, 2)
        # tmp9
        for p in range(self.p_loc_num):
            node = self.p_loc.get_link(p)
            tmp9 = 0
            tmp9 += self.c_p[p]
            for k in range(self.p_capacity_num):
                tmp9 -= self.alpha_p[p][k]*self.p_capacity_list[k]
            dominator += math.pow(tmp9, 2)
        # tmp10
        for s in range(self.s_loc_num):
            node = self.s_loc.get_link(s)
            tmp10 = 0
            tmp10 += self.c_s[s]
            for k in range(self.s_capacity_num):
                tmp10 -= self.alpha_s[s][k]*self.s_capacity_list[k]
            dominator += math.pow(tmp10, 2)
        # tmp11
        for q in range(self.q_loc_num):
            node = self.q_loc.get_link(q)
            tmp11 = 0
            tmp11 += self.c_q[q]
            for k in range(self.q_capacity_num):
                tmp11 -= self.alpha_q[q][k]*self.q_capacity_list[k]
            dominator += math.pow(tmp11, 2)
        # tmp12
        for c in range(self.comm_link_num):
            tmp12 = 0
            tmp12 += self.F_c[c]
            for k in range(self.comm_capacity_num):
                tmp12 -= self.beta[c][k]*self.comm_capacity_list[k]
            dominator += math.pow(tmp12, 2)
        # tmp13
        for i in range(self.r_loc_num, (self.r_loc_num + self.o_loc_num + self.p_loc_num + self.q_loc_num - 1)):   # o, p, q
            if i < self.r_loc_num + self.o_loc_num:   # o
                link = self.o_loc.get_link(i-self.r_loc_num)
            elif i >= self.r_loc_num + self.o_loc_num and i < self.r_loc_num + self.o_loc_num + self.p_loc_num:   # p
                link = self.p_loc.get_link(i-(self.r_loc_num+self.o_loc_num))
            elif i >= self.r_loc_num + self.o_loc_num + self.p_loc_num and i < self.r_loc_num + self.o_loc_num + self.p_loc_num + self.q_loc_num:
                link = self.q_loc.get_link(i-(self.r_loc_num+self.o_loc_num+self.p_loc_num))

            for w in range(self.userpair_num):
                tmp13 = 0
                userpair = self.pairset.get_pair(w)
                path_num = userpair.path_number
                for p in range(path_num):
                    path = userpair.path_set.get_path(p)
                    if link in path.node_list:
                        tmp13 += 1
                tmp13 -= 1  
            dominator += math.pow(tmp13, 2)

        for i in range(self.comm_link_num):    # comm links
            for w in range(self.userpair_num):
                tmp13 = 0
                userpair = self.pairset.get_pair(w)
                path_num = userpair.path_number
                for p in range(path_num):
                    path = userpair.path_set.get_path(p)
                    if link in path.link_list:
                        tmp13 += 1
                tmp13 -= 1  
            dominator += math.pow(tmp13, 2)

        # compute max Fw
        path_nums = np.zeros(self.userpair_num)
        for w in range(self.userpair_num):
            path_nums[w] = self.pairset.get_pair(w).path_number
        max_Fw = np.amax(path_nums)

        # tmp14
        tmp14 = max_Fw
        value = 0
        for o in range(self.o_loc_num):
            for k in range(self.o_capacity_num):
                value += self.alpha_o[o][k]
        tmp14 = tmp14 - value
        dominator += math.pow(tmp14, 2)
        # tmp15
        tmp15 = max_Fw
        value = 0
        for p in range(self.p_loc_num):
            for k in range(self.p_capacity_num):
                value += self.alpha_p[p][k]
        tmp15 = tmp15 - value
        dominator += math.pow(tmp15, 2)
        # tmp16
        tmp16 = max_Fw
        value = 0
        for s in range(self.s_loc_num):
            for k in range(self.s_capacity_num):
                value += self.alpha_s[s][k]
        tmp16 = tmp16 - value
        dominator += math.pow(tmp16, 2)
        # tmp17
        tmp17 = max_Fw
        value = 0
        for q in range(self.q_loc_num):
            for k in range(self.q_capacity_num):
                value += self.alpha_q[q][k]
        tmp17 = tmp17 - value
        dominator += math.pow(tmp17, 2)
        # tmp18 ====================== 未完成 =============================
        tmp18 = 0
        for r in range(self.r_loc_num):
            if self.c_r[r] - self.g_r[r] == 0:
                tmp18 += 0
            else:
                tmp18 += self.g_r[r] / (self.c_r[r] - self.g_r[r])
        for o in range(self.o_loc_num):
            if self.c_o[o] - self.g_o[o] == 0:
                tmp18 += 0
            else:
                tmp18 += self.g_o[o] / (self.c_o[o] - self.g_o[o])
        for p in range(self.p_loc_num):
            if self.c_p[p] - self.g_p[p] == 0:
                tmp18 += 0
            else:
                tmp18 += self.g_p[p] / (self.c_p[p] - self.g_p[p])
        for s in range(self.s_loc_num):
            if self.c_s[s] - self.g_s[s] == 0:
                tmp18 += 0
            else:
                tmp18 += self.g_s[s] / (self.c_s[s] - self.g_s[s])
        # c_q, g_q =========================== 先用 MM1 代替 =====================
        for q in range(self.q_loc_num):
            if self.c_q[q] - self.g_q[q] == 0:
                tmp18 += 0
            else:
                tmp18 += self.g_q[q] / (self.c_q[q] - self.g_q[q])
        for c in range(self.comm_link_num):
            if self.F_c[c] - self.f_c[c] == 0:
                tmp18 += 0
            else:
                tmp18 += self.f_c[c] / (self.F_c[c] - self.f_c[c])
        tmp18 /= self.gamma
        tmp18 -= self.delay_toler
        dominator += math.pow(tmp18, 2)

        for c in range(self.comm_link_num):
            if self.F_c[c] - self.f_c[c] == 0:
                tmp18 += 0
            else:
                tmp18 += self.f_c[c] / (self.F_c[c] - self.f_c[c])
        tmp18 = tmp18 / self.gamma
        tmp18 -= self.delay_toler
        dominator += math.pow(tmp18, 2)

        # Compute step size
        step_size = lambda_value * (Z_star - Zd) / dominator

        # ========================================= Update ===========================================
        # mu1
        for r in range(self.r_loc_num):
            node = self.r_loc.get_link(r)
            tmp = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp += traffic
            tmp -= self.g_r[r]
            self.mu1[r] = max(0, self.mu1[r] + step_size * tmp)
        # mu2
        for o in range(self.o_loc_num):
            node = self.o_loc.get_link(o)
            tmp = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp += traffic
            tmp -= self.g_o[o]
            self.mu2[o] = max(0, self.mu2[o] + step_size * tmp)
        # mu3
        for p_idx in range(self.p_loc_num):
            node = self.p_loc.get_link(p_idx)
            tmp = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp += traffic
            tmp -= self.g_p[p_idx]
            self.mu3[p_idx] = max(0, self.mu3[p_idx] + step_size * tmp)
        # mu4
        for s in range(self.s_loc_num):
            node = self.s_loc.get_link(s)
            tmp = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp += traffic
            tmp -= self.g_s[s]
            self.mu4[s] = max(0, self.mu4[s] + step_size * tmp)
        # mu5
        for q in range(self.q_loc_num):
            node = self.q_loc.get_link(q)
            tmp = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if node in userpair.path_set.get_path(p).node_list:
                        tmp += traffic
            tmp -= self.g_q[q]
            self.mu5[q] = max(0, self.mu5[q] + step_size * tmp)

        # mu6
        for c in range(self.comm_link_num):
            link = self.comm_links.get_link(c)
            tmp = 0
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                traffic = userpair.traffic
                path_num = userpair.path_number
                for p in range(path_num):
                    if link in userpair.path_set.get_path(p).link_list:
                        tmp += traffic
            tmp -= self.f_c[c]
            self.mu6[c] = max(0, self.mu6[c] + step_size * tmp)

        # mu7 (+, 0, -)
        for r in range(self.r_loc_num):
            node = self.r_loc.get_link(r)
            tmp = 0
            tmp += self.c_r[r]
            for k in range(self.r_capacity_num):
                tmp -= self.alpha_r[r][k] * self.r_capacity_list[k]
            self.mu7[r] = self.mu7[r] + step_size * tmp

        # mu8 (+, 0, -)
        for o in range(self.o_loc_num):
            node = self.o_loc.get_link(o)
            tmp = 0
            tmp += self.c_o[o]
            for k in range(self.o_capacity_num):
                tmp -= self.alpha_o[o][k]*self.o_capacity_list[k]
            self.mu8[o] = self.mu8[o] + step_size * tmp

        # mu9 (+, 0, -)
        for p in range(self.p_loc_num):
            node = self.p_loc.get_link(p)
            tmp = 0
            tmp += self.c_p[p]
            for k in range(self.p_capacity_num):
                tmp -= self.alpha_p[p][k]*self.p_capacity_list[k]
            self.mu9[p] = self.mu9[p] + step_size * tmp

        # mu10 (+, 0, -)
        for s in range(self.s_loc_num):
            node = self.s_loc.get_link(s)
            tmp = 0
            tmp += self.c_s[s]
            for k in range(self.s_capacity_num):
                tmp -= self.alpha_s[s][k]*self.s_capacity_list[k]
            self.mu10[s] = self.mu10[s] + step_size * tmp

        # mu11 (+, 0, -)
        for q in range(self.q_loc_num):
            node = self.q_loc.get_link(q)
            tmp = 0
            tmp += self.c_q[q]
            for k in range(self.q_capacity_num):
                tmp -= self.alpha_q[q][k]*self.q_capacity_list[k]
            self.mu11[q] = self.mu11[q] + step_size * tmp

        # mu12 (+, 0, -)
        for c in range(self.comm_link_num):
            tmp = 0
            tmp += self.F_c[c]
            for k in range(self.comm_capacity_num):
                tmp -= self.beta[c][k]*self.comm_capacity_list[k]
            self.mu12[c] = self.mu12[c] + step_size * tmp

        # mu13 
        for i in range(self.r_loc_num, (self.r_loc_num + self.o_loc_num + self.p_loc_num + self.q_loc_num - 1)):   # o, p, q
            if i < self.r_loc_num + self.o_loc_num:   # o
                link = self.o_loc.get_link(i-self.r_loc_num)
            elif i >= self.r_loc_num + self.o_loc_num and i < self.r_loc_num + self.o_loc_num + self.p_loc_num:   # p
                link = self.p_loc.get_link(i-(self.r_loc_num+self.o_loc_num))
            elif i >= self.r_loc_num + self.o_loc_num + self.p_loc_num and i < self.r_loc_num + self.o_loc_num + self.p_loc_num + self.q_loc_num:
                link = self.q_loc.get_link(i-(self.r_loc_num+self.o_loc_num+self.p_loc_num))

            for w in range(self.userpair_num):
                tmp = 0
                userpair = self.pairset.get_pair(w)
                path_num = userpair.path_number
                for p in range(path_num):
                    path = userpair.path_set.get_path(p)
                    if link in path.node_list:
                        tmp += 1
                tmp -= 1  
            
        for i in range(self.comm_link_num):    # comm links
            for w in range(self.userpair_num):
                userpair = self.pairset.get_pair(w)
                path_num = userpair.path_number
                for p in range(path_num):
                    path = userpair.path_set.get_path(p)
                    if link in path.link_list:
                        tmp += 1
                tmp -= 1  
                self.mu13[i][w] = max(0, self.mu13[i][w] + step_size * tmp)
        # mu14 
        tmp = max_Fw
        value = 0
        for o in range(self.o_loc_num):
            for k in range(self.o_capacity_num):
                value += self.alpha_o[o][k]
        tmp = tmp - value
        self.mu14 = max(0, self.mu14 + step_size * tmp)

        # mu15
        tmp = max_Fw
        value = 0
        for p in range(self.p_loc_num):
            for k in range(self.p_capacity_num):
                value += self.alpha_p[p][k]
        tmp = tmp - value
        self.mu15 = max(0, self.mu15 + step_size * tmp)

        # mu16
        tmp = max_Fw
        value = 0
        for s in range(self.s_loc_num):
            for k in range(self.s_capacity_num):
                value += self.alpha_s[s][k]
        tmp = tmp - value
        self.mu16 = max(0, self.mu16 + step_size * tmp)

        # mu17
        tmp = max_Fw
        value = 0
        for q in range(self.q_loc_num):
            for k in range(self.q_capacity_num):
                value += self.alpha_q[q][k]
        tmp = tmp - value
        self.mu17 = max(0, self.mu17 + step_size * tmp)

        # mu18
        tmp = 0
        for r in range(self.r_loc_num):
            if self.c_r[r] - self.g_r[r] == 0:
                tmp += 0
            else:
                tmp += self.g_r[r] / (self.c_r[r] - self.g_r[r])
        for o in range(self.o_loc_num):
            if self.c_o[o] - self.g_o[o] == 0:
                tmp += 0
            else:
                tmp += self.g_o[o] / (self.c_o[o] - self.g_o[o])
        for p in range(self.p_loc_num):
            if self.c_p[p] - self.g_p[p] != 0:
                tmp += self.g_p[p] / (self.c_p[p] - self.g_p[p])
        for s in range(self.s_loc_num):
            if self.c_s[s] - self.g_s[s] != 0:
                tmp += self.g_s[s] / (self.c_s[s] - self.g_s[s])
        # c_q, g_q ======================= 先用 MM1 代替 =====================
        for q in range(self.q_loc_num):
            if self.c_q[q] - self.g_q[q] != 0:
                tmp += self.g_q[q] / (self.c_q[q] - self.g_q[q])
        for c in range(self.comm_link_num):
            if self.F_c[c] - self.f_c[c] != 0:
                tmp += self.f_c[c] / (self.F_c[c] - self.f_c[c])
        tmp = tmp / self.gamma
        tmp -= self.delay_toler
        self.mu18 = max(0, self.mu18 + step_size * tmp)

    def lagrangian_relaxation(self, Z_star, t_start, iteration_limit = 1000):
        # iteration_limit = 1000
        improvement_limit = 10
        improvement_count = 0
        count = 0
        lambda_value = 1.1
        lower_bound = -900000000
        upper_bound = 90000000000
        primal_case = "2"
        lb = np.zeros((iteration_limit))
        zstar = np.zeros((iteration_limit))
        ub = np.zeros((iteration_limit))
        result = ""

        for iter in range(iteration_limit):
            if primal_case == "2":  
                for pair in self.pairset.pairs:
                    pair.lr_weighted_matrix = pair.adjacency.get_lr_weighted_matrix(self.mu12, self.comm_links)
                    pair.path_set = pair.generate_paths("lr")

            self.initialize_decision_variables()
            sub1 = self.solve_sub1()
            sub2 = self.solve_sub2()
            sub3 = self.solve_sub3()
            sub4 = self.solve_sub4()
            sub5 = self.solve_sub5()
            sub6 = self.solve_sub6()
            sub7 = self.solve_sub7()
            sub8 = self.solve_sub8()
            sub9 = self.solve_sub9()
            sub10 = self.solve_sub10()
            sub11 = self.solve_sub11()
            sub12 = self.solve_sub12()
            sub13 = self.solve_sub13()
            constant = self.constant_value()
            Zd = sub1 + sub2 + sub3 + sub4 + sub5 + sub6 + sub7 + sub8 + sub9 + sub10 + sub11 + sub12 + sub13 + constant
            print("Iter: ", iter)
            print("Zd: ", Zd)

            # Update lower bound   
            if Zd > lower_bound:   # LB improve
                lower_bound = Zd
                lb[iter] = Zd
                improvement_count = 0
                count += 1
            else:
                improvement_count += 1
                lb[iter] = lower_bound

            upper_bound, deployed_node, deployed_link, node_level, link_level = self.primal()  
            ub[iter] = upper_bound  
            # Update upper bound
            Z_star = min(Z_star, upper_bound)
            zstar[iter] = Z_star

            print("====================================================================")
            print("UB: ", upper_bound)
            print("Z*: ", Z_star)
            print("LB: ", lower_bound)

            # Check termination
            gap = (math.fabs(Z_star - lower_bound) / (max(math.fabs(lower_bound), math.fabs(Z_star)) + sys.float_info.epsilon)) 
            print("Gap: ", gap)
            print('\n')

            if lower_bound > Z_star:
                print("====================================================================")
                print("LB > Z*")
                print("Stop at iteration: ", iter)
                print("Gap: ", gap)
                return "fail"
                break

            elif iter == iteration_limit-1:
                print("====================================================================")
                print("Iteration limit reached.")
                print("Stop at iteration: ", iter)
                print("Gap: ", gap)
                print("improvement count: ", improvement_count)
                # print("Time : ", time.clock()-t_start)
                # Write output file
                f = open("output.txt", "w")
                f.write("Node: "+str(deployed_node)+"\n")
                f.write("Capacity level: "+str(node_level)+"\n")
                f.write("\n")
                f.write("Link: "+str(deployed_link)+"\n")
                f.write("Capacity level: "+str(link_level)+"\n")
                f.close()
                # Plot the Z* 
                figure, ax = plt.subplots(figsize = (8,4), dpi=100)
                ax.plot(zstar, label="LRPS", color="darkseagreen", linewidth=2)
                ax.plot(lb, label="Lower Bound", color="cadetblue", linewidth=2)
                major_tricks = np.arange(0, upper_bound+1000, 10000) 
                ax.legend(loc="lower right")
                ax.set_title("Objective Values of LB and LRPS")
                ax.set_xlabel("Iteration")
                ax.set_ylabel("Objective Value")
                figure.tight_layout()
                plt.savefig("primal"+primal_case+".png")
                # plt.show()
                return "success"
                break

            # Adjust multipliers
            if improvement_count == improvement_limit:
                lambda_value /= 2
                improvement_count = 0
                count = 0
            
            self.adjust_multiplier(lambda_value, Z_star, Zd)









 