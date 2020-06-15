/* -----------------------------------------------------------------------------------------------------------------------------------
Title (Task Number): 637
Purpose: Linking to for date calculations to save processing along with date cleansing

Development Server: Local SQL Server Instance
Production Server:	DFCRVSQLDW01 | REPORTING	

Prerequisite:	dbo.dimNumbers

Notes:

 See ISO 8601 for details on standard date formats, the Acts Interpretation Act for details on the date treatment for intervals.
 https://www.legislation.sa.gov.au/lz/c/a/acts%20interpretation%20act%201915.aspx

Status: Available for Production

Version				DD/MM/YY				Author				   Description
8                 29/12/2017        Andrew Wood          Improved consistency of PUblic and Private School details
7                 27/12/2017        Andrew Wood          Added Zodiac Horoscope details (8 Fields)
6                 27/12/2017        Andrew Wood          Added Chinese Horoscope details (7 Fields)
5                 27/12/2017        Andrew Wood          Removed Scalar Function [dbo].[fn_JulianDayNumber] dependency
4                 27/12/2017        Andrew Wood          Added 29 new fields which may prove useful for Date table
3                 27/12/2017        Andrew Wood          Corrected Fiscal dates
2                 27/12/2017        Andrew Wood          Extended Date Range from [1900-2020] to [1887-2147] 
1	               03/02/2017	      P. Worthington-Ayre	Initial Date implementation
----------------------------------------------------------------------------------------------------------------------------------- */

--IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'idl')
--   DECLARE @i VARCHAR(50) = 'CREATE SCHEMA [idl]';
--   EXEC (@i);


IF OBJECT_ID('dbo.dimDate') IS NOT NULL DROP TABLE dbo.[dimDate];

