#include"rfid2.h"
RFID1 rfid;

uchar serNum[5];  // array to store your ID
int incomingByte = 0;   // for incoming serial data

void setup()
{
  Serial.begin(9600);
  pinMode(10, OUTPUT);

  rfid.begin(7, 5, 4, 3, 6, 2);  
  delay(100);
  rfid.init();

}
void loop()
{
  digitalWrite(10, HIGH);
  uchar status;
  uchar str[MAX_LEN];
  String hello;
  status = rfid.request(PICC_REQIDL, str);
  if (status != MI_OK)
  {
    return;
  }
  
  status = rfid.anticoll(str);
  
  if (status == MI_OK)
  {
    if (Serial.available()) {
        char serialListener = Serial.read();
        if (serialListener == 'H') {
            digitalWrite(10, LOW);
            delay(300000);
        }
    }
    Serial.print("Number: ");
    memcpy(serNum, str, 5);
    rfid.showCardID(serNum);
    Serial.println();
    Serial.println();
  }  
  delay(500);
   
  rfid.halt(); //command the card into sleep mode 
}
