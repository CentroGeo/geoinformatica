# La anatomía de una página Web

Aquí vamos a hablar un poco de cómo está estructurada una página Web. La idea no es que aprendan a hacer páginas sino que entiendan cuáles son los principales elementos que la conforman y cómo interactúan entre ellos.

## HTML

El [HTML](https://www.w3schools.com/html/) es el bloque de construcción más básico de una página, con el definimos la estructura general y organizamos el contenido. No es un lenguaje de programación sino un lenguaje de _marcado_, es decir, usa etiquetas para definir elementos como encabezados, párrafos, imágenes, etcétera. El _browser_ se encarga de convertir el HTML en la página que vemos.

Aquí tenemos un ejemplo súper simple de un HTML, cópialo y pégalo en un archivo y ábrelo con un navegador.

```html
<!DOCTYPE html>
<html>
<head>
<title>El título</title>
</head>
<body>

<h1>Un encabezado</h1>
<p>Y algo interesante que decir.</p>

</body>
</html>
```
Como puedes ver, el _estilo_ de la página es muy _austero_, esto es porque en el modelo de desarrollo Web el estilo, la organización y el contenido están separados: la organización es el HTML, el contenido es lo que está adentro de las etiquetas y el estilo, el estilo se cuece aparte...

## CSS

[CSS](https://www.w3schools.com/css/) quiere decir **C**ascading **S**tyle **S**heets y es el lenguaje con el que se define el estilo de una página. Permite definir los atributos de los elementos de HTML que definen la forma en la que el _browser_ los va a _dibujar_. Como ejemplo, definamos un CSS para la página del ejemplo anterior:

```css
body {
    background-color: lightblue;
}

h1 {
    color: white;
    text-align: center;
}

p {
    font-family: verdana;
    font-size: 20px;
}
```

Los encabezados que aparecen a la izquierda de las llaves se llaman _selectores_ y permiten seleccio9nar elementos ya sea por tipo, clase, identificador o relación. Para ver como funciona, vamos a agregarlo a nuestra página de ejemplo. Edita el HTML para que se vea así:

```html
<!DOCTYPE html>
<html>
<head>
<title>El título</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>

<h1>Un encabezado</h1>
<p>Y algo interesante que decir.</p>

</body>
</html>
```
Copia pega el CSS de arriba en un archivo y guárdalo como estilo.css. Ahora vuelve a abrir el HTML con el navegador.


## El DOM

DOM significa **D**ocument **O**bject **M**odel.

El Document Object Model ([DOM](https://www.w3schools.com/js/js_htmldom.asp)) conecta páginas web a scripts o lenguajes de programación. De este modo, se puede interactuar (programáticamente) con los elementos de la página y, entre otras cosas, modificarlos.

Una manera de ver al DOM, es como una representación en forma de _árbol_ del HTML.
Los elementos de este árbol en realidad son _objetos_ de HTML (como los `div`s, `input`s, `p`s, etc.).

Con este modelo, JavaScript puede acceder a los elementos del HTML, reaccionar a la interacción del usuario y crear contenido dinámico, por ejemplo:
* cambiar todo el HTML en la página
* cambiar todos los atributos de HTML en la página
* cambiar todos los estilos de CSS en la página
* eliminar elementos de HTML y sus atributos
* agregar elementos de HTML y atributos
* reaccionar a todos los eventos de HTML que existan en la página
* crear nuevos eventos de HTML en la página

<img src="https://www.w3schools.com/js/pic_htmltree.gif" alt="https://www.w3schools.com/js/js_htmldom.asp" title="https://www.w3schools.com/js/js_htmldom.asp"/>

## Y ¿cómo accedo al DOM?

En un browser moderno usa la tecla **F12** o **Shift+Ctrl+J** o **Shift+Ctrl+I** o en el menú del navegador escoge "Herramientas de desarrollador" o "Developer Tools".

![Herramientas de desarrollador](./img/dev_tools.png "Title")

Estas herramientas nos permiten identificar elementos del DOM e interactuar con ellos, por ejemplo cambiando sus propiedades o incluso moviéndolos de lugar. Inténtalo con esta página.

En resumen, el DOM es la representación que nos permite interactuar, a través de Javascript, con el contenido y el formato de una página Web. A partir de su organización podemos seleccionar elementos para modificarlos o agregar elementos en lugares específicos. 

## Javascript

[Javascript](https://www.w3schools.com/js/) es el lenguaje de programación para los navegadores, es la forma de interactuar programáticamente con el DOM. Javascript dota a las páginas web de las capacidades necesarias para la interactividad a la que estamos acostumbrados, sin el, todas las páginas serían [estáticas](http://toastytech.com/evil/).

En general, el código de javascript se incluye de la misma forma en la que incluimos el CSS, sin embargo, a través de las Herramientas de Desarrollo, podemos también escribir código, seleccionando la consola.

