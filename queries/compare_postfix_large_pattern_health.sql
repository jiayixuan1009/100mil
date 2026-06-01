select
    'response_codes' as source,
    "Status Code" as status_code,
    Status as status,
    Indexability as indexability,
    "Indexability Status" as indexability_status,
    count(*) as row_count
from v_large_pattern_response_codes
where matched_patterns like '%compare%'
group by 1,2,3,4,5
union all
select
    'internal_all' as source,
    "Status Code" as status_code,
    Status as status,
    Indexability as indexability,
    "Indexability Status" as indexability_status,
    count(*) as row_count
from v_large_pattern_internal_all
where matched_patterns like '%compare%'
group by 1,2,3,4,5
order by source, row_count desc;