import cv2
import numpy as np
from skimage.feature import local_binary_pattern
from scipy.spatial.distance import euclidean
from src.model.fish_img_model import FishImg, db
import os

class FishService:
    TARGET_SIZE = (224, 224)

    @staticmethod
    def preprocess_image(image):
        """Preprocess an image by resizing it to the target size."""
        return cv2.resize(image, FishService.TARGET_SIZE, interpolation=cv2.INTER_AREA)

    @staticmethod
    def extract_color_histogram(image):
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        return hist.flatten()

    @staticmethod
    def extract_hu_moments(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        moments = cv2.HuMoments(cv2.moments(gray)).flatten()
        return moments

    @staticmethod
    def extract_lbp(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lbp = local_binary_pattern(gray, 8, 1, method='uniform')
        (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, 11), range=(0, 10))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-7)
        return hist

    @staticmethod
    def extract_features(image):
        image = FishService.preprocess_image(image)
        color_hist = FishService.extract_color_histogram(image)
        hu_mom = FishService.extract_hu_moments(image)
        lbp_hist = FishService.extract_lbp(image)
        return color_hist, hu_mom, lbp_hist

    @staticmethod
    def populate_database(image_dir):
        for filename in os.listdir(image_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(image_dir, filename)
                image = cv2.imread(img_path)
                if image is None:
                    continue

                color_hist, hu_mom, lbp_hist = FishService.extract_features(image)
                fish_img = FishImg(
                    raw_image_path=img_path,
                    color_histogram=color_hist,
                    hu_moments=hu_mom,
                    lbd=lbp_hist
                )
                db.session.add(fish_img)
        db.session.commit()

    @staticmethod
    def search_similar_images(query_image):
        query_image = FishService.preprocess_image(query_image)
        query_color_hist, query_hu_mom, query_lbp = FishService.extract_features(query_image)
        results = []

        for fish_img in FishImg.query.all():
            color_dist = euclidean(query_color_hist, fish_img.color_histogram)
            hu_dist = euclidean(query_hu_mom, fish_img.hu_moments)
            lbp_dist = euclidean(query_lbp, fish_img.lbd)

            total_dist = 0.4 * color_dist + 0.3 * hu_dist + 0.3 * lbp_dist
            results.append({"path": fish_img.image_path, "distance": total_dist})

        results.sort(key=lambda x: x["distance"])
        return results[:3]