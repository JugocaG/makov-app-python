import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, geom, binom

# Función para cargar parámetros desde un archivo
def cargar_parametros_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        parametros = {}
        for linea in lineas:
            clave, valor = linea.strip().split('=')
            try:
                if '.' in valor:
                    parametros[clave] = float(valor)
                else:
                    parametros[clave] = int(valor)
            except ValueError:
                parametros[clave] = valor
    return parametros

configuracion = cargar_parametros_archivo('data.txt')

# Extraer valores del archivo de configuración
tipo_distribucion = configuracion.get('distribucion')
valor_lambda = configuracion.get('lambda')
cantidad_eventos = configuracion.get('n', 10)
prob_exito = configuracion.get('p', 0.5)
min_cantidad_pedir = configuracion.get('valor_minimo_pedir')
max_cantidad_pedir = configuracion.get('valor_maximo_pedir')
min_punto_reorden = configuracion.get('valor_minimo_reorden')
max_punto_reorden = configuracion.get('valor_maximo_reorden')
costo_orden = configuracion.get('costo_orden')
costo_mantenimiento = configuracion.get('costo_mantenimiento')
costo_faltante = configuracion.get('costo_faltante')

# Generar probabilidades según la distribución especificada
if tipo_distribucion == 'Poisson':
    demanda = np.arange(0, cantidad_eventos)
    probabilidades_demanda = poisson.pmf(demanda, valor_lambda)
elif tipo_distribucion == 'Geometrica':
    demanda = np.arange(0, cantidad_eventos)
    probabilidades_demanda = geom.pmf(demanda, prob_exito)
elif tipo_distribucion == 'Binomial':
    demanda = np.arange(0, cantidad_eventos)
    probabilidades_demanda = binom.pmf(demanda, cantidad_eventos, prob_exito)
elif tipo_distribucion == 'Empirica':
    def cargar_datos_empiricos(nombre_archivo):
        datos = np.loadtxt(nombre_archivo, delimiter=',', skiprows=1)
        demanda = datos[:, 0]
        probabilidades_demanda = datos[:, 1]
        return demanda, probabilidades_demanda
    
    demanda, probabilidades_demanda = cargar_datos_empiricos('empirica.txt')
    cantidad_eventos = len(demanda)
else:
    raise ValueError("Distribución no reconocida")

distribucion_demanda = np.array([demanda, probabilidades_demanda], dtype=object)

def calcular_costo_mantenimiento(costo_unidad, distribucion):
    costos_mant = []
    for i in distribucion[0]:
        costos_mant.append(costo_unidad * i)
    return costos_mant

def calcular_costo_orden(fijo, nivel_reorden, distribucion):
    costos_orden = np.zeros(len(distribucion[0]))
    for i in range(nivel_reorden + 1):
        costos_orden[i] = fijo
    return costos_orden

faltantes_esperados = []
def costo_faltante_por_estado(estado_actual, distribucion, costo_faltante):
    total_faltante = 0
    probabilidades = distribucion[1]
    for demanda in range(estado_actual + 1, len(distribucion[0])):
        faltante = demanda - estado_actual
        total_faltante += probabilidades[demanda] * faltante
        faltantes_esperados.append(total_faltante)
    return round(costo_faltante * total_faltante, 4)

def calcular_costo_total_faltante(costo_faltante, distribucion):
    costos_faltante = []
    for estado in range(len(distribucion[0])):
        costo = costo_faltante_por_estado(estado, distribucion, costo_faltante)
        costos_faltante.append(costo)
    return costos_faltante

# Calcular los costos totales combinando los tres tipos de costos
def calcular_costos_totales(costo_mant, costo_orden, costo_faltante, distribucion, nivel_reorden):
    costos_mant = calcular_costo_mantenimiento(costo_mant, distribucion)
    costos_orden = calcular_costo_orden(costo_orden, nivel_reorden, distribucion)
    costos_faltante = calcular_costo_total_faltante(costo_faltante, distribucion)
    return costos_mant, costos_orden, costos_faltante

