from modules.data_collector import DataCollector
from modules.risk_calculator import RiskCalculator
from modules.alert_system import AlertSystem
from modules.disaster_recovery import DisasterRecoveryManager
import schedule
import time

def initialize_system():
    dr_manager = DisasterRecoveryManager()
    collector = DataCollector(dr_manager)
    calculator = RiskCalculator()
    alerter = AlertSystem()
    return dr_manager, collector, calculator, alerter

def run_monitoring_cycle():
    dr, collector, calculator, alerter = initialize_system()
    market_data = collector.collect_market_data()
    sentiment_data = collector.collect_sentiment_data()
    risk_score = calculator.calculate_risk_score(market_data, sentiment_data)
    if risk_score['level'] >= 40:
        alerter.send_alert(risk_score)
    print("✅ Monitoring cycle complete")

def main():
    print("🚀 Starting Strategic Risk Monitoring System")
    schedule.every(1).minutes.do(run_monitoring_cycle)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()