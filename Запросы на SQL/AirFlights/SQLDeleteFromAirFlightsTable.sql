USE AirFlightsDBNew62
GO
  --  Удаляет все строки в указанной ниже таблице

SET Transaction Isolation Level Serializable
DELETE FROM dbo.AirFlightsTable
-- WHERE FlightDescription LIKE '+++_T_ONTIME_REPORTING_1987_11.csv'
