model pendulum
  constant Real g = 9.81;
  parameter Real L = 1;
  
  Real phi;
  Real derPhi(start = 5);
  
equation
  der(phi) = derPhi;
  der(derPhi) = - g/L * sin(phi);
end pendulum;