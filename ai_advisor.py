import os
from typing import List
import requests
from datetime import datetime

class AIAdvisor:
    def __init__(self):
        """Initialize the AI Advisor.
        Currently using fallback suggestions, will be updated to use OpenAI/Claude."""
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    def get_suggestions(self, savings: float) -> str:
        """Get AI-powered suggestions for savings allocation."""
        return self._get_fallback_suggestions(savings)

    def _create_prompt(self, savings: float) -> str:
        """Create prompt for the LLM."""
        return f"""
        Given a savings amount of Rp {savings:,.0f}, suggest 3-4 specific ways to 
        allocate these savings. Consider:
        1. Bitcoin investment opportunities (with current BTC price)
        2. Travel plans (with specific destinations and ticket prices)
        3. Education savings
        4. Emergency fund
        Be specific with suggestions and include approximate prices and links.
        """

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