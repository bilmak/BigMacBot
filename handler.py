
def handle_meal_fries(order, meal_name: str) -> str:
    if "meal" not in meal_name.lower() or not order.is_item_in_menu(meal_name):
        return ""

    fries_options = order.get_combo_slot_fries(meal_name)

    input_type_of_fries = input(
        f"What kind of fries do you want?\nOptions: {', '.join(fries_options)}\n"
    ).strip()

    if not input_type_of_fries:
        print("Ok, I add French Fries\n")
        return "French Fries"

    if input_type_of_fries in fries_options:
        print(f"You ordered {meal_name} with {input_type_of_fries}\n")
        return input_type_of_fries

    print(f"We don't have '{input_type_of_fries}'. I add French Fries\n")
    return "French Fries"


def handle_meal_drinks(order, meal_name: str)->str:
    if "meal" not in meal_name.lower() or not order.is_item_in_menu(meal_name):
        return ""

    drinks_options = order.get_combo_slot_drinks(meal_name)
    while True:
        input_type_of_drinks = input(
            f"What kind of drinks do you want?\nOptions: {', '.join(drinks_options)}\n"
        ).strip()

        if input_type_of_drinks in drinks_options:
            print(f"You ordered {meal_name} with {input_type_of_drinks}")
            return input_type_of_drinks

        print(
            f"We don't have {input_type_of_drinks}. Try again\n"
        )
