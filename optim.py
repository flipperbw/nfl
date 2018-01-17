#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pulp
from numpy import random
from collections import Counter

iterations = 10

total_cap = 200
bench_cap = 30
cap = total_cap - bench_cap

roster = {
    "qb": 1,
    "rb": 2,
    "wr": 2,
    "te": 1,
    "flex": 2
}

#needs = ["Aaron Rodgers|QB|GB"]
needs = []

cost_range = 0.1
vbd_range = 0.005

#{"player": "Aaron Rodgers|QB|GB", "pos": "QB", "cost": 71.1219845721039, "vbd": 241.912},
player_data = [
    {"player": "Aaron Rodgers|QB|GB", "pos": "QB", "cost": 71.1219845721039, "vbd": 241.912},
    {"player": "Tom Brady|QB|NE", "pos": "QB", "cost": 64.136923034646, "vbd": 220.808},
    {"player": "Drew Brees|QB|NO", "pos": "QB", "cost": 61.2639921141979, "vbd": 212.128},
    {"player": "Matt Ryan|QB|ATL", "pos": "QB", "cost": 59.2304336377887, "vbd": 205.984},
    {"player": "Russell Wilson|QB|SEA", "pos": "QB", "cost": 56.0781532130943, "vbd": 196.46},
    {"player": "Jameis Winston|QB|TB", "pos": "QB", "cost": 52.4611729021892, "vbd": 185.532},
    {"player": "Cam Newton|QB|CAR", "pos": "QB", "cost": 52.0984157260589, "vbd": 184.436},
    {"player": "Marcus Mariota|QB|TEN", "pos": "QB", "cost": 48.8925160837249, "vbd": 174.75},
    {"player": "Kirk Cousins|QB|WAS", "pos": "QB", "cost": 48.3702251859752, "vbd": 173.172},
    {"player": "Andrew Luck|QB|IND", "pos": "QB", "cost": 48.2212829147538, "vbd": 172.722},
    {"player": "Dak Prescott|QB|DAL", "pos": "QB", "cost": 47.0893216534713, "vbd": 169.302},
    {"player": "Matthew Stafford|QB|DET", "pos": "QB", "cost": 47.0436460236301, "vbd": 169.164},
    {"player": "Philip Rivers|QB|LAC", "pos": "QB", "cost": 46.99201270294, "vbd": 169.008},
    {"player": "Ben Roethlisberger|QB|PIT", "pos": "QB", "cost": 46.8999994776077, "vbd": 168.73},
    {"player": "Derek Carr|QB|OAK", "pos": "QB", "cost": 45.7362638651313, "vbd": 165.214},
    {"player": "Andy Dalton|QB|CIN", "pos": "QB", "cost": 44.1157719542426, "vbd": 160.318},
    {"player": "Tyrod Taylor|QB|BUF", "pos": "QB", "cost": 42.885839776779, "vbd": 156.602},
    {"player": "Eli Manning|QB|NYG", "pos": "QB", "cost": 40.9992376746414, "vbd": 150.902},
    {"player": "Carson Wentz|QB|PHI", "pos": "QB", "cost": 39.0285659349701, "vbd": 144.948},
    {"player": "Carson Palmer|QB|ARI", "pos": "QB", "cost": 38.6942732817843, "vbd": 143.938},
    {"player": "Joe Flacco|QB|BAL", "pos": "QB", "cost": 36.264859346751, "vbd": 136.598},
    {"player": "Alex Smith|QB|KC", "pos": "QB", "cost": 32.4022897797432, "vbd": 124.928},
    {"player": "Sam Bradford|QB|MIN", "pos": "QB", "cost": 30.8837405789349, "vbd": 120.34},
    {"player": "Jay Cutler|QB|MIA", "pos": "QB", "cost": 27.9883028263912, "vbd": 111.592},
    {"player": "Blake Bortles|QB|JAC", "pos": "QB", "cost": 24.2541545954587, "vbd": 100.31},
    {"player": "Jared Goff|QB|LAR", "pos": "QB", "cost": 19.4774104659764, "vbd": 85.878},
    {"player": "Trevor Siemian|QB|DEN", "pos": "QB", "cost": 18.6393619532375, "vbd": 83.346},
    {"player": "Brian Hoyer|QB|SF", "pos": "QB", "cost": 16.898392294072, "vbd": 78.086},
    {"player": "Mike Glennon|QB|CHI", "pos": "QB", "cost": 12.9312321543842, "vbd": 66.1},
    {"player": "DeShone Kizer|QB|CLE", "pos": "QB", "cost": 11.157164212725, "vbd": 60.74},
    {"player": "Josh McCown|QB|NYJ", "pos": "QB", "cost": 9.69538099236174, "vbd": 52.782},
    {"player": "Deshaun Watson|QB|HOU", "pos": "QB", "cost": 8.39542624864335, "vbd": 45.705},
    {"player": "Tom Savage|QB|HOU", "pos": "QB", "cost": 4.08318411729774, "vbd": 22.229},
    {"player": "Mitch Trubisky|QB|CHI", "pos": "QB", "cost": 0.804366514447199, "vbd": 4.379},
    {"player": "David Johnson|RB|ARI", "pos": "RB", "cost": 63.2865959157589, "vbd": 202.04},
    {"player": "Le'Veon Bell|RB|PIT", "pos": "RB", "cost": 58.1861505834889, "vbd": 186.63},
    {"player": "LeSean McCoy|RB|BUF", "pos": "RB", "cost": 38.9891467371772, "vbd": 128.63},
    {"player": "Devonta Freeman|RB|ATL", "pos": "RB", "cost": 36.1923418664646, "vbd": 120.18},
    {"player": "Melvin Gordon|RB|LAC", "pos": "RB", "cost": 34.6102439632685, "vbd": 115.4},
    {"player": "Jordan Howard|RB|CHI", "pos": "RB", "cost": 33.3028618047697, "vbd": 111.45},
    {"player": "Jay Ajayi|RB|MIA", "pos": "RB", "cost": 31.8531570315482, "vbd": 107.07},
    {"player": "DeMarco Murray|RB|TEN", "pos": "RB", "cost": 29.9930335554056, "vbd": 101.45},
    {"player": "Todd Gurley|RB|LAR", "pos": "RB", "cost": 27.1829893716955, "vbd": 92.96},
    {"player": "Lamar Miller|RB|HOU", "pos": "RB", "cost": 24.1710456647742, "vbd": 83.86},
    {"player": "Leonard Fournette|RB|JAC", "pos": "RB", "cost": 22.1255718066672, "vbd": 77.68},
    {"player": "Ezekiel Elliott|RB|DAL", "pos": "RB", "cost": 20.1065765745551, "vbd": 71.58},
    {"player": "Isaiah Crowell|RB|CLE", "pos": "RB", "cost": 20.096647089807, "vbd": 71.55},
    {"player": "Dalvin Cook|RB|MIN", "pos": "RB", "cost": 18.7627863053133, "vbd": 67.52},
    {"player": "Christian McCaffrey|RB|CAR", "pos": "RB", "cost": 18.123989453186, "vbd": 65.59},
    {"player": "Ty Montgomery|RB|GB", "pos": "RB", "cost": 17.4653336315626, "vbd": 63.6},
    {"player": "Marshawn Lynch|RB|OAK", "pos": "RB", "cost": 17.3759682688298, "vbd": 63.33},
    {"player": "Bilal Powell|RB|NYJ", "pos": "RB", "cost": 17.0648444133895, "vbd": 62.39},
    {"player": "Mark Ingram|RB|NO", "pos": "RB", "cost": 16.5518210347381, "vbd": 60.84},
    {"player": "Kareem Hunt|RB|KC", "pos": "RB", "cost": 14.8571889710637, "vbd": 55.72},
    {"player": "Joe Mixon|RB|CIN", "pos": "RB", "cost": 14.4136719856489, "vbd": 54.38},
    {"player": "Carlos Hyde|RB|SF", "pos": "RB", "cost": 13.5928345798066, "vbd": 51.9},
    {"player": "Ameer Abdullah|RB|DET", "pos": "RB", "cost": 11.4877838132111, "vbd": 45.54},
    {"player": "Tevin Coleman|RB|ATL", "pos": "RB", "cost": 11.4282069047225, "vbd": 45.36},
    {"player": "Frank Gore|RB|IND", "pos": "RB", "cost": 10.3359635824324, "vbd": 42.06},
    {"player": "C.J. Anderson|RB|DEN", "pos": "RB", "cost": 8.43943199554675, "vbd": 36.33},
    {"player": "Terrance West|RB|BAL", "pos": "RB", "cost": 8.29379955257474, "vbd": 35.89},
    {"player": "Danny Woodhead|RB|BAL", "pos": "RB", "cost": 7.63514373095128, "vbd": 33.9},
    {"player": "Theo Riddick|RB|DET", "pos": "RB", "cost": 7.40676558174516, "vbd": 33.21},
    {"player": "Paul Perkins|RB|NYG", "pos": "RB", "cost": 6.93676997033546, "vbd": 31.79},
    {"player": "Duke Johnson|RB|CLE", "pos": "RB", "cost": 5.99677874751606, "vbd": 28.95},
    {"player": "Eddie Lacy|RB|SEA", "pos": "RB", "cost": 4.47094792455922, "vbd": 24.34},
    {"player": "Robert Kelley|RB|WAS", "pos": "RB", "cost": 4.31297688038827, "vbd": 23.48},
    {"player": "Mike Gillislee|RB|NE", "pos": "RB", "cost": 4.24960477545922, "vbd": 23.135},
    {"player": "Doug Martin|RB|TB", "pos": "RB", "cost": 3.91253865214097, "vbd": 21.3},
    {"player": "Matt Forte|RB|NYJ", "pos": "RB", "cost": 3.60761779943891, "vbd": 19.64},
    {"player": "Darren Sproles|RB|PHI", "pos": "RB", "cost": 3.59384125488912, "vbd": 19.565},
    {"player": "Adrian Peterson|RB|NO", "pos": "RB", "cost": 3.29718632891692, "vbd": 17.95},
    {"player": "James White|RB|NE", "pos": "RB", "cost": 3.2393248418078, "vbd": 17.635},
    {"player": "Jonathan Stewart|RB|CAR", "pos": "RB", "cost": 3.17319742796879, "vbd": 17.275},
    {"player": "Derrick Henry|RB|TEN", "pos": "RB", "cost": 2.82511006901071, "vbd": 15.38},
    {"player": "LeGarrette Blount|RB|PHI", "pos": "RB", "cost": 2.66070997071653, "vbd": 14.485},
    {"player": "Chris Thompson|RB|WAS", "pos": "RB", "cost": 2.3530338091045, "vbd": 12.81},
    {"player": "Giovani Bernard|RB|CIN", "pos": "RB", "cost": 2.2869063952655, "vbd": 12.45},
    {"player": "Darren McFadden|RB|DAL", "pos": "RB", "cost": 2.05086826531239, "vbd": 11.165},
    {"player": "C.J. Prosise|RB|SEA", "pos": "RB", "cost": 1.66145127270493, "vbd": 9.04499999999999},
    {"player": "Jamaal Charles|RB|DEN", "pos": "RB", "cost": 1.58981324104602, "vbd": 8.655},
    {"player": "Shane Vereen|RB|NYG", "pos": "RB", "cost": 1.5135830278705, "vbd": 8.23999999999999},
    {"player": "Thomas Rawls|RB|SEA", "pos": "RB", "cost": 0.66862162881658, "vbd": 3.64},
    {"player": "Charles Sims|RB|TB", "pos": "RB", "cost": 0.503303094219073, "vbd": 2.73999999999999},
    {"player": "Rex Burkhead|RB|NE", "pos": "RB", "cost": 0.0450033788626539, "vbd": 0.244999999999997},
    {"player": "Rob Gronkowski|TE|NE", "pos": "TE", "cost": 21.593444880538, "vbd": 69.21},
    {"player": "Travis Kelce|TE|KC", "pos": "TE", "cost": 15.784696302904, "vbd": 51.66},
    {"player": "Greg Olsen|TE|CAR", "pos": "TE", "cost": 14.1330920064713, "vbd": 46.67},
    {"player": "Jordan Reed|TE|WAS", "pos": "TE", "cost": 9.52912091160592, "vbd": 32.76},
    {"player": "Jimmy Graham|TE|SEA", "pos": "TE", "cost": 7.31153598453199, "vbd": 26.06},
    {"player": "Kyle Rudolph|TE|MIN", "pos": "TE", "cost": 6.16302558200264, "vbd": 22.59},
    {"player": "Zach Ertz|TE|PHI", "pos": "TE", "cost": 4.93507930148857, "vbd": 18.88},
    {"player": "Tyler Eifert|TE|CIN", "pos": "TE", "cost": 3.04516737110168, "vbd": 13.17},
    {"player": "Delanie Walker|TE|TEN", "pos": "TE", "cost": 2.98559046261313, "vbd": 12.99},
    {"player": "Martellus Bennett|TE|GB", "pos": "TE", "cost": 1.63849036512195, "vbd": 8.92000000000001},
    {"player": "Eric Ebron|TE|DET", "pos": "TE", "cost": 1.22519402862818, "vbd": 6.67},
    {"player": "Hunter Henry|TE|LAC", "pos": "TE", "cost": 0.759546822845209, "vbd": 4.13500000000001},
    {"player": "Jack Doyle|TE|IND", "pos": "TE", "cost": 0.294818053365552, "vbd": 1.605},
    {"player": "Jason Witten|TE|DAL", "pos": "TE", "cost": 0.0385743247394195, "vbd": 0.210000000000008},
    {"player": "Antonio Brown|WR|PIT", "pos": "WR", "cost": 45.3136044145065, "vbd": 147.48},
    {"player": "Julio Jones|WR|ATL", "pos": "WR", "cost": 44.4398097566744, "vbd": 144.84},
    {"player": "Odell Beckham Jr.|WR|NYG", "pos": "WR", "cost": 38.8197213892542, "vbd": 127.86},
    {"player": "Mike Evans|WR|TB", "pos": "WR", "cost": 35.4436965749029, "vbd": 117.66},
    {"player": "Jordy Nelson|WR|GB", "pos": "WR", "cost": 34.9207437115033, "vbd": 116.08},
    {"player": "A.J. Green|WR|CIN", "pos": "WR", "cost": 32.4549216657271, "vbd": 108.63},
    {"player": "Michael Thomas|WR|NO", "pos": "WR", "cost": 31.4321847366736, "vbd": 105.54},
    {"player": "T.Y. Hilton|WR|IND", "pos": "WR", "cost": 28.2117218500424, "vbd": 95.81},
    {"player": "Doug Baldwin|WR|SEA", "pos": "WR", "cost": 26.6064551491008, "vbd": 90.96},
    {"player": "Amari Cooper|WR|OAK", "pos": "WR", "cost": 26.3648376868972, "vbd": 90.23},
    {"player": "Brandin Cooks|WR|NE", "pos": "WR", "cost": 24.9978786199098, "vbd": 86.1},
    {"player": "Dez Bryant|WR|DAL", "pos": "WR", "cost": 24.4517569587648, "vbd": 84.45},
    {"player": "DeAndre Hopkins|WR|HOU", "pos": "WR", "cost": 22.7339560973448, "vbd": 79.26},
    {"player": "Demaryius Thomas|WR|DEN", "pos": "WR", "cost": 22.6743791888563, "vbd": 79.08},
    {"player": "Allen Robinson|WR|JAC", "pos": "WR", "cost": 20.7381296629783, "vbd": 73.23},
    {"player": "Michael Crabtree|WR|OAK", "pos": "WR", "cost": 20.6421446437467, "vbd": 72.94},
    {"player": "Larry Fitzgerald|WR|ARI", "pos": "WR", "cost": 19.9239119136347, "vbd": 70.77},
    {"player": "Golden Tate|WR|DET", "pos": "WR", "cost": 19.7584205011665, "vbd": 70.27},
    {"player": "Alshon Jeffery|WR|PHI", "pos": "WR", "cost": 19.3546214547441, "vbd": 69.05},
    {"player": "Jarvis Landry|WR|MIA", "pos": "WR", "cost": 18.0009017007542, "vbd": 64.96},
    {"player": "Terrelle Pryor|WR|WAS", "pos": "WR", "cost": 17.4680193526066, "vbd": 63.35},
    {"player": "Emmanuel Sanders|WR|DEN", "pos": "WR", "cost": 17.153585668917, "vbd": 62.4},
    {"player": "Stefon Diggs|WR|MIN", "pos": "WR", "cost": 16.9185878632121, "vbd": 61.69},
    {"player": "Tyreek Hill|WR|KC", "pos": "WR", "cost": 16.6868998857566, "vbd": 60.99},
    {"player": "Keenan Allen|WR|LAC", "pos": "WR", "cost": 16.5214084732884, "vbd": 60.49},
    {"player": "Davante Adams|WR|GB", "pos": "WR", "cost": 16.2301435873444, "vbd": 59.61},
    {"player": "Kelvin Benjamin|WR|CAR", "pos": "WR", "cost": 15.6939514109474, "vbd": 57.99},
    {"player": "Willie Snead|WR|NO", "pos": "WR", "cost": 14.7307913903825, "vbd": 55.08},
    {"player": "Sammy Watkins|WR|LAR", "pos": "WR", "cost": 14.3203726874613, "vbd": 53.84},
    {"player": "Jamison Crowder|WR|WAS", "pos": "WR", "cost": 13.4300288883824, "vbd": 51.15},
    {"player": "Pierre Garcon|WR|SF", "pos": "WR", "cost": 13.0891165786979, "vbd": 50.12},
    {"player": "Devante Parker|WR|MIA", "pos": "WR", "cost": 11.2223734460565, "vbd": 44.48},
    {"player": "Martavis Bryant|WR|PIT", "pos": "WR", "cost": 11.2025144765603, "vbd": 44.42},
    {"player": "Randall Cobb|WR|GB", "pos": "WR", "cost": 11.1098392855782, "vbd": 44.14},
    {"player": "Brandon Marshall|WR|NYG", "pos": "WR", "cost": 10.5835765939293, "vbd": 42.55},
    {"player": "Kenny Britt|WR|CLE", "pos": "WR", "cost": 9.19675855744572, "vbd": 38.36},
    {"player": "Jeremy Maclin|WR|BAL", "pos": "WR", "cost": 9.08091456871797, "vbd": 38.01},
    {"player": "Mike Wallace|WR|BAL", "pos": "WR", "cost": 8.87901504550677, "vbd": 37.4},
    {"player": "DeSean Jackson|WR|TB", "pos": "WR", "cost": 8.32627372786296, "vbd": 35.73},
    {"player": "Eric Decker|WR|TEN", "pos": "WR", "cost": 8.20711991088585, "vbd": 35.37},
    {"player": "Adam Thielen|WR|MIN", "pos": "WR", "cost": 7.24395989032091, "vbd": 32.46},
    {"player": "Tyrell Williams|WR|LAC", "pos": "WR", "cost": 7.12480607334381, "vbd": 32.1},
    {"player": "Donte Moncrief|WR|IND", "pos": "WR", "cost": 6.98579328687051, "vbd": 31.68},
    {"player": "Jordan Matthews|WR|BUF", "pos": "WR", "cost": 6.85670998514531, "vbd": 31.29},
    {"player": "Rishard Matthews|WR|TEN", "pos": "WR", "cost": 5.8074944300969, "vbd": 28.12},
    {"player": "Corey Coleman|WR|CLE", "pos": "WR", "cost": 4.9866570242546, "vbd": 25.64},
    {"player": "Robby Anderson|WR|NYJ", "pos": "WR", "cost": 4.63250540157265, "vbd": 24.57},
    {"player": "Marvin Jones|WR|DET", "pos": "WR", "cost": 4.36440931337416, "vbd": 23.76},
    {"player": "John Brown|WR|ARI", "pos": "WR", "cost": 4.13020805602769, "vbd": 22.485},
    {"player": "Cole Beasley|WR|DAL", "pos": "WR", "cost": 4.10081809432147, "vbd": 22.325},
    {"player": "Chris Hogan|WR|NE", "pos": "WR", "cost": 4.06683595109865, "vbd": 22.14},
    {"player": "Ted Ginn|WR|NO", "pos": "WR", "cost": 3.7251776462638, "vbd": 20.28},
    {"player": "Sterling Shepard|WR|NYG", "pos": "WR", "cost": 3.65813179612148, "vbd": 19.915},
    {"player": "Corey Davis|WR|TEN", "pos": "WR", "cost": 3.56720660209285, "vbd": 19.42},
    {"player": "Kevin White|WR|CHI", "pos": "WR", "cost": 3.14656277517253, "vbd": 17.13},
    {"player": "Zay Jones|WR|BUF", "pos": "WR", "cost": 3.08502754285013, "vbd": 16.795},
    {"player": "Mohamed Sanu|WR|ATL", "pos": "WR", "cost": 3.04645321811071, "vbd": 16.585},
    {"player": "Tyler Lockett|WR|SEA", "pos": "WR", "cost": 2.91327995412938, "vbd": 15.86},
    {"player": "Allen Hurns|WR|JAC", "pos": "WR", "cost": 2.4568171113796, "vbd": 13.375},
    {"player": "Breshad Perriman|WR|BAL", "pos": "WR", "cost": 2.40079249687711, "vbd": 13.07},
    {"player": "Torrey Smith|WR|PHI", "pos": "WR", "cost": 2.38334220711404, "vbd": 12.975},
    {"player": "Kenny Stills|WR|MIA", "pos": "WR", "cost": 2.37140253517089, "vbd": 12.91},
    {"player": "Taylor Gabriel|WR|ATL", "pos": "WR", "cost": 2.17761247517048, "vbd": 11.855},
    {"player": "Marqise Lee|WR|JAC", "pos": "WR", "cost": 2.14730407716094, "vbd": 11.69},
    {"player": "Devin Funchess|WR|CAR", "pos": "WR", "cost": 1.90851063829787, "vbd": 10.39},
    {"player": "Kendall Wright|WR|CHI", "pos": "WR", "cost": 1.58613949583274, "vbd": 8.63499999999999},
    {"player": "Kenny Golladay|WR|DET", "pos": "WR", "cost": 1.32897733090328, "vbd": 7.23499999999999},
    {"player": "Terrance Williams|WR|DAL", "pos": "WR", "cost": 1.16549566891242, "vbd": 6.34499999999999},
    {"player": "J.J. Nelson|WR|ARI", "pos": "WR", "cost": 1.13702414350951, "vbd": 6.19},
    {"player": "Chris Conley|WR|KC", "pos": "WR", "cost": 1.04793582208752, "vbd": 5.70499999999999},
    {"player": "Josh Doctson|WR|WAS", "pos": "WR", "cost": 0.96711342739541, "vbd": 5.265},
    {"player": "Marquise Goodwin|WR|SF", "pos": "WR", "cost": 0.753117768721971, "vbd": 4.09999999999999},
    {"player": "ArDarius Stewart|WR|NYJ", "pos": "WR", "cost": 0.689745663792927, "vbd": 3.755},
    {"player": "Tavon Austin|WR|LAR", "pos": "WR", "cost": 0.677805991849774, "vbd": 3.69},
    {"player": "John Ross|WR|CIN", "pos": "WR", "cost": 0.38758012000082, "vbd": 2.11},
    {"player": "Brandon LaFell|WR|CIN", "pos": "WR", "cost": 0.363700776114511, "vbd": 1.97999999999999},
    {"player": "Robert Woods|WR|LAR", "pos": "WR", "cost": 0.318697397251859, "vbd": 1.735}
]

