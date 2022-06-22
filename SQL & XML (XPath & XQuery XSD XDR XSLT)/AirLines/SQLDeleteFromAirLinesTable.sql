USE AirLinesDBNew62
GO 

SET Transaction Isolation Level Serializable
DECLARE @iata NVARCHAR(50), @icao NVARCHAR(50)
SET @iata = 'ZW'
SET @icao = 'AWI'
IF @iata IS NULL
	BEGIN
		SELECT * 
		  FROM dbo.AirLinesTable
		  WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = @icao
	END
ELSE
	BEGIN
		IF @icao IS NULL
			BEGIN
				SELECT * 
				  FROM dbo.AirLinesTable
				  WHERE AirLineCodeIATA = @iata AND AirLineCodeICAO IS NULL
			END
		ELSE
			BEGIN
				SELECT * 
				  FROM dbo.AirLinesTable
				  WHERE AirLineCodeIATA = @iata AND AirLineCodeICAO = @icao
			END
	END

DELETE FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = 30608
GO