from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.metrics import dp
import mysql.connector

Window.clearcolor = (1, 1, 1, 1)  # Set background color to white


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="InventoryManagement"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS Products (product_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description TEXT, price DECIMAL(10, 2) NOT NULL, quantity INT NOT NULL)")

class InventoryManagementApp(App):
    
    def build(self):
        
        layout = BoxLayout(orientation='vertical')
        title = Label(text='Inventory Management System', size_hint=(1, 0.1), color=(0, 0, 1, 1), font_size='30sp')
        layout.add_widget(title)

        search_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.01))
        search_input = TextInput(hint_text='Search Keyword', size_hint=(0.7, None), height=60)
        search_layout.add_widget(search_input)

        search_button = Button(text='Search', size_hint=(0.3, None), height=60, background_color=(0, 0, 1, 1))
        search_button.bind(on_press=lambda x: self.search_products(search_input.text))
        search_layout.add_widget(search_button)

        layout.add_widget(search_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        add_product_button = Button(text='Add Product', size_hint=(0.25, None), height=60, background_color=(0, 0, 1, 1))
        add_product_button.bind(on_press=self.add_product_window)
        button_layout.add_widget(add_product_button)

        view_products_button = Button(text='View Products', size_hint=(0.25, None), height=60, background_color=(0, 0, 1, 1))
        view_products_button.bind(on_press=self.view_products_window)
        button_layout.add_widget(view_products_button)

        edit_product_button = Button(text='Edit Product', size_hint=(0.25, None), height=60, background_color=(0, 0, 1, 1))
        edit_product_button.bind(on_press=self.edit_product_window)
        button_layout.add_widget(edit_product_button)

        delete_product_button = Button(text='Delete Product', size_hint=(0.25, None), height=60, background_color=(0, 0, 1, 1))
        delete_product_button.bind(on_press=self.delete_product_window)
        button_layout.add_widget(delete_product_button)

        layout.add_widget(button_layout)

        return layout

    def add_product_window(self, instance):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Add New Product', size_hint=(1, 0.1))
        layout.add_widget(label)

        name_input = TextInput(hint_text='Product Name', size_hint=(1, 0.1))
        layout.add_widget(name_input)

        description_input = TextInput(hint_text='Product Description', size_hint=(1, 0.1))
        layout.add_widget(description_input)

        price_input = TextInput(hint_text='Product Price', input_type='number', size_hint=(1, 0.1))
        layout.add_widget(price_input)

        quantity_input = TextInput(hint_text='Product Quantity', input_type='number', size_hint=(1, 0.1))
        layout.add_widget(quantity_input)

        save_button = Button(text='Save', size_hint=(1, 0.1), background_color=(0, 0, 0.5, 1))  # Dark blue color
        save_button.bind(on_press=lambda x: self.add_product(name_input.text, description_input.text, float(price_input.text), int(quantity_input.text)))
        layout.add_widget(save_button)

        cancel_button = Button(text='Cancel', size_hint=(1, 0.1))
        cancel_button.bind(on_press=self.close_window)
        layout.add_widget(cancel_button)

        self.popup = Popup(title='Add Product', content=layout, size_hint=(None, None), size=(500, 500))
        self.popup.open()

    def view_products_window(self, instance):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Product List', size_hint=(1, 0.1))
        layout.add_widget(label)

        mycursor.execute("SELECT * FROM Products")
        products = mycursor.fetchall()

        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        for product in products:
            product_label = Label(text=f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Quantity: {product[4]}", size_hint=(1, None))
            scroll_layout.add_widget(product_label)

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)

        close_button = Button(text='Close', size_hint=(1, 0.1))
        close_button.bind(on_press=self.close_window)
        layout.add_widget(close_button)

        self.popup = Popup(title='View Products', content=layout, size_hint=(None, None), size=(800, 400))
        self.popup.open()




    def edit_product_window(self, instance):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Edit Product', size_hint=(1, 0.1))
        layout.add_widget(label)

        product_id_input = TextInput(hint_text='Product ID', input_type='number', size_hint=(1, 0.1))
        layout.add_widget(product_id_input)

        name_input = TextInput(hint_text='New Product Name', size_hint=(1, 0.1))
        layout.add_widget(name_input)

        description_input = TextInput(hint_text='New Product Description', size_hint=(1, 0.1))
        layout.add_widget(description_input)

        price_input = TextInput(hint_text='New Product Price', input_type='number', size_hint=(1, 0.1))
        layout.add_widget(price_input)

        quantity_input = TextInput(hint_text='New Product Quantity', input_type='number', size_hint=(1, 0.1))
        layout.add_widget(quantity_input)

        save_button = Button(text='Save', size_hint=(1, 0.1), background_color=(0, 0, 0.5, 1))  # Dark blue color
        save_button.bind(on_press=lambda x: self.edit_product(int(product_id_input.text), name_input.text, description_input.text, float(price_input.text), int(quantity_input.text)))
        layout.add_widget(save_button)

        cancel_button = Button(text='Cancel', size_hint=(1, 0.1))
        cancel_button.bind(on_press=self.close_window)
        layout.add_widget(cancel_button)

        self.popup = Popup(title='Edit Product', content=layout, size_hint=(None, None), size=(500, 500))
        self.popup.open()

    def delete_product_window(self, instance):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Delete Product', size_hint=(1, 0.1))
        layout.add_widget(label)

        product_id_input = TextInput(hint_text='Product ID', input_type='number', size_hint=(1, 0.1))
        layout.add_widget(product_id_input)

        delete_button = Button(text='Delete', size_hint=(1, 0.1), background_color=(0, 0, 0.5, 1))  # Dark blue color
        delete_button.bind(on_press=lambda x: self.delete_product(int(product_id_input.text)))
        layout.add_widget(delete_button)

        cancel_button = Button(text='Cancel', size_hint=(1, 0.1))
        cancel_button.bind(on_press=self.close_window)
        layout.add_widget(cancel_button)

        self.popup = Popup(title='Delete Product', content=layout, size_hint=(None, None), size=(500, 400))
        self.popup.open()

    def search_products_window(self, instance):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        label = Label(text='Search Product', size_hint=(1, None), height=40)
        layout.add_widget(label)

        keyword_input = TextInput(hint_text='Search Keyword', size_hint=(1, None), height=40)
        layout.add_widget(keyword_input)

        search_button = Button(text='Search', size_hint=(1, None), height=40, background_color=(0, 0, 0.5, 1))
        search_button.bind(on_press=lambda x: self.search_products(keyword_input.text))
        layout.add_widget(search_button)

        cancel_button = Button(text='Cancel', size_hint=(1, None), height=40)
        cancel_button.bind(on_press=self.close_window)
        layout.add_widget(cancel_button)

        scroll_view = ScrollView(size_hint=(None, None), size=(400, 400))
        scroll_view.add_widget(layout)

        self.popup = Popup(title='Search Product', content=scroll_view, size_hint=(None, None), size=(800, 400))
        self.popup.open()

    def add_product(self, name, description, price, quantity):
        sql = "INSERT INTO Products (name, description, price, quantity) VALUES (%s, %s, %s, %s)"
        val = (name, description, price, quantity)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        self.popup.dismiss()

    def edit_product(self, product_id, name, description, price, quantity):
        sql = "UPDATE Products SET name = %s, description = %s, price = %s, quantity = %s WHERE product_id = %s"
        val = (name, description, price, quantity, product_id)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected.")
        self.popup.dismiss()

    def delete_product(self, product_id):
        sql = "DELETE FROM Products WHERE product_id = %s"
        val = (product_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted.")
        self.popup.dismiss()

    def search_products(self, keyword):
        sql = "SELECT * FROM Products WHERE name LIKE %s OR description LIKE %s"
        val = ('%' + keyword + '%', '%' + keyword + '%')
        mycursor.execute(sql, val)
        products = mycursor.fetchall()

        layout = BoxLayout(orientation='vertical')
        label = Label(text='Search Results', size_hint=(1, 0.1))
        layout.add_widget(label)

        # Create a ScrollView to contain the search results
        scrollview = ScrollView(size_hint=(1, 0.8))
        scrolllayout = BoxLayout(orientation='vertical', size_hint_y=None)
        scrolllayout.bind(minimum_height=scrolllayout.setter('height'))

        for product in products:
            product_label = Label(text=f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Quantity: {product[4]}", size_hint_y=None, height=40)
            scrolllayout.add_widget(product_label)

        scrollview.add_widget(scrolllayout)
        layout.add_widget(scrollview)

        close_button = Button(text='Close', size_hint=(1, 0.1))
        close_button.bind(on_press=self.close_window)
        layout.add_widget(close_button)

        self.popup = Popup(title='Search Results', content=layout, size_hint=(None, None), size=(800, 400))
        self.popup.open()
        
    def close_window(self, instance):
        self.popup.dismiss()

if __name__ == '__main__':
    InventoryManagementApp().run()
