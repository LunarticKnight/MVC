from model.model import Farm, Goat, Cattle
from model.modelMilk import MilkManager
from model.CalculatedMilk import MilkCalculator 

class FarmController:
    def __init__(self, data_file):
        self.farm = Farm(data_file)

    def check_animal(self, code):
        animal = self.farm.find_animal_by_code(code)
        if not animal:
            return "Animal not found."

        if isinstance(animal, Goat):  # เชคว่าแพะไหม
            return "This is a goat. Send it back to the mountains."
        elif isinstance(animal, Cattle):  # เช็คว่าวัวไหม
            milk_manager = MilkManager(animal)
            milk_calculator = MilkCalculator(animal)

            if animal.teats == 4:
                milk_amount = milk_manager.milk_cattle()  # รีดนม
                milk_amount = milk_calculator.calculate_milk_production()  
                return f"Cattle {animal.code} was milked and produced {milk_amount} liters of milk."
            else:
                milk_manager.recover_teats()  
                return f"Cattle {animal.code} cannot be milked with {animal.teats} teats. Checking for recovery."