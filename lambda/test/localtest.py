import sys
sys.path.append("..")

from pathlib import Path
from json import loads
from src.lambda_function import fetch_schedule, extract_schedule, to_text

#sd = loads(Path("station.json").read_text())
#sh = extract_schedule(sd)
#print(to_text(sh))

print(fetch_schedule("stop__9649375"))
