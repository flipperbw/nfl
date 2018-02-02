import requests
from bs4 import BeautifulSoup
import cPickle as pickle
from time import sleep
import collections
import sys

base_url = 'http://www.muthead.com'

dump_file = 'all_players.pkl'

max_pages = 22
max_chems = 4 #add to keylist

harv_dict = {
    '339': 'Harvester',
    '340': 'Turkey',
    '341': 'Stuffing',
    '342': 'Mashed Potatoes',
    '343': 'Pumpkin Pie',
    '344': 'Corn',
    '345': 'Green Beans',
    '346': 'Gravy',
    '347': 'Cranberry'
}

trait_list = [
    'High Motor',
    'Penalty',
    'Clutch',
    'QB Style',
    'Throws Tight Spiral',
    'Senses Pressure',
    'Throws Ball Away',
    'Forces Passes',
    'Covers Ball',
    'Fights for Extra Yards',
    'Makes Possession Catches',
    'Makes Aggressive Catches',
    'Makes RAC Catches',
    'Makes Sideline Catches',
    'Drops Open Passes',
    'LB Style',
    'DL Swim Move',
    'DL Bull Rush Move',
    'DL Spin Move',
    'Big Hitter',
    'Strips Ball',
    'Plays Ball in Air'
]

ratings_list = [
    'Mobile Passer',
    'Pocket Passer',
    'West Coast',
    'Deep Ball',
    'Scramble',
    'Power',
    'Elusive',
    'Receiving',
    'Pass Protection',
    'Goal Line',
    'Lead Blocker',
    'Rushing',
    'Vertical Threat',
    'Slot',
    'Possession',
    'Jump Ball',
    'Run Blocking',
    'RAC',
    'Red Zone',
    'Pass Blocking',
    'Mobility',
    'Bulldozer',
    '3-4',
    '4-3',
    'Pass Rush',
    'Run Stuff',
    'Physical',
    'Coverage',
    'Range',
    'Hands',
    'Man',
    'Zone',
    'Run Support',
    'Kick Accuracy',
    'Kick Power',
    'Fake'
]

keylist = ['name', 'fname', 'lname', 'pos', 'team', 'tier', 'overall', 'capHit', 'mobile_passer', 'pocket_passer', 'west_coast', 'deep_ball', 'scramble', 'power', 'elusive', 'receiving', 'pass_protection', 'goal_line', 'lead_blocker', 'rushing', 'vertical_threat', 'slot', 'possession', 'jump_ball', 'run_blocking', 'rac', 'red_zone', 'pass_blocking', 'mobility', 'bulldozer', '3-4', '4-3', 'pass_rush', 'run_stuff', 'physical', 'coverage', 'range', 'hands', 'man', 'zone', 'run_support', 'kick_accuracy', 'kick_power', 'fake', 'high_motor', 'penalty', 'clutch', 'qb_style', 'throws_tight_spiral', 'senses_pressure', 'throws_ball_away', 'forces_passes', 'covers_ball', 'fights_for_extra_yards', 'possession_catches', 'aggressive_catches', 'rac_catches', 'sideline_catches', 'drops_open_passes', 'lb_style', 'dl_swim_move', 'dl_bull_rush_move', 'dl_spin_move', 'big_hitter', 'strips_ball', 'plays_ball_in_air','fprice_ps4', 'fprice_xb1', 'program', 'desc_short', 'desc_long', 'jersey', 'ch1', 'ch2', 'ch3', 'ch4', 'canAuction', 'canTrade', 'url', 'pricesUrl', 'urlid', 'id', 'img', 'ACC', 'AGI', 'AWR', 'BCV', 'BKS', 'CAR', 'CIT', 'CTH', 'ELU', 'FNM', 'HT', 'HTI', 'WT', 'IMP', 'INJ', 'JKM', 'JMP', 'KAC', 'KPW', 'KR', 'MCV', 'PAC', 'PBF', 'PBK', 'PBS', 'POW', 'PRC', 'PRS', 'PUR', 'PWM', 'RBF', 'RBK', 'RBS', 'RLS', 'RTE', 'SFA', 'SPC', 'SPD', 'SPM', 'STA', 'STR', 'TAD', 'TAK', 'TAM', 'TAS', 'THA', 'THP', 'TOR', 'TRK', 'ZCV']

try:
    stored = pickle.load(open(dump_file, 'r'))
except IOError:
    stored = {}

# fetch from api
a = {}
for i in range(1, max_pages):
    print 'Fetching Page {}'.format(i)
    q = requests.get('{}/ajax/18/players/{}'.format(base_url, i))
    qj = q.json()
    a.update(qj)
    sleep(1.5)

for k in stored.keys():
    if sk not in a:
        del stored[sk]

