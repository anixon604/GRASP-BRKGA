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
	   "nNurses": 1800,
	   "nHours":24,
	   "minHours": 6,
	   "maxHours": 18,
	   "maxConsec": 7,
	   "maxPresence": 24,
	   "demand": [964, 650, 966, 1021, 824, 387, 828, 952, 611, 468, 403, 561, 862,
               597, 1098, 855, 918, 1016, 897, 356, 615, 670, 826, 349]
}