from . import orders, handler, upsell, calculator, llm
import json
from .menu import Menu, MenuUpsell, VirtualMenu
from .double_deals import DoubleDeals


def process_item(user_input: str,
                 order: orders.Order,
                 data_menu: Menu,
                 upsells: upsell.Upseller,
                 double_deals: DoubleDeals,
                 size: str | None = None,
                 fries: str | None = None,
                 drink: str | None = None,
                 is_double_deal: bool = False):

    if not data_menu.is_item_in_menu(user_input):
        print(
            f"We don't have {user_input} in menu. Please use exact item names from the menu.\n")
        return

    if "meal" in user_input.lower():
        if not fries:
            fries = handler.handler_meal_fries(user_input)
        if not drink:
            drink = handler.handler_meal_drinks(user_input)
        order.add_meal(
            user_input,
            fries, drink
        )
        sauce = handler.handler_sauce(user_input)
        if sauce:
            order.add_raw_item(sauce)
        return
    else:
        if data_menu.is_burger(user_input):
            if is_double_deal:
                order.add_raw_item(user_input, size)
                order.user_order[-1]["double_deal"] = True
                print(f"You added {user_input} as part of double deal")
                return
            if handler.handler_double_deal(user_input, double_deals, order):
                return

            if upsells.offer_meal_upsell(user_input):
                return
            answer = input(
                "Do you want to customize this burger? (yes/no)\n").strip().lower()
            if answer in ("yes", "y", "ye"):
                burger_data = handler.handler_burger(user_input)
                order.user_order.append(burger_data)
                print("You customized your burger")
            else:
                if not size:
                    size = handler.handler_item_size(user_input)
                order.add_raw_item(user_input, size)
                if size:
                    print(f"You added {size} {user_input}")
                else:

                    print(f"You added {user_input}")
        else:
            if not size:

                size = handler.handler_item_size(user_input)
            order.add_raw_item(user_input, size)
            if size:
                print(f"You added {size} {user_input}")
            else:
                print(f"You added {user_input}")


def validate_llm_items(items_from_llm: list[dict], data_menu: Menu) -> tuple[bool, list[dict]]:
    cleaned: list[dict] = []
    for raw_item in items_from_llm:
        if not isinstance(raw_item, dict):
            return False, []

        name = raw_item.get("name")
        if not name:
            return False, []

        if not data_menu.is_item_in_menu(name):
            print(f"We don't have {name} in menu")
            return False, []

        sizes = data_menu.get_item_sizes(name)
        if sizes and "meal" not in name.lower():
            size = raw_item.get("size")
            if size and size.lower() not in [s.lower() for s in sizes]:
                print(
                    f"Size '{size}' is not valid for {name}. Valid sizes: {', '.join(sizes)}"
                )
                return False, []

        if "meal" in name.lower():
            fries_options = data_menu.get_combo_slot_fries(name)
            drink_options = data_menu.get_combo_slot_drinks(name)

            fries = raw_item.get("fries")
            drink = raw_item.get("drink")

            if fries and fries.lower() not in [f.lower() for f in fries_options]:
                print(f"We don't have {fries} as fries options for {name}")
                return False, []
            if drink and drink.lower() not in [d.lower() for d in drink_options]:
                print(f"We don't have {drink} as drink options for {name}")
                return False, []
        cleaned.append(raw_item)
    return True, cleaned


