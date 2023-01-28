USE AirFlightsDBNew62Test2
GO

DECLARE @City varchar(250), @Reg VARCHAR(50)
SET @Reg = 'N394DL'  -- BOEING 767-324(ER) - 27394 -- 2854
SET @City = 'Denver'  -- 148
/*
SELECT FlightNumberString AS FN,
		(SELECT AirPortName FROM AirPortsAndRoutesDBNew62.dbo.AirPortsTable WHERE AirPortUniqueNumber =
				(SELECT AirPortDeparture FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable WHERE AirRouteUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirRoute)) AS DEPARTURE,
		(SELECT AirPortCity FROM AirPortsAndRoutesDBNew62.dbo.AirPortsTable WHERE AirPortUniqueNumber =
				(SELECT AirPortDeparture FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable WHERE AirRouteUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirRoute)) AS CITY_OUT,
		(SELECT AirPortCodeIATA FROM AirPortsAndRoutesDBNew62.dbo.AirPortsTable WHERE AirPortUniqueNumber =
				(SELECT AirPortDeparture FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable WHERE AirRouteUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirRoute)) AS IATA_OUT,
		(SELECT AirPortName FROM AirPortsAndRoutesDBNew62.dbo.AirPortsTable WHERE AirPortUniqueNumber =
				(SELECT AirPortArrival FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable WHERE AirRouteUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirRoute)) AS ARRIVAL,
		(SELECT AirPortCity FROM AirPortsAndRoutesDBNew62.dbo.AirPortsTable WHERE AirPortUniqueNumber =
				(SELECT AirPortArrival FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable WHERE AirRouteUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirRoute)) AS CITY_IN,
		(SELECT AirPortCodeIATA FROM AirPortsAndRoutesDBNew62.dbo.AirPortsTable WHERE AirPortUniqueNumber =
				(SELECT AirPortArrival FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable WHERE AirRouteUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirRoute)) AS IATA_IN,
		QuantityCounted,
		(SELECT AirCraftRegistration FROM AirFlightsDBNew62.dbo.AirCraftsTable WHERE AirCraftUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirCraft) AS REG,
		(SELECT ModelName FROM AirFlightsDBNew62.dbo.AirCraftModelsTable WHERE AirCraftModelUniqueNumber =
				(SELECT AirCraftModel FROM AirFlightsDBNew62.dbo.AirCraftsTable WHERE AirCraftUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirCraft)) AS Model,
		(SELECT [Name] FROM AirFlightsDBNew62.dbo.AirCraftManufacturersTable WHERE AirCraftManufacturersUniqueNumber =
				(SELECT AirCraftModel FROM AirFlightsDBNew62.dbo.AirCraftsTable WHERE AirCraftUniqueNumber = AirFlightsDBNew62.dbo.AirFlightsTable.AirCraft)) AS Manufacturer
  FROM AirFlightsDBNew62.dbo.AirFlightsTable
  */
SET STATISTICS XML ON
SET Transaction Isolation Level Read Committed

SELECT		AirFlightsDBNew62Test2.dbo.AirFlightsTable.FlightDate AS FLIGHTDATE,
			-- AirFlightsDBNew62.dbo.AirFlightsTable.BeginDate AS BEGINDATE,
			-- AirFlightsDBNew62.dbo.AirFlightsTable.LoadDate AS LOADDATE,
			AirFlightsDBNew62Test2.dbo.AirFlightsTable.FlightNumberString AS FN,
			AirFlightsDBNew62Test2.dbo.AirFlightsTable.QuantityCounted,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName AS DEPARTURE,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity AS CITY_OUT,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA AS IATA_OUT,
			AirPortsTable_1.AirPortName AS ARRIVAL,
			AirPortsTable_1.AirPortCity AS CITY_IN,
			AirPortsTable_1.AirPortCodeIATA AS IATA_IN,
			AirFlightsDBNew62Test2.dbo.AirCraftsTable.SourceCSVFile AS SOURCEFILE
