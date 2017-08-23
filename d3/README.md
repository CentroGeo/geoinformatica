## D3.js

Este tutorial trata sobre el uso de D3 para hacer gráficas dinámicas en web.

Los elementos principales para poder utilizar D3, requerimos ciertos elementos básicos:

- Navegadores web
- HTML
- CSS
- Javascript

Estos elementos los pueden recordar de sus clsaes de Leaflet...
Pero lo que hay que rescatar es que se usan muchas **etiquetas**.

Luego hay que saber qué es un [XML](https://www.w3schools.com/Xml/) y, en particular, un [SVG](https://www.w3schools.com/graphics/svg_intro.asp).

En corto, un SVG es un XML que describe o define un dibujo vectorial.

Un SVG tiene ciertos elementos básicos como:
- Rectángulos
- Círculos
- Elipses
- (Poli)Líneas
- Polígonos
- Paths
- Text

El _path_ tiene muchos modificadores:
* M = moveto
* L = lineto
* H = horizontal lineto
* V = vertical lineto
* C = curveto
* S = smooth curveto
* Q = quadratic Bézier curve
* T = smooth quadratic Bézier curveto
* A = elliptical Arc
* Z = closepath

Un ejemplo de un SVG sencillo puede ser algo como:

```html
<svg width="100" height="100">
  <circle cx="50" cy="50" r="40" stroke="red" stroke-width="4" fill="blue" />
</svg>
```
<img src="https://centrogeo.github.io/geoinformatica/d3/circle.svg"/>

Un ejemplo un poco más elaborado puede ser:

```html
<svg height="400" width="450" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <path id="lineAB" d="M 100 350 l 150 -300" stroke="red"
  stroke-width="3" fill="none" />
  <path id="lineBC" d="M 250 50 l 150 300" stroke="red"
  stroke-width="3" fill="none" />
  <path d="M 100 350 q 150 -300 300 0" stroke="blue"
  stroke-width="5" fill="none" />
  <!-- Mark relevant points -->
  <g stroke="black" stroke-width="3" fill="black">
    <circle id="pointA" cx="100" cy="350" r="3" />
    <circle id="pointB" cx="250" cy="50" r="3" />
    <circle id="pointC" cx="400" cy="350" r="3" />
  </g>
  <!-- Label the points -->
  <g font-size="30" font-family="sans-serif" fill="black" stroke="none"
  text-anchor="middle">
    <text x="100" y="350" dx="-30">A</text>
    <text x="250" y="50" dy="-10">B</text>
    <text x="400" y="350" dx="30">C</text>
  </g>
</svg>
```
<img src="https://centrogeo.github.io/geoinformatica/d3/path.svg"/>
