def separator():
    print("----------------------------------------------")


def get_game_settings():
    settings = {"players_num": 4, "target_score": 200, "rounds_played": 0}

    while True:
        user_input = input("تعداد بازیکنان را وارد نمایید: ").strip()
        if user_input == "":
            break
        if user_input.isdigit() and int(user_input) in [4, 5]:
            settings["players_num"] = int(user_input)
            break
        print("فقط ۴ یا ۵ بازیکن مجاز است!")

    while True:
        target_input = input("بازنده با چند امتیاز تعیین می‌گردد؟ ").strip()
        if target_input == "":
            break
        if target_input.isdigit() and int(target_input) > 0:
            settings["target_score"] = int(target_input)
            break
        print("امتیاز باید عددی مثبت و بزرگتر از صفر باشد!")

    message = f"این بازی {settings['players_num']} نفره، تا امتیاز {
        settings['target_score']} و "
    return settings, message


def create_players_list(num):
    if num not in [4, 5]:
        print("فقط ۴ یا ۵ بازیکن مجاز است!")
        return None, None

    orders = ["اول", "دوم", "سوم", "چهارم", "پنجم"]
    players = []

    for i in range(num):
        while True:
            name = input(f"نام بازیکن {orders[i]} را وارد نمایید: ").strip()
            if name:
                players.append({"name": name, "score": 0})
                break
            print("لطفاً نام معتبری وارد کنید!")

    names = [p["name"] for p in players]
    message = "بین " + "، ".join(names) + " خواهد بود!"
    return players, message


def game_results(settings, players):
    result = "نتایج پیش از شروع بازی:" if settings["rounds_played"] == 0 else "نتایج پس از این دور بازی:"
    sorted_players = sorted(players, key=lambda p: p["score"])
    result += "\n" + \
        "\n".join([f"{p['name']}: {p['score']}" for p in sorted_players])
    return result


def cards_dealer(rounds):
    deals = ["سمت راست", "سمت چپ", "روبرو"]
    deal_num = rounds % 4
    if rounds == 0:
        return f'شروع بازی 🏁\nسه کارت به بازیکن "{deals[deal_num]}" بدهید و بازی کنید'
    if deal_num == 3:
        return f'دور {rounds + 1}ام بازی\nاین دور را "بدون" جابجا کردن کارت بازی کنید'
    return f'دور {rounds + 1}ام بازی\nسه کارت به بازیکن "{deals[deal_num]}" بدهید و بازی کنید'


def get_scores(settings, players):
    round_num = settings["rounds_played"]
    temp_scores, total_score = [], 0

    prompt_msg = "آیا بازیکنان دارای امتیاز اولیه هستند؟ " if round_num == 0 else None
    if round_num == 0:
        while True:
            answer = input(prompt_msg).strip()
            if answer == "":
                return settings, players
            if answer == "بله":
                break
            print("فقط 'بله' یا خالی گذاشتن فیلد مجاز است!")

    for player in players:
        while True:
            label = f"{player['name']} با چند امتیاز بازی را شروع می‌کند؟ " if round_num == 0 else f"امتیاز {
                player['name']} در دور {round_num}ام بازی: "
            inp = input(label).strip()
            if inp == "":
                score = 0
                break
            if inp.isdigit():
                score = int(inp)
                if round_num == 0 and score >= 0:
                    break
                elif round_num > 0 and 0 <= score <= 26:
                    break
            print("لطفاً مقدار صحیح وارد نمایید.")
        temp_scores.append(score)
        total_score += score

    if round_num == 0:
        if total_score % 26 != 0:
            print("جمع امتیاز بازیکنان باید مضربی از ۲۶ باشد!")
            return get_scores(settings, players)
    else:
        if total_score not in [26, 78, 104]:
            print(f"جمع امتیاز بازیکنان ({total_score}) اشتباه است!")
            return get_scores(settings, players)
        if 26 in temp_scores:
            if temp_scores.count(26) != (len(players) - 1) or temp_scores.count(0) != 1:
                print("توزیع امتیاز اشتباه است!")
                return get_scores(settings, players)

    for i in range(len(players)):
        players[i]["score"] += temp_scores[i]

    return settings, players


def game_loser(settings, players):
    sorted_players = sorted(players, key=lambda p: p["score"])
    top = sorted_players[-1]
    return f"{top['name']} با {top['score']} امتیاز بازنده بازی شد!" if top["score"] >= settings["target_score"] else "هنوز هیچ بازنده‌ای مشخص نشده است."


def game_reset():
    answer = input("دوباره بازی می‌کنید؟ ").strip()
    print()
    if answer == "بله":
        separator()
        game_player()
    elif answer == "":
        print("خروج از بازی. 👋")
    else:
        print("ورودی نامعتبر! فقط 'بله' یا خالی مجاز است.")
        game_reset()


def game_player():
    try:
        separator()
        print()
        settings, msg1 = get_game_settings()
        players, msg2 = create_players_list(settings["players_num"])
        print()
        separator()

        print()
        settings, players = get_scores(settings, players)
        print()
        separator()

        print()
        print(msg1 + msg2)
        print()
        separator()

        print()
        print(game_results(settings, players))
        print()
        separator()

        print()
        print(cards_dealer(settings["rounds_played"]))
        print()
        separator()

        while max(p["score"] for p in players) < settings["target_score"]:
            settings["rounds_played"] += 1
            print()
            settings, players = get_scores(settings, players)
            print()
            print(game_results(settings, players))
            print()
            separator()
            print()
            print(cards_dealer(settings["rounds_played"]))
            print()
            separator()

        print()
        print(game_loser(settings, players))
        print()
        separator()
        print()
        game_reset()
        print()
        separator()

    except Exception as e:
        print("خطا در اجرای مراحل بازی:", e)


if __name__ == "__main__":
    game_player()
