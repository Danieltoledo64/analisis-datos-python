#Crear programa que analice datos ingresados por el usuario
#Y retorne el orden y promedio de los datos ingresados con todas las validaciones necesarias y 
#guardar los resultados en un archivo de texto.
#Autor: Daniel Toledo
#Fecha: 20-07-2025
# analisis1.py
from datetime import datetime
import pandas as pd
import re
#VALIDACIONES PARA INGRESO DE DATOS (GENERALILZACIÓN)
def pedir_datos():
    while True:
        datos = input('Ingrese hasta 5 números entre 0 y 100, separados por espacios: ')
        valores = [v for v in datos.split() if v.strip() != '']

        if not valores:
            print('Debe ingresar al menos un número.')
            continue
        if len(valores) > 5:
            print('¡Error! Solo puede ingresar hasta 5 números.')
            continue
        try:
            lista = [float(x) for x in valores]
        except ValueError:
            print('Todos los datos deben ser números.')
            continue
        if any(x < 0 or x > 100 for x in lista):
            print('Todos los números deben estar entre 0 y 100.')
            continue
        if len(lista) != len(set(lista)):
            print('No se permiten números repetidos.')
            continue

        return lista

def guardar_resultado(tipo, datos, resultado=None):
    momento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('resultados.txt', 'a', encoding='utf-8') as f:
        f.write('='*30 + '\n')
        f.write(f' Fecha y hora: {momento}\n')
        f.write(f' Tipo de análisis: {tipo}\n')
        f.write(f' Datos: {[f"{x:.2f}" for x in datos]}\n')
        if resultado is not None:
            if isinstance(resultado, (int, float)):
                f.write(f' Resultado: {resultado:.2f}\n')
            else:
                f.write(f' Resultado: {resultado}\n')
        f.write('='*30 + '\n\n')

#DEFINICIONES DEL MENU PRINCIPAl
def orden():
    print('\n--- Ordenar Datos ---')
    lista = pedir_datos()
    while True:
        orden_tipo = input('¿Orden ascendente (A) o descendente (D)? ').upper()
        if orden_tipo in ['A', 'D']:
            break
        print('Opción no válida. Ingrese "A" para ascendente o "D" para descendente.')
    if orden_tipo == 'D':
        lista.sort(reverse=True)
    else:
        lista.sort()
    print(f'Datos ordenados: {lista}\n')
    guardar_resultado('Ordenar', lista)

def prom():
    print('\n--- Promedio de Datos ---')
    lista = pedir_datos()
    promedio = sum(lista) / len(lista)
    print(f'El promedio es: {promedio:.2f}\n')
    guardar_resultado('Promedio',lista, promedio)

def ver_historial():
    print('\n--- Historial de Resultados ---')
    try:
        with open('resultados.txt', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if contenido:
                print(contenido)
            else:
                print('No hay resultados guardados aún.')
    except FileNotFoundError:
        print('No hay resultados guardados aún.')
    print('')

def borrar_historial():
    with open('resultados.txt', 'w', encoding='utf-8') as f:
        pass
    print('Historial borrado exitosamente.\n')

# --- NUEVO: Análisis estadístico en Excel ---
def generar_analisis_excel():
    print('\n--- Generar análisis estadístico en Excel ---')
    try:
        with open('resultados.txt', 'r', encoding='utf-8') as f:
            contenido = f.read()
        # Extraer listas de datos usando regex
        datos = re.findall(r"Datos: \[(.*?)\]", contenido)
        todas_las_listas = []
        for grupo in datos:
            # Quitar comillas y espacios, convertir a float
            nums = [float(x.replace('"','').replace("'",'')) for x in grupo.split(',') if x.strip()]
            if nums:
                todas_las_listas.append(nums)
        if not todas_las_listas:
            print('No hay datos para analizar.')
            return
        # Unir todos los datos en una sola lista
        flat_list = [item for sublist in todas_las_listas for item in sublist]
        df = pd.DataFrame(flat_list, columns=['Datos'])
        # Calcular estadísticas
        estadisticas = {
            'Promedio': df['Datos'].mean(),
            'Mediana': df['Datos'].median(),
            'Desviación estándar': df['Datos'].std(),
            'Máximo': df['Datos'].max(),
            'Mínimo': df['Datos'].min(),
            'Cantidad de datos': len(df)
        }
        # Guardar datos y estadísticas en Excel
        with pd.ExcelWriter('analisis_estadistico.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
            estad_df = pd.DataFrame(list(estadisticas.items()), columns=['Estadística','Valor'])
            estad_df.to_excel(writer, index=False, sheet_name='Estadísticas')
        print('Análisis estadístico guardado en analisis_estadistico.xlsx\n')
    except Exception as e:
        print(f'Error al generar el análisis: {e}\n')


while True:
    print('-- Menú Principal --')
    print('1. Ordenar datos')
    print('2. Calcular promedio')
    print('3. Ver historial de resultados')
    print('4. Borrar historial')
    print('5. Generar análisis estadístico en Excel')
    print('6. Salir del programa')

    try:
        opcion = int(input('Ingrese una opción: '))
        if opcion == 1:
            orden()
        elif opcion == 2:
            prom()
        elif opcion == 3:
            ver_historial()
        elif opcion == 4:
            borrar_historial()
        elif opcion == 5:
            generar_analisis_excel()
        elif opcion == 6: 
            print('Saliendo del programa...')
            break   
        else:
            print('Opción no válida, intente de nuevo.\n')
    except ValueError:
        print('Por favor, ingrese un número válido.\n')
    except KeyboardInterrupt:
        print('\nSaliendo del programa...')
        break
    except Exception as e:
        print(f'Ocurrió un error: {e}\n')

print('Gracias por usar el programa.')
    
        
    
    

            
