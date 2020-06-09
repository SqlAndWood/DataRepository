-- Properties sourced from http://msdn.microsoft.com/en-au/library/ms174396.aspx
CREATE VIEW dbo.vSQLServerProperties AS 

SELECT 
	  @@SERVERNAME AS Server
	, SERVERPROPERTY('MachineName') AS Machine
	, CASE SERVERPROPERTY('productlevel')
		WHEN 'RTM' THEN 'Original release version'
		WHEN 'SP%' THEN 'Service pack version' 
		WHEN 'CTP' THEN 'Community Technology Preview version'
	  END AS ProductLevel
	, SERVERPROPERTY ('ProductVersion') AS Version
	, SERVERPROPERTY ('edition') AS Edition
	, CASE SERVERPROPERTY ('EngineEdition') 
		WHEN 1 THEN 'Personal or Desktop Engine'
		WHEN 2 THEN 'Standard'
		WHEN 3 THEN 'Enterprise'
		WHEN 4 THEN 'Express'
		WHEN 5 THEN 'SQL Database'
		ELSE 'Unknown' 
	  END AS EditionEngine
	, CASE SERVERPROPERTY ('editionid') 
		WHEN 1804890536 THEN 'Enterprise'
		WHEN 1872460670 THEN 'Enterprise Edition: Core-based Licensing'
		WHEN 610778273 THEN 'Enterprise Evaluation'
		WHEN 284895786 THEN 'Business Intelligence'
		WHEN -2117995310 THEN 'Developer'
		WHEN -1592396055 THEN 'Express'
		WHEN -133711905 THEN 'Express with Advanced Services'
		WHEN -1534726760 THEN 'Standard'
		WHEN 1293598313 THEN 'Web'
		WHEN 1674378470 THEN 'SQL Database'
	  END AS EditionIDValue
	, CASE SERVERPROPERTY ('HadrManagerStatus') 
		WHEN 0 THEN 'Not started, pending communication'
		WHEN 1 THEN 'Started and running'
		WHEN 2 THEN 'Not started and failed'
	  END AS AlwaysOn
	, CASE SERVERPROPERTY ('IsClustered')
		WHEN 1 THEN 'Clustered'
		WHEN 0 THEN 'Not Clustered'
	  END AS FailoverClustering
	, CASE SERVERPROPERTY ('IsFullTextInstalled') 
		WHEN 1 THEN 'Full-text and semantic indexing components are installed'
		WHEN 0 THEN 'Full-text and semantic indexing components are not installed'
	  END AS FullTextIndexing
	, CASE SERVERPROPERTY ('IsIntegratedSecurityOnly')
		WHEN 1 THEN 'Integrated security (Windows Authentication)'
		WHEN 0 THEN 'Not integrated security. (Both Windows Authentication and SQL Server Authentication.)'
	  END AS IntegratedSecurityMode
	, CASE SERVERPROPERTY ('IsXTPSupported')
		WHEN 1 THEN 'Server supports In-Memory OLTP'
		WHEN 0 THEN 'Server does not supports In-Memory OLTP'
	  END AS InMemoryOLTP
--	, SERVERPROPERTY ('Collation') AS Collation
--  , SERVERPROPERTY ('ComparisonStyle')
	, @@VERSION AS VersionString
	--, (SELECT convert(decimal(5,2),(CAST(total_physical_memory_kb AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) AS MemoryGB
	--, (SELECT convert(decimal(5,2),(CAST(total_page_file_kb AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) AS PagefileGB	
	--, (SELECT convert(decimal(5,2),(CAST(total_physical_memory_kb AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) AS MemoryGB
	--, (SELECT convert(decimal(5,2),(CAST(total_page_file_kb AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) - (SELECT convert(decimal(5,2),(CAST(available_page_file_kb  AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) AS InUsePagefileGB
	--, (SELECT convert(decimal(5,2),(CAST(total_page_file_kb AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) AS PagefileGB	
	--, (SELECT convert(decimal(5,2),(CAST(available_page_file_kb  AS DECIMAL(15,2))/1024/1024)) FROM sys.dm_os_sys_memory) AS AvailablePagefileGB
	--, (SELECT system_memory_state_desc FROM sys.dm_os_sys_memory) AS SystemMemoryState
	--, (SELECT windows_release FROM sys.dm_os_windows_info) AS WindowsRelease
	--, (SELECT windows_service_pack_level FROM sys.dm_os_windows_info) AS WindowsServicePackLevel
	--, (SELECT windows_sku FROM sys.dm_os_windows_info) AS WindowsSKU
