import Distance_Fetch_3
import pandas as pd

class Nation:
    def __init__(self, name, power_tier,zone):#Power Tier are 0,1 and 2 Zones are 0,1,2 and 3
        self.name = name
        self.power_tier = power_tier
        self.zone = zone
        #these 3 below indicate no of troops
        self.btroops = 0
        self.ntroops = 0
        self.atroops = 0
        self.total_power = self.btroops*1 + self.ntroops*1.2 + self.atroops*1.5
        self.btroops_p = 1*self.btroops
        self.ntroops_p = 1.2*self.ntroops
        self.atroops_p = 1.5*self.atroops
        self.health = 0
        self.bt_ratio = 0
        self.nt_ratio = 0
        self.at_ratio = 0
        self.n_upgrade = False
        self.f_upgrade = False
        if self.power_tier == 0 : 
            self.health = 100
            self.max_troops = 700
        if self.power_tier == 1 : 
            self.health = 300
            self.max_troops = 1200
        if self.power_tier == 2 : 
            self.health = 500
            self.max_troops = 1800
        
    def set_power(self) :
        try:
            self.total_power = self.btroops*1 + self.ntroops*1.2 + self.atroops*1.5
            self.btroops_p = 1*self.btroops
            self.ntroops_p = 1.2*self.ntroops
            self.atroops_p = 1.5*self.atroops
            if self.total_power == 0 :
                self.bt_ratio = 0
                self.nt_ratio = 0
                self.at_ratio = 0
            self.bt_ratio = self.btroops_p/self.total_power
            self.nt_ratio = self.ntroops_p/self.total_power
            self.at_ratio = self.atroops_p/self.total_power
        except ZeroDivisionError:
            self.bt_ratio = 0
            self.nt_ratio = 0
            self.at_ratio = 0
    

    def print(self) : 
        print(" Name of the Nation : \t ",self.name, "\n Power Tier : \t ",self.power_tier , "\n Zone : \t" , self.zone ,"\n Total base troops : \t",self.btroops,
              "\n Total naval troops : \t",self.ntroops,"\n Total air troops : \t",self.atroops) #self.zone and self.powerlevel will be implemented as function def get_zone()


class Troop : 
    def __init__(self,level):
        self.level = level
        if self.level == 0 : 
            self.conversion_cost = 0
            self.attack_power = 1
            self.max_distance = 9000
            self.maintenance_cost = 10
        if self.level == 1 : 
            self.conversion_cost = 100
            self.attack_power = 1.2
            self.max_distance = 12000
            self.maintenance_cost = 20
        if self.level == 2 :
            self.conversion_cost = 250
            self.attack_power = 1.5
            self.max_distance = 900000000000
            self.maintenance_cost = 50

