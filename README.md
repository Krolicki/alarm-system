System alarmowy - Raspberry Pi

**Elementy systemu:**

 - Raspberry Pi 4b 2GB
 - Czujnik ruchu HC-SR501
 - Moduł RFID MF RC522 
 - Buzzer z generatorem FY248
 - Czujnik magnetyczny otwarcia drzwi/okien CMD14
 - 3x Dioda LED (czerwona, zielona ,żółta)

**Czujnik ruchu:**
 - zasilanie 5V - PIN 2 PWR
 - sygnał - GPIO 18 (PIN 12)
 - masa - PIN 14

**Buzzer:**
 - "+" - GPIO 4 (PIN 7)
 - "-" - PIN 9

**Czujnik otwarcia (polaryzacja dowolna):**
 - GPIO 12 (PIN 32)
 - masa - PIN 34

**Diody LED:**
 - Czerwona - GPIO 26 (PIN 37)
 - Zielona - GPIO 13 (PIN 33)
 - Żółta - GPIO 6 (PIN 31)
 - Masa układu - PIN 39
Do każdej diody dodany rezystor 100 Ω (Ohm) 1/4W

**Moduł RFID:**
 - SDA - GPIO 7 (PIN 26) - SPI0 CS1
 - SCK - GPIO 11 (PIN 23) - SPI0 SCLK
 - MOSI - GPIO 10 (PIN 19) - SPI0 MOSI
 - MISO - GPIO 9 (PIN 21) - SPI0 MISO
 - GND - PIN 25
 - RST - GPIO 25 (PIN 22)
 - zasilanie 3.3V - PIN 17 PWR
 - IQR - nieużywany
Do działania należy włączyć interfejs SPI:
sudo raspi-config -> (3)Interface... -> (I4)SPI -> Yes
sudo reboot
