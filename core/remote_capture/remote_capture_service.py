from exceptions.exception import RemoteCaptureException
from utils.logger import get_logger
from adapters.remote_capture import DirectConnector, UrlRequestor
from adapters.config import AppConfigAdapter
class RemoteCaptureService:
    def __init__(self, remote_capture_repository : UrlRequestor):
        self.remote_capture_repository = remote_capture_repository
        self.logger = get_logger("RemoteCaptureService")

    def remote_capture(self) -> bool:
        try:
            # request_photo_from_slaves has retry mechanism inside so if fails, it will raise exception
            result = self.remote_capture_repository.request_photos_from_slaves()
            if not result:
                raise RemoteCaptureException("Remote capture failed after retries.")
            return True
        except Exception as e:
            raise RemoteCaptureException("Something went wrong while remote capturing",e)