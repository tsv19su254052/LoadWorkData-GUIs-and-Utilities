USE AirCraftsDBNew62
GO

-- Делаем схему XML в этой БД
-- Связываем эту схему со столбцом типа типизированный xml, для проверки его типа
SET Transaction Isolation Level SERIALIZABLE
INSERT INTO dbo.AirCraftsTableNew2Xsd(AirLineOwner, AirLineOperator) VALUES ('<owner> 1 </owner> <date> 03.2010 </date>', '<operator> 2 </operator> <date> 03.2010 </date>')
GO
