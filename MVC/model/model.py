import csv

class Cattle:
    def __init__(self, code, age_years, age_months, teats):
        self.code = code
        self.age_years = age_years
        self.age_months = age_months
        self.teats = teats

    def milk_yield(self):
        return self.age_years + self.age_months

class Goat:
    def __init__(self, code):
        self.code = code

class Farm:
    def __init__(self, file_path):
        self.animals = []
        self.load_data(file_path)

    def load_data(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # ข้าม Header แถวแรก
            for row in reader:
                try:
                    # ตรวจสอบว่าข้อมูลในแถวไม่ครบให้ถือว่าเป็นแพะ
                    if len(row) < 4 or any(col.strip() == '' for col in row):
                        # ถ้าแถวนี้มีข้อมูลไม่ครบ หรือมีค่าว่าง ถือว่าเป็นแพะ
                        code = row[0]  # รับเฉพาะรหัส
                        if len(code) == 8 and code.isdigit() and code[0] != '0':
                            self.animals.append(Goat(code))
                        else:
                            print(f"Invalid code format for goat: {code}, skipping this row.")
                    else:
                        # ถ้ามีข้อมูลครบ 4 คอลัมน์และไม่มีค่าว่างถือว่าเป็นวัว
                        code, age_years, age_months, teats = row
                        
                        # แปลงค่าคอลัมน์ที่เป็นตัวเลขหลังจากตรวจสอบว่ามีข้อมูลครบ
                        age_years = int(age_years)
                        age_months = int(age_months)
                        teats = int(teats)

                        if teats not in [3, 4]:
                            raise ValueError("Invalid number of teats")

                        if len(code) == 8 and code.isdigit() and code[0] != '0':
                            self.animals.append(Cattle(code, age_years, age_months, teats))
                        else:
                            print(f"Invalid code format for cattle: {code}, skipping this row.")
                except ValueError as e:
                    print(f"Error converting data for code {row[0]}: {e}, skipping this row.")
                except Exception as e:
                    print(f"Unexpected error with code {row[0]}: {e}, skipping this row.")

    def find_animal_by_code(self, code):
        for animal in self.animals:
            if animal.code == code:
                return animal
        return None
