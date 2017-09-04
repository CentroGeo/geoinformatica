# Selecciones, Joins y General Update Pattern


En las secciones anteriores vimos, sin mucha atención al detalle, cómo crear una gráfica de 
barras utilizando D3.js. En este taller, vamos a analizar con detenimiento un par de conceptos que utilizamos, sin explicar, 
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
Como estamos seleccionando todos los `div`s de la clase `bar`, la selección nos regresa un arreglo de _grupos_ 
de elementos. Fíjense cómo el primer (y único) elemento de `divs._groups` es un `NodeList` (una lista de nodos del DOM) y,
para acceder a cada nodo (cada `div`, en este caso) necesitamos hacer `divs._groups[0][j]` 
(donde j es el índice del elemento en el array). Entonces, lo que está sucediendo es que los elementos de la selección 
quedan agrupados de acuerdo a su estructura en el DOM. Consideremos un caso más complejo:

```html
<!DOCTYPE html>
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
Esta selección nos regresa tres grupos, uno para cada fila. Como el primer grupo es el encabezado de la tabla, 
no contiene elementos, los otros dos grupos contienen, cada uno, la lista de nodos con los datos para cada celda de
la tabla.

En conclusión, las selecciones **siempre** regresan grupos y estos grupos mantienen la esructura lógica del DOM. 

Ahora vamos a ver cómo funciona esto cuando lo empezamos a ligar con datos, empecemos con el siguiente HTML que contiene un svg con tres círculos:

```html
<!DOCTYPE html>
<body>
  <svg width="720" height="120">
    <circle cx="40" cy="60" r="10"></circle>
    <circle cx="80" cy="60" r="10"></circle>
    <circle cx="120" cy="60" r="10"></circle>
  </svg>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
</html>
```
Como ya vimos, es fácil cambiar sus propiedades con D3.js:

```javascript
var circle = d3.selectAll("circle");
circle.style("fill", "steelblue");
circle.attr("r", 30);
```
En el taller anterior, vimos que podemos cambiar los atributos de acuerdo al resultado de una función:

```javascript
circle.attr("cx", function() { return Math.random() * 720; });
```
Ahora vamos a unir unos datos a nuestros círculos y cambiar el tamaño de acuerdo a los datos:

```javascript
datos = [32, 57, 112];
circle.data(datos);
circle.attr("r", function(d) { return Math.sqrt(d); });
```

Aquí es donde la _magia_ de D3 se empieza a notar: cuando hacemos `circle.data(datos)`, estamos ligando cada uno de los circulos con un valor del arreglo de datos (el `datum` de cada círculo), entonces, cuando le damos valor al atributo "r" la función se ejecuta una vez por cada elemento que tenga un dato ligado: es un `for` implícito.

En este ejemplo tenemos el mismo número de círculos que elementos en el arreglo de datos, pero ¿qué pasaría si tuviéramos más datos que círculos? Aquí es donde entra la selección `enter`. Antes de continuar, recarga la página de forma que tengas los tres círculos negros con los que empezamos.

```javascript
datos = [32, 57, 112, 33];
var svg = d3.select("svg");
var circle = svg.selectAll("circle").data(datos)
var circleEnter = circle.enter().append("circle");
```
Como pueden ver, `circleEnter` contiene un grupo con un elemento: ¡el círculo que no existe en nuestro dibujo! Vamos a pintarlo:


```javascript
circleEnter.attr("cy", 60);
circleEnter.attr("cx", function(d, i) { return i * 100 + 30; });
circleEnter.attr("r", function(d) { return Math.sqrt(d); });
```

Fíjense en la linea `circleEnter.attr("cx", function(d, i) { return i * 100 + 30; })`, ahí estamos diciendo que, para cada elemento de la selección `enter` la coordenada `x` se recorra a la derecha una cantidad de unidades que depende del índice `i` del elemento. Intenten ahora ligar un arreglo de datos con más de cuatro elementos.

Hasta aquí vimos el caso en el que tenemos más datos que elementos en el DOM, pero en general, cuando unimos un nuevo conjunto de datos a una selección vamos a tener grupos:

<img src="https://centrogeo.github.io/geoinformatica/d3/enter_update_exit.svg"/>

En el centro del diagrama tenemos la selección `update`: los datos que ya están unidos a elementos del DOM, del lado izquierdo los datos que todavía no tienen elemento creado (`enter`) y del lado derecho están los elementos que ya no quedan unidos a ningún elemento del DOM, la selección `exit`. Estos son los tres elementos que permiten la actualización dinámica de las gráficas en D3.

## General Update Pattern

El Patrón General de Actualización (GUP) es, junto con la unión de datos, la base de D3.js. Es a través del GUP como se implementa la dinámica de las visualizaciones: reaccionar a nuevos datos, input del usuario, etcétera.

En la sección anterior vimos cómo se puede ligar un conjunto de datos a una selección y cómo, cuando no tenemos elementos para acomodarlos, nuestros datos quedan ligados en una selección especial llamada `enter`. También comenzamos a ver lo que sucede cuando _actualizamos_ los datos de una selección y describimos los tres casos posibles: `enter`, `update` y `exit`. Ahora, vamos a trabajar con un caso sencillo pero que explícitamente maneja las tres selecciones.

Vamos a comenzar con un HTML que contiene únicamente un `div` donde vamos a albergar nustra _gráfica_:

```html
<!DOCTYPE html>
<body>
  <div id="contenedor"></div>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
</html>
```

Ahora, vamos a crear un svg adentro de nuestro contenedor, agregar elementos al svg y ligarlos a un conjunto de datos:

```javascript
datos = [{"x": 25, "y": 25}, {"x": 80, "y": 25}, {"x": 150, "y": 25}];
contenedor = d3.select("#contenedor");
svg = contenedor.append("svg")
      .attr("width", 500)
      .attr("height", 500);
