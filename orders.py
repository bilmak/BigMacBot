import yaml


class Order:

    def __init__(self):
        self.menu_data = self.load_menu("menu_virtual_items.yaml")
        self.menu_ingredients = self.load_menu("menu_ingredients.yaml")
        self.user_order: list[dict] = []

    def add_raw_item(self, item_name: str):
        self.user_order.append({"name": item_name})

    def add_meal(self, meal_name: str, fries: str, drink: str):
        self.user_order.append({
            "name": meal_name,
            "fries": fries,
            "drink": drink,
        })

    def add_burger_ingredients(self, name, additionals, quantity):
        self.user_order.append({
            "name": name,
            "additionals": additionals,
            "quantity": quantity,
        })

    def update_order(self, old_name, new_name):
        for item in self.user_order:
            if item.get("name") == old_name:
                item["name"] = new_name
                print(f"You updated {old_name} to {new_name}\n")
                return
        print(f"Item '{old_name}' not found in your order")

    def delete_item(self, item_name):
        for i, item in enumerate(self.user_order):
            if item["name"] == item_name:
                self.user_order.pop(i)
                print(f"You removed {item_name}\n")
                return
        print(f"Item '{item_name}' not found in your order")

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
        ingredients = self.menu_ingredients.get("ingredients", [])

        new_structures_combos_by_name = {}
        for combo in combos:
            key = combo["name"]
            new_structures_combos_by_name[key] = combo

        new_structures_items_by_name = {}
        for item in items:
            key = item["name"]
            new_structures_items_by_name[key] = item

        new_structures_ingredients_by_name = {}
        for ing in ingredients:
            key = ing["name"]
            new_structures_ingredients_by_name[key] = ing

        for order_item in self.user_order:
            name = order_item.get("name")
            quantity = order_item.get("quantity", 1)

            if name in new_structures_combos_by_name:
                combo = new_structures_combos_by_name[name]
                price = float(combo["price"])
                total += price * quantity
                continue
            if name in new_structures_items_by_name:
                item = new_structures_items_by_name[name]
                price = float(item["price"])
                total += price * quantity
            if "additionals" in order_item:
                additionals = order_item["additionals"]
                if isinstance(additionals, dict):
                    additionals = [additionals]
                for add in additionals:
                    add_name = add.get("name")
                    add_number = add.get("number", 1)
                    ing = new_structures_ingredients_by_name.get(add_name)
                    if ing is None:
                        continue

                    ing_price = float(ing["price"])
                    total += ing_price * add_number * quantity
        return total
