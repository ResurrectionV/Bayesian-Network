# import part
import random
from collections import deque
import statistics


# function
def list_stdev(l):
    return statistics.pstdev(l)

def Average(lst):
    return sum(lst) / len(lst)

def randomS(l):
    lnt = len(l)
    rn = random.randint(1, lnt)
    return l[rn - 1]

def normalize(probs):
    prob_factor = 1 / sum(probs)
    return [prob_factor * p for p in probs]

def sortL(l):
    if l == []:
        return l
    count = 0
    for i in l:
        l[count] = int(i)
        count = count + 1
    l.sort()
    count = 0
    for i in l:
        l[count] = str(i)
        count = count + 1
    return l

# bfs
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.parent = None


class lList:
    def __init__(self):
        self.head = None

# class part
class graph:

    def __init__(self):
        self.graph = {}

    def addNode(self, k):
        # neighbours,target, agent, probability, check_position, probability of evidence P(x_t:e_t)
        self.graph[str(k)] = [[], 0, 0, 0, 0, [0,0]]  # 0 means not at the this Node

    def addEdge(self, k, val):
        if len(self.graph[str(k)][0]) == 3:
            # False, not able to add any more edges because it has reached maximal degree
            return 0
        else:
            list_temp = self.graph[str(k)][0]
            list_temp.append(str(val))
            self.graph[str(k)][0] = list_temp
            return 1

    def printNb(self):
        for p1, p2 in self.graph.items():
            if len(p2[0]) == 0:
                print("Node " + p1 + " has no edge.")
            if len(p2[0]) == 1:
                print("The Node " + p1 + " is connected to Node " + p2[0][0] + ".")
            if len(p2[0]) == 2:
                print("The Node " + p1 + " is connected to Nodes " + p2[0][0] + " and " + p2[0][1] + ".")
            if len(p2[0]) == 3:
                print("The Node " + p1 + " is connected to Nodes " + p2[0][0] + ", " + p2[0][1] + ", and " + p2[0][
                    2] + ".")

    def EvnSet(self, numN):
        for i in range(1, numN + 1):
            self.addNode(i)
            if i == numN:
                self.addEdge(i, i - 1)
                self.addEdge(i, 1)
            elif i == 1:
                self.addEdge(i, i + 1)
                self.addEdge(i, numN)
            else:
                self.addEdge(i, i - 1)
                self.addEdge(i, i + 1)
        newEcount = 0
        while not newEcount == 10:
            n1 = randomS(list(self.graph))
            if len(self.graph[n1][0]) == 3:
                continue
            n2 = n1
            while n2 == n1 or n2 in self.graph[n1][0] or len(self.graph[n2][0]) == 3:
                n2 = randomS(list(self.graph))
            self.addEdge(n1, n2)
            self.addEdge(n2, n1)
            newEcount = newEcount + 1
        for i in range(1, numN + 1):
            self.graph[str(i)][0] = sortL(self.graph[str(i)][0])

    def setA(self, pos):
        self.graph[str(pos)][2] = 1

    def setT(self, pos):
        self.graph[str(pos)][1] = 1
        
    def setC(self, pos):
        self.graph[str(pos)][4] = 1

    def printT(self):
        for i in list(self.graph):
            if self.graph[i][1] == 1:
                print("Target is currently located at Node " + i + ".")
                return i

    def printA(self):
        for i in list(self.graph):
            if self.graph[i][2] == 1:
                print("Agent is currently located at Node " + i + ".")
                return i
    
    def printC(self):
        for i in list(self.graph):
            if self.graph[i][4] == 1:
                print("check_position is currently located at Node " + i + ".")
                return i
            
            
    def clearAT(self):
        # function for set all the agent and target as 0
        t = self.printT()
        a = self.printA()
        self.graph[t][1] = 0
        self.graph[a][2] = 0
        print("All the data are reset")
        pass

