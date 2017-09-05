# Ejercicio práctico con D3

En este último apartdo vamos a usar lo que hemos aprendido de D3 (y en el camino aprender otras cosas) para hacer un mapa.

Vamos a retomar los datos históricos de los distritos electorales de 1994 a 2012.
Los puedes descargar de [aquí](https://github.com/CentroGeo/geoinformatica/tree/master/d3/shp).

Como te podrás dar cuenta, el `.shp` es de ~4.5 MB. Vamos a generalizarlo un poco para evitar tanto detalle
en la geometría de los distritos electorales. Ve a [mapshaper](http://mapshaper.org/) y arrastra los **4**
archivos del _shape_. Luego haz clic en _Simplify_, escoge cualquier método de simplificación y luego escoge
un porcentaje (por ejemplo, 75%). Luego haz clic en _Export_ y salva el resultado como **TopoJSON**.

Puedes ver que el TopoJSON es de alrededor de 1.5 MB. Un ahorro de ~3 veces el tamaño original.

**TAREA:** leer qué es un TopoJSON (que resulta ser que lo desarrolló el mismo Mike Bostock).

Para hacer un mapa en D3, necesitamos  incluir dos librerías de JS: `D3` y `topojson`. La primera es la base de D3, que es lo que hemos usado siempre hasta ahora, la segunda es una extensión para manejar datos de tipo `topoJSON`

Lo primero que vamos a hacer es leer los datos y dibujar un mapa pintando todos los polígonos de un mismo color:

```html
<!DOCTYPE html>
<head>
</head>
<body>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
  <script src="https://unpkg.com/topojson@3"></script>
  <script>
    var features;
	
    var width = 800,
        height = 600;
  
    var projection = d3.geoMercator()
                       .scale(1400)
                       .center([-102.584065, 23.62755])
                       .translate([width/2, height/2]);

    var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);
		
    var g = svg.append("g")
               .attr("id", "estados");
		
    d3.json('elecciones.json', function(error, datos) {
        features = topojson.feature(datos, datos.objects.elecciones);
        g.selectAll("path")
           .data(features.features)
           .enter().append("path")
           .attr("d", d3.geoPath().projection(projection));
    });
  </script>
</html>
```
Aqui tenemos ya todos los pasos básicos para dibujar un mapa con d3:

- Definir una proyección, las coordenadas del centro del mapa y el nivel de zoom:

```javascript
var projection = d3.geoMercator()
                   .scale(1400)
                   .center([-102.584065, 23.62755])
                   .translate([width/2, height/2]);
```
- Leer los datos: `d3.json` funciona igual que `d3.csv` como un _wrapper_ para una llamada AJAX. Entonces toda la acción va a suceder en el _callback_ de esa función.

- Desempacar los _features_: `features = topojson.feature(datos, datos.objects.elecciones);`

- Agregar un _path_ para cada uno de los features.

Para colorear este mapa de acuerdo a una de las variables, por ejemplo, el porcentaje de votos del PRD en 1994, hay que modificar el código para leer ese dato en particular y definir estilos para nuestra clasificación de colores. 
Esto lo hacemos con la función `d3.scaleQuantize()`. 

```html
<!DOCTYPE html>
<head>
<style>
/* Los colores para las clases */
  .q0 { fill:#fcc383; }
  .q1 { fill:#fc9f67; }
  .q2 { fill:#f4794e; }
  .q3 { fill:#e65338; }
  .q4 { fill:#ce2a1d; }
  .q5 { fill:#b30000; }
</style>
</head>
<body>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
  <script src="https://unpkg.com/topojson@3"></script>
  <script>
    var features;
    
    var width = 800,
        height = 600;
  
    var projection = d3.geoMercator()
                       .scale(1400)
                       .center([-102.584065, 23.62755])
                       .translate([width/2, height/2]);

    var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);

    var g = svg.append("g")
               .attr("id", "estados");
	       
    d3.json('elecciones.json', function(error, datos) {
        features = topojson.feature(datos, datos.objects.elecciones);
        
        var quantize = d3.scaleQuantize()
                         .domain([0, 52])
                         .range(d3.range(6).map(function(i) { return "q" + i; }));
                     
         g.selectAll("path")
            .data(features.features)
            .enter().append("path")
            .attr("d", d3.geoPath().projection(projection))
            .attr("class", function(d){ return quantize(d.properties['PRD94']) } );
    });
  </script>
```
Fíjense que definimos un conjunto de estilos para cada clase y luego, en la función `quantize` regresamos un _string_ con el nombre de la clase que le corresponde a cada dato.

Pero ¿qué pasa si queremos pintar el mapa con otra variable? Es claro que ese valor de `max` que usamos
va a cambiar dependiendo de la variable que se use, entonces necesitamos leer el máximo directamente 
de los datos, dentro del callback.
```html
<!DOCTYPE html>
<head>
<style>
/* Los colores para las clases */
  .q0 { fill:#fcc383; }
  .q1 { fill:#fc9f67; }
  .q2 { fill:#f4794e; }
  .q3 { fill:#e65338; }
  .q4 { fill:#ce2a1d; }
  .q5 { fill:#b30000; }
</style>
</head>
<body>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
  <script src="https://unpkg.com/topojson@3"></script>
  <script>
    var features;
    
    var width = 800,
        height = 600;
  
    var projection = d3.geoMercator()
                       .scale(1400)
                       .center([-102.584065, 23.62755])
                       .translate([width/2, height/2]);

    var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);

    var g = svg.append("g")
               .attr("id", "estados");
        
    d3.json('elecciones.json', function(error, datos) {
        features = topojson.feature(datos, datos.objects.elecciones);
        var interes = 'PRD94';
        var max = d3.max(features.features, function(d) { return d.properties[interes]; })
        
        var quantize = d3.scaleQuantize()
                         .domain([0, max])
                         .range(d3.range(6).map(function(i) { return "q" + i; }));
                     
        g.selectAll("path")
           .data(features.features)
           .enter().append("path")
           .attr("d", d3.geoPath().projection(projection))
           .attr("class", function(d){ return quantize(d.properties[interes]) } );
    });
  </script>
</html>
```

¿Y si queremos cambiar de manera interactiva la variable? Vamos a agregar un control al mapa que nos permita
seleccionarla. Esto lo podríamos hacer con un `<select>`o con un `<input type="radio">`.
Vamos a agregarle un `<select>` al DOM justo antes de agregar el `svg`. Para que se vea mejor, vamos a definir en
donde queremos que salga en la pantalla. Para esto, el elemeto agregado tiene una clase `variable`, cuyo estilo
está definido dentro de `<style>`.
```javascript
var select = d3.select("body")
               .append("select")
               .attr("class", "variable");
```
Hay que agregar las distintas variables que queremos poner en ese elemento de selección. Lo más facil es leer
los datos y ver qué columnas tienen y agregarlas. Para eso, dentro del _callback_ agregamos lo siguiente:
```javascript
var opciones = d3.keys(features.features[0].properties);
select.selectAll("option")
      .data(opciones)
      .enter()
      .append("option")
      .attr("value", function (d) { return d; })
      .property("selected", function(d){ return d === 'PRD94'; })
      .text(function (d) { return d; });
```
Aquí leemos las variables del primer elemento de los del JSON (puesto que todos traen las mismas columnas) con la
función `d3.keys()`. Luego agarramos el elemento `<select>` del DOM y le agregamos etiquetas de `<option>`. Hacemos 
una unión de los datos de las opciones, hacemos la selección  `enter()` y le decimos al DOM que agregue un atributo
`value`, que selecciones el que se llame `PRD94` y que le ponga un texto.

Hay que definir qué queremos que pase cuando se cambie la selección de esa variable. Para esto, usamos los 
populares _event listeners_ de JavaScript: cuando **este evento** ocurra, ejecuta _esta función_.
```javascript
select.on("change", function(d) {
    interes = d3.select(this).property("value");
    d3.select("svg").selectAll("path").remove();
    hazMapa(interes);
});
```
Aquí estamos diciendo que cuando _cambie_ la selección del `<select>`, a la variable `interes` le asignamos lo
que acabamos de seleccionar, "limpiamos" el mapa y ejecutamos la función que hace el mapa, que es la misma que
usamos anteriormente, pero como ahora estamos haciendo varios mapas, es más eficiente llamar todas esas instrucciones
como una función:
```javascript
function hazMapa(interes){

    var max = d3.max(features.features, function(d) { return d.properties[interes]; })

    var quantize = d3.scaleQuantize()
                     .domain([0, max])
                     .range(d3.range(6).map(function(i) { return "q" + i; }));
                     
    svg.selectAll("path")
       .data(features.features)
       .enter().append("path")
       .attr("d", d3.geoPath().projection(projection))
       .attr("class", function(d){ return quantize(d.properties[interes]) } );
}
```

Y para que al inciar la página haya un mapa, escribimos:
```javascript
var interes = d3.select('select').property("value");
hazMapa(interes);
```
después de haber creado las entradas del elemento `<select>`. Aquí vemos qué variable está seleccionada (`PRD94`)
y hacemos el mapa con esta variable.

El código completo queda así:
```html
<!DOCTYPE html>
<head>
<style>
/* Los colores para las clases */
  .q0 { fill:#fcc383; }
  .q1 { fill:#fc9f67; }
  .q2 { fill:#f4794e; }
  .q3 { fill:#e65338; }
  .q4 { fill:#ce2a1d; }
  .q5 { fill:#b30000; }
  
  .variable {
    position: absolute;
    top: 100px;
    left: 650px;
  }
</style>
</head>
<body>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
  <script src="https://unpkg.com/topojson@3"></script>
  <script>
    var features;
    
    var width = 800,
        height = 600;
  
    var projection = d3.geoMercator()
                       .scale(1400)
                       .center([-102.584065, 23.62755])
                       .translate([width/2, height/2]);

    var select = d3.select("body")
                   .append("select")
                   .attr("class", "variable");
                   
    var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);

    var g = svg.append("g")
               .attr("id", "estados");
        
    d3.json('elecciones.json', function(error, datos) {
    
        features = topojson.feature(datos, datos.objects.elecciones);
        
        var opciones = d3.keys(features.features[0].properties);
        select.selectAll("option")
              .data(opciones)
              .enter()
              .append("option")
              .attr("value", function (d) { return d; })
              .property("selected", function(d){ return d === 'PRD94'; })
              .text(function (d) { return d; });
        
        select.on("change", function(d) {
           interes = d3.select(this).property("value");
           d3.select("svg").selectAll("path").remove();
           hazMapa(interes);
        });
        var interes = d3.select('select').property("value");
        hazMapa(interes);
    });
    
    function hazMapa(interes){
        
        var max = d3.max(features.features, function(d) { return d.properties[interes]; })
        
        var quantize = d3.scaleQuantize()
                         .domain([0, max])
                         .range(d3.range(6).map(function(i) { return "q" + i; }));
                     
         g.selectAll("path")
           .data(features.features)
           .enter().append("path")
           .attr("d", d3.geoPath().projection(projection))
           .attr("class", function(d){ return quantize(d.properties[interes]) } );
    }
  </script>
</html>
```

## Agregar una gráfica que esté ligada a los datos (y al mapa)

Grafica con esas variables que cambie con la interactividad

Grafica que muestre promedio

Al hacer clic en estado que se actualiced la grafica con los datos de es estado

Regresar a [Selecciones, Joins y General Update Pattern](d3_selecciones.md)
