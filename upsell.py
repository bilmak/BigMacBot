import orders


class Upseller:
    def __init__(self, order):
        self.order: orders.Order = order

    def find_products_to_upsell(self) -> list:
        main_order = self.order.user_order
        for ord in main_order:
            if ord in ("meal"):
                return True
        return False