SET ANSI_PADDING ON
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE dbo.[dimDate]
      (	-- SET A: 3 Rows
      [DateKey] INT NOT NULL
      , [ActualDate] DATE NOT NULL /* Actual date */
      , [CalendarDate] DATE NOT NULL /* actual date */

      , ActualDateYMD varchar(8) /* YYYYMMDD */
      , ActualDateYDM varchar(8) /* YYYYDDMM */
      , ActualDateDMY varchar(8) /* DDMMYYYY */
      , ActualDateMDY varchar(8) /* MMDDYYYY */

      , ActualDateISO8601 CHAR(10) /* YYYY-MM-DD */
      , ActualDateShortDescription char(11) /* DD MMM YYYY */
      , ActualDateLongDescription varchar(30) /* WeekDayName d month YYYY */

      --
      , SASDate INT /* increment from 1 Jan 1960 as day zero */
      , ExcelDate INT /* increment from 1 Jan 1900 as day 1 */
 
      --Calendar stuff
      , CalendarYearNumber INT /* Calendar year */
      , CalendarYearShortDescription CHAR(6) /* CYXXXX */
      , CalendarYearLongDescription VARCHAR(18) /* Calendar Year XXXX */

      , CalendarHalfYearNumber TINYINT /* 1 or 2 */
      , CalendarHalfYearShortDescription VARCHAR(8) /* CYXXXXH1 */
      , CalendarHalfYearLongDescription VARCHAR(28) /* CYXXXXH1 */

      , CalendarQuarterNumber TINYINT NOT NULL /* Add */
      , CalendarQuarterShortDescription VARCHAR(10) NULL /* CYXXXXQX */ 
      , CalendarQuarterLongDescription VARCHAR(28) NULL /* Full desc */ 

      , CalendarMonthNumber tinyint NOT NULL /* 1-12 */
      , CalendarMonthName varchar(15) /* full name */
      , CalendarMonthAbbreviation CHAR(3) /* 3 letter abbreviation Jan-Dec */
      , CalendarDayOfMonthNumber tinyint /* 1-31 */
      , CalendarDayOfMonthDescription CHAR(3) /* D1-31 */

      ,[CalendarMonthNameAndYearAbbreviated] [nvarchar](8) NULL
      , [CalendarMonthNameAndYearFull] [varchar](14) NULL

      , CalendarDayName VARCHAR(10) /* full name */
      , CalendarDayAbbreviation VARCHAR(3) /* 3 letter abbreviation Sun-Sat */

      , CalendarISOWeekNumber tinyint /* ISO week number 1-52/53.The ISO week-numbering year starts at the first day (Monday) of week 01 and ends at the Sunday before the new ISO year (hence without overlap or gap). It consists of 52 or 53 full weeks. */
      , [CalendarDayOfWeekNumber] int NULL
      , CalendarISOWeekShortDescription varchar(9) /* CYYYYYWww */
      , CalendarWeekNumber TINYINT /* week number SQL format */
      , CalendarWeekShortDescription varchar(9) /* CYYYYYWww */
      , CalendarWeekLongDescription varchar(26) /* Calendar Year XXXX Week ww */

      , OrdinalDateDescription varchar(8) /* YYYY-OOO Ordinal date is days of the year */

      , CalendarDayOfYearNumber SMALLINT /* ordinal calendar day */
      , CalendarDaySuffixDescription VARCHAR(2) /* th, st, etc. */

      ,[ContainsSearch] VARCHAR(31) /* CY1975 + MonthName + D1:D31    Used for Broad Contains Search */


      /* Newly added Fields */
      ,[FirstDayOfMonthFlag] [bit] NULL
      ,[LastDayOfMonthFlag] [bit] NULL
      ,[FirstDayOfMonthDate] [date] NULL
      ,[LastDayOfMonthDate] [date] NULL

      ,[LastSundayOfMonth] [date] NULL
      ,[LastMondayOfMonth] [date] NULL
      ,[LastTuesdayOfMonth] [date] NULL
      ,[LastWednesdayOfMonth] [date] NULL
      ,[LastThursdayOfMonth] [date] NULL
      ,[LastFridayOfMonth] [date] NULL
      ,[LastSaturdayOfMonth] [date] NULL

      ,[FirstDayOfCalendarQuarterFlag] [int] NOT NULL
      ,[LastDayOfCalendarQuarterFlag] [int] NOT NULL
      ,[FirstDayOfCalendarQuarterDate] [date] NULL
      ,[LastDayOfCalendarQuarterDate] [date] NULL

      ,[FirstDayOfCalendarWeekDate] [date] NULL
      ,[LastDayOfCalendarWeekDate] [date] NULL

      ,[FirstDayOfWorkWeek] [datetime] NULL
      ,[LastDayOfWorkWeek] [datetime] NULL

      ,[FirstDayOfMonth] [date] NULL
      ,[LastDayOfMonth] [date] NULL

      ,[FirstDayOfCalendarYear] [date] NULL
      ,[LastDayOfCalendarYear] [date] NULL

      /* Financial */
      , [FinancialYearNumber] [char](4) NULL /* Year of financial year ending */
      ,[FinancialYearShortDescription] [varchar](6) NULL /* FYXXXX */
      ,[FinancialYearLongDescription] [varchar](24) NULL /* Financial Year XXXX-XXXX */

      ,[FinancialYearStartDate] [date] NULL /* beginning of financial year */
      ,[FinancialYearEndDate] [date] NULL /* end of financial year */
      ,[FinancialYearQuarterNumber] [numeric](9, 0) NULL /* 1-4 */
      ,[FinancialYearQuarterDescription] [varchar](14) NULL /* FYXXXXQ1 */
      ,[FinancialYearQuarterNameShortDescription] [varchar](8) NULL/* full desc */
      ,[FinancialYearQuarterNameLongDescription] [varchar](29) NULL
      ,[FinancialYearDayOfYearNumber] [int] NULL
      ,[FinancialYearWeekOfYearNumber] [numeric](18, 0) NULL
      ,[FinancialYearPeriodMonth] [varchar](3) NULL

      -- /* Special 8 Fields*/
      ,[SouthAustralianUTCOffset] VARCHAR(5) NOT NULL /* 9.5 or 10.5 */
      ,[WeekendFlag] INT NOT NULL /* Flag for Saturday or Sunday */
      ,[WeekdayFlag] INT NOT NULL /* Flag for Mon - Fri */
      ,[IsLeapYear] INT NOT NULL
      ,[IsLeapYearDescription] VARCHAR(11) NOT NULL
      ,[PublicHolidaySouthAustraliaFlag] bit NULL /* Flag for Public Holiday */
      ,[PublicHolidaySouthAustraliaName] VARCHAR(200) NULL /* Name of Public Holiday */
      ,[BusinessDayFlag] [bit] NULL /* If for the purposes of an Act or statutory instrument a business day, working day or other period is expressed as excluding a public holiday, the exclusion does not extend to a part-day public holiday (unless the Act expressly provides to the contrary). */
 
      /* 6 fields*/
      ,[PublicSchoolTermNumber] TINYINT NULL
      ,[PublicSchoolDayFlag] BIT NULL
      ,[PrivateSchoolTermNumber] TINYINT NULL
      ,[PrivateSchoolDayFlag] BIT NULL

      ,[DaylightSavingsFlag] INT NULL
      ,[DaylightSavingsUTCOffset]    DECIMAL (3, 1) NULL
      ,[JulianDayNumber] BIGINT NULL

      /*Zodiac Horoscope */
      ,[Zodiac Star Sign Name] VARCHAR(10) NOT NULL --This will become the Primary Key.
      , [Zodiac Star Sign] VARCHAR(16) NOT NULL -- ie Ram, Bull, Twins, Crab, Lion, Maiden ....
      , [Zodiac Star Symbol] NCHAR(1) NOT NULL --a single character symbolic depiction of the Star Sign
      , [Zodiac Star Start Month] VARCHAR(15) NOT NULL
      , [Zodiac Star Start Day] TINYINT NOT NULL
      , [Zodiac Star End Month] VARCHAR(15) NOT NULL
      , [Zodiac Star End Day] TINYINT NOT NULL
      , [Zodiac Star Start Month Day] AS [Zodiac Star Start Month] + ' ' + CAST([Zodiac Star Start Day] AS CHAR(2)) PERSISTED
      , [Zodiac Star End Month Day] AS [Zodiac Star End Month] + ' ' + CAST([Zodiac Star End Day] AS CHAR(2)) PERSISTED
      , [Zodiac Star Sign Order] TINYINT NOT NULL -- https://en.wikipedia.org/wiki/Astrological_sign states there is an order to the Zodiac.

      --The following two fields are used for the mathmatical calculations requried to create the [Date Zodiac Horoscope Derived] table.
      -- these two fields are dropped at the end of this script.
      -- ,[Zodiac Star Start Date] DATETIME NOT NULL
      -- ,[Zodiac Star End Date] DATETIME NOT NULL
 
      /* Chinese Horoscope*/
      , [Chinese Horoscope Animal Name]      VARCHAR(15) NOT NULL
      , [Chinese Horoscope Odd/Even]         VARCHAR(15) NOT NULL
      , [Chinese Horoscope Yin/Yang]         VARCHAR(15) NOT NULL
      , [Chinese Horoscope Attribute]        VARCHAR(15) NOT NULL
      , [Chinese Horoscope Saying]           VARCHAR(60) NOT NULL
      , [Chinese Horoscope Element]          VARCHAR(5) NOT NULL
      , [Chinese Horoscope Characteristics]  VARCHAR(100) NOT NULL

      /* System information 11 */
      , Data_LoadDateTime           DATETIMEOFFSET(7)  DEFAULT (SYSDATETIMEOFFSET()) NOT NULL
      , Data_CurrencyDateTime       DATETIMEOFFSET(7)  DEFAULT (SYSDATETIMEOFFSET()) NOT NULL
      , Data_RecordCleanedFlag      BIT                DEFAULT (0)                   NOT NULL
      , Data_PrimarySourceSystem    VARCHAR(200)                                     NULL
      , Security_Classification     VARCHAR(20)        DEFAULT 'Public'              NOT NULL  /* In absence, default to protected level */
      , Security_PublicFlag         BIT                DEFAULT (0)                   NOT NULL
      , Security_UnclassifiedFlag   BIT                DEFAULT (0)                   NOT NULL
      , Security_ProtectedFlag      BIT                DEFAULT (0)                   NOT NULL
      , Security_ConfidentialFlag   BIT                DEFAULT (0)                   NOT NULL
      , Security_SecretFlag         BIT                DEFAULT (0)                   NOT NULL
      , Security_TopSecretFlag      BIT                DEFAULT (0)                   NOT NULL

      )
