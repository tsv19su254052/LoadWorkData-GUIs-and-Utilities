USE AirCraftsDBValue62
GO

DECLARE @Reg VARCHAR(50)
SET @Reg = 'N637AA'  -- 'CS-TFS'

SET Transaction Isolation Level Read Committed

SELECT * 
  FROM AirCraftsTableNew2Xsd
	WHERE AirCraftRegistration.exist('/CustReg/step[@CraftRegFK=sql:variable("@Reg")]') = 1
