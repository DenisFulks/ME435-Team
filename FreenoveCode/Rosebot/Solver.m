m = 1;
B = 0;
speed = [50];

expectedInches = 36;

inPsec = m * speed + B;
seconds = inches/inPsec;



figure
scatter(speed, difference)