# lista de ordens; o id é o indice da lista
class order:
    def __init__(self, order_type, price, quantity):
        self.type = order_type  # 'buy' ou 'sell'
        self.price = float(price)
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

    def match_orders(self, quantity=None, price=None, type=None):
        # Confere o topo do livro de ordens para ver se há correspondência entre ordens de compra e venda
        # Se há quantity, atua como match, caso contrário, atua como limit
        if quantity is not None and price is not None:
            # Se uma ordem de correspondência foi fornecida, 
            # tentamos corresponder a quantidade e preço especificados
            # Se for uma ordem de compra, tentamos corresponder com as ordens de venda
            if type == 'buy':
                for sell_order in self.sell_orders:
                    if sell_order.price <= price:
                        matched_quantity = min(quantity, sell_order.quantity)
                        print(f"Correspondência encontrada: {matched_quantity} @ {sell_order.price}, ID: {sell_order.id}")
                        sell_order.quantity -= matched_quantity
                        quantity -= matched_quantity
                        if sell_order.quantity == 0:
                            self.sell_orders.remove(sell_order)
                        if quantity == 0:
                            break
            elif type == 'sell':
                for buy_order in self.buy_orders:
                    if buy_order.price >= price:
                        matched_quantity = min(quantity, buy_order.quantity)
                        print(f"Correspondência encontrada: {matched_quantity} @ {buy_order.price}, ID: {buy_order.id}")
                        buy_order.quantity -= matched_quantity
                        quantity -= matched_quantity
                        if buy_order.quantity == 0:
                            self.buy_orders.remove(buy_order)
                        if quantity == 0:
                            break
        else:
            # Se não houver uma ordem de correspondência, tentamos corresponder as ordens no topo do livro
            while self.buy_orders and self.sell_orders and self.buy_orders[0].price >= self.sell_orders[0].price:
                buy_order = self.buy_orders[0]
                sell_order = self.sell_orders[0]
                matched_quantity = min(buy_order.quantity, sell_order.quantity)
                # Preço definido pelo preço mais antigo, pelo id
                if buy_order.id < sell_order.id:
                    print(f"Correspondência encontrada: {matched_quantity} @ {buy_order.price}, ID: {buy_order.id}")
                else:
                    print(f"Correspondência encontrada: {matched_quantity} @ {sell_order.price}, ID: {sell_order.id}")
                buy_order.quantity -= matched_quantity
                sell_order.quantity -= matched_quantity
                if buy_order.quantity == 0:
                    self.buy_orders.pop(0)
                if sell_order.quantity == 0:
                    self.sell_orders.pop(0)

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
            for order in order_list:
                if order.id == int(order_id):
                    order_list.remove(order)
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
        if user_input.lower() == 'print':
            book_instance.print_book()
            continue
        parts = user_input.split()
        if len(parts) != 4:
            print("Formato inválido. Use: <tipo> <ação> <quantidade> <preço>")
            continue
        action, order_type, quantity, price = parts
        quantity = int(quantity)
        price = float(price)
        if action == 'limit':
            book_instance.add_order(order(order_type, price, quantity))
        elif action == 'match':
            book_instance.match_orders(quantity, price, order_type)
        else:
            print("Ação inválida. Use 'limit' ou 'match'.")

input_market()