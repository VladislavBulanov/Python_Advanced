SELECT DISTINCT Ships.name AS head_ship
FROM Ships
LEFT JOIN Outcomes ON Ships.name = Outcomes.ship
WHERE Ships.name = Ships.class
OR Ships.class NOT IN (SELECT DISTINCT name FROM Ships);