GO

EXEC sys.sp_addextendedproperty @name=N'Purpose', @value=N'
The dbo.dimDate table is used to store each possible date in time between two dates
along with the various different ways these dates may be required to be presented.
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimDate'
GO

EXEC sys.sp_addextendedproperty @name=N'Dependencies', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimDate'
GO

EXEC sys.sp_addextendedproperty @name=N'RequiredBy', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimDate'
GO

EXEC sys.sp_addextendedproperty @name=N'Example', @value=N'' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimDate'
GO

EXEC sys.sp_addextendedproperty @name=N'Revisions', @value=N'
Version				DD/MM/YY				Author				   Description
8                 29/12/2017        Andrew Wood          Improved consistency of PUblic and Private School details
7                 27/12/2017        Andrew Wood          Added Zodiac Horoscope details (8 Fields)
6                 27/12/2017        Andrew Wood          Added Chinese Horoscope details (7 Fields)
5                 27/12/2017        Andrew Wood          Removed Scalar Function [dbo].[fn_JulianDayNumber] dependency
4                 27/12/2017        Andrew Wood          Added 29 new fields which may prove useful for Date table
3                 27/12/2017        Andrew Wood          Corrected Fiscal dates
2                 27/12/2017        Andrew Wood          Extended Date Range [1887 through to 2147] up from [1900 to 2020] 
1	               03/02/2017	      P. Worthington-Ayre	Initial Date implementation
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'dimDate'
GO

ALTER TABLE dbo.[dimDate]
	ADD CONSTRAINT PK_dimDate_DateKey PRIMARY KEY CLUSTERED([DateKey] );

GO

CREATE NONCLUSTERED INDEX NCIX_Date_CalendarMonthNumber ON [dbo].[dimDate] ([CalendarMonthNumber])
INCLUDE ([CalendarMonthName])

GO

CREATE NONCLUSTERED INDEX NCIX_Date_CalendarMonthName ON [dbo].[dimDate] ([CalendarYearShortDescription],[CalendarMonthName],[CalendarDayOfMonthNumber])
INCLUDE ([DateKey],[ActualDate],[ActualDateISO8601],[CalendarMonthNumber],[CalendarMonthNameAndYearFull])
GO

 --Thought required. re-write required.  
--CREATE UNIQUE CLUSTERED INDEX NIX_dimDate_Covering
-- ON dbo.[dimDate] ([DateKey],[Date],[IsWeekday],[MonthNameFull],[CalendarYear],[IsLeapYear], [WeekOfYear], [DateAU], [FinancialYearQuarterFullName], [LastTuesdayOfMonth])
-- INCLUDE ([DayNameFull],[MonthNumber], [DayNameAbbreviated], [MonthNameAbbreviated], [MonthNameAndYearAbbreviated]) ;

----GO
--TODO:-- INSERT A DUMMY LINE INTO THE TABLE.  INSERT INTO dbo.[dimDate]VALUES ();

SET NOCOUNT ON;

DECLARE @CodeStartTime TIME; SET @CodeStartTime = CAST(SYSDATETIME() AS TIME) ;
DECLARE @RecordCounter BIGINT;

DECLARE @YearsToPopulate INT = 130;

-- Use the Magic of SQL to identify 1 Jan and then 31st December at the various edges of the requied date time frames.
DECLARE @StartDate DATE = DATEADD(yy, DATEDIFF(yy,0,DATEADD(yyyy,-@YearsToPopulate,GETDATE())), 0);
DECLARE @EndDate DATE = DATEADD(yy, DATEDIFF(yy,0,DATEADD(yyyy,@YearsToPopulate,GETDATE())) + 1, -1);

--We can make the CTE Faster, by using TOP (N) records
-- Instead of using a WHERE Clause to test each output.
DECLARE @RecordsToCreate INT = DATEDIFF(dd,@StartDate,@EndDate);

