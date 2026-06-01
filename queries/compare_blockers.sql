select
    url,
    primary_query,
    impressions,
    estimated_click_uplift,
    status,
    error
from v_compare_blockers
order by impressions desc nulls last;