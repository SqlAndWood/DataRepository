/* -----------------------------------------------------------------------------------------------------------------------------------
Title (Task Number): 637
Purpose: Linking to for time calculations to save processing along with Time cleansing

Development Server: Local SQL Server Instance
Production Server:	 | 	

Prerequisite:	dbo.dimNumbers

Notes: Need to work on the appearance of Time while retaining the data type of time.


Status: Available for Production

Version				DD/MM/YY				Author				   Description

1	               28/12/2017	      Andrew Wood       	Initial Date implementation
----------------------------------------------------------------------------------------------------------------------------------- */


GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF OBJECT_ID('dbo.dimTime') IS NOT NULL DROP TABLE dbo.dimTime;

CREATE TABLE dbo.dimTime(
	[Time]               CHAR(8)  NOT NULL,
	[TimeAMPM]           CHAR(11) NULL,
	[24Hour]             CHAR(8)  NULL,
	[24HourAMPM]         CHAR(11) NULL,
	[HourNumber]         TINYINT NULL,
	[24HourNumber]       TINYINT NULL,
	[MinuteNumber]       TINYINT NULL,
	[SecondNumber]       TINYINT NULL,
	[HourDescription]    CHAR(2) NULL,
	[24HourDescription]  CHAR(2) NULL,
	[MinuteDescription]  CHAR(2) NULL,
	[SecondDescription]  CHAR(2) NULL,
	[AMPM]               CHAR(2) NOT NULL,
	[SecondsFromMidnight]   INT  NOT NULL,
	[SeondsToMidnight]      INT  NOT NULL,
   [Time2]              TIME  NOT NULL

   , Data_LoadDateTime           DATETIMEOFFSET(7)  DEFAULT (SYSDATETIMEOFFSET()) NOT NULL
   , Data_CurrencyDateTime       DATETIMEOFFSET(7)  DEFAULT (SYSDATETIMEOFFSET()) NOT NULL
   , Data_RecordCleanedFlag      BIT                DEFAULT (1)                   NOT NULL
   , Data_PrimarySourceSystem    VARCHAR(200)       DEFAULT ('http://www.poodwaddle.com/worldclock/')           NULL
   , Security_Classification     VARCHAR(20)        DEFAULT 'Public'           NOT NULL  /* In absence, default to protected level */
   , Security_PublicFlag         BIT                DEFAULT (0)                   NOT NULL
   , Security_UnclassifiedFlag   BIT                DEFAULT (0)                   NOT NULL
   , Security_ProtectedFlag      BIT                DEFAULT (0)                   NOT NULL
   , Security_ConfidentialFlag   BIT                DEFAULT (0)                   NOT NULL
   , Security_SecretFlag         BIT                DEFAULT (0)                   NOT NULL
   , Security_TopSecretFlag      BIT                DEFAULT (0)    


) ON [PRIMARY]
GO


EXEC sys.sp_addextendedproperty @name=N'Purpose', @value=N'
The dbo.dimTime table maintains a list of each second between Midnight and 11:59:59 PM
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimTime'
GO

EXEC sys.sp_addextendedproperty @name=N'Dependencies', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimTime'
GO

EXEC sys.sp_addextendedproperty @name=N'RequiredBy', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimTime'
GO

EXEC sys.sp_addextendedproperty @name=N'Example', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimTime'
GO

EXEC sys.sp_addextendedproperty @name=N'Revisions', @value=N'
Version				DD/MM/YY				Author				   Description
1	               28/12/2017	      Andrew Wood       	Initial Date implementation
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimTime'
GO

ALTER TABLE dbo.[dimTime]
	ADD CONSTRAINT PK_dimTime_SecondsFromMidnight PRIMARY KEY NONCLUSTERED([SecondsFromMidnight] );

 GO

SET NOCOUNT ON;

DECLARE @CodeStartTime TIME; SET @CodeStartTime = CAST(SYSDATETIME() AS TIME) ;
DECLARE @RecordCounter BIGINT;

DECLARE @StartTime TIME = '12:00:00 AM';
DECLARE @EndTime TIME = '11:59:59 PM'

DECLARE @SecondsPerDay INT = (SELECT Datediff(s, @StartTime, @EndTime) + 1);

