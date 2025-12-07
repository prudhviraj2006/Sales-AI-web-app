import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import OpenAI

logger = logging.getLogger(__name__)


class ChatService:
    """AI-powered chat service for sales forecasting insights"""
    
    def __init__(self, forecast_data: Dict = None):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            logger.warning("OPENROUTER_API_KEY not set")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.io/api/v1"
        )
        self.model = "openai/gpt-4-turbo"
        self.forecast_data = forecast_data or {}
        self.conversation_history = []
    
    def _build_context(self) -> str:
        """Build context from forecast data"""
        context = "You are an AI Sales Forecasting Assistant. "
        
        if self.forecast_data:
            metrics = self.forecast_data.get('metrics', {})
            forecast = self.forecast_data.get('forecast', [])
            historical = self.forecast_data.get('historical', [])
            
            context += f"""Current Forecast Data:
- Model Type: {self.forecast_data.get('model_type', 'Prophet')}
- MAPE (Accuracy): {metrics.get('mape', 'N/A')}%
- Confidence Score: {metrics.get('confidence_score', 'N/A')}%
- Risk Level: {metrics.get('risk_level', 'N/A')}
- Total Forecast Points: {len(forecast)}
- Historical Data Points: {len(historical)}

When answering questions, reference this data and provide specific insights. Be concise and actionable."""
        
        return context
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Send a message and get AI response
        
        Args:
            user_message: User's message
            conversation_history: Previous messages for context
        
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Build context
            context = self._build_context()
            
            # Prepare messages
            messages = []
            
            # Add system message with context
            messages.append({
                "role": "system",
                "content": context
            })
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenRouter API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'success': True,
                'response': ai_response,
                'timestamp': datetime.now().isoformat(),
                'model': self.model,
                'tokens_used': 0
            }
        
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to get response: {str(e)}",
                'response': "Sorry, I encountered an error. Please try again."
            }
    
    def generate_insights_from_query(self, question: str, forecast_data: Dict) -> str:
        """Generate specific insights based on question"""
        self.forecast_data = forecast_data
        
        queries = {
            'forecast': 'What is the forecast trend for the next period?',
            'growth': 'What is the growth rate trend?',
            'seasonal': 'Explain the seasonal patterns in the data',
            'anomaly': 'Are there any anomalies in the data?',
            'product': 'Which products are performing best?',
            'region': 'How are different regions performing?'
        }
        
        # Map question to query type
        query_type = 'forecast'
        for key, pattern in queries.items():
            if any(word in question.lower() for word in key.split()):
                query_type = key
                break
        
        response = self.chat(question)
        return response.get('response', '')
