class Product:
    # Товар: название, цена, остаток
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        # Меняем остаток на складе (можно положительное или отрицательное)
        new_stock = self.stock + quantity
        if new_stock < 0:
            raise ValueError("Количество на складе не может быть отрицательным.")
        self.stock = new_stock


class Order:
    # Заказ: словарь {товар: количество}
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity):
        # Добавляем товар в заказ
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля.")
        if product.stock < quantity:
            raise ValueError("Недостаточно товара на складе.")
        # Склады не трогаем, только записываем в заказ
        self.products[product] = self.products.get(product, 0) + quantity

    def calculate_total(self):
        # Считаем сумму по всем позициям
        return sum(p.price * q for p, q in self.products.items())


class Store:
    # Магазин: список товаров
    def __init__(self):
        self.products = []

    def add_product(self, product):
        # Добавляем товар в магазин
        self.products.append(product)

    def list_products(self):
        # Возвращаем строку с товарами, ценами и остатком
        if not self.products:
            return "В магазине нет товаров."
        lines = []
        for idx, p in enumerate(self.products, start=1):
            lines.append(f"{idx}. {p.name} — {p.price} (на складе: {p.stock})")
        return "\n".join(lines)

    def create_order(self):
        # Создаём новый заказ
        return Order()
