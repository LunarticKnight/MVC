from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QDialog, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from controller.controller import FarmController
from model.model import Farm, Goat, Cattle
from model.modelMilk import MilkManager
from model.CalculatedMilk import MilkCalculator 


class CowFarmView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.total_milk = 0  # Initialize total milk produced
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cow and Goat Farm Management')
        self.setGeometry(300, 300, 500, 300)
        self.setStyleSheet("background-color: #f9f9f9;")  # Light grey background

        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('🐄🐐 Cow and Goat Farm Management 🐐🐄', self)
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("margin: 10px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 10px;")
        main_layout.addWidget(header)

        # Input layout
        input_layout = QHBoxLayout()

        # Input field for animal code
        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText('Enter animal code (8 digits)')
        self.code_input.setFont(QFont("Arial", 12))
        self.code_input.setStyleSheet("padding: 8px; border: 2px solid #cccccc; border-radius: 5px;")
        self.code_input.setToolTip('Enter the 8-digit animal code here')
        input_layout.addWidget(self.code_input)

        # Check button
        self.check_button = QPushButton('Check Animal', self)
        self.check_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.check_button.setIcon(QIcon('icons/check.png'))  # Add an icon to the button
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 10px;
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.check_button.setToolTip('Click to check the animal code')
        self.check_button.clicked.connect(self.check_code)
        input_layout.addWidget(self.check_button)

        # Add input layout to the main layout
        main_layout.addLayout(input_layout)

        # Add a frame for additional information or features (optional)
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #ffffff; border: 1px solid #cccccc; border-radius: 5px; padding: 10px;")
        frame.setLayout(QVBoxLayout())  # Can add more widgets to this frame if needed
        main_layout.addWidget(frame)

        # Set the main layout
        self.setLayout(main_layout)

    def check_code(self):
        code = self.code_input.text()

        # Validate the code
        if not code.isdigit() or len(code) != 8 or code[0] == '0':
            QMessageBox.warning(self, 'Invalid Code', 'Code must be 8 digits and not start with 0.')
            return

        # Get result from controller
        result = self.controller.check_animal(code)

        # Add emojis to the result based on the animal type
        if "goat" in result.lower():
            result = "🐐 " + result  # Add goat emoji if it's a goat
        elif "cow" in result.lower():
            result = "🐄 " + result  # Add cow emoji if it's a cow

        # Show the result in a popup window
        self.show_result_popup(result)

    def show_result_popup(self, result):
        # Create a QDialog for the popup
        popup = QDialog(self)
        popup.setWindowTitle('Result')
        popup.setGeometry(350, 350, 400, 200)
        popup.setStyleSheet("background-color: #ffffff; border: 2px solid #cccccc; border-radius: 10px;")

        # Layout for the popup
        layout = QVBoxLayout()

        # Label to display the result
        result_label = QLabel(result, popup)
        result_label.setWordWrap(True)
        result_label.setFont(QFont("Arial", 14))
        result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(result_label)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Milking button
        milking_button = QPushButton('Milking', popup)
        milking_button.setFont(QFont("Arial", 11, QFont.Bold))
        milking_button.setIcon(QIcon('icons/milking.png'))  # Add an icon to the button (optional)
        milking_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        milking_button.setToolTip('Click to milk the cow')
        milking_button.clicked.connect(self.milk_cattle)  # Connect to milking function
        button_layout.addWidget(milking_button)

        # Go to the Mountain button
        mountain_button = QPushButton('Go to the Mountain', popup)
        mountain_button.setFont(QFont("Arial", 11, QFont.Bold))
        mountain_button.setIcon(QIcon('icons/mountain.png'))  # Add an icon to the button (optional)
        mountain_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                padding: 8px;
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        mountain_button.setToolTip('Send the animal to the mountain')
        mountain_button.clicked.connect(self.send_to_mountain)  # Connect to go to mountain function
        button_layout.addWidget(mountain_button)

        # Add button layout to the main layout
        layout.addLayout(button_layout)

        # Set the layout for the popup
        popup.setLayout(layout)
        popup.exec_()  # Use exec_() to display the dialog modally

    def milk_cattle(self):
        """
        Handle the action when the Milking button is clicked.
        """
        code = self.code_input.text()
        animal = self.controller.farm.find_animal_by_code(code)
        if isinstance(animal, Cattle):
            milk_manager = MilkManager(animal)
            milk_calculator = MilkCalculator(animal)
            if animal.teats == 4:
                milk_amount = milk_calculator.calculate_milk_production()
                self.total_milk += milk_amount
                milk_manager.milk_cattle()  # Assuming this function performs the milking action
                QMessageBox.information(self, 'Milking Result', f"Cattle {animal.code} produced {milk_amount} liters of milk.\nTotal milk produced: {self.total_milk} liters.")
            elif animal.teats == 3:
                QMessageBox.information(self, 'Milking Result', f"Cattle {animal.code} has only 3 teats and cannot be milked.")
            else:
                QMessageBox.information(self, 'Milking Result', f"Cattle {animal.code} cannot be milked.")
        else:
            QMessageBox.warning(self, 'Milking Error', 'This action is only available for cattle.')

    def send_to_mountain(self):
        """
        Handle the action when the Go to the Mountain button is clicked.
        """
        code = self.code_input.text()
        animal = self.controller.farm.find_animal_by_code(code)
        if isinstance(animal, Goat):
            QMessageBox.information(self, 'Animal Sent', f"Goat {animal.code} has been sent back to the mountains.")
        elif isinstance(animal, Cattle):
            QMessageBox.information(self, 'Cattle Sent', f"Cattle {animal.code} has been sent back to the mountains.")
        else:
            QMessageBox.warning(self, 'Error', 'This action is only available for goats and cattle.')

if __name__ == '__main__':
    app = QApplication([])
    controller = FarmController('data/cow_goat_data.csv')
    view = CowFarmView(controller)
    view.show()
    app.exec_()