solution_list = {"qb": [], "rb": [], "wr": [], "te": []}
solution_cost_list = []

for loop in range(0, iterations):
    l = []
    for p in player_data:
        i = p.copy()
        newc = max(1, i.get('cost') + (random.normal(0,50) / 100.0 * cost_range))
        newv = max(0, i.get('vbd') * (1 + random.normal(0, 500) / 1000.0 * vbd_range))
        i['cost'] = newc
        i['vbd'] = newv
        l.append(i)

    player_names = {"QB":[], "RB":[], "WR": [], "TE": []}
    for pl in l:
        player_names[pl.get('pos')].append(pl.get('player'))

    qb_names = player_names['QB']
    rb_names = player_names['RB']
    wr_names = player_names['WR']
    te_names = player_names['TE']
    flex_names = rb_names + wr_names + te_names
    all_names = qb_names + rb_names + wr_names + te_names

    prob = pulp.LpProblem("Optimization", pulp.LpMaximize)

#- Set the variables (boolean player names)
    player_vars = pulp.LpVariable.dicts("Players", all_names, cat="Binary")

#- Set the objective (maximize points)
    prob += pulp.lpSum([filter(lambda x: x['player'] == i, l)[0].get('vbd') * player_vars[i] for i in all_names]), "Total VBD"

