from random import randint
from time import sleep
#Імпорт
global knife_picked
knife_picked = False
global med_kit_picked
med_kit_picked = False
global shield_picked
shield_picked = False
hp = 100
damage = 10
inventory = []
def shield():
    health += 50

def damage_boss():
    health -= 25

def main():
    name = input("Впишіть ім'я: ")
    sleep(2)
    print(f"Привіт, {name}, я Дух-хранитель цих джунглів і ти реінкарувався на моїх землях  ")
    sleep(2)
    print("Оскільки ти тут не знайомий з середовищем я тобі дам факел який завжи горить і допоможе тобі відлякувати хижих істот")
    sleep(2)
    print("Твоє завдання зібрати 3 частини артефакту щоб вибратись з цих джунглів. Удачі!")
    sleep(1)
    location_1()


def death():
    print("Ви померли")


def items():
    if 'ніж' in inventory:
        damage += 20
    if shield_picked==True:
        shield_hits = 2
    if 'аптечка' in inventory:
        med_kit_picked = True
        inventory.append("аптечка")
    if knife_picked==True:
        inventory.append("ніж")
        print("Ти підібрав ніж! Твоя шкода збільшилася на 20.")
    if med_kit_picked==True:
        inventory.append("аптечка")
        print("Ти підібрав аптечку! Ти можеш відновити 50 здоров'я.")
    if shield_picked==True:
        print("Ти підібрав щит! Ти можеш блокувати 2 удари.")




def status():
    print("Інвентар:", inventory)
    print("Здоров'я:", hp)
    print("Шкода:", damage)
    print("Удари щита:", shield_hits)


def location_1():
    print("Ти опинився на зарослій стежці. Перед тобою три шляхи: густі кущі, підвісний міст, та покинутий табір.")
    print("Куди ти хочеш піти? (кущі/міст/табір)")
    choice = input("Ваш вибір: ")
    if choice == "кущі":
        location_1_1()
    elif choice == "міст":
        location_1_2()
    elif choice == "табір":
        location_1_3()
    else:
        print("Невірний вибір. Спробуй ще раз.")
        location_1()



def location_1_1():
    global knife_picked
    print("Ти обрав шлях через густі кущі. Раптом ти бачиш труп біля якого лежить змія в яку втикнутий ніж. Ти можеш оглянути труп або повернутися назад на стежку.")
    print("Що ти робиш? (оглянути/повернутися)")
    choice = input("Ваш вибір: ")
    if choice == "оглянути":
        print("Ти підійшов до трупа і побачив, що ніж в ньому. Ти можеш взяти ніж або повернутися назад на стежку.")
        print("Що ти робиш? (взяти/повернутися)")
        choice = input("Ваш вибір: ")
        if choice == "взяти":
            if knife_picked == True:
                print("Ти вже підібрав ніж раніше.")
                location_1_1()
            else:
                knife_picked = True
                inventory.append("ніж")
                print("Ти підібрав ніж! Твоя шкода збільшилася на 20.")
                location_1_1()   
        elif choice == "повернутися":
            print("Ти повертаєшся назад на стежку.")
            location_1()
    else:
        print("Невірний вибір. Спробуй ще раз.")
        location_1_1()


def location_1_2():
    print("Ти обрав шлях через підвісний міст. Міст був старим і тріщав.")
    random_number = random.randint(1, 2)
    if random_number == 1:
        print("Ти успішно перейшов міст і опинився на іншому боці.")
        location_2()
    else:
        print("Міст обвалився і ти впав у річку. Ти втратив 30 здоров'я. Річка донесла тебе до таємничого болота.")
        hp -= 30
        location_2()



def location_1_3():
    print("Ти обрав шлях через покинутий табір. Табір був порожнім, але ти знайшов аптечку.")
    med_kit_picked = True
    inventory.append("аптечка")
    print("Ти підібрав аптечку! Ти можеш відновити 50 здоров'я.")    
    
main()
