import json
import numpy as np


def get_elements() -> "returns a dict of elements: {element: description}":
    file_name = "PeriodicTableJSON.json"
    file = open(file_name, "r")

    element_information = json.load(file)["elements"]  # the elements dictionary value
    elements = {}
    for element in element_information:
        # make it so that it is in the format of name: information
        elements[element["name"]] = {key: value for key, value in element.items() if key != "name"}

    return elements


def symbol_mass_key_pair() -> dict:
    # this essentially makes the key the symbol get paired up with its mass
    symbol_mass_pair = {}
    for element, properties in get_elements().items():
        symbol_mass_pair[properties["symbol"]] = properties["atomic_mass"]
    return symbol_mass_pair


def process_element_information(element: dict) -> "returns a dict of information for an element":
    # TODO process the following information in other tabs.
    things_not_for_show = ["source", "spectral_img", "xpos", "ypos", "shells"]
    information = ""
    for key, value in element.items():
        if key not in things_not_for_show:
            key = key.split("_")
            category = " ".join(key).capitalize()
            information += f"{category}: {value}\n"
    return information


def symbol_element_name_key_pair() -> dict:
    return {symbol["symbol"]: name for name, symbol in get_elements().items()}


def element_mass(element: dict) -> "returns the mass of an element":
    return element["atomic_mass"]


class MolarMass:
    def __init__(self, molecule: str):
        self.capital_letters = [chr(x) for x in range(65, 91)]
        self.lowercase_letters = [chr(x) for x in range(97, 123)]
        self.molecule = molecule
        # the frequency of each element
        self.element_frequencies = self._count_molecule()
        # a whole dictionary of each element mass base off of atomic symbol
        self.dict_of_element_mass = symbol_mass_key_pair()
        # the molar mass of the given element
        self.molar_mass = self._calculate_molar_mass()
        # the element composition {element: (total mass, abundance in decimal)}
        self.element_composition = self._element_composition()

    def __str__(self):
        return self.molecule

    def _separate_molecule(self):

        list_of_elements = []
        list_of_elements_with_count = []
        instance_of_capital = True
        element = ""
        times_to_continue = 0
        # for each character in the molecule
        for i, character in enumerate(self.molecule):
            if character in self.capital_letters and instance_of_capital:
                element += character
                instance_of_capital = False
                if i == len(self.molecule) - 1:
                    list_of_elements.append(element)
            elif character in self.lowercase_letters:
                element += character
                if i == len(self.molecule) - 1:
                    list_of_elements.append(element)
            elif character in self.capital_letters:
                list_of_elements.append(element)
                element = ""
                element += character
                if i == len(self.molecule) - 1:
                    list_of_elements.append(element)
            elif isinstance(eval(character), int):
                element += character
                instance_of_capital = True
                index = i
                while True:
                    try:
                        if isinstance(eval(self.molecule[index + 1]), int):
                            element += self.molecule[index + 1]
                            index += 1
                        else:
                            break
                    except Exception as e:
                        break
                list_of_elements.append(element)
                element = ""

        for entry in list_of_elements:
            try:
                if isinstance(eval(entry), int):
                    continue
            except Exception as e:
                list_of_elements_with_count.append(entry)

        return list_of_elements_with_count

    def _count_molecule(self):
        separated_molecule = self._separate_molecule()
        dict_of_elements = {}
        for entry in separated_molecule:
            key, value = "", ""
            for character in entry:
                if character in self.capital_letters or character in self.lowercase_letters:
                    key += character
                else:
                    value += character
            if value == "":
                value = 1
            dict_of_elements[key] = int(value)
        return dict_of_elements

    def _calculate_molar_mass(self):
        molar_mass = 0
        for element, frequency in self.element_frequencies.items():
            molar_mass += self.dict_of_element_mass[element] * frequency
        return molar_mass

    def _element_composition(self):
        calculations = {}
        for element, frequency in self.element_frequencies.items():
            mass = self.dict_of_element_mass[element] * frequency
            calculations[element] = (mass, mass / self.molar_mass)

        return calculations

    def show_element_composition(self):
        answer = "{:<12}{:<20}{:<20}\n".format(self.molecule, "Relative Mass (g)", "Percent Mass")
        percent = 0
        for element, value in self.element_composition.items():
            percent += value[1]
            answer += "{:<12}{:<20}{:<20}\n".format(element, value[0], f"{round(value[1] * 100, 1)}%")

        answer += "______________________________________________\n"
        answer += "{:<12}{:<20}{:<20}".format("Total", self.molar_mass, f"{percent * 100}%")
        return answer

    def show_calculation(self):
        answer = "First, count up each element that resides within the molecule.\n"
        for element, frequency in self.element_frequencies.items():
            answer += f"{element}: {frequency}\n"
        answer += "\nThen search up the mass of each respective element.\n"
        for element in self.element_composition:
            answer += f"{element}: {self.dict_of_element_mass[element]} g \n"
        answer += "\nThen multiply the mass by the number of elements that exists within the molecule.\n"
        for element, mass in self.element_composition.items():
            answer += f"{element}: {self.element_frequencies[element]} x " \
                      f"{self.dict_of_element_mass[element]} g = {mass[0]} g\n"
        answer += f"\nThen add all of the calculated masses and that would be the total molar mass.\nTotal mass:" \
                  f" {self.molar_mass}"
        return answer


