import serial

def parse_nmea(sentence):
    data = sentence.split(',')
    sentence_type = data[0]
    if sentence_type == '$GPGGA':  # Example sentence type, adjust as needed
        try:
            latitude = float(data[2])
            longitude = float(data[4])
            lat_direction = data[3]
            lon_direction = data[5]
            # Convert latitude and longitude to decimal format
            lat_decimal = latitude // 100 + (latitude % 100) / 60
            lon_decimal = longitude // 100 + (longitude % 100) / 60
            if lat_direction == 'S':
                lat_decimal *= -1
            if lon_direction == 'W':
                lon_decimal *= -1
            print("Latitude:", lat_decimal)
            print("Longitude:", lon_decimal)
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
