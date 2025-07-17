with channels as (
    select distinct 'lobelia4cosmetics' as channel_name from {{ ref('stg_lobelia4cosmetics') }}
    union
    select distinct 'tikvahpharma' as channel_name from {{ ref('stg_tikvahpharma') }}
)
select
    row_number() over (order by channel_name) as channel_id,
    channel_name
from channels 