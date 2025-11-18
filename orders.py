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

        free_fries = set()
        free_drinks = set()

        for order_name in self.user_order:
            combo = combos_name.get(order_name)
            if not combo:
                continue

            slots = combo.get("slots", {})
            fries_choices = set(slots.get("fries", []))
            drinks_choices = set(slots.get("drinks", []))

            for item_name in self.user_order:
                if item_name in fries_choices:
                    free_fries.add(item_name)
                if item_name in drinks_choices:
                    free_drinks.add(item_name)

        for order_name in self.user_order:
            if order_name in combos_name:
                total += combos_name[order_name]["price"]
                continue

            for item in items:
                if order_name == item["name"]:
                    if item.get("category") == "fries" and order_name in free_fries:
                        break
                    if item.get("category") == "drinks" and order_name in free_drinks:
                        break

                    total += item["price"]
                    break

        return total
