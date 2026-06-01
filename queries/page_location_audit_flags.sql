select
    audit_flag,
    hostname,
    page_location,
    event_name,
    sessions,
    active_users,
    event_count
from v_raw_ga4_page_location_events
where audit_flag <> 'normal'
order by sessions desc nulls last
limit 200;