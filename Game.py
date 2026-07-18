import json
import sys
import time
from pathlib import Path
from random import randint
class Game:
    SCREEN_WIDTH = 70

    def __init__(self, save_file=None):
        self.player_hp = 100
        self.has_knife = False
        self.has_medkit = False
        self.has_shield = False
        self.adventurer = False
        self.artifact_count = 0
        self.inventory = []
        self.text_delay = 0
        self.damage = 10  
        self.save_file = Path(save_file) if save_file else Path("game_save.json")
        self.load_game()
        

    def choose_text_speed(self):
        """Запитує швидкість поступового виводу тексту та зберігає у self.text_delay."""
        speed_settings = {
            "1": (0, "миттєво"), 
            "2": (0.01, "швидко"), 
            "3": (0.025, "середньо"), 
            "4": (0.04, "повільно"), 
            "5": (0.07, "дуже повільно"),  
        }

        self.print_title("Оберіть швидкість появи тексту")
        self.print_slowly("1 — миттєво ".center(self.SCREEN_WIDTH))
        self.print_slowly("2 — швидко".center(self.SCREEN_WIDTH))
        self.print_slowly("3 — середньо".center(self.SCREEN_WIDTH))
        self.print_slowly("4 — повільно".center(self.SCREEN_WIDTH))
        self.print_slowly("5 — дуже повільно".center(self.SCREEN_WIDTH))

        while True:
            choice = input("Ваша швидкість (1–5): ").strip()
            if choice in speed_settings:
                self.text_delay, speed_name = speed_settings[choice]
                self.print_slowly(f"\nОбрано швидкість: {speed_name}.")
                return

            print("Будь ласка, введіть число від 1 до 5.")

    def print_title(self, title):
        """Виводить великий заголовок по центру консолі з рамкою з '='."""
        self.print_slowly("\n" + "=" * self.SCREEN_WIDTH)
        self.print_slowly(title.upper().center(self.SCREEN_WIDTH))
        self.print_slowly("=" * self.SCREEN_WIDTH)

    def print_slowly(self, text="", end="\n"):
        """Виводить текст посимвольно з обраною затримкою (або миттєво якщо затримка = 0)."""
        if self.text_delay == 0:
            print(text, end=end)
            return

        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(self.text_delay)

        sys.stdout.write(end)
        sys.stdout.flush()

    def save_game(self):
        """Зберігає поточний стан гри у JSON-файл."""
        data = {
            "player_hp": self.player_hp,
            "bosshp": self.bosshp,
            "has_knife": self.has_knife,
            "has_medkit": self.has_medkit,
            "has_shield": self.has_shield,
            "inventory": list(self.inventory),
            "damage": self.damage,
        }
        self.save_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.save_file, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def load_game(self):
        """Завантажує стан гри з JSON-файлу, якщо він існує."""
        try:
            with open(self.save_file, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            return False
        except (json.JSONDecodeError, TypeError, ValueError):
            return False

        self.player_hp = data.get("player_hp", 100)
        self.has_knife = data.get("has_knife", False)
        self.has_medkit = data.get("has_medkit", 0)
        self.has_shield = data.get("has_shield", False)
        self.inventory = list(data.get("inventory", []))
        self.damage = data.get("damage", 10)
        return True

    def exit_game(self):
        """Зберігає гру і завершує її."""
        self.save_game()
        self.print_slowly("Гру збережено. До побачення!")
        raise SystemExit

    def start(self):
        """Головна функція - запускає всю гру, починаючи з привітання та отримання імені гравця."""
        self.choose_text_speed()
        self.traveler_alive = False
        self.save_file = Path("game_save.json")
        self.damage = 10
        self.artifact_count = 0
        self.has_medkit = 0
        self.has_knife = False
        self.player_hp = 100
        self.inventory = []
        self.bosshp = 150
        self.print_slowly("!Всі відповіді треба писати з маленької букви без зайвих пробілів!")
        name = input("Впишіть ім'я: ")
        time.sleep(2)
        self.print_slowly(f"Привіт, {name}, я Дух-хранитель цих джунглів і ти реінкарувався на моїх землях")
        time.sleep(2)
        self.print_slowly("Оскільки ти тут не знайомий з середовищем я тобі дам факел який завжи горить і допоможе тобі відлякувати хижих істот")
        time.sleep(2)
        self.print_slowly("Твоє завдання зібрати 3 частини артефакту щоб вибратись з цих джунглів. Удачі!")
        time.sleep(1)
        self.location_1()

    def location_1(self):
        """Перша локація - заросла стежка з трьома шляхами."""
        self.print_title(" ЗАРОСЛА СТЕЖКА")
        self.print_slowly("Ти опинився на зарослій стежці. Перед тобою три шляхи: густі кущі, підвісний міст, та покинутий табір.")
        self.print_slowly("Куди ти хочеш піти? (кущі: 1/міст: 2/табір: 3/ подивитися статус: 0)")
        choice = input("Ваш вибір: ").strip()
        
        if choice == 1 or choice == "1":
            self.location_1_1()
        elif choice == 2 or choice == "2":
            self.location_1_2()
        elif choice == 3 or choice == "3":
            self.location_1_3()
        elif choice == "0" or choice == 0:
            self.show_status()
        else:
            self.print_slowly("Невірний вибір. Спробуй ще раз.")
            self.location_1()

    def location_1_1(self):
        """Друга локація - густі кущі з мертвецем і ножем."""
        self.print_slowly("Ти обрав шлях через густі кущі. Раптом ти бачиш труп біля якого лежить змія в яку втикнутий ніж. Ти можеш оглянути труп або повернутися назад на стежку.")
        self.print_slowly("Що ти робиш? (оглянути: 1/повернутися: 2)")
        choice = input("Ваш вибір: ").strip()
        
        if choice == "1":
            self.print_slowly("Ти підійшов до трупа і побачив, що ніж в ньому. Ти можеш взяти ніж або повернутися назад на стежку.")
            self.print_slowly("Що ти робиш? (взяти: 1/повернутися: 2)")
            choice = input("Ваш вибір: ").strip()
            
            if choice == "1":
                if self.has_knife:
                    self.print_slowly("Ти вже підібрав ніж раніше.")
                    self.location_1_1()
                else:
                    self.has_knife = True
                    self.inventory.append("ніж")
                    self.damage += 20
                    self.save_game()
                    self.print_slowly("Ти підібрав ніж! Твоя шкода збільшилася на 20.")
                    self.location_1_1()
            elif choice == "2":
                self.print_slowly("Ти повертаєшся назад на стежку.")
                self.location_1()
            else:
                self.print_slowly("Невірний вибір. Спробуй ще раз.")
                self.location_1_1()
        elif choice == "2":
            self.print_slowly("Ти повертаєшся назад на стежку.")
            self.location_1()
        else:
            self.print_slowly("Невірний вибір. Спробуй ще раз.")
            self.location_1_1()

    def location_1_2(self):
        """Третя локація - підвісний міст з випадковим наслідком."""
        self.print_slowly("Ти обрав шлях через підвісний міст. Міст був старим і тріщав.")
        random_number = randint(1, 2)
        
        if random_number == 1:
            self.print_slowly("Ти успішно перейшов міст і опинився на іншому боці.")
            self.location_2()
        else:
            self.print_slowly("Міст обвалився і ти впав у річку. Ти втратив 30 здоров'я. Річка донесла тебе до таємничого болота.")
            self.player_hp -= 30
            self.save_game()
            self.location_2()

    def location_1_3(self):
        """Четверта локація - покинутий табір з аптечкою."""
        self.print_slowly("Ти обрав шлях через покинутий табір. Табір був порожнім, але ти знайшов аптечку і першу частину артефакту.")
        self.artifact_count += 1
        time.sleep(0.1)
        self.has_medkit = 1
        self.inventory.append("аптечка")
        time.sleep(0.1)
        self.save_game()
        self.print_slowly("Ти підібрав аптечку! Ти можеш відновити 50 здоров'я.")
        time.sleep(1)
        self.print_slowly("Ти повернувся назад")
        self.location_1()

    def casino(self):
        self.print_slowly('це лотерея, вибивши три однакових цифри ти виграєш у неї і отримаєш річ яка допоможе тобі у майбутньому, а якщо програєш... Фіні теля комедія..')
        while True:
            answer = input('Ти хочеш зіграти у лотерею? (так/ні)')
            if answer == 'так':
                break
            else:
                self.print_slowly("-10 здоров'я")
                self.player_hp -= 10
            if self.player_hp <= 10:
                # death()
                print('ХА лох')
                exit()
        print('Вам випало:')
        num_1 = randint(1, 3)
        num_2 = randint(1, 5)
        if num_1 == 1:
            self.has_shield = True
            self.player_hp += 50
            print('Щит') 
        elif num_1 == 2:
            self.player_hp -= 10
            print('hp -= 10')
        else:
            if num_2 == 1:
                print('Анекдот: Як називається кіт якого зловили на гарячому? -Котлета')
            elif num_2 == 2:
                print('Анекдот:Колобок повісився')
            elif num_2 == 3:
                print('Анекдот:Що кажуть хірурги коли грають у мафію? -Ну що вскриваємося?')
            elif num_2 == 4:
                print('Анекдот:У вас є рекомендація з минулої роботи? - Так, рекомендували знайти іншу роботу')
            else:
                print('Анекдот:Як називаються брудні накачані люди? -Нечиста сила')

    def location_2(self):
        """Друга локація - болото забутих з мандрівником."""
        self.print_title(" БОЛОТО ЗАБУТИХ")
        self.print_slowly("Ви стоїте посеред туманного болота. Повітря важке, під ногами хлюпає вода.")
        self.casino()
        self.print_slowly("Ви бачите постать мандрівника, що сидить на старому пні.")
        
        self.print_slowly("\nМандрівник дивиться на вас і усміхається:")
        self.print_slowly('"Вітаю, гравець. Болото сьогодні особливо мовчазне, чи не так?"')
        self.print_slowly("Тримай жарт для підняття духу: Чому жаби не грають у карти?")
        self.print_slowly('Бо вони постійно бояться, що їх "зажаблять"!')

        options = ["1 - Взяти аптечку мирно"]
        if self.has_knife:
            options.append("2 - Напасти на мандрівника з ножем")
        else:
            self.print_slowly("У вас немає ножа, тому напасти на мандрівника неможливо.")
        for option in options:
            self.print_slowly(option.center(self.SCREEN_WIDTH))

        choice = input("Ваш вибір: ").strip()

        if choice == "2" and self.has_knife:
            self.print_slowly("\nВи різко вихоплюєте ніж і нападаєте на мандрівника...")
            self.print_slowly("Той падає...")
            self.print_slowly(
                'Мандрівник на останньому подиху шепоче: "Ти робиш велику помилку..."'
            )
            self.traveler_alive = False
            self.print_slowly(" З його речей випадають дві аптечки.")
            self.inventory.append("аптечка")
            self.inventory.append("аптечка")
            self.has_medkit += 2

        elif choice == "1":
            self.traveler_alive = True
            self.print_slowly("\nВи дякуєте мандрівнику і забираєте аптечку.")
            self.inventory.append("аптечка")
            self.has_medkit += 1

        else:
            self.print_slowly("\nНевірний вибір. Ви нічого не отримали.")
        
        time.sleep(2)
        self.print_slowly("\nТи продовжуєш свою подорож...")
        self.location_3()

    def location_3(self):
        """Третя локація - храм джунглів."""
        self.print_title(" ХРАМ ДЖУНГЛІВ")
        self.print_slowly("Через туман болота ти виходиш до стародавнього храму, обвитого лозами.")
        self.print_slowly("Це місце, де мандрівники кажуть, що легендарні артефакти прихованої історії чекають на сміливців.")
        self.print_slowly("В тебе є 2 шляхи:")
        self.print_slowly("1 - ти маєш розгадати 5 загадок. За кожне неправильне розгадування тобі знімається 25hp")
        self.print_slowly("2 - в тебе дуже малий шанс пройти кріз всі пастки і голодних диких тварин")
        choice = input("Ваш вибір: ").strip()
        if choice == "1":
            self.location_3_1()
        elif choice == "2":
            self.location_3_2()
        else:
            self.print_slowly("Невірний вибір, повторіть спробу")
            self.location_3()
        time.sleep(2)

    def location_3_1(self):
        answer1 = input("Загадка: Я найвища тварина в джунглях, маю довгу шию. Хто я?")
        if answer1 == 'жирафа':
            self.print_slowly("Першу загадку розгадано")
        else:
            self.print_slowly("Першу загадку не розгадано")
            self.player_hp -= 25

        answer2 = input("Я люблю банани, стрибаю по деревах і маю довгий хвіст. Хто я?")
        if answer2 == 'мавпа':
            self.print_slowly("Другу загадку розгадано")
        else:
            self.print_slowly("Другу загадку не розгадано")
            self.player_hp -= 25

        answer3 = input("Я великий сірий, маю хобот і великі вуха. Хто я?")
        if answer3 == 'слон':
            self.print_slowly("Третю загадку розгадано")
        else:
            self.print_slowly("Третю загадку не розгадано")
            self.player_hp -= 25

        answer4 = input("Я смугастий хижак із гострими зубами. Хто я?")
        if answer4 == 'тигр':
            self.print_slowly("Четверту загадку розгадано")
        else:
            self.print_slowly("Четверту загадку не розгадано")
            self.player_hp -= 25

        answer5 = input("Я зелений, люблю сидіти на листках і голосно квакаю. Хто я?")
        if answer5 == 'жаба':
            self.print_slowly("П'яту загадку розгадано")
        else:
            self.print_slowly("П'яту загадку не розгадано")
            self.player_hp -= 25
        if self.player_hp <= 0:
            self.print_slowly("Ти помер")
            self.save_game()
        else:
            self.print_slowly("Вітаю, ви пройшли храм джунглів та отримали артефакт")
            self.location_4()
            self.save_game()


    def location_3_2(self):
        """Друга гілка - пройти крізь пастки і тварин."""
        random_chance = randint(1, 10)
        if random_chance < 3:
            self.print_slowly("Вітаю, ви пройшли всі пастки і відбились від тварин та ви отримали артефакт")
            self.location_4()

        elif random_chance >= 3:
            self.print_slowly("На жаль вам не повезло і ви не пройшли")
            self.player_hp = 0  
            self.save_game()

    def location_4(self):
        """Фінальна локація гри."""
        self.artifact_count += 1
        self.print_title("ВЕЛИКЕ ДЕРЕВО")
        self.print_slowly("Ви дойшли до фінальної локації де на вас чекає великий кам'яний страж")
        self.print_slowly("Цей страж охороняє останній уламок артефакту - ядро")
        self.print_slowly("Щоб забрати останній уламок треба перемогти стража. Удачі!")
        self.save_game()
        self.bosshp = 150
        self.bossfight_playerchoice()
        
    def bossfight_playerchoice(self):
        while self.bosshp > 0 and self.player_hp > 0:
            self.print_slowly(f"\nВаше здоров'я: {self.player_hp}")
            self.print_slowly(f"Здоров'я стража: {self.bosshp}")
            self.print_slowly("Ви можете атакувати або використати аптечку (1/2)")

            choice = input("Ваша дія: ").strip()

            if choice == "1":
                attack_chance = randint(1, 10)

                if attack_chance <= 9:
                    self.print_slowly("Атака успішна")
                    self.bosshp -= self.damage
                else:
                    self.print_slowly("Атака не вдалася, страж ухилився")

            elif choice == "2":
                if self.has_medkit:
                    self.player_hp += 50
                    self.has_medkit -= 1
                    if self.player_hp > 100:
                        self.player_hp += 50
                        self.has_medkit -= 1
                    self.has_medkit <= 0
                    self.print_slowly("Ви використали аптечку")
                else:
                    self.print_slowly("У вас немає аптечки")

            else:
                self.print_slowly("Невірний вибір")
                continue

            if self.bosshp > 0:
                self.bossfight_bosschoice()

        if self.player_hp <= 0:
            self.print_slowly("Ви були переможені стражем!")
        elif self.artifact_count == 2:
            self.print_slowly("Ви перемогли стража і забрали останній уламок артефакту")
            self.print_slowly("Ви склали артефакт і відкрився портал назад. Вітаю!")
            time.sleep(0.1)
        elif self.artifact_count != 2:
            self.print_slowly("Ви перемогли стража, але не зібрали всі уламки артефакту")
            self.print_slowly("Тому ви застрягаєте в цих джунглях назавжди")
            time.sleep(0.1)

    def bossfight_bosschoice(self): 
        if self.traveler_alive == True and self.player_hp <= 50:
            self.print_slowly("Мандрівник гуляв і замітив що ти б'єшся з стражем")
            self.print_slowly("Він витягнув лук і попав по стражу(-25hp)")
            self.bosshp -= 25
            self.traveler_alive = False
        attack_chance = randint(1,10)
        if attack_chance <= 9:
            self.print_slowly("Атака стража успішна")
            self.player_hp -= 20
        if attack_chance > 9 :
            self.print_slowly("Атака не удачна, ви ухилилися")
            self.bossfight_playerchoice()
       


    def show_status(self):
        """Показує поточний статус гравця: здоров'я, шкода, інвентар."""
        self.print_slowly("\n--- СТАТУС ---")
        self.print_slowly(f"Здоров'я: {self.player_hp}")
        self.print_slowly(f"Шкода: {self.damage}")
        self.print_slowly(f"Уламків артефакту: {self.artifact_count}")
        self.print_slowly("Інвентар: {}".format(", ".join(self.inventory) if self.inventory else "порожно"))
        self.print_slowly("--- КІНЕЦЬ ---\n")
        self.location_1()


if __name__ == "__main__":
    game = Game()
    game.start()
