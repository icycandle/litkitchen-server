import threading
import time


class SystemState:
    # Simple state machine for demo
    state = "idle"  # idle, param1, param2, param3, printing, done
    last_action_time = time.time()
    lock = threading.Lock()

    @classmethod
    def set_state(cls, new_state):
        with cls.lock:
            cls.state = new_state
            cls.last_action_time = time.time()

    @classmethod
    def get_state(cls):
        with cls.lock:
            return cls.state

    @classmethod
    def check_timeout_and_reset(cls, timeout=60):
        with cls.lock:
            if time.time() - cls.last_action_time > timeout:
                cls.state = "idle"
