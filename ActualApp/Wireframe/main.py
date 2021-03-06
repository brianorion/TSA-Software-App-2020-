from DataStorage import Authentication, Database
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text.markup import MarkupLabel
from kivy.core.window import Window
from kivy.core.text import LabelBase
import json
import Elements as elements


# all of the screens
class Login(Screen):
    pass


class ForgotPassword(Screen):
    pass


class SignupStudentOrTeacher(Screen):
    pass


class SignupStudent(Screen):
    pass


class SignupTeacher(Screen):
    pass


class HomePageStudent(Screen):
    pass


class HomePageStudentMolarTab(Screen):
    pass


class HomePageTeacher(Screen):
    pass


class SearchElement(Screen):
    pass


class BalancingEquations(Screen):
    pass


class MolarCalculator(Screen):
    pass


class AcidBase(Screen):
    pass


class CalculateFormula(Screen):
    pass


class LewisStructure(Screen):
    pass


# Some Helpful Methods
def process_error_message(error_message):
    error_message = error_message.split("_")
    return_message = ""
    for message in error_message:
        return_message += message.capitalize() + " "

    return return_message


def process_message(messages: str, key=True):
    returned_message = ""
    if key:
        messages = messages.split("_")
        for index, message in enumerate(messages):
            if len(messages) - 1 != index:
                returned_message += message.capitalize() + "\n"
            else:
                returned_message += message.capitalize()
    else:
        for index, message, in enumerate(messages):
            message = str(message)
            if index % 2 == 0:
                returned_message += "\n"
            returned_message += message + ", "
            print(message)
        returned_message = returned_message.rstrip(", ")
    return returned_message

# All of the fonts
Cabin_Sketch_Dir = "Fonts/Cabin_Sketch/"
Open_Sans_Dir = "Fonts/Open_Sans/"
LabelBase.register(name="Cabin Sketch", fn_regular=f"{Cabin_Sketch_Dir}CabinSketch-Regular.ttf")
LabelBase.register(name="Open Sans Light", fn_regular=f"{Open_Sans_Dir}OpenSans-Light.ttf")
LabelBase.register(name="Open Sans", fn_regular=f"{Open_Sans_Dir}OpenSans-Regular.ttf",
                   fn_bold=f"{Open_Sans_Dir}OpenSans-ExtraBold.ttf")

kv = Builder.load_file("kv/main.kv")


