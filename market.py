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

    # Adiciona uma ordem ao livro de ordens 
    # Ordens de compra são ordenadas por preço decrescente e ordens de venda por preço crescente. 
    # Em caso de empate, a ordem mais antiga tem prioridade.
    def add_order(self, order):
        order.id = self.orders
        self.orders += 1
        print(f"Adicionando ordem: {order.type} {order.quantity} @ {order.price}, ID: {order.id}")
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
        # Ao fim, de adicionar a ordem, chamamos a função de correspondência de ordens
        self.match_orders()

    def match_orders(self):
        # Implementação de correspondência de ordens
        pass

    def print_book(self):
        print("Ordens de Compra               | Ordens de Venda")
        for i in range(max(len(self.buy_orders), len(self.sell_orders))):
            buy_order = self.buy_orders[i] if i < len(self.buy_orders) else None
            sell_order = self.sell_orders[i] if i < len(self.sell_orders) else None
            buy_str = f"{buy_order.quantity} @ {buy_order.price}, ID: {buy_order.id}" if buy_order else ""
            sell_str = f"{sell_order.quantity} @ {sell_order.price}, ID: {sell_order.id}" if sell_order else ""
            print(f"{buy_str:<30} | {sell_str}")

    # Cancelar uma ordem pelo ID
    def cancel_order(self, order_id):
        for order_list in [self.buy_orders, self.sell_orders]:
            for i, order in enumerate(order_list):
                if order.id == order_id:
                    del order_list[i]
                    print(f"Ordem ID {order_id} cancelada.")
                    return True
        return False


book_instance = book()


book_instance.add_order(order('buy', 100, 10))
book_instance.add_order(order('buy', 105, 5))
book_instance.add_order(order('buy', 100, 8))
book_instance.add_order(order('buy', 100, 800))
book_instance.add_order(order('sell', 110, 8))
book_instance.add_order(order('sell', 110, 8))
book_instance.print_book()

# Ordens podem ser adicionadas por input no terminal, podendo ser do tipo limit ou match. 
# As ordens limit são adicionadas ao livro de ordens, enquanto as ordens match 
# são executadas imediatamente contra as ordens existentes no livro.
# exemplos:
# limit sell 20 200
# match buy 15 200
def input_market():
    while True:
        user_input = input()
        if user_input.lower() == 'help':
            print("Formato de entrada: <tipo> <ação> <quantidade> <preço>")
            print("Exemplo: limit buy 10 100")
            print("Exemplo: match sell 5 105")
            # cancel <id> para cancelar uma ordem existente
            print("Digite 'cancel <id>' para cancelar uma ordem existente.")
            print("Exemplo: cancel 2")
            print("Digite 'sair' para encerrar.")
            continue
        if user_input.lower() == 'sair':
            break
        if user_input.lower().startswith('cancel '):
            order_id = user_input[7:]
            book_instance.cancel_order(order_id)
            continue
        parts = user_input.split()
        if len(parts) != 4:
            print("Formato inválido. Use: <tipo> <ação> <quantidade> <preço>")
            continue
        order_type, action, quantity, price = parts
        quantity = int(quantity)
        price = float(price)
        if action == 'limit':
            book_instance.add_order(order(order_type, price, quantity))
        elif action == 'match':
            # Implementar lógica de correspondência imediata
            print("Ordem de correspondência não implementada ainda.")
        else:
            print("Ação inválida. Use 'limit' ou 'match'.")

input_market()