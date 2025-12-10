from exceptions.exception import RemoteCaptureException
from utils.logger import get_logger

class RemoteCaptureService:
    def __init__(self, remote_capture_repository):
        self.remote_capture_repository = remote_capture_repository
        self.logger = get_logger()

    def remote_capture(self) -> bool:
        raise RemoteCaptureException("Remote capture service is not implemented yet.")