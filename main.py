import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import WEEKLY,MONTHLY, DateFormatter, rrulewrapper, RRuleLocator 
import numpy as np
import csv
from matplotlib.patches import Rectangle



class Gantt:

	def __init__(self,filename_str):

		self.x_dates = [
				'2021-01-01',
				'2021-07-01',
				'2022-01-01',
				'2022-07-01',
				'2023-01-01',
				'2023-07-01',
				'2024-01-01',
				'2024-07-01'
			]

		self.colors = ['#0074D9','#FF4136','#85144b','#111111','#3D9970','#FFDC00']
		self.y_labels = self.read_data_column(filename_str,'task')
		self.x_labels = [self.create_date(date) for date in self.x_dates ]
		self.start_date_list = self.read_data_column(filename_str,'start_date')
		self.end_date_list = self.read_data_column(filename_str,'end_date')
		self.WP_list = self.read_data_column(filename_str,'wp')
		self.task_timespan_list = [self.start_date_list] + [self.end_date_list]


	def read_data_column(self,file_name,column_name_str):
		return_list = []
		with open(file_name, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				return_list.append(row[column_name_str])
		return return_list

	def create_date(self,datetxt):
	    """Creates the date"""
	    year,month,day=datetxt.split('-')
	    date = dt.datetime(int(year), int(month), int(day))
	    mdate = matplotlib.dates.date2num(date) 
	    return mdate

    # I am the one who plots!
	def plotter(self):
		ilen=len(self.y_labels)
		pos = np.arange(0.5,ilen*0.5+0.5,0.5)
		task_dates = {}
		wp_colors = {}
		wp = list(dict.fromkeys(self.WP_list))
		wp.reverse()

		temp_wp = wp
		for i,temp_wp in enumerate(temp_wp):
			wp_colors[temp_wp] = self.colors[i]


		for i,task in enumerate(self.y_labels):
			task_dates[task] = [
				self.create_date(self.task_timespan_list[0][i]),
				self.create_date(self.task_timespan_list[1][i])
			]

		fig = plt.figure(figsize=(12,7))
		ax = fig.add_subplot(111)
		for i in range(len(self.y_labels)):
			start_date,end_date = task_dates[self.y_labels[i]]
			ax.barh(
				(i*0.5)+0.5,
				end_date - start_date,
				left=start_date,
				height=0.4,
				align='center',
				edgecolor='lightgreen',
				color= wp_colors[self.WP_list[i]],
				alpha = 0.8
	        )

		rule = rrulewrapper(WEEKLY, interval=1)
		loc = RRuleLocator(rule)
		formatter = DateFormatter("%d-%b '%y")
		lcsy, labelsy = plt.yticks(pos,self.y_labels)
		font = font_manager.FontProperties(size='small')
		p = []
		for i in range(len(self.colors)):
			p.append(Rectangle((0, 0), 1, 1, fc=self.colors[i]))

		ax.set_ylim(ymin = -0.1, ymax = ilen*0.5+0.5)
		ax.grid(color = 'g', linestyle = ':')
		ax.xaxis_date()
		ax.xaxis.set_major_locator(loc)
		ax.xaxis.set_major_formatter(formatter)
		ax.invert_yaxis()
		ax.legend(p, wp,loc=1,prop=font) 

		plt.setp(labelsy, fontsize = 10)
		plt.xticks(self.x_labels)
		plt.savefig('gantt.svg')
		plt.show()

g = Gantt('./data.csv')

g.plotter()
