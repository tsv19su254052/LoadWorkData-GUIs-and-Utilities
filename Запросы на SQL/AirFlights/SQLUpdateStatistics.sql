USE AirFlightsDBNew62Test
GO
-- Обновление статистики с помощью полной проверки
UPDATE STATISTICS dbo.AirFlightsTable
	WITH FULLSCAN

GO
-- Время выполнения 30 минут 12 секунд