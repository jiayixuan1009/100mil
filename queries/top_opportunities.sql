select
    url,
    page_type,
    primary_query,
    opportunity_class,
    priority,
    impressions,
    ctr,
    avg_position,
    estimated_click_uplift,
    recommended_action
from v_top_gsc_opportunities
limit 50;