#include <Arduino_FreeRTOS.h>

#define BAUD 115200

// define two tasks for Blink & AnalogRead
void read_adc(void *pvParameters);
//void TaskAnalogRead(void *pvParameters);

void setup(){
    Serial.begin(BAUD);

    // BaseType_t xTaskCreate(    TaskFunction_t pvTaskCode,
    //                            const char * const pcName,
    //                            unsigned short usStackDepth,
    //                            void *pvParameters,
    //                            UBaseType_t uxPriority,
    //                            TaskHandle_t *pxCreatedTask
    //                          );
    // priority : highest = 3, lowest = 0
    xTaskCreate(read_adc,  (const portCHAR *)"read_adc", 128,
        NULL, 1, NULL);
}

void loop(){
}

void read_adc(void *pvParameters __attribute__((unused))){
    pinMode(D, OUTPUT);
    const TickType_t xDelay = 50 / portTICK_PERIOD_MS;
    for (;;){
        int = analog0 = analogRead(A0);
        // block for 50 ms
        digitalWrite(D, LOW);
        vTaskDelay(xDelay);
        digitalWrite(D, HIGH);
        vTaskDelay(xDelay);
    }
}

// void serialEvent(){
//     // An interrupt on serial Rx.
//     // If an 'R' character is read, a reset will be triggered.
//     // If a 'T' character is read, a configuration string is expected
//     // and thus read, and then the configuration step is deferred to a
//     // new thread. (Idea for deferring from https://developer.mbed.org/
//     // blog/entry/Simplify-your-code-with-mbed-events/)
//     while (Serial.available()){
//         char input = (char)Serial.read();
//
//         if (input == 'R'){
//             reset();
//         }
//         // 'T' signals the beginning of the configuration string. In
//         // that case 14 more characters must be read.
//         else if (input == 'T'){
//             for (uint8_t i=0; i<14; i++){
//                 config_buffer[i] = (char)Serial.read();
//             }
//             // After reading the configuration string defer
//             // configuration to a different thread to release the main
//             // thread.
//             //TODO queue.call(&configure);
//         }
//     }
// }
