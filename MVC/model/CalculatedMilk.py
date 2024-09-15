class MilkCalculator:
    def __init__(self, cattle):
        self.cattle = cattle

    def calculate_milk_production(self):
        """
        Calculate the amount of milk produced based on age.
        """
        if self.cattle.teats == 4:
            milk_amount = self.cattle.age_years + self.cattle.age_months
            print(f"Cattle {self.cattle.code} produced {milk_amount} liters of milk.")
            return milk_amount
        return 0
