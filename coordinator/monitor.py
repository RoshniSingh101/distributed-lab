class AvailabilityMonitor:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0

    def record(self, success: bool):
        self.total_requests += 1
        if success: 
            self.successful_requests += 1

    def get_uptime_percentage(self):
        if self.total_requests == 0: 
            return 100.0
        return (self.successful_requests / self.total_requests) * 100

    def get_sla_status(self):
        uptime = self.get_uptime_percentage()
        if uptime >= 99.99999: 
            return "5 Nines (Carrier Grade)"
        if uptime >= 99.999: 
            return "3 Nines (Standard)"
        return "Failing SLA"