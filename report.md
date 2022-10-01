De volgende 3 functies wil ik graag verder uitlichten.

expired update
show profit
charity

expired update.
Met expired update worden alle producten die over datum zijn automatisch naar expired.csv geplaatst. Deze zijn dan niet meer terug te vinden in de instock.csv. Ik heb hier eerst de functie laten kijken of de datum in date.txt wel op de datum van vandaag staat. Hierdoor kan nooit worden geupdate als je bijvoorbeeld 2 dagen vooruit aan het kijken bent. Hierbij heb ik gebruik gemaakt van een extra if statement. Ook gebruik ik Pandas om als de datum goed is de producten van het ene naar het andere csv bestand te verplaatsen.

show profit.
Bij show profit word de winst van een bepaalde tijd weergegeven. Met de gebruikte indeling van de csv bestanden moet voor deze functie gebruik gemaakt worden van 2 verschillende csv bestanden. Ik heb gekozen om over het algemeen gebruik te maken van Dataframes met Pandas. Het probleem was hier dat bought.csv en sold.csv geen gelijk aantal regels hebben en ze niet goed vergeleken konder worden. Ik heb dit opgelost door de dataframes met merge samen te voegen op inkoop ID en daarna de gewenste waarden eruit te halen.

charity.
Bij charity word een PDF bestand met producten die de volgende dag over datum gaan gemaakt.
Een PDF bestand kan makkelijk naar een andere organisatie worden gemaild en niet worden aangepast. Ik  heb hiermee een voorbeeld gemaakt wat er bijvoorbeeld naar een voedselbank kan worden gemaild aan het einde van de dag om de volgende dag te worden opgehaald. Hierbij heb ik gebruik gemaakt van matplotlib om een tabel te maken die via een speciale module naar PDF kan worden omgezet. Dit PDF bestand word automatisch opgeslagen in een gemaakte folder in de superpy folder.