with targets as (
    select
        url,
        regexp_replace(url, '\\?.*$', '') as base_url,
        primary_query,
        impressions,
        estimated_click_uplift
    from docs_phase2_compare_top30_live_health
)
select
    targets.url,
    targets.primary_query,
    targets.impressions,
    targets.estimated_click_uplift,
    count(inlinks.Source) as inlink_rows,
    count(distinct inlinks.Source) as source_urls,
    count(distinct inlinks.Anchor) as anchor_variants
from targets
left join v_large_pattern_inlinks inlinks
    on inlinks.Destination = targets.base_url
    or inlinks.Destination like targets.base_url || '?%'
group by 1,2,3,4
order by cast(nullif(targets.impressions, '') as double) desc nulls last;