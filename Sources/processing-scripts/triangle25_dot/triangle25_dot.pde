OPC opc;
PImage dot;
TriangleGrid triangle;

void setup()
{
  size(500, 400);

  // Load a sample image
  dot = loadImage("dot.png");

  // Connect to the local instance of fcserver
  opc = new OPC(this, "127.0.0.1", 7890);

  // Map our triangle grid to the center of the window
  triangle = new TriangleGrid();
  triangle.grid25();
  triangle.printcells(1);
  triangle.mirrorv();              // trinagle upside down, ist nachher nach unten
    triangle.printcells(2);
  triangle.scale(height * 0.21);    // umsetzen in Fensterhöhe, x ist null
    triangle.printcells(3);
  triangle.translate(width * 0.37, height * 0.7);   // umsetzten in fentergrösse
    triangle.printcells(4);
  triangle.leds(opc, 0);

}

void draw()
{
  background(0);

  // Draw the image, centered at the mouse location
  float dotSize = height * 0.7;
  image(dot, mouseX - dotSize/2, mouseY - dotSize/2, dotSize, dotSize);
}

