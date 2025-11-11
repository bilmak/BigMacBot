import yaml


class Order:
    user_order: list = []

    def __init__(self):
        self.menu_data = self.load_menu("menu_deals.yaml")

    def add_item(self, item_name):
        self.user_order.append(item_name)

    def update_order(self):
        pass

    def delete_item(self, item_name):
        self.user_order.remove(item_name)

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

        return total
