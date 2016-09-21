# Bill Marty's code to test Matthew West's adc.py

import adc
import time

#Which pin are we reading?
pin = 'P9_38'

print('Calling setup().')
adc.setup()
if adc.adc_setup:
    print('Setup returned adc_setup = True.' )
else:
    print('Setup returned adc_setup = False.')

print('Reading P9_38:')
for n in [10]:
    time.sleep(0.5)
    volts = adc.read_volts(pin)
    adc_count = read_raw(pin)
    print(str(pin) + ': volts = ' + str(volts) + ', counts = ' + str(adc_count))
