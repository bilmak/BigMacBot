from llm import chat_with_gpt
import orders


if __name__ == "__main__":
    order = orders.Order()

    user_input = input("what do you want to order?\n")
    order.add_item(user_input)

    while user_input.lower() != "no":
        print(
            f"\nYou ordered: {', '.join(order.user_order)}."
            "\nIf you want to add something else, write it below or say 'no'.\n"
        )
        user_input = input().strip()
        if not user_input:
            continue
        if user_input.lower() == "no":
            break

        order.add_item(user_input)

    print(order.calculate_total())


# while True:
#     user_input = input(
#         "Hi, my hungry friend, what do you want to order?\n")
#     if user_input.lower() in ['bye']:
#         break

#     response = chat_with_gpt(user_input)
#     print("Chatbot:", response)
