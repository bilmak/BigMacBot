from llm import chat_with_gpt
import orders


def handle_meal_fries(order, meal_name: str) -> None:
    if "Meal" not in meal_name or not order.is_item_in_menu(meal_name):
        return

    fries_options = order.get_combo_slot_fries(meal_name)

    input_type_of_fries = input(
        f"What kind of fries do you want?\nOptions: {', '.join(fries_options)}\n"
    ).strip()

    if not input_type_of_fries:
        print("Ok, I will skip fries choice.\n")
        return

    if input_type_of_fries in fries_options:
        order.add_item(input_type_of_fries)
        print(f"You ordered {meal_name} with {input_type_of_fries}")
    else:
        print(
            f"We don't have {input_type_of_fries}. I will skip fries choice.\n")


def handle_meal_drinks(order, meal_name):

    if "Meal" not in meal_name or not order.is_item_in_menu(meal_name):
        return
    drinks_options = order.get_combo_slot_drinks(meal_name)
    input_type_of_drinks = input(
        f"What kind of drinks do you want?\nOptions: {', '.join(drinks_options)}\n"
    ).strip()

    if not input_type_of_drinks:
        print("Ok, I will skip drinks choice.\n")
        return

    if input_type_of_drinks in drinks_options:
        order.add_item(input_type_of_drinks)
        print(f"You ordered {meal_name} with {input_type_of_drinks}")
    else:
        print(
            f"We don't have {input_type_of_drinks}. I will skip drinks choice.\n")


if __name__ == "__main__":
    order = orders.Order()

    user_input = input("What do you want to order?\n").strip()
    if user_input.lower() == "no":
        print("Ok, no order.")
    else:
        if not order.is_item_in_menu(user_input):
            print(f"We don't have {user_input} in menu\n")
        else:
            order.add_item(user_input)
            handle_meal_fries(order, user_input)
            handle_meal_drinks(order, user_input)

        while user_input.lower() != "no":
            print(
                f"\nYour order: {', '.join(order.user_order) if order.user_order else 'Empty'}.\n"
            )

            print(
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
                    print(f"We don't have {user_input} in menu\n")
                else:
                    order.add_item(user_input)
                    print(f"You added {user_input}")
                    handle_meal_fries(order, user_input)
                    handle_meal_drinks(order, user_input)

        print(f"Total: {order.calculate_total():.2f}")
        print(f"Items: {', '.join(order.user_order)}")
