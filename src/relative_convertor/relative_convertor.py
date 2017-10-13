import src.irulez.log as log
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util
import lib.paho.mqtt.client as mqtt
import src.irulez.configuration as configuration
import src.irulez.factory as factory
import src.button.processors as button_processor
import src.relative_convertor.processors as relative_processor
import src.communication.mqtt_sender as mqtt_sender


logger = log.get_logger('absolute_update')

# Get database, MariaDB
logger.debug('Getting database')
db = src.irulez.db.get_maria_db()
factory = factory.ArduinoConfigFactory(db)

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
logger.debug('Creating arduinos')
arduinos = {}
for arduino in factory.create_arduino_config().arduinos:
    arduinos[arduino.name] = arduino

# Create client
client = mqtt.Client()

sender = mqtt_sender.MqttSender(client, arduinos)
update_processor = button_processor.RelayStatusProcessor(arduinos)
relative_action_processor =  relative_processor.RelativeActionProcessor(sender, arduinos)

def on_connect(client, userdata, flags, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/+/" + constants.statusTopic)
    client.subscribe(constants.arduinoTopic + "/+/" + constants.statusTopic)
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/+/" + constants.actionTopic + "/" + constants.relative)
    client.subscribe(constants.arduinoTopic + "/+/" + constants.actionTopic + "/" + constants.relative)


def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Find arduino name of topic
    if not (util.is_arduino_status_topic(msg.topic) or util.is_arduino_relative_action_topic(msg.topic)):
        logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")
        # Unknown topic
        return

    # Get the name of the arduino from the topic
    name = util.get_arduino_name_from_topic(msg.topic)

    # Check if the topic is a relay or button update.
    if util.is_arduino_status_topic(msg.topic):
        logger.debug(f"Update the relay status")
        update_processor.update_arduino_output_pins(name, msg.payload)
        return

    if util.is_arduino_relative_action_topic(msg.topic):
        logger.debug(f"Convert relative to absolute ")
        relative_action_processor.process_relative_action_message(name, msg.payload.decode("utf-8"))
        pass



# Set callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()

client.username_pw_set(mqttConfig['username'], mqttConfig['password'])
client.connect(mqttConfig['ip'], int(mqttConfig['port']), 60)

logger.info("Starting loop forever")
# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
