import cv2
import numpy as np
from flask import request, jsonify
from src.services.fish_service import FishService
class FishControler:
    @staticmethod
    def search_similar_images(file):
        if not file:
            return jsonify({"error" : "No image provided"}), 400

        # Read and preprocess img
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        query_image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if query_image is None:
            return jsonify({"error" : "Invalid image"}), 400
        # Search for similar images
        top_matches = FishService.search_similar_images(query_image)
        return jsonify({"matches": top_matches})
