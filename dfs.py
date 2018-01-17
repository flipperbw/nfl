import requests
import pandas
from bs4 import BeautifulSoup
import pulp

site_settings = {
	"draft-street": {
		"caps": [100000],
		"roster": {
			"qb": 2,
			"rb": 2,
			"wr": 2,
			"te": 1,
			"flex": 2,
			"dst": 1,
			"k": 0
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.04,
			"pass_ints": -1,
			"bonus_300": 0,
			
			"td": 6,
			"yd": 0.1,
			"rec": 0.5,
			"bonus_100": 0,
			
			"fumbles": -1,
			
			"dp": 12,
			"dpa": -0.5,
			"dint": 1,
			"fr": 1,
			"sack": 0.5,
			"sfty": 2,
			
			"xpt": 0,
			"fg": 0

		}
	},

	"draftkings": {
		"caps": [50000],
		"roster": {
			"qb": 1,
			"rb": 2,
			"wr": 2,
			"te": 1,
			"flex": 1,
			"dst": 1,
			"k": 1
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.04,
			"pass_ints": -1,
			"bonus_300": 3,
			
			"td": 6,
			"yd": 0.1,
			"rec": 1,
			"bonus_100": 3,
			
			"fumbles": -1,
			
			"dp": 10,
			"dpa": -0.5,
			"dint": 2,
			"fr": 2,
			"sack": 1,
			"sfty": 2,
			
			"xpt": 1,
			"fg": 3
		}
	},

	"fanthrowdown": {
		"caps": [100000], #maybe others, none listed
		"roster": {
			"qb": 1,
			"rb": 2,
			"wr": 3,
			"te": 1,
			"flex": 1,
			"dst": 1,
			"k": 1
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.04,
			"pass_ints": -1,
			"bonus_300": 0,
			
			"td": 6,
			"yd": 0.1,
			"rec": 0.5,
			"bonus_100": 0,
			
			"fumbles": -2,
			
			"dp": 10,
			"dpa": -0.5,
			"dint": 2,
			"fr": 2,
			"sack": 1,
			"sfty": 2,
			
			"xpt": 1,
			"fg": 3
		}
	},

	"fantasyaces": {
		"caps": [50000,55000], #unclear which. also salarypro, not sure what that is
		"roster": {
			"qb": 2,
			"rb": 2,
			"wr": 2,
			"te": 1,
			"flex": 2,
			"dst": 1,
			"k": 1
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.05,
			"pass_ints": -2,
			"bonus_300": 0,
			
			"td": 6,
			"yd": 0.1,
			"rec": 0.5,
			"bonus_100": 0,
			
			"fumbles": -2,
			
			"dp": 10,
			"dpa": -0.5,
			"dint": 2,
			"fr": 2,
			"sack": 1,
			"sfty": 2,
			
			"xpt": 1,
			"fg": 3
		}
	},

	"starstreet": {
		"caps": [100000],
		"roster": {
			"qb": 2,
			"rb": 2,
			"wr": 2,
			"te": 1,
			"flex": 2,
			"dst": 0,
			"k": 0
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.04,
			"pass_ints": -2,
			"bonus_300": 0,
			
			"td": 6,
			"yd": 0.1,
			"rec": 1,
			"bonus_100": 0,
			
			"fumbles": -2,
			
			"dp": 0,
			"dpa": 0,
			"dint": 0,
			"fr": 0,
			"sack": 0,
			"sfty": 0,
			
			"xpt": 0,
			"fg": 0
		}
	},

	"fantasy-feud": {
		"caps": [1000000],
		"roster": {
			"qb": 2,
			"rb": 2,
			"wr": 2,
			"te": 1,
			"flex": 1,
			"dst": 1,
			"k": 0
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.04,
			"pass_ints": -2,
			"bonus_300": 0,
			
			"td": 6,
			"yd": 0.1,
			"rec": 0.5,
			"bonus_100": 0,
			
			"fumbles": -2,
			
			"dp": 10,
			"dpa": -0.5,
			"dint": 2,
			"fr": 2,
			"sack": 1,
			"sfty": 2,
			
			"xpt": 0,
			"fg": 0
		}
	},

	"fan-duel": {
		"caps": [55000,60000,65000],
		"roster": {
			"qb": 1,
			"rb": 2,
			"wr": 3,
			"te": 1,
			"flex": 0,
			"dst": 1,
			"k": 1
		},
		
		"scoring": {
			"pass_tds": 4,
			"pass_yds": 0.04,
			"pass_ints": -1,
			"bonus_300": 0,
			
			"td": 6,
			"yd": 0.1,
			"rec": 0.5,
			"bonus_100": 0,
			
			"fumbles": -2,
			
			"dp": 10,
			"dpa": -0.5,
			"dint": 2,
			"fr": 2,
			"sack": 1,
			"sfty": 2,
			
			"xpt": 1,
			"fg": 3
		}
	}
}

