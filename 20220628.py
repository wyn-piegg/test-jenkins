# class Hero:
#     # 定义基本属性
#     Hp=200 # 英雄生命值
#     AttackRange=36 # 攻击距离
#     AttackSpeed=12 # 攻击速度
#     Ad=50 # 物理伤害
#     Ap=60 # 魔法伤害
#     Mdef=20 # 魔法防御
#     Def=10 # 物理防御
#     def __init__(self,Damagetypes,Defensetype):
#         self.Damagetypes=Damagetypes # 伤害类型
#         self.Defensetype=Defensetype # 防御类型
#     def heroattack(self,Hero):
#         '''
#         英雄战斗
#         :return:
#         '''
#         #如果敌方英雄在攻击范围内
#         if self.AttackRange>=Hero.AttackRange:
#             if self.Damagetypes==self.Ad: # 判断英雄的伤害类型
#                 if Hero.Defensetype==Hero.Def: # 判断敌方英雄的防御类型
#                     Hero.Hp=Hero.Hp-self.Ad+Hero.Def
#                     if Hero.Hp<=0:
#                         return
#                 if Hero.Defensetype==Hero.Mdef:
#                     Hero.Hp=Hero.Hp-self.Ad
#                     if Hero.Hp<=0:
#                         return
#             if self.Damagetypes==self.Ap: # 判断英雄的伤害类型
#                 if Hero.Defensetype == Hero.Def: # 判断敌方英雄的防御类型
#                     Hero.Hp = Hero.Hp - self.Ad + Hero.Def
#                     if Hero.Hp <= 0:
#                         return
#                 if Hero.Defensetype == Hero.Mdef:
#                     Hero.Hp = Hero.Hp - self.Ad
#                     if Hero.Hp <= 0:
#                         return
import random
import time

# 定义一个英雄的基类
class Hero:
    def __init__(self, name, health, attack, q_hurt, w_hurt, e_hurt):
        self.name = name
        self.health = health
        self.attack = attack
        self.q_hurt = q_hurt
        self.w_hurt = w_hurt
        self.e_hurt = e_hurt
    def attack(self,enemy):
        enemy.health-=self.attack
        print(f"\033[38m {self.name}使用普通攻击对{enemy.name}造成{self.attack}点伤害，目前{enemy.name}剩余血量为{enemy.health}点\033[0m")

    def q_hurt(self,enemy):
        enemy.health-=self.attack
        print(f"\033[33m {self.name}使用Q攻击对{enemy.name}造成{self.q_hurt}点伤害，目前{enemy.name}剩余血量为{enemy.health}点\033[0m")

    def w_hurt(self,enemy):
        enemy.health-=self.attack
        print(f"\033[32m {self.name}使用W攻击对{enemy.name}造成{self.w_hurt}点伤害，目前{enemy.name}剩余血量为{enemy.health}点\033[0m")

    def e_hurt(self,enemy):
        enemy.health-=self.attack
        print(f"\033[34m {self.name}使用E攻击对{enemy.name}造成{self.e_hurt}点伤害，目前{enemy.name}剩余血量为{enemy.health}点\033[0m")
# 判断是谁死亡，将其移除英雄池
def kill_hero(enemy,team):
    if enemy.health<=0:
        print(f"\033[31m** {enemy.name} ** 阵亡。\033[0m")
        if team=='side':
            side_team.remove(enemy)
        elif team=='hostile':
            hostile_team.remove(enemy)
# 随机选择一种攻击方式
def get_random_skill():
    # random_index = random.randint(1, 4)
    # random_skill = skill_list.get(random_index)
    # return random_skill  # 函数名当做返回值返回，拿到可以直接加括号调用执行函数
    return skill_list.get(random.randint(1, 4))  # 上面代码的简便写法
# 随机选择一个己方英雄
def get_random_side_team_hero():
    sideteam_list=random.randint(0,len(side_team)-1)
    hero=side_team[sideteam_list]
    return hero
# 随机选择一个敌方英雄
def get_random_hostile_team_hero():
    return hostile_team[random.randint(0,len(hostile_team)-1)]
# 己方英雄池
side_team=[
# 英雄名 生命值 普通攻击力 Q技能伤害 W技能伤害 E技能伤害
    Hero('德莱文',500,45,60,65,80),
    Hero('加里奥',600,40,55,65,85),
    Hero('塔姆',650,45,65,65,80),
    Hero('阿狸',400,45,50,55,65),
    Hero('马尔扎哈',350,40,45,50,65),
    Hero('薇古丝',600,35,45,50,55)
]
# 敌方英雄池
hostile_team=[
# 英雄名 生命值 普通攻击力 Q技能伤害 W技能伤害 E技能伤害
    Hero('金克丝',600,45,60,65,80),
    Hero('萨勒芬妮',500,45,50,55,55),
    Hero('维克托',600,50,55,65,80),
    Hero('卡沙',400,45,50,55,65),
    Hero('希维尔',400,50,55,60,65),
    Hero('纳尔',600,35,40,45,80)
]
# 技能数字对应表（方便根据随机数取技能）
skill_list = {
    1: Hero.attack,
    2: Hero.q_hurt,
    3: Hero.w_hurt,
    4: Hero.e_hurt,
}
def run():
    while len(side_team)>0 and len(hostile_team)>0:
        # 随机选择一种攻击方式
        kill=get_random_skill()
        # 随机选择一个己方英雄
        side=get_random_side_team_hero()
        # 随机选择一个敌方英雄
        hostile=get_random_hostile_team_hero()
        # 随机选择一方为攻击方（那么另一方就是被攻击方）
        flag = random.randint(0, 1)
        if flag:
            kill(side, hostile)
            kill_hero(hostile, 'hostile')
        else:
            kill(hostile, side)
            kill_hero(side, 'side')
            # 暂停0.3秒，可以慢慢看战斗过程
        time.sleep(0.3)
        if len(side_team)==0:
            print("很遗憾，敌方胜出，己方惨败")
            print('敌方所剩英雄状态如下:')
            for hero in hostile_team:
                print(f"{hero.name} 剩余生命值 {hero.health}")
        elif len(hostile_team)==0:
            print("恭喜你，打败了敌人")
            print('己方所剩英雄状态如下:')
            for hero in side_team:
                print(f"{hero.name} 剩余生命值 {hero.health}")

if __name__ == '__main__':
    run()















































