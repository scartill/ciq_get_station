import sys
sys.path.append("..")

from pathlib import Path
from json import loads
from argparse import ArgumentParser
from src.lambda_function import fetch_schedule, extract_schedule, to_text

parser = ArgumentParser()
parser.add_argument('--online', action='store_true')
parser.add_argument('--file', action='store_true')
args = parser.parse_args()

if args.file:
    sd = loads(Path("station.json").read_text(encoding='utf-8'))
    sh = extract_schedule(sd)
    print(to_text(sh))

if args.online:
    print(fetch_schedule("stop__9649375"))

from src.lambda_function import calc_eta
