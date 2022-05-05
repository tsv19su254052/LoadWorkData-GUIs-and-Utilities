USE AirFlightsDBNew42Test
GO

--  Число строк в таблице 
SET Transaction Isolation Level Serializable
-- SELECT COUNT(*) FROM dbo.AirFlightsTable -- INT или BIGINT динамическое преобразование типа
-- SELECT COUNT_BIG(*) FROM dbo.AirFlightsTable  -- BIGINT с явным преобразованием типа дольше

SELECT COUNT(*) AS COUNT FROM dbo.AirPortsTable -- INT или BIGINT динамическое преобразование типа
SELECT COUNT_BIG(*) FROM dbo.AirPortsTable  -- BIGINT с явным преобразованием типа дольше