class Team:
    def __init__(self, name):
        self.name = name
        self.nations = []
        self.synergy = 0
        self.synergy_score = 0
        self.n_upgrade = False
        self.f_upgrade = False
        self.bt = Troop(0)
        self.nt = Troop(1)
        self.at = Troop(2)
        self.corpus = 1200000  # $1.2 million gold bars

    def set_nations(self, n1, n2, n3) : #The arguements should be put as nation example set_nations(Nation(America,2),...)
        self.nations.append(n1)
        self.nations.append(n2)
        self.nations.append(n3)

    def calculate_synergy_score(self,syn1,syn2,syn3,syn4,syn5,syn6):
        if len(self.nations) != 3:
            raise ValueError("Each team must have exactly three nations.")
        self.synergy_score = (syn1 + syn2 + syn3 + syn4 + syn5 + syn6) / 6 #Synergy needs to be transformed to synergy score or else relpace synergy by synergy score

    def set_synergy_direct(self,synergy) : 
        self.synergy_score = synergy

    def distribute_troops(self, nation, btroops, ntroops, atroops): #nation should be an integer value 0,1 or 2
        if btroops + ntroops + atroops > self.nations[nation].max_troops:
            raise ValueError("Total troop count exceeds limit. for : ", "Team : " ,self.name ,"and Nation : " ,self.nations[nation].name)
        
        self.nations[nation].btroops = btroops
        self.nations[nation].ntroops = ntroops
        self.nations[nation].atroops = atroops
        self.nations[nation].total_troops = self.nations[nation].btroops + self.nations[nation].ntroops + self.nations[nation].atroops
        self.nations[nation].set_power()
        total_cost = (ntroops*self.nt.conversion_cost) + (atroops*self.at.conversion_cost)
        self.corpus = self.corpus - total_cost

    def add_troops(self, nation, btroops, ntroops, atroops) : 
        return 0 

    def calculate_attack(self, nation,bt,nt,at): #attacking nation should be integer
        land_attack = bt*self.bt.attack_power
        naval_attack = nt*self.nt.attack_power
        air_attack = at*self.at.attack_power
        if self.nations[nation].n_upgrade :
            n_multiplier = 2
        else : 
            n_multiplier = 1
        attack_power = (land_attack + naval_attack + air_attack)*self.synergy_score*n_multiplier
        return attack_power 
    
    def calculate_attack_cost(self,nation,distance,bt,nt,at) :
        land_attack = bt*10
        naval_attack = nt*25
        air_attack = at*50
        total_cost  = (land_attack + naval_attack + air_attack)*(distance/1000)
        if total_cost > self.corpus : 
            raise ValueError(f"The total cost for attack is greater than the corpus for team {self.name}")
        print(f"Total cost: {total_cost}")
        return int(total_cost)
    
    def calculate_reallocation_cost(self, sending_nation, receiving_nation ,btroops,ntroops,atroops,distance) : 
        land_attack = btroops*2
        naval_attack = ntroops*5
        air_attack = atroops*8
        total_cost = (land_attack + naval_attack + air_attack)*distance/1000
        if total_cost > self.corpus : 
            raise ValueError(f"The total cost for attack is greater than the corpus for team {self.name}")
        return int(total_cost)

    def calculate_defense(self, nation) : #defending nation should be integer
        land_def = self.nations[nation].btroops*self.bt.attack_power
        naval_def = self.nations[nation].ntroops*self.nt.attack_power
        air_def = self.nations[nation].atroops*self.at.attack_power
        if self.nations[nation].zone == 0 : 
            air_def *= 1.2
        elif self.nations[nation].zone == 1 : 
            land_def *= 1.2
        elif self.nations[nation].zone == 2 : 
            naval_def *= 1.2
        elif self.nations[nation].zone == 3 : 
            land_def *= 1.05
            naval_def *= 1.05
            air_def *= 1.05
    
        def_power = (land_def + naval_def + air_def)*self.synergy_score
        return def_power

    def buy_nuclear_upgrade(self,nation,black_market=False): 
        self.nations[nation].n_upgrade = True
        if not black_market:
            if self.corpus < 120000 : 
                raise ValueError(f"Team {self.name} cannot afford nuclear")
            self.corpus -= 120000
        else:
            if self.corpus < 30000 : 
                raise ValueError(f"Team {self.name} cannot afford nuclear")
            self.corpus -= 30000

    def buy_fortification_upgrade(self,nation,black_market=False): 
        self.nations[nation].f_upgrade = True
        if  not black_market:
            if self.corpus < 120000 : 
                raise ValueError(f"Team {self.name} cannot afford fortification")
            self.corpus -= 120000
        else:
            if self.corpus < (30000) : 
                raise ValueError(f"Team {self.name} cannot afford fortification")
            self.corpus -= 30000
    
    def peace_table(self) :
        total_cost = 0 
        for i in range(len(self.nations)) : 
            base_cost = self.nations[i].btroops*(self.bt.maintenance_cost)
            naval_cost = self.nations[i].ntroops*(self.nt.maintenance_cost)
            air_cost = self.nations[i].atroops*(self.at.maintenance_cost)
            total_cost += base_cost + naval_cost + air_cost
        if total_cost > self.corpus : 
            raise ValueError(f"The total cost for maintainenece is greater than the corpus for team {self.name}, and hence will be eliminated")
        self.corpus -= total_cost
        print("Value deducted successfully")

    def peace_table_no_funds(self,nation,btroops,ntroops,atroops) :
        base_cost = btroops*(self.bt.maintenance_cost)
        naval_cost = ntroops*(self.nt.maintenance_cost)
        air_cost = atroops*(self.at.maintenance_cost)
        total_cost = base_cost + naval_cost + air_cost
        if total_cost < self.corpus : 
            raise ValueError("The total cost for maintainenece is greater than the corpus")
        self.corpus -= total_cost
    
    def remove_nation(team,nation) : 
        team.nations.pop(nation)
    
    def update_ratio(self,nation) :
        self.nations[nation].set_power()

    def economic_crisis(self):
        self.corpus *= 0.8

    def print(self) :
        '''
        print("Team Name : \t" , self.name)
        print("Nations :")
        print("Money : \t",self.corpus)
        print("Synergy : \t",self.synergy_score)
        for i in range(len(self.nations)) : 
            self.nations[i].print()
        '''
        print(pd.DataFrame([[self.name],[self.corpus],[self.synergy_score]],index=['Team Name','Money','Synergy']))
        index=[nation.name for nation in self.nations]
        columns=["Army","Navy","Air Force","Health"]
        stats=[[nation.btroops,nation.ntroops,nation.atroops,nation.health] for nation in self.nations]
        display=pd.DataFrame(stats,index=index,columns=columns)
        print(display)
        print([[nation.f_upgrade,nation.n_upgrade] for nation in self.nations])
        #for i in range(len(self.nations)) : 
            #self.nations[i].print()

