# Selecciones Joins y General Update Pattern


En las secciones anteriores vimos, sin mucha atención al detalle, cómo crear una gráfica de 
barras utilizando D3.js. En este taller, vamos a analizar con detenimiento un par de conceptos que utilizamos, sin explicar 
en los talleres anteriores: las selecciones y la unión de los datos y los elementos del DOM. Además, 
vamos a introducir un concepto fundamental de D3.js, el _**G**eneral **U**pdate **P**attern_ (Patrón General de Actualización), 
que es la forma de actualizar los elementos de una página en función de los datos.


## Selecciones y Joins

Cuando creamos nuestra gráfica de barras utilizamos las selecciones de dos formas diferentes:

```javascript
var chart = d3.select(".chart");
var barras = chart.selectAll("div");
```

En el primer caso, seleccionamos un elemento existente, mientras que en el segundo caso seleccionamos 
los `div`s que queremos crear. Además hay otra diferencia, `d3.select()` contra `d3.selectAll()`, en el primer caso, 
esperamos que exista exactamente un elemento que coincida con nuestro selector, mientras que en el segundo caso, 
el número de elementos está, en principio, indeterminado. En ambos casos, el selector regresa un _grupo_ de elementos, es decir,
un objeto de la clase [selection](https://github.com/d3/d3-selection/blob/master/README.md#selection) que es una 
especie de _Array_ que implementa, adicionalmente, los métodos de D3.js.

Para entender todo esto un poco mejor, consideremos el siguiente HTML:

```html
<!DOCTYPE html>
<style>

.chart div {
  font: 10px sans-serif;
  background-color: steelblue;
  text-align: right;
  padding: 3px;
  margin: 1px;
  color: white;
}

</style>
<body>
  <div class="chart">
    <div style="width: 20px;" class="bar">2</div>
    <div style="width: 70px;" class="bar">7</div>
    <div style="width: 130px;" class="bar">13</div>
    <div style="width: 190px;" class="bar">19</div>
    <div style="width: 230px;" class="bar">23</div>
    <div style="width: 470px;" class="bar">47</div>
  </div>
  </body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
</html>

```
Vamos a ver cómo se comportan las selecciones en la consola de Javascript:

```javascript
b = d3.select("body");
b._groups;
b._groups[0];
```
Como pueden ver, la propiedad `_groups` de la selección es un `array` que contiene el elemento seleccionado. 
Ahora veamos cómo funciona `selectAll()`: 

```javascript
divs = d3.selectAll(".bar");
divs._groups;
divs._groups[0];
```
Ahora, como estamos seleccionando todos los `div`s de la clase `bar`, la selección nos regresa un arreglo de _grupos_ 
de elementos. Fíjense cómo el primer (y único) elemento de `divs._groups` es un `NodeList` (una lista de nodos del DOM) y,
para acceder a cada nodo (cada `div`, en este caso) necesitamos hacer `divs._groups[0][j]` 
(donde j es el índice del elemento en el array). Entonces, lo que está sucediendo es que los elementos de la selección 
quedan agrupados de acuerdo a su estructura en el DOM. Consideremos este caso un poco más complejo:

```html
<!DOCTYPE html>

</style>
<body>
<table style="width:100%">
  <tr>
    <th>Nombre</th>
    <th>Apellido</th> 
    <th>Edad</th>
  </tr>
  <tr>
    <td>Juan</td>
    <td>Nepomuceno</td> 
    <td>20</td>
  </tr>
  <tr>
    <td>Austreberto</td>
    <td>Martínez</td> 
    <td>14</td>
  </tr>
</table>
  </body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
</html>
```
Aquí tenemos una tabla con 3 filas (un encabezado y dos registros), vamos a ver qué sucede cuando seleccionamos 
las filas:

```javascript
filas = d3.selectAll("tr")
```
Como pueden ver, en la selección tenemos un solo grupo con 3 listas de nodos en su interior. Esto nos permite operar 
sobre cada una de esas listas (es decir, sobre las filas) pero, ¿Qué pása si quisiéramos operar sobre los datos 
("td") de la tabla?

```javascript
td = d3.selectAll("tr").selectAll("td")
```
Esta selección nos regresa tres grupos, uno para cada fila, como el primer grupo es el encabezado de la tabla, 
no contiene elementos, los otros dos grupos contienen, cada uno, la lista de nodos con los datos para cada celda de
la tabla.






