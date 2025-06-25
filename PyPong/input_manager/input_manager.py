"""
Enhanced InputManager with unified chart and continuous/non-continuous tagging
"""

from typing import Set

class InputManager:
    def __init__(self) -> None:
        self.input_chart = {
            'discrete': {},
            'continuous': {},
            'touch': {},
        }

        self.pressed_keys: Set[int] = set()
        self.previous_keys: Set[int] = set()

        self.enabled = True

    def update_pressed_keys(self, pressed) -> None:
        """
            Update pressed key state using pygame.key.get_pressed()
            Only tracks keys that have continuous actions registered
        """
        self.previous_keys = self.pressed_keys.copy()

        continuous = self.input_chart.get('continuous', {})
        self.pressed_keys.clear()

        for key in continuous.keys():
            keys = key if isinstance(key, tuple) else (key,)
            self.pressed_keys.update(
                k for k in keys if isinstance(k, int) and pressed[k]
            )

    def handling_discrete_input(self, event) -> bool:

        if not self.enabled:
            return False

        discrete_chart = self.input_chart.get('discrete', {})
        if action := discrete_chart.get('default'):
            action()

        if event_type_action := discrete_chart.get(event.type):
            action = (
                event_type_action.get(getattr(event, 'key', None)) or
                event_type_action.get(getattr(event, 'ui_element', None))
            ) if isinstance(event_type_action, dict) else event_type_action

            if action:
                try:
                    action()
                    return True
                except Exception as e:
                    print(f"Error executing discrete action:{action} with error:{e}")
                    return False
        return False

    def handling_continuous_input(self):

        if not self.enabled:
            return

        continuous_chart = self.input_chart.get('continuous', {})
        if action := continuous_chart.get('default'):
            action()

        for key, action in continuous_chart.items():
            keys = key if isinstance(key, tuple) else (key,)
            if any(k in keys for k in self.pressed_keys):
                try:
                    action()
                except Exception as e:
                    print(f"Error executing continuous action '{action}': {e}")
                
        # for key in self.pressed_keys:
        #     if action := continuous_chart.get(key):
        #         try:
        #             action()
        #         except Exception as e:
        #             print(f"Error executing continuous action '{action}': {e}")

    def handling_touch_input(self, event) -> bool:

        if not self.enabled or event.type not in {1792, 1794, 1793}:
            return False

        touch_chart = self.input_chart.get('touch', {})
        event_type_chart = touch_chart.get(event.type, {})
        if action := touch_chart.get('default'):
            action()

        if callable(event_type_chart):
            event_type_chart(event)
        else:
            for item, action in event_type_chart.items():
                if callable(item):
                    try:
                        item()
                        return True
                    except Exception as e:
                        print(f"Error executing discrete action:{action} with error:{e}")
                        return False
            
                elif isinstance(item, tuple) and len(item) == 4:
                    x1, x2, y1, y2 = item 
                    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                        try:
                            action(event)
                            return True
                        except Exception as e:
                            print(f"Error executing discrete action:{action} with error:{e}")
                            return False
        return False


    def handle_input(self, events, keys) -> None:
        """
        Main input handling function that processes both discrete and continuous input
        This replaces your original handle_input function
        """
        # Handle discrete events from input_chart['discrete']
        for event in events:
            self.handling_discrete_input(event)
            self.handling_touch_input(event)
        
        # Handle continuous input from input_chart['continuous']
        self.update_pressed_keys(keys)
        self.handling_continuous_input()   
