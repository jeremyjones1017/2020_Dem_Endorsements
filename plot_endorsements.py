import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import os

def main():
	#Download the data
	url = "https://projects.fivethirtyeight.com/endorsements-2020-data/endorsements-2020.csv"
	filename = 'endorsements-2020.csv'
	
	today = datetime.datetime.today()
	statbuf = os.stat(filename)
	edit_time = datetime.datetime.fromtimestamp(statbuf.st_mtime)
	days_since_edit = (today-edit_time).days
	if days_since_edit > 0:
		download_data(filename,url)
	else:
		print('File last downloaded within 24 hours')
	
	
	endorse_df = pd.read_csv(filename)
	#print(endorse_df.columns)
	endorse_df = endorse_df[pd.isna(endorse_df.date) == False]
	#print(endorse_df[['date','endorsee','points']])
	dates = list(endorse_df.date)
	datetimes = []
	for date in dates:
		datetimes.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
	endorse_df['datetimes'] = datetimes
	endorsees = list(endorse_df.endorsee)
	points = list(endorse_df.points)
	
	cands = dict()
	
	start_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
	days_ago = (today - start_date).days
	
	recent_endorsements = endorse_df[endorse_df.datetimes > (today - datetime.timedelta(days = 7))]
	print(recent_endorsements[['date','endorsee','position','city','state','endorser','points']])
	
	int_days = list(range(days_ago))
	all_days = []
	for i in int_days:
		all_days.append(start_date + datetime.timedelta(days = i))
	
	for i,str_date in enumerate(dates):
		date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
		days_after_start = (date - start_date).days
		if endorsees[i] not in cands:
			cands[endorsees[i]] = np.zeros(days_ago)
		to_add = np.zeros(days_ago)
		for j,test_date in enumerate(all_days):
			if test_date >= date:
				to_add[j] += points[i]
		cands[endorsees[i]] += to_add
	
	the_cands = []
	current_points = []
	
	for cand in cands:
		the_cands.append(cand)
		current_points.append(cands[cand][-1])
	
	max_points = max(current_points)
	
	zipped = zip(current_points, the_cands)
	zipped = sorted(zipped, reverse = True)
		
	debate_1 = datetime.datetime.strptime('2019-06-26', '%Y-%m-%d')
	debate_2 = datetime.datetime.strptime('2019-06-27', '%Y-%m-%d')
	
	plt.plot([debate_1,debate_1],[-2,max_points+2],'k-')
	plt.plot([debate_2,debate_2],[-2,max_points+2],'k-')
	
	for i in zipped:
		cand = i[1]
		plt.plot(all_days,cands[cand],label = cand)
	
	plt.xlim(datetime.datetime.strptime('2018-12-01', '%Y-%m-%d'),today)
	plt.ylim(-1,max_points+1)
	plt.xlabel('Date')
	plt.ylabel('Endorsement Points')
	plt.legend()
	plt.show()
	
	state_codes = ['AL','AK','AZ','AR','CA','CO','CT','DC','DE','FL',
					'GA','HI','ID','IL','IN','IA','KS','KY','LA','ME',
					'MD','MA','MI','MN','MS','MO','MT','NE','NV','NH',
					'NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI',
					'SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
					
	print(state_codes)

def download_data(filename,url):
	print('Downloading up to date endorsement data')
	curl_command = 'curl -o {} {}'.format(filename,url)
	print(curl_command)
	os.system(curl_command)


if __name__ == '__main__':
	main()
