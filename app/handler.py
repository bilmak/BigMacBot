from . import menu
from .double_deals import DoubleDeals
from .orders import Order

menu_data = menu.Menu("data/menu_ingredients.yaml")
menu_data_upsell = menu.MenuUpsell("data/menu_upsells.yaml")


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
        # print(f"You ordered {meal_name} with {input_type_of_fries}\n")
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
        ).strip()

        for opt in drinks_options:
            if input_type_of_drinks.lower() == opt.lower():
                return opt
        if input_type_of_drinks in drinks_options:
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
        f"Do you want to add sauce to your burger meal?\n"
        f"Options: {', '.join(sauce_options)}\n"
        "Type sauce name or 'no' to skip\n").strip()

    if not answer or answer.lower() in ("no", 'n'):
        return ""

    for s in sauce_options:
        if s.lower() == answer.lower():
            print(f"Added {s} to your order\n")
            return s

    print("We dont have this type of sauce. No sauce added\n")
    return ""


def handler_double_deal(burger_name: str, double_deals: DoubleDeals, order: Order) -> bool:
    deal = double_deals.get_deal_for_burger(burger_name)
    if not deal:
        return False

    deal_name = deal.get("name", "Double Deal")
    possible_items = deal.get("possible_items", [])

    print(f"This burger is part of {deal_name}")
    print("Available burgers for this Double Deal:")
    for item in possible_items:
        print(f"- {item}")
    raw = input(
        "Do you want to create a Double Deal and get 20% discount on 2 burgers? (yes/no)\n").strip().lower()
    if raw not in ("yes", "ye", "y"):
        return False

    burgers_chosen = [burger_name]
    while len(burgers_chosen) < 2:
        second = input("Please choose the second burger from list\n").strip()
        if second not in possible_items:
            print("We dont have this burger in menu, try again\n")
            continue
        burgers_chosen.append(second)

    for b_name in burgers_chosen:
        order.add_raw_item(b_name)
        order.user_order[-1]["double_deal"] = True
    print(
        f"Double Deal added:{burgers_chosen[0]} and {burgers_chosen[1]} with 20% discont\n")
    return True


def handler_deals_keyword(double_deals: DoubleDeals, order: Order) -> bool:

    small = double_deals.get_deal_by_name("Small Double Deal")
    big = double_deals.get_deal_by_name("Big Double Deal")
    print("\nAvailable deals:")
    print("Small double deals include: " +
          ", ".join(small.get("possible_items", [])))

    print("Big double deals include: " +
          ", ".join(big.get("possible_items", [])))

    deal_type = input(
        "Which double deal do you want? Small or Big?\n").strip().lower()
    if deal_type.startswith("s"):
        deal = small
    elif deal_type.startswith("b"):
        deal = big
    else:
        print("Unknown double deal\n")
        return False

    burger_chosen: list[str] = []
    possible_items = deal.get("possible_items", [])

    while len(burger_chosen) < 2:
        id = len(burger_chosen)+1
        choice = input(f"Choose burger{id} from the list:\n").strip()
        if choice not in possible_items:
            print("This burger not in deal list, try again")
            continue
        burger_chosen.append(choice)

    for b_name in burger_chosen:
        order.add_raw_item(b_name)
        order.user_order[-1]["double_deal"] = True

    print(
        f"Double deal created: {burger_chosen[0]} and {burger_chosen[1]} with 20% discount\n")
    return True
