model struc_param
	parameter Integer N = 1;
	
	Real v[N];

equation
	for i in 1:N loop
		v[i] = i * sin(time + i * 3.14);
	end for;
end struc_param;
