import logging
import qrcode


def create_qr(word: str) -> str:
    """
    :param word: word, inside QR
    :type word: str
    :return: full filename of a resulted qr-code
    :rtype: str
    This is a qr-creating submodule.
    """

    logging.info("start creating QR")
    logging.debug(f"create QR with word - {word} ")
    qr_big: qrcode.QRCode = qrcode.QRCode(version=8, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_big.add_data(word)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert(
        "RGB"
    )  # some standard code to create qr-code with a python lib

    logging.info("save QR")
    qrpic: str = "qr/qr.png"
    logging.debug(f"save QR. Find here {qrpic}")
    img_qr_big.save(qrpic)  # saving picture for further printing with a timestamp
    return qrpic


if __name__ == '__main__':
    create_qr("text")