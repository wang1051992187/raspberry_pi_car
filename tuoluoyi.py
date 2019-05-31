"""
    陀螺仪
    资料http://m.elecfans.com/article/591397.html
"""
import smbus
import time
import math

bus = smbus.SMBus(1)

LSM303_ADDRESS_ACCEL = 0x18  # Default Accel address
LSM303_ADDRESS_MAG = 0x1e  # Default Mag address

# Accel registers

LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20  # 00000111   rw
LSM303_REGISTER_ACCEL_CTRL_REG2_A = 0x21  # 00000000   rw
LSM303_REGISTER_ACCEL_CTRL_REG3_A = 0x22  # 00000000   rw
LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23  # 00000000   rw
LSM303_REGISTER_ACCEL_CTRL_REG5_A = 0x24  # 00000000   rw
LSM303_REGISTER_ACCEL_CTRL_REG6_A = 0x25  # 00000000   rw
LSM303_REGISTER_ACCEL_REFERENCE_A = 0x26  # 00000000   r
LSM303_REGISTER_ACCEL_STATUS_REG_A = 0x27  # 00000000   r
LSM303_REGISTER_ACCEL_OUT_X_L_A = 0x28
LSM303_REGISTER_ACCEL_OUT_X_H_A = 0x29
LSM303_REGISTER_ACCEL_OUT_Y_L_A = 0x2A
LSM303_REGISTER_ACCEL_OUT_Y_H_A = 0x2B
LSM303_REGISTER_ACCEL_OUT_Z_L_A = 0x2C
LSM303_REGISTER_ACCEL_OUT_Z_H_A = 0x2D
LSM303_REGISTER_ACCEL_FIFO_CTRL_REG_A = 0x2E
LSM303_REGISTER_ACCEL_FIFO_SRC_REG_A = 0x2F
LSM303_REGISTER_ACCEL_INT1_CFG_A = 0x30
LSM303_REGISTER_ACCEL_INT1_SOURCE_A = 0x31
LSM303_REGISTER_ACCEL_INT1_THS_A = 0x32
LSM303_REGISTER_ACCEL_INT1_DURATION_A = 0x33
LSM303_REGISTER_ACCEL_INT2_CFG_A = 0x34
LSM303_REGISTER_ACCEL_INT2_SOURCE_A = 0x35
LSM303_REGISTER_ACCEL_INT2_THS_A = 0x36
LSM303_REGISTER_ACCEL_INT2_DURATION_A = 0x37
LSM303_REGISTER_ACCEL_CLICK_CFG_A = 0x38
LSM303_REGISTER_ACCEL_CLICK_SRC_A = 0x39
LSM303_REGISTER_ACCEL_CLICK_THS_A = 0x3A
LSM303_REGISTER_ACCEL_TIME_LIMIT_A = 0x3B
LSM303_REGISTER_ACCEL_TIME_LATENCY_A = 0x3C
LSM303_REGISTER_ACCEL_TIME_WINDOW_A = 0x3D

# Mag registers

LSM303_REGISTER_MAG_CRA_REG_M = 0x00
LSM303_REGISTER_MAG_CRB_REG_M = 0x01
LSM303_REGISTER_MAG_MR_REG_M = 0x02
LSM303_REGISTER_MAG_OUT_X_H_M = 0x03
LSM303_REGISTER_MAG_OUT_X_L_M = 0x04
LSM303_REGISTER_MAG_OUT_Z_H_M = 0x05
LSM303_REGISTER_MAG_OUT_Z_L_M = 0x06
LSM303_REGISTER_MAG_OUT_Y_H_M = 0x07
LSM303_REGISTER_MAG_OUT_Y_L_M = 0x08
LSM303_REGISTER_MAG_SR_REG_Mg = 0x09
LSM303_REGISTER_MAG_IRA_REG_M = 0x0A
LSM303_REGISTER_MAG_IRB_REG_M = 0x0B
LSM303_REGISTER_MAG_IRC_REG_M = 0x0C
LSM303_REGISTER_MAG_TEMP_OUT_H_M = 0x31
LSM303_REGISTER_MAG_TEMP_OUT_L_M = 0x32