class MainApp(App):
    error_messages = ["INVALID_EMAIL", "INVALID_PASSWORD", "WEAK_PASSWORD : Password should be at least 6 characters",
                      "EMAIL_EXISTS", "EMAIL_NOT_FOUND"]
    can_change_screen = True
    screen_manager = "screen_manager"
    forgot_password_popup = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.local_id = None
        self.SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        self.SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    def build(self):
        Window.size = (1080, 2050)  # 1080, 2050
        return kv

    # changes the current screen to another screen if a button was pressed.
    def change_screen(self, screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.transition = NoTransition()
        try:
            error_text = self.root.ids[screen_name].ids["error_text"]
            error_text.text = ""
        except Exception as e:
            print("No text available")
        if screen_manager.current == "signup_student":
            self.sign_up_for_students()

        if self.can_change_screen:
            screen_manager.current = screen_name
            print(screen_manager.current)

    def back_button(self, screen_name, change_screen: bool):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.transition = NoTransition()
        if change_screen:
            screen_manager.current = screen_name
            self.can_change_screen = True
            print(screen_manager.current)

    # Popup window method
    def show_popup(self):
        self.forgot_password_popup = ForgotPassword()
        popup_window = Popup(title="Chem Hero", content=self.forgot_password_popup,
                             size_hint=(0.8333333333333334, 0.43902439024390244))
        popup_window.open()

    # student sign up
    def sign_up_for_students(self):
        sign_up_student_screen = self.root.ids["signup_student"]
        email = sign_up_student_screen.ids["student_email_signup"]
        password = sign_up_student_screen.ids["student_password_signup"]
        name = sign_up_student_screen.ids["name"]
        dob = sign_up_student_screen.ids["DOB"]
        username = sign_up_student_screen.ids["username"]
        error_text = sign_up_student_screen.ids["error_text"]

        # the authentication process
        auth = Authentication()
        local_id = auth.signup(email.text, password.text)

        if email.text == "" or password.text == "" or name.text == "" or dob == "" or username == "":
            error_text.text = "Missing Inputs"
            self.can_change_screen = False
        elif local_id in self.error_messages:
            error_text.text = process_error_message(local_id)
            self.can_change_screen = False
        else:
            # the data
            data = {"Occupation": "Student", "name": name.text,
                    "Date of Birth": dob.text, "Username": username.text,
                    "Email": email.text}

            # the database storing process
            database = Database.db
            database.child("Users").child(local_id).set(data)

            email.text = ""
            password.text = ""
            self.can_change_screen = True

    # method used to sign in
    def sign_in(self):
        login_screen = self.root.ids["login_screen"]
        email = login_screen.ids["email_text"]
        password = login_screen.ids["password_text"]
        error_text = login_screen.ids["error_text"]

        auth = Authentication()
        ids = auth.sign_in(email.text, password.text)
        self.local_id = ids[0]

        if email.text == "" or password.text == "":
            error_text.text = "Missing Inputs"
            email.text = ""
            password.text = ""
        elif self.local_id in self.error_messages:
            if self.local_id == "EMAIL_NOT_FOUND":
                error_text.text = "Incorrect Inputs"
            else:
                error_text.text = process_error_message(self.local_id)
            email.text = ""
            password.text = ""
        else:
            database = Database.db
            error_text.text = ""
            email.text = ""
            password.text = ""
            home_page = ""
            id_token = ids[1]
            user_data = auth.get_user_data(id_token)
            email_verified = Authentication.check_email_verified(user_data)
            if email_verified:
                occupation = Database.get_occupation(database, self.local_id, "Occupation", "Users")
                if occupation == "Student":
                    home_page = "home_page_student"
                    #self.initial_settings("student")
                elif occupation == "Teacher":
                    home_page = "home_page_teacher"
                    #self.initial_settings("teacher")
                self.change_screen(home_page)
            else:
                error_text.text = "Email not Verified"

    # sends a email link to reset password
    def send_email_to_reset_password(self):
        email = self.forgot_password_popup.ids["email"]
        error_text = self.forgot_password_popup.ids["error_text"]
        auth = Authentication()
        request = auth.reset_password(email.text)
        data = json.loads(request.content.decode())

        if not request.ok:
            error_message = data["error"]["message"]
            error_message = process_error_message(error_message)
            error_text.text = error_message
        else:
            self.forgot_password_popup.clear_widgets()
            self.forgot_password_popup.add_widget(Label(text="A link has been sent your E-mail", size_hint=(1, 0.1),
                                                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                        font_name="Open Sans", font_size="16dp"))
        email.text = ""

    # show the properties of the elements
    def show_element_property(self):
        homepage_student = self.root.ids["search_element"]
        scroll_view_gridlayout = homepage_student.ids["searching_table"]  # the gridlayout
        search_text = homepage_student.ids["search_text"]  # the input box
        dictionary_of_elements = elements.get_elements()
        dict_of_symbols = elements.symbol_element_name_key_pair()
        scroll_view_gridlayout.clear_widgets()

        print(dictionary_of_elements)
        print(dict_of_symbols)
        # TODO make the information more viewable
        if search_text.text.capitalize() in dictionary_of_elements:
            element = dictionary_of_elements[search_text.text.capitalize()]
            for key, value in element.items():
                if key in ["source", "spectral_img", "xpos", "ypos", "shells", "summary", "ionization_energies",
                           "appearance", "electron_configuration"]:
                    continue
                if key == "density":
                    value = f"{value} g/L"
                if isinstance(value, str) and key != "discovered_by" and key != "named_by":
                    value = value.capitalize()
                scroll_view_gridlayout.add_widget(Label(text=str(process_message(key)), color=(0, 0, 0, 1)))
                scroll_view_gridlayout.add_widget(Label(text=str(value), color=(0, 0, 0, 1)))
        elif search_text.text.capitalize() in dict_of_symbols:
            element = dict_of_symbols[search_text.text.capitalize()]
            element_information = dictionary_of_elements[element]
            for key, value in element_information.items():
                if key in ["source", "spectral_img", "xpos", "ypos", "shells", "summary", "ionization_energies",
                           "appearance", "electron_configuration"]:
                    continue
                if isinstance(value, str) and key != "discovered_by" and key != "named_by":
                    value = value.capitalize()
                if key == "density":
                    value = f"{value} g/L"
                scroll_view_gridlayout.add_widget(Label(text=str(process_message(key)), color=(0, 0, 0, 1)))
                scroll_view_gridlayout.add_widget(Label(text=str(value), color=(0, 0, 0, 1)))
        elif search_text.text == "":
            pass
        else:
            scroll_view_gridlayout.add_widget(Label(text="Invalid Search",
                                                    font_name="Open Sans",
                                                    font_size="26dp",
                                                    color=(0, 0, 0, 1)))

    # calculate the molar mass
    def calculate_molar_mass(self):
        home_page_student = self.root.ids["molar_calculator"]
        scroll_calculation_text = home_page_student.ids["calculation_text"]
        chemical_formula_text = home_page_student.ids["chemical_formula_text"]
        molar_mass = elements.MolarMass(chemical_formula_text.text)
        if molar_mass.molar_mass <= 0:
            answer = f"Compound [b]{chemical_formula_text.text}[/b] is invalid"
            scroll_calculation_text.text = answer
        else:
            answer = f"[b]Compound[/b]: {molar_mass}\n[b]Element Frequency[/b]: \n"
            print(molar_mass)
            for element, frequency in molar_mass.element_frequencies.items():
                answer += f"{element}: {frequency} \n"
            answer += "\n[b]Relative Masses and Percent[/b]:\n"
            for element, information in molar_mass.element_composition.items():
                answer += f"[u]Total mass of {element}[/u]: {information[0]} g\n"
                answer += f"[u]Percent composition of {element}[/u]: " \
                          f"{round(information[1] * 100, 1)}%\n\n"
            answer += f"[b]Total mass[/b]: {molar_mass.molar_mass} g"
            scroll_calculation_text.text = answer + "\n\n\n"
            scroll_calculation_text.text += "[b]Calculations[/b]\n" + molar_mass.show_calculation()

    # calculate empirical or molecular formula base off of percent composition and abundance
    def calculate_formula(self):
        # TODO take in formula names and symbol
        home_page_screen = self.root.ids["calculate_formula"]
        element_list_text = home_page_screen.ids["element_list_text"]
        percent_list_text = home_page_screen.ids["percent_list_text"]
        mass = home_page_screen.ids["mass"]
        calculate_formula_scroll_view = home_page_screen.ids["calculate_formula_scroll_view"]
        calculate_formula_scroll_view.text = ""
        percentage_contains_string = False
        there_is_mass = False

        try:
            if isinstance(eval(mass), int) or isinstance(eval(mass), float):  # if the mass is actually a number
                there_is_mass = True
        except:
            there_is_mass = False

        element_list = element_list_text.text.replace(" ", "").split(",")
        init_percent_list = percent_list_text.text.replace(" ", "").split(",")
        term_percent_list = []
        if element_list_text.text == "" or percent_list_text.text == "":
            calculate_formula_scroll_view.text = "Missing Inputs"
        elif len(init_percent_list) > 0:
            for percent in init_percent_list:
                try:
                    if percent[-1] == "%":
                        percent = float(percent.strip("%")) / 100
                        term_percent_list.append(percent)
                    elif isinstance(eval(percent), float) or isinstance(eval(percent), int):
                        term_percent_list.append(eval(percent))
                    else:
                        calculate_formula_scroll_view.text = "Invalid Percentage Values."
                        break
                except:
                    percentage_contains_string = True
                    break
            if percentage_contains_string:
                calculate_formula_scroll_view.text = "Percentage Values contains characters."
            elif sum(term_percent_list) != 1:
                calculate_formula_scroll_view.text = "Given percentages does not add up to 100%."
            else:
                if there_is_mass:
                    percent_comp_obj = elements.PercentComp(element_list, term_percent_list, eval(mass))
                    empirical_formula = percent_comp_obj.empirical_formula_markup
                    molecular_formula = elements.MolarMass(percent_comp_obj.molecular_formula)
                    moles = percent_comp_obj.empirical_formula[1]
                    for element, mole in moles.items():
                        calculate_formula_scroll_view.text += f"The molecule contains {round(mole)} moles of {element}\n"
                    calculate_formula_scroll_view.text += f"The empirical formula would be: {empirical_formula}"
                    calculate_formula_scroll_view.text += f"The molecular formula would be: {molecular_formula}"
                else:
                    percent_comp_obj = elements.PercentComp(element_list, term_percent_list)
                    empirical_formula = percent_comp_obj.empirical_formula_markup
                    moles = percent_comp_obj.empirical_formula[1]
                    for element, mole in moles.items():
                        calculate_formula_scroll_view.text += f"The molecule contains {round(mole)} moles of {element}\n"
                    calculate_formula_scroll_view.text += f"The empirical formula would be: {empirical_formula}"
        else:
            calculate_formula_scroll_view.text = "No percentages are given."

    # balance a equation
    def balance_equation(self):
        homepage = self.root.ids["balancing_equations"]
        reactant_list = homepage.ids["reactant_list"].text
        product_list = homepage.ids["product_list"].text
        scroll_view_text = homepage.ids["balance_equation_scroll_view"]
        # Check if the entries are valid
        reactants = reactant_list.replace(" ", "").split(",")
        products = product_list.replace(" ", "").split(",")
        invalid = False
        for reactant in reactants:
            molar_mass = elements.MolarMass(reactant)
            if molar_mass.molar_mass <= 0:
                invalid = True
                break
        for product in products:
            if invalid:
                break
            else:
                molar_mass2 = elements.MolarMass(product)
                if molar_mass2.molar_mass <= 0:
                    invalid = True
                    break
        print(reactants, products)
        if reactants[0] == "" or products[0] == "":
            scroll_view_text.text = f"Missing Inputs"
        elif invalid:
            scroll_view_text.text = f"Invalid Input"
        else:
            balanced_equation = elements.EquationBalance(reactant_list, product_list)
            scroll_view_text.text = f"The balanced equation is {balanced_equation.balance_equation()}"

    # method to update user setting
    def initial_settings(self, occupation: str):
        homepage = self.root.ids["home_page_student"]
        if occupation == "student":
            name = homepage.ids["name"]
            dob = homepage.ids["DOB"]
            username = homepage.ids["username"]
            email = homepage.ids["email"]
            status = homepage.ids["status"]
            name.text = Database.get_occupation(Database.db, local_id=self.local_id, key="name", folder="Users")
            dob.text = Database.get_occupation(Database.db, local_id=self.local_id, key="Date of Birth", folder="Users")
            username.text = Database.get_occupation(Database.db, local_id=self.local_id, key="Username", folder="Users")
            email.text = Database.get_occupation(Database.db, local_id=self.local_id, key="Email", folder="Users")
            status.text = Database.get_occupation(Database.db, local_id=self.local_id, key="Occupation", folder="Users")
        elif occupation == "teacher":
            pass

    def sign_out(self):

        self.change_screen("login_screen")

if __name__ == "__main__":
    MainApp().run()
