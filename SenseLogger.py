from sense_hat import SenseHat
from datetime import datetime
import time

### Logging settings ###

FILENAME = ""
WRITE_FREQUENCY = 10 #100

### Functions ###

def file_setup(filename):
	header = ["temp_h", "temp_p", "humidity", "pressure", "pitch", "roll", "yaw", "mag_x", "mag_y", "mag_z", "accel_x","accel_y","accel_z","gyro_x","gyro_y","gyro_z","timestamp"]
	
	with open(filename,"w") as f:
		f.write(" , ".join(str(value) for value in header)+ "\n")
		

def log_data():

	output_string = " , ".join(str(value) for value in sense_data)
	batch_data.append(output_string)
	
	
def get_sense_data():
	sense_data =[]
	
	sense_data.append(round(sense.get_temperature_from_humidity(), 4))
	sense_data.append(round(sense.get_temperature_from_pressure(), 4))
	sense_data.append(round(sense.get_humidity(), 4))
	sense_data.append(round(sense.get_pressure(), 4))
	
	
	yaw, pitch, roll = sense.get_orientation().values()
	sense_data.extend([round(pitch, 4), round(roll, 4), round(yaw, 4)])
	
	
	mag_x, mag_y, mag_z = sense.get_compass_raw().values()
	sense_data.extend([round(mag_x, 4), round(mag_y, 4), round(mag_z, 4)])
	
	
	x, y, z = sense.get_accelerometer_raw().values()
	sense_data.extend([round(x, 4),round(y, 4),round(z, 4)])
	
	
	gyro_x, gyro_y, gyro_z = sense.get_gyroscope_raw().values()
	sense_data.extend([round(gyro_x, 4), round(gyro_y, 4), round(gyro_z, 4)])
	
	
	sense_data.append(datetime.now())
	
	return sense_data
	
	
### MAIN ###

sense = SenseHat()
batch_data = []

if FILENAME == "":
	filename = "SenseLog-"+str(datetime.now())+".csv"
else:
	filename = FILENAME+"-"+str(datetime.now())+".csv"
	
file_setup(filename)

while True:
	sense_data = get_sense_data()
	log_data()
	
	if len(batch_data) >= WRITE_FREQUENCY:
		print("Writing to file...")
		with open(filename,"a") as f:
			for line in batch_data:
				f.write(line + "\n")
		batch_data = []
		
	print("Daten erfasst und geloggt")
	time.sleep(5)