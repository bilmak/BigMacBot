from .menu import Menu, MenuUpsell


class Calculator:
    def __init__(self, menu: Menu, menuUpsell: MenuUpsell):
        self.menu = menu
        self.menuUpsell = menuUpsell

    def calculate_total(self, user_order: list[dict]) -> float:
        total = 0.0

        combos = self.menu.data.get("combos", [])
        items = self.menu.data.get("items", [])
        ingredients = self.menu.data.get("ingredients", [])

        new_structures_combos_by_name = {}
        for combo in combos:
            key = combo.get("name", "").strip().lower()
            new_structures_combos_by_name[key] = combo

        new_structures_items_by_name = {}
        for item in items:
            key = item.get("name", "").strip().lower()
            new_structures_items_by_name[key] = item

        new_structures_ingredients_by_name = {}
        for ing in ingredients:
            key = ing.get("name", "").strip().lower()
            new_structures_ingredients_by_name[key] = ing

        size_changer = {
            "small": 0.7,
            "medium": 1.0,
            "large": 1.25,
        }
        double_deal_burgers = []

        sauces = self.menuUpsell.data.get("items", [])
        sauces_by_name = {}
        for s in sauces:
            if s.get("category") == "sauces":
                name_key = s.get("name", "").strip().lower()
                sauces_by_name[name_key] = s

        for order_item in user_order:
            name = order_item.get("name")
            if not name:
                continue

            key = name.strip().lower()
            quantity = order_item.get("quantity", 1)

            # sauces
            if key in sauces_by_name:
                sauce = sauces_by_name[key]
                sauce_price = float(sauce.get("price", 0.0))
                total += sauce_price * quantity
                continue

            # ingredients
            if key in new_structures_ingredients_by_name:
                ing = new_structures_ingredients_by_name[key]
                ing_price = float(ing.get("price", 0.0))
                total += ing_price*quantity
                continue
            # combos
            if key in new_structures_combos_by_name:
                combo = new_structures_combos_by_name[key]
                price = float(combo.get("price", 0.0))
                total += price*quantity
                continue
            # items
            if key in new_structures_items_by_name:
                item = new_structures_items_by_name[key]
                price = float(item.get("price", 0.0))

                size = order_item.get("size", "").lower()
                price *= size_changer.get(size, 1.0)
                line_total = price*quantity

                if item.get("category") == "burgers" and order_item.get("double_deal"):
                    double_deal_burgers.append(line_total)
                total += line_total

                if item.get("category") == "burgers":

                    additionals = order_item.get("additionals") or []
                    if isinstance(additionals, dict):
                        additionals = [additionals]
                    for add in additionals:
                        add_name = add.get("name")
                        if not add_name:
                            continue

                        add_key = add_name.strip().lower()
                        ing = new_structures_ingredients_by_name.get(add_key)
                        if not ing:
                            continue
                        ing_price = float(ing.get("price", 0.0))
                        count = add.get("number", 1)
                        total += ing_price*count * quantity
        if len(double_deal_burgers) >= 2:
            discount = double_deal_burgers[0]+double_deal_burgers[1]
            base = discount*0.2
            total -= base
        return total