#-------------------------------------------------------------
#Code for agent0
    def agent0(self):
        start_pos_a = randomS(list(self.graph))
        self.graph[start_pos_a][2] = 1

    def target_randomwalk(self, cur_pos):
        self.graph[cur_pos][1] = 0
        nb_list = self.graph[cur_pos][0]
        next_pos = randomS(nb_list)
        self.graph[next_pos][1] = 1
        
    def agent0_main(self, t_pos):
        self.setT(str(t_pos))
        self.agent0()
        a = self.printA()
        t = self.printT()
        count = 0
        while not t == a:
            self.target_randomwalk(t)
            print("After one timestep move")
            t = self.printT()
            count = count + 1
        if t == a:
            print("Target is catched by agent_0 at position " + t + "!")
            return count
            
        
#-------------------------------------------------------------
#Code for agent1

    
    def bfs(self):
        a_pos = self.printA()
        t_pos = self.printT()
        q = [a_pos]
        visited = []
        ll = lList()
        ll.head = Node(a_pos)
        cur_node = ll.head
        
        
        while not q == []:
            q = deque(q)
            cur = q.popleft()
            q = list(q)
            visited.append(cur)
            check_node = ll.head
            if check_node.data == cur:
                prev_node = check_node
            else:
                while not check_node.data == cur:
                    check_node = check_node.next
                    prev_node = check_node
                    #then we get the parent node which should be assigned to connected node
            
            if cur == t_pos:
                while not prev_node.parent == ll.head:
                    prev_node = prev_node.parent
                return prev_node.data
            
            for item in self.graph[cur][0]:
                if item not in visited:
                    q.append(item)
                    cur_node.next = Node(item)
                    cur_node = cur_node.next
                    cur_node.parent = prev_node
        print("Path not found")
        return False

    def agent1_main(self, t_pos):
        self.setT(t_pos)
        self.agent0()
        a = self.printA()
        t = self.printT()
        count = 0
        if t == a:
            print("Target is catched by agent_0 at position " + t + "!")
            return count
        else:
            while not t == a:
                count = count + 1
                print("After one timestep, Tagret move to:")
                self.target_randomwalk(t)
                t = self.printT()
                if t == a:
                    print("Target is catched by agent_0 at position " + t + "!")
                    return count
                a_next_pos = self.bfs()
                self.graph[a][2] = 0
                self.graph[a_next_pos][2] = 1
                a = a_next_pos
                
                if t == a:
                    print("Target is catched by agent_1 at position " + t + "!")
                    return count
                
        return False
#-------------------------------------------------------------
#Code for agent2
        
    def DFS(self):
        a_pos = self.printA()
        t_pos = self.printT()
        q = [a_pos]
        visited = []
        ll = lList()
        ll.head = Node(a_pos)
        cur_node = ll.head
        
        
        while not q == []:
            cur = q.pop()
            visited.append(cur)
            check_node = ll.head
            if check_node.data == cur:
                prev_node = check_node
            else:
                while not check_node.data == cur:
                    check_node = check_node.next
                    prev_node = check_node
                    #then we get the parent node which should be assigned to connected node
            
            if cur == t_pos:
                while not prev_node.parent == ll.head:
                    prev_node = prev_node.parent
                return prev_node.data
            
            for item in self.graph[cur][0]:
                if item not in visited:
                    q.append(item)
                    cur_node.next = Node(item)
                    cur_node = cur_node.next
                    cur_node.parent = prev_node
        print("Path not found")
        return False

    def agent2_main(self, t_pos):
        self.setT(t_pos)
        self.agent0()
        a = self.printA()
        t = self.printT()
        count = 0
        if t == a:
            print("Target is catched by agent_0 at position " + t + "!")
            return count
        else:
            while not t == a:
                count = count + 1
                print("After one timestep, Tagret move to:")
                self.target_randomwalk(t)
                t = self.printT()
                if t == a:
                    print("Target is catched by agent_0 at position " + t + "!")
                    return count
                a_next_pos = self.DFS()
                self.graph[a][2] = 0
                self.graph[a_next_pos][2] = 1
                a = a_next_pos
                if t == a:
                    print("Target is catched by agent_2 at position " + t + "!")
                    return count
        return False
       
