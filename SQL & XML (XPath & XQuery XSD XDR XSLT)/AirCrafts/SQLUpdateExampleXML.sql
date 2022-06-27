USE AirCraftsDBNew62
  GO

DECLARE @registration XML, @owner XML, @operator XML  -- @registration XML(DOCUMENT SchemaCollection)
/*
SET @registration = '
-- todo читать исходный файл:
-- "file://P:\Programming\Python Scripts\LoadWorkDataAirFlightsDBNew\Запросы на SQL\AirCraftRegistrationXMLSource_VQ-BTQ.xml"

'
SET @owner = '
-- читать исходный файл:
-- "file://P:\Programming\Python Scripts\LoadWorkDataAirFlightsDBNew\Запросы на SQL\AirCraftOwnerXMLSource_VQ-BTQ.xml"
'
SET @operator = '
-- читать исходный файл:
-- "file://P:\Programming\Python Scripts\LoadWorkDataAirFlightsDBNew\Запросы на SQL\AirCraftOperatorXMLSource_VQ-BTQ.xml"
'
*/

DECLARE @MSN VARCHAR(10), @LN VARCHAR(100)
SET @MSN = '30435'
SET @LN = '827'
DECLARE @LN_MSN VARCHAR(200)
SET @LN_MSN = CONCAT(@LN, ' ', @MSN)
SET @registration = (SELECT AirCraftRegistration
						FROM dbo.AirCraftsTableNew2Xsd
						WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN)
-- SELECT @registration[reg]  -- выводит всю ветку "CustReg"
SET @owner = (SELECT AirLineOwner
				FROM dbo.AirCraftsTableNew2Xsd
				WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN)
SET @operator = (SELECT AirLineOperator
					FROM dbo.AirCraftsTableNew2Xsd
					WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN)

SELECT @owner.query('/CustOwn') AS OWNERBEFORE  -- выводит все ветки "step", ругается (несколько корневых элементов)
IF (SELECT @owner.exist('/CustOwn/step[@CraftOwnerFK=6610] ')) = 0  -- выдает "1", если есть такая ветка, выдает "0" - если нет
	BEGIN
		SET @owner.modify('insert <!-- New Aviation 1 --> into (/CustOwn)[1] ')
		SET @owner.modify('insert <step CraftOwnerFK="6610" /> into (/CustOwn)[1] ')
	END
DECLARE @newOwner XML
SET @newOwner = '<BeginDate> 2015-03-01 </BeginDate>'
SET @owner.modify('insert sql:variable("@newOwner") into (/CustOwn/step[@CraftOwnerFK=6610])[1] ')
IF (SELECT @owner.exist('/CustOwn/step[@CraftOwnerFK=6611] ')) = 0
	BEGIN
		SET @owner.modify('insert <!-- New Aviation 2 --> into (/CustOwn)[1] ')
		SET @owner.modify('insert <step CraftOwnerFK="6611" /> into (/CustOwn)[1] ')
	END
SET @newOwner = '<BeginDate> 2015-05-01 </BeginDate>'
SET @owner.modify('insert sql:variable("@newOwner") into (/CustOwn/step[@CraftOwnerFK=6611])[1] ')
SELECT @owner.query('/CustOwn') AS OWNERAFTER  -- выводит всю ветку "CustOwn", все нормально

SELECT @operator.query('/CustOp') AS OPERATORBEFORE
-- SELECT @operator[operator]  -- выводит всю ветку "CustOp"
IF (SELECT @operator.exist('/CustOp/step[@CraftOperatorFK=6612] ')) = 0  -- выдает "1", если есть такой, выдает "0" - если нет
	BEGIN
		SET @operator.modify('insert <!-- New Age 1 --> into (/CustOp)[1] ')
		SET @operator.modify('insert <step CraftOperatorFK="6612" /> into (/CustOp)[1] ')
	END
