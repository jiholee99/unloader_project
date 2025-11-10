import cv2
from core.process.pre_process.image_pre_processor import ImagePreprocessor  # adjust import if needed
from exceptions.exception import AppException
from core.analysis.fullness_validator import FullnessValidator
from utils.logger import get_logger
from core.process.pre_process.image_pre_process_service import ImagePreprocessService
from core.process.post_process.image_post_processor_service import ImagePostProcessorService
from utils.visual_debugger import overlay_filled_contours, show_scaled
from utils.app_config_handler import AppConfigHandler
import json

def main():
    logger = get_logger()

    # 1️⃣ Load an image
    image_path = r"assets\test_images\full.jpeg"  # change to your image path
    # image_path = r"assets/test_images/full.jpeg"  # For Linux
    image = cv2.imread(image_path)

    if image is None:
        print("❌ Could not load image. Check the path.")
        return

    try:
        # Config options
        pre_process_options = AppConfigHandler.get_preprocess_options()
        post_process_options = AppConfigHandler.get_postprocess_options()
        judgement_options = AppConfigHandler.get_judgement_options()
        
        # Preprocess
        logger.info("Starting image preprocessing...")
        pre_process_service = ImagePreprocessService(options=pre_process_options)
        roi = AppConfigHandler.get_roi_settings()
        roi_coords = [roi["x"], roi["y"], roi["w"], roi["h"]]
        processed_mask = pre_process_service.process_image(image=image, roi_coords=roi_coords,)
        show_scaled(f"Processed Mask", processed_mask)
        logger.info("Image preprocessing completed.")

        # post-process
        logger.info("Starting image post-processing...")
        post_processor_service = ImagePostProcessorService(options=post_process_options)
        post_processed_img = post_processor_service.post_process(processed_mask)
        # post_processor_service.log_contour_info()
        show_scaled(f"Post Processed Mask", post_processed_img)
        logger.info("Image post-processing completed.")

        # Visual debug contours overlay
        from utils.visual_debugger import overlay_filled_contours
        blended_image = overlay_filled_contours(image=pre_process_service.get_roi_image(), contours=post_processor_service.get_contours())
        show_scaled(f"Contours using post processed image", blended_image)


        # 5️⃣ Validate distance using DistanceValidator
        validator = FullnessValidator()
        cutoff_point = judgement_options.get("fullness_cutoff", 0.5)  # example cutoff
        is_valid_fullness_pre = validator.is_valid(processed_mask, pre_process_options.get("threshold", 0), cutoff_point)
        is_valid_fullness_post = validator.is_valid(post_processed_img, pre_process_options.get("threshold", 0), cutoff_point)
        print(f"✅ Fullness Valid (Pre-processed): {is_valid_fullness_pre}")
        print(f"✅ Fullness Valid (Post-processed): {is_valid_fullness_post}")

    except AppException as e:
        get_logger().error(f"{e}")

    print("Press any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

