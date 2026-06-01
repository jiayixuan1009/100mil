select
    host,
    category,
    count(*) as urls,
    sum(gsc_impressions_16m) as impressions_16m,
    sum(gsc_clicks_16m) as clicks_16m,
    sum(case when overlap_with_other_host is not null and overlap_with_other_host <> '' then 1 else 0 end) as overlap_urls,
    sum(case when recommend_d2_action = 'pending' then 1 else 0 end) as pending_urls
from v_raw_cross_stock_mapping
group by host, category
order by impressions_16m desc nulls last;