DECLARE @newOperator XML
SET @newOperator = '<BeginDate> 2015-04-01 </BeginDate>'
SET @operator.modify('insert sql:variable("@newOperator") into (/CustOp/step[@CraftOperatorFK=6612])[1] ')
IF (SELECT @operator.exist('/CustOp/step[@CraftOperatorFK=6613] ')) = 0
	BEGIN
		SET @operator.modify('insert <!-- New Age 2 --> into (/CustOp)[1] ')
		SET @operator.modify('insert <step CraftOperatorFK="6613" /> into (/CustOp)[1] ')
	END
SET @newOperator = '<BeginDate> 2015-06-01 </BeginDate>'
SET @operator.modify('insert sql:variable("@newOperator") into (/CustOp/step[@CraftOperatorFK=6613])[1] ')
SELECT @operator.query('/CustOp') AS OPERATORAFTER  -- выводит всю ветку "CustOwn", все нормально

-- UPDATE dbo.AirCraftsTableNew2Xsd SET AirLineOwner = @owner, AirLineOperator = @operator WHERE AirCraftLineNumber_LN = @LN AND AirCraftLineNumber_MSN = @MSN

SELECT AirLineOwner AS AIRLINEOWNER,
		AirLineOperator.query('//step') AS AIRLINEOPERATOR
  FROM dbo.AirCraftsTableNew2Xsd -- относительный путь до ветки /step
SELECT @owner.value('(/CustOwn/step/@CraftOwnerFK)[4]', 'int') AS CRAFTOWNERFK  -- внешний ключ 4-го владельца
SELECT @owner.value('(/CustOwn/step[@CraftOwnerFK=6610]/BeginDate)[6]', 'date') AS BEGINOWN  -- 6-ая дата владельца с указанным внешним ключем
SELECT @operator.value('(/CustOp/step/BeginDate)[5]', 'date') AS BEGINOPERATE  -- 5-ая дата оператора с указанным внешним ключем
GO
  
DECLARE @reg NVARCHAR(50)
SET @reg = 'N635TW'
SELECT	AirCraftRegistration.query('/CustReg/step/BeginDate') AS REGS,
		AirLineOperator.query('/CustOp/step/BeginDate') AS OPERATOR
  -- SELECT XMLELEMENT  -- SQL/XML установлен
  FROM dbo.AirCraftsTableNew2Xsd
  WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[1]', 'VARCHAR(50)') = @reg

-- Первый вариант (все сразу)
SELECT AirLineName, AirLineAlias, AirLineCodeIATA, AirLineCodeICAO, CreationDate
  FROM AirLinesDBNew62.dbo.AirLinesTable
  WHERE AirLineUniqueNumber = (SELECT AirLineOperator.value('(CustOp/step/@CraftOperatorFK)[1]', 'BIGINT')
								FROM dbo.AirCraftsTableNew2Xsd
								WHERE AirCraftRegistration.value('(CustReg/step/@CraftRegFK)[1]', 'VARCHAR(50)') = @reg)
SELECT AirLineOperator.value('(/CustOp/step/@CraftOperatorFK)[1]', 'BIGINT') AS FK,
	   AirCraftRegistration.value('(/CustReg/step[@CraftRegFK=sql:variable("@reg")]/BeginDate)[1]', 'DATE') AS BEGINDATE
  FROM dbo.AirCraftsTableNew2Xsd
  WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[1]', 'VARCHAR(50)') = @reg

-- Второй вариант (в два хода)
DECLARE @fk BIGINT
SET @fk = (SELECT AirLineOperator.value('(/CustOp/step/@CraftOperatorFK)[1]', 'BIGINT')
			FROM dbo.AirCraftsTableNew2Xsd
			WHERE AirCraftRegistration.value('(/CustReg/step/@CraftRegFK)[1]', 'VARCHAR(50)') = @reg)

SELECT AirLineName, AirLineAlias, AirLineCodeIATA, AirLineCodeICAO, CreationDate
  FROM AirLinesDBNew62.dbo.AirLinesTable
  WHERE AirLineUniqueNumber = @fk
GO
