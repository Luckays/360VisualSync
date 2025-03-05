import re
from datetime import datetime

def parse_nmea_gga(gga_message, zda_message):
    gga_parts = gga_message.split(',')
    zda_parts = zda_message.split(',')

    if len(gga_parts) < 15 or len(zda_parts) < 5:  # Check if the messages have enough elements
        print("Unexpected NMEA message format:", gga_message, zda_message)
        return None, None, None, None, None

    try:
        lat_deg = int(gga_parts[2][:2])
        lat_min = float(gga_parts[2][2:])
        lat = lat_deg + lat_min / 60.0 if gga_parts[3] == 'N' else -(lat_deg + lat_min / 60.0)

        lon_deg = int(gga_parts[4][:3])
        lon_min = float(gga_parts[4][3:])
        lon = lon_deg + lon_min / 60.0 if gga_parts[5] == 'E' else -(lon_deg + lon_min / 60.0)

        ele = float(gga_parts[9])+float(gga_parts[11])

        time_str = gga_parts[1]
        print(time_str)
        day = int(zda_parts[2])
        month = int(zda_parts[3])
        year = int(zda_parts[4])
        zda_time = datetime.strptime(f"{year}-{month:02d}-{day:02d} {time_str}", "%Y-%m-%d %H%M%S.%f").strftime(
            "%Y-%m-%dT%H:%M:%S.00Z")
        print(zda_time)
        print(lat, lat_deg, lat_min)

        fix_indicator = int(gga_parts[6])
        if fix_indicator == 4:  # RTK Fixed, xFill
            fix = "fix"
        elif fix_indicator == 5:  # RTK Float, OmniSTAR XP/HP, Location RTK, RTX
            fix = "float"
        else:
            fix = "Unknown"

        return lat, lon, ele, zda_time, fix

    except Exception as e:
        print("Error parsing NMEA messages:", e)
        return None, None, None, None, None
def create_gpx(wpt_list):
    gpx = '<?xml version="1.0" encoding="UTF-8"?>\n'
    gpx += '<gpx version="1.1" creator="RTKLIB 2.4.3" xmlns="http://www.topografix.com/GPX/1/1">\n'
    for wpt in wpt_list:
        gpx += '<wpt lat="{}" lon="{}">\n'.format(wpt[0], wpt[1])
        gpx += ' <ele>{}</ele>\n'.format(wpt[2])
        gpx += ' <time>{}</time>\n'.format(wpt[3])
        gpx += ' <fix>{}</fix>\n'.format(wpt[4])
        gpx += '</wpt>\n'
    gpx += '</gpx>'
    return gpx

def main():
    # Read NMEA messages from a file
    with open("D:/CVUT/PhD/insta360kampus/240514_092800_14.ubx", "r", encoding="latin-1") as file:
        nmea_data = ""
        binary_data = []
        for line in file:
            if line.startswith('$'):
                nmea_data += line
            else:
                binary_data.append(line)

    # Find all GGA and ZDA messages
    gga_messages = re.findall(r'\$GNGGA[^$]*\r?\n', nmea_data)
    zda_messages = re.findall(r'\$GNZDA[^$]*\r?\n', nmea_data)

    # Parse GGA and ZDA messages and create GPX waypoints
    gpx_waypoints = []
    for gga_message, zda_message in zip(gga_messages, zda_messages):
        lat, lon, ele, time, fix = parse_nmea_gga(gga_message, zda_message)
        gpx_waypoints.append((lat, lon, ele, time, fix))

    # Create GPX file
    gpx_content = create_gpx(gpx_waypoints)
    with open("D:/CVUT/PhD/insta360kampus/output.gpx", "w", encoding="utf-8") as file:
        file.write(gpx_content)

        # Reopen the file in write mode to remove NMEA messages
    with open("D:/CVUT/PhD/insta360kampus/output_bin.ubx", "w", encoding="latin-1") as file:
        for line in binary_data:
            file.write(line)
if __name__ == "__main__":
    main()
