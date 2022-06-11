USE AirFlightsDBNew62
GO
-- Подымаем очередь на таблице
CREATE QUEUE dbo.AirFlightsQueue
GO
-- Подымаем службу
CREATE SERVICE AirFlightsService ON QUEUE dbo.AirFlightsQueue
GO