import sys
from client import *

from utils.json_reader import *

def main(argv):
	jsonLoader = JsonReader()

	client = HomestuckUpdater()

	client.run(jsonLoader.getServerKey())
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
