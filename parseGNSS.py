import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt
def parse_GPX_gnss(path):
    tree = ET.parse(path)
    root = tree.getroot()
    wpt_elements = root.findall('.//{http://www.topografix.com/GPX/1/1}wpt')

    lat_list = []
    lon_list = []
    ele_list = []
    time_list = []
    fix_list = []
    rtk_std_lat_list = []
    rtk_std_lon_list = []
    rtk_std_hgt_list = []
    for wpt_element in wpt_elements:

        lat = wpt_element.attrib['lat']
        lon = wpt_element.attrib['lon']
        ele_element = wpt_element.find('{http://www.topografix.com/GPX/1/1}ele')
        ele = ele_element.text if ele_element is not None else None
        time_element = wpt_element.find('{http://www.topografix.com/GPX/1/1}time')
        time = time_element.text if time_element is not None else None
        fix_element = wpt_element.find('{http://www.topografix.com/GPX/1/1}fix')
        fix = fix_element.text if fix_element is not None else None
        rtk_std_lat = None
        rtk_std_lon = None
        rtk_std_hgt = None
        if time is None:
            break
        else:
            lat_list.append(lat)
            lon_list.append(lon)
            ele_list.append(ele)
            fix_list.append(fix)
            time_list.append(dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ"))
            rtk_std_lat_list.append(rtk_std_lat)
            rtk_std_lon_list.append(rtk_std_lon)
            rtk_std_hgt_list.append(rtk_std_hgt)

    df = pd.DataFrame({
        'Time': time_list,
        'Latitude': lat_list,
        'Longitude': lon_list,
        'Elevation': ele_list,
        'Fix': fix_list,
        "Std lat": rtk_std_lat_list,
        "Std lon": rtk_std_lon_list,
        "Std ele": rtk_std_hgt_list,
    })
    return df


def parse_POS_gnss(path, filename):
    print("pos")