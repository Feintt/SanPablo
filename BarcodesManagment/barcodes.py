from DataTier.database import DataBase
from dataclasses import dataclass


@dataclass()
class BarcodeManager:
    DataBase = DataBase('SanPablo.db')
    DataBase.create_table_if_not_exists('barcodes', 'barcode TEXT NULL, product_id INT NULL')

    def add_barcode_to_database(self, barcode: str, product_id: int):
        self.DataBase.try_to_add_to_table('barcodes', 'barcode, product_id', f'"{barcode}", {product_id}')

    def return_product_id_from_barcode(self, barcode: str):
        return self.DataBase.cursor.execute(f'SELECT product_id FROM barcodes WHERE barcode = "{barcode}"').fetchone()[0]

    def return_barcode_from_product_id(self, product_id: int):
        return self.DataBase.cursor.execute(f'SELECT barcode FROM barcodes WHERE product_id = {product_id}').fetchone()[0]

    def return_barcode_from_product_name(self, product_name: str):
        product_id = self.DataBase.cursor.execute(f'SELECT ID FROM products WHERE name = "{product_name}"').fetchone()[0]
        return self.DataBase.cursor.execute(f'SELECT barcode FROM barcodes WHERE product_id = {product_id}').fetchone()[0]

    def return_product_name_from_barcode(self, barcode: str):
        product_id = self.DataBase.cursor.execute(f'SELECT product_id FROM barcodes WHERE barcode = "{barcode}"').fetchone()[0]
        return self.DataBase.cursor.execute(f'SELECT name FROM products WHERE ID = {product_id}').fetchone()[0]

    def return_barcodes_from_table(self):
        return self.DataBase.cursor.execute(f'SELECT barcode FROM barcodes').fetchall()