# from exceptions.exception import AppException
# from utils.logger import get_logger
# from utils.visual_debugger import overlay_filled_contours, show_scaled
# from app.runner import Runner

# def main():
#     logger = get_logger("Main")
#     try:
#         logger.info("------Application started.------")
#         runner = Runner()
#         runner.run()
#         logger.info("------Application finished successfully.------")
#     except AppException as e:
#        logger.error(f"{e}")
#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
    

# if __name__ == "__main__":
#     main()


import argparse
from exceptions.exception import AppException
from utils.logger import get_logger
from app.runner import Runner

def parse_args():
    parser = argparse.ArgumentParser(description="Roller Inspection Controller")

    parser.add_argument(
        "-picamera",
        action="store_true",
        help="Use Picamera as grabber"
    )
    parser.add_argument(
        "-camera",
        action="store_true",
        help="Use USB camera as grabber"
    )
    parser.add_argument(
        "-file",
        action="store_true",
        help="Use file grabber"
    )

    return parser.parse_args()


def main():
    logger = get_logger("Main")
    args = parse_args()

    logger.info("------ Application started ------")

    try:
        runner = Runner(args)   # pass CLI arguments into Runner
        runner.run()

    except AppException as e:
        logger.error(f"{e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("------ Application terminated ------")


if __name__ == "__main__":
    main()
