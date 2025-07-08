class DataCollector:
    def __init__(self, recovery):
        self.recovery = recovery

    def collect_market_data(self):
        return {
            'spy': 440.25,
            'vix': 21.45,
            'dxy': 102.3
        }

    def collect_sentiment_data(self):
        return {
            'reddit': -0.2,
            'twitter': -0.1,
            'news': -0.3
        }