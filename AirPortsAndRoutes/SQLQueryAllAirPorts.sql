USE AirPortsAndRoutesDBNew62
GO

SET Transaction Isolation Level Read Committed

SELECT	AirPortCodeIATA,
		AirPortCodeICAO,
		AirPortCodeFAA_LID,
		AirPortCodeWMO,
		AirPortName,
		AirPortCity,
		AirPortGeo.ToString() AS GeoCoordinates,
		LogCountViewed,
		LogDateAndTimeViewed,
		LogCountChanged,
		LogDateAndTimeChanged FROM dbo.AirPortsTable
	WHERE LogDateAndTimeViewed IS NOT NULL
		ORDER BY AirPortCodeIATA, AirPortCodeICAO
