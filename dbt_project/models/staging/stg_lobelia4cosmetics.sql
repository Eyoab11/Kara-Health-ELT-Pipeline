with source as (
    select
        id,
        message_id,
        date,
        text,
        image_path,
        raw_json
    from raw.lobelia4cosmetics
)
select
    id as staging_id,
    message_id,
    date::timestamp as message_date,
    text,
    image_path,
    raw_json
from source 