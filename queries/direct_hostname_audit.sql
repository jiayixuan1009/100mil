select
    hostname_class,
    hostname,
    sum(active_users) as active_users,
    sum(new_users) as new_users,
    sum(engaged_sessions) as engaged_sessions,
    sum(event_count) as event_count,
    sum(key_events) as key_events
from v_raw_ga4_hostname_audit
group by hostname_class, hostname
order by active_users desc nulls last;