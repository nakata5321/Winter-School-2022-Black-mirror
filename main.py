from robonomicsinterface import RobonomicsInterface, Subscriber, SubEvent
from scripts import create_qr
from PIL import Image
import threading
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


logging.info("initializing interface")
interface: RobonomicsInterface = RobonomicsInterface()
list_of_devices: list = []
logging.info("get list of devices")
list_of_devices = interface.rws_list_devices("4GgRRojuoQwKCZP9wkB69ZxJY4JprmHtpzEzqJLjnqu4jk1r")
logging.info(f" len is {len(list_of_devices)}")
logging.info("open image")
im = Image.open("./qr/qr.png")
im.show()


def callback(data: list) -> None:
    logging.info(f"get data {data}")
    create_qr(data[2])


logging.info("create subscriber")
my_thread = threading.Thread(target=Subscriber, args=(interface, SubEvent.NewRecord, callback, list_of_devices,))
my_thread.start()


while True:
    try:
        logging.debug("checking list of devices")
        new_list_devices = interface.rws_list_devices("4GgRRojuoQwKCZP9wkB69ZxJY4JprmHtpzEzqJLjnqu4jk1r")
        time.sleep(10)
        if len(new_list_devices) != len(list_of_devices):
            logging.info(f"update list of devices. new list length is {len(new_list_devices)}.")
            my_thread.join()
            my_thread = threading.Thread(target=Subscriber, args=(interface, SubEvent.NewRecord, callback,
                                                                  new_list_devices,))
            my_thread.start()
            list_of_devices = new_list_devices
        else:
            continue
    except KeyboardInterrupt:
        logging.debug("get shutdown signal. Terminating.")
        my_thread.join()
        im.close()
        break
