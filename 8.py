import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from pymongo import MongoClient

# Replace the connection string with your own
client = MongoClient("mongodb+srv://tusharpatil:tushar@cluster0.ewinp3v.mongodb.net/test")

db = client.test_database
collection = db.test_collection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MongoDB CRUD Demo")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.add_widget = QWidget()
        self.add_layout = QHBoxLayout()
        self.add_widget.setLayout(self.add_layout)

        self.add_label = QLabel("Add item:")
        self.add_edit = QLineEdit()
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item)

        self.add_layout.addWidget(self.add_label)
        self.add_layout.addWidget(self.add_edit)
        self.add_layout.addWidget(self.add_button)

        self.layout.addWidget(self.add_widget)

        self.central_widget.setLayout(self.layout)

        self.refresh_list()

    def refresh_list(self):
        self.list_widget.clear()
        items = collection.find()
        for item in items:
            list_item = QListWidgetItem(item["name"])
            list_item.setData(0, item["_id"])
            self.list_widget.addItem(list_item)

    def add_item(self):
        name = self.add_edit.text()
        if name:
            collection.insert_one({"name": name})
            self.add_edit.clear()
            self.refresh_list()

    def delete_item(self, item_id):
        collection.delete_one({"_id": item_id})
        self.refresh_list()

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
