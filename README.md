# Simulación de Políticas de Inventario

### Mariana Chacon Casallas

### Juan David Gomez Calderon

### Sebastian Andres Guerra Rodriguez

### Juan Pablo Mateus Pardo

Este programa simula políticas de inventario utilizando diferentes distribuciones de demanda (Poisson, Geométrica, Binomial o Empírica). Calcula los costos totales esperados para diferentes combinaciones de cantidad de pedido y nivel de reorden, generando gráficos que muestran el costo total esperado.

## Requisitos

1. **Python 3.x**
2. Librerías necesarias:
   - `numpy`
   - `matplotlib`
   - `scipy`

Puedes instalar las dependencias utilizando `pip`:

```bash
pip install numpy matplotlib scipy
```

## Archivos de Configuración

### 1. **Archivo de parámetros (`data.txt`)**

Este archivo contiene los parámetros de la simulación, como el tipo de distribución de la demanda, el número de eventos, los costos asociados, entre otros.

El formato es clave=valor, y cada parámetro debe estar en una nueva línea.

#### Ejemplo de `data.txt`:

```
distribucion=Poisson
lambda=4.5
n=10
p=0.5
valor_minimo_pedir=10
valor_maximo_pedir=50
valor_minimo_reorden=5
valor_maximo_reorden=20
costo_orden=50
costo_mantenimiento=2.5
costo_faltante=10
```

#### Parámetros:

- `distribucion`: Define la distribución de la demanda. Puede ser `Poisson`, `Geometrica`, `Binomial` o `Empirica`.
- `lambda`: Parámetro de la distribución Poisson.
- `n`: Número de eventos (usado para definir el rango de la demanda).
- `p`: Probabilidad de éxito (usado en las distribuciones Geométrica y Binomial).
- `valor_minimo_pedir` y `valor_maximo_pedir`: Rango de las cantidades de pedido que se evaluarán.
- `valor_minimo_reorden` y `valor_maximo_reorden`: Rango de los niveles de reorden que se evaluarán.
- `costo_orden`: Costo fijo de hacer un pedido.
- `costo_mantenimiento`: Costo de mantener una unidad de inventario.
- `costo_faltante`: Costo de faltante por cada unidad no disponible.

### 2. **Archivo de demanda empírica (`empirica.txt`)**

Si eliges `Empirica` como distribución de demanda, este archivo deberá contener los datos empíricos. El formato debe ser un archivo de texto con dos columnas: la primera columna es el valor de la demanda y la segunda es la probabilidad asociada.

#### Ejemplo de `empirica.txt`:

```
0, 0.1
1, 0.2
2, 0.4
3, 0.2
4, 0.1
```

#### Notas:

- La suma de todas las probabilidades debe ser igual a 1.
- Asegúrate de que los valores de demanda estén en la primera columna y las probabilidades en la segunda.

## Uso

1. Asegúrate de tener el archivo de parámetros `data.txt` y, si es necesario, el archivo de datos empíricos `empirica.txt` en el mismo directorio que el programa.

2. Ejecuta el programa con Python:

```bash
python inventario.py
```

3. El programa mostrará el costo total esperado para cada combinación de cantidad de pedido y nivel de reorden, y generará un gráfico que visualiza estas combinaciones en función del costo esperado.

## Resultados

El programa imprimirá en la consola las combinaciones de políticas de inventario (cantidad de pedido y nivel de reorden) junto con el costo total esperado para cada combinación:

```
Cantidad: 10, Nivel de Reorden: 5, Costo Esperado: 235.50
Cantidad: 10, Nivel de Reorden: 6, Costo Esperado: 240.75
...
```

Al finalizar, se generará un gráfico donde los ejes representan la cantidad de pedido y el nivel de reorden, y el color indica el costo total esperado.

## Personalización

Puedes ajustar los parámetros del archivo `data.txt` para simular diferentes situaciones de demanda, costos y políticas de inventario. Además, puedes crear tus propios archivos de datos empíricos si deseas utilizar datos reales de demanda.

## Ejemplo Visual del Gráfico

El gráfico generado por el programa muestra las combinaciones de políticas de inventario evaluadas. A medida que varían la cantidad de pedido y el nivel de reorden, los colores representan el costo total esperado, permitiéndote identificar las combinaciones más eficientes.

---
