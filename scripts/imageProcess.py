import subprocess
import datetime as dt
import os
import time
import threading
import parseGNSS
import concurrent.futures


class ImageProcessing:
    def __init__(self, callback, cancel_flag, offset_value, out_dir, ffmpeg_path, input_video):
        super().__init__()
        self.cancel_flag = cancel_flag
        self.offset_value = offset_value
        self.out_dir = out_dir
        self.ffmpeg_path = ffmpeg_path
        self.input_video = input_video
        self.callback = callback
        self.running = False
        self.max_processes = 4
        self.semaphore = threading.Semaphore(self.max_processes)

    def parse_images(self, only_first_image):
        self.only_first_image = only_first_image
        base_name_video = os.path.basename(self.input_video)
        self.running = True
        if self.only_first_image:
            ffmpeg_command = [
                self.ffmpeg_path + "/ffmpeg.exe",
                '-itsoffset', f'{self.offset_value}',
                '-i', f'{self.input_video}',
                '-vsync', '1',
                '-vf', "select='eq(n,0)'",
                '-r', '1',
                '-q:v', '1',
                f'{self.out_dir}/{base_name_video}_firstimage.png'
            ]

        else:
            ffmpeg_command = [
                self.ffmpeg_path + "/ffmpeg.exe",
                '-itsoffset', f'{self.offset_value}',
                '-i', f'{self.input_video}',
                '-vsync', '1',
                '-vf', "fps=1,select='not(mod(t,1))',setpts=N/FRAME_RATE/TB",
                '-r', '1',
                '-q:v', '1',
                f'{self.out_dir}/{base_name_video}_%05d.png'
            ]

        try:
            self.parse_process = subprocess.Popen(ffmpeg_command)
            while not self.cancel_flag.is_set() and self.parse_process.poll() is None:
                time.sleep(0.1)

                # If cancel_flag is set, terminate ffmpeg process
            print("endprocess")
            self.running = False
            if self.cancel_flag.is_set():
                self.parse_process.terminate()

                self.callback("Process canceled")
            else:
                self.callback("Process completed")

        except subprocess.CalledProcessError as e:
            self.callback(f"Process error {e}")

    def add_exif(self, roundedTime, GNSSvar, selected_gnss_file_path):
        print("exif")
        self.first_image_time = roundedTime
        self.GNSSvar = GNSSvar
        self.selected_gnss_file_path = selected_gnss_file_path

        print(self.first_image_time, self.GNSSvar)
        if GNSSvar:
            self.parse_GNSS()

        else:
            self.GNSS_corr = None

        new_photos = []
        while self.running:
            new_photos = self.check_for_new_photos(new_photos)
            self.add_exif_data_to_photos(new_photos)

    def check_for_new_photos(self, new_photos):

        for file_name in os.listdir(self.out_dir):
            if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
                file_path = os.path.join(self.out_dir, file_name)
                if file_path not in [item['file_path'] for item in new_photos]:
                    new_photos.append({'file_path': file_path, 'has_exif': False})
        print(new_photos)
        return new_photos

    def add_exif_data_to_photos(self, photos):
        while any(not photo['has_exif'] for photo in photos):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for photo in photos:
                    if not photo['has_exif']:
                        file_path = photo['file_path']
                        # Submitting the task to executor
                        future = executor.submit(self.accuracy_of_image, file_path)
                        futures.append((future, photo))
                # Waiting for all tasks to complete
                for future, photo in futures:
                    future.result()
                    photo['has_exif'] = True
            photos = self.check_for_new_photos(photos)

    def parse_GNSS(self):
        if self.selected_gnss_file_path.endswith(".gpx") and os.path.isfile(self.selected_gnss_file_path):
            self.GNSS_corr = parseGNSS.parse_GPX_gnss(self.selected_gnss_file_path)
        else:
            self.GNSS_corr = parseGNSS.parse_POS_gnss(self.selected_gnss_file_path)

    def accuracy_of_image(self, filepath):
        image_number = int(filepath.split('.png')[0].split('_')[-1])
        datetime_original = dt.datetime.strptime(self.first_image_time, "%Y-%m-%d %H:%M:%S") + dt.timedelta(
            seconds=(image_number - 1))

        if self.GNSS_corr is not None:
            datetime_condition = self.GNSS_corr["Time"] == datetime_original
            lat = ""
            lon = ""
            ele = ""
            rtk_std_lat = ""
            rtk_std_lon = ""
            rtk_std_hgt = ""

            if datetime_condition.any():
                index_of_row = datetime_condition.idxmax()
                row = self.GNSS_corr.loc[index_of_row]
                lat = row["Latitude"]
                lon = row["Longitude"]
                ele = row["Elevation"]
                qlt = row["Fix"]
                rtk_std_lat = row["Std lat"]
                rtk_std_lon = row["Std lon"]
                rtk_std_hgt = row["Std ele"]
                if None in (rtk_std_lat, rtk_std_lon, rtk_std_hgt) or "" in (rtk_std_lat, rtk_std_lon, rtk_std_hgt):
                    if qlt == "fix":
                        rtk_std_lat = 0.014
                        rtk_std_lon = 0.013
                        rtk_std_hgt = 0.028
                    elif qlt == "float":
                        rtk_std_lat = 1.4
                        rtk_std_lon = 1.3
                        rtk_std_hgt = 2.8
                    else:
                        rtk_std_lat = 10
                        rtk_std_lon = 10
                        rtk_std_hgt = 10
            else:
                i = 0
                time_up = None
                i_up = 0
                time_down = None
                i_down = 0

                while i < 20:

                    if time_up is None:
                        search_time_up = datetime_original + dt.timedelta(seconds=i)
                        datetime_condition_up = self.GNSS_corr["Time"] == search_time_up
                        if datetime_condition_up.any():
                            index_of_row_up = datetime_condition_up.idxmax()
                            time_up = self.GNSS_corr.loc[index_of_row_up]
                            i_up = i

                    if time_down is None:
                        search_time_down = datetime_original - dt.timedelta(seconds=i)
                        datetime_condition_down = self.GNSS_corr["Time"] == search_time_down
                        if datetime_condition_down.any():
                            index_of_row_down = datetime_condition_down.idxmax()
                            time_down = self.GNSS_corr.loc[index_of_row_down]
                            i_down = i

                    if time_down is not None and time_up is not None:
                        break
                    i += 1

                if time_up is not None and time_down is not None:
                    lat = (float(time_up["Latitude"]) * i_up + float(time_down["Latitude"]) * i_down) / (i_up + i_down)
                    lon = (float(time_up["Longitude"]) * i_up + float(time_down["Longitude"]) * i_down) / (
                            i_up + i_down)
                    ele = (float(time_up["Elevation"]) * i_up + float(time_down["Elevation"]) * i_down) / (
                            i_up + i_down)
                    rtk_std_lat = rtk_std_lon = rtk_std_hgt = 5
                elif time_up is not None:
                    lat = time_up["Latitude"]
                    lon = time_up["Longitude"]
                    ele = time_up["Elevation"]
                    rtk_std_lat = rtk_std_lon = rtk_std_hgt = 10
                elif time_down is not None:
                    lat = time_down["Latitude"]
                    lon = time_down["Longitude"]
                    ele = time_down["Elevation"]
                    rtk_std_lat = rtk_std_lon = rtk_std_hgt = 10

            if lat != "" or lon != "" or ele != "":


                addDateAndPositionToImage(filepath, datetime_original, lat, lon, ele, rtk_std_lat,
                                          rtk_std_lon, rtk_std_hgt)
            else:
                addDateToImage(filepath, datetime_original)

        else:
            addDateToImage(filepath, datetime_original)


