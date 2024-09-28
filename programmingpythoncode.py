class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def update_quantity(self, amount):
        self.quantity += amount
        if self.quantity < 0:
            self.quantity = 0

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity


class InventorySystem:
    def __init__(self):
        self.products = {}

    def add_product(self, name, quantity):
        if name in self.products:
            existing_product = self.products[name]
            existing_product.update_quantity(quantity)
            print(f"{name} mahsulotining miqdori yangilandi: {existing_product.get_quantity()}.")
        else:
            self.products[name] = Product(name, quantity)
            print(f"{name} mahsuloti qo'shildi.")

    def update_product(self, name, amount):
        if name in self.products:
            product = self.products[name]
            if amount < 0 and abs(amount) > product.get_quantity():
                print(f"Xato: {name} mahsulotidan ayirilayotgan miqdor bazadagi miqdordan ko'p. Mavjud miqdor: {product.get_quantity()}.")
            else:
                product.update_quantity(amount)
                print(f"Yangilangan miqdor: {product.get_quantity()} ta {name}.")
                if product.get_quantity() == 0:
                    print(f"{name} mahsuloti endi qolmagan mahsulotlar ro'yxatida.")
        else:
            print(f"{name} mahsuloti topilmadi.")

    def display_quantity(self, name):
        if name in self.products:
            print(f"{name} mahsulotidan qolgan miqdor: {self.products[name].get_quantity()}")
        else:
            print(f"{name} mahsuloti topilmadi.")

    def display_out_of_stock_products(self):
        print("Qolmagan mahsulotlar ro'yxati:")
        has_out_of_stock = False
        for product in self.products.values():
            if product.get_quantity() == 0:
                print(product.get_name())
                has_out_of_stock = True
        if not has_out_of_stock:
            print("Hozirgi vaqtda qolmagan mahsulotlar yo'q.")


def main():
    system = InventorySystem()

    while True:
        print("\nAmalni tanlang:")
        print("1 - Mahsulot qo'shish")
        print("2 - Mahsulotni yangilash (miqdorni oshirish yoki kamaytirish)")
        print("3 - Mahsulot miqdorini ko'rsatish")
        print("4 - Qolmagan mahsulotlar ro'yxatini ko'rsatish")
        print("0 - Chiqish")

        try:
            action = int(input("Amal raqamini kiriting: "))
        except ValueError:
            print("Noto'g'ri amal tanlandi.")
            continue

        if action == 1:
            add_input = input("Mahsulot nomi va miqdorini kiriting (misol: Olma 100): ")
            parts = add_input.split(' ')
            if len(parts) != 2 or not parts[1].isdigit():
                print("Noto'g'ri format. Misol: Olma 100")
                continue
            name = parts[0]
            quantity = int(parts[1])
            system.add_product(name, quantity)

        elif action == 2:
            update_input = input("Mahsulot nomi, miqdorini kiriting (misol: Olma 50 yoki Olma -50): ")
            parts = update_input.split(' ')
            if len(parts) != 2 or not parts[1].lstrip('-').isdigit():
                print("Noto'g'ri format. Misol: Olma 50 yoki Olma -50")
                continue
            name = parts[0]
            amount = int(parts[1])
            system.update_product(name, amount)

        elif action == 3:
            name = input("Mahsulot nomini kiriting: ")
            system.display_quantity(name)

        elif action == 4:
            system.display_out_of_stock_products()

        elif action == 0:
            print("Dasturdan chiqish...")
            break

        else:
            print("Noto'g'ri amal tanlandi.")


if __name__ == "__main__":
    main()
