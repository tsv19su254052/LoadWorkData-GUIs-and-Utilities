USE AirCraftsDBValue62
GO

-- Время выполнения - 

IF EXISTS (SELECT name FROM sys.indexes
            WHERE name = N'SecondaryXmlIndex_PropertiesOfFlights')
    DROP INDEX SecondaryXmlIndex_PropertiesOfFlights
        ON dbo.AirCraftsTableNew2XsdIntermediate
GO  

CREATE XML INDEX SecondaryXmlIndex_PropertiesOfFlights
    ON AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate (FlightsByRoutes)
    USING XML INDEX PrimaryXMLIndex FOR PROPERTY 
GO