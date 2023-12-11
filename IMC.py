import PySimpleGUI as sg
import mysql.connector

def conectar_bd():
    dados_bd = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'imc'
    }

    conexao = mysql.connector.connect(**dados_bd)
    return conexao

def calcular_imc(altura, peso):
    try:
        return float(peso) / (float(altura) ** 2)
    except ValueError:
        return None

def categorizar_imc(imc):
    if imc is None:
        return None

    if imc < 18.5:
        return 'Baixo peso'
    elif 18.5 <= imc <= 24.9:
        return 'Peso normal'
    elif 25.0 <= imc <= 29.9:
        return 'Sobrepeso'
    elif 30.0 <= imc <= 34.9:
        return 'Obesidade Grau 1'
    elif 35.0 <= imc <= 39.9:
        return 'Obesidade Grau 2'
    elif imc >= 40.0:
        return 'Obesidade Grau 3'
    else:
        return None

def inserir_registro(nome, endereco, altura, peso, imc, categoria_imc):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    # Inserir dados na tabela do banco de dados
    query = "INSERT INTO registros (nome, endereco, altura, peso, imc, categoria_imc) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (nome, endereco, altura, peso, imc, categoria_imc)
    cursor.execute(query, valores)

    # Commit e fechar conexão
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_tela():
    sg.theme('DarkTeal12')
    layout = [
        [sg.Text('Nome Completo:', size=(15, 1)), sg.InputText(key='nome')],
        [sg.Text('Endereço:', size=(15, 1)), sg.InputText(key='endereco')],
        [sg.Text('Altura (cm):', size=(15, 1)), sg.InputText(key='altura')],
        [sg.Text('Peso (kg):', size=(15, 1)), sg.InputText(key='peso')],
        [
            sg.Button('Calcular', button_color=('white', 'grey')),
            sg.Button('Reiniciar', button_color=('white', 'green')),
            sg.Button('Sair', button_color=('white', 'red'))
        ],
    ]

    janela = sg.Window('Calculadora de IMC', layout, resizable=False)

    while True:
        evento, valores = janela.read()

        if evento == sg.WINDOW_CLOSED or evento == 'Sair':
            break
        elif evento == 'Calcular':
            nome, endereco, altura, peso = valores['nome'], valores['endereco'], valores['altura'], valores['peso']

            if nome and endereco and altura and peso:
                imc = calcular_imc(altura, peso)
                categoria_imc = categorizar_imc(imc)

                if imc is not None:
                    # Mostrar resultados na janela
                    layout_resultado = [
                        [sg.Text(f'Nome: {nome}')],
                        [sg.Text(f'Endereço: {endereco}')],
                        [sg.Text(f'Altura: {altura} cm')],
                        [sg.Text(f'Peso: {peso} kg')],
                        [sg.Text(f'IMC Calculado: {imc:.2f}')],
                        [sg.Text(f'Referência'), sg.Text(categoria_imc, text_color='yellow') if categoria_imc else sg.Text('')],
                    ]

                    janela_resultado = sg.Window('Resultado', layout_resultado, resizable=False, size=(500, 200))

                    evento_resultado, _ = janela_resultado.read()

                    if evento_resultado == sg.WINDOW_CLOSED or evento_resultado == 'OK':
                        janela_resultado.close()

                    # Inserir registro no banco de dados
                    inserir_registro(nome, endereco, altura, peso, imc, categoria_imc)

                else:
                    sg.popup_error("Por favor, insira valores válidos para Altura e Peso.")

        elif evento == 'Reiniciar':
            janela['nome'].update('')
            janela['endereco'].update('')
            janela['altura'].update('')
            janela['peso'].update('')

    janela.close()

criar_tela()
