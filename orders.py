
from menu import Menu
from menu import MenuUpsell


class Order:
    def __init__(self) -> None:
        self.menu = Menu("menu_ingredients.yaml")
        # self.menu_upsell = MenuUpsell("menu_upsells.yaml")
        self.user_order: list[dict] = []

    def add_raw_item(self, item_name: str, size: str | None = None) -> None:
        item = {"name": item_name}
        if size:
            item["size"] = size
        self.user_order.append(item)

    def add_meal(self, meal_name: str, fries: str, drink: str) -> list:
        self.user_order.append({
            "name": meal_name,
            "fries": fries,
            "drink": drink,
        })

    def add_burger_ingredients(self, name, additionals, quantity) -> list:
        self.user_order.append({
            "name": name,
            "additionals": additionals,
            "quantity": quantity,
        })

    def add_burger(self, name, additionals, removed) -> list:
        self.user_order.append({
            "name": name,
            "additionals": additionals,
            "removed": removed
        })

    def update_order(self, old_name, new_name) -> None:
        for item in self.user_order:
            if item.get("name") == old_name:
                item["name"] = new_name
                print(f"You updated {old_name} to {new_name}\n")
                return
        print(f"Item '{old_name}' not found in your order")

    def delete_item(self, item_name) -> None:
        for i, item in enumerate(self.user_order):
            if item["name"] == item_name:
                self.user_order.pop(i)
                print(f"You removed {item_name}\n")
                return
        print(f"Item '{item_name}' not found in your order")
