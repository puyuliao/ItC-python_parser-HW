import argparse
from datetime import datetime


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--start-date',required=True, help='Crawl Start Date')
	parser.add_argument('--end-date',required=False, help='Crawl End Date')
	args = parser.parse_args()
	args.start_date = datetime.strptime(args.start_date,'%Y-%m-%d')
	args.end_date = datetime.strptime(args.end_date,'%Y-%m-%d')
	return args
