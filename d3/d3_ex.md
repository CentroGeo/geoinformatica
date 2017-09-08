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

Esta forma de hacerlo funciona, pero no es la forma _D3_, es decir, no estamos usando los datos para llevar el flujo del documento. Fíjense que en el evento de _clic_ hacemos `d3.select("svg").selectAll("path").remove();`, esto efectivamente elimina todos los _paths_ junto con sus datos, una mejor opción es usar la selección de `update` para actualizar los datos:

```javascript
    function hazMapa(interes){

        var max = d3.max(features.features, function(d) { return d.properties[interes]; })
        
        var quantize = d3.scaleQuantize()
                         .domain([0, max])
                         .range(d3.range(6).map(function(i) { return "q" + i; }));
                     
         var mapUpdate = g.selectAll("path")
                          .data(features.features);
         
         var mapEnter = mapUpdate.enter();
         
         mapEnter.append("path")
                 .merge(mapUpdate)
                 .attr("d", path)
                 .attr("class", function(d){ return quantize(d.properties[interes]) } )
                 .on("click", clicked);
    }
```

Ahora ya estamos utilizando la selección `update` para actualizar los colores del mapa en función de la variable de interés. Realmente no cambia nada, más que la satisfacción de hacer las cosas como se debe.


## Agregar una gráfica que esté ligada a los datos (y al mapa)

Para terminar el ejercicio, vamos a añadir a nuestra visualización una gráfica de barras que mustre los resultados electorales en el distrito en que se haga clic, para el año seleccionado en la variable de interés. De los talleres anteriores ya sabemos cómo hacer gráficas de barras y actualizar sus datos, lo que no sabemos es como ligar las acciones entre los dos elementos. Antes de empezar, hay que hacer algunos arreglos para ayudar a la interacción del usuario con la visualización.

Primero que nada, algunos distritos son muy pequeños, por lo que hacer clic directamente sobre ellos resultaría difícil. Una forma de arreglar este problema es implementar un _zoom_: al hacer clic en un distritu, la visualización debe centrarse en el distrito y acercarse a la extensión del mismo. Para hacer esto vamos a hacer una transición sobre el `translate` del mapa. Lo primero que necesitamos hacer es decirle a cada `path` que _escuche_ los clics:

```javascript
 mapEnter.append("path")
	 .merge(mapUpdate)
	 .attr("d", path)
	 .attr("class", function(d){ return quantize(d.properties[interes]) } )
	 .on("click", clicked);
```
Aquí ligamos el _clic_ a la función `clicked` que es donde vamos a programar la _magia_ del zoom:


```javascript
    function clicked(d) {
        if (active.node() === this) return reset();
        active.classed("active", false);
        active = d3.select(this).classed("active", true);

        var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

        g.transition()
         .duration(750)
         .style("stroke-width", 1.5 / scale + "px")
         .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
   }

   function reset() {
        active.classed("active", false);
        active = d3.select(null);

        g.transition()
         .duration(750)
         .style("stroke-width", "1.5px")
         .attr("transform", "");
    }

```

Lo primero que estamos haciendo es ver si el polígono en el que hicimos clic es el polígono q7ue ya tenemos seleccionado, de esta forma, volver a hacer clic sobre el polígono nos regresa a la extensión original (esa lógica está en la función `reset`). Luego le cambiamos la clase al polígono seleccionado y calculamos su _bounding box_ y su centro. La escala es entonces el inverso del máximo entre las relaciones de los lados del _bounding box_ y el tamaño correspondiente del svg (lo multiplicamos por 0.9 para dar un poco de espacio alrededor). A partir de ahí ya sólo tenemos que aplicar una transición con los valores que acabamos de calcular (también cambiamos un poco el estilo del polígono para indicar que está resaltado).

La siguiente modificación que hay que hacer para mejorar la _usabilidad_ del la visualización es cambiar la forma en la que seleccionamos la varibale de interés. En lugar de ligar todas la variables al _dropdown_, vamos a hacer dos selectores: uno para el partido y otro para el año:

```html
  <select id="partido" class="select">
    <option value="PRI" selected=true>PRI</option>
    <option value="PAN">PAN</option>
    <option value="PRD">PRD</option>
  </select>
  <select id="anho", class="select">
    <option value="94">1994</option>
    <option value="00">2000</option>
    <option value="06">2006</option>
    <option value="12">2012</option>
  </select>

```
y reconstruir la variable de interés:

```javascript
select.on("change", function(d) {
   var interes = "";
   d3.selectAll(".select").each(function(d,i){ return interes+=this.value;});
   hazMapa(interes);
});
```

