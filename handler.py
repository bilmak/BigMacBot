
def handler_meal_fries(order, meal_name: str) -> str:
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


def handler_meal_drinks(order, meal_name: str) -> str:
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
            f"There is no default drink product, so be sure to choose it yourself.\n"
        )


def handler_item_size(order, item_name: str) -> str:
    if "meal" in item_name.lower():
        return ""

    size_options = order.get_item_sizes(item_name)
    # for milk
    if not size_options:
        return ""

    while True:
        input_size = input(
            f"What size of {item_name} do you want?\nOptions: {', '.join(size_options)}\n"
        ).strip().lower()
        if not input_size:
            if "medium" in size_options:
                print(f"Ok, I set {item_name} size to medium\n")
                return "medium"
            else:
                print(f"Ok, I set {item_name} size to {size_options[0]}\n")
                return size_options[0]

        if input_size in size_options:
            print(f"Ok, {item_name} {input_size}\n")
            return input_size

        print("Wrong size, choose from the list\n")
