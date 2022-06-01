from robonomicsinterface import RobonomicsInterface, Subscriber, SubEvent
from playsound import playsound
from scripts import create_qr
import multiprocessing
import websocket
import logging
import time
import json


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


def callback(datalog: list) -> None:
    logging.info(f"get data {datalog}")
    data = datalog[2]
    data_dict = json.loads(data)
    if 'blackmirror' in data_dict:
        create_qr(data_dict['blackmirror'])
        logging.info("playing a sound")
        playsound('play.wav')
    else:
        logging.info("wrong key")


logging.info("create subscriber")
my_thread = multiprocessing.Process(target=Subscriber, args=(interface, SubEvent.NewRecord, callback, list_of_devices,))
my_thread.start()


while True:
    try:
        try:
            logging.debug("checking list of devices")
            new_list_devices = interface.rws_list_devices("4GgRRojuoQwKCZP9wkB69ZxJY4JprmHtpzEzqJLjnqu4jk1r")
        except Exception as e:
            logging.info(f"get error {e}")
            pass
        time.sleep(10)
        if not my_thread.is_alive():
            my_thread = multiprocessing.Process(target=Subscriber,
                                                args=(interface, SubEvent.NewRecord, callback, list_of_devices,))
            my_thread.start()

        if len(new_list_devices) != len(list_of_devices):
            logging.info(f"update list of devices. new list length is {len(new_list_devices)}.")
            my_thread.terminate()
            my_thread = multiprocessing.Process(target=Subscriber, args=(interface, SubEvent.NewRecord, callback,
                                                                  new_list_devices,))
            my_thread.start()
            list_of_devices = new_list_devices
        else:
            continue
    except KeyboardInterrupt:
        logging.debug("get shutdown signal. Terminating.")
        my_thread.terminate()
        break
    except websocket.WebSocketConnectionClosedException as exs:
        try:
            logging.debug(f"get error {exs}")
            my_thread.terminate()
        except Exception as ex:
            logging.debug(ex)
        finally:
            my_thread = multiprocessing.Process(target=Subscriber,
                                                args=(interface, SubEvent.NewRecord, callback, list_of_devices,))
            my_thread.start()
    except Exception as e:
        logging.debug(f"global error - {e}")
        break
