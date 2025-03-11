import os
from typing import List
import requests

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
        Given a savings amount of ${savings:,.2f}, suggest 3-4 ways to allocate 
        these savings across different investment options and goals. Consider:
        1. Investment opportunities (stocks, crypto, etc.)
        2. Travel plans
        3. Education savings
        4. Emergency fund
        Be specific with suggestions and approximate allocations.
        """

    def _format_suggestions(self, raw_suggestions: str) -> str:
        """Format the AI response into a readable format."""
        formatted = "Here are some suggestions for allocating your savings:\n\n"
        formatted += raw_suggestions
        return formatted

    def _get_fallback_suggestions(self, savings: float) -> str:
        """Provide basic suggestions when API is not available."""
        suggestions = f"""
        Here are some general suggestions for your ${savings:,.2f} savings:

        1. Emergency Fund (40%): ${savings * 0.4:,.2f}
           - Keep this in a high-yield savings account

        2. Investment (30%): ${savings * 0.3:,.2f}
           - Consider low-cost index funds or ETFs

        3. Short-term Goals (20%): ${savings * 0.2:,.2f}
           - Travel fund
           - Major purchases

        4. Education/Personal Development (10%): ${savings * 0.1:,.2f}
           - Online courses
           - Skills development
        """
        return suggestions