def generar_combinaciones_pedido(max_pedido, min_pedido, max_reorden, min_reorden):
    cantidades_pedido = list(range(min_pedido, max_pedido + 1))
    puntos_reorden = list(range(min_reorden, max_reorden + 1))
    return cantidades_pedido, puntos_reorden

def calcular_probabilidades_estacionarias(matriz):
    for i in range(len(matriz)):
        matriz[i, i] -= 1
    for i in range(len(matriz)):
        matriz[i, 0] = 1
    vector_cero = np.zeros(len(matriz))
    vector_cero[0] = 1
    probabilidades_estacionarias = np.linalg.inv(matriz.T).dot(vector_cero)
    return probabilidades_estacionarias

def calcular_matriz_transicion(max_pedido, min_pedido, max_reorden, min_reorden, distribucion, num_estados, costo_mant, costo_orden, costo_faltante):
    cantidades_pedido, puntos_reorden = generar_combinaciones_pedido(max_pedido, min_pedido, max_reorden, min_reorden)
    
    num_estados = min(num_estados, len(distribucion[0]))
    
    estados_demanda = distribucion[0][:num_estados]
    prob_estados = distribucion[1][:num_estados]
    n_estados = len(estados_demanda)
    
    matriz_transicion = np.zeros((n_estados, n_estados))
    for i in range(n_estados):
        for j in range(n_estados):
            if i <= j:
                prob = prob_estados[j - i]
                matriz_transicion[j, i] = prob

    for i in range(matriz_transicion.shape[0]):
        suma_columna = np.sum(matriz_transicion[i, 1:])
        matriz_transicion[i, 0] = 1 - suma_columna

    resultados = []

    for nivel_reorden in puntos_reorden:
        for cantidad in cantidades_pedido:
            matriz_temp = matriz_transicion.copy()
            max_estado = min(cantidad + nivel_reorden, matriz_transicion.shape[0] - 1)
            matriz_temp[:nivel_reorden + 1, :] = matriz_temp[max_estado, :]
            probabilidades_estacionarias = calcular_probabilidades_estacionarias(matriz_temp)

            costos_mant, costos_orden, costos_faltante = calcular_costos_totales(costo_mantenimiento, costo_orden, costo_faltante, distribucion, nivel_reorden)
            costos_mant = costos_mant[:num_estados]
            costos_orden = costos_orden[:num_estados]
            costos_faltante = costos_faltante[:num_estados]

            for x in range(nivel_reorden + 1):
                costos_faltante[x] = costos_faltante[max_estado]

            costos_totales = [costos_mant[i] + costos_orden[i] + costos_faltante[i] for i in range(num_estados)]
            costo_esperado = np.dot(probabilidades_estacionarias, costos_totales)

            # Imprimir el costo esperado
            print(f"Cantidad: {cantidad}, Nivel de Reorden: {nivel_reorden}, Costo Esperado: {costo_esperado:.2f}")

            resultados.append({
                'cantidad_pedido': cantidad,
                'nivel_reorden': nivel_reorden,
                'costo_esperado': costo_esperado,
                'probabilidad_estacionaria': probabilidades_estacionarias.sum()
            })

    return resultados

def graficar_resultados(combinaciones):
    cantidades_pedido = [c['cantidad_pedido'] for c in combinaciones]
    niveles_reorden = [c['nivel_reorden'] for c in combinaciones]
    costos_totales = [c['costo_esperado'] * c['probabilidad_estacionaria'] for c in combinaciones]

    plt.figure(figsize=(10, 6))
    grafico_dispersion = plt.scatter(cantidades_pedido, niveles_reorden, c=costos_totales, cmap='plasma', s=100)
    plt.colorbar(grafico_dispersion, label='Costo Total Esperado')
    plt.xlabel('Cantidad de Pedido')
    plt.ylabel('Nivel de Reorden')
    plt.title('Cantidad de Pedido vs Nivel de Reorden vs Costo Total Esperado')
    plt.show()

combinaciones_politicas_inventario = calcular_matriz_transicion(max_cantidad_pedir, min_cantidad_pedir, max_punto_reorden, min_punto_reorden, distribucion_demanda, 20, costo_mantenimiento, costo_orden, costo_faltante)

graficar_resultados(combinaciones_politicas_inventario)