Ahora sí ya tenemos todo listo para agregar nuestra gráfica de barras. Para esto, en la función que maneja el clic sobre cada polígono vamos a llamar a una función que haga las barras. Esa parte es relativamente fácil, el problema es la forma en la que tenemos los datos. Si recuerdan el ejemplo final de las gráficas de barras, en las que leímos el csv, el json que regresa es un _array_ de filas, es decir, tenemos una lista de objetos cada uno de los cuales es un par con el nombre de la columna y el valor. Si exploran los datos que nos regresa leer el `topoJSON`no se parecen a eso, hay que procesarlos para poder usarlos. D3 provee una serie de operadores para manipular datos, equivalentes a las funcionalidades de R para hacer _melt_ o _pivot_, el problema es que como operan sobre objetos (JSON), son bastante más complicadas de entender. En el callback de `d3.json` vamos a manipular los datos para mandarlos a la gráfica de barras:


```javascript
features = topojson.feature(datos, datos.objects.elecciones);

var propiedades = features.features.map(function(distrito) {return distrito.properties;});
nest = d3.nest()
  .key(function(d) { return d.CLAVEGEO; })
  .rollup(function(values) {
    return {
      PRI94: +d3.values(values)[0]['PRI94'],
      PRI00: +d3.values(values)[0]['PRI00'],
      PRI06: +d3.values(values)[0]['PRI06'],
      PRI12: +d3.values(values)[0]['PRI12'],
      PAN94: +d3.values(values)[0]['PAN94'],
      PAN00: +d3.values(values)[0]['PAN00'],
      PAN06: +d3.values(values)[0]['PAN06'],
      PAN12: +d3.values(values)[0]['PAN12'],
      PRD94: +d3.values(values)[0]['PRD94'],
      PRD00: +d3.values(values)[0]['PRD00'],
      PRD06: +d3.values(values)[0]['PRD06'],
      PRD12: +d3.values(values)[0]['PRD06']
    };
  })
  .entries(propiedades);
```

Lo que tenemos es un objeto (del tipo `nest`) que nos permite seleccionar cada distrito por su clave (CVEGEO), este objeto lo guardamos en la variable global `nest` para poder usarlo en la función que va a hacer la gráfica.


