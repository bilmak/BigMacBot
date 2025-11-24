import yaml


class Order:

    def __init__(self)->None:
        # self.menu_data = self.load_menu("menu_virtual_items.yaml")
        self.menu_ingredients = self.load_menu("menu_ingredients.yaml")
        self.user_order: list[dict] = []

    def add_raw_item(self, item_name: str, size: str)->None:
        item = {"name": item_name}
        if size:
            item["size"] = size
        self.user_order.append(item)

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

    def add_burger(self, name, additionals, removed):
        self.user_order.append({
            "name": name,
            "additionals": additionals,
            "removed": removed
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
        for combo in self.menu_ingredients["combos"]:
            names.append(combo["name"])

        for item in self.menu_ingredients["items"]:
            names.append(item["name"])
        return names

    def is_item_in_menu(self, item: str) -> bool:
        return item.lower() in (name.lower() for name in self.menu_names())

    def get_combo_slot_fries(self, name_meal: str) -> list:
        meal_name = name_meal.strip().lower()

        for combo in self.menu_ingredients.get("combos", []):
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == meal_name:
                slot = combo.get("slots", {})
                return slot.get("fries", [])

        return []

    def get_combo_slot_drinks(self, name_meal: str) -> list:
        meal_name = name_meal.strip().lower()

        for combo in self.menu_ingredients.get("combos", []):
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == meal_name:
                slot = combo.get("slots", {})
                return slot.get("drinks", [])

        return []

    def get_item_sizes(self, item_name: str) -> list:
        name_lower = item_name.strip().lower()

        for item in self.menu_ingredients.get("items", []):
            item_name_in_menu = item.get("name", "").strip().lower()
            if item_name_in_menu == name_lower:
                for proper in item.get("properties", []):
                    if proper.get("name") == "size":
                        return proper.get("values", [])
                break

        return []

    def get_burger_options(self, burger_name: str):
        name_lower = burger_name.strip().lower()

        for item in self.menu_ingredients.get("items", []):
            item_name = item.get("name", "").strip().lower()
            if item_name == name_lower and item.get("category") == "burgers":
                return item
        return None

    def is_burger(self, name: str) -> bool:
        name_lower = name.strip().lower()
        for item in self.menu_ingredients.get("items", []):
            if item.get("name", "").strip().lower() == name_lower and item.get("category") == "burgers":
                return True
        return False

    def calculate_total(self) -> float:
        total = 0.0

        combos = self.menu_ingredients.get("combos", [])
        items = self.menu_ingredients.get("items", [])
        ingredients = self.menu_ingredients.get("ingredients", [])

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

        for order_item in self.user_order:
            name = order_item.get("name")
            if not name:
                continue

            key = name.strip().lower()
            quantity = order_item.get("quantity", 1)

            if key in new_structures_combos_by_name:
                combo = new_structures_combos_by_name[key]
                price = float(combo.get("price", 0.0))
                total += price * quantity

            elif key in new_structures_items_by_name:
                item = new_structures_items_by_name[key]
                price = float(item.get("price", 0.0))
                total += price * quantity

            additionals = order_item.get("additionals")or  []
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
        return total
