from BussinesTier.product import Product
from BussinesTier.sales import Sale
from BussinesTier.payment import Payment

# import os


def display_barcode_image() -> None:
    Product('', '', '', 0, 0, 0, '').print_product_names()
    ide = int(input('Choose the id of the product to display the barcode or 0 to cancel: '))
    if ide != 0:
        Product('', '', '', 0, 0, 0, '').display_barcode(ide)


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
        product_name = product.DataBase.return_single_value_from_table('products', 'name', ide)
        # Return the sale value
        sale_value = product.DataBase.return_single_value_from_table('products', 'sale_vale', ide)
        # Return the IVA
        IVA = product.DataBase.return_single_value_from_table('products', 'IVA', ide)
        print(IVA)
        # Create the sale
        sale = Sale(amount_sold=quantity_purchased,
                    subtotal=quantity_purchased * sale_value,
                    total=(quantity_purchased * sale_value if IVA == 0 else quantity_purchased * sale_value * 1.16),
                    type_of_payment='cash',
                    was_the_order_billed=False,
                    product_name=product_name)
        sale.create_record()


def main():
    # This is the main menu
    while True:
        print('''
        1. Show products
        2. Add product
        3. Buy products
        4. Show records
        5. Show all records
        6. Update a product
        7. Show/Display barcodes
        8. Show products by filter
        9. Show products info by filtering values
        ''')
        option = int(input('Choose an option: '))
        # os.system('cls' if os.name == 'nt' else 'clear')
        if option == 1:
            """
            This option shows the products by creating a Product object with trash values, then 
            calling the show_products function from the Product class.
            """
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
        elif option == 7:
            display_barcode_image()
        elif option == 8:
            Product('', '', '', 0, 0, 0, '').print_product_by_column()
        elif option == 9:
            Product('', '', '', 0, 0, 0, '').print_product_info_by_typing_the_column()
        elif option == 10:
            Payment(input('Type your credit/debit card: '))
        elif option == 0:
            exit()


if __name__ == '__main__':
    main()
