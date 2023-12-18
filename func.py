from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def create_main_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Ставки 🏆", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Баланс 💸", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("История ставок 👑", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Магазин 🛒", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


def create_betting_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("CS 2🎯", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Dota 2📸", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


def create_matches_keyboard(game):
    keyboard = VkKeyboard(one_time=True)
    matches = []

    if game == "cs 2🎯":
        matches = ["PSUTI-HQD", "NVPG-Navi", "G2-C9", "Vitality-Spirit"]
    elif game == "dota 2📸":
        matches = ["PSUTI-HQD", "NVPG-Navi", "G2-C9", "Vitality-Spirit"]

    for match in matches:
        keyboard.add_button(match.capitalize(), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()

    keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


def create_bet_selection_keyboard(match):
    keyboard = VkKeyboard(one_time=True)

    coefficients = {
        "psuti-hqd": {"П1": 1.5, "П2": 2.0, "Ничья": 1.8},
        "nvpg-navi": {"П1": 1.7, "П2": 1.9, "Ничья": 1.5},
        "g2-c9": {"П1": 1.6, "П2": 1.7, "Ничья": 1.6},
        "vitality-spirit": {"П1": 1.8, "П2": 2.0, "Ничья": 1.9}
    }

    match_coef = coefficients.get(match.lower(), {})

    keyboard.add_button(f"П1 ({match_coef.get('П1', 0)})", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(f"П2 ({match_coef.get('П2', 0)})", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(f"Ничья ({match_coef.get('Ничья', 0)})", color=VkKeyboardColor.PRIMARY)

    keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


def create_cancel_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Отмена", color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()