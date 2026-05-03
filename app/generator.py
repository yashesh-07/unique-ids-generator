import time
import threading

class SnowflakeGenerator:
    def __init__(self, machine_id, epoch):
        self.machine_id = machine_id
        self.epoch = epoch
        
        # Bit lengths for each section
        self.machine_id_bits = 10
        self.sequence_bits = 12
        
        # Max values (using bit shifts)
        # Hint: -1 ^ (-1 << self.machine_id_bits)
        
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _get_timestamp(self):
        # Return current time in milliseconds
        return int(time.time() * 1000)

    def generate_id(self):
        with self.lock:
            timestamp = self._get_timestamp()

            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards! Rejecting requests.")
            
            if timestamp == self.last_timestamp:
                # Keep sequence within 12 bits (0-4095)
                self.sequence = (self.sequence + 1) & 0xFFF 
                
                # If sequence wraps back to 0, we've exhausted this millisecond
                if self.sequence == 0:
                    timestamp = self._wait_for_next_millis(self.last_timestamp)
            else:
                self.sequence = 0
            
            self.last_timestamp = timestamp

            generated_id = (
                (timestamp - self.epoch) << (self.machine_id_bits + self.sequence_bits) | 
                (self.machine_id << self.sequence_bits) | 
                self.sequence
            )
            
            return generated_id

    def _wait_for_next_millis(self, last_timestamp):
        """Busy-wait loop to wait for the clock to tick forward."""
        timestamp = self._get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_timestamp()
        return timestamp