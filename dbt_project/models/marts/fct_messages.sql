with stg as (
    select *, 'lobelia4cosmetics' as channel_name from {{ ref('stg_lobelia4cosmetics') }}
    union all
    select *, 'tikvahpharma' as channel_name from {{ ref('stg_tikvahpharma') }}
),
channels as (
    select * from {{ ref('dim_channels') }}
),
dates as (
    select * from {{ ref('dim_dates') }}
),
joined as (
    select
        stg.message_id,
        ch.channel_id,
        dt.date_id,
        stg.text,
        stg.image_path,
        stg.message_date,
        stg.raw_json
    from stg
    left join channels ch on stg.channel_name = ch.channel_name
    left join dates dt on stg.message_date::date = dt.date
)
select
    message_id,
    channel_id,
    date_id,
    length(text) as message_length,
    case when image_path is not null and image_path != '' then true else false end as has_image,
    message_date,
    raw_json
from joined 