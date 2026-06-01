with channel as (
    select
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
        end as path_group,
        default_channel_group,
        sum(sessions) as sessions
    from v_cross_ga4_3host_landing_channel
    where hostname = 'www.biyapay.com'
    group by 1, 2
), grouped as (
    select
        case
            when path_group in ('login', 'download', 'register')
                then 'exclude_lifecycle_paths'
            when path_group = 'home_or_not_set'
              and default_channel_group in ('Unassigned', 'Referral', 'Organic Social')
                then 'exclude_home_unassigned_or_nonclean'
            when path_group = 'announcement'
              and default_channel_group in ('Direct', 'Unassigned')
                then 'exclude_promo_announcement'
            when path_group in ('compare', 'converter', 'sendmoney')
              and default_channel_group = 'Direct'
                then 'hold_tool_intent_direct'
            when path_group in ('swift', 'blogdetail', 'stock', 'other')
              and default_channel_group = 'Direct'
                then 'hold_content_tool_direct'
            when path_group = 'home_or_not_set'
              and default_channel_group = 'Direct'
                then 'keep_home_direct_candidate'
            else 'review_with_more_source_detail'
        end as action_bucket,
        sessions
    from channel
)
select
    action_bucket,
    round(sum(sessions), 2) as sessions
from grouped
group by 1
order by sessions desc;
