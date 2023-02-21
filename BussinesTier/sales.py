from dataclasses import dataclass
from datetime import datetime
from DataTier.database import DataBase
from table2ascii import table2ascii


# This class will be used to create a table in the database to store all the records of the sales
@dataclass()
class Sale:
    DataBase = DataBase('Records.db')
    product_name: str
    date = datetime.now().strftime('%d/%m/%Y')
    time = datetime.now().strftime('%H:%M:%S')
    amount_sold: int
    subtotal: float
    total: float
    type_of_payment: str
    was_the_order_billed: bool

    def create_record(self):
        self.DataBase.create_table_if_not_exists(table_name=f'{self.product_name}',
                                                 columns='product_sold TEXT NULL, order_number TEXT NULL, '
                                                         'date TEXT NULL, time TEXT NULL, '
                                                         'amount_sold INT NULL, subtotal REAL NULL, total REAL NULL, '
                                                         'type_of_payment TEXT NULL, was_the_order_billed BOOL NULL')
        self.DataBase.try_to_add_to_table(table_name=f'{self.product_name}',
                                          columns='product_sold, order_number, date, time, '
                                                  'amount_sold, subtotal, total, '
                                                  'type_of_payment, '
                                                  'was_the_order_billed',
                                          values=f'"{self.product_name}",'
                                                 f'"{self.product_name[:2]}{self.create_order_number()}", '
                                                 f'"{self.date}", '
                                                 f'"{self.time}", '
                                                 f'{self.amount_sold}, {self.subtotal}, '
                                                 f'{self.total}, '
                                                 f'"{self.type_of_payment}", '
                                                 f'{self.was_the_order_billed}')

    def show_record(self, product_name):
        records = self.DataBase.cursor.execute(f'SELECT * FROM {product_name}').fetchall()
        output = table2ascii(
            header=['#', 'Product Sold', 'Order Number', 'Date', 'Time', 'Amount Sold', 'Subtotal', 'Total', 'Type of Payment',
                    'Was the order billed?'],
            body=records,
        )
        print(output)

    def create_order_number(self):
        return self.DataBase.cursor.execute(f'SELECT COUNT(*) FROM {self.product_name}').fetchone()[0] + 1

    def print_tables_names(self):
        body = self.return_table_names()
        output = table2ascii(
            header=['#', 'Table Name'],
            body=body,
        )
        print(output)
        names = []
        for i in body:
            names.append(i[1])
        return names

    def return_table_names(self):
        tables = self.DataBase.return_table_names()
        body = []
        index = 0
        for table in tables:
            if table[0] != 'sqlite_sequence':
                index += 1
                body.append([index, table[0]])
        return body
