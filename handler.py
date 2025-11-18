import orders



def handle_meal_fries(order, meal_name: str) -> None:
    if "Meal" not in meal_name or not order.is_item_in_menu(meal_name):
        return

    fries_options = order.get_combo_slot_fries(meal_name)

    input_type_of_fries = input(
        f"What kind of fries do you want?\nOptions: {', '.join(fries_options)}\n"
    ).strip()

    if not input_type_of_fries:
        print("Ok, I will skip fries choice\n")
        return

    if input_type_of_fries in fries_options:
        order.add_item(input_type_of_fries)
        print(f"You ordered {meal_name} with {input_type_of_fries}")
    else:
        print(
            f"We don't have {input_type_of_fries}. I will skip fries choice\n")


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
