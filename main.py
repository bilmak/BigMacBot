from llm import chat_with_gpt
import orders
import handler


def print_order(order):
    if not order.user_order:
        print("Your order: Empty\n")
        return

    names = []
    for item in order.user_order:
        names.append(item["name"])

    print("Your order:", ", ".join(names), "\n")


if __name__ == "__main__":
    order = orders.Order()

    user_input = input("What do you want to order?\n").strip()
    if user_input.lower() == "no":
        print("Ok, no order.")
    else:
        if not order.is_item_in_menu(user_input):
            print(f"We don't have {user_input} in menu\n")
        else:
            if "meal" in user_input.lower():
                order.add_meal(
                    user_input,
                    handler.handle_meal_fries(order, user_input),
                    handler.handle_meal_drinks(order, user_input),
                )
            else:
                order.add_raw_item(user_input)
                print(f"You added {user_input}")

        while user_input.lower() != "no":
            print_order(order)

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
            # delete
            elif user_input.lower().startswith("delete "):
                item_name = user_input[7:].strip()
                order.delete_item(item_name)
            # update
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
                    if "meal" in user_input.lower():
                        order.add_meal(
                            user_input,
                            handler.handle_meal_fries(order, user_input),
                            handler.handle_meal_drinks(order, user_input),
                        )
                    else:
                        order.add_raw_item(user_input)
                        print(f"You added {user_input}")

        print(f"Total: {order.calculate_total():.2f}")

        names = [item["name"] for item in order.user_order]
        print("Items:", ", ".join(names))