#-------------------------------------------------------------
#Code for agent3
    
    def agent3(self):
        start_pos_a = randomS(list(self.graph))
        self.graph[start_pos_a][2] = 1


    def agent3_main(self, t_pos):
        self.setT(str(t_pos))
        self.agent0()
        self.setA(str(random.randrange(1,40)))
        a = self.printA()
        t = self.printT()
        print("Checked position is at " + a)
        count = 0
        while not t == a:
            self.target_randomwalk(t)
            #print("After one timestep move")
            t = self.printT()
            print("After one timestep, target is at " + t)
            print("--------------------------------------------------")
            count = count + 1
        if t == a:
            print("Target is catched by agent_3 at position " + t + "!")
            return count
            
            
            
#-------------------------------------------------------------
#Code for agent4
    
    def agent4(self):
        prev_state = []
        new_state = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prev_state.append(item)
        for i in prev_state:
            for j in self.graph[i][0]:
                if j not in new_state:
                    new_state.append(j)
        
        for item in new_state:
            prob = 0
            for j in self.graph[item][0]:
                if not self.graph[j][3] == 0:
                    prob = prob + (1/len(self.graph[j][0]))*self.graph[j][3]
            self.graph[item][3] = prob
        
        for item in prev_state:
            self.graph[item][3] = 0
            
        normalize_list_pos = []
        normalize_list_value = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                normalize_list_pos.append(item)
                normalize_list_value.append(self.graph[item][3])
        #print(normalize_list_pos)
        #print(normalize_list_value)
        normalize_list_value = normalize(normalize_list_value)
        #print(normalize_list_value)
        for item in range(len(normalize_list_pos)):
            self.graph[normalize_list_pos[item]][3] = normalize_list_value[item]
        print("List of position that contains probability")
        print(normalize_list_pos)
        print("List of values of estimated probability corresponding to positions")
        print(normalize_list_value)
        print("------------------------------------------")
        print()
        print()
    
    
    def agent4_main(self):
        #randomly select a position to start
        check_pos = randomS(list(self.graph))
        for item in self.graph[check_pos][0]:
            self.graph[item][3] = 1/len(self.graph[check_pos][0])
        prob_list = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prob_list.append(item)
        
        t_pos = randomS(list(self.graph))
        if t_pos == check_pos:
            print("Target is found at our check_position " + check_pos + "!")
            return True
        print("----------------------------------")
        print("The check_position is currently at " + check_pos)
        print("The target_position is currently at " + t_pos)
        print()
        print(prob_list)
        prob_list_value = []
        for item in prob_list:
            prob_list_value.append(self.graph[item][3])
        print(prob_list_value)
        
        count = 0
        while not check_pos == t_pos:
            highest_prob_list = []
            prob_list = []
            highest_prob = 0
            print("After a timestep:")
            self.target_randomwalk(t_pos)
            t_pos = self.printT()
            
            for item in list(self.graph):
                if not self.graph[item][3] == 0:
                    prob_list.append(item)
            for item in prob_list:
                if self.graph[item][3] > highest_prob:
                    highest_prob_list = []
                    highest_prob = self.graph[item][3]
                    highest_prob_list.append(item)
                    continue
                if self.graph[item][3] == highest_prob:
                    highest_prob_list.append(item)
            check_pos = randomS(highest_prob_list)
            print("----------------------------------")
            print("The check_position is currently at " + check_pos)
            print("The target_position is currently at " + t_pos)
            print()
            if check_pos == t_pos:
                print("Target is found at our check_position " + check_pos + "!")
                return count
            self.graph[check_pos][3] = 0
            self.agent4()
            count = count + 1


