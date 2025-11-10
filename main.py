from chat_bot import chat_with_gpt
import yaml


def load_menu(file_path):
    with open(file_path, 'r') as deals_file:
        data = yaml.safe_load(deals_file)
        return data


def find_menu_and_calculate(menu_data, user_order: list):
    total = 0.00
    for order_name in user_order:
        for item in menu_data["combos"]:
            if order_name == item["name"]:
                total += item["price"]

    return total


if __name__ == "__main__":
    menu_data = load_menu("menu_deals.yaml")

    user_inputs: list[str] = []
    user_input = input("what do you want to order?\n")
    user_inputs.append(user_input)

    while user_input.lower() != "stop":
        print(f"You ordered: {user_input}")
        user_input = input(
            "do you want to add something else? if not say stop\n")
        if user_input == "stop":
            break
        user_inputs.append(user_input)

    print(find_menu_and_calculate(menu_data, user_inputs))


# while True:
#     user_input = input(
#         "Hi, my hungry friend, what do you want to order?\n")
#     if user_input.lower() in ['bye']:
#         break

#     response = chat_with_gpt(user_input)
#     print("Chatbot:", response)
