from model.contour import Contour

class PrettyPrint:
    @staticmethod
    def printContourInfos(contours : list[Contour]):
        result = ""
        sorted_contours = sorted(contours, reverse=True)
        for contour in sorted_contours:
            result += repr(contour) + "\n\n"
        return result