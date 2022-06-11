USE AirPortsAndRoutesDBNew62
GO
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT AirPortName, AirPortCodeIATA,  COUNT(*) AS Duplicates
  FROM [dbo].[AirPortsTable]
  GROUP BY AirPortName, AirPortCodeIATA
  HAVING COUNT(*) > 1 -- 2 шт. с дубликатами - оставил только первые, остальные удалил