#-------------------------------------------------------------
#Code for agent5
    def agent5(self):
        prev_state = []
        new_state = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prev_state.append(item)
        for i in prev_state:
            for j in self.graph[i][0]:
                if j not in new_state:
                    new_state.append(j)
        
        for item in new_state:
            prob = 0
            prob_1 = 0
            prob_2 = 0
            for j in self.graph[item][0]:
                if not self.graph[j][3] == 0:
                    prob = prob + (1/len(self.graph[j][0]))*randomS(self.graph[j][5])
                    prob_1 = prob_1  + (1/len(self.graph[j][0]))*self.graph[j][5][0]
                    prob_2 = prob_2  + (1/len(self.graph[j][0]))*self.graph[j][5][1]
            self.graph[item][3] = prob
            self.graph[item][5][0] = prob_1 * 0.7
            self.graph[item][5][1] = prob_2 * 0.4
            self.graph[item][5] = normalize(self.graph[item][5])
        
        for item in prev_state:
            self.graph[item][3] = 0
            
        normalize_list_pos = []
        normalize_list_value = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                normalize_list_pos.append(item)
                normalize_list_value.append(self.graph[item][3])
        #print(normalize_list_pos)
        #print(normalize_list_value)
        normalize_list_value = normalize(normalize_list_value)
        #print(normalize_list_value)
        for item in range(len(normalize_list_pos)):
            self.graph[normalize_list_pos[item]][3] = normalize_list_value[item]
        print("List of position that contains probability")
        print(normalize_list_pos)
        print("List of values of estimated probability corresponding to positions")
        print(normalize_list_value)
        print("------------------------------------------")
        print()
        print()
        
        
    def agent5_step1(self):
        prev_state = []
        new_state = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prev_state.append(item)
        for i in prev_state:
            for j in self.graph[i][0]:
                if j not in new_state:
                    new_state.append(j)
        
        for item in new_state:
            prob = 0
            prob_1 = 0
            prob_2 = 0
            for j in self.graph[item][0]:
                if not self.graph[j][3] == 0:
                    prob = prob + (1/len(self.graph[j][0]))*randomS([0.7,0.4])
                    prob_1 = prob_1  + (1/len(self.graph[j][0]))*self.graph[j][3]
                    prob_2 = prob_2  + (1/len(self.graph[j][0]))*self.graph[j][3]
            self.graph[item][3] = prob
            self.graph[item][5][0] = prob_1 * 0.7
            self.graph[item][5][1] = prob_2 * 0.4
            self.graph[item][5] = normalize(self.graph[item][5])
        
        for item in prev_state:
            self.graph[item][3] = 0
            
        normalize_list_pos = []
        normalize_list_value = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                normalize_list_pos.append(item)
                normalize_list_value.append(self.graph[item][3])
        #print(normalize_list_pos)
        #print(normalize_list_value)
        normalize_list_value = normalize(normalize_list_value)
        #print(normalize_list_value)
        for item in range(len(normalize_list_pos)):
            self.graph[normalize_list_pos[item]][3] = normalize_list_value[item]
        print("List of position that contains probability")
        print(normalize_list_pos)
        print("List of values of estimated probability corresponding to positions")
        print(normalize_list_value)
        print("------------------------------------------")
        print()
        print()



    def agent5_main(self):
        #randomly select a position to start
        check_pos = randomS(list(self.graph))
        for item in self.graph[check_pos][0]:
            self.graph[item][3] = 1/len(self.graph[check_pos][0])
        prob_list = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prob_list.append(item)
        
        t_pos = randomS(list(self.graph))
        if t_pos == check_pos:
            print("Target is found at our check_position " + check_pos + "!")
            return True
        print("----------------------------------")
        print("The check_position is currently at " + check_pos)
        print("The target_position is currently at " + t_pos)
        print()
        print(prob_list)
        prob_list_value = []
        for item in prob_list:
            prob_list_value.append(self.graph[item][3])
        print(prob_list_value)
        
        count = 0
        while not check_pos == t_pos:
            highest_prob_list = []
            prob_list = []
            highest_prob = 0
            print("After a timestep:")
            self.target_randomwalk(t_pos)
            t_pos = self.printT()
            
            for item in list(self.graph):
                if not self.graph[item][3] == 0:
                    prob_list.append(item)
            for item in prob_list:
                if self.graph[item][3] > highest_prob:
                    highest_prob_list = []
                    highest_prob = self.graph[item][3]
                    highest_prob_list.append(item)
                    continue
                if self.graph[item][3] == highest_prob:
                    highest_prob_list.append(item)
            check_pos = randomS(highest_prob_list)
            print("----------------------------------")
            print("The check_position is currently at " + check_pos)
            print("The target_position is currently at " + t_pos)
            print()
            if check_pos == t_pos:
                print("Target is found at our check_position " + check_pos + "!")
                return count
            self.graph[check_pos][3] = 0
            if count == 0:
                self.agent5_step1()
            else:
                self.agent5()
            
            for item in list(self.graph):
                if self.graph[item][3] > 0:
                    print(item)
                    print("Probability of moving to this position")
                    print(self.graph[item][3])
                    print("Probability of evidence assigned to this position")
                    print(self.graph[item][5])
                    print("--------------------------------")
            count = count + 1






