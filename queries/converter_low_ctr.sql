select
    page_key,
    url,
    clicks,
    impressions,
    ctr,
    avg_position,
    top_queries
from v_converter_low_ctr
where impressions >= 1000
order by ctr asc, impressions desc;