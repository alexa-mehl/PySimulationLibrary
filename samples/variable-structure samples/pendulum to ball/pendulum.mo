model pendulum
  constant Real g = 9.81;
  parameter Real L = 1;
  parameter Real m = 20;
  
  Real phi;
  Real derPhi(start = 5);
  Real F;
  
equation
  der(phi) = derPhi;
  der(derPhi) = - g/L * sin(phi);
  F = m * g * cos(phi) + m * L * derPhi^2;
end pendulum;
