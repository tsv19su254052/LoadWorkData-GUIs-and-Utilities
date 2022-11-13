USE AirFlightsDBNew52
GO
/* ќпредел€ем уровень изол€ции транзакций */
SELECT transaction_isolation_level FROM sys.dm_exec_sessions WHERE session_id = @@spid
SELECT	CASE	transaction_isolation_level 
		WHEN 0 THEN 'Unspecified' 
		WHEN 1 THEN 'ReadUncomitted' 
		WHEN 2 THEN 'ReadComitted' 
		WHEN 3 THEN 'Repeatable' 
		WHEN 4 THEN 'Serializable' 
		WHEN 5 THEN 'Snapshot'
		END	AS TIL
FROM	sys.dm_exec_sessions
WHERE	session_id = @@SPID