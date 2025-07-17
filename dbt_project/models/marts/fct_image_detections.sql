with detections as (
    select
        message_id,
        image_path,
        detected_object_class,
        confidence_score,
        detection_timestamp
    from raw.image_detections
),
messages as (
    select
        message_id,
        channel_id,
        date_id
    from {{ ref('fct_messages') }}
)
select
    d.message_id,
    m.channel_id,
    m.date_id,
    d.detected_object_class,
    d.confidence_score,
    d.image_path,
    d.detection_timestamp
from detections d
left join messages m on d.message_id = m.message_id 