;WITH MyFullDateRange AS 
(
    SELECT TOP (@RecordsToCreate) CAST(DATEADD(dd, Number, @StartDate) AS DATE) AS DayInTime
    FROM dbo.[Numbers]
) ,
ZodiacIdentified ( [Zodiac Star Sign Name], [Zodiac Star Sign], [Zodiac Star Symbol] ,[Zodiac Star Start Month], [Zodiac Star Start Day] ,[Zodiac Star End Month], [Zodiac Star End Day] ,[Zodiac Star Sign Order],[Zodiac Star Start Date], [Zodiac Star End Date] )
AS
(
 SELECT 'Aries', 'Ram', NCHAR(9800), 'March', 21, 'April', 19, 1, '1900-03-21', '1900-04-19'
 UNION ALL SELECT 'Taurus', 'Bull', NCHAR(9801), 'April', 20, 'May', 20, 2, '1900-04-20', '1900-05-20'
 UNION ALL SELECT 'Gemini', 'Twins', NCHAR(9802), 'May', 21, 'June', 20, 3, '1900-05-21', '1900-06-20'
 UNION ALL SELECT 'Cancer', 'Crab', NCHAR(9803), 'June', 21, 'July', 22, 4, '1900-06-21', '1900-07-22'
 UNION ALL SELECT 'Leo', 'Lion', NCHAR(9804), 'July', 23, 'August', 22, 5, '1900-07-23', '1900-08-22'
 UNION ALL SELECT 'Virgo', 'Maiden', NCHAR(9805), 'August', 23, 'September',22, 6, '1900-08-23', '1900-09-22'
 UNION ALL SELECT 'Libra', 'Scales', NCHAR(9806), 'September', 23, 'October', 21, 7, '1900-09-23', '1900-10-21'
 UNION ALL SELECT 'Scorpio', 'Scorpion', NCHAR(9807), 'October', 23, 'November', 21, 8, '1900-10-22', '1900-11-21'
 UNION ALL SELECT 'Sagitarius', 'Archer (Centaur)', NCHAR(9808), 'November', 22, 'December', 21, 9, '1900-11-22', '1900-12-21'
 UNION ALL SELECT 'Capricorn', 'Sea-Goat (Goat)', NCHAR(9809), 'December', 22, 'January', 19, 10, '1900-12-22', '1901-12-31'
 UNION ALL SELECT 'Capricorn', 'Sea-Goat (Goat)', NCHAR(9809), 'December', 22, 'January', 19, 99, '1900-01-01', '1900-01-19'
 UNION ALL SELECT 'Aquarius', 'Water-bearer', NCHAR(9810), 'January', 20, 'Feburary', 18, 11, '1900-01-20', '1900-02-18'
 UNION ALL SELECT 'Pisces', 'Fish', NCHAR(9811), 'February', 19, 'March', 20, 12, '1900-02-19', '1900-03-20'
),
ChineseHoroscopeIdentified ([Chinese Horoscope Code], [Chinese Animal Year Mod Integer], [Chinese Animal Name], [Chinese Animal Odd/Even] , [Chinese Animal Yin/Yang] , [Chinese Animal Attribute], [Chinese Animal Saying], [Chinese Animal Element], [Chinese Animal Characteristics] ) AS
(
 SELECT 9, 00, 'Monkey' , 'Odd' ,'Yin' ,'Changability' , 'Changability without being constant leads to foolishness.' , 'Metal' , 'Quick-witted, charming, lucky, adaptable, bright, versatile, lively, smart'
 UNION ALL SELECT 10, 01, 'Rooster' , 'Even' ,'Yang' ,'Being constant' , 'Being constant without changability leads to woodeness.' , 'Metal' , 'Honest, energetic, intelligent, flamboyant, flexible, diverse, confident.'
 UNION ALL SELECT 11, 02, 'Dog' , 'Odd' ,'Yin' ,'Fidelity' , 'Fidelity without amiability leads to rejection.' , 'Earth' , 'Loyal, sociable, courageous, diligent, steady, lively, adaptable, smart'
 UNION ALL SELECT 12, 03, 'Pig (Boar)' , 'Even' ,'Yang' ,'Amiability' , 'Amiability' , 'Water' , 'Honorable, philanthropic, determined, optimistic, sincere, sociable '
 UNION ALL SELECT 1, 04, 'Rat' , 'Even and Odd' ,'Yin and Yang' ,'Wisdom' , 'Wisdom without industriousness leads to triviality.' , 'Water' , 'Intelligent, adaptable, quick-witted, charming, artistic, sociable'
 UNION ALL SELECT 2, 05, 'Ox (Bull)' , 'Even' ,'Yang' ,'Industriousness' , 'Industriousness without wisdom leads to futility.' , 'Earth' , 'Loyal, reliable, thorough, strong, reasonable, steady, determined'
 UNION ALL SELECT 3, 06, 'Tiger' , 'Odd' ,'Yin' ,'Valor' , 'Valor without caution leads to recklessness.' , 'Wood' , 'Enthusiastic, courageous, ambitious, leadership, confidence, charismatic'
 UNION ALL SELECT 4, 07, 'Rabbit' , 'Even' ,'Yang' ,'Caution' , 'Caution without valor leads to cowardice.' , 'Wood' , 'Trustworthy, empathic, modest, diplomatic, sincere, sociable, caretakers'
 UNION ALL SELECT 5, 08, 'Dragon' , 'Odd' ,'Yin' ,'Strength' , 'Strength without flexibility leads to fracture.' , 'Earth' , 'Lucky, flexible, eccentric, imaginative, artistic, spiritual, charismatic'
 UNION ALL SELECT 6, 09, 'Snake' , 'Even' ,'Yang' ,'Flexibility' , 'Flexibility without strength leads to compromise.' , 'Fire' , 'Philosophical, organized, intelligent, intuitive, elegant, attentive, decisive'
 UNION ALL SELECT 7, 10, 'Horse' , 'Odd' ,'Yin' ,'Forging ahead' , 'Forging ahead without unity leads to abandonment.' , 'Fire' , 'Adaptable, loyal, courageous, ambitious, intelligent, adventurous, strong'
 UNION ALL SELECT 8, 11, 'Sheep (Goat)', 'Even' ,'Yang' ,'Unity' , 'Unity without forging ahead leads to stagnation.' , 'Earth' , ' Tasteful, crafty, warm, elegant, charming, intuitive, sensitive, calm '
 
)
INSERT INTO dbo.[dimDate]
SELECT 

 CONVERT (char(8),DayInTime,112) as DateKey

 , DayInTime AS [ActualDate] /* Actual date */
 , DayInTime AS [CalendarDate] /* actual date */

 , CONVERT(CHAR(8), DayInTime, 112) AS ActualDateYMD /* YYYYMMDD 112 */
 , RTRIM(YEAR(DayInTime)) + RIGHT('00' + RTRIM(DAY(DayInTime)),2) + RIGHT('00' + RTRIM(MONTH(DayInTime)),2) AS ActualDateYDM /* YYYYDDMM */
 , RIGHT('00' + RTRIM(DAY(DayInTime)),2) + RIGHT('00' + RTRIM(MONTH(DayInTime)),2) + RTRIM(YEAR(DayInTime)) AS ActualDateDMY /* DDMMYYYY */
 , RIGHT('00' + RTRIM(MONTH(DayInTime)),2) + RIGHT('00' + RTRIM(DAY(DayInTime)),2) + RTRIM(YEAR(DayInTime)) AS ActualDateMDY /* MMDDYYYY */

 , CONVERT(CHAR(11), DayInTime, 126) AS ActualDateISO8601
 , CONVERT(CHAR(11), DayInTime, 106) AS ActualDateShortDescription /* DD MMM YYYY */
 , CONVERT(CHAR(11), DayInTime, 126) AS ActualDateLongDescription /* WeekDayName d month YYYY */

 , DATEDIFF(d, '1960-01-01', DayInTime) AS SASDate 
 , CASE
 WHEN DayInTime < '1900-01-01' THEN NULL
 WHEN DayInTime <= '1900-02-28' THEN DATEDIFF(d, '1900-01-01', DayInTime) + 1 /* Excel incorrectly assumes 1900 was a leap year */
 ELSE DATEDIFF(d, '1900-01-01', DayInTime) + 2
 END AS ExcelDate

 /* Calendar Dates */

 , RTRIM(YEAR(DayInTime)) AS CalendarYearNumber
 , 'CY' + RTRIM(YEAR(DayInTime)) AS CalendarYearShortDescription
 , 'Calendar Year ' + RTRIM(YEAR(DayInTime)) AS CalendarYearLongDescription

 , CASE WHEN MONTH(DayInTime) <= 6 THEN 1 ELSE 2 END AS CalendarYearHalfYearNumber
 , 'CY' + RTRIM(YEAR(DayInTime)) + CASE WHEN MONTH(DayInTime) <= 6 THEN 'H1' ELSE 'H2' END AS CalendarHalfYearShortDescription
 , 'Calendar Year ' + RTRIM(YEAR(DayInTime)) + CASE WHEN MONTH(DayInTime) <= 6 THEN ' 1st half' ELSE ' 2nd half' END AS CalendarHalfYearLongDescription 

 , Datepart(Q, DayInTime) aS CalendarQuarterNumber
 , 'CY' + RTRIM(YEAR(DayInTime)) + 'Q' + CAST(Datepart(Q, DayInTime) AS CHAR(1)) AS CalendarQuarterShortDescription
 , 'Calendar Year ' + RTRIM(YEAR(DayInTime)) + ' Quarter ' + CAST(DATEPART(Q, DayInTime) AS CHAR(1)) AS CalendarQuarterLongDescription

 , RTRIM(MONTH(DayInTime)) AS CalendarMonthNumber
 , DATENAME(MONTH, DayInTime) AS CalendarMonthName
 , LEFT(DATENAME(MONTH, DayInTime), 3) AS CalendarMonthAbbreviation
 , DAY(DayInTime) AS CalendarDayOfMonthNumber
 , 'D' + CAST( DAY(DayInTime) AS CHAR(2) ) AS CalendarDayOfMonthDescription

