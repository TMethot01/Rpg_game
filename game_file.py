from pandas import *
import time
import random

player_sheet = []
gold = 0
player_atk = 4
player_health = 25
player_def = 10
player_chc = 10
player_chd = 50
border = "*********************************************************"
stat_border = "??????????????????????????????????????????????????????????"
shop_border = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
quests = read_csv("quests.csv", index_col=0)
quests.index.name = None
enemy_df = read_csv("enemies.csv", index_col=0)
player_name = "Tyler"
items = read_csv("items.csv", index_col=0)
inventory = read_csv("inventory.csv", index_col=0)
quests.index.name, enemy_df.index.name, items.index.name, inventory.index.name = None, None, None, None


def menu():
    print(border)
    print("what would you like to do?         " + str(gold) + "G     Lvl 1")
    print("fight (1)")
    print("shop (2)")
    print("check inventory (3)")
    print("check quests (4)")
    print("settings (5)")
    action = input("->")
    print(border)

    if action == "1":
        print("which enemy would you like to fight?")
        for mons in range(len(enemy_df.index)):
            print(str(enemy_df.index[mons]) + "(" + str(mons + 1) + ")")
        choice = input("-> ")
        return fights(enemy_df.index[int(choice) - 1])
    elif action == "2":
        print("you walk to the store")
        time.sleep(1)
        return shop()
    elif action == "3":
        print(inventory)
        print(border)
        print("what would you like to do?")
        print("equip an item (1)")
        print("view an item's stats (2)")
        choice = input("-> ")
        if choice == "1":
            return equip()
        return menu()
    elif action == "4":
        print("what would you like to do?")
        print("check active quests (1)")
        print("check for new quests (2)")
        choice = input("-> ")
        if choice == "1":
            return active_quests()
        elif choice == "2":
            return #questboard()


def equip():
    print("which item would you like to equip?")
    currently_equipped = "null"
    counter = 1
    for i in inventory.index:
        print(i + "(" + str(counter) + ")")
        counter += 1
    print("back to menu (" + str(counter) + ")")
    choice = input("-> ")
    chosen = inventory.index[int(choice)-1]
    x = (inventory[inventory["item_type"] == "weapon"]["equipped"])
    for w in range(len(x)):
        if x[w]:
            currently_equipped = x.index[w]
    if inventory.loc[chosen, "equipped"]:
        print("this item is already equipped")
    elif currently_equipped == "null":
        inventory.loc[chosen, "equipped"] = True

    else:
        inventory.loc[currently_equipped, "equipped"] = False
        inventory.loc[chosen, "equipped"] = True
    return menu()

def active_quests():
    global gold
    print(quests)
    input("press enter to collect rewards...")
    for q in quests.index:
        if quests.loc[q, "current"] >= quests.loc[q, "goal"]:
            if quests.loc[q, "reward"] == "gold":
                gold += quests.loc[q, "reward_quant"]
            quests.loc[q, "current"] = quests.loc[q, "current"] - quests.loc[q, "goal"]
    print(quests)
    input("press enter to continue...")
    return menu()


def shop():
    print(shop_border)
    print(str(gold) + "G")
    input()
    return menu()


def damage(atkr_atk, atkr_chc, atkr_chd, defender_def, defend):
    if random.random() < (atkr_chc/100):
        atkr_atk = atkr_atk * ((100 + atkr_chd)/100)
    if defend:
        return round(atkr_atk * (100 - defender_def)/50)
    else:
        return round(atkr_atk * (100 - defender_def)/100)


def fights(monster):
    global inventory
    global gold
    player_atk = 8
    player_health = 25
    player_def = 10
    player_chc = 10
    enemy_def = int(enemy_df.loc[monster, "def"])
    enemy_health = int(enemy_df.loc[monster, "health"])
    enemy_atk = int(enemy_df.loc[monster, "atk"])
    print("you have encountered a " + monster)
    time.sleep(0.5)
    while enemy_health > 0 and player_health > 0:
        print(border)
        print(player_name + ": " + str(player_health) + "HP        " + monster + ": " + str(enemy_health) + "HP")
        action = input("What will you do?\nFight (1)\nDefend (2) \nRun (3)\nStats (4) \n -> ")
        time.sleep(0.5)
        if action == "1":
            print("\nyou attack!")
            time.sleep(0.5)
            dmg = damage(player_atk, player_chc, player_chd, enemy_def, False)
            if enemy_health - dmg <= 0:
                print("you did " + str(enemy_health) + " damage and the enemy died!\n")
                print("you gained " + str(enemy_df.loc[monster, "gold_drop"]) + "G")
                gold += enemy_df.loc[monster, "gold_drop"]
                if random.random() < enemy_df.loc[monster, "droprate1"]/100:
                    if enemy_df.loc[monster, "item1"] in inventory.index:
                        inventory.loc[enemy_df.loc[monster, "item1"], "quantity"] += 1
                        print("you got: " + enemy_df.loc[monster, "item1"])
                if monster in quests.index:
                    quests.loc[monster, "current"] += 1
                time.sleep(1)
                break
            else:
                print("you did " + str(dmg) + " damage!\n")
                enemy_health = enemy_health - dmg
                time.sleep(1)
            print("the enemy attacks you!")
            time.sleep(1)
            enemy_dmg = damage(enemy_atk, 0, 0, player_def, False)
            if player_health - enemy_dmg > 0:
                print("you took " + str(enemy_dmg) + " damage.\n")
                time.sleep(1)
                player_health = player_health - enemy_dmg
            else:
                print("he needs some milk\n")
                break
        elif action == "2":
            print("\nyou defend.")
            time.sleep(0.5)
            enemy_dmg = damage(enemy_atk, 0, 0, player_def, True)
            if player_health - enemy_dmg > 0:
                print("you took " + str(enemy_dmg) + " damage.\n")
                player_health = player_health - enemy_dmg
                time.sleep(1)
            else:
                print("he needs some milk")
                break
        elif action == "3":
            print("you ran away")
            break
        elif action == "4":
            print(stat_border)
            print("Player Stats")
            print("HP: " + str(player_health))
            print("attack: " + str(player_atk))
            print("Defence: " + str(player_def))
            print("critical hit chance: " + str(player_chc))
            print("critical hit damage: " + str(player_chd))
            input("(press enter to continue...)")
        else:
            print("INVALID INPUT\n")
    return menu()


# fights("zombie")
menu()