#- Get projected stats
dataframes = {}
positions = ('qb','rb','wr','te','dst','k')
for p in positions:
	#max-yes=true&min-yes=true, use stddev
	ts = requests.get('http://www.fantasypros.com/nfl/projections/%s.php?export=xls' % p).text
	ts_split = [i.strip().split('\t') for i in ts.strip().split('\n')[4:]]
	
	headers = [r.strip() for r in ts_split[0]]
	data = ts_split[1:]

	#- Name mismatch fixes
	for d in data:
		if p == 'dst' and ' ' in d[0]:
			data.append([d[0].split()[-1]] + d[1:])
			if d[0] == 'St. Louis Rams':
				data.append(['St Louis Rams'] + d[1:])
		elif d[0] == 'Ty Hilton':
			data.append(['T.Y. Hilton'] + d[1:])
			data.append(['TY Hilton'] + d[1:])
		elif d[0] == 'Christopher Ivory':
			data.append(['Chris Ivory'] + d[1:])
		elif d[0] == 'Robert Housler':
			data.append(['Rob Housler'] + d[1:])
		elif d[0] == 'Josh Morgan':
			data.append(['Joshua Morgan'] + d[1:])
		elif d[0] == 'Ted Ginn Jr.':
			data.append(['Ted Ginn'] + d[1:])
		elif d[0] == 'C.J. Spiller':
			data.append(['CJ Spiller'] + d[1:])
		elif d[0] == 'Le\'Veon Bell':
			data.append(['LeVeon Bell'] + d[1:])
		elif d[0] == 'A.J. Green':
			data.append(['AJ Green'] + d[1:])
		elif d[0] == 'A.J. Jenkins':
			data.append(['AJ Jenkins'] + d[1:])
		elif d[0] == 'Tim Wright':
			data.append(['Timothy Wright'] + d[1:])
		
	df = pandas.DataFrame(data, columns=headers)
	#remove all zero entries
	
	dataframes[p] = df

def get_pandas_value(metric):
	try:
		met_val = pd[metric].values[0]
	except KeyError:
		met_val = 0
	return float(met_val)