--AW
 ,	LEFT (DATENAME(MM, DayInTime) , 3) + ' ' + CAST(DATEPART(YEAR, DayInTime) AS CHAR(4)) AS [CalendarMonthNameAndYearAbbreviated]
 ,	CAST(DATENAME(MM, DayInTime) AS VARCHAR(9)) + ' ' + CAST(DATEPART(YEAR, DayInTime) AS CHAR(4)) AS [CalendarMonthNameAndYearFull]

 , DATENAME(weekday, DayInTime) AS CalendarDayName
 , LEFT(DATENAME(weekday, DayInTime),3) AS CalendarDayAbbreviation

 , DATEPART(iso_week, DayInTime) AS CalendarISOWeekNumber
 --AW: The DATEPART converts Mon = 1, Tues = 2 etc. -- Mod 7 perorms a 'wrap around' from 1 to 7. 
 , (DATEPART(dw, DayInTime) + 5) % 7 + 1 AS [CalendarDayOfWeekNumber]
 -- /*
 -- NB: Why is there a Scalar function here? ---- , CalendarISOWeekShortDescription = 'CY' + CAST(dbo.fn_ISOYear(@CurrentDate) AS CHAR(4)) + 'W' + RIGHT('00' + rtrim(CAST(datepart(iso_week, @CurrentDate) AS CHAR(2))), 2) 
 -- */
 , 'CY' + RTRIM(YEAR(DayInTime))+ 'W' + RIGHT('00' + RTRIM(CAST(DATEPART(ISO_WEEK, DayInTime) AS CHAR(2))), 2) AS CalendarISOWeekShortDescription
 
 , CalendarWeekNumber = DATEPART(WK, DayInTime)

 , CalendarWeekShortDescription = 'CY' + RTRIM(YEAR(DayInTime)) + 'W' + RIGHT('00' + rtrim(CAST(datepart(wk, DayInTime) AS CHAR(2))), 2)
 , CalendarWeekLongDescription = 'Calendar Year ' + RTRIM(YEAR(DayInTime)) + ' Week ' + RIGHT('00' + rtrim(CAST(datepart(wk, DayInTime) AS CHAR(2))), 2)
 , OrdinalDateDescription = RTRIM(YEAR(DayInTime)) + '-' + RIGHT('000' + rtrim(CAST(datepart(dy, DayInTime) AS CHAR(2))), 3)
 , CalendarDayOfYearNumber = datepart(dy, DayInTime)
 , CASE
 WHEN DATEPART(DD,DayInTime) IN (11,12,13) THEN 'th'
 WHEN RIGHT(DATEPART(DD,DayInTime),1) = 1 THEN 'st'
 WHEN RIGHT(DATEPART(DD,DayInTime),1) = 2 THEN 'nd'
 WHEN RIGHT(DATEPART(DD,DayInTime),1) = 3 THEN 'rd'
 ELSE 'th'
 END AS CalendarDaySuffixDescription


 , 'CY' + RTRIM(YEAR(DayInTime)) + ' ' +  DATENAME(MONTH, DayInTime) + ' ' +  'D' + CAST( DAY(DayInTime) AS CHAR(2) ) + ' ' +  ' CY* M* D*'  AS [ContainsSearch]
  
 , FirstDayOfMonthFlag = CAST(CASE WHEN DAY(DayInTime) = 1 THEN 1 ELSE 0 END AS BIT)
 , LastDayOfMonthFlag = CAST(CASE WHEN CAST(DATEADD(s,-1,DATEADD(mm, DATEDIFF(m,0,DayInTime)+1,0)) AS DATE) = DayInTime THEN 1 ELSE 0 END AS BIT)
 , FirstDayOfMonthDate = CONVERT(DATE, CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, DayInTime) - 1), DayInTime)))
 , LastDayOfMonthDate = CAST(DATEADD(s,-1,DATEADD(mm, DATEDIFF(m,0,DayInTime)+1,0)) AS DATE)
  
		--Sunday [DayOfWeek] = 1.. Need to convert 1 to 0 <-> N + (7 - 1) % 7
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7 - 1) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastSundayOfMonth]
 
	--Monday [DayOfWeek] = 2.. Need to convert 2 to 0 <-> N + (7 - 2) % 7 
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7 - 2) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastMondayOfMonth]
		
	--Tuesday [DayOfWeek] = 3.. Need to convert 3 to 0 <-> N + (7 - 3) % 7
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7 -3) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastTuesdayOfMonth]
		
	--Wednesday [DayOfWeek] = 4.. Need to convert 4 to 0 <-> N + (7 - 4) % 7
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7 - 4) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastWednesdayOfMonth]
		
	--Thursday [DayOfWeek] = 5.. Need to convert 5 to 0 <-> N + (7 - 5 ) % 7
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7 - 5) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastThursdayOfMonth]
		
	--Friday [DayOfWeek] = 6.. Need to convert 6 to 0 <-> N + (7 - 6 ) % 7
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7-6) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastFridayOfMonth]
		
	--Saturday [DayOfWeek] = 7.. Need to convert 7 to 0 <-> N + (7 - 7 ) % 7
	,DATEADD(DD,
			- ((DATEPART(dw, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) + (7-7) ) % 7 ,
			CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))
		)
		AS [LastSaturdayOfMonth]

 -- /* Can these two be improved?*/
 , FirstDayOfCalendarQuarterFlag = CASE WHEN DATEADD(QQ, DATEDIFF(QQ, 0, DayInTime), 0) = DayInTime THEN 1 ELSE 0 END
 , LastDayOfCalendarQuarterFlag = CASE WHEN DATEADD(QQ, DATEDIFF(QQ, -1, DayInTime), -1) = DayInTime THEN 1 ELSE 0 END

 , CAST( DATEADD(QQ, DATEDIFF(QQ, 0, DayInTime), 0)AS DATE) AS FirstDayOfCalendarQuarterDate
 , CAST( DATEADD(QQ, DATEDIFF(QQ, -1, DayInTime), -1)AS DATE) AS LastDayOfCalendarQuarterDate

 , DATEADD(dd, -(DATEPART(dw, DayInTime)-1), DayInTime) AS FirstDayOfCalendarWeekDate
 , DATEADD(dd, 7-(DATEPART(dw, DayInTime)), DayInTime) AS LastDayOfCalendarWeekDate


 -- 	/* Double check to see if these are new items and rename accordingly */
 , DATEADD(WEEK, DATEDIFF(WEEK, 0, DayInTime), 0) AS [FirstDayOfWorkWeek]
 , DATEADD(DAY,4, DATEADD(WEEK, DATEDIFF(WEEK, 0, DayInTime), 0)) AS [LastDayOfWorkWeek] --NB, this is the same formula as [FistDayOfWeek], but hten we add 5 days to this date.

 , CONVERT(DATE, CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, DayInTime) - 1), DayInTime))) AS [FirstDayOfMonth]
 , CONVERT(DATE, CONVERT(DATE, DATEADD(DD, - (DATEPART(DD, (DATEADD(MM, 1, DayInTime)))), DATEADD(MM, 1, DayInTime)))) AS [LastDayOfMonth]

 , CONVERT(DATE, '01/01/' + CONVERT(VARCHAR, DATEPART(YY, DayInTime))) AS [FirstDayOfCalendarYear]
 , CONVERT(DATE, '12/31/' + CONVERT(VARCHAR, DATEPART(YY, DayInTime))) AS [LastDayOfCalendarYear]
 -- /* Financial */ 
 -- -- Set Fiscal: XX Rows; 12xChars; 4xDates

 , CAST(YEAR(DATEADD(MONTH, 6, DayInTime)) AS CHAR(4) ) FinancialYearNumber
 , 'FY' + CAST(YEAR(DATEADD(MONTH, 6, DayInTime)) AS CHAR(4) ) AS FinancialYearShortDescription -- CONCAT('FYE ', YEAR(@CurrentDate + 184) ) 
 , 'Financial year ' + CAST(YEAR(DATEADD(MONTH, 6, DayInTime)) -1 AS CHAR(4) ) + '-' + CAST(YEAR(DATEADD(MONTH, 6, DayInTime)) AS CHAR(4) ) AS FinancialYearLongDescription 

 , CAST(DATEADD(YEAR,DATEDIFF(MONTH,'18010701',DayInTime)/12,'18010701') AS DATE) AS [FinancialYearStartDate] 
 , CAST(DATEADD(YEAR, 1, DATEADD(YEAR, DATEDIFF(MONTH,'18010701', DayInTime) / 12 , '18010630') ) AS DATE) AS [FinancialYearEndDate]
 , CEILING(CAST(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END AS NUMERIC(3,1)) /3.0) AS [FinancialYearQuarterNumber]
 
 , CASE 
 WHEN RIGHT ('00' + LTRIM(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END),2 ) 
 BETWEEN 7 AND 9 THEN 'Third Quarter'
 WHEN RIGHT ('00' + LTRIM(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END),2 ) 
 BETWEEN 10 AND 12 THEN 'Fourth Quarter'
 WHEN RIGHT ('00' + LTRIM(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END),2 ) 
 BETWEEN 1 AND 3 THEN 'First Quarter'
 WHEN RIGHT ('00' + LTRIM(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END),2 ) 
 BETWEEN 4 AND 6 THEN 'Second Quarter'
 END FinancialYearQuarterDescription
 
 , 'FY' + CAST(YEAR(DATEADD(MONTH, 6, DayInTime)) AS CHAR(4) ) + 'Q' + CAST( CEILING(CAST(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END AS NUMERIC(3,1)) /3.0) AS CHAR(1)) AS [FinancialYearQuarterNameShortDescription]
 , 'Financial year ' + CAST(YEAR(DATEADD(MONTH, 6, DayInTime)) AS CHAR(4) ) + ' Quarter ' + CAST( CEILING(CAST(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END AS NUMERIC(3,1)) /3.0) AS CHAR(1)) AS [FinancialYearQuarterNameLongDescription]
 , DATEDIFF(dd,DATEADD(YEAR,DATEDIFF(MONTH,'18010701',DayInTime)/12,'18010701'),DayInTime) + 1 AS [FinancialYearDayOfYearNumber]
 , CEILING((DATEDIFF(dd,DATEADD(YEAR,DATEDIFF(MONTH,'18010701',DayInTime)/12,'18010701'),DayInTime) + 1.0 ) / 7.0 ) AS [FinancialYearWeekOfYearNumber]
 , 'P' + RIGHT ('00' + LTRIM(CASE WHEN (DATEPART(MONTH,DayInTime)-(6))<=(0) THEN DATEPART(MONTH,DayInTime)+(6) ELSE DATEPART(MONTH,DayInTime)-(6) END),2 ) AS [FinancialYearPeriodMonth]
 
 /* Time Offsets */
 , CASE 
 WHEN RIGHT( CONVERT(datetime2(0), DayInTime, 126) AT TIME ZONE 'Cen. Australia Standard Time',6) = '+09:30' THEN '9.50'
 ELSE '10.50'
 END AS SouthAustralianUTCOffset

 /* Flags */
 , CASE DATEPART(DW, DayInTime)
		WHEN 1 THEN 0
	 WHEN 7 THEN 0
		ELSE 1
	END AS WeekendFlag

 , CASE DATEPART(DW, DayInTime)
		WHEN 1 THEN 1
	 WHEN 7 THEN 1
		ELSE 0
	END AS WeekdayFlag

 , CASE
 WHEN ISDATE(CAST(YEAR(DayInTime) AS CHAR(4) ) + '0229') = 1 THEN 1 
 ELSE 0
 END AS [IsLeapYear],

 CASE
 WHEN ISDATE(CAST(YEAR(DayInTime) AS CHAR(4) ) + '0229') = 1 THEN 'LEAP YEAR' 
 ELSE 'NORMAL YEAR' 
 END AS [IsLeapYearDescription]

 ,0 AS PublicHolidaySouthAustraliaFlag 
 ,'Not a public holiday' AS PublicHolidaySouthAustraliaName 
 ,BusinessDayFlag = CAST( CASE WHEN DATENAME(weekday, DayInTime) NOT IN ('Saturday', 'Sunday') THEN 1 ELSE 0 END AS BIT )
 --Prefer to update these directly into the table. If the tables below are modified or missing, the dimDate table will refuse to function.
 --, PublicHolidaySouthAustraliaFlag = CAST(coalesce((SELECT 1 FROM dbo.ODS_PublicHolidays WHERE CalendarDate = DayInTime),0) AS BIT)
 --, PublicHolidaySouthAustraliaName = coalesce((SELECT PublicHolidayDescription FROM dbo.ODS_PublicHolidays WHERE CalendarDate = DayInTime AND FullDayFlag = 1),'Not a public holiday')
 --, BusinessDayFlag = CAST(CASE WHEN coalesce((SELECT 1 FROM dbo.ODS_PublicHolidays WHERE CalendarDate = DayInTime AND FullDayFlag = 1),0) = 0 AND DATENAME(weekday, DayInTime) NOT IN ('Saturday', 'Sunday') THEN 1 ELSE 0 END AS BIT)

 /* Special */

  ,99 AS [PublicSchoolTermNumber] 
  ,0 AS [PublicSchoolDayFlag]
  ,99 AS [PrivateSchoolTermNumber] 
  ,0 AS [PrivateSchoolDayFlag] 
  ,0 AS [DaylightSavingsFlag]
  ,-99.9 AS [DaylightSavingsUTCOffset]

  --Prefer to update these directly into the table. If the tables below are modified or missing, the dimDate table will refuse to function.
 --, PublicSchoolTermNumber = coalesce((SELECT termnumber FROM dbo.ODS_SchoolTerms WHERE CountryName = 'Australia' AND StateName = 'South Australia' AND DayInTime BETWEEN datefrom AND dateto AND PublicSchoolFlag = 1),0)
 --, PublicSchoolDayFlag = coalesce((SELECT 1 FROM dbo.ODS_SchoolTerms WHERE CountryName = 'Australia' AND StateName = 'South Australia' AND DayInTime BETWEEN datefrom AND dateto AND PublicSchoolFlag = 1),0)
 --, PrivateSchoolTermNumber = coalesce((SELECT termnumber FROM dbo.ODS_SchoolTerms WHERE CountryName = 'Australia' AND StateName = 'South Australia' AND DayInTime BETWEEN datefrom AND dateto AND PrivateSchoolFlag = 1),0)
 --, DaylightSavingsFlag = coalesce((SELECT 1 FROM dbo.ODS_DaylightSavingTime WHERE DayInTime BETWEEN CAST(DaylightSavingsFromDateTime AS DATE) AND CAST(DaylightSavingsToDateTime AS DATE)), 0)
 
 -- https://en.wikipedia.org/wiki/Julian_day JulianDayNumber 
 , (1461 * (YEAR(DayInTime) + 4800 + (MONTH (DayInTime) - 14)/12))/4 +(367 * (MONTH (DayInTime) - 2 - 12 * ((MONTH (DayInTime) - 14)/12)))/12 - (3 * ((YEAR (DayInTime) + 4900 + (MONTH (DayInTime) - 14)/12)/100))/4 + DAY (DayInTime) - 32075 AS JulianDayNumber

 /*Zodiac Horoscope*/
 , ZodiacHoroscope.[Zodiac Star Sign Name]
 , ZodiacHoroscope.[Zodiac Star Sign]
 , ZodiacHoroscope.[Zodiac Star Symbol] 
 , ZodiacHoroscope.[Zodiac Star Start Month]
 , ZodiacHoroscope.[Zodiac Star Start Day] 
 , ZodiacHoroscope.[Zodiac Star End Month]
 , ZodiacHoroscope.[Zodiac Star End Day] 
 , ZodiacHoroscope.[Zodiac Star Sign Order]

 /* Chinese Horoscope */

 , [ChineseHoroscope].[Chinese Animal Name]
 , [ChineseHoroscope].[Chinese Animal Odd/Even] 
 , [ChineseHoroscope].[Chinese Animal Yin/Yang] 
 , [ChineseHoroscope].[Chinese Animal Attribute]
 , [ChineseHoroscope].[Chinese Animal Saying]
 , [ChineseHoroscope].[Chinese Animal Element]
 , [ChineseHoroscope].[Chinese Animal Characteristics]

 /* Security*/

 , Data_LoadDateTime = SYSDATETIMEOFFSET()
 , Data_CurrencyDateTime = SYSDATETIMEOFFSET()
 , Data_RecordCleanedFlag = CAST(0 AS BIT)
 , Data_PrimarySourceSystem = 'Office for Data Analytics'
 , Security_Classification = 'Public'
 , Security_PublicFlag = CAST(1 AS BIT)
 , Security_UnclassifiedFlag = CAST(0 AS BIT)
 , Security_ProtectedFlag = CAST(0 AS BIT)
 , Security_ConfidentialFlag = CAST(0 AS BIT)
 , Security_SecretFlag = CAST(0 AS BIT)
 , Security_TopSecretFlag = CAST(0 AS BIT)
 