def attack(team_1,team_2,attacking_nation,defending_nation,bt,nt,at) : #Attacking and Defending Nation should be integers
    print(f'{team_1.name}:{team_1.nations[attacking_nation].name} attacks {team_2.name}:{team_2.nations[defending_nation].name}')
    distance=Distance_Fetch_3.fetch_dist(team_1.nations[attacking_nation].name,team_2.nations[defending_nation].name)
    f_multiplier=1
    # add exception to check if the attacking nations have these troops available
    if (bt > team_1.nations[attacking_nation].btroops) or (nt > team_1.nations[attacking_nation].ntroops) or (at > team_1.nations[attacking_nation].atroops) : 
        raise ValueError(f"Not enough troops available with team : {team_1.name}, Nation  {team_1.nations[attacking_nation].name}")
    if (attacking_nation > len(team_1.nations) - 1) : 
        raise ValueError("Attacking Nation out of bounds for : ",team_1.name)
    if (defending_nation > len(team_2.nations) - 1) : 
        raise ValueError("Defending Nation out of bounds for : ",team_2.name) 
    if team_2.nations[defending_nation].f_upgrade :
        f_multiplier = 0.7
    else : 
        f_multiplier = 1
    team_2.update_ratio(defending_nation)
    total_troop_power = bt + 1.2*nt + 1.5*at
    bt_ratio = bt/total_troop_power
    nt_ratio = 1.2*nt/total_troop_power
    at_ratio = 1.5*at/total_troop_power
    attack = (team_1.calculate_attack(attacking_nation,bt,nt,at))*f_multiplier
    team_1.nations[attacking_nation].btroops -= bt
    team_1.nations[attacking_nation].ntroops -= nt
    team_1.nations[attacking_nation].atroops -= at
    
    attack_cost = team_1.calculate_attack_cost(attacking_nation,distance,bt,nt,at)
    team_1.corpus -= attack_cost
    team_1.nations[attacking_nation].n_upgrade = False
    team_2.nations[defending_nation].f_upgrade = False
    defense = team_2.calculate_defense(defending_nation)
    damage = attack - defense
    attack1 = attack/team_2.synergy_score
    print(f"{team_1.nations[attacking_nation].name} inflicts {damage} damage on {team_2.nations[defending_nation].name}")
    if damage < 0 :  
        if f_multiplier == 1 : 
            if team_2.nations[defending_nation].zone == 0 : 
                team_2.nations[defending_nation].btroops -= int(attack1*team_2.nations[defending_nation].bt_ratio/1)
                team_2.nations[defending_nation].ntroops -= int(attack1*team_2.nations[defending_nation].nt_ratio/1.2)
                team_2.nations[defending_nation].atroops -= int(attack1*team_2.nations[defending_nation].at_ratio/(1.5*1.2))  
            if team_2.nations[defending_nation].zone == 1 : 
                team_2.nations[defending_nation].btroops -= int(attack1*team_2.nations[defending_nation].bt_ratio/(1*1.2))
                team_2.nations[defending_nation].ntroops -= int(attack1*team_2.nations[defending_nation].nt_ratio/1.2)
                team_2.nations[defending_nation].atroops -= int(attack1*team_2.nations[defending_nation].at_ratio/1.5)
            if team_2.nations[defending_nation].zone == 2 : 
                team_2.nations[defending_nation].btroops -= int(attack1*team_2.nations[defending_nation].bt_ratio/1)
                team_2.nations[defending_nation].ntroops -= int(attack1*team_2.nations[defending_nation].nt_ratio/(1.2*1.2))
                team_2.nations[defending_nation].atroops -= int(attack1*team_2.nations[defending_nation].at_ratio/1.5) 
            if team_2.nations[defending_nation].zone == 3 : 
                team_2.nations[defending_nation].btroops -= int(attack1*team_2.nations[defending_nation].bt_ratio/(1*1.05))
                team_2.nations[defending_nation].ntroops -= int(attack1*team_2.nations[defending_nation].nt_ratio/(1.2*1.05))
                team_2.nations[defending_nation].atroops -= int(attack1*team_2.nations[defending_nation].at_ratio/(1.5*1.05))
            print("F multiplier 1")
        if f_multiplier == 0.7 :
            if team_2.nations[defending_nation].zone == 0 : 
                team_2.nations[defending_nation].btroops -= int((attack1*team_2.nations[defending_nation].bt_ratio)*0.7)
                team_2.nations[defending_nation].ntroops -= int((attack1*team_2.nations[defending_nation].nt_ratio*0.7))
                team_2.nations[defending_nation].atroops -= int((attack1*team_2.nations[defending_nation].at_ratio/1.2)*0.7)  
            if team_2.nations[defending_nation].zone == 1 : 
                team_2.nations[defending_nation].btroops -= int((attack1*team_2.nations[defending_nation].bt_ratio/1.2)*0.7)
                team_2.nations[defending_nation].ntroops -= int((attack1*team_2.nations[defending_nation].nt_ratio)*0.7)
                team_2.nations[defending_nation].atroops -= int((attack1*team_2.nations[defending_nation].at_ratio)*0.7)
            if team_2.nations[defending_nation].zone == 2 : 
                team_2.nations[defending_nation].btroops -= int((attack1*team_2.nations[defending_nation].bt_ratio)*0.7)
                team_2.nations[defending_nation].ntroops -= int((attack1*team_2.nations[defending_nation].nt_ratio/1.2)*0.7)
                team_2.nations[defending_nation].atroops -= int((attack1*team_2.nations[defending_nation].at_ratio)*0.7) 
            if team_2.nations[defending_nation].zone == 3 : 
                team_2.nations[defending_nation].btroops -= int((attack1*team_2.nations[defending_nation].bt_ratio/1.05)*0.7)
                team_2.nations[defending_nation].ntroops -= int((attack1*team_2.nations[defending_nation].nt_ratio/1.05)*0.7)
                team_2.nations[defending_nation].atroops -= int((attack1*team_2.nations[defending_nation].at_ratio/1.05)*0.7)
            print("F multiplier 2")

        if team_2.nations[defending_nation].btroops < 0 : 
            team_2.nations[defending_nation].btroops = 0
        if team_2.nations[defending_nation].ntroops < 0 : 
            team_2.nations[defending_nation].ntroops = 0
        if team_2.nations[defending_nation].atroops < 0 : 
            team_2.nations[defending_nation].atroops = 0

            
            
    if damage > 0 :
        damage1 = damage/(team_1.synergy_score)
        team_2.nations[defending_nation].btroops = 0
        team_2.nations[defending_nation].ntroops = 0
        team_2.nations[defending_nation].atroops = 0
        team_2.nations[defending_nation].health -= damage
        if team_2.nations[defending_nation].health < 0 : 
            team_2.nations[defending_nation].health = 0
        print("Health Left ; \t",team_2.nations[defending_nation].health)
        if team_2.nations[defending_nation].health == 0 : 
            print(team_2.nations[defending_nation].name,"  destroyed !!!")
            team_2.nations.pop(defending_nation)
            
        print(team_1.nations[attacking_nation].bt_ratio,"bt ratio of at \n")
        team_1.nations[attacking_nation].btroops += min(int(damage1*bt_ratio/1),(bt-5))
        team_1.nations[attacking_nation].ntroops += min(int(damage1*nt_ratio/1.2),(nt-5))
        team_1.nations[attacking_nation].atroops += min(int(damage1*at_ratio/1.5),(at-5))
        print("Attack troops returning \n")
    print("---------------------------------------------------------")


    
    return damage 
    


