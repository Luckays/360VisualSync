import argparse
import datetime
import os

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Please use YYYY-MM-DD HH:MM:SS.sss")

class Requirements:
    def __init__(self, parser):
        self.args = parser.parse_args()
        self.path = self.args.path
        self.mp4 = self.args.mp4
        self.gnss = self.args.gnss
        self.FF = self.args.FF
        self.out = self.args.out
        if not self.FF:
            project_path = os.path.dirname(os.path.abspath(__file__))
            self.FF = project_path
        self.time = self.args.time if self.args.time else datetime.datetime.now()

parser = argparse.ArgumentParser(description="360VizualSync")
parser.add_argument("--path", type=str, required=True, help="Path to project")
parser.add_argument('--mp4', type=str, help='MP4')
parser.add_argument('--gnss', type=str, help='GPX')
parser.add_argument('--FF', type=str, help='path to FF')
parser.add_argument("--out", type=str, required=True, help="Project output")
parser.add_argument("--time", type=parse_date, default=None, help="Input date in the format YYYY-MM-DD HH:MM:SS.sss")
req = Requirements(parser)