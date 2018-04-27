from datetime import time
from typing import List, Optional


class Arduino:
    def __init__(self, id: int, name: str, template_id: int):
        self.id = id
        self.name = name
        self.template_id = template_id


class Template:
    def __init__(self, id: int, name: str, nb_input_pins: int, nb_output_pins: int):
        self.id = id
        self.name = name
        self.nb_input_pins = nb_input_pins
        self.nb_output_pins = nb_output_pins


class OutputPin:
    def __init__(self, id: int, number: int, parent_id: int):
        self.parent_id = parent_id
        self.number = number
        self.id = id


class InputPin:
    def __init__(self, id: int, number: int, action_ids: List[int], parent_id: int, time_between_clicks: float):
        self.parent_id = parent_id
        self.action_ids = action_ids
        self.number = number
        self.time_between_clicks = time_between_clicks
        self.id = id


class Action:
    def __init__(self,
                 id: int,
                 action_type: int,
                 trigger_id: int,
                 notification_ids: List[int],
                 delay: int,
                 timer: int,
                 output_pin_ids: List[int],
                 condition_id: Optional[int],
                 master_id: Optional[int],
                 click_number: int,
                 dimmer_speed: Optional[int],
                 cancel_on_button_release: Optional[bool],
                 dimmer_light_value: Optional[int]):
        # General properties
        self.id = id
        self.trigger_id = trigger_id
        self.action_type = action_type
        self.delay = delay
        self.output_pin_ids = output_pin_ids
        self.notification_ids = notification_ids
        self.condition_id = condition_id
        self.click_number = click_number

        # ON/OFF/ON_DIMMER/OFF_DIMMER action
        self.timer = timer

        # TOGGLE/TOGGLE_DIMMER action
        self.master_id = master_id

        # DIMMER
        self.dimmer_speed = dimmer_speed
        self.cancel_on_button_release = cancel_on_button_release

        # ON_DIMMER/TOGGLE_DIMMER action
        self.dimmer_light_value = dimmer_light_value


class Trigger:
    def __init__(self, id: int, trigger_type: int, seconds_down: Optional[int]):
        self.id = id
        self.trigger_type = trigger_type
        self.seconds_down = seconds_down


class Condition:
    def __init__(self, id: int, type: int, operator: Optional[int], condition_ids: Optional[List[int]],
                 output_pin_id: Optional[int], status: Optional[bool], from_time: Optional[time],
                 to_time: Optional[time]):
        self.id = id
        self.type = type
        self.to_time = to_time
        self.from_time = from_time
        self.status = status
        self.output_pin_id = output_pin_id
        self.condition_ids = condition_ids
        self.operator = operator


class Notification:
    def __init__(self, id: int, message: str, notification_type: int, enabled: bool, subject: Optional[str],
                 mail_adress: List[str], tokens: List[str]):
        self.id = id
        self.notification_type = notification_type
        self.message = message
        self.enabled = enabled
        self.subject = subject
        self.emails = mail_adress
        self.tokens = tokens