def reallocate(team,sending_nation, receiving_nation ,btroops,ntroops,atroops) : #sending and receving nations are integers
    if (btroops > team.nations[sending_nation].btroops) or (ntroops > team.nations[sending_nation].ntroops) or (atroops > team.nations[sending_nation].atroops) : 
        raise ValueError("Not enough troops available with team : \t",team.name ,"Nation \t" ,team.nations[sending_nation].name)
    distance=Distance_Fetch_3.fetch_dist(team.nations[sending_nation].name,team.nations[receiving_nation].name)
    cost = team.calculate_reallocation_cost(sending_nation, receiving_nation ,btroops,ntroops,atroops,distance)
    team.nations[sending_nation].btroops -= btroops
    team.nations[sending_nation].ntroops -= ntroops
    team.nations[sending_nation].atroops -= atroops
    team.nations[receiving_nation].btroops += btroops
    team.nations[receiving_nation].ntroops += ntroops
    team.nations[receiving_nation].atroops += atroops
    team.update_ratio(receiving_nation)
    team.update_ratio(sending_nation)
    team.corpus -= cost


def trade(team1,team2,nation1,nation2) : 
    nation = team1.nations[nation1]
    team1.nations[nation1] = team2.nations[nation2]
    team2.nations[nation2] = nation

    
