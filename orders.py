import yaml


class Order:

    def __init__(self):
        self.menu_data = self.load_menu("menu_virtual_items.yaml")
        self.user_order: list = []

    def add_item(self, item_name: str):
        self.user_order.append(item_name)

    def update_order(self, old_name, new_name):
        if old_name in self.user_order:
            index = self.user_order.index(old_name)
            self.user_order[index] = new_name
            print(f"You updated {old_name} on {new_name}\n")
        else:
            print(f"Item '{old_name}' not found in your order")

    def delete_item(self, item_name):
        if item_name not in self.user_order:
            print(f"Item '{item_name}' not found in your order")
            return
        self.user_order.remove(item_name)
        print(f"You removed {item_name}\n")

    def load_menu(self, file_path):
        with open(file_path, 'r') as deals_file:
            data = yaml.safe_load(deals_file)
            return data

    def menu_names(self):
        names = []
        for combo in self.menu_data["combos"]:
            names.append(combo["name"])

        for item in self.menu_data["items"]:
            names.append(item["name"])
        return names

    def is_item_in_menu(self, item: str) -> bool:
        return item.lower() in (name.lower() for name in self.menu_names())

    def get_combo_slot_fries(self, name_meal: str) -> list:
        meal_name = name_meal.strip().lower()

        for combo in self.menu_data.get("combos", []):
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == meal_name:
                slot = combo.get("slots", {})
                return slot.get("fries", [])

        return []

    def get_combo_slot_drinks(self, name_meal: str) -> list:
        meal_name = name_meal.strip().lower()

        for combo in self.menu_data.get("combos", []):
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == meal_name:
                slot = combo.get("slots", {})
                return slot.get("drinks", [])

        return []

    def calculate_total(self):
        total = 0.0

        combos = self.menu_data.get("combos", [])
        items = self.menu_data.get("items", [])

        combos_name = {}
        for combo in combos:
            key = combo["name"]
            combos_name[key] = combo

        meals_count = 0
        for name in self.user_order:
            if name in combos_name:
                meals_count += 1

        fries_count = {}
        drinks_count = {}

        for name in self.user_order:
            for item in items:
                if item["name"] == name:
                    category = item.get("category")

                    if category == "fries":
                        if name not in fries_count:
                            fries_count[name] = 1
                        else:
                            fries_count[name] += 1

                    if category == "drinks":
                        if name not in drinks_count:
                            drinks_count[name] = 1
                        else:
                            drinks_count[name] += 1

        for name in self.user_order:
            if name in combos_name:
                price = float(combos_name[name]["price"])
                total += price
                continue

            price = None
            category = None
            for item in items:
                if item["name"] == name:
                    price = float(item["price"])
                    category = item.get("category")
                    break

            if price is None:
                continue

            if category == "fries":
                if meals_count > 0 and fries_count.get(name, 0) > 0:
                    fries_count[name] -= 1
                    meals_count -= 1
                    continue
                else:
                    total += price
                    continue

            if category == "drinks":
                if meals_count > 0 and drinks_count.get(name, 0) > 0:
                    drinks_count[name] -= 1
                    meals_count -= 1
                    continue
                else:
                    total += price
                    continue

            total += price

        return total
