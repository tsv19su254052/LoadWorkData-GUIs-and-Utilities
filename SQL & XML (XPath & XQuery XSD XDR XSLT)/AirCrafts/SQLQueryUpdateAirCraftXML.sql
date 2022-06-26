USE AirCraftsDBNew62
GO

-- Связать эту схему со столбцом типа типизированный xml для проверки его подлинности - СДЕЛАЛ
-- todo читать содержимое исходных файлов *.xml
SET Transaction Isolation Level SERIALIZABLE
UPDATE dbo.AirCraftsTableNew2Xsd SET AirCraftRegistration =
'<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<!-- standalone - Автономный документ -->
<CustReg>
	<step>
		<reg> N68160 </reg>
		<date> 10.2001 </date>
	</step>
	<step>
		<reg> VP-BAL </reg>
		<date> 07.2014 </date>
	</step>
</CustReg>',
					AirLineOwner =
'<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<CustOwn>
	<step>
		<owner> 2320 </owner>
		<date> 10.2001 </date>
	</step>
	<!--Continental AirLines-->
	<step>
		<owner> 6543 </owner>
		<date> 10.2010 </date>
	</step>
	<!--United AirLines-->
	<step>
		<owner> 6609 </owner>
		<date> 07.2014 </date>
	</step>
	<!--UTair Aviation-->
</CustOwn>',
					AirLineOperator =
'<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<CustOp>
	<step>
		<operator> 2320 </operator>
		<date> 10.2001 </date>
	</step>
	<!--Continental AirLines-->
	<step>
		<operator> 6543 </operator>
		<date> 10.2010 </date>
	</step>
	<!--United AirLines-->
	<step>
		<operator> 6609 </operator>
		<date> 07.2014 </date>
	</step>
	<!--UTair Aviation-->
</CustOp>',
					AirCraftLineNumber_LN = '851',
					AirCraftLineNumber_MSN = '30439'
	WHERE AirCraftUniqueNumber = 3
