import yaml


class DoubleDeals:
    def __init__(self, file_path):
        self.data = self.load_menu(file_path)

    def load_menu(self, file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data

    def get_deal_for_burger(self, burger_name) -> dict | None:
        burger_name = burger_name.strip().lower()
        for deal in self.data.get("deals", []):
            for item in deal.get("possible_items", []):
                if item.strip().lower == burger_name:
                    return deal
        return None
