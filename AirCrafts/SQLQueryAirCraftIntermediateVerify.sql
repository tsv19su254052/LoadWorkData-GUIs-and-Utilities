SET Transaction Isolation Level Read Committed

/*
-- ѕровер€ем, как отработал трансфер
SELECT * 
	FROM AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		-- WHERE AirCraftSerialNumber_SN_OLD IS NOT NULL  -- у всех пустые SN
			ORDER BY AirCraftRegistrationOld, AirCraftModel  -- 84691
*/

SELECT COUNT(*) AS CountTotal
	FROM AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate  -- 84691 -> 84781

-- ¬ базе самолетов:
--  - ¬ таблице самолетов "AirCraftsTableNew2Xsd" проверить и вручную привести в пор€док модели самолетов и их описани€ (через прикладное ѕќ по данным с сайтов или через сайт) -> ѕќ«ƒЌ≈≈.
--  - –егистраци€ самолета (англ. Tail Number) с течением времени может последовательно несколько раз переходить от одного самолета к другому.
--  - —амолет за врем€ эксплуатации может несколько раз изменить свой регистрационный номер.
--  - —амолет однозначно определ€етс€ сочетанием его заводских номеров `LN`, `MSN`, `SN`, `CN` в зависимости от фирмы-изготовител€.
-- ¬ базе авиаперелетов:
--  - ¬ базе авиаперелетов хранитс€ только сам факт, что самолет с регистрацией совершил перелет в указанную дату, на остальное можно не обращать внимание.
--  - ѕереписывать регистрацию самолета из одной компании в другую нет смысла.

-- UPDATE AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = NULL

SELECT	AirCraftRegistration,
		FlightsByRoutes,
		BuildDate,
		RetireDate,
		EndDate,
		AirCraftLineNumber_LN_OLD AS LN_OLD,
		AirCraftLineNumber_LN_NEW AS LN_NEW,
		AirCraftLineNumber_MSN AS MSN,
		AirCraftSerialNumber_SN AS SN,
		AirCraftCNumber_CN_OLD AS CN_OLD,
		AirCraftCNumber_CN_NEW AS CN_NEW,
		-- AirCraftModel,
		ManufacturerName,
		ModelName,
		SourceCSVFile,
		AirCraftDescription
	FROM AirCraftsDBValue62.dbo.AirCraftsTableNew2XsdIntermediate
		INNER JOIN AirCraftsDBValue62.dbo.AirCraftModelsTable ON AirCraftsTableNew2XsdIntermediate.AirCraftModel = AirCraftModelsTable.AirCraftModelUniqueNumber
		INNER JOIN AirCraftsDBValue62.dbo.AirCraftManufacturersTable ON AirCraftModelsTable.Manufacturer = AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber
		WHERE ModelName = 'A350'
		-- WHERE FlightsByRoutes IS NOT NULL  -- AND AirCraftRegistration = 'nan'
		-- WHERE FlightsByRoutes.value(('/FlightsByRoutes/Flight/Route/step/@BeginDate'), 'DATE') = '1995-01-01'  -- VARCHAR(50)
			ORDER BY AirCraftRegistration

/*
SELECT	AirCraftRegistrationOld,
		BuildDate,
		RetireDate,
		EndDate,
		AirCraftSerialNumber_SN,
		AirCraftCNumber,
		ManufacturerName,
		ModelName,
		SourceCSVFile
	FROM	AirCraftsDBNew62.dbo.AirCraftManufacturersTable
			INNER JOIN AirCraftsDBNew62.dbo.AirCraftModelsTable ON AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber = AirCraftModelsTable.Manufacturer 
			CROSS JOIN AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		ORDER BY AirCraftRegistrationOld, ModelName  -- вываливает 17107582 строк (умножено на 202 - количество моделей)!!!!

SELECT	AirCraftRegistrationOld,
		BuildDate,
		RetireDate,
		EndDate,
		AirCraftSerialNumber_SN,
		AirCraftCNumber,
		ManufacturerName,
		ModelName,
		SourceCSVFile
	FROM	AirCraftsDBNew62.dbo.AirCraftManufacturersTable
			INNER JOIN AirCraftsDBNew62.dbo.AirCraftModelsTable ON AirCraftManufacturersTable.AirCraftManufacturerUniqueNumber = AirCraftModelsTable.Manufacturer 
			CROSS APPLY AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate
		ORDER BY AirCraftRegistrationOld, ModelName  -- вываливает 17107582 строк (умножено на 202 - количество моделей)!!!!
*/
