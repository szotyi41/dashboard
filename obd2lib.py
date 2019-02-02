import obd

global obdconn
global trip_km
obdconn = obd.Async()
'''
obdstatic = obd.OBD()
dtc = obdstatic.query(obd.commands.GET_CURRENT_DTC)
print(dtc)
obdstatic.close()
'''
def get_connected():
	return obdconn.status()

def get_speed(data):
	global speed
	if not data.is_null():
		speed = int(data.value.magnitude)
		return speed

def get_rpm(data):
	global rpm
	if not data.is_null():
		rpm = int(data.value.magnitude)
		return rpm

def get_load(data):
	global load
	if not data.is_null():
		load = int(data.value.magnitude)
		return load

def get_fuel_status(data):
	global fuel_status
	if not data.is_null():
		fuel_status = int(data.value.magnitude)
		return fuel_status

def get_fuel_level(data):
	global fuel_level
	if not data.is_null():
		fuel_level = int(data.value.magnitude)
		return fuel_level

def get_engine_temp(data):
	global engine_temp
	if not data.is_null():
		engine_temp = int(data.value.magnitude)
		return engine_temp

def get_oil_temp(data):
	global oil_temp
	if not data.is_null():
		oil_temp = int(data.value.magnitude)
		return oil_temp

def get_throttle_pos(data):
	global throttle_pos
	if not data.is_null():
		throttle_pos = int(data.value.magnitude)
		return throttle_pos

def get_fuel_rate(data):
	global fuel_rate
	if not data.is_null():
		fuel_rate = int(data.value.magnitude)
		return fuel_rate

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
