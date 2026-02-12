#include <Control_Surface.h> // Include the Control Surface library
#include <Adafruit_NeoPixel.h>

#define POLLINGTIME 10000

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, 47, NEO_RGB + NEO_KHZ800);

// Instantiate a MIDI over USB interface.
USBMIDI_Interface midi;

// Instantiate a CCButton object
CCButton button {
  // Push button on pin 10:
  10,
  // General Purpose Controller #1 on MIDI channel 1:
  {MIDI_CC::General_Purpose_Controller_1, Channel_1},
};

uint32_t polling;
bool first=true;
bool error=false;
volatile uint32_t pingtime;
uint32_t oldcolor= 0;
  bool state;

// Custom MIDI callback that prints incoming messages.
struct MyMIDI_Callbacks : MIDI_Callbacks {
 
  // Callback for channel messages (notes, control change, pitch bend, etc.).
  void onChannelMessage(MIDI_Interface &, ChannelMessage cm) override {
    pingtime=millis();
    //midi.read();
    //midi.getChannelMessage();
  }
   // Callback for system exclusive messages
  void onSysExMessage(MIDI_Interface &, SysExMessage se) override {
    pingtime=millis();
  }
 
  // Callback for real-time messages
  void onRealTimeMessage(MIDI_Interface &, RealTimeMessage rt) override {
    pingtime=millis();
  } 
} callback;

void setup() {

  //button.begin();
  Control_Surface.begin(); // Initialize Control Surface
  //midi.begin(); // Initialize Control Surface
  midi.setCallbacks(callback); // Attach the custom callback
  midi.alwaysSendImmediately();
  
  pixels.begin();            //INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear();            // Turn OFF all pixels ASAP
  pixels.show();  
  pixels.setBrightness(255);  // Set BRIGHTNESS (max = 255)
  pixels.setPixelColor(0, 255, 0, 0);
  pixels.show();  
  delay(1000);
  pixels.setPixelColor(0, 0, 255, 0);
  pixels.show();  
  delay(1000);
  pixels.setPixelColor(0, 0, 0, 255);
  pixels.show();  
  delay(1000);
  pixels.clear();            // Turn OFF all pixels ASAP
  pixels.show();  
  delay(1000);

  Control_Surface.begin();
  Control_Surface.loop(); // Update the Control Surface
  //midi.begin(); // Initialize Control Surface
  //midi.update();
  //button.update();
  state=button.getButtonState();
  
  if (state){
    pixels.setPixelColor(0, 0, 0, 255);      
  }else{
    pixels.setPixelColor(0, 0, 255, 0);
  }
  pixels.show();  
  polling=millis();
  pingtime=millis();

}
 
void loop() {
  
  error=(millis() - pingtime) >= (2*POLLINGTIME);

  while (not first && (millis() < (polling + POLLINGTIME))){
    Control_Surface.loop(); // Update the Control Surface
    //midi.update();
    //button.update();
    state=button.getButtonState();

    if (error){
      pixels.setPixelColor(0, 255, 0, 0);
    }else{
      if (state){
	pixels.setPixelColor(0, 0, 0, 255);      
      }else{
	pixels.setPixelColor(0, 0, 255, 0);
      }
    }

   uint32_t color= pixels.getPixelColor(0);
   if (oldcolor != color){
     pixels.show();
     oldcolor=color;
   }
  }
  
  uint8_t value;
  if(state) {
    value=0;
  }else{
    value=0x7F;
  }
  
  Control_Surface.sendControlChange ({MIDI_CC::General_Purpose_Controller_1, Channel_1}, value);
  //midi.sendControlChange ({MIDI_CC::General_Purpose_Controller_1, Channel_1}, value);
  //midi.sendNow();

  Control_Surface.loop(); // Update the Control Surface  
  //midi.update();
  //button.update();
  
  first=false;
  polling=millis();
}
