/*********************************************
* OPL 12.5.1.0 Model
* Author: mathieu.chiavassa, anthony.nixon
* Creation Date: 19/12/2017 at 18:20:16
*********************************************/

int numNurses = ...;
int hours = ...;
range N = 1..numNurses;
range H = 1..hours;

int demand [h in H]= ...;
int minHours = ...;
int maxHours = ...;
int maxConsec = ...;

int maxPresence = ...;

dvar boolean works[n in N][h in H]; 	  // Whether nurse n works at hour h
dvar boolean worksBefore[n in N][h in H]; // Relative to a given hour, tracks if the nurse works before
dvar boolean worksAfter[n in N][h in H];  // Relative to a given hour, tracks if the nurse works after
dvar boolean rests[n in N][h in H]; 	  // Whether a nurse rests at hour h
dvar boolean used[n in N];				  // If nurse n is used or not

minimize sum(n in N) used[n]; 			  // Objective is to minimize the number of nurses 
subject to {

	// Constraint 1
	// The number of provided nurses must be greater or equal to the demand of each hour
	forall(h in H)
		sum(n in N) works[n][h] >= demand[h]; 

	// Constraint 2
	// Each nurse that is working must work at least minHours.
	forall(n in N)
		sum (h in H) works[n][h] >= minHours*used[n];

	// Constraint 3
	// No nurse that is working can work more than maxHours hours.
	forall(n in N)
		sum (h in H) works[n][h] <= maxHours*used[n];

	// Constraint 4
	// Each nurse should work at most maxConsec consecutive hours - must have a break to work more.
	// - algorithm uses sliding window comparisons
	forall(n in N)
		forall(i in 1..(hours-maxConsec))
			sum(j in i..(i+maxConsec)) works[n][j] <= maxConsec*used[n];

	// Constraint 5 and 6
	// No nurse can stay at the hospital for more than maxPresence number of hours
	// Rests must be no longer than one hour in length
	forall(n in N)
		forall (h in H: h <= hours-maxPresence)
			worksBefore[n][h] + worksAfter[n][h+maxPresence] <= 1;
	
	forall(n in N)
		forall (h in H: h <= hours-1){
			worksAfter[n][h] >= worksAfter[n][h+1];   // allowed: 11110, rejected: 10101
			worksBefore[n][h] <= worksBefore[n][h+1]; // allowed: 00111, rejected: 01110
			rests[n][h] + rests[n][h+1] <= 1;         // allowed: 10100, rejected: 11001
		}

	forall(n in N)
		forall (h in H)
			rests[n][h] == (1-works[n][h]) - (1-worksAfter[n][h]) - (1-worksBefore[n][h]); 
}

execute { // Should not be changed. Assumes that variables works[n][h] are used.
	for (var n in N) {
		write("Nurse ");
		if (n < 10) write(" ");
		write(n + " works: ");
		var minHour = -1;
		var maxHour = -1;
		var totalHours = 0;
		for (var h in H) {
			if (works[n][h] == 1) {
			totalHours++;
			write(" W"); 
			if (minHour == -1) minHour = h;
			maxHour = h; 
			}
			else write(" .");
		}
		if (minHour != -1) write(" Presence: " + (maxHour - minHour +1));
		else write(" Presence: 0")
		writeln ("\t(TOTAL " + totalHours + "h)"); 
	} 
	writeln("");
	write("Demand: ");

	for (h in H) {
		if (demand[h] < 10) write(" ");
		write(" " + demand[h]); 
	}
	writeln("");
	write("Assigned: ");
	for (h in H) {
		var total = 0;
		for (n in N)
		if (works[n][h] == 1) total = total+1;
		if (total < 10) write(" ");
		write(" " + total); 
	} 
}