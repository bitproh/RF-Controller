RF controller is a centralised autommated control panel for controlling the RF instruments.

This program comprises of the capability of controlling instruments such as keysight PSG signal generator and Spectrum analyzer.

For the proper working of the program the  following script files are mandatory.
1. Main.py
2. GA_test_sequence.py
3. SA_test_sequence.py
4. SG_test_sequence.py
5. utils.py

These are the mandatory files which directly get connected to the instruments and make a proper connection and establishes the application.

Before uploading the code, test the code and their working inputs by turning the live mode toggle on the main.py TRUE. which enables the test mode and runs a mock test on 
the device itself.
For running the mock test, the following files are mandatory:-

1. SA_test_mode.py
2. SG_test_mode.py
3. GA_test_mode.py

After making sure the inputs are correct turn the test mode toggle FALSE.

ALSO, make sure the visa resource address of your instrument matches the address in the known instruments array in the main.py

The files with the tail end _basic_sequence.py are only for checking the basic functionalities which include adjusting the frequency, power and center frequency.