#- Set the contraints (budget and then roster)
    prob += pulp.lpSum([filter(lambda x: x['player'] == i, l)[0].get('cost') * player_vars[i] for i in all_names]) <= cap, "Total Cost"

    prob += pulp.lpSum([player_vars[i] for i in qb_names]) == roster['qb'], "Total QBs"
    prob += pulp.lpSum([player_vars[i] for i in rb_names]) >= roster['rb'], "Total RBs"
    prob += pulp.lpSum([player_vars[i] for i in wr_names]) >= roster['wr'], "Total WRs"
    prob += pulp.lpSum([player_vars[i] for i in te_names]) >= roster['te'], "Total TEs"
    prob += pulp.lpSum([player_vars[i] for i in flex_names]) == roster['rb'] + roster['wr'] + roster['te'] + roster['flex'], "Total Flexs"

    for i in needs:
        prob += pulp.lpSum([player_vars[i]]) == 1, "Required: {}".format(i)

#- Solve
    #prob.writeLP("espn_solution.lp")
    prob.solve()
    #prob.solve(pulp.GLPK())

    if pulp.LpStatus[prob.status] != 'Optimal':
        print 'Status not optimal -> %s' % pulp.LpStatus[prob.status]
    else:
        new_player_vars = {}
        for on,nn in player_vars.iteritems():
            new_player_vars[nn.name] = on

        solution = {"qb": [], "rb": [], "wr": [], "te": [], "flex": []}
        total_salary = 0
        rb_count = wr_count = te_count = 0
        solution_cost = {"qb": 0, "rb": 0, "wr": 0, "te": 0, "flex": 0}
        
        var_list = []
        for v in prob.variables():
            if v.varValue == 1:
                old_name = new_player_vars[v.name]

                old_player = filter(lambda x: x['player'] == old_name, l)[0]
                old_player_pos = old_player.get('pos').lower()
                old_player_cost = round(old_player.get('cost'), 1)
                old_player_vbd = round(old_player.get('vbd'), 1)

                var_list.append((old_name, old_player_pos, old_player_cost, old_player_vbd))

        var_list = sorted(var_list, key=lambda s: s[3], reverse=True)

        for y in var_list:
            old_name = y[0]
            old_player_pos = y[1]
            old_player_cost = y[2]
            old_player_vbd = y[3]
            
            add_list = solution_list[old_player_pos]
            add_list.append(old_name)

            
            if old_player_pos == 'rb':
                if rb_count < roster['rb']:
                    solution[old_player_pos].append((old_name, old_player_cost, old_player_vbd))
                    solution_cost[old_player_pos] += old_player_cost
                    rb_count += 1
                else:
                    solution["flex"].append((old_name, old_player_cost, old_player_vbd))
                    solution_cost['flex'] += old_player_cost
            elif old_player_pos == 'wr':
                if wr_count < roster['wr']:
                    solution[old_player_pos].append((old_name, old_player_cost, old_player_vbd))
                    solution_cost[old_player_pos] += old_player_cost
                    wr_count += 1
                else:
                    solution["flex"].append((old_name, old_player_cost, old_player_vbd))
                    solution_cost['flex'] += old_player_cost
            elif old_player_pos == 'te':
                if te_count < roster['te']:
                    solution[old_player_pos].append((old_name, old_player_cost, old_player_vbd))
                    solution_cost[old_player_pos] += old_player_cost
                    te_count += 1
                else:
                    solution["flex"].append((old_name, old_player_cost, old_player_vbd))
                    solution_cost['flex'] += old_player_cost
            else:
                solution[old_player_pos].append((old_name, old_player_cost, old_player_vbd))
                solution_cost[old_player_pos] += old_player_cost

            total_salary += old_player_cost

        solution_cost_list.append(solution_cost)

        
        print "%-*s: %-*s%-*s%s" % (5, 'Pos', 30, 'Player', 10, 'Cost', 'Points')
        for pp in solution['qb']:
            print "%-*s: %-*s%-*s%s" % (5, 'QB', 30, pp[0], 10, pp[1], pp[2])
        for pp in solution['rb']:
            print "%-*s: %-*s%-*s%s" % (5, 'RB', 30, pp[0], 10, pp[1], pp[2])
        for pp in solution['wr']:
            print "%-*s: %-*s%-*s%s" % (5, 'WR', 30, pp[0], 10, pp[1], pp[2])
        for pp in solution['te']:
            print "%-*s: %-*s%-*s%s" % (5, 'TE', 30, pp[0], 10, pp[1], pp[2])
        for pp in solution['flex']:
            print "%-*s: %-*s%-*s%s" % (5, 'Flex', 30, pp[0], 10, pp[1], pp[2])
        
        print
        print "Total Points: ", pulp.value(prob.objective)
        print "Total Salary: %s (%s%% of %s)" % (total_salary, (total_salary*1.0/cap*1.0)*100.0, cap)
        print
        print '-------------'
        print
        

"""
for pp in ('qb', 'rb', 'wr', 'te'):
    count_players = Counter(solution_list[pp])
    print pp.upper()
    for a in count_players.most_common():
        print "\t%-*s: %-*s" % (5, a[1], 30, a[0])

for pp in ('qb', 'rb', 'wr', 'te', 'flex'):
    print pp.upper()
    pl_cnt = 0
    tot_cos = 0
    for j in solution_cost_list:
        pl_cnt += 1
        tot_cos += j.get(pp)
    print tot_cos * 1.0 / pl_cnt
    print
"""
