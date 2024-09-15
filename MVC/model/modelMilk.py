import random

class MilkManager:
    def __init__(self, cattle):
        self.cattle = cattle

    def milk_cattle(self):
        """
        Milks the cattle if it has 4 teats and has a 25% chance to lose one teat during milking.
        """
        if self.cattle.teats == 4:
            # Calculate the amount of milk produced
            milk_amount = self.cattle.milk_yield()
            print(f"Cattle {self.cattle.code} was milked and produced {milk_amount} liters of milk.")

            # 25% chance to lose a teat
            if random.random() < 0.05:
                self.cattle.teats -= 1
                print(f"Cattle {self.cattle.code} lost a teat during milking. Now has {self.cattle.teats} teats.")

            return milk_amount
        else:
            print(f"Cattle {self.cattle.code} cannot be milked because it does not have 4 teats.")
            return 0

    def recover_teats(self):
        """
        Checks if a cattle with 3 teats has a 20% chance to recover to 4 teats.
        """
        if self.cattle.teats == 3:
            # 20% chance to recover to 4 teats
            if random.random() < 0.20:
                self.cattle.teats = 4
                print(f"Cattle {self.cattle.code} has recovered and now has 4 teats.")
        else:
            print(f"Cattle {self.cattle.code} does not need recovery, it already has {self.cattle.teats} teats.")
