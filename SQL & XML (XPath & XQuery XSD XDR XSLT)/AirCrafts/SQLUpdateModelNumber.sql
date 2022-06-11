USE AirFlightsDBNew5
GO

SET Transaction isolation Level Repeatable Read
BEGIN TRANSACTION
    UPDATE dbo.AirCraftsTable SET AirCraftModel = 186 WHERE (AirCraftRegistration = 'nan') AND (AirCraftModel = 123)
COMMIT TRANSACTION