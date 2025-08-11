# Builder
a small, dependency-less html templating engine in two files of python.

## Features
- **Minimal**: `builder` will let you write html how you want, and will just do the building for you
- **Easy**: define some components, and use them wherever
- **Tiny**: it's two python files (+config). Builds into plain html you can put anywhere you like, no big bloated frameworks necessary.

# Usage
Set up your config in `config.py`.

Define some components in your components folder. Components are plain html files, structured as follows:
```html
<!--
@param parameter
-->
<p>Hello $parameter</p>
```
List the parameters in a comment at the top, and reference them with the `$` syntax. (If you have no parameters, you can omit the comment)

You can then save this in the components folder as `mytemplate.html`, and then in any html (including other components), call it using `<mytemplate parameter="World!">`.

When you run `builder.py`, it will populate and build all your html, and copy across any other files, into the destination folder, ready to serve as a static site.

*Licensed under the MIT license*