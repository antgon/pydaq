/* Data aquisition.

ADC data are sampled at regular intervals and sent to the master over
the serial port in data packets. Here, three ADC channels (pins A0, A1
and A2) are set-up as a working example. The system can easily be
modified to add or remove ADC channels as needed, and also to incoporate
data from other sources (e.g. SPI-connected hardware).


User settings
-------------

The user must:

(1) Define the correct BAUD rate to match that of the master. The
    default 115200 baud rate is probably a good choice.
(2) Set the right number of (analog) signals by (a) defining the
    required AnalogIn pins and their corresponding values, and (b)
    modifying the `read_adc` function so that those pins are read and
    their values are placed in the data buffer. Other data sources (e.g.
    SPI or 2-Wire) can be added in a similar way.


Summary
-------

Upon starting, the mbed will freeze while awaiting for serial input from
the master. (LED1 will be on.) This input must be a string of characters
of pre-defined format that will configure the mbed. Once this is
received, a string of characters will be sent back to the master to
verify the configuration and then the data aquisition will take place
periodically. (LED1 will switch off.)

If the character 'R' is received from the master at any time during data
acquisition the system will reset, thus freezing again the mbed again
until a new configuration input is received from the master.


Data output
-----------

Each data packet is structured so that the (16-bit) values are
concatenated as follows:

    0xffff
    0xffff
    adc0_sample_0
    adc1_sample_0
    adc2_sample_0
    adc0_sample_1
    adc1_sample_1
    adc2_sample_1
    ...
    adc0_sample_n
    adc1_sample_n
    adc2_sample_n

where n is `output_size` (calculated based on sampling frequency and
number of signals), and the first two 0xffff values are the header
that signals the beginning of a data packet. (Note that because serial
data must be sent as 8-bit values, the values above are split into two
bytes each upon sending, effectively sending twice as many bytes as
there are samples, but the master should be aware of this and unpack the
data accordingly.)

Principles of operation
-----------------------

* A vector of fixed size (BUFFER_SIZE) is initialised to a large, fixed
 value, e.g. 1024.

* Data are sent every 0.2 seconds. But to ensure that no samples are
  lost, this is not done based on time but on the number of samples
  acquired during that time. Fo example, if 3 signals are sampled at
  100 Hz, in 0.2 seconds there will be 20 samples per signal, or 60
  samples in total (0.2 * 100 * 3). In this case the data will be sent
  whenever the buffer completes the acquisition of 60 samples
  (`output_size`).

* TODO if somehow output_size is larger than BUFFER_SIZE the system will
  stop reading/sending data and instead a flashing led will be used to
  signal the error.


Caveats
-------

Using a header as above to signal the beginnning of the data packet
implies that two 16-bit values of 0xffff (i.e. four 0xff bits) will
never occur naturally in the data. This is only true if the resolution
of the data is 15 bits or less. For example, the resolution of the adc
in the mbed LPC1768 is 12 bits, so the maximum value that this can
produce is (2**12) - 1 = 0xfff, thus there will never be four sequential
0xff bits and the header works. The system is thus limited to reading
data encoded in 15 bits or less.
*/

#include "mbed.h"
Serial pc(USBTX, USBRX);
Ticker sampler;
Timer timer;
EventQueue queue;

/*********************
User-defined variables
**********************/

// Acquisition definitions.
#define BAUD 115200

// If defined, the ADC will not read data and instead timer values will
// be packed and sent. Useful for testing that data packing, sending,
// and unpacking work as expected.
//#define TEST

// Analog input variables. After setting these up, the `read_adc`
// function must be modified so that the values are read and added
// to the data buffer.
const uint8_t number_of_signals = 3;
AnalogIn analog_0(A0);
AnalogIn analog_1(A1);
AnalogIn analog_2(A2);
volatile uint16_t val_0 = 0;
volatile uint16_t val_1 = 0;
volatile uint16_t val_2 = 0;

