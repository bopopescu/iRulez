import src.irulez.util as util
import src.irulez.constants as constants
import src.irulez.log as log

logger = log.get_logger('mqtt_sender')


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_action(self, absolute):
        for name in absolute:
            payload = util.convert_array_to_hex(absolute[name])
            topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
            logger.debug(f"Publishing: '{topic}'/'{payload}'")
            self.client.publish(topic, payload)

    def send_absolute_update(self, on_pins: {}, off_pins: {}):
        # TODO: improve 'send_update' mechanism to only send updates to arduinos with updates.
        #  Current implementation sends updates to all arduinos or none.
        send_update = False
        absolute = {}
        for name in on_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                # Continue means hop to the next cycle of the for loop
                continue
            absolute[name] = [False] * arduino.number_of_relay_pins
            for pin in arduino.relay_pins.values():
                absolute[name][pin.number] = pin.state
                if on_pins[name][pin.number] and not pin.state:
                    send_update = True
                    absolute[name][pin.number] = True

        for name in off_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                return
            if name not in absolute.keys():
                absolute[name] = [False] * arduino.number_of_relay_pins
            for pin in arduino.relay_pins.values():
                absolute[name][pin.number] = pin.state
                if off_pins[name][pin.number] and pin.state:
                    absolute[name][pin.number] = False
                    send_update = True

        if send_update:
            self.publish_action(absolute)
        else:
            logger.info("No change to publish")

    def send_relative_update(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        on_pins = {}
        off_pins = {}

        for name in pins_to_switch_on:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                return
            on_pins[name] = [False] * arduino.number_of_relay_pins
            for pin in pins_to_switch_on[name]:
                on_pins[name][pin] = True

        for name in pins_to_switch_off:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                return
            off_pins[name] = [False] * arduino.number_of_relay_pins
            for pin in pins_to_switch_off[name]:
                off_pins[name][pin] = True

        self.send_absolute_update(on_pins, off_pins)