# LSM303_REGISTER_MAG_CRB_REG_M (Mag Gain) values

LSM303_MAGGAIN_1_3 = 0x20,  # +/- 1.3
LSM303_MAGGAIN_1_9 = 0x40,  # +/- 1.9
LSM303_MAGGAIN_2_5 = 0x60,  # +/- 2.5
LSM303_MAGGAIN_4_0 = 0x80,  # +/- 4.0
LSM303_MAGGAIN_4_7 = 0xA0,  # +/- 4.7
LSM303_MAGGAIN_5_6 = 0xC0,  # +/- 5.6
LSM303_MAGGAIN_8_1 = 0xE0  # +/- 8.1


def WRITE_ACCEL(register, value):
    bus.write_byte_data(LSM303_ADDRESS_ACCEL, register, value)
    return -1


def WRITE_MAG(register, value):
    bus.write_byte_data(LSM303_ADDRESS_MAG, register, value)
    return -1


def READ_ACCEL(register):
    bus.read_byte_data(LSM303_ADDRESS_ACCEL, register)
    return -1


def READ_MAG(register):
    bus.read_byte_data(LSM303_ADDRESS_MAG, register)
    return -1


def accelDatax():
    gxhi = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_OUT_X_L_A)
    gxlo = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_OUT_X_H_A)
    gxtotal = ((gxhi << 8) | gxlo)
    return gxtotal


def accelDatay():
    gyhi = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_OUT_Y_L_A)
    gylo = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_OUT_Y_H_A)
    gytotal = ((gyhi << 8) | gylo)
    return gytotal


def accelDataz():
    gzhi = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_OUT_Z_L_A)
    gzlo = bus.read_byte_data(LSM303_ADDRESS_ACCEL, LSM303_REGISTER_ACCEL_OUT_Z_H_A)
    gztotal = ((gzhi << 8) | gzlo)
    return gztotal


def accelDataTotal():
    gtotal = (((accelDatax() ** 2) + (accelDatay() ** 2) + (accelDataz() ** 2)) ** 0.5)
    return gtotal


def magDatax():
    hxhi = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_OUT_X_H_M)
    hxlo = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_OUT_X_L_M)
    hxtotal = ((hxhi << 8) | hxlo)
    return hxtotal


def magDatay():
    hyhi = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_OUT_Y_H_M)
    hylo = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_OUT_Y_L_M)
    hytotal = ((hyhi << 8) | hylo)
    return hytotal


def magDataz():
    hzhi = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_OUT_Z_H_M)
    hzlo = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_OUT_Z_L_M)
    hztotal = ((hzhi << 8) | hzlo)
    return hztotal


def magDataTotal():
    htotal = (((magDatax() ** 2) + (magDatay() ** 2) + (magDataz() ** 2)) ** 0.5)
    return htotal


def magDataTemp():
    thi = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_TEMP_OUT_H_M)
    tlo = bus.read_byte_data(LSM303_ADDRESS_MAG, LSM303_REGISTER_MAG_TEMP_OUT_L_M)
    ttotal = ((thi << 8) | tlo)
    return ttotal


WRITE_ACCEL(LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)  # initialise the Accelerometer
WRITE_ACCEL(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0x40)

WRITE_MAG(LSM303_REGISTER_MAG_MR_REG_M, 0x00)  # initialise the Magnetometer

while True:
    print("\n\n\n**********************************************************")
    print("LSM303DLHC Raw Data \n磁场 output: \nHx: ", magDatax())
    print("Hy: ", magDatay())
    x = magDatax()
    y = magDatay()
    print("Hz: ", magDataz())
    print("Htotal: ", magDataTotal(), "\n")
    print("\n加速度 output: \nGx: ", accelDatax())
    print("Gy: ", accelDatay())
    print("Gz: ", accelDataz())
    print("Gtotal: ", accelDataTotal(), "\n")
    print("Temp: ", magDataTemp())
    print("angle:",math.atan2(y,x) * (180/math.pi) +180)
    time.sleep(1)