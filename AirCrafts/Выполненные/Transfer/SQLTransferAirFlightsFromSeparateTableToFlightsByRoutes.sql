-- ¬ базе самолетов копируем перелеты из таблицы перелетов в €чейки FlightsByRoutes таблицы регистраций
-- fixme SSMS сильно подвисала и слетела на 125 строке
DECLARE @begindate DATE, @enddate DATE, @currentdate DATE
SET @begindate = '2002-05-01'
SET @enddate = '2002-12-31'
SET NOCOUNT ON  -- ѕробуем убрать сообщени€ о затронутых строках -> fixme SSMS сделала 122 строки и слетела

SET Transaction Isolation Level Repeatable Read
SET @currentdate = @begindate
WHILE @currentdate <= @enddate
	BEGIN
		DECLARE @rt BIGINT, @ac BIGINT, @reg VARCHAR(50), @fns VARCHAR(50), @q BIGINT, @fd DATE, @bd DATE, @inserted BIGINT, @added BIGINT, @padded BIGINT, @fails BIGINT
		SET @inserted = 0
		SET @added = 0
		SET @padded = 0
		SET @fails = 0
		DECLARE cursor_flightByRoute CURSOR FORWARD_ONLY STATIC FOR  -- статический непрокручиваемый (более быстрый)
			SELECT	AirRoute,
					AirCraft,
					FlightNumberString,
					QuantityCounted,
					FlightDate,
					BeginDate
				FROM AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate
					WHERE FlightDate = @currentdate
						ORDER BY AirCraft, FlightNumberString
		PRINT ' + курсор объ€влен'
		-- «аполн€ем указанный выше набор в tempdb (как надстройка над временной таблицей)
		OPEN cursor_flightByRoute
		-- —тановимс€ на первую строку в наборе и присваиваем ее переменным
		FETCH NEXT FROM cursor_flightByRoute INTO @rt, @ac, @fns, @q, @fd, @bd  
		WHILE @@FETCH_STATUS = 0
			-- ƒалее сдвигаемс€ по одной строке в цикле
			BEGIN
				SET @reg = (SELECT AirCraftRegistration FROM AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftUniqueNumber = @ac)
				-- ”читываем QuantityCounted
				DECLARE @counter BIGINT
				SET @counter = @q
				WHILE @counter >= 1
					BEGIN
						DECLARE @RetryCount INT 
						SET @RetryCount = 750  -- число попыток
						-- ÷икл попыток
						WHILE @RetryCount >= 0
							BEGIN
								DECLARE @ReturnValue INT
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
				FETCH NEXT FROM cursor_flightByRoute
				INTO @rt, @ac, @fns, @q, @fd, @bd
			END
		CLOSE cursor_flightByRoute
		DEALLOCATE cursor_flightByRoute
		SELECT	@currentdate AS CurrentDate,
				COUNT(*) AS LinesCount,
				@inserted AS LinesInserted,
				@added AS LinesAdded,
				@padded AS LinesPadded,
				@fails AS FailedPoints
			FROM AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate
				WHERE FlightDate = @currentdate  -- загружает tempdb
		SET @currentdate = DATEADD(DAY, 1, @currentdate)  -- с шагом в 1 день
	END
-- —мотрим »тоги
SET Transaction Isolation Level Read Committed
SELECT COUNT(*) AS LinesCountTotal
	FROM AirCraftsDBValue62.dbo.AirFlightsTableIntermediateByFlightDate  -- загружает tempdb
SET NOCOUNT OFF
