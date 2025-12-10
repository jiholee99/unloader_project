from exceptions.exception import RemoteCaptureException
from utils.logger import get_logger
from adapters.remote_capture import DirectConnector
from adapters.config import AppConfigAdapter
class RemoteCaptureService:
    def __init__(self, remote_capture_repository : DirectConnector):
        self.remote_capture_repository = remote_capture_repository
        self.logger = get_logger()

    def remote_capture(self) -> bool:
        try:
            self.remote_capture_repository.signal_to_slaves()
            return True
        except Exception as e:
            raise RemoteCaptureException("Something went wrong while remote capturing",e)