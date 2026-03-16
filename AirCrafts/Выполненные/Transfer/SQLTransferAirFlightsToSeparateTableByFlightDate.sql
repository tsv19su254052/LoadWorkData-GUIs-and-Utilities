--  опируем перелеты из базы авиаперелетов в таблицу базы самолетов

DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
-- ƒаем диапазон дат дл€ копировани€
SET @begindate = '2024-07-01'
SET @enddate = '2024-12-31'
SET @currentdate = @begindate


-- —мотрим вначале
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountBefore
	FROM AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate  -- «агружает tempdb

SET Transaction Isolation Level Serializable
WHILE @currentdate <= @enddate
	--  опируем по одному дню (врем€ выполнени€ без хранимки - 56 ... 58 мин, с хранимкой - 18 суток)
	BEGIN
		DECLARE @rt BIGINT, @ac BIGINT, @acnew BIGINT, @fns VARCHAR(50), @q BIGINT, @fd DATE, @bd DATE, @fails BIGINT
		SET @fails = 0
		DECLARE cursor_flight CURSOR FORWARD_ONLY STATIC FOR
			SELECT	AirRoute,
					AirCraft,
					FlightNumberString,
					QuantityCounted,
					FlightDate,
					BeginDate
				FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
					WHERE FlightDate = @currentdate
						ORDER BY AirCraft, FlightNumberString  -- возможно не требуетс€
		PRINT ' + курсор объ€влен'
		OPEN cursor_flight  -- заполн€ет указанный выше набор
		FETCH NEXT FROM cursor_flight INTO @rt, @ac, @fns, @q, @fd, @bd  -- становимс€ на первую строку и раскладываем ее по переменным

		WHILE @@FETCH_STATUS = 0
			BEGIN
				/*
				SET @acnew = (SELECT TOP 1 AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate.AirCraftUniqueNumber
								FROM	AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
								INNER JOIN AirFlightsDBNew72WorkBase.dbo.AirCraftsTable ON AirCraftsTable.AirCraftRegistration = AirCraftsTableNew2XsdIntermediate.AirCraftRegistration
								INNER JOIN AirFlightsDBNew72WorkBase.dbo.AirFlightsTable ON AirFlightsTable.AirCraft = AirCraftsTable.AirCraftUniqueNumber
									WHERE AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.AirCraft = @ac)
				*/
				SET @acnew = (SELECT AirCraftUniqueNumber 
								FROM AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate 
									WHERE AirCraftRegistration = (SELECT AirCraftRegistration FROM AirFlightsDBNew72WorkBase.dbo.AirCraftsTable 
																	WHERE AirCraftUniqueNumber = @ac))
				IF @acnew IS NULL
					SET @acnew = 3 -- соответствует регистрации 'UNKNOWN' (пока используетс€ только здесь)
				IF @q IS NULL OR @q = 0
					SET @q = 1
				IF @rt IS NOT NULL AND @fns IS NOT NULL
					BEGIN
						INSERT INTO AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate (
							AirRoute,  -- BIGINT NOT NULL PRIMARY KEY - распределенный внешний ключ на маршрут в другой базе
							AirCraft,  -- BIGINT NOT NULL - внешний ключ на регистрацию самолета
							FlightNumberString,  -- VARCHAR(50) NOT NULL
							QuantityCounted,  -- BIGINT
							FlightDate,  -- DATE
							BeginDate,  -- DATE
							LoadDate) VALUES (@rt, @acnew, @fns, @q, @fd, @bd, GETDATE())
						/*
						SET @reg = (SELECT AirCraftRegistration FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftUniqueNumber = @acnew)
						EXECUTE @ReturnValue = AirCraftsDBNew62.dbo.SPFlightInsertOrUpdate @reg, @fns, @rt, @fd, @bd  -- есть отказы из-за взаимоблокировок
						IF @ReturnValue = 0
							SET @fails += 1
						*/
					END
				ELSE 
					SET @fails += 1
				FETCH NEXT FROM cursor_flight
				INTO @rt, @ac, @fns, @q, @fd, @bd
			END
		CLOSE cursor_flight
		DEALLOCATE cursor_flight
		SELECT	@currentdate AS CurrentDate,
				COUNT(*) AS LinesCount,
				@fails AS FailedPoints
			FROM AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate
				WHERE FlightDate = @currentdate  -- «агружает tempdb
		SET @currentdate = DATEADD(DAY, 1, @currentdate)  -- с шагом в 1 день
	END

PRINT ' + перелеты скопированы, отказов = ' +  CONVERT(VARCHAR(100), @fails)

-- ѕровер€ем сколько было
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountFromAirFlights
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- «агружает tempdb
-- и сколько вставилось
SELECT COUNT(*) AS LinesCountAfter
	FROM AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- «агружает tempdb
-- —делал индекс на AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.FlightDate -> в 3 раза быстрее