def check_troops(teams) : 
    for i in range(len(teams)) : 
        total_troops = 0
        for ii in range(len(teams[i].nations)) : 
            total_troops += teams[i].nations[ii].btroops
            total_troops += teams[i].nations[ii].ntroops
            total_troops += teams[i].nations[ii].atroops
        if total_troops > 2500 : 
            print("Team : ",teams[i].name,"is a cheater. Deduct penalty \n")

def reallocate_interteam(team1,team2,sending_nation,receiving_nation,btroops,ntroops,atroops) : 
    if (btroops > team1.nations[sending_nation].btroops) or (ntroops > team1.nations[sending_nation].ntroops) or (atroops > team1.nations[sending_nation].atroops) : 
        raise ValueError("Not enough troops available with team : \t",team1.name ,"Nation \t" ,team1.nations[sending_nation].name)
    distance=Distance_Fetch_3.fetch_dist(team1.nations[sending_nation].name,team2.nations[receiving_nation].name)
    cost = team1.calculate_reallocation_cost(sending_nation, receiving_nation ,btroops,ntroops,atroops,distance)
    team1.nations[sending_nation].btroops -= btroops
    team1.nations[sending_nation].ntroops -= ntroops
    team1.nations[sending_nation].atroops -= atroops
    team2.nations[receiving_nation].btroops += btroops
    team2.nations[receiving_nation].ntroops += ntroops
    team2.nations[receiving_nation].atroops += atroops
    team1.update_ratio(sending_nation)
    team2.update_ratio(receiving_nation)
    team1.corpus -= cost

def update_all_ratio(teams) : 
    for i in range(len(teams)) :
        for ii in range(len(teams[i].nations)) : 
            teams[i].update_ratio(ii)

    
    
def printall(teams) : 
    for i in range(len(teams)) : 
        teams[i].print()
        print("\n \n")



