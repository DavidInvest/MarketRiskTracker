class DisasterRecoveryManager:
    def __init__(self):
        pass

    def fallback(self, service_name):
        print(f"[Failover] Switching to fallback for {service_name}")