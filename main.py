import cv2
from core.process.pre_process.image_pre_processor import ImagePreprocessor  # adjust import if needed
from exceptions.exception import AppException
from core.analysis.distance_validator import DistanceValidator
from utils.logger import get_logger
from core.process.pre_process.image_pre_process_service import ImagePreprocessService
from core.process.post_process.image_post_processor_service import ImagePostProcessorService
from utils.visual_debugger import overlay_filled_contours, show_scaled
from utils.app_config_handler import AppConfigHandler

def get_roi_coordinates(file_path="config/roi_settings.yaml"):
    """read from yaml"""
    with open(file_path, 'r') as f:
        import yaml
        config = yaml.safe_load(f)
        roi = config.get('roller_roi', {})
        x = roi.get('x', 0)
        y = roi.get('y', 0)
        w = roi.get('w', 100)
        h = roi.get('h', 100)
        return x, y, w, h

def main():
    preprocessor = ImagePreprocessor()

    # 1️⃣ Load an image
    image_path = r"assets\test_images\full.jpeg"  # change to your image path
    image = cv2.imread(image_path)

    if image is None:
        print("❌ Could not load image. Check the path.")
        return

    # show_scaled("Original", image)

    try:
        

        # Preprocess
        # Get ROI , apply threshold and returns mask
        service = ImagePreprocessService()
        preprocessor_config = AppConfigHandler.get_preprocess_options()
        x, y, w, h = get_roi_coordinates()
        roi_coords = [x, y, w, h]
        threshold_value = preprocessor_config.get("threshold", 10)
        processed_mask = service.process_image(image=image, roi_coords=roi_coords, threshold=threshold_value)
        show_scaled(f"Processed Mask (>{threshold_value})", processed_mask)

        # post-process
        post_processor = ImagePostProcessorService()
        post_processed_img = post_processor.post_process(processed_mask)

        show_scaled(f"Post Processed Mask", post_processed_img)

        from utils.visual_debugger import overlay_filled_contours
        blended_image = overlay_filled_contours(image=service.get_roi_image(), contours=post_processor.get_contours())
        show_scaled(f"Overlay: Filled Contours", blended_image)

        # 5️⃣ Validate distance using DistanceValidator
        validator = DistanceValidator()
        roi_coords = [0, 0, w, h]  # since we cropped, ROI is the whole cropped image
        cutoff_point = 0.5  # example cutoff
        is_valid_distance = validator.is_valid(post_processed_img, roi_coords, threshold_value, cutoff_point)
        print(f"✅ Distance Valid: {is_valid_distance}")

        

    except AppException as e:
        get_logger().error(f"{e}")

    print("Press any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

