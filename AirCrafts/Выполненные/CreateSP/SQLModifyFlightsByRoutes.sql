USE AirCraftsDBNew62
GO

SET STATISTICS XML ON
SET STATISTICS IO ON
SET STATISTICS TIME ON
SET STATISTICS PROFILE ON

DECLARE @Reg VARCHAR(50), @FNS VARCHAR(100), @Route BIGINT, @FD DATE, @BD DATE, @Quantity BIGINT, @Result INT, @ReturnValue INT, @xml XML
SET @Reg = 'N000AA'  -- не менять
SET @FNS = '9E5028Test'  -- было 9E5028
SET @Route = 87  -- было 87
SET @FD = '2023-08-21'  -- было 2023-09-21
SET @BD = '2023-08-01'  -- было 2023-09-01
SET @Quantity = 1

SET Transaction Isolation Level Repeatable Read
BEGIN TRANSACTION
IF (SELECT FlightsByRoutes FROM AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = @Reg) IS NULL
	BEGIN
		-- Если XML-ное поле еще пустое
		PRINT 'Записываем с нуля новый рейс ' + CONVERT(VARCHAR(100), @FNS) + ', маршрут ' + CONVERT(VARCHAR(100), @Route) + ' и авиаперелет ' + CONVERT(VARCHAR(100), @FD)
		SET @xml = '<FlightsByRoutes>
						<Flight FlightNumberString="' + CONVERT(VARCHAR(5000), @FNS) + '">
							<Route RouteFK="' + CONVERT(VARCHAR(5000), @Route) + '">
								<step FlightDate="' + CONVERT(VARCHAR(5000), @FD) + '" BeginDate="' + CONVERT(VARCHAR(5000), @BD) + '">
									1
								</step>
							</Route>
						</Flight>
					</FlightsByRoutes>'
		-- PRINT ' ++ xml для новой записи = ' + CONVERT(VARCHAR(5000), @xml)
		UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = @xml WHERE AirCraftRegistration = @Reg
		SET @Result = 3
	END
ELSE
	BEGIN
		IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]') 
			FROM  AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
			BEGIN
				IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]') 
					FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
					BEGIN
						IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]') 
							FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
								BEGIN
									PRINT 'В рейсе ' + CONVERT(VARCHAR(100), @FNS) + ' и в маршруте ' + CONVERT(VARCHAR(100), @Route) + ' плюсуем авиаперелет ' + CONVERT(VARCHAR(100), @FD)
									SET @Quantity = (SELECT FlightsByRoutes.value(('(/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")])[1]'), 'BIGINT') 
														FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg)
									SET @Quantity += 1
									-- с условием WHERE не работает, см. статью https://www.mssqltips.com/sqlservertip/2738/examples-of-using-xquery-to-update-xml-data-in-sql-server/ раздел "Modify() Limitations Issue # 1"
									-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('replace value of (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]/text()) with sql:variable("@Quantity") ')  WHERE AirCraftRegistration = @Reg
									-- Здесь читается все XML-ное поле, но только в случае плюсования
									SET @xml = (SELECT FlightsByRoutes FROM AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg)
									SET @xml.modify('replace value of (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]/text())[1] with sql:variable("@Quantity") ')
									UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = @xml WHERE AirCraftRegistration = @Reg
									PRINT ' - авиаперелетов = ' + CONVERT(VARCHAR(100), @Quantity)
									SET @Result = 2
								END
						ELSE
							BEGIN
								PRINT 'Дописываем в рейс ' + CONVERT(VARCHAR(100), @FNS) + ' и в маршрут ' + CONVERT(VARCHAR(100), @Route) + ' новый авиаперелет ' + CONVERT(VARCHAR(100), @FD)
								UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <step FlightDate="{sql:variable("@FD")}" BeginDate="{sql:variable("@BD")}">1</step> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
								SET @Result = 1
							END
					END
				ELSE
					BEGIN
						PRINT 'Дописываем в рейс ' + CONVERT(VARCHAR(100), @FNS) + ' новый маршрут ' + CONVERT(VARCHAR(100), @Route) + ' и авиаперелет ' + CONVERT(VARCHAR(100), @FD)
						UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <Route RouteFK="{sql:variable("@Route")}"><step FlightDate="{sql:variable("@FD")}" BeginDate="{sql:variable("@BD")}">1</step></Route> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")])[1]') WHERE AirCraftRegistration = @Reg
						SET @Result = 1
					END
			END
		ELSE
			BEGIN
				PRINT 'Дописываем новый рейс ' + CONVERT(VARCHAR(100), @FNS) + ', маршрут ' + CONVERT(VARCHAR(100), @Route) + ' и авиаперелет ' + CONVERT(VARCHAR(100), @FD)
				UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <Flight FlightNumberString="{sql:variable("@FNS")}"><Route RouteFK="{sql:variable("@Route")}"><step FlightDate="{sql:variable("@FD")}" BeginDate="{sql:variable("@BD")}">1</step></Route></Flight> into (/FlightsByRoutes)[1]') WHERE AirCraftRegistration = @Reg
				SET @Result = 1
			END
	END
COMMIT TRANSACTION
PRINT ' - результат запроса = ' + CONVERT(VARCHAR(100), @Result) + ' (Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали, 3 - первая запись в еще пустую ячейку)'

PRINT 'То же с помощью хранимой процедуры'
EXECUTE @ReturnValue = dbo.SPFlightInsertOrUpdate @Reg, @FNS, @Route, @FD, @BD
PRINT ' - результат процедуры = ' + CONVERT(VARCHAR(100), @ReturnValue) + ' (Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали, 3 - первая запись в еще пустую ячейку)'

PRINT 'Смотрим'
SELECT	AirCraftRegistration,
		FlightsByRoutes.query('for $flights in /FlightsByRoutes/Flight where $flights/Route/step/@BeginDate = sql:variable("@BD") return $flights') AS FlightsAfter
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@BD")]') = 1 AND AirCraftRegistration = @Reg
		-- WHERE AirCraftRegistration = @Reg
			ORDER BY AirCraftRegistration

-- fixme возможны варианты (ячейка была пустая), XSD-схема футболит -> обнулить отдельно
UPDATE AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('delete /FlightsByRoutes/Flight[@FlightNumberString = sql:variable("@FNS")]') WHERE AirCraftRegistration = @Reg
PRINT 'Вернули обратно за ' + CONVERT(VARCHAR(100), @FD)

PRINT 'Проверяем'
SELECT	AirCraftRegistration,
		FlightsByRoutes.query('for $flights in /FlightsByRoutes/Flight where $flights/Route/step/@BeginDate = sql:variable("@BD") return $flights') AS FlightsBefore
	FROM AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE FlightsByRoutes.exist('/FlightsByRoutes/Flight/Route/step[@BeginDate = sql:variable("@BD")]') = 1 AND AirCraftRegistration = @Reg
		-- WHERE AirCraftRegistration = @Reg
			ORDER BY AirCraftRegistration
