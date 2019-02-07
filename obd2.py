import obd
from obd import OBDStatus
import datetime

global speed
global fuelrates
global fueling_time
global obdconn
global trip_km

obddata = {
	'speed': 0, 
	'rpm': 0,
	'load': 0,
	'fuel_status': 0,
	'fuel_level': 0,
	'fuel_rate': 0,
	'engine_temp': 0,
	'oil_temp': 0,
	'throttle_pos': 0,
	'fuel_rates': 0,
	'fueling_time': 0 
}

fuelrates = []


obdconn = obd.Async()
'''
obdstatic = obd.OBD()
dtc = obdstatic.query(obd.commands.GET_CURRENT_DTC)
print(dtc)
obdstatic.close()
'''

def get_obd_data():
	return obddata

def get_connected():
	return obdconn.status()

def get_speed(data):
	if not data.is_null():
		obddata['speed'] = int(data.value.magnitude)

def get_rpm(data):
	if not data.is_null():
		obddata['rpm'] = int(data.value.magnitude)

def get_load(data):
	if not data.is_null():
		obddata['load'] = int(data.value.magnitude)

def get_fuel_status(data):
	if not data.is_null():
		obddata['fuel_status'] = int(data.value.magnitude)

def get_fuel_level(data):
	if not data.is_null():
		obddata['fuel_level'] = int(data.value.magnitude)

def get_engine_temp(data):
	if not data.is_null():
		obddata['engine_temp'] = int(data.value.magnitude)

def get_oil_temp(data):
	if not data.is_null():
		obddata['oil_temp'] = int(data.value.magnitude)

def get_throttle_pos(data):
	if not data.is_null():
		obddata['throttle_pos'] = int(data.value.magnitude)

def get_fuel_rate(data):
	if not data.is_null():
		obddata['fuel_rate'] = int(data.value.magnitude)
		fuel_rates.append(obddata['fuel_rate'])
		if(len(fuelrates) > 0):
			check_fueling(obddata['fuel_rate'])
	return fuel_rate

def check_fueling(fuel_rate):
	if fuel_rate > fuelrates[len(fuel_rates) - 1]:
		obddata['fueling_time'] = str(datetime.datetime.utcnow())
		print('Fueling detected at: ' + fueling_time)



if obdconn.status() == OBDStatus.NOT_CONNECTED:
	print('Obd not connected')

if obdconn.status() == OBDStatus.CAR_CONNECTED:
	obdconn.watch(obd.commands.SPEED, callback=get_speed)
	obdconn.watch(obd.commands.RPM, callback=get_rpm)
	obdconn.watch(obd.commands.ENGINE_LOAD, callback=get_load)
	obdconn.watch(obd.commands.FUEL_STATUS, callback=get_fuel_status)
	obdconn.watch(obd.commands.FUEL_LEVEL, callback=get_fuel_level)
	obdconn.watch(obd.commands.COOLANT_TEMP, callback=get_engine_temp)
	obdconn.watch(obd.commands.OIL_TEMP, callback=get_oil_temp)
	obdconn.watch(obd.commands.THROTTLE_POS, callback=get_throttle_pos)
	obdconn.watch(obd.commands.FUEL_RATE, callback=get_fuel_rate)
	obdconn.start()