FROM		AirFlightsDBNew62Test2.dbo.AirFlightsTable INNER JOIN
            AirFlightsDBNew62Test2.dbo.AirCraftsTable ON AirFlightsDBNew62Test2.dbo.AirFlightsTable.AirCraft = AirFlightsDBNew62Test2.dbo.AirCraftsTable.AirCraftUniqueNumber INNER JOIN
            AirPortsAndRoutesDBNew62.dbo.AirRoutesTable ON AirFlightsDBNew62Test2.dbo.AirFlightsTable.AirRoute = AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirRouteUniqueNumber INNER JOIN
            AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortDeparture = AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
            AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber  
  WHERE AirFlightsDBNew62Test2.dbo.AirCraftsTable.AirCraftRegistration = @Reg
  -- WHERE AirFlightsDBNew62Test2.dbo.AirCraftsTable.AirCraftRegistration = @Reg AND (AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName = @City OR AirPortsTable_1.AirPortCity = @City)
  -- WHERE AirFlightsDBNew62Test2.dbo.AirCraftsTable.AirCraftRegistration = @Reg AND AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName = @City  -- не работает
  -- (большие самолеты American AirLines, Continental как правило более привязаны к маршруту)
/*	UTair Boeing 767-224(ER):
		VP-BAG UTair Aviation 15.07.2012 Moscow - Dushanbe, Tashkent, Makhachkala - Jeddah, Anadyr		(N76156 Continental Airlines 15.02.2001 -> United Airlines 01.12.2011) 95 строк
		VP-BAI UTair Aviation 02.09.2012 Moscow - Dushanbe, Tashkent ,Bukhara, Anadyr					(N67158 Continental Airlines 30.05.2001 -> United Airlines 01.12.2011) 97 строк
		VP-BAL UTair Aviation 21.07.2014 Moscow - Dushanbe, Tashkent ,Bukhara							(N68160 Continental Airlines 30.10.2001 -> United Airlines 01.12.2011) 157 строк
	New York City 11.09.2001
		N334AA - 11.09.2001 New York City 92(i)+1600 crashed into WTC Northern tower 8:45 am after hyjack ER Boston - Los Angeles flight #11, tt 58350, 11538 l, most died at collapse of tower at 10:29 am, own NEMLC 8.07.87, FUNB r6.01.00 118 строк
		N612UA - 11.09.2001 New York City 65(i)+1000 crashed into WTC Southern tower 9:03 am after hyjack ER Boston - Los Angeles flight #175, tt 66647, 17549 l, most occ. killed when tower collapsed at 09:50 am 179 строк */
  ORDER BY FLIGHTDATE, FN, CITY_OUT, CITY_IN  -- 8281

SELECT		-- AirFlightsDBNew62.dbo.AirFlightsTable.FlightNumberString AS FN,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName AS DEPARTURE,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity AS CITY_OUT,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA AS IATA_OUT,
			AirPortsTable_1.AirPortName AS ARRIVAL,
			AirPortsTable_1.AirPortCity AS CITY_IN,
			AirPortsTable_1.AirPortCodeIATA AS IATA_IN,
			SUM(AirFlightsDBNew62Test2.dbo.AirFlightsTable.QuantityCounted) AS QUANTITY
			-- AirFlightsDBNew62.dbo.AirCraftsTable.SourceCSVFile AS SOURCEFILE
FROM		AirFlightsDBNew62Test2.dbo.AirFlightsTable INNER JOIN
            AirFlightsDBNew62Test2.dbo.AirCraftsTable ON AirFlightsDBNew62Test2.dbo.AirFlightsTable.AirCraft = AirFlightsDBNew62Test2.dbo.AirCraftsTable.AirCraftUniqueNumber INNER JOIN
            AirPortsAndRoutesDBNew62.dbo.AirRoutesTable ON AirFlightsDBNew62Test2.dbo.AirFlightsTable.AirRoute = AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirRouteUniqueNumber INNER JOIN
            AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortDeparture = AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
            AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber  
  WHERE AirFlightsDBNew62Test2.dbo.AirCraftsTable.AirCraftRegistration = @Reg
  GROUP BY --AirFlightsDBNew62.dbo.AirFlightsTable.FlightNumberString,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName,
			-- AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortDeparture,
			-- AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortArrival,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity,
			AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA,
			AirPortsTable_1.AirPortName,
			AirPortsTable_1.AirPortCity,
			AirPortsTable_1.AirPortCodeIATA
  ORDER BY CITY_OUT, CITY_IN  -- 361
GO
