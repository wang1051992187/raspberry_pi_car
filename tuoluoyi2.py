import smbus


class acc_LSM303DLHC(object):

	__ctrl_reg1_a				= 0x18
	__ctrl_reg4_a				= 0x1e

	def __init__(self, slave_address):
		self.bus = smbus.SMBus(1)
		self.acc_address = slave_address
		self.bus.write_byte_data(self.acc_address, self.__ctrl_reg1_a, 0x27)
		self.bus.write_byte_data(self.acc_address, self.__ctrl_reg4_a, 0x00)

	def get_x_acc(self):
		msb = self.bus.read_byte_data(self.acc_address,0x29)
		lsb = self.bus.read_byte_data(self.acc_address,0x28)
		x_acc = msb*256 + lsb
		if x_acc > 32767:
			x_acc -= 65536
		x_acc = self.set_scale(x_acc,2)
		return x_acc

	def get_y_acc(self):
		msb = self.bus.read_byte_data(self.acc_address,0x2a)
		lsb = self.bus.read_byte_data(self.acc_address,0x2b)
		y_acc = msb*256 + lsb
		if y_acc > 32767:
			y_acc -= 65536
		y_acc = self.set_scale(y_acc,2)
		return y_acc

	def get_z_acc(self):
		msb = self.bus.read_byte_data(self.acc_address,0x2c)
		lsb = self.bus.read_byte_data(self.acc_address,0x2d)
		# msb = self.two_complement_to_byte(msb)
		z_acc = msb*256 + lsb
		if z_acc > 32767:
			z_acc -= 65536
		z_acc = self.set_scale(z_acc,2)
		return z_acc

	def get_acc_data(self):
		acc_data = [self.get_x_acc(), self.get_y_acc(), self.get_z_acc()]
		return acc_data

	def set_scale(self, sensor_value, scale):
		return sensor_value*(scale/32768.0)

	def two_complement_to_byte(self, value):
	    if value >= 0 and value <= 127:
	        return value
	    else:
	        return value - 256

if __name__ == '__main__':
    lsm = acc_LSM303DLHC()
    x = lsm.get_x_acc()
    y = lsm.get_y_acc()
    z = lsm.get_z_acc()

    print("磁场：x:",x,"y:",y,'z:',z,'\n')

    print("加速度:",lsm.get)