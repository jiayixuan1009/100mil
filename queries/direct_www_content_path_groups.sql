with base as (
    select
        page_location,
        sessions,
        active_users,
        regexp_extract(page_location, '^https?://[^/]+(/[^?#]*)', 1) as path
    from v_raw_ga4_page_location_events
    where hostname = 'www.biyapay.com'
      and page_location not in (
        'https://www.biyapay.com/',
        'https://www.biyapay.com/en',
        'https://www.biyapay.com/zh'
      )
      and page_location not like '%/login%'
      and page_location not like '%/download%'
), grouped as (
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
        sessions,
        active_users
    from base
)
select
    path_group,
    round(sum(sessions), 2) as sessions,
    round(sum(active_users), 2) as active_users,
    count(*) as row_count
from grouped
group by 1
order by sessions desc;with base as (
    select
        page_location,
        sessions,
        active_users,
        regexp_extract(page_location, '^https?://[^/]+(/[^?#]*)', 1) as path
    from v_raw_ga4_page_location_events
    where hostname = 'www.biyapay.com'
      and page_location not in (
        'https://www.biyapay.com/',
        'https://www.biyapay.com/en',
        'https://www.biyapay.com/zh'
      )
      and page_location not like '%/login%'
      and page_location not like '%/download%'
), grouped as (
    select
        case
            when path like '/zh/announcement%' or path like '/en/announcement%'
                then 'announcement'
            when path like '/en/register%' or path like '/zh/register%' or path like '/register%'
                then 'register'
            when path like '/zh/virtualcard%' or path like '/en/virtualcard%'
                then 'virtualcard'
            when path like '/zh/blogdetail%' or path like '/en/blogdetail%'
                then 'blogdetail'
            when path like '/zh/swift%' or path like '/en/swift%'
                then 'swift'
            when path like '/zh/stock%' or path like '/en/stock%'
                then 'stock'
            when path like '/zh/bank-code%' or path like '/en/bank-code%'
                then 'bank-code'
            when path like '/zh/iban%' or path like '/en/iban%' or path like '/iban%'
                then 'iban'
            when path like '/zh/sendmoney%' or path like '/en/sendmoney%'
                then 'sendmoney'
            when path like '/zh/compare%' or path like '/en/compare%'
                then 'compare'
            when path like '/zh/converter%' or path like '/en/converter%'
                then 'converter'
            when path like '/zh/%'
                then 'zh_other'
            when path like '/en/%'
                then 'en_other'
            else 'other'
        end as path_group,
        sessions,
        active_users
    from base
)
select
    path_group,
    round(sum(sessions), 2) as sessions,
    round(sum(active_users), 2) as active_users,
    count(*) as rows
from grouped
group by 1
order by sessions desc;