```html
<!DOCTYPE html>
<head>
<style>
/*Los colores para las clases de población*/
  .q0 { fill:#fcc383; }
  .q1 { fill:#fc9f67; }
  .q2 { fill:#f4794e; }
  .q3 { fill:#e65338; }
  .q4 { fill:#ce2a1d; }
  .q5 { fill:#b30000; }
  
  #partido{
    position: absolute;
    top: 100px;
    left: 650px;
  }
  
  #anho{
    position: absolute;
    top: 100px;
    left: 705px;
  }
  
  .variable{
    position: absolute;
    top: 130px;
    left: 665px;
  }
  
  .background {
    fill: none;
    pointer-events: all;
  }

  #estados .active {
    stroke: black;
  }
  
  #bars {
    position: absolute;
    margin-top: 100px;
    margin-left: 50px;
  }

  .bar text {
    fill: black;
    font: 10px sans-serif;
    text-anchor: right;
  }
  
  #titulo {
    position: absolute;
    top: 50px;
    left: 900px;
    font: 20px sans-serif;
  }
  
</style>
</head>
<body>
  <select id="partido" class="select">
    <option value="PRI" selected=true>PRI</option>
    <option value="PAN">PAN</option>
    <option value="PRD">PRD</option>
  </select>
  <select id="anho", class="select">
    <option value="94">1994</option>
    <option value="00">2000</option>
    <option value="06">2006</option>
    <option value="12">2012</option>
  </select>
  <div id="titulo"></div>
</body>
  <script src="https://d3js.org/d3.v4.min.js"></script>
  <script src="https://unpkg.com/topojson@3"></script>
  <script>
    var features, nest, bar;
    
    var width = 800,
        height = 600,
        active = d3.select(null);
  
    var projection = d3.geoMercator()
                       .scale(1400)
                       .center([-102.584065, 23.62755])
                       .translate([width/2, height/2]);

    var select = d3.selectAll(".select");
                   
    var svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height);
                
    svg.append("rect")
       .attr("class", "background")
       .attr("width", width)
       .attr("height", height)
       .on("click", reset);
          
    var g = svg.append("g")
               .attr("id", "estados");
               
    var barSvg = d3.select("body").append("svg")
               .attr("id", "bars")
               .attr("height", 260)
               .attr("width", 400);
               

    var path = d3.geoPath().projection(projection);
        
    d3.json('elecciones.json', function(error, datos) {
    
        features = topojson.feature(datos, datos.objects.elecciones);
        
        var propiedades = features.features.map(function(distrito) {return distrito.properties;});
        nest = d3.nest()
          .key(function(d) { return d.CLAVEGEO; })
          .rollup(function(values) {
            return {
              PRI94: +d3.values(values)[0]['PRI94'],
              PRI00: +d3.values(values)[0]['PRI00'],
              PRI06: +d3.values(values)[0]['PRI06'],
              PRI12: +d3.values(values)[0]['PRI12'],
              PAN94: +d3.values(values)[0]['PAN94'],
              PAN00: +d3.values(values)[0]['PAN00'],
              PAN06: +d3.values(values)[0]['PAN06'],
              PAN12: +d3.values(values)[0]['PAN12'],
              PRD94: +d3.values(values)[0]['PRD94'],
              PRD00: +d3.values(values)[0]['PRD00'],
              PRD06: +d3.values(values)[0]['PRD06'],
              PRD12: +d3.values(values)[0]['PRD06']
            };
          })
          .entries(propiedades);
        
        
        select.on("change", function(d) {
           var interes = "";
           d3.selectAll(".select").each(function(d,i){ return interes+=this.value;});
           hazMapa(interes);
        });
        var interes = "";
           d3.selectAll(".select").each(function(d,i){ return interes+=this.value;});
           hazMapa(interes);
    });
    
    function hazMapa(interes){

        var max = d3.max(features.features, function(d) { return d.properties[interes]; })
        
        var quantize = d3.scaleQuantize()
                         .domain([0, max])
                         .range(d3.range(6).map(function(i) { return "q" + i; }));
                     
         var mapUpdate = g.selectAll("path")
                          .data(features.features);
         
         var mapEnter = mapUpdate.enter();
         
         mapEnter.append("path")
                 .merge(mapUpdate)
                 .attr("d", path)
                 .attr("class", function(d){ return quantize(d.properties[interes]) } )
                 .on("click", clicked);
    }
    
    function hazGrafica(anho, distrito){
        var partidos = ['PRI', 'PAN', 'PRD'];
        var colores = {"PRI": "#cc0000", "PAN": "#4da6ff", "PRD": "#ffee17"};
        var datos = [];
        
        for (i = 0; i <= 2 ; i++){
            c = {};
            c["nombre"] = partidos[i];
            c["valor"] = distrito[0].value[partidos[i]+anho];
            datos.push(c);
        }
        
        var barWidth = 400,
            barHeight = 86;
        var x = d3.scaleLinear()
                  .range([0, barWidth])
                  .domain([0, 100]);
        
        bar = barSvg.selectAll(".bar")
                    .data(datos, function(d){ return d.nombre;});
        
        var barEnter = bar.enter()
            .append("g")
            .attr("class", "bar")
            .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; })
        
        d3.select("#titulo").html("Estado:" + distrito[0].key.substr(0,2) + " - Distrito:" + distrito[0].key.substr(3));
        
        barEnter.append("rect")
            .transition()
            .duration(500)
            .attr("width", function(d) { return x(d.valor); })
            .attr("height", barHeight - 1)
            .attr("fill", function(d) { return colores[d.nombre]; });
            
        
            
        barEnter.append("text")
                .transition()
                .duration(500)
                .attr("x", function(d) { return x(d.valor) + 10; })
                .attr("y", barHeight / 2)
                .attr("dy", ".35em")
                .text(function(d) { return d.valor });
                
        barEnter.append("text")
                .transition()
                .duration(500)
                .attr("x", 10 )
                .attr("y", barHeight / 2)
                .attr("dy", ".35em")
                .text(function(d) { return d.nombre });
            
        bar.select("rect")
           .transition()
           .duration(500)
           .attr("width", function(d) { return x(d.valor); });

        bar.select("text")
           .transition()
           .duration(500)
           .attr("x", function(d) { return x(d.valor) + 10; })
           .text(function(d) { return d.valor; });
           
    }
    
    function clicked(d) {
        if (active.node() === this) return reset();
        active.classed("active", false);
        active = d3.select(this).classed("active", true);

        var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

        g.transition()
         .duration(750)
         .style("stroke-width", 1.5 / scale + "px")
         .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
         
        var distrito = nest.filter(function(a) {
              return a.key == d.properties.CLAVEGEO;
           });
           
        var anho = d3.select("#anho").node().value;
        hazGrafica(anho, distrito);
   }

   function reset() {
        active.classed("active", false);
        active = d3.select(null);

        g.transition()
         .duration(750)
         .style("stroke-width", "1.5px")
         .attr("transform", "");
    }
  </script>
</html>
```

Regresar a [Selecciones, Joins y General Update Pattern](d3_selecciones.md)
