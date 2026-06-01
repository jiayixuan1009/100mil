select
    category,
    channel,
    count(*) as tested_queries,
    sum(case when cited_biyapay = 'Y' then 1 else 0 end) as cited_queries,
    round(100.0 * sum(case when cited_biyapay = 'Y' then 1 else 0 end) / nullif(count(*), 0), 2) as citation_rate_pct,
    avg(biyapay_position) as avg_biyapay_position
from v_raw_ai_search_baseline
group by category, channel
order by citation_rate_pct asc, tested_queries desc;