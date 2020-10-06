#!/usr/bin/env python

import dxfgrabber
import math
import sys

# SVG TEMPLATES

SVG_PREAMBLE = \
'<svg xmlns="http://www.w3.org/2000/svg" ' \
'version="1.1" viewBox="{0} {1} {2} {3}">\n'

SVG_MOVE_TO = 'M {0} {1} '
SVG_LINE_TO = 'L {0} {1} '
SVG_ARC_TO  = 'A {0} {1} {2} {3} {4} {5} {6} '

SVG_PATH = \
'<path d="{0}" fill="none" stroke="{1}" stroke-width="{2:.2f}" />\n'

SVG_LINE = \
'<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" stroke="{4}" stroke-width="{5:.2f}" />\n'

SVG_CIRCLE = \
'<circle cx="{0}" cy="{1}" r="{2}" stroke="{3}" stroke-width="{4}" fill="none" />\n'

# SVG DRAWING HELPERS

def angularDifference(startangle, endangle):
  result = endangle - startangle
  while result >= 360:
    result -= 360
  while result < 0:
    result += 360
  return result

def pathStringFromPoints(points):  
  pathString = SVG_MOVE_TO.format(*points[0])
  for i in range(1,len(points)):
    pathString += SVG_LINE_TO.format(*points[i])
  return pathString

# CONVERTING TO SVG

def handleEntity(svgFile, e):
  # TODO: handle colors and thickness
  # TODO: handle ellipse and spline and some other types
  
  if isinstance(e, dxfgrabber.entities.Line):      
    svgFile.write(SVG_LINE.format(
      e.start[0], e.start[1], e.end[0], e.end[1],
      'black', 1          
    ))

  elif isinstance(e, dxfgrabber.entities.LWPolyline):
    pathString = pathStringFromPoints(e)
    if e.is_closed:
      pathString += 'Z'
    svgFile.write(SVG_PATH.format(pathString, 'black', 1))
    
  elif isinstance(e, dxfgrabber.entities.Circle):
    svgFile.write(SVG_CIRCLE.format(e.center[0], e.center[1],
      e.radius, 'black', 1))

  elif isinstance(e, dxfgrabber.entities.Arc):
    
    # compute end points of the arc
    x1 = e.center[0] + e.radius * math.cos(math.pi * e.startangle / 180)
    y1 = e.center[1] + e.radius * math.sin(math.pi * e.startangle / 180)
    x2 = e.center[0] + e.radius * math.cos(math.pi * e.endangle / 180)
    y2 = e.center[1] + e.radius * math.sin(math.pi * e.endangle / 180)

    pathString  = SVG_MOVE_TO.format(x1, y1)
    pathString += SVG_ARC_TO.format(e.radius, e.radius, 0,
      int(angularDifference(e.startangle, e.endangle) > 180), 1, x2, y2)

    svgFile.write(SVG_PATH.format(pathString, 'black', 1))
  elif isinstance(e, dxfgrabber.entities.Insert):
    # TODO: handle group instances
    pass
#end: handleEntity

def saveToSVG(svgFile, dxfData):
  minX = dxfData.header['$EXTMIN'][0]
  minY = dxfData.header['$EXTMIN'][1]
  maxX = dxfData.header['$EXTMAX'][0]
  maxY = dxfData.header['$EXTMAX'][1]
  
  # TODO: also handle groups
  svgFile.write(SVG_PREAMBLE.format(
    minX, minY, maxX - minX, maxY - minY))

  for entity in dxfData.entities:
    layer = dxfData.layers[entity.layer]
    if layer.on and not layer.frozen:
      handleEntity(svgFile, entity)
     
  svgFile.write('</svg>\n')
#end: saveToSVG

if __name__ == '__main__':
  # TODO: error handling
  if len(sys.argv) < 2:
    sys.exit('Usage: {0} file-name'.format(sys.argv[0]))

  filename = sys.argv[1]

  # grab data from file
  dxfData = dxfgrabber.readfile(filename)

  # TODO: show alert if the file already exist
  # convert and save to svg
  svgName = '.'.join(filename.split('.')[:-1] + ['svg'])
  svgFile = open(svgName, 'w')

  saveToSVG(svgFile, dxfData)

  svgFile.close()
#end: __main__

