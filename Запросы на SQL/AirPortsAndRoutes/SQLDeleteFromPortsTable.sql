USE AirFlightsDBNew52
GO

SET Transaction Isolation Level Serializable
DELETE FROM dbo.AirPortsTable WHERE AirPortUniqueNumber = 100
