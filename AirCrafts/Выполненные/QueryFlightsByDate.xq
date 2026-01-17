let $date := "2003-08-01"
for $steps in /FlightsByRoutes/Flight/Route/step
where $steps/@BeginDate=$date
return $steps