def addDateToImage(image_path, datetime_original):
    try:
        datetime = str(datetime_original)
        # Use ExifTool to add or update DateTimeOriginal metadata
        subprocess.run(['exiftool', "-overwrite_original", '-DateTimeOriginal=' + datetime, image_path], check=True)
        print(f"Added DateTimeOriginal metadata to {image_path} {datetime}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding metadata to {image_path}: {e}")


def addDateAndPositionToImage(image_path, datetime_original, lat, lon, ele, rtk_std_lat, rtk_std_lon, rtk_std_hgt):
    try:
        # Convert datetime to string
        datetime = str(datetime_original)

        # Use ExifTool to add or update metadata
        exiftool_cmd = ["exiftool",
                        "-overwrite_original",
                        "-DateTimeOriginal=" + datetime,
                        "-XMP:GPSLatitude=" + str(lat),
                        "-XMP:GPSLongitude=" + str(lon),
                        "-XMP:GPSAltitude=" + str(ele),
                        "-XMP:RtkStdLat=" + str(rtk_std_lat),
                        "-XMP:RtkStdLon=" + str(rtk_std_lon),
                        "-XMP:RtkStdHgt=" + str(rtk_std_hgt),
                        image_path]

        subprocess.run(exiftool_cmd, check=True)
        print(f"Added metadata to {image_path} {datetime} {lat} {lon} {ele} {rtk_std_lat} {rtk_std_lon} {rtk_std_hgt}")

    except subprocess.CalledProcessError as e:
        print(f"Error adding metadata to {image_path}: {e}")
