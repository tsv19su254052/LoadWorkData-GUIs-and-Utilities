USE AirCraftsDBValue62
GO

DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
-- Даем диапазон дат
SET @begindate = '2012-10-01'
SET @enddate = '2027-01-01'

SET Transaction Isolation Level Read Committed

SELECT COUNT(*) AS LinesCountFromFlightsTable
-- SELECT FlightNumberString, QuantityCounted, FlightDate, BeginDate, LoadDate
	FROM AirFlightsTable
		-- WHERE FlightDate BETWEEN @begindate AND @enddate
		WHERE FlightDate >= @begindate AND FlightDate < @enddate  -- (3394763 -> 3650830 -> 4038628 -> 4609583 -> 4767867 -> 5328661 -> 5739850 -> 5903038 -> 6079669 -> 7412818)

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $steps in /FlightsByRoutes/Flight/Route/step where $steps/@FlightDate >= sql:variable("@begindate") and $steps/@FlightDate < sql:variable("@enddate") return $steps') AS FlightsBetweenDates,
		FlightsByRoutes.value('count(for $steps in /FlightsByRoutes/Flight/Route/step where $steps/@FlightDate >= sql:variable("@begindate") and $steps/@FlightDate < sql:variable("@enddate") return $steps)', 'BIGINT') AS CountOfFlightsBetweenDates,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрацией налазили друг на друга)
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		ManufacturerName,
		ModelName
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@FlightDate >= sql:variable("@begindate") and @FlightDate < sql:variable("@enddate")]') = 1  -- нагружает базу и tempdb
		-- WHERE FlightsByRoutes IS NOT NULL  -- fixme выводит и пустые строки тоже
			ORDER BY AirCraftRegistration  -- 4999

-- время выполнения - 64 минуты (на новой базе под нагрузкой)
