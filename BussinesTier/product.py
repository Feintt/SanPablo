from dataclasses import dataclass
from DataTier.database import DataBase
from table2ascii import table2ascii
from barcode import Code39
from barcode.writer import ImageWriter
from BarcodesManagment.barcodes import BarcodeManager


@dataclass()
class Product:
    name: str
    presentation: str
    laboratory: str
    stock: int
    cost_value: float
    sale_vale: float
    expiration_date: str
    IVA = bool
    DataBase = DataBase('SanPablo.db')
    DataBase.create_table_if_not_exists('products',
                                        'SKU TEXT NULL, name TEXT NULL, presentation TEXT NULL, laboratory TEXT NULL, '
                                        'stock INT NULL, cost_value REAL NULL, sale_vale REAL NULL, '
                                        'expiration_date TEXT NULL, IVA BOOL NULL')
    barcode = BarcodeManager()

    def show_products(self):
        products = self.DataBase.cursor.execute('SELECT * FROM products').fetchall()
        output = table2ascii(
            header=['#', 'SKU', 'Name', 'Presentation', 'Laboratory', 'Stock', 'Cost', 'Sale', 'Expiration', 'IVA'],
            body=products,
        )
        print(output)

    def add_product_to_database(self):
        self.DataBase.try_to_add_to_table('products', 'SKU, name, presentation, laboratory, stock, cost_value, '
                                                      'sale_vale, '
                                                      'expiration_date, IVA',
                                          f'"SKU-{self.name[:3]}-{int(self.cost_value)}{self.presentation}", '
                                          f'"{self.name}", "{self.presentation}", '
                                          f'"{self.laboratory}", {self.stock}, {self.cost_value}, '
                                          f'{self.sale_vale}, "{self.expiration_date}", {self.IVA}')
        with open(f'../Barcodes/{self.name}_barcode.png', 'wb') as f:
            Code39(f'{self.name}', writer=ImageWriter()).write(f)
        self.barcode.add_barcode_to_database(barcode=f'{self.name}', product_id=self.DataBase.cursor.lastrowid)

    def edit_product_stock(self, ide: int, quantity_purchased: int):
        current_stock = self.DataBase.cursor.execute(f'SELECT stock FROM products WHERE ID = {ide}').fetchone()[0]
        if current_stock >= quantity_purchased:
            self.DataBase.update_stock_from_table(table_name='products', column='stock',
                                                  value=quantity_purchased, ide=ide)
            return quantity_purchased
        else:
            print('There is not enough stock')

    def return_value_from_database(self, ide: int, column: str):
        return self.DataBase.cursor.execute(f'SELECT {column} FROM products WHERE ID = {ide}').fetchone()[0]

    def create_product(self):
        self.name = input('Type the Name: ')
        self.presentation = input('Type the Presentation: ')
        self.laboratory = input('Type the Laboratory: ')
        self.stock = int(input('Type the Stock: '))
        self.cost_value = float(input('Type the Cost Value: '))
        self.sale_vale = float(input('Type the Sale Value: '))
        self.expiration_date = input('Type the Expiration Date: ')
        self.IVA = bool(input('Type the status of IVA True/False: '))

    def update_product(self, ide: int):
        column_names = self.print_columns()
        column_name = int(input('Type the column name you want to edit: '))
        column = str(column_names[column_name - 1][1])
        if column_names[column_name - 1][2] == 'INT':
            value = int(input('Type the new value: '))
            if column == 'name':
                self.DataBase.change_table_name(f'{self.return_value_from_database(ide=ide, column=column)}', f'{value}')
            self.DataBase.update_table_for_strings(table_name='products', column=column, value=value, ide=ide)
        elif column_names[column_name - 1][2] == 'REAL':
            value = float(input('Type the new value: '))
            self.DataBase.update_table_for_strings(table_name='products', column=column, value=value, ide=ide)
        elif column_names[column_name - 1][2] == 'TEXT':
            value = input('Type the new value: ')
            self.DataBase.update_table_for_strings(table_name='products', column=column, value=value, ide=ide)
        elif column_names[column_name - 1][2] == 'BOOL':
            value = bool(input('Type the new value True/False: '))
            self.DataBase.update_table_for_any_other(table_name='products', column=column, value=value, ide=ide)

    def print_columns(self):
        table_info = self.DataBase.list_columns_of_a_table('products')
        columns_names = []
        for index, column in enumerate(table_info):
            if index > 0:
                columns_names.append([index, column[1], column[2]])
        output = table2ascii(
            header=['#', 'Column Name'],
            body=[column[:2] for column in columns_names],
        )
        print(output)
        return columns_names

    def show_barcodes(self):
        barcodes = self.barcode.return_barcodes_from_table()
        print(barcodes)
