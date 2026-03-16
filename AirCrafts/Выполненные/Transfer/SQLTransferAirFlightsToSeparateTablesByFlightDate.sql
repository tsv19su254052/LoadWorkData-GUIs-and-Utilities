--  опируем перелеты из базы авиаперелетов в таблицу базы самолетов
DECLARE @begindate DATE, @enddate DATE, @currentdate DATE, 
		@rt BIGINT, @ac BIGINT, @acnew BIGINT, 
		@fns VARCHAR(50), @reg VARCHAR(50),
		@q BIGINT, @fd DATE, @bd DATE, 
		@inserted BIGINT, @added BIGINT, @padded BIGINT, @fails BIGINT, 
		@useSP TINYINT,  -- 0 - таблица -> таблица + хранимка, 1 - таблица -> таблица, 2 - таблица -> хранимка (врем€ выполнени€ без хранимки - 56 ... 58 мин, с хранимкой - 18 суток)
		@counter BIGINT, @RetryCount INT, @ReturnValue INT
-- ƒаем диапазон дат дл€ копировани€
SET @begindate = '2026-07-01'
SET @enddate = '2026-07-31'
SET @currentdate = @begindate

-- ѕровер€ем сколько надо вставить
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountFromAirFlights
	FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- «агружает tempdb

DECLARE cursor_flight CURSOR FORWARD_ONLY STATIC FOR  -- статический непрокручиваемый (более быстрый)
	SELECT	AirRoute,
			AirCraft,
			FlightNumberString,
			QuantityCounted,
			FlightDate,
			BeginDate
		FROM AirFlightsDBNew72WorkBase.dbo.AirFlightsTable
			WHERE FlightDate = @currentdate
				ORDER BY AirCraft, FlightNumberString
SET @useSP = 1  -- пока хранимую процедуру не используем до уточнени€ дополнительных сведений

SET Transaction Isolation Level Serializable
WHILE @currentdate <= @enddate
	BEGIN
		SET @inserted = 0
		SET @added = 0
		SET @padded = 0
		SET @fails = 0
		OPEN cursor_flight  -- заполн€ет указанный выше набор в tempdb (как надстройка над временной таблицей)
		FETCH NEXT FROM cursor_flight INTO @rt, @ac, @fns, @q, @fd, @bd  -- становимс€ на первую строку и раскладываем ее по переменным
		WHILE @@FETCH_STATUS = 0
			BEGIN
				IF @q IS NULL OR @q = 0
					SET @q = 1
				IF @rt IS NOT NULL AND @fns IS NOT NULL
					BEGIN
						IF @useSP = 0 OR @useSP = 1
							BEGIN
								SET @acnew = (SELECT AirCraftUniqueNumber 
												FROM AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate 
													WHERE AirCraftRegistration = (SELECT AirCraftRegistration FROM AirFlightsDBNew72WorkBase.dbo.AirCraftsTable 
																					WHERE AirCraftUniqueNumber = @ac))
								IF @acnew IS NULL
									SET @acnew = 3 -- первичный ключ регистрации 'UNKNOWN' (пока используетс€ только здесь)
								INSERT INTO AirCraftsDBValue62.dbo.AirFlightsTable (
									AirRoute,  -- BIGINT NOT NULL PRIMARY KEY - распределенный внешний ключ на маршрут в другой базе
									AirCraft,  -- BIGINT NOT NULL - внешний ключ на регистрацию самолета
									FlightNumberString,  -- VARCHAR(50) NOT NULL
									QuantityCounted,  -- BIGINT
									FlightDate,  -- DATE
									BeginDate,  -- DATE
									LoadDate) VALUES (@rt, @acnew, @fns, @q, @fd, @bd, GETDATE())
							END
						IF @useSP = 0 OR @useSP = 2
							BEGIN
								SET @reg = (SELECT AirCraftRegistration FROM AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftUniqueNumber = @ac)
								-- ”читываем QuantityCounted
								SET @counter = @q
								WHILE @counter >= 1
									BEGIN
										SET @RetryCount = 750  -- число попыток
										-- ÷икл попыток
										WHILE @RetryCount >= 0
											BEGIN
												EXECUTE @ReturnValue = AirCraftsDBValue62.dbo.SPFlightInsertOrUpdate @reg, @fns, @rt, @fd, @bd
												IF @ReturnValue = 0
													SET @fails += 1  -- перезапрос
												IF @ReturnValue = 3
													BEGIN
														SET @inserted += 1
														BREAK
													END
												IF @ReturnValue = 1
													BEGIN
														SET @added += 1
														BREAK
													END
												IF @ReturnValue = 2
													BEGIN
														SET @padded += 1
														BREAK
													END
												SET @RetryCount -= 1
											END
										SET @counter -= 1
									END
							END
					END
				ELSE 
					SET @fails += 1
				FETCH NEXT FROM cursor_flight INTO @rt, @ac, @fns, @q, @fd, @bd  -- становимс€ на следующую строку и раскладываем ее по переменным
			END
		CLOSE cursor_flight
		SELECT	@currentdate AS CurrentDate,
				COUNT(*) AS LinesCount,
				@inserted AS LinesInserted,
				@added AS LinesAdded,
				@padded AS LinesPadded,
				@fails AS FailedPoints
			FROM AirCraftsDBValue62.dbo.AirFlightsTable
				WHERE FlightDate = @currentdate  -- «агружает tempdb
		SET @currentdate = DATEADD(DAY, 1, @currentdate)  -- становимс€ на следующий день
	END
DEALLOCATE cursor_flight
-- PRINT ' + перелеты скопированы, отказов = ' +  CONVERT(VARCHAR(100), @fails)

-- ѕровер€ем сколько вставилось
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountAfter
	FROM AirCraftsDBValue62.dbo.AirFlightsTable
		WHERE FlightDate BETWEEN @begindate AND @enddate  -- «агружает tempdb
-- —делал индекс на AirFlightsDBNew72WorkBase.dbo.AirFlightsTable.FlightDate -> в 3 раза быстрее
