import numpy as np
import math
import sys
from link import LinkSet


class Primal():
    def __init__(self, odpair_set, link_set: LinkSet,prioritylv):
        self.odpair_set = odpair_set
        self.link_set = link_set
        self.prioritylv = prioritylv
        temp = [0 for i in range(len(odpair_set))]
        for w in range(len(odpair_set)):
            temp[w] = [0 for p in range(len(odpair_set[w].paths))]
        self.x = temp
        self.a = np.full((len(odpair_set),link_set.length(),prioritylv),sys.float_info.epsilon)   # a_wlk
        self.h = np.full((len(odpair_set),link_set.length()),  prioritylv*sys.float_info.epsilon) 
        self.g =  np.full((link_set.length(),prioritylv),sys.float_info.epsilon)  
        self.rho = np.zeros((link_set.length(),prioritylv))                             
        self.gamma = np.full((link_set.length(),prioritylv),sys.float_info.epsilon)
        for l in range(link_set.length()):
            self.alpha = np.full((link_set.length(),prioritylv),1/link_set.links[l].svcRate)
            self.t = np.full((link_set.length(),prioritylv),1/link_set.links[l].svcRate)
            self.b = np.full((len(odpair_set),link_set.length(),prioritylv),sys.float_info.epsilon/link_set.links[l].svcRate)
            self.f = np.full((len(odpair_set),link_set.length()),sys.float_info.epsilon*prioritylv/link_set.links[l].svcRate)
        self.d = np.zeros(len(odpair_set))
        
    def initialize_decision_variables(self):                        
        temp = [0 for i in range(len(self.odpair_set))]
        for w in range(len(self.odpair_set)):
            temp[w] = [0 for p in range(len(self.odpair_set[w].paths))]
        self.x = temp
        self.a = np.full((len(self.odpair_set),self.link_set.length(),self.prioritylv),sys.float_info.epsilon)   # a_wlk
        self.h = np.full((len(self.odpair_set),self.link_set.length()),self.prioritylv*sys.float_info.epsilon)  
        self.g = np.full((self.link_set.length(),self.prioritylv),sys.float_info.epsilon)  
        self.rho = np.zeros((self.link_set.length(),self.prioritylv))                             
        self.gamma = np.full((self.link_set.length(),self.prioritylv),sys.float_info.epsilon)
        for l in range(self.link_set.length()):
            self.alpha = np.full((self.link_set.length(),self.prioritylv),1/self.link_set.links[l].svcRate)
            self.t = np.full((self.link_set.length(),self.prioritylv),1/self.link_set.links[l].svcRate)
            self.b = np.full((len(self.odpair_set),self.link_set.length(),self.prioritylv),sys.float_info.epsilon/self.link_set.links[l].svcRate)
            self.f = np.full((len(self.odpair_set),self.link_set.length()),sys.float_info.epsilon*self.prioritylv/self.link_set.links[l].svcRate)
        self.d = np.zeros(len(self.odpair_set))

    def initial_solution(self):
        self.initialize_decision_variables()
        # x_p
        for w in range(len(self.odpair_set)):
            shortest_path = (math.inf,-1)
            for p in range(len(self.odpair_set[w].paths)):
                if(len(self.odpair_set[w].paths[p].link_list) < shortest_path[0]):
                    shortest_path = (len(self.odpair_set[w].paths[p].link_list),p)
            self.x[w][shortest_path[1]] = 1    
        
        # no priority for a_wlk, h_wl
        for w in range(len(self.odpair_set)):
            for p in range(len(self.odpair_set[w].paths)):
                if self.x[w][p] == 1:
                    for l in range(len(self.odpair_set[w].paths[p].link_list)):
                        self.a[w][self.odpair_set[w].paths[p].link_list[l].id][0] = 1
                        self.h[w][self.odpair_set[w].paths[p].link_list[l].id] = 1+(self.prioritylv-1)*sys.float_info.epsilon
            
        self.d = self.calDelay()
        z_star = self.calObjective()
        
        return z_star,self.d
    
    def get_primal_feasible(self, mu, a_wlk):
        mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8, mu9, mu10 = mu
        self.initialize_decision_variables()
        
        # x_p find path
        for w in range(len(self.odpair_set)):
            shortest_path = (math.inf,-1)
            for p in range(len(self.odpair_set[w].paths)):
                mu1_sum = 0
                for l in range(len(self.odpair_set[w].paths[p].link_list)):
                    mu1_sum += mu1[w][self.odpair_set[w].paths[p].link_list[l].id]
                if mu1_sum < shortest_path[0]:
                    shortest_path = (mu1_sum,p)
            if shortest_path[1] == -1:
                raise Exception('can not find path for primal')
            else:
                self.x[w][shortest_path[1]] = 1
                
        # a_wlk assign priority                        
        for w in range(len(self.odpair_set)):
            for p in range(len(self.odpair_set[w].paths)):
                if self.x[w][p] == 1:
                    for l in range(len(self.odpair_set[w].paths[p].link_list)):
                        #self.a[w][self.odpair_set[w].paths[p].link_list[l].id][self.odpair_set[w].priority-1] = 1
                        
                        for k in range(self.prioritylv):
                            self.a[w][self.odpair_set[w].paths[p].link_list[l].id][k] = a_wlk[w][self.odpair_set[w].paths[p].link_list[l].id][k]
                        
                        self.h[w][self.odpair_set[w].paths[p].link_list[l].id] = 1+(self.prioritylv-1)*sys.float_info.epsilon

                          
        self.d = self.calDelay()
        
        UB = self.calObjective()
        
        return UB            
    
    def adjust_pri_1(self):
        
        #找出所有不滿足delay tolerance的O-D pair w index
        unsatisfied = []
        satisfied = []
        #i = 0 #計算有多少不滿足delay tolerance的O-D pairs
        for w in range(len(self.odpair_set)):
            difference = self.d[w] - self.odpair_set[w].delayTol
            if(difference > 0):
                unsatisfied.append((w,difference)) #不滿足的index與量
            elif(difference < 0): #滿足並有餘裕調整之O-D pairs
                satisfied.append((w,difference))
                
        if(len(unsatisfied)==0):
            return
        
        unsatisfied.sort(key = lambda unsatisfied: unsatisfied[1],reverse = True) #依不滿足量由大到小排序
        satisfied.sort(key = lambda satisfied: satisfied[1],reverse = False) #依滿足量由小到大排序，負越多餘裕越多        

        
        #找出每條link上具有最大餘裕的O-D pair
        satisOnLink = []
        for l in range(self.link_set.length()):
            for pair in satisfied:
                if(self.h[pair[0]][l]>=1):
                    satisOnLink.append(pair[0])
                    break
        
            
        maxW = unsatisfied[0][0]
        #找出最不滿足O-D pair各link上的delay並由大到小排序
        linkDelay = []            
        for l in range(self.link_set.length()):
            if(self.h[maxW][l]>=1):
                linkDelay.append((l,self.f[maxW][l]))
        linkDelay.sort(key = lambda linkDelay: linkDelay[1],reverse = True)
        #print(linkDelay)
        
        
        while((self.d[maxW]-self.odpair_set[maxW].delayTol)>0):
            print(self.d[maxW])
            #重新調整priority 
            if(len(linkDelay) == 0):
                return
            maxL = linkDelay[0][0]
            #if(satisOnLink[maxL])
            satisW = satisOnLink[maxL]
            for k in range(self.prioritylv):
                if(self.a[maxW][maxL][k] >= 1):
                    maxk = k
                if(self.a[satisW][maxL][k] >= 1):
                    satisk = k
            
            if(maxk == satisk):
                if(maxk == 0):
                    self.a[maxW][maxL][maxk] = 0
                    self.a[maxW][maxL][maxk+1] = 1
                elif(satisk == self.prioritylv-1):
                    self.a[satisW][maxL][satisk] = 0
                    self.a[satisW][maxL][satisk-1] = 1
            else:  
                self.a[maxW][maxL][maxk] = 0
                self.a[satisW][maxL][satisk] = 0
                self.a[maxW][maxL][satisk] = 1
                self.a[satisW][maxL][maxk] = 1
            
            del linkDelay[0]
            self.d[maxW] = self.calWDelay(maxW)
            print(self.d[maxW])
            
        self.d = self.calDelay()
        
        for w in range(len(self.odpair_set)):
            difference = self.d[w] - self.odpair_set[w].delayTol
            if(difference > 0):
                self.adjust_pri_1()
        
        
        
        
        max_dw = max(self.d)
        max_dw_index = self.d.argmax()
        print(max_dw,max_dw_index)
        
        count = 0
        while(max_dw > self.odpair_set[max_dw_index].delayTol):
            #for w in range(len(self.odpair_set)):
            w = max_dw_index
            for p in range(len(self.odpair_set[w].paths)):
                if self.x[w][p] == 1:
                    # max_dw中某link上delay最高者，調整其priority
                    max_delay_link = self.f[w].argmax()
                    print(max_delay_link)
                    #for l in range(len(self.odpair_set[w].paths[p].link_list)):
                    min_glk = (math.inf, -1)
                    for k in range(self.prioritylv):
                        if(self.g[max_delay_link][k] < min_glk[0]):
                            min_glk = (self.g[max_delay_link][k], k)
                    print(min_glk)

                        #if(self.g[self.odpair_set[w].paths[p].link_list[l].id][k] < min_glk[0]):
                            #min_glk = (self.g[self.odpair_set[w].paths[p].link_list[l].id][k], k)


                    self.a[w][max_delay_link][self.odpair_set[w].priority-1] = 0
                    self.a[w][max_delay_link][min_glk[1]] = 1
                   
                    #self.a[w][self.odpair_set[w].paths[p].link_list[l].id][self.odpair_set[w].priority-1] = 0
                    #self.a[w][self.odpair_set[w].paths[p].link_list[l].id][min_glk[1]] = 1
                    

            self.d = self.calDelay()
            #print(self.d)
            
            max_dw = max(self.d)
            max_dw_index = self.d.argmax()
            print(max_dw,max_dw_index)
            count += 1
            if(count >= 10):
                break
            
            
    def adjust_pri_2(self):
        dw_gap = []
        #infeasible_dw = []
        for w in range(len(self.odpair_set)):
             dw_gap.append(self.d[w] - self.odpair_set[w].delayTol)
             #if(dw_gap[w]):
                 
        if(dw_gap < 0): #不符合od pair w delay tolerance
            max_dw_index = dw_gap.index(min(dw_gap))
            
            max_l_delay = (-math.inf,-1)
            for l in range(self.link_set.length()):
                if(self.f[max_dw_index][l] > max_l_delay[0] and self.h[max_dw_index][l] == 1):
                    max_l_delay = (self.f[max_dw_index][l],l)
            for k in range(self.prioritylv):
                if(self.a[max_dw_index][max_l_delay[1]][k] == 1):
                    self.a[max_dw_index][max_l_delay[1]][k] = 0
            self.a[max_dw_index][max_l_delay[1]][0] = 1   
            
            print(self.d[max_dw_index])
            self.d = self.calDelay()
            print(self.d[max_dw_index])
        
        max_dw = max(self.d)
        max_dw_index = self.d.argmax()
        print(max_dw,max_dw_index)
        
        
        while(max_dw > self.odpair_set[max_dw_index].delayTol):
            #for w in range(len(self.odpair_set)):
            w = max_dw_index
            for p in range(len(self.odpair_set[w].paths)):
                if self.x[w][p] == 1:
                    # max_dw中某link上delay最高者，調整其priority
                    max_delay_link = self.f[w].argmax()
                    print(max_delay_link)
                    #for l in range(len(self.odpair_set[w].paths[p].link_list)):
                    min_glk = (math.inf, -1)
                    for k in range(self.prioritylv):
                        if(self.g[max_delay_link][k] < min_glk[0]):
                            min_glk = (self.g[max_delay_link][k], k)
                    print(min_glk)

                        #if(self.g[self.odpair_set[w].paths[p].link_list[l].id][k] < min_glk[0]):
                            #min_glk = (self.g[self.odpair_set[w].paths[p].link_list[l].id][k], k)


                    self.a[w][max_delay_link][self.odpair_set[w].priority-1] = 0
                    self.a[w][max_delay_link][min_glk[1]] = 1
                   
                    #self.a[w][self.odpair_set[w].paths[p].link_list[l].id][self.odpair_set[w].priority-1] = 0
                    #self.a[w][self.odpair_set[w].paths[p].link_list[l].id][min_glk[1]] = 1
                    

            self.d = self.calDelay()
            #print(self.d)
            
            max_dw = max(self.d)
            max_dw_index = self.d.argmax()
      
        
            
    def all_value(self):
            return self.x, self.h, self.a, self.g, self.rho, self.gamma, self.alpha, self.t, self.b, self.f, self.d
        
    
            
    def calObjective(self):
        sum_ld = 0
        total_traffic = 0
        for w in range(len(self.odpair_set)):
            sum_ld += self.odpair_set[w].traffic * self.d[w]
            total_traffic += self.odpair_set[w].traffic
            #sum_ld += self.odpair_set[w].traffic
        UB = sum_ld / total_traffic
        #UB = sum_ld / len(self.odpair_set)
        return UB        
    
    def calDelay(self):
        # g_lk
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                temp_g = 0
                for w in range(len(self.odpair_set)):
                    temp_g += self.a[w][l][k]*self.odpair_set[w].traffic
                self.g[l][k] = temp_g   
                #print(self.g[l][k])
                
                if(self.g[l][k] > self.link_set.links[l].svcRate):
                    raise Exception('svcRate < traffic')
                   
                
                #print(self.g[l][k])
        
        # rho_lk
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):                
                self.rho[l][k] = self.g[l][k] / self.link_set.links[l].svcRate

        # gamma_lk
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                rho_sum = 0
                for j in range(k+1):
                    rho_sum += self.rho[l][j]
                self.gamma[l][k] = 1 - rho_sum

                    
        # alpha_lk
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                self.alpha[l][k] = (2-self.gamma[l][k])/self.link_set.links[l].svcRate

        
        # t_lk
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                self.t[l][k] = self.alpha[l][k]/(self.gamma[l][k]*self.gamma[l][k-1])


                
        # b_wlk
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                for k in range(self.prioritylv):
                    self.b[w][l][k] = self.a[w][l][k] * self.t[l][k]

        # f_wl
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                b_sum = 0
                for k in range(self.prioritylv):
                    b_sum += self.b[w][l][k]
                self.f[w][l] = b_sum

        # d_w
        for w in range(len(self.odpair_set)):
            f_sum = 0
            for l in range(self.link_set.length()):
                f_sum += self.f[w][l]
            self.d[w] = f_sum
        
            
        return self.d
    

    def calWDelay(self,w):
        # b_wlk
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                self.b[w][l][k] = self.a[w][l][k] * self.t[l][k]
        
        # f_wl
        for l in range(self.link_set.length()):
            b_sum = 0
            for k in range(self.prioritylv):
                b_sum += self.b[w][l][k]
            self.f[w][l] = b_sum
        
        # d_w
        f_sum = 0
        for l in range(self.link_set.length()):
            f_sum += self.f[w][l]
        self.d[w] = f_sum
        
        return self.d[w]
    


                    
          