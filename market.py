# lista de ordens; o id é o indice da lista
class order:
    def __init__(self, order_type, price, quantity):
        self.type = order_type  # 'buy' ou 'sell'
        self.price = price
        self.quantity = quantity
        self.id = None

# livro de ordens
class book:
    orders = 0 # id da próxima ordem
    def __init__(self):
        # 
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        order.id = self.orders
        self.orders += 1
        if order.type == 'buy':
            position =  len(self.buy_orders)
            while position > 0 and self.buy_orders[position - 1].price < order.price and order.id > self.buy_orders[position - 1].id:
                position -= 1
            self.buy_orders.insert(position, order)
        elif order.type == 'sell':
            position = len(self.sell_orders)
            while position > 0 and self.sell_orders[position - 1].price > order.price and order.id > self.sell_orders[position - 1].id:
                position -= 1
            self.sell_orders.insert(position, order)

    def match_orders(self):
        # Implementação de correspondência de ordens
        pass

    def print_book(self):
        print("Ordens de Compra        | Ordens de Venda")
        for i in range(max(len(self.buy_orders), len(self.sell_orders))):
            buy_order = self.buy_orders[i] if i < len(self.buy_orders) else None
            sell_order = self.sell_orders[i] if i < len(self.sell_orders) else None
            buy_str = f"{buy_order.quantity} @ {buy_order.price}, ID: {buy_order.id}" if buy_order else "        "
            sell_str = f"{sell_order.quantity} @ {sell_order.price}, ID: {sell_order.id}" if sell_order else ""
            print(f"{buy_str:<30} | {sell_str}")


book_instance = book()
book_instance.add_order(order('buy', 100, 10))
book_instance.add_order(order('buy', 105, 5))
book_instance.add_order(order('sell', 110, 8))
book_instance.add_order(order('sell', 110, 8))
book_instance.print_book()