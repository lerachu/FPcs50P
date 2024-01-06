import requests
import csv
import sys
import argparse
    

class Minerals:
    """Class objects aim to count the daily intake of minerals and compare them to norms"""
    # List of minerals 
    microelements = ["Chromium, Cr (µg)", "Copper, Cu (mg)", "Fluoride, F (µg)", "Iodine, I (µg)", "Iron, Fe (mg)", "Manganese, Mn (mg)", "Molybdenum, Mo (µg)", "Selenium, Se (µg)", "Zinc, Zn (mg)", "Magnesium, Mg (mg)", "Calcium, Ca (mg)", "Potassium, K (mg)", "Phosphorus, P (mg)"]

    def __init__(self, minerals_dict, person):
        """
        :param minerals_dict: dict with minerals as keys
        :type minerals_dict: dict
        :param person: tuple ("human category", "age")
        :type person: tuple
        """
        # Tracks chosen minerals
        self._minerals = minerals_dict
        # Contains chosen minerals norms
        self._norms = self.norms_for_minerals(person)

    @property
    def minerals(self):
        return self._minerals
    
    @property
    def norms(self):
        return self._norms
    

    def update(self, elem, weight):
        """
        Updates the value of mineral(elem) weight in "minerals" dictionary
        :param elem: name of mineral
        :type elem: string
        :param weight: weight of mineral to update on
        :type weight: float
        """
        self._minerals[elem] += weight

    def add_food(self, product, weight):
        """
        Calls "update" function on minerals of "minerals" dict that are in product

        :param product: the dict with information on food
        :type product: dict
        :param weight: weight of food
        :type weight: float
        """
        for elem in self.minerals:
            for nutrient in product["foodNutrients"]:
                # For each element in minerals if element is in nutrients - update minerals dict on this element
                if nutrient["nutrientName"].startswith(elem.split(" ")[0].strip(",")):
                    # Count weight of the element in the food
                    elem_weight = nutrient["value"] * weight / 100
                    self.update(elem, elem_weight)

    def norms_for_minerals(self, person):
        """
        Exepts tuple of "human category" and class object
        Counts minerals's norms for person for each chosen mineral
        Returns dict with key - "mineral", value - norm 
        """
        minerals_norms = dict()

        for elem in self.minerals:
            minerals_norms[elem] = Minerals.count_mineral_norm_for_person(person, elem)

        return minerals_norms
    
    def compare_with_norms(self):
        """
        Counts shortages for each mineral
        Returns dict with key - "mineral", value - shortage 
        """
        shortages = dict()
        for elem in self.minerals:
            shortages[elem] = self.norms[elem] - self.minerals[elem] 

        return shortages
    
    def print_shortages(self):
        """
        Prints shortages
        """
        # Count shortages
        shortages = self.compare_with_norms()
        s = False # If there are no shortages
        for elem in shortages:
                # If value in dict > 0 - there is deficit of mineral(key)
                if shortages[elem] > 0:
                    s = True
                    print(f"Shortage for {elem} is {shortages[elem]:.2f}")
                    print()
        if not s:
            print("No mineral deficiency")
    
    @classmethod
    def count_mineral_norm_for_person(cls, person, elem):
        """
        Counts norm for mineral(elem) for given person
        Returns norm
        """
        # Use table of minerals' norms for categories of people
        with open("data.csv") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Search within suitable category
                if row["category"] == person[0]:
                    if person[1] >= 51:
                        if row["age"] == "51+":
                            return float(row[elem])
                    else: 
                        min, max = [float(age) for age in row["age"].split("-")]
                            
                        if min <= person[1] <= max:
                            return float(row[elem])
    
    @classmethod
    def choose(cls, person):
        """
        Method for creating Minerals object by choosing minerals of interest;
        :Returns call for class object initialization or None if user haven't chosen any mineral
        """

        minerals_dict = dict()  # Empty dict for choosing minerals
        while True:
            # Printing available minerals
            for i, el in enumerate(cls.microelements):
                print(f"{i + 1}:", el)

            print()    
            m = input(f"Input mineral's index you want to choose from the list above (or enter 'all' for all): ")
            print()
            # If user chooses all minerals - add all minerals to the dict
            if m == "all":
                # If user have chosen minerals before entering "all" - the dict will concatenate with rest of minerals in cls.minerals
                minerals_dict = {**minerals_dict, **{elem: 0 for elem in cls.microelements}}  
                break
            # If user finished with choosing - break    
            if not m:
                break
            else:
                # Check on correct input (integer)
                try:
                    m = int(m)
                except ValueError:
                    print("Not an integer number\n")
                else:
                    # Check on correct input (correct index)
                    if m <= 0 or m > len(cls.microelements):
                        print("No such index\n")
                    else:
                        # Add mineral to a dict (with "weight" 0 as key)
                        minerals_dict[cls.microelements[m -1]] = 0
                        cls.microelements.pop(m - 1)  # Delete chosen mineral from list
        # If User haven't chosen any mineral
        if not minerals_dict:
            return None
        
        print("You chose: ")
        for i, mineral in enumerate(minerals_dict):
            print(f"{i + 1}:", mineral)
        print() 

        return cls(minerals_dict, person)