// A digital pin configured in output mode and held up when the mbed
// is not configured or when it is reset (just as LED1). It will be
// pulled down when the mbed starts acquiring data. This pin can be used
// to synchronise e.g. video acquisition with the RPi.
#define CAMERA_PIN p21


/*************************
END user-defined variables
**************************/

// Acquisition variables.

// Fixed size of data aquistion buffer.
#define BUFFER_SIZE 1024
// Size of the output data buffer. Depends on configuration received
// from the master.
uint16_t output_size = 0;
// Initialise data acquisition buffer and related variables.
static uint16_t   data_buffer[2][BUFFER_SIZE];
volatile uint16_t buffer_index  = 0;
volatile bool     buffer_select = 0;
volatile bool     buffer_ready  = false;

// Configuration variables.
// `config_buffer` is a character array used for storing the
// configuration string sent by the master. This string is expected to
// be: 'T', datetime in seconds (10 digits), 'F', sampling frequency in
// Hz (3 digits), as in e.g. T1234567890F100 (15 chars). But the 'T'
// character is read by the serial interrupt to determine the beginning
// of the string, so the config_buffer is really 14 characters long
// (plus the null character at the end).
time_t seconds;
float sampling_freq;
char config_buffer[15];
volatile uint32_t timestamp = 0;

// An LED to signal 'waiting for configuration'.
DigitalOut led1(LED1);
#ifdef CAMERA_PIN
DigitalOut picamera(CAMERA_PIN);
#endif

// Function prototypes.
void serial_rx_interrupt();
void reset();
void configure();
void read_adc();
void send_data();


void read_adc(){
    // Reset timer at the beginning of the data buffer.
    if (buffer_index == 0){
        timestamp += timer.read_ms();
        timer.reset();
    }
#ifdef TEST
    // A good trick to test the system without an analog signal is
    // to send the time (`timestamp` measured by the timer), split
    // into two. When the master reads these data the fidelity of
    // the packing, sending, and unpacking of the bytes can be
    // confirme visually: val_0 should increment every BUFFER_SIZE,
    // resetting to 0 when it reaches 0xffff, and val_1 should
    // increment by one when val_0 resets. A fixed value on val_2 is
    // used to check that there's no cross-over between signals when
    // the data are unpacked.
    val_0 = (uint16_t)(timestamp & 0xffff);
    val_1 = (uint16_t)(timestamp >> 16);
    val_2 = 3000;
#else
    // Read samples.
    val_0 = analog_0.read_u16();
    val_1 = analog_1.read_u16();
    val_2 = analog_2.read_u16();

    // The ADC has a 12-bit resolution but the reading operation
    // returns the voltage normalised to 16 bits. To convert back to
    // the original 12-bit value, shift as below.
    val_0 = ((val_0) >> 4) & 0xfff;
    val_1 = ((val_1) >> 4) & 0xfff;
    val_2 = ((val_2) >> 4) & 0xfff;
    // (According to this post https://developer.mbed.org/questions/
    // 61297/ADC-normalized-number-in-LPC1768 the operation should
    // be
    //   val_2 = ((val_2 >> 4) | (val_2 << 8)) & 0xfff;
    // but the result is the same if the value is simply right
    // shifted by 4.)
#endif
    // Move samples to data buffer.
    data_buffer[buffer_select][buffer_index] = val_0; buffer_index++;
    data_buffer[buffer_select][buffer_index] = val_1; buffer_index++;
    data_buffer[buffer_select][buffer_index] = val_2; buffer_index++;

    // Raise flag if the buffer is ready to be sent.
    if (buffer_index == output_size){
        buffer_index = 0;
        buffer_ready = true;
        buffer_select = !buffer_select;
    }
}

