/*
 * Object for keeping track of the layout of our triangular grid.
 * The triangle is made of cells, which have information about their
 * connectedness to nearby cells.
 */

public class TriangleGrid
{
  Cell[] cells;
  
  class Cell
  {
    PVector center;
    int[] neighbors;

    Cell(float cx, float cy, int n1, int n2, int n3)
    {
      this.center = new PVector(cx, cy);
      this.neighbors = new int[3];
      this.neighbors[0] = n1;
      this.neighbors[1] = n2;
      this.neighbors[2] = n3;
    }
  };

  void grid25()
  {
    // Layout for a 25-cell triangular grid.

    // Each triangle side is 1 unit. "h" is the triangle height
    float h = sin(radians(60));

    cells = new Cell[25];

    // Bottom row, left to right 
    cells[ 0] = new Cell( 0.0, h*0 + h*1/3,  -1,  1, -1 ); 
    cells[ 1] = new Cell( 0.5, h*0 + h*2/3,  15,  2,  0 ); 
    cells[ 2] = new Cell( 1.0, h*0 + h*1/3,  -1,  3,  1 ); 
    cells[ 3] = new Cell( 1.5, h*0 + h*2/3,  13,  4,  2 ); 
    cells[ 4] = new Cell( 2.0, h*0 + h*1/3,  -1,  5,  3 ); 
    cells[ 5] = new Cell( 2.5, h*0 + h*2/3,  11,  6,  4 ); 
    cells[ 6] = new Cell( 3.0, h*0 + h*1/3,  -1,  7,  5 ); 
    cells[ 7] = new Cell( 3.5, h*0 + h*2/3,   9,  8,  6 ); 
    cells[ 8] = new Cell( 4.0, h*0 + h*1/3,  -1, -1,  7 ); 

    // Second row, right to left
    cells[ 9] = new Cell( 3.5, h*1 + h*1/3,  10,  7, -1 ); 
    cells[10] = new Cell( 3.0, h*1 + h*2/3,  20,  9, 11 ); 
    cells[11] = new Cell( 2.5, h*1 + h*1/3,  10,  5, 12 ); 
    cells[12] = new Cell( 2.0, h*1 + h*2/3,  18, 11, 13 ); 
    cells[13] = new Cell( 1.5, h*1 + h*1/3,  14, 12,  3 ); 
    cells[14] = new Cell( 1.0, h*1 + h*2/3,  13, 15, 16 ); 
    cells[15] = new Cell( 0.5, h*1 + h*1/3,   1, -1, 14 ); 
    
    // Third row, left to right
    cells[16] = new Cell( 1.0, h*2 + h*1/3,  17, 14, -1 ); 
    cells[17] = new Cell( 1.5, h*2 + h*2/3,  18, 16, 23 ); 
    cells[18] = new Cell( 2.0, h*2 + h*1/3,  19, 17, 12 ); 
    cells[19] = new Cell( 2.5, h*2 + h*2/3,  21, 20, 18 ); 
    cells[20] = new Cell( 3.0, h*2 + h*1/3,  10, -1, 19 ); 

    // Fourth row, right to left
    cells[21] = new Cell( 1.5, h*3 + h*1/3,  19, 22, -1 ); 
    cells[22] = new Cell( 2.0, h*3 + h*2/3,  24, 21, 23 ); 
    cells[23] = new Cell( 2.5, h*3 + h*1/3,  -1, 22, 17 ); 
 
    // Top
    cells[24] = new Cell( 2.0, h*4 + h*1/3,  22, -1, -1 );     

    // Move the centroid to the origin
    translate(-1.3, -h*4/3);
  }

  void leds(OPC opc, int index)
  {
    // Create LED mappings, using the current grid coordinates
    for (int i = 0; i < cells.length; i++) {
      opc.led(index + i, int(cells[i].center.x + 0.5), int(cells[i].center.y + 0.5));
    }
  }
  
  void translate(float x, float y)
  {
    // Translate all points by this amount
    PVector t = new PVector(x, y);
    for (int i = 0; i < cells.length; i++) {
      cells[i].center.add(t);
    }
  }
  
  void mirror()
  {
    // Mirror all points left-to-right
    for (int i = 0; i < cells.length; i++) {
      cells[i].center.x = -cells[i].center.x;
    }
  }
  
    void mirrorv()
  {
    // Mirror all points up-down
    for (int i = 0; i < cells.length; i++) {
      cells[i].center.y = -cells[i].center.y;

    }
  }
  void scale(float s)
  {
    // Scale all points by this amount
    for (int i = 0; i < cells.length; i++) {
      cells[i].center.mult(s);
    }
  }
 
  void rotate(float angle)
  {
    // Rotate all points around the origin by this angle, in radians
    for (int i = 0; i < cells.length; i++) {
      cells[i].center.rotate(angle);
    }
  }


  void printcells (int text)
  {
   
    for (int i = 0; i < cells.length; i++) {
      println ("cellpos-",text,": ", i,": ", cells[i].center.x, "   ",cells[i].center.y);
    
    }
      println (" ");
  }

}
;