def main() : 

    # Superpowers
    united_states = Nation("United States of America",2,0)
    china = Nation("China",2,2)
    russia = Nation("Russia",2,1)
    eu = Nation("European Union",2,3)
    india = Nation("India",2,1)
    brazil = Nation("Brazil",2,0)

    #High Powers
    japan = Nation("Japan",1,2)
    turkey = Nation("Turkey",1,1)
    australia = Nation("Australia",1,2)
    iran = Nation("Iran",1,1)
    south_africa = Nation("South Africa",1,3)
    saudi = Nation("Saudi Arabia",1,1)

    #Low POwers
    mexico = Nation("Mexico",0,0)
    indonesia = Nation("Indonesia",0,2)
    pakistan = Nation("Pakistan",0,1)
    ethiopia = Nation("Ethiopia",0,3)
    argentina = Nation("Argentina",0,0)
    canada = Nation("Canada",0,0)

    t1 = Team("Ashish")     
    t2 = Team("Bhoomi")
    t3 =  Team("Sneha")
    t4 = Team("Loventika")
    t5 = Team("Namaya")
    t6 = Team("Deepika")

    """
    t1.set_nations(united_states,japan,canada)
    t2.set_nations(india,australia,mexico)
    t3.set_nations(eu,turkey,indonesia)
    t4.set_nations(russia,south_africa,ethiopia)
    t5.set_nations(china,iran,pakistan)
    t6.set_nations(brazil,saudi,argentina)
    
    teams = [t1,t2,t3,t4,t5,t6]
    t1.set_synergy_direct(1.87)
    t2.set_synergy_direct(1.7)
    t3.set_synergy_direct(1.5)
    t4.set_synergy_direct(1.7)
    t5.set_synergy_direct(1.83)
    t6.set_synergy_direct(1.5)
    t2.corpus+=15000
    t4.corpus-=15000
    
    
    t1.distribute_troops(0,350,50,600) , t1.distribute_troops(1,200,600,100) , t1.distribute_troops(2,300,50,250)
    t2.distribute_troops(0,700,100,400) , t2.distribute_troops(1,0,500,200) , t2.distribute_troops(2,100,0,500)
    t3.distribute_troops(0,200,400,500) , t3.distribute_troops(1,600,100,150) , t3.distribute_troops(2,100,350,100)
    t4.distribute_troops(0,550,300,300) , t4.distribute_troops(1,225,250,225) , t4.distribute_troops(2,225,200,225)
    t5.distribute_troops(0,400,500,300) , t5.distribute_troops(1,300,200,200) , t5.distribute_troops(2,200,200,200)
    t6.distribute_troops(0,500,550,550) , t6.distribute_troops(1,100,50,50) , t6.distribute_troops(2,200,200,300)
    check_troops(teams)

    t2.buy_nuclear_upgrade(0)
    t6.buy_nuclear_upgrade(0)
    t1.buy_nuclear_upgrade(0)
    
    
    attack(t1,t6,0,2,350,50,600) ,t1.update_ratio(0)
    attack(t2,t5,0,2,400,100,200) ,t2.update_ratio(0)
    attack(t3,t1,2,1,50,50,100) ,t3.update_ratio(2)
    attack(t4,t6,0,1,150,150,100) ,t4.update_ratio(0)
    attack(t5,t1,0,1,100,150,100) ,t5.update_ratio(0)
    attack(t6,t1,0,0,450,450,350) , t6.update_ratio(0) 

    #printall(teams)
    
    update_all_ratio(teams)

    for team in teams:
        team.peace_table()

    print("at end of round 1 \n \n")
    #printall(teams)
    print("\n \n ROUND 2 \n")
    t6.buy_nuclear_upgrade(0)
    t6.buy_fortification_upgrade(0)
    t6.corpus-=50000
    t4.corpus+=50000
    t1.buy_nuclear_upgrade(0)
    t1.buy_fortification_upgrade(0)
    t1.buy_fortification_upgrade(1)
    reallocate(t1,1,0,300,50,250)

    
    teams.pop(0)
    t2.corpus-=180000
    t3.corpus-=180000
    t4.corpus-=180000
    t5.corpus-=180000
    t6.corpus-=180000
    attack(t2,t3,0,1,150,50,150) ,t2.update_ratio(0)
    attack(t3,t2,1,0,140,28,32) ,t3.update_ratio(1)
    attack(t4,t2,2,0,150,150,50) ,t4.update_ratio(2)
    attack(t5,t2,0,0,100,50,150) ,t5.update_ratio(0)
    t2.print()
    attack(t6,t2,0,2,200,200,100) ,t6.update_ratio(0)
    t2.print()
    teams.pop(-1)
    #printall(teams)
    
    
    
    update_all_ratio(teams)

    for team in teams:
        team.peace_table()

    print("at end of round 2 \n \n")
    printall(teams)
    print("\n \n ROUND 3 \n")


    t2.buy_fortification_upgrade(0)
    t4.buy_nuclear_upgrade(1)
    t5.buy_nuclear_upgrade(0)
    

    attack(t2,t4,1,1,0,300,100) ,t2.update_ratio(1)
    t5.print()
    attack(t3,t5,0,0,100,100,100) ,t3.update_ratio(0)
    t5.print()
    t4.corpus-=180000
    attack(t4,t5,1,0,99,110,99) ,t4.update_ratio(1)
    attack(t5,t4,0,0,0,50,200) ,t5.update_ratio(0)
   
    

    
    update_all_ratio(teams)
    for team in teams:
        team.peace_table()
    print("at end of round 3 \n \n")
    #printall(teams)
    print("\n \n ROUND 4 \n")
    t5.buy_fortification_upgrade(0)
    t4.buy_fortification_upgrade(0)
    t3.buy_nuclear_upgrade(1)
    
    
    
    
    attack(t2,t4,1,0,0,200,100) ,t2.update_ratio(1)
    attack(t3,t5,1,0,200,20,40) ,t3.update_ratio(1)
    attack(t4,t5,2,0,75,50,175) ,t4.update_ratio(2)
    t4.corpus-=180000
    teams.pop(2)
    
    
    #attack(t5,t4,0,1,100,50,100) ,t5.update_ratio(0)

    update_all_ratio(teams)

    for team in teams:
        team.peace_table()
    

    print("at end of round 4 \n \n")
    #printall(teams)
    print("\n \n ROUND 5 \n")
    
    
    t5.buy_fortification_upgrade(0,True)
    t2.buy_nuclear_upgrade(0,True)
    t3.buy_nuclear_upgrade(0,True)
    
    

    attack(t2,t3,0,0,30,1,1) ,t2.update_ratio(0)
    attack(t3,t5,0,0,0,100,100) ,t3.update_ratio(0)
    #t2.print()
    #t3.print()
    print("GAME OVER T3 WINS WOOOOOOO")
    
    attack(t4,t6,0,0,643,325,316) ,t4.update_ratio(0)
    attack(t5,t6,0,0,1,0,0) ,t5.update_ratio(0)
    attack(t6,t5,0,0,364,159,319) , t6.update_ratio(0)
    
    

    attack(t2,t5,0,0,300,170,99) ,t2.update_ratio(0)
    t5.corpus-=246923
    t4.corpus+=246923
    printall(teams)
    
    print("at end of round 5 \n \n")
    printall(teams)
    print("\n \n ROUND 6 \n")
    
    t1.buy_nuclear_upgrade(0,True)
    t2.buy_nuclear_upgrade(0,True)
    t5.buy_nuclear_upgrade(0,True)
    t6.buy_nuclear_upgrade(0,True)
    attack(t1,t4,0,0,0,30,150) ,t1.update_ratio(0) 
    attack(t2,t6,0,1,0,127,106) ,t2.update_ratio(0)
    attack(t3,t5,1,0,1,0,0) ,t3.update_ratio(1)
    attack(t5,t6,0,0,0,50,100) ,t5.update_ratio(0)
    #attack(t5,t4,0,0,0,0,100) ,t5.update_ratio(0)
    attack(t6,t5,0,0,0,0,200) , t6.update_ratio(0)
    print("at end of round 4 \n \n")
    printall(teams)
    print("\n \n ROUND 5 \n")
    t1.buy_nuclear_upgrade(0,True)
    t3.buy_nuclear_upgrade(0,True)
    t5.buy_nuclear_upgrade(1,True)
    t6.buy_nuclear_upgrade(1,True)

    attack(t1,t2,0,0,0,0,100) ,t1.update_ratio(0) 
    #attack(t3,t1,0,0,0,0,100) ,t3.update_ratio(0)
    attack(t5,t2,1,0,0,100,100) ,t5.update_ratio(1)
    attack(t6,t1,2,2,0,0,200) , t6.update_ratio(2)
    print("at end of round 4 \n \n")
    printall(teams)
    
    
    
    

    
    #t1 = Team("Team 1")
    t2 = Team("Team 2")
    t1.set_nations(america,brazil,india)
    t2.set_nations(america2,brazil2,india2)
    print(t2.nations[0].name)
    print(t1.nations[0].name)
    t1.distribute_troops(0,20,20,20)
    t2.distribute_troops(0,20,20,20)
    t1.synergy_score = 1
    t2.synergy_score = 1
    t1.buy_nuclear_upgrade()
    dmg = attack_and_get_damage(t1,t2,0,0,100)
    print(dmg)
    post_attack_and_stabilise(t1,t2,0,0,dmg,True)
    print(t1.nations[0].name)
    t1.print()
    t2.print()
    """


main()