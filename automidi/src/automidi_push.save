#include <Control_Surface.h> // Include the Control Surface library
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, 47, NEO_GRB + NEO_KHZ800);

/*
// Custom callback to handle output for a selector.
class MySelectorCallback {
 public:
  // Constructor
  MySelectorCallback(pin_t redLED, pin_t greenLED, pin_t blueLED)
    : redLED(redLED), greenLED(greenLED), blueLED(blueLED) {}
 
  // Begin function is called once by Control Surface.
  // Use it to initialize everything.
  void begin() {
    pinMode(redLED, OUTPUT);
    pinMode(greenLED, OUTPUT);
    pinMode(blueLED, OUTPUT);
    show(0);
  }
 
  // Update function is called continuously by Control Surface.
  // Use it to implement things like fading, blinking ...
  void update() {}
 
  // Update function with arguments is called when the setting
  // changes.
  // Use it to update the LEDs.
  void update(setting_t oldSetting, setting_t newSetting) {
    (void)oldSetting; // unused in this example
    show(newSetting);
  }
 
 private:
  // Show the color of the given setting.
  void show(setting_t setting) {
    uint8_t color = getColor(setting);
    digitalWrite(redLED, color & 0b001 ? HIGH : LOW);
    digitalWrite(greenLED, color & 0b010 ? HIGH : LOW);
    digitalWrite(blueLED, color & 0b100 ? HIGH : LOW);
  }
 
  // Convert the given setting to a 3-bit RGB color value.
  static uint8_t getColor(setting_t setting) {
    switch (setting) {
      case 0: return 0b001;
      case 1: return 0b011;
      case 2: return 0b010;
      case 3: return 0b110;
      case 4: return 0b100;
      case 5: return 0b101;
      default: return 0b000;
    }
  }
 
 private:
  // Member variables to remember the pin numbers of the LEDs.
  pin_t redLED, greenLED, blueLED;
};
*/

// Instantiate a MIDI over USB interface.
USBMIDI_Interface midi;
bool oldstate1;
bool oldstate2;
bool oldstate3;
bool oldstate4;

// Instantiate a CCButton object
CCButtonLatched button1 {
  // Push button on pin 10:
  10,
  // General Purpose Controller #1 on MIDI channel 1:
  {MIDI_CC::General_Purpose_Controller_1, Channel_1},
};

CCButtonLatched button2 {
  11,{MIDI_CC::General_Purpose_Controller_1, Channel_2},
};
CCButtonLatched button3 {
  13,{MIDI_CC::General_Purpose_Controller_1, Channel_3},
};
CCButtonLatched button4 {
  12,{MIDI_CC::General_Purpose_Controller_1, Channel_4},
};

void setup() {
  Control_Surface.begin(); // Initialize Control Surface
  oldstate1=button1.getState();
  oldstate2=button2.getState();
  oldstate3=button3.getState();
  oldstate4=button4.getState();

  pixels.begin();            //INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear();            // Turn OFF all pixels ASAP
  pixels.setBrightness(25);  // Set BRIGHTNESS (max = 255)
  pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  pixels.show();  
  delay(1000);
  pixels.setPixelColor(0, pixels.Color(0, 255, 0));
  pixels.show();  
  delay(1000);
  pixels.setPixelColor(0, pixels.Color(0, 0, 255));
  pixels.show();  
  delay(1000);  
}
 
void loop() {
  Control_Surface.loop(); // Update the Control Surface
  bool state;
  state=button1.getState();
  if (oldstate1 != state){
    oldstate1=state;
    if (state){
      pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    }else{
      pixels.setPixelColor(0, pixels.Color(255, 255, 255));      
    }
    pixels.show();  
  }

  state=button2.getState();
  if (oldstate2 != state){
    oldstate2=state;
    if (state){
      pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    }else{
      pixels.setPixelColor(0, pixels.Color(255, 255, 255));      
    }
    pixels.show();  
  }

  state=button3.getState();
  if (oldstate3 != state){
    oldstate3=state;
    if (state){
      pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    }else{
      pixels.setPixelColor(0, pixels.Color(255, 255, 255));      
    }
    pixels.show();  
  }

  state=button4.getState();
  if (oldstate4 != state){
    oldstate4=state;
    if (state){
      pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    }else{
      pixels.setPixelColor(0, pixels.Color(255, 255, 255));      
    }
    pixels.show();  
  }
}


/*
  This example will show how to use a switch to toggle between two different
  MIDI messages. It could allow a switch to toggle START and STOP for example.
*/
/*
#include "MIDIcontroller.h"

const int switchPin = 2; 
bool state = false;

MIDIswitch myInput(switchPin, START); // Don't use LATCH

void setup(){
  pinMode(ledPin, OUTPUT);
}

void loop(){
  if ( myInput.send() > -1) { // no input == -1
    state = !state;
    if (state) myInput.setControlNumber(STOP);
    else myInput.setControlNumber(START);
  }

  digitalWrite(ledPin, state); // LED indicates state


// This prevents crashes that happen when incoming usbMIDI is ignored.
  while(usbMIDI.read()){}

// Also uncomment this if compiling for standard MIDI
//  while(MIDI.read()){}
}
/*
#include <Control_Surface.h> // Include the Control Surface library
 
// The MIDI over USB interface to use
USBMIDI_Interface midi;
 
void setup() {
  midi.begin(); // Initialize the MIDI interface
}
 
// MIDI note number, channel, and velocity to use
const MIDIAddress address {MIDI_Notes::C[4], Channel_1};
const uint8_t velocity = 0x7F;
 
void loop() {
  midi.sendNoteOn(address, velocity);
  delay(500);
  midi.sendNoteOff(address, velocity);
  delay(500);
 
  midi.update(); // Handle or discard MIDI input
}

/*
#include <Control_Surface.h> // Include the Control Surface library
 
// Instantiate a MIDI over USB interface.
USBMIDI_Interface midi;
 
// Instantiate a CCButton object
CCButton button1 {
  // Push button on pin 5:
  5,
  // General Purpose Controller #1 on MIDI channel 1:
  {MIDI_CC::General_Purpose_Controller_1, Channel_1},
};

CCButton button2 {
  // Push button on pin 6:
  6,
  // General Purpose Controller #1 on MIDI channel 1:
  {MIDI_CC::General_Purpose_Controller_1, Channel_1},
};

CCButton button3 {
  // Push button on pin 7:
  7,
  // General Purpose Controller #1 on MIDI channel 1:
  {MIDI_CC::General_Purpose_Controller_1, Channel_1},
};

void setup() {
  Control_Surface.begin(); // Initialize Control Surface
}
 
void loop() {
  Control_Surface.loop(); // Update the Control Surface
}
*/
