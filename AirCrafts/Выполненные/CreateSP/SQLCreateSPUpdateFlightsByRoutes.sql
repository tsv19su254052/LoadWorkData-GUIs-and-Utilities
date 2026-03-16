USE [AirCraftsDBNew62]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Тарасов СЕРГЕЙ
-- Create date:	01 мая 2024 года
-- Description:	Вставка или Обновление авиаперелетов самолета внутри БД самолетов
-- =============================================
CREATE PROCEDURE [dbo].[SPUpdateFlightsByRoutes] (@Reg NVARCHAR(50), @FNS NVARCHAR(100), @Route BIGINT, @FD DATE, @BD DATE)
AS
BEGIN
	-- Тело процедуры
	SET XACT_ABORT ON -- закрываем открытые безхозные транзакции, исходя из того, что одновременно пусть будет открыта только одна транзакция
	SET NOCOUNT ON; -- снимаем ограничение "row(s) affected", SET NOCOUNT ON added to prevent extra result sets from
	BEGIN TRY
		-- Первичный ключ уникален, но присваивается автоинкрементом в разных сессиях и поэтому возможны разрывы в сквозной нумерации
		-- Каскадные правила на UPDATE и DELETE 
		DECLARE @TransactionName VARCHAR(32)
		SET @TransactionName = CONCAT('Transaction_SelectCountOf_', @Route)  -- используются <= 32 символов
		SET Transaction Isolation Level SERIALIZABLE
		BEGIN TRANSACTION @TransactionName WITH MARK  -- пометка транзакции (работает с SQL Server 2008-го)
		--  Вставить WITH UPDLOCK
		IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]') 
			FROM  AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
			BEGIN
				PRINT 'Такой FlightNumberString есть'
				IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]') 
					FROM  AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
					BEGIN
						PRINT 'Такой маршрут есть'
						IF (SELECT FlightsByRoutes.exist('/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")]/step[@FlightDate=sql:variable("@FD")]') 
							FROM  AirCraftsDBNew62.dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = @Reg) = 1
								PRINT 'Такой авиперелет есть'
						ELSE
							BEGIN
								PRINT 'Вставляем авиперелет = ' + CONVERT(VARCHAR(100), @FD)
								-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <step FlightDate=sql:variable("@FD") BeginDate=sql:variable("@BD")> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
							END
					END
				ELSE
					BEGIN
						PRINT 'Вставляем маршрут = ' + CONVERT(VARCHAR(100), @Route)  -- UPDATE 2 раза подряд -> Вероятно будет ошибка
						-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <Route RouteFK=sql:variable("@Route") BeginDate=sql:variable("@BD")> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
						PRINT 'Вставляем авиперелет = ' + CONVERT(VARCHAR(100), @FD)
						-- UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes.modify('insert <step FlightDate=sql:variable("@FD") BeginDate=sql:variable("@BD")> into (/FlightsByRoutes/Flight[@FlightNumberString=sql:variable("@FNS")]/Route[@RouteFK=sql:variable("@Route")])[1]') WHERE AirCraftRegistration = @Reg
					END
			END
		ELSE
			BEGIN
				PRINT 'Вставляем FlightNumberString = ' + CONVERT(VARCHAR(100), @FNS)
				PRINT 'Вставляем маршрут = ' + CONVERT(VARCHAR(100), @Route)
				PRINT 'Вставляем авиперелет = ' + CONVERT(VARCHAR(100), @FD)
			END
		COMMIT TRANSACTION
	END TRY

	-- Обработка исключения
	BEGIN CATCH
		IF @@trancount > 0 ROLLBACK TRANSACTION  -- это откат всей процедуры, не "RowInsertionWithParam"
		DECLARE @msg NVARCHAR(2048) = error_message() -- текст ошибки
		RAISERROR (@msg, 16, 1)
		RETURN 55555 -- просто страховка для SQL Server 2005  и более ранних (не использовать в триггерах)
	END CATCH

	PRINT @TransactionName
	-- Выключаем обратно
	SET XACT_ABORT OFF
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT OFF
END
GO
