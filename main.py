from pprint import pprint
import sys
from bbldecoder.reader import LogParser, LogReader, load_logs

def main():
    logs = load_logs(sys.argv[1])
    for log in logs:
        pprint(log.headers, indent=2, width=120, sort_dicts=False)
        pprint(log.fields, indent=2, width=120, sort_dicts=False)
        parser = LogParser(log)
        parser.load()
        # [print(frame) for frame in log.frames]

def main1():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <filename>")
        print("   Or: uv run main.py <filename>")
        return

    filename = sys.argv[1]
    reader = LogReader()
    reader.load(filename)

    for frame in reader.frames:
        print(f'{frame.type.value}: {frame.data}')
            
if __name__ == "__main__":
    main()
