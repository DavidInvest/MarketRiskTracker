class RiskCalculator:
    def calculate_risk_score(self, market_data, sentiment_data):
        vix_score = (market_data['vix'] - 15) * 2
        sentiment_score = (1 - (sentiment_data['reddit'] + sentiment_data['twitter'] + sentiment_data['news']) / 3) * 25
        raw_score = vix_score + sentiment_score
        score = min(100, max(0, raw_score))
        level = "LOW"
        if score >= 80:
            level = "RED"
        elif score >= 60:
            level = "ORANGE"
        elif score >= 40:
            level = "YELLOW"
        return {
            'value': round(score, 2),
            'level': level
        }