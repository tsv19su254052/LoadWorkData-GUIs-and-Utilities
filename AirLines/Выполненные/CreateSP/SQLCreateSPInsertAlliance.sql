:CONNECT terminalserver\mssqlserver15
USE AirLinesDBNew62
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Тарасов СЕРГЕЙ
-- Create date: 30 декабря 2023 года>
-- Description:	<Выбор маршрутов по аэропорту>
-- =============================================
CREATE PROCEDURE dbo.SPInsertAlliance (@AllianceName NVARCHAR(500), @CreationDate DATE, @AllianceDescription NTEXT)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	SET STATISTICS XML ON
	SET Transaction Isolation Level Serializable
	INSERT INTO AirLinesDBNew62.dbo.AlliancesTable (AllianceName, CreationDate, AllianceDescription) VALUES (@AllianceName, @CreationDate, @AllianceDescription)
END
GO
