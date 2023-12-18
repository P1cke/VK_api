import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tok import TOKEN #Импротировать файл с токеном TOKEN = ''
from func import create_betting_menu, create_main_menu, create_bet_selection_keyboard, \
    create_cancel_keyboard, create_matches_keyboard

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

users_balance = {}
users_bets = {}


def send_message(user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        keyboard=keyboard
    )


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message_text = event.text.lower()

            if message_text == "начать":
                users_balance[user_id] = 5000
                send_message(user_id, "Привет! Я бот для ставок на киберспортивные матчи.",
                             create_main_menu())

            elif message_text == "баланс 💸":
                balance = users_balance.get(user_id, 0)
                send_message(user_id, f"Ваш текущий баланс: {balance}", create_main_menu())

            elif message_text == "история ставок 👑":
                bets_history = users_bets.get(user_id, [])
                history_text = "\n".join(bets_history) if bets_history else "У вас пока нет ставок"
                send_message(user_id, f"История ваших ставок:\n{history_text}", create_main_menu())

            elif message_text == "ставки 🏆":
                send_message(user_id, "Выберите дисциплину:", create_betting_menu())

            elif message_text == "назад":
                send_message(user_id, "Выберите действие:", create_main_menu())

            elif message_text in ["cs 2🎯", "dota 2📸"]:
                send_message(user_id, "Выберите матч:", create_matches_keyboard(message_text))

            elif message_text in ["psuti-hqd", "nvpg-navi", "g2-c9", "vitality-spirit"]:
                users_bets[user_id] = {"match": message_text.capitalize()}
                send_message(user_id,
                             f"Вы выбрали матч: {message_text.capitalize()}. Выберите ставку: П1, П2 или ничья.",
                             create_bet_selection_keyboard(users_bets[user_id]["match"]))

            elif "п1" in message_text.lower() or "п1" in message_text.lower() or "ничья" in message_text.lower():
                users_bets[user_id]["bet"] = message_text.capitalize()
                send_message(user_id, "Введите сумму ставки:", create_cancel_keyboard())


            elif message_text.isdigit() and int(message_text) > 0 and "bet" in users_bets[user_id]:
                users_bets[user_id]["amount"] = int(message_text)
                place_bet(user_id)
                send_message(user_id, get_bet_confirmation(user_id), create_main_menu())

            elif message_text == "отмена":
                send_message(user_id, "Выберите ставку: П1, П2 или ничья.", create_bet_selection_keyboard())


def place_bet(user_id):
    user_bet = users_bets.get(user_id, {})
    match = user_bet.get("match")
    bet = user_bet.get("bet")
    amount = user_bet.get("amount")

    coefficients = {
        "psuti-hqd": {"П1": 1.5, "П2": 2.0, "Ничья": 1.8},
        "nvpg-navi": {"П1": 1.7, "П2": 1.9, "Ничья": 1.5},
        "g2-c9": {"П1": 1.6, "П2": 1.7, "Ничья": 1.6},
        "vitality-spirit": {"П1": 1.8, "П2": 2.0, "Ничья": 1.9}
    }

    match_coef = coefficients.get(match.lower(), {})
    coef = match_coef.get(bet.lower(), 0)

    if user_id in users_balance:
        users_balance[user_id] -= amount
    else:
        users_balance[user_id] = -amount
    if user_id in users_bets:
        if "bets" in users_bets[user_id]:
            users_bets[user_id]["bets"].append(f"Матч: {match}, Ставка: {bet}, Кэф: {coef}, Цена: {amount}")
        else:
            users_bets[user_id]["bets"] = [f"Матч: {match}, Ставка: {bet}, Кэф: {coef}, Цена: {amount}"]
    else:
        users_bets[user_id] = {"bets": [f"Матч: {match}, Ставка: {bet}, Кэф: {coef}, Цена: {amount}"]}

    return coef


def get_bet_confirmation(user_id):
    user_bet = users_bets[user_id]
    match = user_bet["match"]
    bet = user_bet["bet"]
    amount = user_bet["amount"]
    return f"Вы поставили на матч '{match}', на '{bet}', сумма ставки '{amount}'."


if __name__ == '__main__':
    main()