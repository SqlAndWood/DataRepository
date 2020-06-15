
/*

I suggest you use Visual Studio Code to run this

as SSMS has a terrible side effect of truncating every line at X thousand characters.

*/
select @@SERVERNAME

	SELECT 
	    [DateKey] AS [CalendarDate_Key]
 
      ,[CalendarDate]
		,[ActualDateDMY] AS DateDMY_Key
		,LEFT([ActualDateDMY], 2) + '/' + RIGHT(LEFT([ActualDateDMY], 4), 2) + '/'+ RIGHT([ActualDateDMY], 4) AS DateDMY
      
   
	FROM [ReferenceData].[dbo].[dimDate]
	where datekey >= 18900101
	and datekey <=  20501231
	
	ORDER BY datekey
	
	FOR JSON AUTO, INCLUDE_NULL_VALUES







