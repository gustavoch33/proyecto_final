#include <xc.h>
#include "config.h"

#define _XTAL_FREQ 32000000

#include <stdio.h>

#define MD3 LATDbits.LATD1
#define MD2 LATDbits.LATD2
#define MD1 LATDbits.LATD3

#define MI3 LATFbits.LATF6
#define MI2 LATFbits.LATF5
#define MI1 LATFbits.LATF4

#define S3 PORTEbits.RE0
#define S2 PORTCbits.RC1
#define S1 PORTCbits.RC0

#define RT LATAbits.LATA6

int f = 40;
char dato[1] = "";

void servoI(int motor) {
    switch (motor) {
        case 3:
            for (int x = 0; x < f; x++) {
                ////Mover 0°
                MI3 = 1;
                __delay_us(700);
                MI3 = 0;
                __delay_ms(20);
            }
            __delay_ms(3400);
            for (int x = 0; x < f; x++) {
                ////Mover 180°
                MI3 = 1;
                __delay_us(2550);
                MI3 = 0;
                __delay_ms(20);
            }
            break;
        case 2:
            for (int x = 0; x < f; x++) {
                ////Mover 0°
                MI2 = 1;
                __delay_us(700);
                MI2 = 0;
                __delay_ms(20);
            }
            __delay_ms(2400);
            for (int x = 0; x < f; x++) {
                ////Mover 180°
                MI2 = 1;
                __delay_us(2550);
                MI2 = 0;
                __delay_ms(20);
            }
            break;
        case 1:
            for (int x = 0; x < f; x++) {
                ////Mover 0°
                MI1 = 1;
                __delay_us(700);
                MI1 = 0;
                __delay_ms(20);
            }
            __delay_ms(1000);
            for (int x = 0; x < f; x++) {
                ////Mover 180°
                MI1 = 1;
                __delay_us(2550);
                MI1 = 0;
                __delay_ms(20);
            }
            break;
    }
}

void servoD(int motor) {
    switch (motor) {
        case 3:
            for (int x = 0; x < 50; x++) {
                ////Mover 180°
                MD3 = 1;
                __delay_us(2550);
                MD3 = 0;
                __delay_ms(20);
            }
            __delay_ms(3400);
            for (int x = 0; x < f; x++) {
                ////Mover 0°
                MD3 = 1;
                __delay_us(600);
                MD3 = 0;
                __delay_ms(20);
            }
            break;
        case 2:
            for (int x = 0; x < f; x++) {
                ////Mover 180°
                MI2 = 1;
                __delay_us(2600);
                MI2 = 0;
                __delay_ms(20);
            }
            __delay_ms(2400);
            for (int x = 0; x < f; x++) {
                ////Mover 0°
                MI2 = 1;
                __delay_us(650);
                MI2 = 0;
                __delay_ms(20);
            }
            break;
        case 1:
            for (int x = 0; x < f; x++) {
                ////Mover 180°
                MI1 = 1;
                __delay_us(2600);
                MI1 = 0;
                __delay_ms(20);
            }
            __delay_ms(1000);
            for (int x = 0; x < f; x++) {
                ////Mover 0°
                MI1 = 1;
                __delay_us(650);
                MI1 = 0;
                __delay_ms(20);
            }
            break;
    }
}

void retirar(void) {
    for (int x = 0; x < 30; x++) {
        ////Mover 180°
        RT = 1;
        __delay_us(2525);
        RT = 0;
        __delay_ms(20);
    }
    for (int x = 0; x < 10; x++) {
        ////Mover 0°
        RT = 1;
        __delay_us(600);
        RT = 0;
        __deley_ms(20);
    }
}

void __interrupt(irq(U5RXB)) recepcion(void) {
    while (U5ERRIRbits.TXMTIF == 0);
    
    dato[0] = U5RXB;  //MXY
    
    /*
     * MG - A
     * MM - B
     * MC - C
     * VG - D
     * VM - E
     * VC - F
     * RT - R
     */
    
    if (dato[0] == 'R') {
        retirar();
    }
    
    U5TXB = dato[0];
    
    return;
}

void main(void) {
    OSCFRQbits.HFFRQ = 0b0110; //Frecuencia a 32MHz
    
    ANSELD = 0; //Coloca todos los pines como digitales
    ANSELF = 0;
    ANSELA = 0;
    ANSELC = 0;
    ANSELE = 0;
    
    LATD = 0;
    LATF = 0;
    LATA = 0;
    LATC = 0;
    LATE = 0;
    
    TRISD = 0; //SALIDAS A LOS SERVOS
    TRISF = 0; //SALIDAS A SERVOS Y UART
    TRISA = 0; //SALIDA PARA EL SERVO QUE RETIRA LA GUAYABA
    TRISEbits.TRISE0 = 1; //ENTRADA SENSOR
    TRISC = 0b00000011;
    
    WPUEbits.WPUE0 = 1;
    WPUC = 0b00000011;
    
    //CONFIGURACIÓN DE LA COMUNICACIÓN SERIAL
    ANSELF = 0; //LED
    TRISFbits.TRISF0 = 0; //TX
    TRISFbits.TRISF1 = 1; //RX
    RF0PPS = 0x2C;
    U5RXPPS = 0b00101001;
    U5CON0bits.BRGS = 0;
    U5CON0bits.TXEN = 1; //TRANSMISION
    U5CON0bits.RXEN = 1; //RECEPCION
    U5CON0bits.MODE = 0b0000; //8bits ASINCRONO
    U5CON1bits.ON = 1; //HABILITA PUERTO SERIE
    U5BRG = 207; //CALCULA MEDIANTE FORMULAS, VALOR ESPECIFICO PARA ESTA FRECUENCIA DE 32MHz
    PIR13bits.U5RXIF = 0; //NO SE PUEDE ESCRIBIR
    
    //CONFIGURAR LAS INTERRUPCIONES
    PIR13bits.U5RXIF = 0; //BANDERA EN 0
    PIE13bits.U5RXIE = 1; //HABILITAR INTERRUPCION POR LECTURA
    INTCON0bits.GIE = 1; //HABILITAR INTERRUPCION GLOBAL
    
    while (1) {
        //Derecha --> Maduras
        //Izquierda --> Verdes
        
        if (dato[0] == 'A') {
            //__delay_ms(1000);
            servoD(3);
        } else if (dato[0] == 'B') {
            //__delay_ms(1000);
            servoD(2);
        } else if (dato[0] == 'C') {
            //__delay_ms(1000);
            servoD(1);
        } else if (dato[0] == 'D') {
            //__delay_ms(1000);
            servoI(3);
        } else if (dato[0] == 'E') {
            //__delay_ms(1000);
            servoI(2);
        } else if (dato[0] == 'F') {
            //__delay_ms(1000);
            servoI(1);
        }
        __delay_us(10);
    }
}