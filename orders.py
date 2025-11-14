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
        self.user_order.remove(item_name)
        print(f"You removed {item_name}\n")

    def load_menu(self, file_path):
        with open(file_path, 'r') as deals_file:
            data = yaml.safe_load(deals_file)
            return data

    def calculate_total(self):
        total = 0.00
        for order_name in self.user_order:
            for item in self.menu_data["combos"]:
                if order_name == item["name"]:
                    total += item["price"]

            for item in self.menu_data["items"]:
                if order_name == item["name"]:
                    total += item["price"]

        return total

    def menu_names(self):
        names = []
        for combo in self.menu_data["combos"]:
            names.append(combo["name"])

        for item in self.menu_data["items"]:
            names.append(item["name"])
        return names

    def is_item_in_menu(self, item: str) -> bool:
        return item.lower() in (name.lower() for name in self.menu_names())