--We can make the CTE Faster, by using TOP (N) records
--REMEMBER, SecondsInTime is a TIME datatype, which means 24 hour time.
;WITH MyFullDateRange AS 
(
 SELECT TOP (@SecondsPerDay) CAST(DATEADD(s, Number, @StartTime) AS TIME) AS SecondsInTime
 FROM dbo.[Numbers]
) 
INSERT INTO  dbo.dimTime
   ([Time] ,[TimeAMPM] ,[24Hour] ,[24HourAMPM] ,[HourNumber] ,[24HourNumber] ,[MinuteNumber] ,[SecondNumber] ,[HourDescription] ,[24HourDescription] ,[MinuteDescription] ,[SecondDescription] ,[AMPM] ,[SecondsFromMidnight] ,[SeondsToMidnight] ,[Time2]
)
SELECT 

   REPLACE(LEFT(CONVERT(VARCHAR(26), SecondsInTime, 109) , 8), '.', '')  AS [Time]

   , REPLACE(LEFT(CONVERT(VARCHAR(26), SecondsInTime, 109) , 8), '.', '')
         + ' ' +  CASE WHEN DATEPART(HOUR, SecondsInTime) BETWEEN 0 AND 11 THEN 'AM' ELSE 'PM' END AS [TimeAMPM]

   , LEFT(CONVERT(VARCHAR(12),SecondsInTime,114), 8)  AS [24Hour]
   , CAST(CONVERT(TIME(0),SecondsInTime) AS CHAR(8)) + ' ' +  CASE WHEN DATEPART(HOUR, SecondsInTime) BETWEEN 0 AND 11 THEN 'AM' ELSE 'PM' END AS [24HourAMPM]
 

    , CASE 
         WHEN DATEPART(HOUR,SecondsInTime)  IN ( 0 , 12) THEN 12
         WHEN DATEPART(HOUR,SecondsInTime)  < 12 THEN DATEPART(HOUR,SecondsInTime) 
         ELSE DATEPART(HOUR,SecondsInTime)  - 12 
      END AS [HourNumber]

   , DATEPART(HOUR,SecondsInTime)   AS [24HourNumber] --Military
   , DATEPART(MINUTE,SecondsInTime) AS [MinuteNumber]
   , DATEPART(SECOND,SecondsInTime) AS [SecondNumber]

    , RIGHT('00' +RTRIM(CAST(
         CASE 
            WHEN DATEPART(HOUR,SecondsInTime)  IN ( 0 , 12) THEN 12
            WHEN DATEPART(HOUR,SecondsInTime)  < 12 THEN DATEPART(HOUR,SecondsInTime) 
            ELSE DATEPART(HOUR,SecondsInTime)  - 12 
       END  AS CHAR(2) ) ),2 ) AS [HourDescription]

   ,  RIGHT('00' + rtrim(CAST(DATEPART(HOUR,SecondsInTime) AS CHAR(2)))  , 2)   AS [24HourDescription] --Military
   ,  RIGHT('00' + rtrim(CAST(DATEPART(MINUTE,SecondsInTime) AS CHAR(2))) , 2)  AS [MinuteDescription]
   ,  RIGHT('00' + rtrim(CAST(DATEPART(SECOND,SecondsInTime) AS CHAR(2))) , 2)  AS [SecondDescription]

   ,  CASE WHEN DATEPART(HOUR, SecondsInTime) BETWEEN 0 AND 11 THEN 'AM' ELSE 'PM' END AS [AMPM]
   
 , DATEDIFF(SECOND, '19000101', SecondsInTime) AS SecondsFromMidnight

 , MAX((DATEPART(hour, SecondsInTime) * 3600) + (DATEPART(minute, SecondsInTime) * 60) + DATEPART(second, SecondsInTime)) OVER (PARTITION BY 0) 
      -  DATEDIFF(SECOND, '19000101', SecondsInTime)  AS SeondsToMidnight

   , SecondsInTime AS [Time2]

FROM MyFullDateRange AS FDR;



RAISERROR (N'**************************************',0,1) WITH NOWAIT;
RAISERROR (N'[Date] Table Populated.',0,1) WITH NOWAIT;
RAISERROR (N'Andrew Wood 2018 ',0,1) WITH NOWAIT;
RAISERROR (N'Senior Business Intelligence Developer',0,1) WITH NOWAIT;
RAISERROR (N'Office for Data Analytics',0,1) WITH NOWAIT;
RAISERROR (N'Department of the Premier and Cabinet',0,1) WITH NOWAIT;
RAISERROR (N'**************************************',0,1) WITH NOWAIT;
RAISERROR (N'',0,1) WITH NOWAIT;

