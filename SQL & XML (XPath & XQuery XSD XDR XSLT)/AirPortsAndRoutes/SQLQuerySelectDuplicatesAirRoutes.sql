USE AirPortsAndRoutesDBNew62
GO
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT AirPortDeparture, AirPortArrival,  COUNT(*) AS Duplicates
  FROM AirRoutesTable
  GROUP BY AirPortDeparture, AirPortArrival
  HAVING COUNT(*) > 1 -- маршрутов с дубликатами пока нету