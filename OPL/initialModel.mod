*****************************************
* OPL 12.5.1.0 Model
* Author: mathieu.chiavassa, anthony.nixon
* Creation Date: 19/12/2017 at 18:20:16
*********************************************/
// A
int numNurses = ...;
int hours = ...;
range N = 1..numNurses;
range H = 1..hours;

int demand [h in H]= ...;
int minHours = ...;
int maxHours = ...;
int maxConsec = ...;

// B
int maxPresence = ...;

// A
dvar boolean works[n in N][h in H]; // this set of variable should suffice for A). Tells whether nurse n works at hour h
dvar boolean worksBefore[n in N][h in H]; // no nurse can rest more than one consec 1/3
dvar boolean worksAfter[n in N][h in H]; // 2/3
dvar boolean rests[n in N][h in H]; // 3/3
dvar boolean used[n in N];

minimize sum(n in N) used[n]; // do not change this for A)
subject to {

	// the number of provided nurses is greater or equal to the demand
	forall(h in H)
		sum(n in N) works[n][h] >= demand[h]; 


	// Each nurse should work at least minHours hours.
	forall(n in N)
		sum (h in H) works[n][h] >= minHours*used[n];

	// Each nurse should work at most maxHours hours.
	forall(n in N)
		sum (h in H) works[n][h] <= maxHours*used[n];

	// Each nurse should work at most maxConsec consecutive hours.
	forall(n in N)
		forall(i in 1..(hours-maxConsec))
			sum(j in i..(i+maxConsec)) works[n][j] <= maxConsec*used[n];

	// No nurse can stay at the hospital for more than max Presence 
	// hours (e.g. if maxP resence is 7, it is OK that a nurse works 
	// at 2am and also at 8am, but it not possible that he/she works 
	// at 2am and also at 9am).
	forall(n in N)
		forall (h in H: h <= hours-maxPresence)
			worksBefore[n][h] + worksAfter[n][h+maxPresence] <= 1;

	forall(n in N)
		forall (h in H: h <= hours-1){
			worksAfter[n][h] >= worksAfter[n][h+1]; // legal: 11111110, illegal: 11111010
			worksBefore[n][h] <= worksBefore[n][h+1]; // legal: 00011111, illegal: 00111110
			rests[n][h] + rests[n][h+1] <= 1;
			// legal: 00010100, illegal: 00110010
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