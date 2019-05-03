Costumes and Backgrounds
======

The Costume and Background classes are child classes of the Appearance class.

The Appearance class contains all the logic common to both, e.g. scaling and rotating images. The child classes contain the actions that are specific to these classes (e.g. certain overlays).

All actions performed on the images can be found in the class ImageRenderer

```eval_rst
.. inheritance-diagram:: miniworldmaker.boards.background.Background miniworldmaker.tokens.costume.Costume
   :top-classes: miniworldmaker.tools.appearance.Appearance
   :parts: 1
```

```eval_rst
.. toctree::
   :glob:
   
   appearances/*
```



