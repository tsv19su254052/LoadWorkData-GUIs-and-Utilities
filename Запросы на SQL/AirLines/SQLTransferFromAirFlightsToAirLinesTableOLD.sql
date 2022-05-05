USE AirLinesDBNew62
GO

SET Transaction Isolation Level SERIALIZABLE
INSERT INTO AirLinesTableOLD (AirLine_ID, AirLineName, AirLineAlias, AirLineCodeIATA, AirLineCodeICAO, AirLineCallSighn, AirLineCity, AirLineCountry, AirLineStatus, CreationDate, AirLineDescription, Aliance)
SELECT AirLine_ID, AirLineName, AirLineAlias, AirLineCodeIATA, AirLineCodeICAO, AirLineCallSighn, AirLineCity, AirLineCountry, AirLineStatus, CreationDate, AirLineDescription, Aliance
  FROM AirFlightsDBNew52.dbo.AirLinesTable
GO
