with base as (
    select
        hostname,
        page_location,
        sessions,
        active_users,
        event_count,
        case
            when hostname in ('active.biyagl.com', 'www.biyapays.com', 'www.biyaglobal.com', 'prv.biyanews.com')
              or hostname like 'prv.%'
              or hostname in ('localhost', '192.168.110.190', '47.242.151.151')
                then 'exclude_non_prod_or_external_host'
            when hostname in ('cn.biyapay.com', 'biyapay.com')
                then 'separate_or_migrate_legacy_cn_host'
            when hostname = 'signup.biyapay.com' and (page_location like '%/download%' or page_location like '%/fastreg%')
                then 'separate_signup_download_or_fastreg'
            when hostname = 'signup.biyapay.com'
                then 'fix_signup_cross_domain_or_not_set'
            when hostname = 'invest.biyapay.com' and (
                page_location like '%/404%'
                or page_location like '%/login%'
                or page_location like '%/download%'
                or page_location like '%assets?accountType=%'
            )
                then 'separate_invest_auth_404_download'
            when hostname = 'invest.biyapay.com'
                then 'review_invest_product_traffic'
            when hostname = 'news.biyapay.com'
                then 'review_news_subdomain_direct'
            when hostname = 'www.biyapay.com' and (
                page_location like '%/login%'
                or page_location like '%/download%'
                or page_location like '%(not set)%'
            )
                then 'separate_www_auth_download_measurement'
            when hostname = 'www.biyapay.com' and page_location in (
                'https://www.biyapay.com/',
                'https://www.biyapay.com/en',
                'https://www.biyapay.com/zh'
            )
                then 'keep_core_home_brand_direct'
            when hostname = 'www.biyapay.com'
                then 'review_www_content_or_tool_direct'
            else 'other_review'
        end as priority_bucket
    from v_raw_ga4_page_location_events
)
select
    priority_bucket,
    round(sum(sessions), 2) as sessions,
    round(sum(active_users), 2) as active_users,
    round(sum(event_count), 2) as event_count,
    count(*) as row_count
from base
group by 1
order by sessions desc;
