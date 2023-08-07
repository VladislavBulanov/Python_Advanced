SELECT DISTINCT Battles.name
FROM Ships
JOIN Classes ON Ships.class = Classes.class
JOIN Outcomes ON Ships.name = Outcomes.ship
JOIN Battles ON Outcomes.battle = Battles.name
WHERE Classes.class = 'Kongo';
