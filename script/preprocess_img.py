import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
from src import init_app, db
from src.model.fish_img_model import FishImg
from src.services.fish_service import FishService
app = init_app()
RAW_DATA_DIR = "static/raw_data/"
with app.app_context():
    # Clear existing data (optional)
    FishImg.query.delete()

    for filename in os.listdir(RAW_DATA_DIR):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(RAW_DATA_DIR, filename)
            image = cv2.imread(img_path)
            if image is None:
                continue

            # Resize and extract features on-the-fly
            color_hist, hu_mom, lbp_hist = FishService.extract_features(image)

            # Save raw image path and features to the database
            fish_img = FishImg(
                image_path=img_path,
                color_histogram=color_hist,
                hu_moments=hu_mom,
                lbd=lbp_hist
            )
            db.session.add(fish_img)

    db.session.commit()
    print("Database populated with raw fish images and features.")