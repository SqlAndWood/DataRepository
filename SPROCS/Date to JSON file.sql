
/*


File menu system: Query
Query Options
Results > Grid > Change to unlimited

*/

	SELECT
	    [DateKey]
 
      ,[CalendarDate]
      ,[ActualDateYMD]
      
      ,[ActualDateDMY]
    
     
      ,[ActualDateShortDescription]

      ,[CalendarYearNumber]
      ,[CalendarYearShortDescription]

      ,[CalendarHalfYearNumber]
      ,[CalendarHalfYearShortDescription]
  
      ,[CalendarQuarterNumber]
      ,[CalendarQuarterShortDescription]
    
      ,[CalendarMonthNumber]
      ,[CalendarMonthName]
      ,[CalendarMonthAbbreviation]
      ,[CalendarDayOfMonthNumber]

      ,[CalendarMonthNameAndYearAbbreviated]
      ,[CalendarMonthNameAndYearFull]
      ,[CalendarDayName]
      ,[CalendarDayAbbreviation]
  
      ,[CalendarDayOfWeekNumber]
      
      ,[CalendarWeekNumber]

 
      ,[CalendarDayOfYearNumber]
      ,[CalendarDaySuffixDescription]
    
      ,[FirstDayOfMonthFlag]
      ,[LastDayOfMonthFlag]
      ,[FirstDayOfMonthDate]
      ,[LastDayOfMonthDate]
      ,[LastSundayOfMonth]
      ,[LastMondayOfMonth]
      ,[LastTuesdayOfMonth]
      ,[LastWednesdayOfMonth]
      ,[LastThursdayOfMonth]
      ,[LastFridayOfMonth]
      ,[LastSaturdayOfMonth]
      ,[FirstDayOfCalendarQuarterFlag]
      ,[LastDayOfCalendarQuarterFlag]
      ,[FirstDayOfCalendarQuarterDate]
      ,[LastDayOfCalendarQuarterDate]
      ,[FirstDayOfCalendarWeekDate]
      ,[LastDayOfCalendarWeekDate]
      ,[FirstDayOfWorkWeek]
      ,[LastDayOfWorkWeek]
      ,[FirstDayOfMonth]
      ,[LastDayOfMonth]
      ,[FirstDayOfCalendarYear]
      ,[LastDayOfCalendarYear]

      ,[FinancialYearNumber]
      ,[FinancialYearShortDescription]

      ,[FinancialYearStartDate]
      ,[FinancialYearEndDate]
      ,[FinancialYearQuarterNumber]
    
      ,[FinancialYearQuarterNameShortDescription]
    
      ,[FinancialYearDayOfYearNumber]
      ,[FinancialYearWeekOfYearNumber]

      ,[WeekendFlag]
      ,[WeekdayFlag]
      ,[IsLeapYear]
      ,[IsLeapYearDescription]
      ,[BusinessDayFlag]
      ,[DaylightSavingsFlag]

      ,[JulianDayNumber]
	FROM [ReferenceData].[dbo].[dimDate]

	ORDER BY datekey
	
	FOR JSON AUTO, INCLUDE_NULL_VALUES







