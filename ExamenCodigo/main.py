from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHeaderView,QDialog, QMessageBox
from database import Database
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Signal
import sys
import os

class VentanaAfegir(QDialog):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        interface_path = os.path.join(os.path.dirname(__file__), "interface_afegir.ui")
        self.interfaz_afegir = loader.load(interface_path, None)
        self.db = Database(db_name=os.path.join(os.path.dirname(__file__), 'users.db'))
        self.db.conn
        self.layout = QVBoxLayout()
        self.interfaz_afegir.setLayout(self.layout)

        self.userapp=UserApp()

        # Formulari (afegit directament a la finestra)
        self.name_input = QLineEdit()
        self.password_input = QLineEdit() 
        self.role_input = QLineEdit() 

        self.layout.addWidget(QLabel("Nom:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Contrasenya:"))  
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(QLabel("Rol (Admin, Usuari, Convidat):")) 
        self.layout.addWidget(self.role_input)

        # Botons per afegir i modificar
        self.add_button = QPushButton("Afegir Usuari")
        self.add_button.clicked.connect(self.add_user)
        self.layout.addWidget(self.add_button)

        self.interfaz_afegir.show()

    def add_user(self):
        name = self.name_input.text()
        password = self.password_input.text() 
        role = self.role_input.text()  
        if name and password and role:
            self.db.add_user(name, password, role)
            UserApp().load_users()

class VentanaModificar(QDialog):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        interface_path = os.path.join(os.path.dirname(__file__), "interface_afegir.ui")
        self.interfaz_modificar = loader.load(interface_path, None)
        self.db = Database(db_name=os.path.join(os.path.dirname(__file__), 'users.db'))
        self.userapp=UserApp()

        self.layout = QVBoxLayout()
        self.interfaz_modificar.setLayout(self.layout)

        # Formulari (afegit directament a la finestra)
        self.name_input = QLineEdit()
        self.password_input = QLineEdit() 
        self.role_input = QLineEdit() 
        #user_id = self.db.get_users()[selected_row][0]
        self.layout.addWidget(QLabel("Nom:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Contrasenya:"))  
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(QLabel("Rol (Admin, Usuari, Convidat):")) 
        self.layout.addWidget(self.role_input)

        # Botons per afegir i modificar
        self.edit_button = QPushButton("Modificar Usuari")
        self.edit_button.clicked.connect(self.edit_user)
        self.layout.addWidget(self.edit_button)

        self.interfaz_modificar.show()

    def edit_user(self):
        selected_row = UserApp().table.currentRow()
        if selected_row == -1:
            return
        user_id = self.db.get_users()[selected_row][0]
        boton_pulsado = QMessageBox.question(
        self,
        "Estas segur?",
        "Seguro que quieres modificar?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No
        )
       
        if boton_pulsado==QMessageBox.Yes:
            if new_name and new_password and new_role:
                new_name = self.name_input.text()
                new_password = self.password_input.text()  
                new_role = self.role_input.text()
                self.db.update_user(user_id, new_name, new_password, new_role)
                self.load_users()
    
    

    

class UserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestió d'Usuaris")
        self.setGeometry(100, 100, 600, 500)
        self.db = Database(db_name=os.path.join(os.path.dirname(__file__), 'users.db'))
        self.ventana_afegir=None
        self.ventana_modificar=None

        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Usuaris")
        accion = QAction("&Afegir", self)
        accion.setShortcut(QKeySequence("Ctrl+A"))
        accion.triggered.connect(self.abrir_ventana_afegir)
        menu.addAction(accion)
        accion2 = QAction("&Modificar", self)
        accion2.setShortcut(QKeySequence("Ctrl+M"))
        accion2.triggered.connect(self.abrir_ventana_modificar)
        menu.addAction(accion2)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_user)
        self.layout.addWidget(self.delete_button)

        # Taula d'usuaris
        self.table = self.create_table()
        self.layout.addWidget(self.table)

        self.load_users()

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nom", "Contrasenya", "Rol"])  
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        table.setSelectionBehavior(QTableWidget.SelectRows)  
        return table

    def load_users(self):
        self.table.setRowCount(0)
        users = self.db.get_users()
        for row_index, (user_id, name, password, role) in enumerate(users):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(password))  
            self.table.setItem(row_index, 2, QTableWidgetItem(role))

    


    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        
        user_id = self.db.get_users()[selected_row][0]

        boton_pulsado = QMessageBox.question(
        self,
        "Estas segur?",
        "Seguro que quieres eliminar?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No
        )
        if boton_pulsado==QMessageBox.Yes:
            self.db.delete_user(user_id)
            self.load_users()
        
    
    def abrir_ventana_afegir(self):
        if self.ventana_afegir is None:
            self.ventana_afegir = VentanaAfegir()
            self.ventana_afegir.move(self.pos())
        else:
            if self.ventana_afegir.isHidden():
                self.ventana_afegir.move(self.pos())
                self.ventana_afegir.interfaz_afegir.show()
            else:
                self.ventana_afegir.hide()

    def abrir_ventana_modificar(self):
        if self.ventana_modificar is None:
            self.ventana_modificar = VentanaModificar()
            self.ventana_modificar.move(self.pos())
        else:
            if self.ventana_modificar.isHidden():
                self.ventana_modificar.move(self.pos())
                self.ventana_modificar.interfaz_modificar.show()
            else:
                self.ventana_modificar.hide()


            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserApp()
    window.show()
    sys.exit(app.exec())