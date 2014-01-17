# dxf2svg

Basic DXF to SVG converter.

## Usage

The only non-standard dependency is `dxfgrabber`.
If you dan't have it already, please install with
your favourite package manager, e.g.
```
pip install dxfgrabber
```
When it's done, you should be able to do things like:
```
python dxf2svg.py myDxfFile.dxf
```
Please note that currently suported types are only `LINE`, `LWPOLYLINE`, `CIRCLE` and `ARC`.
There is no support for block instances yet, though it should be quite easy to implement.

## TODO

* Add support for other entity types.
* Add support for block instances.
* Add support for line thickness and color.
* Add some example files.