# fix harvester and get additional data from each player page
for k,v in a.iteritems():
    if k in stored:
        continue

    """
    ch = v.get('chemistries')
    for c in ch:
        if c.get('name') in ('Madden Harvest', 'Harvester'):
            i = unicode(c.get('ID'))
            hv = harv_dict.get(i, '')
            new = 'Madden Harvest - {}'.format(hv)
            c['name'] = new
    """
    
    pid = v.get('url')
    print pid
    
    res = requests.get('{}/{}'.format(base_url, pid))

    soup = BeautifulSoup(res.text, 'lxml')

    player_data = {
        u'ratings': {},
        u'traits': {},
        u'extra': {}
    }
    
    name_stats = soup.find('div', {'class': 'name-stats'})
    jersey = name_stats.find('span', {'class': 'number'}).text.strip().replace('#','')
    weight = name_stats.find('span', {'class': 'height-weight'}).text.strip().split('Wt: ')[-1]

    desc_l = soup.find('p', {'class': 'player-description-long'})
    desc_s = soup.find('p', {'class': 'player-description-short'})
    desc_short = ''
    desc_long = ''
    if desc_l and desc_s:
        desc_short = desc_l.text.strip()
        desc_long = desc_s.text.strip()
    elif desc_l:
        desc_short = desc_l.text.strip()
    elif desc_s:
        desc_short = desc_s.text.strip()
    
    player_data['extra']['jersey'] = jersey
    player_data['extra']['weight'] = weight
    player_data['extra']['desc_short'] = desc_short
    player_data['extra']['desc_long'] = desc_long

    ratings = soup.find('div', {'class', 'player-ratings'})
    trs = ratings.find_all('tr')

    for tr in trs:
        num = tr.select('.player-rating-number')
        typ = tr.select('.player-rating-name')
        if len(num) > 0 and len(typ) > 0:
            rat_num = num[0].text.strip()
            rat_typ = typ[0].text.strip()

            player_data['ratings'][rat_typ] = rat_num

    traits = soup.find('div', {'class', 'player-traits'})
    lis = traits.find_all('li')

    for li in lis:
        conts = li.contents
        if len(conts) > 1:
            tr_typ = conts[0].text.strip()
            tr_val = conts[1].strip()
        
            player_data['traits'][tr_typ] = tr_val
    
    v.update(player_data)
    stored.update({k: v})
    
    sleep(1)

pickle.dump(stored, open(dump_file, 'wb'))

#stored = pickle.load(open(dump_file, 'r'))
    
def gd(d, k, ig=[]):
    v = d.get(k, '')
    if v in ig or v == None:
        v = ''
    str_v = unicode(v)
    return str_v

def parse(k, v):
    flat = []
    
    flat.append(gd(v, 'n'))
    flat.append(gd(v, 'fname'))
    flat.append(gd(v, 'lname'))
    flat.append(gd(v, 'positionAbbr'))
    flat.append(gd(v, 'teamAbbr'))
    flat.append(gd(v, 'tier'))
    flat.append(gd(v, 'overall'))
    flat.append(gd(v, 'capHit'))
    
    p_rats = v.get('ratings', {})
    for rat in ratings_list:
        flat.append(gd(p_rats, rat))
    
    p_traits = v.get('traits', {})
    for tra in trait_list:
        flat.append(gd(p_traits, tra))
    
    fprice = v.get('prices', {}).get('full', {})
    flat.append(gd(fprice, 'ps4', ['No Auction', 'Unknown', '0', 0]))
    flat.append(gd(fprice, 'xb1', ['No Auction', 'Unknown', '0', 0]))
    
    prog = v.get('program', {})
    flat.append(gd(prog, 'name'))
    
    extra = v.get('extra', {})
    flat.append(gd(extra, 'desc_short'))
    flat.append(gd(extra, 'desc_long'))
    flat.append(gd(extra, 'jersey'))
    weight = gd(extra, 'weight')
    
    chems = v.get('chemistries', [])
    chemlist = [''] * max_chems
    for i,c in enumerate(chems):
        cn = gd(c, 'name')
        cq = gd(c, 'quantity')
        chemlist[i] = '{}:{}'.format(cn, cq)
    for ch in chemlist:
        flat.append(ch)
    
    flat.append(gd(v, 'canAuction'))
    flat.append(gd(v, 'canTrade'))
    flat.append(gd(v, 'url'))
    flat.append(gd(v, 'pricesUrl'))
    flat.append(gd(v, 'urlid'))
    flat.append(gd(v, 'id'))
    flat.append(gd(v, 'img'))
    
    stats = v.get('stats', {})
    #expecting them all to be there
    st = [''] * 50
    i = 0
    for s in sorted(stats):
        v = stats[s]
        st[i] = str(v).replace(' ', '')
        i += 1
        if s == 'HT':
            vs = v.split("'")
            inch = 0
            inch += (int(vs[0]) * 12)
            inch += (int(vs[1].strip().replace('"','')))
            st[i] = str(inch)
            i += 1
            st[i] = str(weight)
            i += 1
    
    for ss in st:
        flat.append(ss)
    
    return flat

# dump to excel format
print '|'.join(keylist)

for k,v in stored.iteritems():
    res = parse(k, v)
    print '|'.join(res)
