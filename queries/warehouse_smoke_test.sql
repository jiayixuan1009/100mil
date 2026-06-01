select 'tables' as metric, count(*) as value from v_workspace_tables
union all
select 'compare_blockers', count(*) from v_compare_blockers
union all
select 'converter_pages', count(*) from v_converter_low_ctr
union all
select 'top_opportunities', count(*) from v_top_gsc_opportunities;