circulos = svg.selectAll("circle")
     .data(datos);
circulos.enter().append("circle")
  .attr("r", 15)
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; });
```

Ahora, suopngamos que _nos llega_ una actualización de los datos y, en consecuencia, necesitamos actualizar el dibujo:


```javascript
datos2 = [{"x": 25, "y": 50}, {"x": 80, "y": 50}, {"x": 150, "y": 50}, {"x": 250, "y": 25}];
circulos = svg.selectAll("circle")
     .data(datos2)
     .attr("fill","red")
     .attr("cy", function(d) { return d.y; });

circulos.enter().append("circle")
    .attr("r", 15)
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .attr("fill","steelblue")
  .merge(circulos)
    .attr("stroke", "black")
    .attr("stroke-width", "10")
```
En este caso, la selección `enter` (los elementos nuevos) está coloreada de azul, mientras que la selección  `update` (los elementos que ya existían), está coloreada de rojo. Fíjense como, al final, usamos la selección `merge` para modificar el estilo de la unión de las selecciónes `enter` y `update`.

Resumiendo, cuando actualizamos los datos `circulos.data(datos2)` nos regresa la selección `update` para que operemos sobre ella. Después podemos trabajar sobre `enter` y, al final, si queremos hacer algo sobre _todos_ los elementos que quedaron en el DOM, podemos usar la selección `merge`.

Pero ¿qué pasa si los nuevos datos tienen menos elementos que los que ya tengo en el DOM?

```javascript
datos3 = [{"x": 25, "y": 100}];
circulos = svg.selectAll("circle")
     .data(datos3)
     .attr("cy", function(d) { return d.y; })
     .attr("fill", "green");

circulos.enter().append("circle")
    .attr("r", 15)
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .attr("fill","steelblue")
  .merge(circulos)
    .attr("cy", function(d) { return d.y; })
    .attr("stroke", "chocolate")

circulos.exit().remove()
```

Nuestros nuevos datos tienen sólo una entrada, mientras que tenemos cuatro elementos en el DOM. Cuando ligamos nuestros nuevos datos, la selección `update` contiene un único elemento: el primero, en el DOM y en el _array_; la selección `enter` está vacía, no hay que crear nuevos elementos del DOM; y aparece una nueva selección: `exit` con los elementos que ya no quedaron ligados a ningun dato y que, por lo tanto, hay que quitar.

Con estos ejemplos ya vimos como funcionan las tres selecciones que forman el GUP: unimos datos a una selección, actualizamos los elementos de la parte interior de la unión, creamos los elementos de la parte izquierda y eliminamos los elementos de la parte derecha. Ahora vamos a extendernos un poco sobre cómo funciona la unión para poder hacer un ejemplo que use las tres selecciones al mismo tiempo.

Todas las uniones que hemos usado hasta aquí están basadas en los índices de los arreglos, es decir, la _llave_ que nos permite unir los datos a los elementos del DOM es la posición en cada uno de los _arrays_: el primer elemento del arreglo de datos se une con el primer elemento de nuestra selección y así sucesivamente. Para tener más control sobre la forma en la que se hace esta unión D3.js soporta la unión a través de llaves, es decir, a partir de identificadores en los elementos del DOM. Consideremos el siguiente HTML:

```html
<!DOCTYPE html>
<body>
  <svg width="500" height="500">
  </svg>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
</html>
```

Vamos a crear unos círculos y unirlos a un Array de _objetos_:

```javascript
 datos = [{nombre:"A", radio:25, x:40, y:60}, {nombre:"B", radio:25, x:100, y:60}, {nombre:"C", radio:25, x:200, y:60}];
 var circulos = d3.select("svg").selectAll("circle");
     circulos.data(datos).enter().append("circle")
         .attr("r", function(d) { return d.radio; })
         .attr("cx", function(d) { return d.x; })
         .attr("cy", function(d) { return d.y; });
```
Hasta aquí todo es igual que antes, ahora vamos a unir un nuevo conjunto de datos, usando la propiedad `nombre` de cada objeto como _llave_ para la unión:

```javascript
 datos2 = [{nombre:"A", radio:25, x:40, y:60}, {nombre:"F", radio:25, x:100, y:120}, {nombre:"C", radio:25, x:200, y:60}];
 var cUpdate = d3.select("svg").selectAll("circle").data(datos2, function(d) { return d.nombre; });
     cUpdate.attr("fill", "red");

 var cEnter = cUpdate.enter();
     cEnter.append("circle")
         .attr("r", function(d) { return d.radio; })
         .attr("cx", function(d) { return d.x; })
         .attr("cy", function(d) { return d.y; })
         .attr("fill", "green");

 cUpdate.exit().remove();         
```

Al hacer la unión, pasamos un segundo argumrnto a la función `data()`: `function(d) { return d.nombre; }`. Esta función regresa, para cada dato, el identificador que vamos a usar como _llave_. De esta forma tenemos un control mucho más fino sobre la forma en la que los nuevos datos actualizan a los datos anteriores. En el ejemplo, el identificador "F" no aparece en los datos originales y por lo tanto forma parte de la selección de `enter` en la actualización (piensen cómo harían esto si hacen esa unión por índice, como en los ejemplos anteriores).

Otra cosa interesante del último ejemplo es que hace uso de las tres selecciones especiales: `enter`, `update` y `exit`. Fíjense como, para poder utlizar las tres, tenemos que manejar cada una por separado: la unión con los datos _siempre_ regresa la selección update; mientras que `update.enter()` y `update.exit()` regresan las selecciones de enter y exit respectivamente.