FROM MyFullDateRange AS FDR

 LEFT JOIN ZodiacIdentified AS ZodiacHoroscope 
   ON  FDR.DayInTime 
 BETWEEN DATEADD(year, DATEDIFF(year, ZodiacHoroscope.[Zodiac Star Start Date], DayInTime), ZodiacHoroscope.[Zodiac Star Start Date])
 AND DATEADD(year, DATEDIFF(year, ZodiacHoroscope.[Zodiac Star End Date], DayInTime) , ZodiacHoroscope.[Zodiac Star End Date])

 LEFT JOIN ChineseHoroscopeIdentified AS [ChineseHoroscope] ON
 YEAR(FDR.DayInTime) % 12 = [ChineseHoroscope].[Chinese Animal Year Mod Integer];

 SET @RecordCounter = @@ROWCOUNT;

   --DECLARE @CodeEndTime DECIMAL(12,0); SET @CodeEndTime = CEILING ( ( SELECT [TotalMilliSeconds]/60 FROM meta.[utf_ConvertSecondsToLengthOfTime] (@CodeStartTime, SYSDATETIME() ) ));
   --EXEC  [meta].[usp_HousingSA_ETLLoad_RecordAction] 
   --           @RecordCount =@RecordCounter
   --         , @Updated = '[Date] Table Populated'
   --         , @TimeToRun = @CodeEndTime;

   --RAISERROR (N'**************************************',0,1) WITH NOWAIT;
   --RAISERROR (N'[Date] Table Populated.',0,1) WITH NOWAIT;
   --RAISERROR (N'Andrew Wood 2018 ',0,1) WITH NOWAIT;
   --RAISERROR (N'Senior Business Intelligence Developer',0,1) WITH NOWAIT;
   --RAISERROR (N'Office for Data Analytics',0,1) WITH NOWAIT;
   --RAISERROR (N'Department of the Premier and Cabinet',0,1) WITH NOWAIT;
   --RAISERROR (N'**************************************',0,1) WITH NOWAIT;
   --RAISERROR (N'',0,1) WITH NOWAIT;

--ENABLE THIS FOR A REAL COMPARISON.
--WHERE FDR.DayInTime BETWEEN '19000101' AND '20201231'

GO