void send_data(){
    // Header.
    pc.putc(0xff);
    pc.putc(0xff);
    pc.putc(0xff);
    pc.putc(0xff);
    // Timestamp.
    // pc.putc((uint8_t)(timestamp & 0xff));
    // pc.putc((uint8_t)(timestamp >> 8));
    // pc.putc((uint8_t)(timestamp >> 16));
    // pc.putc((uint8_t)(timestamp >> 24));
    // Data buffer.
    for (uint16_t i = 0; i < output_size; i++){
        pc.putc((uint8_t)(data_buffer[!buffer_select][i] & 0xff));
        pc.putc((uint8_t)(data_buffer[!buffer_select][i] >> 8));
    }
}

void serial_rx_interrupt(){
    // An interrupt on serial Rx.
    // If an 'R' character is read, a reset will be triggered.
    // If a 'T' character is read, a configuration string is expected
    // and thus read, and then the configuration step is deferred to a
    // new thread. (Idea for deferring from https://developer.mbed.org/
    // blog/entry/Simplify-your-code-with-mbed-events/)
    while (pc.readable()){
        char input = pc.getc();

        if (input == 'R'){
            reset();
        }
        // 'T' signals the beginning of the configuration string. In
        // that case 14 more characters must be read.
        else if (input == 'T'){
            for (uint8_t i=0; i<14; i++){
                config_buffer[i] = pc.getc();
            }
            // After reading the configuration string deferr
            // configuratione to a different thread to release the main
            // thread.
            queue.call(&configure);
        }
    }
}

void reset(){
    // Reset variables.
    sampler.detach();
    output_size = 0;
    buffer_index  = 0;
    buffer_select = 0;
    buffer_ready  = false;
    led1 = 1;
#ifdef CAMERA_PIN
    picamera = 1;
#endif
}

void configure() {
    // Get configuration variables.
    sscanf(config_buffer, "%liF%f", &seconds, &sampling_freq);

    // Set-up time and timer.
    set_time(seconds);
    timer.start();

    // `output_size` is the number of sample size in each data packet
    // sent to the master. It is calculated so any samples acquired
    // every 0.2 seconds are sent, based on the sampling frequency.
    // To avoid missing samples it is critical that this value is a
    // multiple of the number of signals.
    //
    // What to do if (freq * saving_period * nsignals) is not an
    // integer, e.g. as in sampling_freq = 118, (118 * 0.2 * 3 = 70.8)?
    // The  solution is to cast to integer before multiplying by
    // number_of_signals; that way the result will always be an integer
    // exact multiple of number_of_signals.
    output_size = (uint16_t)(sampling_freq * 0.2) * number_of_signals;
    // If the sampling frequency is too low the operation above will
    // result in 0; for example, if sampling_freq is 1 Hz,
    // int(1 * 0.2) = 0. These lines avoid that situation.
    if (output_size == 0){
        output_size = number_of_signals;
    }

    // Send back the received values to the master for confirmation.
    pc.printf("%i %3.0f %u\n", seconds, sampling_freq, output_size);

    // Start ticker. 'Ticker.attach' takes the interval value in seconds
    // (float), thus the inverse of the sampling frequency.
    sampler.attach(&read_adc, 1/sampling_freq);

    // Switch off led to indicate that configuration has taken place and
    // data acquisition is in progress.
    led1 = 0;
#ifdef CAMERA_PIN
    picamera = 0;
#endif
}

int main(){
    pc.baud(BAUD);
    // Switch on 'waiting for configuration' led.
    led1 = 1;
#ifdef CAMERA_PIN
    picamera = 1;
#endif

    // Set-up an interrupt on serial Rx. An 'R' character will trigger a
    // reset/configuration in a new thread.
    Thread eventThread;
    eventThread.start(callback(&queue, &EventQueue::dispatch_forever));
    pc.attach(&serial_rx_interrupt, Serial::RxIrq);

    while(1){
        // Check regularly to see if the data buffer is full. If it is
        // send it to the master.
        if (buffer_ready == true){
            send_data();
            buffer_ready = false;
        }
    }
}