class PercentComp:
    def __init__(self, elements: list, percents: list, abundance=None):
        self.elements_percent_pair = {element: percents[i] for i, element in enumerate(elements)}
        self.abundance = abundance
        self.symbol_mass_key_pair = symbol_mass_key_pair()
        self.fractions = [0, 1/3, 0.25, 2/3, 0.5, 0.75, 1]
        self.empirical_formula = self._empirical_formula()
        self.molecular_formula = self._molecular_formula()

    @ staticmethod
    def closest(fractions, mole_value):
        return fractions[min(range(len(fractions)), key=lambda i: abs(fractions[i] - mole_value))]

    def _empirical_formula(self):
        moles = {}
        smallest_mole = None
        for element, percent in self.elements_percent_pair.items():
            moles[element] = percent * 100 / self.symbol_mass_key_pair[element]
            if smallest_mole is None:
                smallest_mole = moles[element]
            else:
                if moles[element] < smallest_mole:
                    smallest_mole = moles[element]
        for element, mole in moles.items():
            moles[element] = round(mole / smallest_mole, 1)

        def mole_multiplier(molecules: dict):
            multiplier = 1
            for element, molecule in molecules.items():
                molecule = float(str(molecule)[1:])
                closest_fraction = self.closest(self.fractions, molecule)
                if closest_fraction == 0:
                    continue
                elif closest_fraction == 1/3 or closest_fraction == 2/3:
                    multiplier *= 3
                elif closest_fraction == 0.25 or closest_fraction == 0.75:
                    multiplier *= 4
                elif closest_fraction == 0.5:
                    multiplier *= 2
                elif closest_fraction == 1:
                    multiplier *= 1
            return multiplier

        multiplier = mole_multiplier(moles)
        empirical_formula = ""
        for element, mole in moles.items():
            mole *= multiplier
            empirical_formula += element + str(int(round(mole)))
        moles.update((x, y * multiplier) for x, y in moles.items())

        return empirical_formula, moles

    def _molecular_formula(self):
        molar_mass = MolarMass(self.empirical_formula[0])
        molecular_formula = None
        # TODO make sure that the rounding is exactly what i wanted it to be. ASK Angel.
        if self.abundance is not None:
            multiplier = round(self.abundance / molar_mass.molar_mass)
            molecular_formula = {key: value * multiplier for key, value in self.empirical_formula[1].items()}
        return molecular_formula


