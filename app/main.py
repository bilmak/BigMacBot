from . import orders, handler, upsell, calculator
import json
from .menu import Menu, MenuUpsell


def process_item(user_input: str, order: orders.Order, data_menu: Menu, upsells: upsell.Upseller):

    if not data_menu.is_item_in_menu(user_input):
        print(f"We don't have {user_input} in menu\n")
        return
    if "meal" in user_input.lower():
        order.add_meal(
            user_input,
            handler.handler_meal_fries(user_input),
            handler.handler_meal_drinks(user_input),
        )
        sauce = handler.handler_sauce(user_input)
        if sauce:
            order.add_raw_item(sauce)
    else:
        if data_menu.is_burger(user_input):
            if upsells.offer_meal_upsell(user_input):
                return
            answer = input(
                "Do you want to customize this burger? (yes/no)\n").strip().lower()
            if answer in ("yes", "y", "ye"):
                burger_data = handler.handler_burger(user_input)
                order.user_order.append(burger_data)
                print("You customized your burger")
            else:
                size = handler.handler_item_size(user_input)
                order.add_raw_item(user_input, size)
                if size:
                    print(f"You added {size} {user_input}")
                else:

                    print(f"You added {user_input}")
        else:
            size = handler.handler_item_size(user_input)
            order.add_raw_item(user_input, size)
            if size:
                print(f"You added {size} {user_input}")
            else:
                print(f"You added {user_input}")


def print_order(order):
    if not order.user_order:
        print("Your order: []\n")
        return

    print("Your order:", json.dumps(order.user_order), "\n")


if __name__ == "__main__":
    order = orders.Order()
    data_menu = Menu("data/menu_ingredients.yaml")
    data_menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calcul = calculator.Calculator(data_menu, data_menu_upsell)
    upsells = upsell.Upseller(order, data_menu_upsell)

    user_input = input("What do you want to order?\n").strip()
    if user_input.lower() in ("no", ""):
        print("Ok, no order")
    else:
        process_item(user_input, order, data_menu, upsells)
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
                process_item(user_input, order, data_menu, upsells)
        upsells.offer_dessert()
        total = calcul.calculate_total(order.user_order)

        if calcul.discount:
            print("\tYou received a 20% discount on 2 combo meals!\n")
        print(f"Total: {total:.2f}")
        print("Items:", json.dumps(order.user_order))
