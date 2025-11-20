from llm import chat_with_gpt

if __name__ == "__main__":
    while True:
        user_input = input(
            "Hi, my hungry friend, what do you want to order?\n")
        if user_input.lower() in ['bye']:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)


# handler.py

def handle_burger_additionals(order, burger_name: str) -> None:
    """
    Питає користувача про додаткові інгредієнти до бургера
    і додає бургер (з додатками або без) у order.user_order.
    """

    burger_name_clean = burger_name.strip().lower()

    # 1. Шукаємо бургер в items
    burger_item = None
    for item in order.menu_data.get("items", []):
        if item.get("name", "").strip().lower() == burger_name_clean:
            burger_item = item
            break

    if burger_item is None:
        print(f"We don't have {burger_name} in menu as a burger.\n")
        return

    # 2. Можливі інгредієнти (імена) для цього бургера
    possible_ingredients_names = burger_item.get("possible_ingredients", [])

    if not possible_ingredients_names:
        # якщо додаткових інгредієнтів нема — просто додаємо бургер як звичайний айтем
        order.add_raw_item(burger_item["name"])
        print(
            f"You added {burger_item['name']} (no extra ingredients available).\n")
        return

    # 3. Робимо мапу всіх інгредієнтів з їх цінами з секції 'ingredients'
    ingredients_list = order.menu_data.get("ingredients", [])
    ingredients_by_name = {ing["name"]: ing for ing in ingredients_list}

    # 4. Питаємо, чи взагалі юзер хоче щось додати
    print(f"You can add extra ingredients to {burger_item['name']}.")
    print("Available extras:", ", ".join(possible_ingredients_names))

    additionals = []

    want_extra = input(
        "Do you want to add extra ingredients? (yes/no)\n").strip().lower()
    if want_extra not in ("yes", "y"):
        # просто додаємо бургер без додатків
        order.add_raw_item(burger_item["name"])
        print(f"You added {burger_item['name']} without extra ingredients.\n")
        return

    # 5. Цикл вибору інгредієнтів
    while True:
        ing_name = input("Which ingredient do you want to add?\n").strip()

        if ing_name not in possible_ingredients_names:
            print(
                "You can't add this ingredient to this burger. Choose from the list above.\n")
            continue

        if ing_name not in ingredients_by_name:
            print("This ingredient has no price in 'ingredients'. Can't add it.\n")
            continue

        # кількість інгредієнта
        number_str = input(
            "How many of this ingredient do you want? (default: 1)\n").strip()
        if number_str == "":
            number = 1
        else:
            try:
                number = int(number_str)
                if number <= 0:
                    print("Number must be positive.\n")
                    continue
            except ValueError:
                print("Please enter a valid number.\n")
                continue

        additionals.append({"name": ing_name, "number": number})
        print(f"Added extra: {ing_name} x{number}")

        more = input(
            "Do you want to add one more ingredient? (yes/no)\n").strip().lower()
        if more not in ("yes", "y"):
            break

    # 6. Скільки бургерів з такими самими додатками
    qty_str = input(
        f"How many '{burger_item['name']}' with these extras do you want? (default: 1)\n").strip()
    if qty_str == "":
        quantity = 1
    else:
        try:
            quantity = int(qty_str)
            if quantity <= 0:
                quantity = 1
        except ValueError:
            quantity = 1

    # 7. Додаємо в order через твій метод
    order.add_burger_ingredients(burger_item["name"], additionals, quantity)

    extras_text = ", ".join(f"{a['name']} x{a['number']}" for a in additionals)
    print(
        f"You added {quantity} x {burger_item['name']} with extras: {extras_text}\n")


# mainimport handler

# ... всередині циклу в main.py, де user_input — назва айтема

if not order.is_item_in_menu(user_input):
    print(f"We don't have {user_input} in menu\n")
else:
    # перевіряємо, чи це бургер (category == "burgers")
    burger_item = None
    for item in order.menu_data.get("items", []):
        if item.get("name", "").lower() == user_input.lower() and item.get("category") == "burgers":
            burger_item = item
            break

    if burger_item:
        # це бургер → питаємо про додаткові інгредієнти
        handler.handle_burger_additionals(order, user_input)
    else:
        # це не бургер → звичайний айтем
        order.add_raw_item(user_input)
        print(f"You added {user_input}")
