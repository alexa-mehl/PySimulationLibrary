model ball
	Real x;
	Real y;
	Real vx(start = 1);
	Real vy(start = 2);
	
	constant Real g = 9.81;
	
	parameter Real m = 20;

equation
  vx = der(x);
  vy = der(y);
  m * der(vx) = 0;
  m * der(vy) = -g*m;

end ball;
