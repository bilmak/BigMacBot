import menu

menu_data = menu.Menu("menu_ingredients.yaml")
menu_data_upsell = menu.MenuUpsell("menu_upsells.yaml")


def handler_meal_fries(meal_name: str) -> str:
    if "meal" not in meal_name.lower():
        return ""

    fries_options = menu_data.get_combo_slot_fries(meal_name)

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


def handler_meal_drinks(meal_name: str) -> None | str:
    if "meal" not in meal_name.lower():
        return ""

    drinks_options = menu_data.get_combo_slot_drinks(meal_name)
    while True:
        input_type_of_drinks = input(
            f"What kind of drinks do you want?\nOptions: {', '.join(drinks_options)}\n"
        )

        if input_type_of_drinks in drinks_options:
            print(f"You ordered {meal_name} with {input_type_of_drinks}")
            return input_type_of_drinks

        print(
            f"There is no default drink product, so be sure to choose it yourself.\n"
        )


def handler_desserts(order, dessert_name: str) -> None | str:
    if "meal" in dessert_name.lower():
        return ""
    desserts = menu_data_upsell.get_desserts_options()
    dessert_list = "\n".join(f"- {d}" for d in desserts)
    while True:
        message = input(
            f"Do you want to order dessert? We have:\n{dessert_list}\n yes/no?").strip().lower()
        if message in ("no", "n", ""):
            return
        if message in ("yes", "y"):
            dessert_input = input("What dessert do you want?\n").strip()
            order.add_raw_item(dessert_input)
            print(f"Added {dessert_input} to your order\n")
            return


def handler_item_size(item_name: str) -> None | str:
    if "meal" in item_name.lower():
        return ""

    size_options = menu_data.get_item_sizes(item_name)
    # only for milk
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


def handler_burger(name: str) -> dict:
    if "meal" in name.lower():
        return {"name": name, "additionals": [], "removed": []}

    burger = menu_data.get_burger_options(name)
    if burger is None:
        print("We don't have this burger in menu\n")
        return {"name": name, "additionals": [], "removed": []}

    default_ings = burger.get("default_ingredients", [])
    possible_ings = burger.get("possible_ingredients", [])

    additionals: list[dict] = []
    removed: list[dict] = []

    print(f"\nCustomizing your {name}:\n")
    if default_ings:
        print(f"Default ingredients: {', '.join(default_ings)}\n")
    if possible_ings:
        print(f"Possible additions: {', '.join(possible_ings)}\n")

    while True:
        add = input(
            "What ingredients do you want to add? press Enter for stop\n").strip()
        if not add:
            break

        if add not in possible_ings:
            print("We dont have this ingredients in menu\n")
            continue

        number_str = input(
            f"How many {add} do you wan to add? (default 1) {add}\n").strip()
        if number_str.isdigit():
            number = int(number_str)
        else:
            number = 1
        additionals.append({"name": add, "number": number})
        print(f"Added {add} {number} times \n")

    while True:
        remove = input(
            "What ingredients do you want to remove?Press Enter for not changing\n").strip()
        if not remove:
            break
        if remove not in default_ings:
            print("You can't remove this ingredient.")
            continue
        removed.append({"name": remove})
        print(f"Removed {remove}\n")

    return {
        "name": burger["name"],
        "additionals": additionals,
        "removed": removed,
    }


def handler_sauce(meal_name: str) -> str:
    if "meal" not in meal_name.lower():
        return ""

    sauce_options = menu_data_upsell.get_souce_options_for_meal(meal_name)
    if not sauce_options:
        return ""

    answer = input(
        f"Do you want to add sauce to your burger meal? Options: {','.join(sauce_options)} (yes/no)\n").strip().lower()
    if answer not in ("yes", "y", "ye"):
        return ""
    sauce_choice = input("What kind of sauce do you want to add?\n").strip()
    if sauce_choice in sauce_options:
        print(f"Added {sauce_choice} to your order\n")
        return sauce_choice
    print("We dont have this type of sauce. No sauce added\n")
    return ""
