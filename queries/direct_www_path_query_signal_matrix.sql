with base as (
    select
        page_location,
        sessions,
        active_users,
        regexp_extract(page_location, '^https?://[^/]+(/[^?#]*)', 1) as path,
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
            when path like '/zh/announcement%' or path like '/en/announcement%' then 'announcement'
            when path like '/en/register%' or path like '/zh/register%' or path like '/register%' then 'register'
            when path like '/zh/virtualcard%' or path like '/en/virtualcard%' then 'virtualcard'
            when path like '/zh/blogdetail%' or path like '/en/blogdetail%' then 'blogdetail'
            when path like '/zh/swift%' or path like '/en/swift%' then 'swift'
            when path like '/zh/stock%' or path like '/en/stock%' then 'stock'
            when path like '/zh/bank-code%' or path like '/en/bank-code%' then 'bank-code'
            when path like '/zh/iban%' or path like '/en/iban%' or path like '/iban%' then 'iban'
            when path like '/zh/sendmoney%' or path like '/en/sendmoney%' then 'sendmoney'
            when path like '/zh/compare%' or path like '/en/compare%' then 'compare'
            when path like '/zh/converter%' or path like '/en/converter%' then 'converter'
            when path like '/zh/%' then 'zh_other'
            when path like '/en/%' then 'en_other'
            else 'other'
        end as path_group,
        case
            when query_string = '' then 'no_query_string'
            when lower(query_string) like '%utm_%' then 'utm_campaign_or_source'
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
    path_group,
    query_bucket,
    round(sum(sessions), 2) as sessions,
    round(sum(active_users), 2) as active_users
from tagged
group by 1, 2
having sum(sessions) >= 1000
order by sessions desc;
