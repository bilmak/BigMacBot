import yaml


class Menu:
    def __init__(self, file_path):
        self.data = self.load_menu(file_path)

    def load_menu(self, file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data

    def menu_names(self):
        names = []

        combos = self.data.get("combos", [])
        for combo in combos:
            names.append(combo.get("name", ""))

        items = self.data.get("items", [])
        for item in items:
            names.append(item.get("name", ""))
        return names

    def is_item_in_menu(self, item_name: str) -> bool:
        item_name = item_name.lower().strip()
        for name in self.menu_names():
            if item_name == name.strip().lower():
                return True
        return False

    def get_combo_slot_fries(self, name_meal: str) -> list:
        meal_name = name_meal.strip().lower()
        combos = self.data.get("combos", [])

        for combo in combos:
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == meal_name:
                slot = combo.get("slots", {})
                return slot.get("fries", [])

        return []

    def get_combo_slot_drinks(self, name_meal: str) -> list:
        meal_name = name_meal.strip().lower()
        combos = self.data.get("combos", [])

        for combo in combos:
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == meal_name:
                slot = combo.get("slots", {})
                return slot.get("drinks", [])

        return []

    def get_item_sizes(self, item_name: str) -> list:
        name_lower = item_name.strip().lower()
        items = self.data.get("items", [])

        for item in items:
            item_name_in_menu = item.get("name", "").strip().lower()
            if item_name_in_menu == name_lower:
                for proper in item.get("properties", []):
                    if proper.get("name") == "size":
                        return proper.get("values", [])
                break

        return []

    def is_burger(self, name: str) -> bool:
        name_lower = name.strip().lower()
        for item in self.data.get("items", []):
            if item.get("name", "").strip().lower() == name_lower and item.get("category") == "burgers":
                return True
        return False

    def get_burger_options(self, name: str):
        name_lower = name.strip().lower()

        for item in self.data.get("items", []):
            item_name = item.get("name", "").strip().lower()
            if item_name == name_lower and item.get("category") == "burgers":
                return item
        return None

    def get_item_price(self, name: str) -> float:
        name_lower = name.strip().lower()
        combos = self.data.get("combos", [])
        for combo in combos:
            combo_name = combo.get("name", "").strip().lower()
            if combo_name == name_lower:
                return float(combo.get("price", 0.0))

        items = self.data.get("items", [])
        for item in items:
            item_name = item.get("name", "").strip().lower()
            if item_name == name_lower:
                return float(item.get("price", 0.0))
        return 0.0

    def get_ingredient_price(self, ing_name: str) -> float:
        name_lower = ing_name.strip().lower()
        ingredients = self.data.get("ingredients", [])

        for ing in ingredients:
            name = ing.get("name", "").strip().lower()
            if name == name_lower:
                return float(ing.get("price", 0.0))
        return 0.0


class MenuUpsell:
    def __init__(self, file_path: str) -> None:
        self.data = self.load_menu(file_path)

    def load_menu(self, file_path: str) -> list:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data

    def get_desserts_options(self) -> list:
        desserts = []
        for item in self.data.get("items", []):
            if item.get("category") == "desserts":
                desserts.append(item.get("name"))
        return desserts

    def is_burger(self, name: str) -> bool:
        name_lower = name.strip().lower()
        for item in self.data.get("items", []):
            if item.get("name", "").strip().lower() == name_lower and item.get("category") == "burgers":
                return True
        return False
