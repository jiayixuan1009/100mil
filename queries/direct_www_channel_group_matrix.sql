with base as (
    select
        hostname,
        landing_page_query,
        default_channel_group,
        sessions,
        active_users,
        case
            when landing_page_query in ('(not set)', '/', '/en', '/zh') then 'home_or_not_set'
            when landing_page_query like '/login%' or landing_page_query like '/en/login%' or landing_page_query like '/zh/login%' then 'login'
            when landing_page_query like '/download%' or landing_page_query like '/en/download%' or landing_page_query like '/zh/download%' then 'download'
            when landing_page_query like '/compare%' or landing_page_query like '/en/compare%' or landing_page_query like '/zh/compare%' then 'compare'
            when landing_page_query like '/converter%' or landing_page_query like '/en/converter%' or landing_page_query like '/zh/converter%' then 'converter'
            when landing_page_query like '/sendmoney%' or landing_page_query like '/en/sendmoney%' or landing_page_query like '/zh/sendmoney%' then 'sendmoney'
            when landing_page_query like '/blogdetail%' or landing_page_query like '/en/blogdetail%' or landing_page_query like '/zh/blogdetail%' then 'blogdetail'
            when landing_page_query like '/swift%' or landing_page_query like '/en/swift%' or landing_page_query like '/zh/swift%' then 'swift'
            when landing_page_query like '/stock%' or landing_page_query like '/en/stock%' or landing_page_query like '/zh/stock%' then 'stock'
            when landing_page_query like '/announcement%' or landing_page_query like '/en/announcement%' or landing_page_query like '/zh/announcement%' then 'announcement'
            when landing_page_query like '/register%' or landing_page_query like '/en/register%' or landing_page_query like '/zh/register%' then 'register'
            else 'other'
        end as path_group
    from v_cross_ga4_3host_landing_channel
    where hostname = 'www.biyapay.com'
)
select
    path_group,
    default_channel_group,
    round(sum(sessions), 2) as sessions,
    round(sum(active_users), 2) as active_users
from base
group by 1, 2
having sum(sessions) >= 1000
order by sessions desc;