class EquationBalance:
    def __init__(self, reactants: str, products: str):
        self.reactants = reactants.replace(" ", "").split(",")
        self.products = products.replace(" ", "").split(",")

    def _separate_compounds(self):
        reactant_objects = []
        product_objects = []
        available_elements = []
        number_of_columns = 0

        for reactant in self.reactants:
            reactant_objects.append(MolarMass(reactant))
            available_elements += [key for key, value in MolarMass(reactant).element_frequencies.items()
                                   if key not in available_elements]
            number_of_columns += 1
        for product in self.products:
            product_objects.append(MolarMass(product))
            number_of_columns += 1
        array_list = []
        for element in available_elements:
            row_array = []
            for reactant in reactant_objects:
                if element in reactant.element_frequencies:
                    row_array.append(-reactant.element_frequencies[element])
                else:
                    row_array.append(0)
            for product in product_objects:
                if element in product.element_frequencies:
                    row_array.append(product.element_frequencies[element])
                else:
                    row_array.append(0)
            array_list.append(row_array)
        end_array = []
        for x in range(number_of_columns):
            end_array.append(0)
        end_array[0] = 1
        array_list.append(end_array)
        if len(array_list) % 2 != 0:
            for elements in array_list:
                elements.append(0.0000000000001)
        return array_list, end_array

    def balance_equation(self):
        fractions = [0, 1/3, 0.25, 2/3, 0.5, 0.75, 1]
        array_lists = self._separate_compounds()
        stoich_mat = np.array(array_lists[0])
        end_array = array_lists[1]
        end_array[0] = 0
        end_array[-1] = 1
        rhs = np.array(end_array)
        raw_coefficients = []
        smallest = None
        coefficients = [x for x in np.linalg.solve(stoich_mat, rhs)]
        if coefficients[-1] == 0:
            coefficients.pop()
        for coefficient in coefficients:
            raw_coefficients.append(coefficient)
            if smallest is None:
                smallest = coefficient
            elif smallest > coefficient:
                smallest = coefficient
        multiplier = 1
        processed_coefficients = []
        for raw_coefficient in raw_coefficients:
            raw_coefficient /= smallest
            processed_coefficients.append(raw_coefficient)
            dummy = float(str(raw_coefficient)[1:])
            closest = PercentComp.closest(fractions=fractions, mole_value=dummy)
            if closest == 0:
                continue
            elif closest == 1 / 3 or closest == 2 / 3:
                multiplier *= 3
            elif closest == 0.25 or closest == 0.75:
                multiplier *= 4
            elif closest == 0.5:
                multiplier *= 2
            elif closest == 1:
                multiplier *= 1
        processed_coefficients = [x * multiplier for x in processed_coefficients]
        balanced_equation = ""
        index = 0
        numbers = [str(x) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
        for i, reactant in enumerate(self.reactants):
            new_reactant = ""
            for letter in reactant:
                if letter in numbers:
                    new_reactant += f"[sub]{letter}[/sub]"
                    continue
                new_reactant += letter
            if i != len(self.reactants) - 1:
                balanced_equation += f"{int(processed_coefficients[i])}({new_reactant}) + "
                index += 1
            else:
                index += 1
                balanced_equation += f"{int(processed_coefficients[i])}({new_reactant}) -> "
        for i, product in enumerate(self.products):
            new_product = ""
            for letter in product:
                if letter in numbers:
                    new_product += f"[sub]{letter}[/sub]"
                    continue
                new_product += letter
            if i != len(self.products) - 1:
                balanced_equation += f"{int(processed_coefficients[i + index])}({new_product}) + "
            else:
                balanced_equation += f"{int(processed_coefficients[i + index])}({new_product})"
        return balanced_equation


if __name__ == "__main__":
    # print(process_element_information(get_elements()["Hydrogen"]))
    # print(element_mass(get_elements()["Hydrogen"]))
    entry_molar_mass = MolarMass("MgSO4")
    # print(entry_molar_mass.show_element_composition())
    # print(entry_molar_mass.molar_mass)
    percent_comp = PercentComp(["C", "H", "N", "O"], [0.5714, 0.0616, 0.0952, 0.2718], 290)
    # # print(percent_comp.elements_percent_pair)
    # # print(get_elements()["Hydrogen"]["atomic_mass"])
    print(percent_comp.empirical_formula[1])
    # print(percent_comp.molecular_formula)
    # print(percent_comp.abundance)
    # temp = EquationBalance("C6H12O6, O2", "CO2, H2O")
    # print(entry_molar_mass.show_calculation())
    # print(symbol_element_name_key_pair())
