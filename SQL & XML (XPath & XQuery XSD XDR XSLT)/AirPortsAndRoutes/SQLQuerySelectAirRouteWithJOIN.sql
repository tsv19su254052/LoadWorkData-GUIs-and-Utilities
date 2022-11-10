/*  Маршруты аэропорта  */
SET Transaction Isolation Level Repeatable Read
DECLARE @AirPortIATA nchar(10)
SET @AirPortIATA = 'XCR'  -- Код IATA исходного аэропорта - 300
SELECT AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortName AS DEPARTURE,
	   AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCity AS DEPARTURE_CITY,
	   AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCountry AS DEPARTURE_COUNTRY,
	   AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA AS Departure_IATA,
	   AirPortsTable_1.AirPortName AS ARRIVAL,
	   AirPortsTable_1.AirPortCity AS ARRIVAL_CITY,
	   AirPortsTable_1.AirPortCountry AS ARRIVAL_COUNTRY,
	   AirPortsTable_1.AirPortCodeIATA AS Arrival_IATA
FROM AirPortsAndRoutesDBNew62.dbo.AirRoutesTable INNER JOIN
     AirPortsAndRoutesDBNew62.dbo.AirPortsTable ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortDeparture = AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
     AirPortsAndRoutesDBNew62.dbo.AirPortsTable AS AirPortsTable_1 ON AirPortsAndRoutesDBNew62.dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
WHERE (AirPortsAndRoutesDBNew62.dbo.AirPortsTable.AirPortCodeIATA = @AirPortIATA) OR (AirPortsTable_1.AirPortCodeIATA = @AirPortIATA)
ORDER BY DEPARTURE_CITY, ARRIVAL_CITY
-- XSD, TPH - Tonopah
-- пусто (KXTA) - Homey (Area 51)
-- HMN - Holloman Air Force Base
-- LSV - Nellis Air Force Base
-- NKX - Marine Corps Air Station Miramar
-- DMA
-- VCV
-- ABQ - Kirtland Air Force Base
-- SUU
-- EDW
-- ALM - Alamogordo
