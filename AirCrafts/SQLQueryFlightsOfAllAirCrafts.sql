USE AirCraftsDBValue62
GO

SET Transaction Isolation Level Read Committed

-- 10876 -> 11956 -> 12749 -> 12759 -> 12907 -> 12921 -> 12955 -> 13253

-- Идея такая: 
	-- Разложить XML-ную ячейку с указанной регистрацией во временную таблицу (перед этим удалить из нее предыдущие строки), потом в эту таблицу подставить аэропорты
	-- Вывести авиаперелеты, не найденные в БД авиаперелетов
SELECT	AirCraftRegistration,
		-- Вставить сюда цикл на xQuery (XML с номерами маршрутов -> XML с названиями аэропортов), в который подставляю поля из подзапроса
		FlightsByRoutes,
		FlightsByRoutes.value('count(/FlightsByRoutes/Flight/Route/step)', 'BIGINT') AS CountOfFlights,
		FlightsByRoutes.query('for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes') AS EmptyRoutes,
		FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where empty($routes/step) return $routes)', 'BIGINT') AS CountOfEmptyRoutes,
		-- FlightsByRoutes.value('count(for $routes in /FlightsByRoutes/Flight/Route where $routes='' return $routes)', 'BIGINT') AS CountOfEmptyRoutes,  -- fixme  Незавершенная строковая константа (начало на строке 1)
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
		WHERE FlightsByRoutes IS NOT NULL
			ORDER BY AirCraftRegistration