#- Calculate projected points for each site
for k in site_settings.keys():
	player_data = {}
	site = site_settings[k]
	roster = site['roster']
	caps = site['caps']
	scoring = site['scoring']
	
	print '====================>  Optimizing site: ', k, ' <===================='

	dfs = requests.get('http://dfsedge.com/tools/?site=%s' % k).text
	soup = BeautifulSoup(dfs)

	dfs_table = soup.find(id='ALLTab').table.tbody.find_all('tr')

	for player in dfs_table:
		tds = player.find_all('td')
		
		name = tds[1].string.strip()
		pos = tds[2].string.lower()
		sal = int(tds[3].string.strip().replace('$','').replace(',',''))
		"""[
		team = tds[4].span.string
		where = tds[5].span.string
		if where == '@ ':
			where = 'away'
		elif where == 'vs. ':
			where = 'home'
		else:
			where = 'n/a (%s)' % where
		opp_team = tds[6].span.string
		weather = tds[7]
		temp = weather.span.text.split(u"°")[0]
		cond = weather.img.get('src').split("/")[-1].split(".")[0]
		pts = tds[8].string
		ppp = tds[9].string.replace('$','')
		
		print name, pos, sal, team, where, opp_team, temp, cond, pts, ppp
		"""
		
		# use st dev to randomize points, loop a few times
		pd = dataframes[pos].get(dataframes[pos]["Player Name"] == '%s' % name)
		if not pd:
			print 'Could not match name for dfsedge/fantasypros: %s' % name
		else:
			payd = get_pandas_value("pass_yds") * scoring['pass_yds']
			patd = get_pandas_value("pass_tds") * scoring['pass_tds']
			paint = get_pandas_value("pass_ints") * scoring['pass_ints']
			pabonus = (payd > 300) * scoring['bonus_300']
			
			td = (get_pandas_value("rec_tds") + get_pandas_value("rush_tds") + get_pandas_value("def_td")) * scoring['td']
			yd = (get_pandas_value("rec_yds") + get_pandas_value("rush_yds")) * scoring['yd']
			rec = get_pandas_value("rec_att") * scoring['rec']
			bonus = (yd > 100) * scoring['bonus_100']
			
			fumble = get_pandas_value("fumbles") * scoring['fumbles']
			
			ddp = (pos == 'dst') * scoring['dp']
			dpa = get_pandas_value("def_pa") * scoring['dpa']
			dint = get_pandas_value("def_int") * scoring['dint']
			fr = get_pandas_value("def_fr") * scoring['fr']
			sack = get_pandas_value("def_sack") * scoring['sack']
			sfty = get_pandas_value("def_safety") * scoring['sfty']
			
			xpt = get_pandas_value("xpt") * scoring['xpt']
			fg = get_pandas_value("fg") * scoring['fg']
			
			#- Now calculate the sum of points
			points = payd + patd + paint + pabonus + td + yd + rec + bonus + fumble + ddp + dpa + dint + fr + sack + sfty + xpt + fg
			
			#- Perhaps use stdev here to adjust the points total
			player_data[name] = (pos, sal, points)
	
	player_names = {"qb":[], "rb":[], "wr": [], "te": [], "dst":[], "k":[]}
	for pl in player_data.keys():
		player_names[player_data[pl][0]].append(pl)
		
	qb_names = player_names['qb']
	rb_names = player_names['rb']
	wr_names = player_names['wr']
	te_names = player_names['te']
	flex_names = rb_names + wr_names + te_names
	dst_names = player_names['dst']
	k_names = player_names['k']
	all_names = qb_names + rb_names + wr_names + te_names + dst_names + k_names

	for cap in caps:
		prob = pulp.LpProblem("%s Optimization" % k, pulp.LpMaximize)
		
		#- Set the variables (boolean player names)
		player_vars = pulp.LpVariable.dicts("Players", all_names, cat="Binary")
		#a = LpVariable('a',0,1,LpInteger)
		
		#- Set the objective (maximize points)
		prob += pulp.lpSum([player_data[i][2] * player_vars[i] for i in all_names]), "Total Points"
		#prob += 23.5*a + 19.3*b + 16.7*c + 14.8*d + 7.1*e + 13*f + 4*g + 17.4*h + 8.2*i + 7.1*j + 3.2*k, 'points'
		
		#- Set the contraints (budget and then roster)
		prob += pulp.lpSum([player_data[i][1] * player_vars[i] for i in all_names]) <= cap, "Total Cost"
		# prob += 15.7*a + 14*b + 13.7*c + 13*d + 6.7*e + 11.2*f + 4*g + 13.7*h + 8.2*i + 14.1*j + 4.1*k <= 100, 'cost'
		
		# prob += a + b == 1, 'qbs'
		prob += pulp.lpSum([player_vars[i] for i in qb_names]) == roster['qb'], "Total QBs"
		prob += pulp.lpSum([player_vars[i] for i in rb_names]) >= roster['rb'], "Total RBs"
		prob += pulp.lpSum([player_vars[i] for i in wr_names]) >= roster['wr'], "Total WRs"
		prob += pulp.lpSum([player_vars[i] for i in te_names]) >= roster['te'], "Total TEs"
		prob += pulp.lpSum([player_vars[i] for i in flex_names]) == roster['rb'] + roster['wr'] + roster['te'] + roster['flex'], "Total Flexs"
		prob += pulp.lpSum([player_vars[i] for i in dst_names]) == roster['dst'], "Total DSTs"
		prob += pulp.lpSum([player_vars[i] for i in k_names]) == roster['k'], "Total Ks"

		#- Solve
		prob.writeLP("%s.lp" % k)
		prob.solve()
		
		if pulp.LpStatus[prob.status] != 'Optimal':
			print 'Status not optimal -> %s' % pulp.LpStatus[prob.status]
		else:
			new_player_vars = {}
			for on,nn in player_vars.iteritems():
				new_player_vars[nn.name] = on
			
			solution = {"qb": [], "rb": [], "wr": [], "te": [], "flex": [], "dst": [], "k": []}
			total_salary = 0
			rb_count = wr_count = te_count = 0
			for v in prob.variables():
				if v.varValue == 1:
					old_name = new_player_vars[v.name]
					
					if player_data[old_name][0] == 'rb':
						if rb_count < roster['rb']:
							solution[player_data[old_name][0]].append((old_name, player_data[old_name][1], player_data[old_name][2]))
							rb_count += 1
						else:
							solution["flex"].append((old_name, player_data[old_name][1], player_data[old_name][2]))
					elif player_data[old_name][0] == 'wr':
						if wr_count < roster['wr']:
							solution[player_data[old_name][0]].append((old_name, player_data[old_name][1], player_data[old_name][2]))
							wr_count += 1
						else:
							solution["flex"].append((old_name, player_data[old_name][1], player_data[old_name][2]))
					elif player_data[old_name][0] == 'te':
						if te_count < roster['te']:
							solution[player_data[old_name][0]].append((old_name, player_data[old_name][1], player_data[old_name][2]))
							te_count += 1
						else:
							solution["flex"].append((old_name, player_data[old_name][1], player_data[old_name][2]))
					else:
						solution[player_data[old_name][0]].append((old_name, player_data[old_name][1], player_data[old_name][2]))
					
					total_salary += player_data[old_name][1]
			
			print "%-*s: %-*s%-*s%s" % (5, 'Pos', 25, 'Player', 10, 'Cost', 'Points')
			for pp in solution['qb']:
				print "%-*s: %-*s%-*s%s" % (5, 'QB', 25, pp[0], 10, pp[1], pp[2])
			for pp in solution['rb']:
				print "%-*s: %-*s%-*s%s" % (5, 'RB', 25, pp[0], 10, pp[1], pp[2])
			for pp in solution['wr']:
				print "%-*s: %-*s%-*s%s" % (5, 'WR', 25, pp[0], 10, pp[1], pp[2])
			for pp in solution['te']:
				print "%-*s: %-*s%-*s%s" % (5, 'TE', 25, pp[0], 10, pp[1], pp[2])
			for pp in solution['flex']:
				print "%-*s: %-*s%-*s%s" % (5, 'Flex', 25, pp[0], 10, pp[1], pp[2])
			for pp in solution['dst']:
				print "%-*s: %-*s%-*s%s" % (5, 'DST', 25, pp[0], 10, pp[1], pp[2])
			for pp in solution['k']:
				print "%-*s: %-*s%-*s%s" % (5, 'K', 25, pp[0], 10, pp[1], pp[2])
			
			print "Total Points: ", pulp.value(prob.objective)
			print "Total Salary: %s (%s%% of %s)" % (total_salary, (total_salary*1.0/cap*1.0)*100.0, cap)

			print '====================>  Done  (', k, ') <===================='