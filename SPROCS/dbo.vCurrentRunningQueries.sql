CREATE VIEW [dbo].[vCurrentRunningQueries] AS

select
    P.spid
,   right(convert(varchar,
            dateadd(ms, datediff(ms, P.last_batch, getdate()), '1900-01-01'),
            121), 12) as 'batch_duration'
,   P.program_name
,   P.hostname
,   P.cmd
,   P.loginame
, t.text
from dbo.sysprocesses P
cross apply sys.dm_exec_sql_text(p.sql_handle) t

where
P.spid > 50
and  P.status not in ('background', 'sleeping')
and      P.cmd not in ('AWAITING COMMAND'
                    ,'MIRROR HANDLER'
                    ,'LAZY WRITER'
                    ,'CHECKPOINT SLEEP'
                    ,'RA MANAGER')
--order by batch_duration DESC
