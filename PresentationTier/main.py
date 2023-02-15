from BussinesTier.product import Product
from BussinesTier.sales import Sale

# import os


def show_products() -> None:
    Product('', '', '', 0, 0, 0, '').show_products()


def show_records(item: str) -> None:
    if item != 'all':
        Sale('', 0, 0, 0, '', False).show_record(item)
    else:
        table_names = Sale('', 0, 0, 0, '', False).return_table_names()
        for name in table_names:
            print(name[1])
            Sale('', 0, 0, 0, '', False).show_record(name[1])


def show_barcodes() -> None:
    Product('', '', '', 0, 0, 0, '').show_barcodes()


def buy_products() -> None:
    show_products()
    ide = int(input('Choose the id of the product to buy or 0 to cancel: '))
    if ide != 0:
        product = Product('', '', '', 0, 0, 0, '')
        quantity_purchased = int(input('Type the quantity to buy: '))
        product.edit_product_stock(ide, quantity_purchased)
        # Return the name
        product_name = product.return_value_from_database(ide, 'name')
        # Return the sale value
        sale_value = product.return_value_from_database(ide, 'sale_vale')
        # Return the IVA
        IVA = product.return_value_from_database(ide, 'IVA')
        # Create the sale
        sale = Sale(amount_sold=quantity_purchased,
                    subtotal=quantity_purchased * sale_value,
                    total=(quantity_purchased * sale_value if IVA == 'y' else quantity_purchased * sale_value * 1.16),
                    type_of_payment='cash',
                    was_the_order_billed=False,
                    product_name=product_name)
        sale.create_record()


def main():
    while True:
        print('''
        1. Show products
        2. Add product
        3. Buy products
        4. Show records
        5. Show all records
        6. Update a product
        ''')
        option = int(input('Choose an option: '))
        # os.system('cls' if os.name == 'nt' else 'clear')
        if option == 1:
            show_products()
        elif option == 2:
            product = Product('', '', '', 0, 0, 0, '')
            product.create_product()
            product.add_product_to_database()
        elif option == 3:
            buy_products()
        elif option == 4:
            names = Sale('', 0, 0, 0, '', False).print_tables_names()
            if len(names) != 0:
                show_records(names[int(input('Choose an option: ')) - 1])
            else:
                print('There are no records')
        elif option == 5:
            show_records('all')
        elif option == 6:
            show_products()
            ide = int(input('Type the ID of the product you want to update: '))
            Product('', '', '', 0, 0, 0, '').update_product(ide)
            show_products()
        elif option == 0:
            exit()


if __name__ == '__main__':
    main()
