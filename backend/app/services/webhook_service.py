import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for sending webhook notifications"""

    def __init__(self):
        self.timeout = 10.0  # 10 seconds timeout

    async def send_webhook(
        self,
        url: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None
    ) -> bool:
        """
        Send webhook to external URL.
        
        Args:
            url: Webhook URL
            data: Data to send
            headers: Optional custom headers
            
        Returns:
            True if successful, False otherwise
        """
        try:
            default_headers = {"Content-Type": "application/json"}
            if headers:
                default_headers.update(headers)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=data,
                    headers=default_headers
                )
                
                response.raise_for_status()
                logger.info(f"Webhook sent successfully to {url}: {response.status_code}")
                return True

        except httpx.HTTPStatusError as e:
            logger.error(f"Webhook failed with status {e.response.status_code}: {url}")
            return False
        except httpx.RequestError as e:
            logger.error(f"Webhook request failed: {url} - {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending webhook to {url}: {e}")
            return False

    async def notify_new_subscriber(
        self,
        subscriber_id: str,
        email: str,
        name: str
    ) -> bool:
        """
        Notify N8N about new verified subscriber.
        
        Args:
            subscriber_id: Subscriber UUID
            email: Subscriber email
            name: Subscriber name
            
        Returns:
            True if webhook sent successfully
        """
        # Check if N8N webhook URL is configured
        n8n_webhook_url = getattr(settings, 'N8N_WEBHOOK_NEW_SUBSCRIBER', None)
        
        if not n8n_webhook_url:
            logger.warning("N8N_WEBHOOK_NEW_SUBSCRIBER not configured, skipping webhook")
            return False

        data = {
            "event": "subscriber.verified",
            "subscriber": {
                "id": subscriber_id,
                "email": email,
                "name": name
            }
        }

        return await self.send_webhook(n8n_webhook_url, data)


# Singleton instance
webhook_service = WebhookService()

