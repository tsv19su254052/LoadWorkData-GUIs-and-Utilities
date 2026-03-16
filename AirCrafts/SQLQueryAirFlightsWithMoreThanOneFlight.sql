USE AirCraftsDBValue62
GO

SET Transaction Isolation Level Read Committed
SELECT	AirCraftRegistration,
		FlightsByRoutes,
		FlightsByRoutes.value('count(for $steps in /FlightsByRoutes/Flight/Route/step where $steps >= 2 return $steps)', 'BIGINT') AS CountOfFlightsWithMoreThanOneFlight,
		AirCraftLineNumber_LN_OLD AS LN_OLD,  -- Столбцы отсюда и ниже возможно недостоверны (данные с разных самолетов с одной регистрвцией налазили друг на друга)
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
		WHERE FlightsByRoutes.exist('for $steps in /FlightsByRoutes/Flight/Route/step where $steps >= 2 return $steps') = 1  -- нагружает базу и tempdb
		-- WHERE FlightsByRoutes IS NOT NULL  -- fixme выводит и пустые строки тоже
			ORDER BY AirCraftRegistration  -- 3674

-- время выполнения -  14 ... 22 минуты (на новой базе под нагрузкой)