#-------------------------------------------------------------
#Code for agent6
    def bfs_agent6(self):
        a_pos = self.printA()
        c_pos = self.printC()
        if a_pos == c_pos:
            return a_pos
        q = [a_pos]
        visited = []
        ll = lList()
        ll.head = Node(a_pos)
        cur_node = ll.head
        
        
        while not q == []:
            q = deque(q)
            cur = q.popleft()
            q = list(q)
            visited.append(cur)
            check_node = ll.head
            if check_node.data == cur:
                prev_node = check_node
            else:
                while not check_node.data == cur:
                    check_node = check_node.next
                    prev_node = check_node
                    #then we get the parent node which should be assigned to connected node
            
            if cur == c_pos:
                while not prev_node.parent == ll.head:
                    prev_node = prev_node.parent
                return prev_node.data
            
            for item in self.graph[cur][0]:
                if item not in visited:
                    q.append(item)
                    cur_node.next = Node(item)
                    cur_node = cur_node.next
                    cur_node.parent = prev_node
        print("Path not found")
        return False
    
    
    def agent6(self):
        prev_state = []
        new_state = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prev_state.append(item)
        for i in prev_state:
            for j in self.graph[i][0]:
                if j not in new_state:
                    new_state.append(j)
        
        for item in new_state:
            prob = 0
            for j in self.graph[item][0]:
                if not self.graph[j][3] == 0:
                    prob = prob + (1/len(self.graph[j][0]))*self.graph[j][3]
            self.graph[item][3] = prob
        
        for item in prev_state:
            self.graph[item][3] = 0
            
        normalize_list_pos = []
        normalize_list_value = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                normalize_list_pos.append(item)
                normalize_list_value.append(self.graph[item][3])
        #print(normalize_list_pos)
        #print(normalize_list_value)
        normalize_list_value = normalize(normalize_list_value)
        #print(normalize_list_value)
        for item in range(len(normalize_list_pos)):
            self.graph[normalize_list_pos[item]][3] = normalize_list_value[item]
        print("List of position that contains probability")
        print(normalize_list_pos)
        print("List of values of estimated probability corresponding to positions")
        print(normalize_list_value)
        print("------------------------------------------")
        print()
        print()
    
    def agent6_main(self):
        #randomly select a position to start
        check_pos = randomS(list(self.graph))
        agent_pos = randomS(list(self.graph))
        self.setC(check_pos)
        self.setA(agent_pos)
        for item in self.graph[check_pos][0]:
            self.graph[item][3] = 1/len(self.graph[check_pos][0])
        prob_list = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prob_list.append(item)
        
        t_pos = randomS(list(self.graph))
        self.setT(t_pos)
        if t_pos == agent_pos:
            print("Target is catched by agent 6 at position " + agent_pos + "!")
            return True
        print("----------------------------------")
        print("The check_position is currently at " + check_pos)
        print("The target_position is currently at " + t_pos)
        print()
        print(prob_list)
        prob_list_value = []
        for item in prob_list:
            prob_list_value.append(self.graph[item][3])
        print(prob_list_value)
        
        count = 0
        while not agent_pos == t_pos:
            highest_prob_list = []
            prob_list = []
            highest_prob = 0
            print("After a timestep:")
            self.target_randomwalk(t_pos)
            t_pos = self.printT()
            
            for item in list(self.graph):
                if not self.graph[item][3] == 0:
                    prob_list.append(item)
            for item in prob_list:
                if self.graph[item][3] > highest_prob:
                    highest_prob_list = []
                    highest_prob = self.graph[item][3]
                    highest_prob_list.append(item)
                    continue
                if self.graph[item][3] == highest_prob:
                    highest_prob_list.append(item)
            check_pos = randomS(highest_prob_list)
            agent_next_pos = self.bfs_agent6()
            self.graph[agent_pos][2] = 0
            agent_pos = agent_next_pos
            self.graph[agent_pos][2] = 1
            print("----------------------------------")
            print("The check_position is currently at " + check_pos)
            print("The target_position is currently at " + t_pos)
            print("The agent_position is currently at " + agent_pos)
            print()
            if agent_pos == t_pos:
                print("Target is catched by agent 6 at position " + agent_pos + "!")
                return count
            self.graph[check_pos][3] = 0
            self.agent6()
            count = count + 1

    
