/* -----------------------------------------------------------------------------------------------------------------------------------
VSTS Title (Task Number): VCP - Create Date Related Tables for CDM (637)

Purpose: Creates a single table with Integers incrementing by a unit of 1 per record. 

Development Server: Local SQL Server Instance
Production Server:  Yet to be 

Notes:
   Default schema is dbo. Code to create new schema included if required.

Status: Available for Production

Version				DD/MM/YY				Author				Description
2                 29/12/2017        Andrew Wood       Created view to mimic dimNumbers (even though the table is called Numbers).
1					   22/12/2017			Andrew Wood			Initial Numbers implementation
----------------------------------------------------------------------------------------------------------------------------------- */

GO
SET STATISTICS IO OFF;
GO
SET NOCOUNT ON;
GO
SET ANSI_PADDING ON
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

--IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dbo')
--   DECLARE @i VARCHAR(50) = 'CREATE SCHEMA [dbo]';
--   EXEC (@i);

IF OBJECT_ID('dbo.Numbers') IS NOT NULL DROP TABLE dbo.Numbers;

SET ANSI_PADDING ON
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

   DECLARE @CodeStartTime TIME; SET @CodeStartTime = CAST(SYSDATETIME() AS TIME) ;
   DECLARE @RecordCounter BIGINT;

   SET NOCOUNT ON;


   --https://docs.microsoft.com/en-us/sql/t-sql/data-types/int-bigint-smallint-and-tinyint-transact-sql
   --https://docs.microsoft.com/en-us/sql/t-sql/functions/power-transact-sql

   DECLARE @UpperBound INT = POWER(2,31-1) - 1; --536,870,911
   --I chose to round it down to a consumable number.
   SET @UpperBound =  250000 ;  

   WITH cteN(Number) AS
   (
     SELECT ROW_NUMBER() OVER (ORDER BY s1.[object_id]) - 1
     FROM sys.all_columns AS s1
     CROSS JOIN sys.all_columns AS s2
   )
   SELECT CAST([Number] AS INT) AS [Number]
      INTO dbo.Numbers
   FROM cteN 
   WHERE [Number] <= @UpperBound;
   SET @RecordCounter = @@ROWCOUNT;

   CREATE UNIQUE CLUSTERED INDEX CIX_Numbers ON dbo.Numbers([Number])
   WITH 
   (
     FILLFACTOR = 100,      -- in the event server default has been changed
     DATA_COMPRESSION = ROW -- if Enterprise & table large enough to matter
   );

GO

EXEC sys.sp_addextendedproperty @name=N'Purpose', @value=N'
  The dbo.Numbers table lists each and every number from 0 up to 89378116
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Numbers';
GO

EXEC sys.sp_addextendedproperty @name=N'Dependencies', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Numbers';
GO

EXEC sys.sp_addextendedproperty @name=N'RequiredBy', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Numbers';
GO

EXEC sys.sp_addextendedproperty @name=N'Example', @value=N'https://www.mssqltips.com/sqlservertip/4176/the-sql-server-numbers-table-explained--part-1/
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Numbers';
GO

EXEC sys.sp_addextendedproperty @name=N'Revisions', @value=N'
Version				DD/MM/YY				Author				Description
2                 27/12/2017        Andrew Wood       Changed Data Type of Number from BIGINT to INT
1					   22/12/2017			Andrew Wood			Initial Numbers implementation
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Numbers';
GO
