from model.contour import Contour

class PrettyPrint:
    @staticmethod
    def printContourInfos(contours : list[Contour]):
        result = ""
        for contour in contours:
            result += repr(contour) + "\n"
        return result