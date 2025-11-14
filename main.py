from llm import chat_with_gpt
import orders


if __name__ == "__main__":
    order = orders.Order()

    user_input = input("what do you want to order?\n")
    if not order.is_item_in_menu(user_input):
        print(f"We dont have {user_input} in menu\n")
    else:
        order.add_item(user_input)

    while user_input.lower() != "no":
        print(
            f"\nYour order: {', '.join(order.user_order) if order.user_order else 'Empty'}.\n"
            "\nIf you want to add something else, write it below."
            "\nIf you want to delete an item, type: delete <item name>."
            "\nIf you want to update an item, type: update <old name> on <new name>."
            "\nOr say 'no' to finish.\n"
        )
        user_input = input().strip()
        if not user_input:
            continue
        if user_input.lower() == "no":
            break

        elif user_input.lower().startswith("delete "):
            item_name = user_input[7:].strip()
            order.delete_item(item_name)

        elif user_input.lower().startswith("update "):
            rest = user_input[7:]
            parts = rest.split(" on ")
            if len(parts) != 2:
                print("Use format: update <old name> on <new name>")
                continue
            old_name = parts[0].strip()
            new_name = parts[1].strip()
            order.update_order(old_name, new_name)

        else:
            if not order.is_item_in_menu(user_input):
                print(f"We dont have {user_input} in menu\n")
            else:
                order.add_item(user_input)
                print(f"You added {user_input}")

    print(f"Total: {order.calculate_total()}")
    print(f"Items: {', '.join(order.user_order)}")


# while True:
#     user_input = input(
#         "Hi, my hungry friend, what do you want to order?\n")
#     if user_input.lower() in ['bye']:
#         break

#     response = chat_with_gpt(user_input)
#     print("Chatbot:", response)
