# Importações
import pyautogui
import pandas as pd
import tabula
import csv
from time import sleep
import os

# Limpa o terminal
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# Captura as coordenadas desejadas
class UserInteraction:
    def aler_user(self, message):
        print(message)

    def get_coordinates(self):
        self.aler_user("Você tem 3 segundos pra marcar o ponto desejado...")
        sleep(3)

        x, y = pyautogui.position()
        self.aler_user(f"Cordernadas {x}, {y} registradas.")
        clear_screen()
        return x, y


class Registrar:
    def __init__(self, data_file, margin, wait_time, max_iterations=None):
        self.data_file = data_file
        self.margin = margin
        self.wait_time = wait_time
        self.max_iterations = max_iterations
        self.mouse_speed = 0.5
        pyautogui.FAILSAFE = True

        # Cria o arquivo de entrada e saída
        self.data_frame = pd.DataFrame()
        self.output_file = "output.csv"


        # DADOS ESPECÍFICOS DESSE FLUXO!!!
        self.DADOS_FISCAIS = [706, 307]
        self.SAVE_POSITION = [562, 209]
        NAMES = ["Unnamed: 0", "VALOR", self.margin, "500", "0,19", "Unnamed: 1"]
        self.user_interaction = UserInteraction()


        # Estrutura que guarda os valores
        self.VALUES = []

        # Armazena as informações na estrutura ser usada no cadastro
        for name in NAMES:
            coordinates = self.user_interaction.get_coordinates()
            self.VALUES.append( {"axis": coordinates, "info": name})


    def register_product(self, product):
        print(f'''
            ---------------------------------
                    {product}
            ---------------------------------
            ''')
        
        for value in self.VALUES:
            sleep(self.wait_time)
            pyautogui.moveTo(value["axis"][0], value["axis"][1], duration=self.mouse_speed)
            sleep(self.wait_time)

            print("click 2x")
            for i in range(0, 2):
                pyautogui.click()
            sleep(self.wait_time)

            if value["info"] in product:
                pyautogui.write(product[value["info"]])
                print(product[value["info"]])
                continue

            pyautogui.write(value["info"])
            print(value["info"])

            sleep(self.wait_time)
            pyautogui.moveTo(*self.SAVE_POSITION, duration=self.mouse_speed)
            # print("save")

        print("----------------------------")

    def run(self):
        # Lê pdf
        print("Lendo arquivo...")
        try:
            pdf = tabula.read_pdf(self.data_file, pages="all", multiple_tables=True)
        except Exception as error:
            print(
            f"Ocorreu um erro durante a leitura do PDF {self.data_file}: {error}"
        )

        # Trata o data frame
        for table in pdf:
            if "CÓDIGO DO" in table:
                self.data_frame = pd.concat([self.data_frame, table], ignore_index=True)

        self.data_frame = self.data_frame[self.data_frame["VALOR"] != "UNITÁRIO"]
        self.data_frame = self.data_frame.astype(object)

        # Salva o csv
        print("Salvando arquivo...")
        try:
            self.data_frame.to_csv(self.output_file, index=False)
        except Exception as error:
            print(f"Ocorreu um erro ao salvar o DataFrame em {self.data_file}: {error}")

        # -----------------------> RPA <---------------------
            
        # Lê csv
        print("Abrindo arquivo...")
        try:
            with open(self.output_file, "r", encoding="utf-8") as file:
                products = list(csv.DictReader(file))
        except Exception as error:
             print(f"Ocorreu um erro ao abrir o arquivo CSV {self.data_file} para leitura: {error}")

        # Alerta 
        pyautogui.alert("ATENÇÃO!!: Não use mouse e tecla, pode atralhar o funcionamento.\nO RPA vai ser executado.")

        # Prepara o ambiente
        pyautogui.moveTo(*self.SAVE_POSITION, duration=self.mouse_speed)
        pyautogui.click()
        sleep(self.wait_time)
        pyautogui.moveTo(*self.DADOS_FISCAIS, duration=self.mouse_speed)
        pyautogui.click()
        sleep(self.wait_time)

        count_iteration = 0
        for product in products:
            self.register_product(product)

            count_iteration += 1
            if self.max_iterations is not None and count_iteration == self.max_iterations:
                break