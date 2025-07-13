# YOLOv8 object detection logic for Task 3 will go here.
def run_enrichment():
    print("Running data enrichment with YOLO...")
    # 1. Scan for new images in the data lake.
    # 2. Load the YOLOv8 model.
    # 3. Process each image and detect objects.
    # 4. Prepare detection results (e.g., message_id, class, score).
    # 5. Load results into the fct_image_detections table in PostgreSQL.
    print("Data enrichment complete.")

if __name__ == "__main__":
    run_enrichment()