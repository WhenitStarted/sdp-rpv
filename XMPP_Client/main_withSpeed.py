from time import sleep
import xmpp
import math
import serial

# XMPP client credentials, user receiver address, and message
username = 'client2'
passwd = '12345'
to = 'admin@localhost'

disableXMPP = False  # Set to True if XMPP sending is disabled
msg = "Latitude: {}, Longitude: {}, Speed: {:.2f} km/hr"  # Message template for latitude, longitude, and speed

# XMPP INITIALIZATION
if not disableXMPP:
    client = xmpp.Client('localhost')
    client.connect(server=('192.168.0.68', 5222))  # connect to ejabberd server using VPN IP
    client.auth(username, passwd)
    client.sendInitPresence()


def send_xmpp_message(lat, lon, speed):
    if not disableXMPP:
        message = xmpp.Message(to, msg.format(lat, lon, speed))
        message.setAttr('type', 'chat')
        client.send(message)


def knots_to_kmh(speed_knots):
    # 1 knot is approximately equal to 1.852 kilometers per hour
    return speed_knots * 1.852


def parse_nmea(sentence):
    data = sentence.split(',')
    sentence_type = data[0]
    if sentence_type == '$GPGGA':  # Example sentence type, adjust as needed
        try:
            latitude = float(data[2])
            longitude = float(data[4])
            lat_direction = data[3]
            lon_direction = data[5]
            speed_knots = float(data[7])  # Speed in knots
            speed_kmh = knots_to_kmh(speed_knots)
            # Convert latitude and longitude to decimal format
            lat_decimal = latitude // 100 + (latitude % 100) / 60
            lon_decimal = longitude // 100 + (longitude % 100) / 60
            if lat_direction == 'S':
                lat_decimal *= -1
            if lon_direction == 'W':
                lon_decimal *= -1
            print("Latitude:", lat_decimal)
            print("Longitude:", lon_decimal)
            print("Speed (km/hr):", speed_kmh)
            send_xmpp_message(lat_decimal, lon_decimal, speed_kmh)  # Send XMPP message with lat, lon, and speed
        except (IndexError, ValueError):
            print("Invalid GPS data")
    # Add other sentence types and their parsing logic as needed


def main():
    serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
    baud_rate = 115200  # Adjust this to match your baud rate

    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            while True:
                try:
                    sentence = ser.readline().decode('utf-8').strip()
                    if sentence.startswith('$'):  # Check if it's an NMEA sentence
                        parse_nmea(sentence)
                except UnicodeDecodeError:
                    # Print raw bytes if decoding fails
                    print("Received data (raw):", ser.readline())
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except serial.SerialException as e:
        print("Serial port error:", e)


if __name__ == "__main__":
    main()
