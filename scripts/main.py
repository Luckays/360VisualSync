import input
import datetime as dt
import parseGNSS
import imageProcess as iP


if __name__ == '__main__':

    # input parameters
    req = input.Requirements(input.parser)
    # first time and offset
    time_str = (req.time +dt.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")

    offset_time = (1000000 - req.time.microsecond) / 1000000

    iP.parseImages(offset_time, req.out, req.FF, req.path +"/"+req.mp4+"mp4")
    if req.gnss is not None:
        GNSS_corr = parseGNSS.parse_GPX_gnss(req.path, req.gnss + ".gpx")
    else:
        GNSS_corr = None

    iP.dataForImages(time_str, req.path, GNSS_corr, req.mp4)


