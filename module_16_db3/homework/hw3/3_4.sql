SELECT Ships.name
FROM Ships
WHERE Ships.name = Ships.class
UNION
SELECT Outcomes.ship
FROM Outcomes
JOIN Classes ON Classes.class = Outcomes.ship;
