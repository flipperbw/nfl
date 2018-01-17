import cPickle as pickle
import scipy

pos_list = ['HB', 'QB', 'SS', 'WR', 'CB', 'RE', 'TE', 'C', 'LT', 'FB', 'MLB', 'DT', 'LG', 'LE', 'FS', 'LOLB', 'RT', 'RG', 'ROLB', 'P', 'K']
a = pickle.load(open('all_players.pkl', 'r'))
cols = []
for k,v in a.iteritems():
    st = v.get('stats')
    l = []
    for s in sorted(st):
        if s not in cols
            cols.append(s)

for pos in pos_list:
    all_p_data = {k:v for k,v in a.iteritems() if v.get('positionAbbr') == pos}
    xs = []
    ys = []
    for k,v in all_p_data.iteritems():
        st = v.get('stats')
        if 'HT' in st:
            del st['HT']
        l = []
        for s in sorted(st):
            ss = st[s]
            l.append(int(ss))
        ys.append(int(v.get('overall')))
        xs.append(l)
    e = scipy.optimize.lsq_linear(xs, ys, bounds=(0., 1.))
    print pos
    print (sum([h**2 for h in e.fun]) / len(e.fun)) ** 0.5
    for i,var in enumerate(cols):
        if e.x[i] >= 0.01:
            print var, round(e.x[i], 3) * 100