def process_text(user_input: str,
                 order: orders.Order,
                 data_menu: Menu,
                 upsells: upsell.Upseller,
                 double_deals: DoubleDeals,
                 virtual_menu: VirtualMenu):
    text = user_input.strip().lower()

    virtual_item = virtual_menu.get_virtual_item(text)
    if virtual_item:
        possible = virtual_menu.get_possible_items(text)
        name = virtual_item.get("name", text)

        if possible:
            print(f"Which {name} exactly would you like?")
            print("\n".join(possible))
            choice = input(">").strip()
            found = None
            for opt in possible:
                opt_norm = opt.strip().lower()
                choice_norm = choice.strip().lower()
                if choice_norm == opt_norm or opt_norm in choice_norm:
                    found = opt
                    break
            if not found:
                print(
                    "I couldn't find that item. Please type the exact name from the list.")
                return
            process_item(found, order, data_menu, upsells, double_deals)

        else:
            print(
                f"What exactly do you mean by '{name}'? Please specify the item name from the menu.")
        return

    if (
            ("double" in text or "deal" in text) and not any(
                data_menu.is_burger(name) and name.lower() in text
                for name in data_menu.menu_names()
            )):

        burgers = virtual_menu.get_possible_items("burger")
        print("Choice first burger for double deals:")
        print("\n".join(burgers))
        first = input(">").strip()

        print("Choice second burger for double deals:")
        print("\n".join(burgers))
        second = input(">").strip()
        process_item(first, order, data_menu, upsells,
                     double_deals, is_double_deal=True)
        process_item(second, order, data_menu, upsells,
                     double_deals, is_double_deal=True)
        print("Double deal is applied")
        return

    items = llm.chat_with_gpt(user_input)
    virtual_words = {"burger", "drink",
                     "fries", "combo", "dessert", "ice cream"}
    concrete_items: list[dict] = []
    virtual_names_in_order: list[str] = []

    for it in items:
        if not isinstance(it, dict):
            continue
        name_llm_raw = it.get("name")
        if not name_llm_raw:
            continue

        name_llm = name_llm_raw.strip().lower()

        if name_llm.lower() in virtual_words:
            virtual_names_in_order.append(name_llm.lower())
        else:
            concrete_items.append(it)

    for vname in virtual_names_in_order:
        possible = virtual_menu.get_possible_items(vname)
        if possible:
            print(f"Which {vname} exactly would you like?")
            print("\n".join(possible))
            choice = input(">").strip()
            found = None
            for opt in possible:
                opt_norm = opt.strip().lower()
                choice_norm = choice.strip().lower()
                if choice_norm == opt_norm or opt_norm in choice_norm:
                    found = opt
                    break
            if not found:
                print(
                    "I couldn't find that item. Please type the exact name from the list.")
                continue
            process_item(found, order, data_menu, upsells, double_deals)
        else:
            print(
                f"What exactly do you mean by '{vname}'? Please specify the item name from the menu.")
            return
    if not concrete_items:
        return

    burger_indexes: list[int] = []
    for idx, it in enumerate(concrete_items):
        if not isinstance(it, dict):
            continue
        n = it.get("name")
        if n and data_menu.is_burger(n):
            burger_indexes.append(idx)
    if len(burger_indexes) >= 2:
        i1, i2 = burger_indexes[0], burger_indexes[1]
        concrete_items[i1]["double_deal"] = True
        concrete_items[i2]["double_deal"] = True
        print("We applyed 20% Double Deal discount.")
    ok, concrete_items = validate_llm_items(concrete_items, data_menu)
    if not ok:
        print(
            "I couldn't understand your order. "
            "Could you specify it again with exact items and sizes?"
        )
        return
    for item in concrete_items:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not name:
            continue
        size = item.get("size")
        fries = item.get("fries")
        drink = item.get("drink")
        is_double = bool(item.get("double_deal"))
        process_item(name, order, data_menu, upsells,
                     double_deals, size,  fries, drink, is_double)


if __name__ == "__main__":
    order = orders.Order()
    data_menu = Menu("data/menu_ingredients.yaml")
    data_menu_upsell = MenuUpsell("data/menu_upsells.yaml")
    calcul = calculator.Calculator(data_menu, data_menu_upsell)
    upsells = upsell.Upseller(order, data_menu_upsell)
    double_deal = DoubleDeals("data/menu_deals.yaml")
    virtual_menu = VirtualMenu("data/menu_virtual_items.yaml")
    print("Welcome to McDonald's! What would you like to order? ")

    while True:
        user_input = input(">").strip()
        if not user_input:
            continue
        if user_input.lower() in ("no", "that's all", "nothing else", "that’s all"):
            break

        process_text(user_input, order, data_menu,
                     upsells, double_deal, virtual_menu)
        if order.user_order:
            print("What else can I get you? (or say 'no' to finish)")

    if not order.user_order:
        print("Ok, no order")
    else:
        upsells.offer_dessert()
        double_count = sum(
            1 for item in order.user_order if item.get("double_deal"))
        if double_count >= 2:
            print("Double Deal: 20 % discount applied to two burgers!")
        total = calcul.calculate_total(order.user_order)

        print(f"TOTAL: {total:.2f}")
        print("You ordered:")
        for item in order.user_order:
            print(" -", json.dumps(item))
