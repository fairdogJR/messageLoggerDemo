import visa
rm = visa.ResourceManager()
SCPI_M8070B = rm.open_resource('TCPIP0::localhost::inst0::INSTR')
idn = SCPI_M8070B.query('*IDN?')
SCPI_M8070B.write(':DATA:LINecoding:VALue "%s",%s' % ('M1.DataOut1', 'NRZ'))


print("\n****************** run testcase ******************************************************")
errorText1 = ""
print ("case1: Fails when pulse is set to 32 and then Pam4 coding is requested")
set = SCPI_M8070B.query(':DATA:SEQuence:SET? "%s"' % ('M1.DataOut1'))
SCPI_M8070B.write(':DATA:SEQuence:SET "%s",%s,"%s"' % ('M1.DataOut1', 'PULSE', '32'))
SCPI_M8070B.write(':DATA:LINecoding:VALue "%s",%s' % ('M1.DataOut1', 'PAM4'))

#get error count
temp_values = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:COUNt?')
print ("error count: ", int(temp_values[0]))

#get message
error_message = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:NEXT?', converter='s')

# individual messages are stored as a list so we have print everything so we get the whole message
for each in error_message:
	errorText1 = errorText1 + each
print("error text:", errorText1)

temp_values = SCPI_M8070B.query_ascii_values(':SYSTem:ERRor:COUNt?')
print ("error count: after reading one message ", int(temp_values[0]))