""" File contains data sets for GRASP.py """

SMALL = {
	   "nNurses": 30,
	   "nHours":9,
	   "minHours": 3,
	   "maxHours": 6,
	   "maxConsec": 7,
	   "maxPresence": 8,
	   "demand": [5, 3, 8, 5, 1, 7, 5, 6, 2]
}

MID = {
	   "nNurses": 200,
	   "nHours":24,
	   "minHours": 6,
	   "maxHours": 12,
	   "maxConsec": 6,
	   "maxPresence": 18,
	   "demand": [53, 24, 33, 40, 70, 12, 33, 55, 66, 12, 30, 22, 55,
               77, 88, 22, 34, 55, 22, 55, 23, 22, 11, 12]
}

LARGE = {
	   "nNurses": 900,
	   "nHours":24,
	   "minHours": 6,
	   "maxHours": 18,
	   "maxConsec": 7,
	   "maxPresence": 24,
	   "demand": [482, 325, 483, 510, 412, 193, 414, 476, 305, 234, 202,
	   		        	280, 431, 300, 549, 426, 460, 508, 448, 178, 307, 345, 413, 178]
}
