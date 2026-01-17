-- :CONNECT terminalserver\mssqlserver15
-- SET STATISTICS XML ON
SET Transaction Isolation Level REPEATABLE READ

INSERT INTO AirLinesDBNew62.dbo.AlliancesTable (AllianceName, CreationDate, AllianceDescription) VALUES ('KLM-NorthWest', '1997-01-01', '1997-2001')
GO