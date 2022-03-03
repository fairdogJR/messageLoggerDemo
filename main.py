#message logger processing example Tim Fairfield  03/03/2022
#please use this with M8070B v8.5.380.14 or higher
import visa
import readm8070bLogfile
rm = visa.ResourceManager()
SCPI_M8070B = rm.open_resource('TCPIP0::localhost::inst0::INSTR')
idn = SCPI_M8070B.query('*IDN?')
print (idn) # sanity check

def process_error_queue():
    global temp_values, totalErrorCount, errorText1, errorNumber1, each
    temp_values = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:COUNt?')
    totalErrorCount = int(temp_values[0])
    while totalErrorCount > 0:
        errorText1 = ""
        print("error queue count:", totalErrorCount)
        temp_values = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:NEXT?', converter='s')
        errorNumber1 = int(temp_values[0])
        temp_values2 = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:COUNt?')
        totalErrorCount = int(temp_values2[0])
        for each in temp_values:
            errorText1 = errorText1 + each
        print("error text:", errorText1)

# case1: Fails when pulse is set to 32 and then Pam4 coding is requested
print("\n************************************************************************")
print ("case1: Fails when pulse is set to 32 and then Pam4 coding is requested")
set = SCPI_M8070B.query(':DATA:SEQuence:SET? "%s"' % ('M1.DataOut1'))
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PULSE', '32'))
SCPI_M8070B.write(':DATA:LINecoding:VALue "%s",%s' % ('M1.DataOut1', 'PAM4'))
temp_values = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:COUNt?')

process_error_queue()


# case2: Fails when Pam4 coding is set and pulse  pattern type which is unsupported is requested
print("\n************************************************************************")
print ("case2: Fails when Pam4 coding is set and pulse  pattern type which is unsupported is requested")
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PRBS', '2^13-1'))
set1 = SCPI_M8070B.query(':DATA:SEQuence:SET? "%s"' % ('M1.DataOut1'))
SCPI_M8070B.write(':DATA:LINecoding:VALue "%s",%s' % ('M1.DataOut1', 'PAM4'))
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PULSE', '32'))
#
process_error_queue()


# case3  where multiple errors in queue
print("\n**************Important to iterate through all entries as there may be many queued****************************")
print("\n**************This should  be part of the error interrogation routine             ****************************")
print ("case3: where multiple errors in queue")
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PRBS', '2^13-1'))
set1 = SCPI_M8070B.query(':DATA:SEQuence:SET? "%s"' % ('M1.DataOut1'))
SCPI_M8070B.write(':DATA:LINecoding:VALue "%s",%s' % ('M1.DataOut1', 'PAM4'))
#purposely load up error queue
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PULSE', '32'))
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PULSE', '32'))
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PULSE', '32'))


#process the error queue
process_error_queue()

SCPI_M8070B.close()
rm.close()

#look through the log file for errors
readm8070bLogfile.getErrorinfo( r'C:\Users\fairfiel.KEYSIGHT\AppData\Local\Keysight\M8070B')
# end

