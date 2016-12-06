// Some real-time FFT! This visualizes music in the frequency domain using a
// polar-coordinate particle system. Particle size and radial distance are modulated
// using a filtered FFT. Color is sampled from an image.

import ddf.minim.analysis.*;
import ddf.minim.*;

OPC opc;
PImage dot;
PImage colors;
TriangleGrid triangle;
Minim minim;
AudioPlayer player;
FFT fft;
float[] fftFilter;

String filename = "blues2.mp3";
float spinleft = -0.001;
float spinright = 0.002;
float spin=spinright;
float radiansPerBucket = radians(2);
float decay = 0.97;
float opacity = 40;
float minSize = 0.1;
float sizeScale = 0.5;
int lasttime=millis();
int newtime=0;

float songPos;
float t = millis()/100;
BeatDetect beat;

void setup()
{
  size(500, 400, P3D);
  

  minim = new Minim(this); 
  // Small buffer size!
  player = minim.loadFile(filename, 512);
  player.play();
  beat = new BeatDetect(player.bufferSize(), player.sampleRate());
  beat.setSensitivity(450);
  //bl = new BeatListener( beat, player);
  background(0);
  fill(0);

  

  dot = loadImage("dot.png");
  colors = loadImage("colors10.png");

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

 beats();
  
//   timer();
  classicLine();
  
  changePos();
  
}

void timer()//------
{
   textSize(14);
  if( player.position() > 8206)
   {
   fill(255,0,0,10); 
   }
   else{
     fill(0);
   }
   text("" + int(player.position()/1000), width/2-5, 9.5*height/10);
}

void slider( )
{
  
  line(0, 9*height/10, width, 9*height/10);
  
  
  songPos = map(player.position(), 0, 240000, 0, width);
  stroke(0,10);
  
  rect(songPos, (9*height/10), 5, 1);
   if( player.position() > 8206)
   {
     stroke(255,10);
     
   }
   
 
}

void changePos()
{
  float pos = ((float) mouseX/width)*player.length();
  if(mousePressed && mouseX >= 0 && mouseX <= width
  && mouseY >= (9*height/10)-5 && mouseY <= (9*height/10)+5)
  {
    player.cue((int)pos);
  }
  
}

void beats()
{
    beat.detect(player.mix);
  
 
    
    stroke(random(10,255), random(10,250), random(10, 250));
    for(int i = 0; i < player.bufferSize() - 1; i++)
    {

    float x1 = map(i, 0, player.bufferSize(), 0, width);
    float x2 = map(i+1, 0, player.bufferSize(), 0, width);
    line(x1, 220 + player.right.get(i)*100, x2, 220 + player.right.get(i+1)*200); 
    }
   
}
 
 
 void classicLine()
 {

   
   stroke(random(10,255), random(10,30), random(10, 100));
   //stroke(255,0,0);
   strokeWeight(random(1,7));
   
   for(int i = 0; i < player.bufferSize() - 1; i++)
  {
   float x1 = map(i, 0, player.bufferSize(), 0, width);
   float x2 = map(i+1, 0, player.bufferSize(), 0, width);
   
 
   line(x1, 220 + player.right.get(i)*350, x2, 220 + player.right.get(i+1)*350); 
  }
  
 // slider();
 }






void stop()
{

  player.close();

  minim.stop();
  
  super.stop();
}