#-------------------------------------------------------------
#Code for agent7

    def bfs_agent7(self):
        a_pos = self.printA()
        c_pos = self.printC()
        if a_pos == c_pos:
            return a_pos
        q = [a_pos]
        visited = []
        ll = lList()
        ll.head = Node(a_pos)
        cur_node = ll.head
        
        
        while not q == []:
            q = deque(q)
            cur = q.popleft()
            q = list(q)
            visited.append(cur)
            check_node = ll.head
            if check_node.data == cur:
                prev_node = check_node
            else:
                while not check_node.data == cur:
                    check_node = check_node.next
                    prev_node = check_node
                    #then we get the parent node which should be assigned to connected node
            
            if cur == c_pos:
                while not prev_node.parent == ll.head:
                    prev_node = prev_node.parent
                return prev_node.data
            
            for item in self.graph[cur][0]:
                if item not in visited:
                    q.append(item)
                    cur_node.next = Node(item)
                    cur_node = cur_node.next
                    cur_node.parent = prev_node
        print("Path not found")
        return False
    
    
    def agent7(self):
        prev_state = []
        new_state = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prev_state.append(item)
        for i in prev_state:
            for j in self.graph[i][0]:
                if j not in new_state:
                    new_state.append(j)
        
        for item in new_state:
            prob = 0
            prob_1 = 0
            prob_2 = 0
            for j in self.graph[item][0]:
                if not self.graph[j][3] == 0:
                    prob = prob + (1/len(self.graph[j][0]))*randomS(self.graph[j][5])
                    prob_1 = prob_1  + (1/len(self.graph[j][0]))*self.graph[j][5][0]
                    prob_2 = prob_2  + (1/len(self.graph[j][0]))*self.graph[j][5][1]
            self.graph[item][3] = prob
            self.graph[item][5][0] = prob_1 * 0.7
            self.graph[item][5][1] = prob_2 * 0.4
            self.graph[item][5] = normalize(self.graph[item][5])
        
        for item in prev_state:
            self.graph[item][3] = 0
            
        normalize_list_pos = []
        normalize_list_value = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                normalize_list_pos.append(item)
                normalize_list_value.append(self.graph[item][3])
        #print(normalize_list_pos)
        #print(normalize_list_value)
        normalize_list_value = normalize(normalize_list_value)
        #print(normalize_list_value)
        for item in range(len(normalize_list_pos)):
            self.graph[normalize_list_pos[item]][3] = normalize_list_value[item]
        print("List of position that contains probability")
        print(normalize_list_pos)
        print("List of values of estimated probability corresponding to positions")
        print(normalize_list_value)
        print("------------------------------------------")
        print()
        print()
        
        
    def agent7_step1(self):
        prev_state = []
        new_state = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prev_state.append(item)
        for i in prev_state:
            for j in self.graph[i][0]:
                if j not in new_state:
                    new_state.append(j)
        
        for item in new_state:
            prob = 0
            prob_1 = 0
            prob_2 = 0
            for j in self.graph[item][0]:
                if not self.graph[j][3] == 0:
                    prob = prob + (1/len(self.graph[j][0]))*randomS([0.7,0.4])
                    prob_1 = prob_1  + (1/len(self.graph[j][0]))*self.graph[j][3]
                    prob_2 = prob_2  + (1/len(self.graph[j][0]))*self.graph[j][3]
            self.graph[item][3] = prob
            self.graph[item][5][0] = prob_1 * 0.7
            self.graph[item][5][1] = prob_2 * 0.4
            self.graph[item][5] = normalize(self.graph[item][5])
        
        for item in prev_state:
            self.graph[item][3] = 0
            
        normalize_list_pos = []
        normalize_list_value = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                normalize_list_pos.append(item)
                normalize_list_value.append(self.graph[item][3])
        #print(normalize_list_pos)
        #print(normalize_list_value)
        normalize_list_value = normalize(normalize_list_value)
        #print(normalize_list_value)
        for item in range(len(normalize_list_pos)):
            self.graph[normalize_list_pos[item]][3] = normalize_list_value[item]
        print("List of position that contains probability")
        print(normalize_list_pos)
        print("List of values of estimated probability corresponding to positions")
        print(normalize_list_value)
        print("------------------------------------------")
        print()
        print()

    
    def agent7_main(self):
        #randomly select a position to start
        check_pos = randomS(list(self.graph))
        agent_pos = randomS(list(self.graph))
        self.setC(check_pos)
        self.setA(agent_pos)
        for item in self.graph[check_pos][0]:
            self.graph[item][3] = 1/len(self.graph[check_pos][0])
        prob_list = []
        for item in list(self.graph):
            if not self.graph[item][3] == 0:
                prob_list.append(item)
        
        t_pos = randomS(list(self.graph))
        self.setT(t_pos)
        if t_pos == agent_pos:
            print("Target is catched by agent 6 at position " + agent_pos + "!")
            return True
        print("----------------------------------")
        print("The check_position is currently at " + check_pos)
        print("The target_position is currently at " + t_pos)
        print()
        print(prob_list)
        prob_list_value = []
        for item in prob_list:
            prob_list_value.append(self.graph[item][3])
        print(prob_list_value)
        
        count = 0
        while not agent_pos == t_pos:
            highest_prob_list = []
            prob_list = []
            highest_prob = 0
            print("After a timestep:")
            self.target_randomwalk(t_pos)
            t_pos = self.printT()
            
            for item in list(self.graph):
                if not self.graph[item][3] == 0:
                    prob_list.append(item)
            for item in prob_list:
                if self.graph[item][3] > highest_prob:
                    highest_prob_list = []
                    highest_prob = self.graph[item][3]
                    highest_prob_list.append(item)
                    continue
                if self.graph[item][3] == highest_prob:
                    highest_prob_list.append(item)
            check_pos = randomS(highest_prob_list)
            agent_next_pos = self.bfs_agent6()
            self.graph[agent_pos][2] = 0
            agent_pos = agent_next_pos
            self.graph[agent_pos][2] = 1
            print("----------------------------------")
            print("The check_position is currently at " + check_pos)
            print("The target_position is currently at " + t_pos)
            print("The agent_position is currently at " + agent_pos)
            print()
            if agent_pos == t_pos:
                print("Target is catched by agent 7 at position " + agent_pos + "!")
                return count
            self.graph[check_pos][3] = 0
            if count == 0:
                self.agent5_step1()
            else:
                self.agent5()
            count = count + 1
    
    def clearG(self):
        for item in list(self.graph):
            self.graph[item][1] = 0
            self.graph[item][2] = 0
            self.graph[item][3] = 0
            self.graph[item][4] = 0
            self.graph[item][5] = [0, 0]

# test part
count_list = []
g = graph()
g.EvnSet(40)
g.printNb()
for i in range(10000):
    count_list.append(g.agent2_main(29))
    g.clearG()
print("Run the code 2000 times: ")
print("The average number of steps is " + str(Average(count_list)) + "!")
print("The standard deviation of number of steps is " + str(list_stdev(count_list)) + "!")
""" Test for agent 0
g = graph()
g.EvnSet(40)
g.printNb()
g.agent0_main(29)
"""


"""Test for agent 1
g = graph()
g.EvnSet(40)
g.printNb()
g.agent1_main(29)
"""

"""Test for agent 2
g = graph()
g.EvnSet(40)
g.printNb()
g.agent2_main(29)
"""

"""Test for agent3
g = graph()
g.EvnSet(40)
g.printNb(29)
print("The total steps in this example is " + str(g.agent3_main()))
"""