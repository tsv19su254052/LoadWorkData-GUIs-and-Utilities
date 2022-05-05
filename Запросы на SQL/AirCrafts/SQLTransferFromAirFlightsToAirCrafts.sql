USE [AirCraftsDBNew62]
GO

SET Transaction Isolation Level SERIALIZABLE
INSERT INTO AirCraftManufacturersTable ([Name], ManufacturerDescription)
SELECT [Name], ManufacturerDescription FROM AirFlightsDBNew62.dbo.AirCraftManufacturersTable
GO

SET Transaction Isolation Level SERIALIZABLE
INSERT INTO AirCraftModelsTable (Manufacturer, ModelName, CodeIATA, CodeICAO, ModelDescription, ModelImage)
SELECT Manufacturer, ModelName, CodeIATA, CodeICAO, ModelDescription, ModelImage FROM AirFlightsDBNew62.dbo.AirCraftModelsTable
GO