def human():
    """
    Returns tuple ("human category", "age")
    """
    # Prompt for age until correct age (> 0, float)
    while True:
        age = input("Input age in years: ") 
        print()   
        try:
            age = float(age)
        except ValueError:
            print("Not a number\n")
        else:
            if age <= 0:
                print("Not an age\n")
            else:
                break
    
    if age >= 9:
        # Prompt for gender until correct input
        while True:
            gender = input('Input gender ("m" for male , "f" for female): ')
            print()
            if gender not in {'m', 'f'}:
                continue
            else:
                break
        # Prompt for additional Information until correct input
        if gender == 'f' and 14 <= age < 51:
            while True:
                f = input("Enter 'p' for pregnant, 'l' for lactation, 'n' for none: ")
                print()
                if f in {'p', 'l', 'n'}:
                    break
    
    if age < 1:
        human = ("baby", round(age, 1))
    elif age < 9:
        human = ("child", age // 1)
    elif gender == 'm':
        human = ("male", age // 1)
    elif age >= 51:
        human = ("female", age // 1)
    elif age < 14:
        human = ("female", age // 1)
    elif f == 'p':
        human = ("femalep", age // 1)
    elif f == 'l':
        human = ("femalel", age // 1)
    elif f == 'n':
        human = ("female", age // 1)

    return human


def human_parser(a, g, i):
    """
    Checks command line arg-s on correctness:
    - Returns None if incorrect, else returns tuple ("human category", "age")
    """
    if a <= 0:
        return None
    if a < 1:  
        human = ("baby", round(a, 1))
    elif a < 9:
        human = ("child", a // 1)
    elif g not in {"m", "f"}:
        return None
    elif g == 'm':
        human = ("male", a // 1)
    elif a >= 51 or i == 'n':
        human = ("female", a // 1)
    elif a < 14:
        human = ("female", a // 1)
    elif i not in {"p", "l", "n"}:
        return None
    elif i == 'p':
        human = ("femalep", a // 1)
    elif i == 'l':
        human = ("femalel", a // 1)
    
    return human


def food_plan_for_a_day():
    """
    Searchs food in remote database, yields sequentionaly chosen products
    """
    while True:
        food_item = input("Enter food item: ")
        # If user finished adding food
        if not food_item:
            break
        # Prompt for food weight until correct input (float > 0)    
        while True:
            try:
                weight = float(input("Enter weight of the item in gramms: "))
            except ValueError:
                print("Should be a number\n")
                continue
            if weight <= 0:
                print("Should be > 0\n")
                continue
            else:
                break

        print()
        # Request to remote database
        response = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={food_item}&pageSize=5")
        # Check status code
        if response.status_code != 200:
            print("Couldn't find the food item in the database, try again.")
        else:
            # If empty list of foods
            if not response.json()["foods"]:
                    print("Couldn't find the food item in the database, try again.")
                    continue
            while True:
                # Print food options fmom response
                for i, option in enumerate(response.json()["foods"]):
                    try:
                        print(i + 1, "Description: ", option["description"],"\n", "Food category:", option["foodCategory"])
                    except KeyError:
                        continue
                    print()

                choice = input("Choose the option that best suits your request (enter index) or enter 'n' for none: ")
                print()
                # If no suitable options - next try
                if choice == "n":
                    print("Try better query")
                    break
                # Check for correctness of the input    
                try:
                    choice = int(choice)   
                except ValueError:
                    print("Index should be an integer number\n")
                    continue
                if choice not in range(1, len(response.json()["foods"]) + 1):
                    print("Wrong index\n")
                    continue
                else:
                    break
            # If no suitable options - next try        
            if choice == "n":
                continue
            # Extract product of choice    
            product = response.json()["foods"][choice - 1]
            # yield to not keep all products at list
            yield (product, weight)
            

def parse_arguments():
    """Parse command line arguments. Returns parser object."""
    parser = argparse.ArgumentParser(description="Calculates mineral deficiency in the daily diet")
    parser.add_argument("-a", help="age", type=float) 
    parser.add_argument("-g", help="gender ('m'/'f' - required only for age >= 9)") 
    parser.add_argument("-i", help="'p' for pregnant, 'l' for lactation, 'n' for none (required only for females of 14 <= age <=50)")
    return parser.parse_args()


def main():
    # Parse command line arguments
    args = parse_arguments()
    # If user entered command line arg-s - use "human_parser" function
    if args.a:
        person = human_parser(args.a, args.g, args.i)
        # Check correctness of arg-s
        if not person:
            sys.exit("Invalid command arguments")
    # Else "human" function
    else:
        person = human()
    
    # Create "Minerals" object
    minerals_obj = Minerals.choose(person)
    if not minerals_obj:
        sys.exit("You haven't chosen any mineral")

    while True:
        # Choose food for a day
        for (product, weight) in food_plan_for_a_day():
            # Call "add_food" on product with weight to update minerals
            minerals_obj.add_food(product, weight)
        print()
        # Prints mineral shortages for chosen diet
        minerals_obj.print_shortages()
        # Ask user if they want to add more food
        more = input("Do you wanna add more food? y/n: ")
        print()
        # If yes - let add more food
        if more != "y":
            break
    

if __name__ == "__main__":
    main()   