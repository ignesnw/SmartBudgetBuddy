import os
from typing import List
import requests
from datetime import datetime

class AIAdvisor:
    def __init__(self):
        # Using HuggingFace Inference API
        self.api_url = "https://api-inference.huggingface.co/models/facebook/opt-350m"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")

    def get_suggestions(self, savings: float) -> str:
        """Get AI-powered suggestions for savings allocation."""
        if not self.api_key:
            return self._get_fallback_suggestions(savings)

        headers = {"Authorization": f"Bearer {self.api_key}"}
        prompt = self._create_prompt(savings)

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json={"inputs": prompt}
            )

            if response.status_code == 200:
                suggestions = response.json()[0]["generated_text"]
                return self._format_suggestions(suggestions)
            else:
                return self._get_fallback_suggestions(savings)

        except Exception as e:
            return f"Unable to generate suggestions at the moment. Error: {str(e)}"

    def _create_prompt(self, savings: float) -> str:
        return f"""
        Given a savings amount of Rp {savings:,.0f}, suggest 3-4 specific ways to 
        allocate these savings. Consider:
        1. Bitcoin investment opportunities (with current BTC price)
        2. Travel plans (with specific destinations and ticket prices)
        3. Education savings
        4. Emergency fund
        Be specific with suggestions and include approximate prices and links.
        """

    def _format_suggestions(self, raw_suggestions: str) -> str:
        """Format the AI response into a readable format."""
        formatted = "Here are some suggestions for allocating your savings:\n\n"
        formatted += raw_suggestions
        return formatted

    def _get_fallback_suggestions(self, savings: float) -> str:
        """Provide detailed suggestions when API is not available."""
        current_month = datetime.now().strftime("%B %Y")
        suggestions = f"""
        Here are some specific suggestions for your Rp {savings:,.0f} savings for {current_month}:

        1. Bitcoin Investment (30%): Rp {savings * 0.3:,.0f}
           - Current BTC Price: ~Rp 900,000,000 per BTC
           - You could buy approximately {(savings * 0.3 / 900000000):,.5f} BTC
           - Consider using Indodax: https://indodax.com/market/BTCIDR

        2. Travel Fund (40%): Rp {savings * 0.4:,.0f}
           - One-way ticket to Singapore: ~Rp 1,300,000
           - Book through:
             • Traveloka: https://www.traveloka.com
             • Booking.com: https://www.booking.com

        3. Emergency Fund (20%): Rp {savings * 0.2:,.0f}
           - Keep in high-yield savings account
           - Consider digital banks like Jenius or TMRW

        4. Education/Personal Development (10%): Rp {savings * 0.1:,.0f}
           - Online courses (Udemy/Coursera)
           - Professional certification
        """
        return suggestions