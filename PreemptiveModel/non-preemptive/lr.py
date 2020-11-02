import numpy as np
import math
import sys
from link import LinkSet, Link


class LR():
    # set decision variables
    # update epsilon
    
    def __init__(self, odpair_set, link_set: LinkSet,prioritylv):
        self.epsilon = sys.float_info.epsilon
        self.odpair_set = odpair_set
        self.link_set = link_set
        self.prioritylv = prioritylv
        temp = [0 for i in range(len(odpair_set))]
        for w in range(len(odpair_set)):
            temp[w] = [0 for p in range(len(odpair_set[w].paths))]
        self.x = temp
        self.a = np.full((len(odpair_set),link_set.length(),prioritylv),self.epsilon)   # a_wlk
        self.h = np.full((len(odpair_set),link_set.length()),  prioritylv*self.epsilon)
        self.g =  np.full((link_set.length(),prioritylv),self.epsilon) 
        self.rho = np.zeros((link_set.length(),prioritylv))                             
        self.gamma = np.full((link_set.length(),prioritylv),self.epsilon)
        self.tau = np.full(link_set.length(),self.epsilon)
        self.q = np.full((link_set.length(),prioritylv),self.epsilon)
        self.t = np.zeros((link_set.length(),prioritylv))
        self.b = np.zeros((len(odpair_set),link_set.length(),prioritylv))
        self.f = np.zeros((len(odpair_set),link_set.length()))
        for l in range(link_set.length()):
            self.t[l] = 1/link_set.links[l].svcRate
        for w in range(len(odpair_set)):
            for l in range(link_set.length()):
                self.b[w][l] = self.epsilon/link_set.links[l].svcRate
                self.f[w][l] = self.epsilon*prioritylv/link_set.links[l].svcRate
        self.d = np.full((len(odpair_set)),self.epsilon*prioritylv/link_set.links[l].svcRate)
        
    def initialize_decision_variables(self):                        
        temp = [0 for i in range(len(self.odpair_set))]
        for w in range(len(self.odpair_set)):
            temp[w] = [0 for p in range(len(self.odpair_set[w].paths))]
        self.x = temp
        self.a = np.full((len(self.odpair_set),self.link_set.length(),self.prioritylv),self.epsilon)   # a_wlk
        self.h = np.full((len(self.odpair_set),self.link_set.length()),self.prioritylv*self.epsilon)  
        self.g =  np.full((self.link_set.length(),self.prioritylv),self.epsilon) 
        self.rho = np.zeros((self.link_set.length(),self.prioritylv))                             
        self.gamma = np.full((self.link_set.length(),self.prioritylv),self.epsilon)
        self.tau = np.full(self.link_set.length(),self.epsilon)
        self.q = np.full((self.link_set.length(),self.prioritylv),self.epsilon)
        self.t = np.zeros((self.link_set.length(),self.prioritylv))
        self.b = np.zeros((len(self.odpair_set),self.link_set.length(),self.prioritylv))
        self.f = np.zeros((len(self.odpair_set),self.link_set.length()))
        for l in range(self.link_set.length()):
            self.t[l] = 1/self.link_set.links[l].svcRate
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                self.b[w][l] = self.epsilon/self.link_set.links[l].svcRate
                self.f[w][l] = self.epsilon*self.prioritylv/self.link_set.links[l].svcRate
        self.d = np.full((len(self.odpair_set)),self.epsilon*self.prioritylv/self.link_set.links[l].svcRate)           
    
    def initialize_lr_multiplier(self):
        init_value = 0.000001
        self.mu1 = np.full((len(self.odpair_set),self.link_set.length()), init_value) 
        self.mu2 = np.full((len(self.odpair_set),self.link_set.length()), init_value)
        self.mu3 = np.full((self.link_set.length(),self.prioritylv), init_value)
        self.mu4 = np.full((self.link_set.length(),self.prioritylv), init_value)
        self.mu5 = np.full((self.link_set.length(),self.prioritylv), init_value)
        self.mu6 = np.full(self.link_set.length(),init_value)
        self.mu7 = np.full((self.link_set.length(),self.prioritylv), init_value)
        self.mu8 = np.full((self.link_set.length(),self.prioritylv), init_value)
        self.mu9 = np.full((len(self.odpair_set),self.link_set.length(),self.prioritylv), init_value)
        self.mu10 = np.full((len(self.odpair_set),self.link_set.length()), init_value)
        self.mu11 = np.full((len(self.odpair_set)), init_value)
        
        return (self.mu1, self.mu2, self.mu3, self.mu4, self.mu5, self.mu6, self.mu7, self.mu8, self.mu9, self.mu10, self.mu11)
    
    def x_value(self):
        return self.x
    
    def h_value(self):
        return self.h
    
    def a_vaule(self):
        return self.a
    
    def g_value(self):
        return self.g
    
    def all_value(self):
        return self.x, self.h, self.a, self.g, self.rho, self.gamma, self.tau, self.t, self.b, self.f, self.d
    
    
    def sol_sub1(self):
        sub1_value = 0
        for w in range(len(self.odpair_set)):
            min_coef_path = (math.inf,-1)
            for p in range(len(self.odpair_set[w].paths)):
                this_coef = 0
                for l in range(len(self.odpair_set[w].paths[p].link_list)):
                    this_coef += self.mu1[w][self.odpair_set[w].paths[p].link_list[l].id]
                if this_coef < min_coef_path[0]:
                    min_coef_path = (this_coef,p)
            #print(min_coef_path)
            if min_coef_path[1] == -1:
                raise Exception('can not find path for sub1')
            else:
                self.x[w][min_coef_path[1]] = 1
                sub1_value += min_coef_path[0]
       
        print('Sub1 solved! value: ', sub1_value)                
        return sub1_value
    
    def sol_sub2(self):
        sub2_value = 0
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                this_coef = 0
                this_coef += self.mu1[w][l]+self.mu2[w][l]
                if this_coef > 0:
                    self.h[w][l] = 1+(self.prioritylv-1)*self.epsilon
                sub2_value -= this_coef*self.h[w][l]
        print('Sub2 solved! value: ', sub2_value)
        return sub2_value
    
    def sol_sub3(self):
        sub3_value = 0
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                #min_value_priority = (-math.inf,-1)
                min_coef_k = (math.inf,-1)
                for k in range(self.prioritylv):
                    #coef_a_epsilon = 0
                    #coef_a_1 = 0
                    #coef_a_epsilon += (self.mu2[w][l]-self.mu3[l][k]*self.odpair_set[w].traffic)*self.epsilon - self.mu8[w][l][k]*math.log(self.epsilon)
                    coef_a_1 = (self.mu2[w][l]-self.mu3[l][k]*self.odpair_set[w].traffic)*1 - self.mu9[w][l][k]*math.log(1)
                    #if coef_a_epsilon >= coef_a_1:
                    #print(coef_a_1,self.mu2[w][l],self.mu3[l][k])
                    if coef_a_1 < min_coef_k[0]:
                        min_coef_k = (coef_a_1,k)
                    #else:
                        #if coef_a_epsilon < min_coef_k[0]:
                            #min_coef_k = (coef_a_epsilon,k)
                if min_coef_k[1] == -1:
                    raise Exception('can not find priority for sub3')
                else:
                    self.a[w][l][min_coef_k[1]] = 1
                coef_a_epsilon = (self.mu2[w][l]-self.mu3[l][k]*self.odpair_set[w].traffic)*self.epsilon - self.mu9[w][l][k]*math.log(self.epsilon)
                '''
                    if(min_value_priority[0] == min_coef_k[0]):
                        self.a[w][l][min_value_priority[1]] = 1
                    else:
                        self.a[w][l][min_value_priority[1]] = self.epsilon
                '''
                sub3_value += min_coef_k[0] + (coef_a_epsilon*(self.prioritylv-1))
        print('Sub3 solved! value: ', sub3_value)
        return sub3_value
    
    def sol_sub4(self):
        sub4_value = 0
        for l in range(self.link_set.length()):
            '''
            min_coef = (math.inf,-1)
            
            for k in range(self.prioritylv): 
                this_coef = self.mu3[l][k]-(self.mu4[l][k]/self.link_set.links[l].svcRate)
                if(this_coef < min_coef[0]):
                    min_coef = (this_coef,k)
                    
            self.g[l][min_coef[1]] = self.link_set.links[l].svcRate
            '''
            for k in range(self.prioritylv):
                #this_coef = self.mu3[l][k]-(self.mu4[l][k]/self.link_set.links[l].svcRate)
                #sub4_value += this_coef*self.g[l][k]
                
                this_coef = 0
                this_coef += self.mu3[l][k]-(self.mu4[l][k]/self.link_set.links[l].svcRate)
                #print(this_coef)
                if this_coef < 0:
                    self.g[l][k] =  self.link_set.links[l].svcRate
                sub4_value += this_coef*self.g[l][k]
                
        print('Sub4 solved! value: ', sub4_value)        
        return sub4_value
    
    def sol_sub5(self):
        sub5_value = 0
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                this_coef = 0
                mu5_coef = 0
                for j in range(k):
                    mu5_coef += self.mu5[l][j]
                this_coef += self.mu4[l][k]+mu5_coef
                if this_coef < 0:
                    self.rho[l][k] =  1-self.epsilon
                sub5_value += this_coef*self.rho[l][k]
        print('Sub5 solved! value: ', sub5_value)        
        return sub5_value
    
    def sol_sub6_1(self):
        sub6_1_value = 0
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv-1):
                value_gamma_lower = 0
                value_gamma_upper = 0
                value_gamma_derivative = 0
                gamma_derivative = (-self.mu7[l][k]-self.mu7[l][k+1])/(self.mu5[l][k])
                value_gamma_lower += (self.mu5[l][k])*self.epsilon + (self.mu7[l][k]+self.mu7[l][k+1])*math.log(self.epsilon)
                value_gamma_upper += (self.mu5[l][k])*(1-self.epsilon) + (self.mu7[l][k]+self.mu7[l][k+1])*math.log(1-self.epsilon)
                if(value_gamma_upper < value_gamma_lower):
                    min_value = value_gamma_upper
                    self.gamma[l][k] = 1-self.epsilon
                else:
                    min_value = value_gamma_lower
                
                if(gamma_derivative > self.epsilon and gamma_derivative < (1-self.epsilon)):
                    value_gamma_derivative += (self.mu5[l][k])*gamma_derivative + (self.mu7[l][k]+self.mu7[l][k+1])*math.log(gamma_derivative)
                    if(value_gamma_derivative < value_gamma_lower and value_gamma_derivative < value_gamma_upper):
                        min_value = value_gamma_derivative
                        self.gamma[l][k] = gamma_derivative
                elif(value_gamma_upper < value_gamma_lower):
                    min_value = value_gamma_upper
                    self.gamma[l][k] = 1-self.epsilon
                else:
                    min_value = value_gamma_lower

                sub6_1_value += min_value
        print('Sub6_1 solved! value: ', sub6_1_value)        
        return sub6_1_value
    
    def sol_sub6_2(self):
        sub6_2_value = 0
        for l in range(self.link_set.length()):
            value_gamma_lower = 0
            value_gamma_upper = 0
            value_gamma_derivative = 0
            gamma_derivative = ((-self.mu7[l][self.prioritylv-1])*self.link_set.links[l].svcRate)/self.mu6[l]
            value_gamma_lower += (self.mu6[l]/self.link_set.links[l].svcRate*self.epsilon) + (self.mu7[l][self.prioritylv-1])*math.log(self.epsilon)
            value_gamma_upper += (self.mu6[l]/self.link_set.links[l].svcRate)*(1-self.epsilon) + (self.mu7[l][self.prioritylv-1])*math.log(1-self.epsilon)
            if(value_gamma_upper < value_gamma_lower):
                min_value = value_gamma_upper
                self.gamma[l][self.prioritylv-1] = 1-self.epsilon
            else:
                min_value = value_gamma_lower
            
            if(gamma_derivative > self.epsilon and gamma_derivative < (1-self.epsilon)):
                value_gamma_derivative += (self.mu6[l]/self.link_set.links[l].svcRate)*gamma_derivative + (self.mu7[l][self.prioritylv-1])*math.log(gamma_derivative)
                if(value_gamma_derivative < value_gamma_lower and value_gamma_derivative < value_gamma_upper):
                    min_value = value_gamma_derivative
                    self.gamma[l][self.prioritylv-1] = gamma_derivative
            elif(value_gamma_upper < value_gamma_lower):
                min_value = value_gamma_upper
                self.gamma[l][self.prioritylv-1] = 1-self.epsilon
            else:
                min_value = value_gamma_lower

            sub6_2_value += min_value
        print('Sub6_2 solved! value: ', sub6_2_value)        
        return sub6_2_value
    
    def sol_sub7(self):
        sub7_value = 0
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                value_tau_lower = 0
                value_tau_upper = 0
                value_tau_derivative = 0
                tau_derivative = self.mu7[l][k]/self.mu6[l]
                value_tau_lower += self.mu6[l]*self.epsilon - self.mu7[l][k]*math.log(self.epsilon)
                value_tau_upper += self.mu6[l]*(1/self.link_set.links[l].svcRate) - self.mu7[l][k]*math.log((1/self.link_set.links[l].svcRate))
                min_value = min(value_tau_lower,value_tau_upper)
                if(min_value==value_tau_upper):
                    self.tau[l] = 1/self.link_set.links[l].svcRate
                if(tau_derivative > self.epsilon and tau_derivative < (1/self.link_set.links[l].svcRate)):
                    value_tau_derivative += self.mu6[l]*tau_derivative - self.mu7[l][k]*math.log(tau_derivative)
                    if(value_tau_derivative < min_value):
                        min_value = value_tau_derivative
                        self.tau[l] = tau_derivative
                sub7_value += min_value
        print('Sub7 solved! value: ', sub7_value)         
        return sub7_value

    def sol_sub8(self):
        sub8_value = 0
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                value_q_lower = 0
                value_q_upper = 0
                value_q_derivative = 0
                q_derivative = self.mu7[l][k]/self.mu8[l][k]
                value_q_lower += self.mu7[l][k]*math.log(self.epsilon) - self.mu8[l][k]*self.epsilon
                value_q_upper += self.mu7[l][k]*math.log(self.link_set.links[l].delayTol[k]) - self.mu8[l][k]*self.link_set.links[l].delayTol[k]
                min_value = min(value_q_lower,value_q_upper)
                if(min_value==value_q_upper):
                    self.q[l][k] = self.link_set.links[l].delayTol[k]
                if(q_derivative > self.epsilon and q_derivative < self.link_set.links[l].delayTol[k]):
                    value_q_derivative += self.mu7[l][k]*math.log(q_derivative) - self.mu8[l][k]*q_derivative
                    if(value_q_derivative < min_value):
                        min_value = value_q_derivative
                        self.q[l][k] = q_derivative
                sub8_value += min_value
        print('Sub8 solved! value: ', sub8_value)         
        return sub8_value

    
    def sol_sub9(self):
        sub9_value = 0
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                for k in range(self.prioritylv):
                    value_t_lower = 0
                    value_t_upper = 0
                    value_t_derivative = 0
                    t_derivative = self.mu9[w][l][k]/self.mu8[l][k]
                    value_t_lower += self.mu8[l][k]*(1/self.link_set.links[l].svcRate) - self.mu9[w][l][k]*math.log((1/self.link_set.links[l].svcRate))
                    value_t_upper += self.mu8[l][k]*(self.link_set.links[l].delayTol[k]) - self.mu9[w][l][k]*math.log((self.link_set.links[l].delayTol[k]))
                    min_value = min(value_t_lower,value_t_upper)
                    if(min_value==value_t_upper):
                        self.t[l][k] = self.link_set.links[l].delayTol[k]
                    if(t_derivative > (1/self.link_set.links[l].svcRate) and t_derivative < (self.link_set.links[l].delayTol[k])):
                        value_t_derivative += self.mu8[l][k]*(t_derivative) - self.mu9[w][l][k]*math.log((t_derivative))
                        if(value_t_derivative < min_value):
                            min_value = value_t_derivative
                            self.t[l][k] = t_derivative
                    sub9_value += min_value
        print('Sub9 solved! value: ', sub9_value)         
        return sub9_value    
    
    def sol_sub10(self):
        sub10_value = 0
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                for k in range(self.prioritylv):
                    value_b_lower = 0
                    value_b_upper = 0
                    value_b_derivative = 0
                    b_lower = self.epsilon/self.link_set.links[l].svcRate
                    b_upper = self.link_set.links[l].delayTol[k]
                    b_derivative = self.mu9[w][l][k]/self.mu10[w][l]
                    value_b_lower += self.mu9[w][l][k]*math.log(b_lower)-(self.mu10[w][l]*b_lower)
                    value_b_upper += self.mu9[w][l][k]*math.log(b_upper)-(self.mu10[w][l]*b_upper)
                    min_value = min(value_b_lower,value_b_upper)
                    if(min_value==value_b_upper):
                        self.b[w][l][k] = b_upper
                    if(b_derivative > b_lower and b_derivative < b_upper):
                        value_b_derivative += self.mu9[w][l][k]*math.log(b_derivative)-(self.mu10[w][l]*b_derivative)
                        if(value_b_derivative < min_value):
                            min_value = value_b_derivative
                            self.b[w][l][k] = b_derivative
                    sub10_value += min_value
        print('Sub10 solved! value: ', sub10_value)
        return sub10_value
    
    def sol_sub11(self):
        sub11_value = 0
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                this_coef = 0
                this_coef += self.mu10[w][l]-self.mu11[w]
                if(this_coef < 0):
                    self.f[w][l] = max(self.link_set.links[l].delayTol)
                sub11_value += this_coef * self.f[w][l]
        print('Sub11 solved! value: ', sub11_value)
        return sub11_value
    
    def sol_sub12(self):
        sub12_value = 0
        total_traffic = 0
        for w in range(len(self.odpair_set)):
            total_traffic += self.odpair_set[w].traffic
        for w in range(len(self.odpair_set)):
            this_coef = 0
            this_coef += self.odpair_set[w].traffic/total_traffic + self.mu11[w]
            if(this_coef < 0):
                self.d[w] = self.odpair_set[w].delayTol
            sub12_value += this_coef * self.d[w]
        print('Sub12 solved! value: ', sub12_value)
        return sub12_value
                
          
    def adjust_multiplier_denominator(self, lamda, z_star, zd):
        dominator = 0
        
        # update mu1
        x_first_term = [[0 for l in range(self.link_set.length())] for w in range(len(self.odpair_set))]
        for w in range(len(self.odpair_set)):
            for p in range(len(self.odpair_set[w].paths)):
                for l in range(len(self.odpair_set[w].paths[p].link_list)): 
                    if self.x[w][p] == 1:
                        x_first_term[w][self.odpair_set[w].paths[p].link_list[l].id] = 1
                    
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                mu1_tmp = 0
                mu1_tmp += x_first_term[w][l]-self.h[w][l]
                dominator += math.pow(mu1_tmp,2)
        
        # update mu2
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                mu2_tmp = 0
                for k in range(self.prioritylv):
                    mu2_tmp += self.a[w][l][k]
                mu2_tmp -= self.h[w][l]
                dominator += math.pow(mu2_tmp,2)
                        
        # update mu3
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                mu3_tmp = 0
                mu3_tmp += self.g[l][k]
                for w in range(len(self.odpair_set)):
                    mu3_tmp -= self.a[w][l][k]*self.odpair_set[w].traffic
                dominator += math.pow(mu3_tmp,2)
        
        # update mu4
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                mu4_tmp = 0
                mu4_tmp += self.rho[l][k] - (self.g[l][k]/self.link_set.links[l].svcRate)
                dominator += math.pow(mu4_tmp,2)
        
        # update mu5
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):     
                mu5_tmp = 0
                mu5_tmp += self.gamma[l][k]
                last_term = 1
                for j in range(k+1):    
                    last_term -= self.rho[l][j]
                mu5_tmp -= last_term
                dominator += math.pow(mu5_tmp,2)
        
        # update mu6
        for l in range(self.link_set.length()):
            mu6_tmp = 0
            mu6_tmp += self.tau[l] - (1/self.link_set.links[l].svcRate*(1-self.gamma[l][self.prioritylv-1]))
            dominator += math.pow(mu6_tmp,2)
        
        # update mu7
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv): 
                mu7_tmp = 0
                mu7_tmp += math.log(self.q[l][k]) - math.log(self.tau[l]) + math.log(self.gamma[l][k-1]) + math.log(self.gamma[l][k])
                dominator += math.pow(mu7_tmp,2)
        
        # update mu8
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                mu8_tmp = 0
                mu8_tmp += self.t[l][k] - self.q[l][k] - (1/self.link_set.links[l].svcRate)
                dominator += math.pow(mu8_tmp,2)

        # update mu9
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                for k in range(self.prioritylv):
                    mu9_tmp = 0
                    mu9_tmp += math.log(self.b[w][l][k]) - math.log(self.a[w][l][k]) - math.log(self.t[l][k])
                    dominator += math.pow(mu9_tmp,2)
        
        # update mu10
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                mu10_tmp = 0
                mu10_tmp += self.f[w][l]
                for k in range(self.prioritylv):
                    mu10_tmp -= self.b[w][l][k]
                dominator += math.pow(mu10_tmp,2)
        
        # update mu11
        for w in range(len(self.odpair_set)):
            mu11_tmp = 0
            mu11_tmp += self.d[w]
            for l in range(self.link_set.length()):
                mu11_tmp -= self.f[w][l]
            dominator += math.pow(mu11_tmp,2)
            
        step_size = lamda * (z_star - zd) / dominator
        
        # update mu1
        x_first_term = [[0 for l in range(self.link_set.length())] for w in range(len(self.odpair_set))]
        for w in range(len(self.odpair_set)):
            for p in range(len(self.odpair_set[w].paths)):
                for l in range(len(self.odpair_set[w].paths[p].link_list)): 
                    if self.x[w][p] == 1:
                        x_first_term[w][self.odpair_set[w].paths[p].link_list[l].id] = 1
                    
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                mu1_tmp = 0
                mu1_tmp += x_first_term[w][l]-self.h[w][l]
                self.mu1[w][l] = max(0, self.mu1[w][l] + step_size * mu1_tmp)
        
        # update mu2
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                mu2_tmp = 0
                for k in range(self.prioritylv):
                    mu2_tmp += self.a[w][l][k]
                mu2_tmp -= self.h[w][l]
                self.mu2[w][l] = self.mu2[w][l] + step_size * mu2_tmp
        
        # update mu3
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                mu3_tmp = 0
                mu3_tmp += self.g[l][k]
                for w in range(len(self.odpair_set)):
                    mu3_tmp -= self.a[w][l][k]*self.odpair_set[w].traffic
                self.mu3[l][k] = self.mu3[l][k] + step_size * mu3_tmp
        
        # update mu4
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):
                mu4_tmp = 0
                mu4_tmp += self.rho[l][k] - (self.g[l][k]/self.link_set.links[l].svcRate)
                self.mu4[l][k] = self.mu4[l][k] + step_size * mu4_tmp
        
        # update mu5
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv):     
                mu5_tmp = 0
                mu5_tmp += self.gamma[l][k]
                last_term = 1
                for j in range(k+1):    
                    last_term -= self.rho[l][j]
                mu5_tmp -= last_term
                self.mu5[l][k] = self.mu5[l][k] + step_size * mu5_tmp
        
        # update mu6
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv): 
                mu6_tmp = 0
                mu6_tmp += self.tau[l] - (1/self.link_set.links[l].svcRate*(1-self.gamma[l][self.prioritylv-1]))
                self.mu6[l] = self.mu6[l] + step_size * mu6_tmp
        
        # update mu7
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv): 
                mu7_tmp = 0
                mu7_tmp += math.log(self.q[l][k]) - math.log(self.tau[l]) + math.log(self.gamma[l][k-1]) + math.log(self.gamma[l][k])
                self.mu7[l][k] = self.mu7[l][k] + step_size * mu7_tmp
        
        # update mu8
        for l in range(self.link_set.length()):
            for k in range(self.prioritylv): 
                mu8_tmp = 0
                mu8_tmp += self.t[l][k] - self.q[l][k] - (1/self.link_set.links[l].svcRate)
                self.mu8[l][k] = self.mu8[l][k] + step_size * mu8_tmp

        # update mu9
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                for k in range(self.prioritylv):
                    mu9_tmp = 0
                    mu9_tmp += math.log(self.b[w][l][k]) - math.log(self.a[w][l][k]) - math.log(self.t[l][k])
                    self.mu9[w][l][k] = self.mu9[w][l][k] + step_size * mu9_tmp
        
        # update mu10
        for w in range(len(self.odpair_set)):
            for l in range(self.link_set.length()):
                mu10_tmp = 0
                mu10_tmp += self.f[w][l]
                for k in range(self.prioritylv):
                    mu10_tmp -= self.b[w][l][k]
                self.mu10[w][l] = self.mu10[w][l] + step_size * mu10_tmp
        
        # update mu11
        for w in range(len(self.odpair_set)):
            mu11_tmp = 0
            mu11_tmp += self.d[w]
            for l in range(self.link_set.length()):
                mu11_tmp -= self.f[w][l]
            self.mu11[w] = self.mu11[w] + step_size * mu11_tmp
        
        
                
    