from . import handler, orders
from .menu import Menu, MenuUpsell


class Upseller:
    def __init__(self, order, m_menu: MenuUpsell):
        self.order: orders.Order = order
        self.m_menu: MenuUpsell = m_menu
        self.dessert_offered = False

    def has_burger_or_meal(self) -> bool:
        for item in self.order.user_order:
            name = item.get("name", "")
            if self.m_menu.is_burger(name):
                return True
            if "meal" in name.lower():
                return True
        return False

    def offer_dessert(self) -> None:
        if self.dessert_offered:
            return
        if not self.has_burger_or_meal():
            return
        self.dessert_offered = True

        desserts = self.m_menu.get_desserts_options()

        answer = input("Do you want to add dessert? (yes/no)\n").lower()
        if answer not in ("yes", "y", "ye"):
            return
        choice_dessert = input(
            f"What kind of dessert do you want to have?\nOptions: {','.join(desserts)}\n").strip()
        if choice_dessert not in desserts:
            print("We dont have this dessert")
        else:
            self.order.add_raw_item(choice_dessert)
            print(f"You add {choice_dessert} to your order")

    def offer_meal_upsell(self, burger_name: str) -> bool:
        combo = self.m_menu.get_combo_for_burger(burger_name)
        if combo is None:
            return False

        combo_name = combo.get("name")
        combo_price = combo.get("price")

        answer = input(
            f"Do you want upgrade your {burger_name} to {combo_name} for {combo_price:.2f}? yes/no\n").lower()
        if answer not in ("yes", "y", "ye"):
            return False

        potato = handler.handler_meal_fries(combo_name)
        drink = handler.handler_meal_drinks(combo_name)
        self.order.add_meal(combo_name, potato, drink)
        sauce = handler.handler_sauce(combo_name)
        if sauce:
            self.order.add_raw_item(sauce)
        print(f"You upgraded your burger to {combo_name}\n")
        return True
