USE AirFlightsDBNew62Test3
GO

DECLARE @faildate DATE
SET @faildate = '2022-10-01'  -- 

SELECT * 
  FROM dbo.AirFlightsTable
  WHERE BeginDate = @faildate

DELETE FROM dbo.AirFlightsTable WHERE BeginDate = @faildate

SELECT * 
  FROM dbo.AirFlightsTable
  WHERE BeginDate = @faildate
GO
