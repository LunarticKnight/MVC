import sys
import os
from PyQt5.QtWidgets import QApplication

# ตั้งค่า sys.path ให้รู้จักโฟลเดอร์หลัก
#Cattle = วัว นะครับ
#Teat = นมวัว
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# นำเข้าโมดูลจากโฟลเดอร์ย่อย
from view.view import CowFarmView
from controller.controller import FarmController

def main():
    app = QApplication(sys.argv)
    controller = FarmController(r'D:\MVC\Data\cow_goat_data.csv')
    view = CowFarmView(controller)
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
