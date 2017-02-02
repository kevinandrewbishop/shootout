from ast import literal_eval
import pandas as pd
logfile = 'log1'

def parse(filename):

	with open(logfile) as f:
		lines = f.readlines()
	
	lines = [l.strip() for l in lines]
	
	cols = ['health_diff', 'los_bonus', 'dist_div', 'health_diff_aggress']
	cols = cols + [c + '_' for c in cols]
	cols.append('iteration')
	cols += ['p1_x', 'p1_y', 'p2_x', 'p2_y', 'p1_health', 'p2_health', 'outcome']
	cols.append('round')
	output = {c: [] for c in cols}
	row = 0
	for l in lines:
		if row == 0:
			iter = l.split(' ')[1]
			output['iteration'].append(iter)
		elif row in (1, 2):
			params = literal_eval(l)
			suffix = ''
			if row == 2:
				suffix = '_'
			for key in params:
				output[key+suffix].append(params[key])
		elif row == 3:
			params = literal_eval(l)
			for key in params:
				output[key].append(params[key])
		elif row == 4:
			output['round'].append(l)
		row += 1
		if row == 5:
			row = 0
	return pd.DataFrame(output)[cols]


