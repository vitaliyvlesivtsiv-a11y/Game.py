"""
=====================================================
ГРА: ВТЕЧА З ДЖУНГЛІВ
=====================================================
Це текстова пригодницька гра, де гравець повинен:
1. Вибирати різні шляхи у джунглях
2. Збирати предмети (ніж, аптечку)
3. Взаємодіяти з персонажами (мандрівник)
4. Робити моральні вибори (мирно чи агресивно)

МЕХАНІКА ГАРИ:
- HP (Здоров'я): 100 (на початку), може зменшуватися
- Damage (Шкода): 10 (базова), збільшується з ножем (+20)
- Inventory (Інвентар): список предметів у гравця
- Локації: різні місця у джунглях з різними подіями
- Вибори: гравець керує розвитком сюжету

=====================================================
"""

import json  # Для збереження прогресу гри
import sys  # Для роботи з системними операціями
import time  # Для додавання затримок (sleep)
from pathlib import Path  # Для роботи з шляхами до файлів збереження
from random import randint  # Для генерування випадкових чисел

# Основний клас гри - всі методи та властивості гри містяться тут
class Game:
    SCREEN_WIDTH = 70  # Ширина екрану для центрування тексту

    def __init__(self, save_file=None):
        # Ініціалізація всіх параметрів гравця на початку гри
        self.player_hp = 100  # Здоров'я гравця (початкове: 100)
        self.has_knife = False  # Чи має гравець ніж (спочатку False)
        self.has_medkit = False  # Чи має гравець аптечку (спочатку False)
        self.has_shield = False  # Чи має гравець щит (спочатку False)
        self.inventory = []  # Список предметів у інвентарі гравця
        self.text_delay = 0  # Затримка для посимвольного виводу тексту (0 = миттєво)
        self.damage = 10  # Базова шкода гравця
        self.save_file = Path(save_file) if save_file else Path("game_save.json")
        self.load_game()

    def choose_text_speed(self):
        """Запитує швидкість поступового виводу тексту та зберігає у self.text_delay."""
        # Словник з варіантами швидкості (затримка в секундах, назва швидкості)
        speed_settings = {
            "1": (0, "миттєво"),  # 0 затримки - виводимо весь текст одразу
            "2": (0.01, "швидко"),  # 0.01 с - дуже швидко посимвольно
            "3": (0.025, "середньо"),  # 0.025 с - середня швидкість
            "4": (0.04, "повільно"),  # 0.04 с - повільно
            "5": (0.07, "дуже повільно"),  # 0.07 с - дуже повільно посимвольно
        }

        # Виводимо заголовок меню вибору швидкості
        self.print_title("Оберіть швидкість появи тексту")
        # Показуємо опції (виводимо центровано по ширині екрану)
        self.print_slowly("1 — миттєво ".center(self.SCREEN_WIDTH))
        self.print_slowly("2 — швидко".center(self.SCREEN_WIDTH))
        self.print_slowly("3 — середньо".center(self.SCREEN_WIDTH))
        self.print_slowly("4 — повільно".center(self.SCREEN_WIDTH))
        self.print_slowly("5 — дуже повільно".center(self.SCREEN_WIDTH))

        # Нескінченний цикл, поки гравець не введе коректний вибір
        while True:
            # Просимо гравця ввести цифру 1-5
            choice = input("Ваша швидкість (1–5): ").strip()
            # Перевіряємо, чи вибір є в словнику
            if choice in speed_settings:
                # Встановлюємо затримку і запам'ятовуємо назву швидкості
                self.text_delay, speed_name = speed_settings[choice]
                # Повідомляємо гравцю про обраний вибір
                self.print_slowly(f"\nОбрано швидкість: {speed_name}.")
                return  # Виходимо з методу, швидкість встановлена

            # Якщо вибір неправильний - просимо спробувати ще раз
            print("Будь ласка, введіть число від 1 до 5.")

    def print_title(self, title):
        """Виводить великий заголовок по центру консолі з рамкою з '='."""
        self.print_slowly("\n" + "=" * self.SCREEN_WIDTH)  # Верхня лінія
        self.print_slowly(title.upper().center(self.SCREEN_WIDTH))  # Заголовок по центру, великими літерами
        self.print_slowly("=" * self.SCREEN_WIDTH)  # Нижня лінія

    def print_slowly(self, text="", end="\n"):
        """Виводить текст посимвольно з обраною затримкою (або миттєво якщо затримка = 0)."""
        if self.text_delay == 0:
            # Якщо затримка = 0, виводимо весь текст одразу
            print(text, end=end)
            return

        # Посимвольний вивід тексту з затримкою
        for character in text:
            sys.stdout.write(character)  # Пишемо один символ
            sys.stdout.flush()  # Очищуємо буфер, щоб символ з'явився одразу
            time.sleep(self.text_delay)  # Чекаємо затримку перед наступним символом

        sys.stdout.write(end)  # Пишемо символ завершення (новий рядок)
        sys.stdout.flush()

    def save_game(self):
        """Зберігає поточний стан гри у JSON-файл."""
        data = {
            "player_hp": self.player_hp,
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
        self.has_medkit = data.get("has_medkit", False)
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
        # Спочатку просимо гравця вибрати швидкість тексту
        self.choose_text_speed()
        # Гра починається з питання про ім'я гравця
        self.print_slowly("!Всі відповіді треба писати з маленької букви без зайвих пробілів!")
        name = input("Впишіть ім'я: ")
        time.sleep(2)  # Невелика пауза для занурення гравця у гру
        # Привіт від Духу-хранителя джунглів
        self.print_slowly(f"Привіт, {name}, я Дух-хранитель цих джунглів і ти реінкарувався на моїх землях")
        time.sleep(2)  # Пауза перед наступним повідомленням
        # Описання завдання і дарування факела
        self.print_slowly("Оскільки ти тут не знайомий з середовищем я тобі дам факел який завжи горить і допоможе тобі відлякувати хижих істот")
        time.sleep(2)  # Пауза для ефекту
        # Основне завдання гри - зібрати 3 частини артефакту
        self.print_slowly("Твоє завдання зібрати 3 частини артефакту щоб вибратись з цих джунглів. Удачі!")
        time.sleep(1)  # Коротка пауза перед стартом гри
        # Стартуємо гру з першої локації
        self.location_1()

    def location_1(self):
        """Перша локація - заросла стежка з трьома шляхами."""
        self.print_title(" ЗАРОСЛА СТЕЖКА")
        # Описуємо локацію гравцю
        self.print_slowly("Ти опинився на зарослій стежці. Перед тобою три шляхи: густі кущі, підвісний міст, та покинутий табір.")
        # Пропонуємо вибір
        self.print_slowly("Куди ти хочеш піти? (кущі: 1/міст: 2/табір: 3)")
        # Отримуємо вибір гравця
        choice = input("Ваш вибір: ").strip()
        
        # Розгалуження за вибором
        if choice == 1 or choice == "1":
            # Якщо гравець обирає кущі - переходимо до location_1_1
            self.location_1_1()
        elif choice == 2 or choice == "2":
            # Якщо гравець обирає міст - переходимо до location_1_2
            self.location_1_2()
        elif choice == 3 or choice == "3":
            # Якщо гравець обирає табір - переходимо до location_1_3
            self.location_1_3()
        else:
            # Якщо гравець введе щось інше - просимо спробувати ще раз
            self.print_slowly("Невірний вибір. Спробуй ще раз.")
            self.location_1()

    def location_1_1(self):
        """Друга локація - густі кущі з мертвецем і ножем."""
        # Описуємо сцену з мертвецем
        self.print_slowly("Ти обрав шлях через густі кущі. Раптом ти бачиш труп біля якого лежить змія в яку втикнутий ніж. Ти можеш оглянути труп або повернутися назад на стежку.")
        # Першій вибір: оглянути чи повернутися
        self.print_slowly("Що ти робиш? (оглянути/повернутися)")
        choice = input("Ваш вибір: ").strip()
        
        if choice == "оглянути":
            # Якщо оглядаємо труп - див ніж
            self.print_slowly("Ти підійшов до трупа і побачив, що ніж в ньому. Ти можеш взяти ніж або повернутися назад на стежку.")
            # Другий вибір: взяти ніж чи повернутися
            self.print_slowly("Що ти робиш? (взяти/повернутися)")
            choice = input("Ваш вибір: ").strip()
            
            if choice == "взяти":
                # Перевіряємо, чи вже має гравець ніж
                if self.has_knife:
                    self.print_slowly("Ти вже підібрав ніж раніше.")
                    self.location_1_1()  # Повертаємось до цієї локації
                else:
                    # Даємо гравцю ніж, додаємо до інвентарю і збільшуємо шкоду
                    self.has_knife = True
                    self.inventory.append("ніж")
                    self.damage += 20  # Ніж дає +20 шкоди
                    self.save_game()
                    self.print_slowly("Ти підібрав ніж! Твоя шкода збільшилася на 20.")
                    self.location_1_1()  # Повертаємось до цієї локації
            elif choice == "повернутися":
                # Повертаємось на першу локацію
                self.print_slowly("Ти повертаєшся назад на стежку.")
                self.location_1()
            else:
                # Невірний вибір - пробуємо ще раз
                self.print_slowly("Невірний вибір. Спробуй ще раз.")
                self.location_1_1()
        elif choice == "повернутися":
            # Повертаємось на першу локацію
            self.print_slowly("Ти повертаєшся назад на стежку.")
            self.location_1()
        else:
            # Невірний вибір - пробуємо ще раз
            self.print_slowly("Невірний вибір. Спробуй ще раз.")
            self.location_1_1()

    def location_1_2(self):
        """Третя локація - підвісний міст з випадковим наслідком."""
        # Описуємо міст
        self.print_slowly("Ти обрав шлях через підвісний міст. Міст був старим і тріщав.")
        # Генеруємо випадкове число (1 або 2)
        random_number = randint(1, 2)
        
        if random_number == 1:
            # Гравець успішно перейшов міст (50% шанс)
            self.print_slowly("Ти успішно перейшов міст і опинився на іншому боці.")
            self.location_2()  # Переходимо до наступної локації
        else:
            # Міст обвалився і гравець втратив здоров'я (50% шанс)
            self.print_slowly("Міст обвалився і ти впав у річку. Ти втратив 30 здоров'я. Річка донесла тебе до таємничого болота.")
            self.player_hp -= 30  # Віднімаємо 30 HP
            self.save_game()
            self.location_2()  # Переходимо до наступної локації

    def location_1_3(self):
        """Четверта локація - покинутий табір з аптечкою."""
        # Описуємо табір
        self.print_slowly("Ти обрав шлях через покинутий табір. Табір був порожнім, але ти знайшов аптечку.")
        # Даємо гравцю аптечку
        self.has_medkit = True
        self.inventory.append("аптечка")
        self.save_game()
        self.print_slowly("Ти підібрав аптечку! Ти можеш відновити 50 здоров'я.")
        time.sleep(1)  # Невелика пауза перед продовженням
        self.print_slowly("Ти повернувся назад")
        self.location_1()  # Повертаємось на першу локацію

    def location_2(self):
        """Друга локація - болото забутих з мандрівником."""
        # Великий заголовок локації
        self.print_title(" БОЛОТО ЗАБУТИХ")
        # Описуємо атмосферу місця
        self.print_slowly("Ви стоїте посеред туманного болота. Повітря важке, під ногами хлюпає вода.")
        self.print_slowly("Ви бачите постать мандрівника, що сидить на старому пні.")
        
        # Діалог з мандрівником
        self.print_slowly("\nМандрівник дивиться на вас і усміхається:")
        self.print_slowly('"Вітаю, гравець. Болото сьогодні особливо мовчазне, чи не так?"')
        # Жарт від мандрівника
        self.print_slowly("Тримай жарт для підняття духу: ")
        self.print_slowly('Бо вони постійно бояться, що їх "зажаблять"!')
        # Мандрівник дарує аптечку
        self.print_slowly("\nВін простягає вам аптечку: 'Візьми, тобі це знадобиться.'")

        # Формуємо меню опцій
        options = ["1 - Взяти аптечку мирно"]  # Завжди доступна опція - взяти аптечку мирно
        if self.has_knife:
            # Якщо гравець має ніж - додаємо опцію атаки
            options.append("2 - Напасти на мандрівника з ножем")
        else:
            # Якщо ножа немає - повідомляємо про це
            self.print_slowly("У вас немає ножа, тому напасти на мандрівника неможливо.")

        # Виводимо опції
        for option in options:
            self.print_slowly(option.center(self.SCREEN_WIDTH))

        # Отримуємо вибір гравця
        choice = input("Ваш вибір: ").strip()

        # Якщо гравець атакує з ножем
        if choice == "2" and self.has_knife:
            # Сцена атаки
            self.print_slowly("\nВи різко вихоплюєте ніж і нападаєте на мандрівника...")
            self.print_slowly("Той падає...")
            self.print_slowly('Мандрівник на останньому подиху шепоче: "Ти робиш велику помилку..."')
            # Мандрівник має ще дві аптечки у своїх речах
            self.print_slowly("З його речей випадають дві аптечки.")
            # Додаємо обидві аптечки до інвентарю
            self.inventory.append("аптечка")
            self.inventory.append("аптечка")
            self.save_game()
            self.print_slowly("Ви взяли 2 аптечки!")

        # Якщо гравець обирає мирний варіант
        elif choice == "1":
            self.print_slowly("\nВи дякуєте мандрівнику і забираєте аптечку.")
            # Додаємо одну аптечку до інвентарю
            self.inventory.append("аптечка")
            self.save_game()
            self.print_slowly("Ви взяли аптечку!")

        # Якщо гравець введе щось інше
        else:
            self.print_slowly("\nНевірний вибір. Ви нічого не отримали.")

        if self.has_knife:
            self.print_slowly("\nОбміркуйте,зустріч могла завершитись інакше")
            time.sleep(3)

        def choose_next_location(self):
        self.print_title("Куди йти далі?")
        self.print_slowly("Попереду з'являються дві дороги:")
        self.print_slowly("1 - Дорога до Храму джунглів".center(self.SCREEN_WIDTH))
        self.print_slowly("2 - Дорога до казино".center(self.SCREEN_WIDTH))

             while True:
            choice = input("Куди підете? ").strip()
            if choice == "1":
                self.print_slowly("\nВи вирушаєте до Храму джунглів.")
                location_3()
                return
            if choice == "2":
                self.print_slowly("\nВи вирушаєте до казино.")
                return

            self.print_slowly("Невірний вибір. Введіть 1 або 2.")
        
        
        # Виводимо поточний статус гравця
        self.print_slowly("\nТвоя позиція: HP={}, Damage={}, Inventory={}".format(self.player_hp, self.damage, self.inventory))

        # Пропонуємо гравцю продовжити
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
        time.sleep(2)

    def location_3_1(self):
        answer1 = input("Загадка: Я найвища тварина в джунглях, маю довгу шию. Хто я?")
        if answer1 == 'жираф':
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
            self.print_slowly("Вітаю, ви пройшли храм джунглів")
            self.save_game()


    def location_3_2(self):
        """Друга гілка - пройти крізь пастки і тварин."""
        random_chance = randint(1, 10)  # Генеруємо випадкове число від 1 до 10
        if random_chance < 8:
            # 70% шанс на успіх
            self.print_slowly("Вітаю, ви пройшли всі пастки і відбились від тварин")
            self.location4()
        elif random_chance >= 8:
            # 30% шанс на невдачу
            self.print_slowly("На жаль вам не повезло і ви не пройшли")
            self.player_hp = 0  # Гравець помирає
            self.save_game()

    def location4(self):
        """Фінальна локація гри."""
        self.print_slowly("Ти вийшов з храму і встиг врятуватися. Гра завершена.")
        self.save_game()

    def show_status(self):
        """Показує поточний статус гравця: здоров'я, шкода, інвентар."""
        self.print_slowly("\n--- СТАТУС ---")
        self.print_slowly("Здоров'я: {}".format(self.player_hp))
        self.print_slowly("Шкода: {}".format(self.damage))
        # Якщо інвентар порожний - показуємо "порожно", інакше виводимо елементи
        self.print_slowly("Інвентар: {}".format(", ".join(self.inventory) if self.inventory else "порожно"))
        self.print_slowly("--- КОНЕЦЬ ---\n")


# ============= ГОЛОВНА ПРОГРАМА =============
# Перевіряємо, чи цей файл запущено як головна програма (не імпортовано)
if __name__ == "__main__":
    # Створюємо об'єкт гри
    game = Game()
    # Запускаємо гру
    game.start()
