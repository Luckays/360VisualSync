
import login as log

if __name__ == '__main__':
    login_window = log.LoginWindow()

    # # input parameters
    # req = input.Requirements(input.parser)
    # # first time and offset
    # time_str = (req.time +dt.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    # offset_time = (1000000 - req.time.microsecond) / 1000000
    #
    # iP.parseImages(offset_time, req.path, req.FF, req.mp4)
    # if req.gnss is not None:
    #     GNSS_corr = gpx.parse_GPX_gnss(req.path, req.gnss + ".gpx")
    # else:
    #     GNSS_corr = None
    #
    # iP.dataForImages(time_str, req.path, GNSS_corr, req.mp4)


