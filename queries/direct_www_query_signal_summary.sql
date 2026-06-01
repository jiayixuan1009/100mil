with base as (
    select
        page_location,
        sessions,
        active_users,
        case when page_location like '%?%' then split_part(page_location, '?', 2) else '' end as query_string
    from v_raw_ga4_page_location_events
    where hostname = 'www.biyapay.com'
      and page_location not in (
        'https://www.biyapay.com/',
        'https://www.biyapay.com/en',
        'https://www.biyapay.com/zh'
      )
      and page_location not like '%/login%'
      and page_location not like '%/download%'
), tagged as (
    select
        case
            when query_string = '' then 'no_query_string'
            when regexp_matches(lower(query_string), '(^|[?&])utm_[^=&]*=') then 'utm_campaign_or_source'
            when lower(query_string) like '%_channel_track_key=%' then 'channel_track_key'
            when lower(query_string) like '%height=44%' or lower(query_string) like '%language=zh-cn%' then 'webview_embed_params'
            when lower(query_string) like '%amount=%' then 'amount_param'
            when lower(query_string) like '%invite=%' then 'invite_param'
            else 'other_query_params'
        end as query_bucket,
        sessions,
        active_users
    from base
)
select
    query_bucket,
    round(sum(sessions), 2) as sessions,
    round(sum(active_users), 2) as active_users,
    count(*) as row_count
from tagged
group by 1
order by sessions desc;
