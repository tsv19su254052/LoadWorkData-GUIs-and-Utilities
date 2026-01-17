USE AirPortsAndRoutesDBNew62
GO

DECLARE @iata NVARCHAR(50)
SET @iata = 'AZN'  --  

SELECT	* 
  FROM dbo.AirPortsTable
	WHERE AirPortCodeIATA = @iata
		ORDER BY AirPortCodeIATA, AirPortCodeICAO

UPDATE dbo.AirPortsTable SET AirPortCodeICAO = 'UZFA' WHERE AirPortUniqueNumber = 602

SELECT	* 
  FROM dbo.AirPortsTable
	WHERE AirPortCodeIATA = @iata
		ORDER BY AirPortCodeIATA, AirPortCodeICAO
