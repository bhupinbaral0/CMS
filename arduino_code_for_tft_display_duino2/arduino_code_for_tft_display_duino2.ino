
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library
#include <SPI.h>


// For the breakout, you can use any 2 or 3 pins
// These pins will also work for the 1.8" TFT shield
#define TFT_CS     10
#define TFT_RST    9  // you can also connect this to the Arduino reset
                      // in which case, set this #define pin to -1!
#define TFT_DC     8

#define TFT_CS2 5
#define TFT_DC2 4
#define TFT_RST2 9




// Option 1 (recommended): must use the hardware SPI pins
// (for UNO thats sclk = 13 and sid = 11) and pin 10 must be
// an output. This is much faster - also required if you want
// to use the microSD card (see the image drawing example)
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS,  TFT_DC,  TFT_RST);



// Option 2: use any pins but a little slower!
#define TFT_SCLK 6  // set these to be whatever pins you like!
#define TFT_MOSI 7   // set these to be whatever pins you like!
Adafruit_ST7735 tft2 = Adafruit_ST7735(TFT_CS2, TFT_DC2, TFT_MOSI, TFT_SCLK, TFT_RST);


char str, character;
int flag=1;
void setup(void) {
  Serial.begin(9600);


  // Use this initializer if you're using a 1.8" TFT
  tft.initR(INITR_BLACKTAB);   // initialize a ST7735S chip, black tab
  tft2.initR(INITR_BLACKTAB);   // initialize a ST7735S chip, black tab
  
  // Use this initializer (uncomment) if you're using a 1.44" TFT
  //tft.initR(INITR_144GREENTAB);   // initialize a ST7735S chip, black tab

  // Use this initializer (uncomment) if you're using a 0.96" 180x60 TFT
  //tft.initR(INITR_MINI160x80);   // initialize a ST7735S chip, mini display

 
  tft.fillScreen(ST7735_BLACK);
  tft2.fillScreen(ST7735_BLACK);


 
  // tft print function!
  tftPrintTest();
  
  

  // a single pixel
  tft.drawPixel(tft.width()/2, tft.height()/2, ST7735_GREEN);
  delay(500);

 


  

}

void loop() {

   
  while(Serial.available())
  {  
    
    str=Serial.read();
    Serial.print(str);

   
    
    if(str=='@')
     {
       tft.fillScreen(ST7735_BLACK);
       tft.setCursor(0,0);
       tft.print("ID     NAME    PRICE");
       while(1)
       {
         character = Serial.read();
         
         
         if (character =='#')
          {
            flag=0;
            break;
          }
  
          else if (character == ',')
          {
            tft.println(" ");
            Serial.println(" ");
          }
  
          else if (((character>='a' || character >'A') && (character <='z' || character <='Z')) || (character >='0' && character<='9') || character==' ' || character=='.')
          {
            tft.print(character);
            Serial.print(character);
          }
      }
      if(flag==0)
        break;
      
     }


    else if (str=='&')
      {
        
          Serial.println(" ");
          tft2.println(" ");
          String txid = Serial.readString();
          tft2.print(txid);
          break;
        
      }
  
   
  }

 

}





void tftPrintTest() {
  tft.setTextColor(ST7735_RED);
  tft2.setTextColor(ST7735_RED);
  tft.println("welcome to");
  tft.println("sagarmatha engineering college");
  tft2.println("SEC CANTEEN");
  tft2.println("Txid of items");
  

  
}
