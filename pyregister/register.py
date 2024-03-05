# Importações
import os
import csv
from time import sleep

import pyautogui


# Limpa o terminal
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Captura as coordenadas do campo desejado
class UserInteraction:
    def aler_user(self, message):
        print(message)

    def get_coordinates(self, name):
        self.aler_user("Você tem 3 segundos pra marcar o ponto desejado...")
        sleep(3)

        x, y = pyautogui.position()
        self.aler_user(f"{name}: Cordernadas {x}, {y} registradas.")
        return x, y


class Registrar:
    def __init__(self, input_file, margin, wait_time, max_iterations=None):
        self.input_file = input_file
        self.margin = margin
        self.wait_time = wait_time
        self.max_iterations = max_iterations

        # Segurança contra falhas (delay de resposta)
        self.mouse_speed = 0.5
        pyautogui.FAILSAFE = True

        # DADOS ESPECÍFICOS DESSE FLUXO!!!
        self.DADOS_FISCAIS = [706, 307]
        self.SAVE = [562, 209]
        COLUMNS = ["nome", "valor", "margin", "cst", "taxa", "ncm"]
        self.user_interaction = UserInteraction()


        # Estrutura dos valores
        self.FIELDS = []

        # Armazena as coordenadas do field e valores do produto na estrutura
        for col in COLUMNS:
            coordinates = self.user_interaction.get_coordinates(col)
            self.FIELDS.append({ "axis": coordinates, "info": col })


    def register_product(self, product):
        print(f'''
            -------------------------------------------------
                    {product}
            -------------------------------------------------
            ''')
        
        for field in self.FIELDS:
            # Move o mouse para os campos escolhidos
            x = field["axis"][0]
            y = field["axis"][1]
            sleep(self.wait_time)
            pyautogui.moveTo(x, y, duration=self.mouse_speed)
            sleep(self.wait_time)

            # Double click
            print("click 2x")
            for i in range(0, 2):
                pyautogui.click()
            sleep(self.wait_time)

            # Escreve o self.margin
            if field["info"] == "margin":
                pyautogui.write(self.margin)
                print(f"maigin: {self.margin}")
                continue

            # Escreve os valores
            key = field["info"]
            pyautogui.write(product[key].replace('.', ','))
            print(f"{ field['info'] }: { product[field['info']] }")

            sleep(self.wait_time)
            pyautogui.moveTo(*self.SAVE, duration=self.mouse_speed)
            # print("save")

        print("----------------------------")

    def run(self):
        # Lê csv
        print("Abrindo arquivo...")
        try:
            with open(self.input_file, "r", encoding="utf-8") as file:
                products = list(csv.DictReader(file))
        except Exception as error:
             print(f"Ocorreu um erro ao abrir o arquivo CSV {self.input_file} para leitura: {error}")

        # Alerta 
        pyautogui.alert("ATENÇÃO!!: Não use mouse e tecla, pode atrapalhar o funcionamento.\nO RPA vai ser executado.")

        # Prepara o ambiente
        pyautogui.moveTo(*self.SAVE, duration=self.mouse_speed)
        pyautogui.click()
        sleep(self.wait_time)

        pyautogui.moveTo(*self.DADOS_FISCAIS, duration=self.mouse_speed)
        pyautogui.click()
        sleep(self.wait_time)


        # Cadastra cada produto
        count_iteration = 0
        for product in products:
            self.register_product(product)

            count_iteration += 1
            if self.max_iterations is not None and count_iteration == self.max_iterations:
                break