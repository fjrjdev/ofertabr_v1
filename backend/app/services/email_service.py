"""
Email service using Brevo (Sendinblue)
"""
import logging
from pathlib import Path

import sib_api_v3_sdk
from jinja2 import Environment, FileSystemLoader
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Brevo"""

    def __init__(self):
        # Limpa a API key de espaços extras
        api_key = settings.BREVO_API_KEY.strip() if settings.BREVO_API_KEY else ""

        if not api_key:
            logger.error("BREVO_API_KEY não está configurada")

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        template_dir = Path(__file__).parent.parent / 'templates' / 'emails'
        self.template_env = Environment(loader=FileSystemLoader(str(template_dir)))

    async def send_newsletter(
        self,
        to_email: str,
        to_name: str,
        newsletter_title: str,
        newsletter_content: str,
        subscriber_id: str
    ) -> bool:
        """
        Send a newsletter to a subscriber.
        
        Args:
            to_email: Recipient email
            to_name: Recipient name
            newsletter_title: Newsletter title
            newsletter_content: Newsletter HTML content
            subscriber_id: Subscriber ID (for unsubscribe link)
            
        Returns:
            True if sent successfully
        """
        try:
            unsubscribe_url = f"{settings.FRONTEND_URL}/unsubscribe/{subscriber_id}"

            template = self.template_env.get_template('newsletter.html')
            html_content = template.render(
                title=newsletter_title,
                content=newsletter_content,
                unsubscribe_url=unsubscribe_url,
                to_name=to_name
            )

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email, "name": to_name}],
                sender={"email": settings.EMAIL_FROM, "name": settings.EMAIL_FROM_NAME},
                subject=newsletter_title,
                html_content=html_content
            )

            self.api_instance.send_transac_email(send_smtp_email)
            return True

        except ApiException as e:
            logger.error(f"Brevo API error sending to {to_email}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False

    async def send_welcome_email(
        self,
        to_email: str,
        to_name: str
    ) -> bool:
        """
        Send welcome email to new subscriber.
        
        Args:
            to_email: Recipient email
            to_name: Recipient name
            
        Returns:
            True if sent successfully
        """
        try:
            template = self.template_env.get_template('welcome.html')
            html_content = template.render(subscriber_name=to_name)

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email, "name": to_name}],
                sender={"email": settings.EMAIL_FROM, "name": settings.EMAIL_FROM_NAME},
                subject="Bem-vindo ao OfertaBR! 🎉",
                html_content=html_content
            )

            self.api_instance.send_transac_email(send_smtp_email)
            return True

        except Exception as e:
            logger.error(f"Error sending welcome email to {to_email}: {e}")
            return False

    async def send_bulk_newsletters(
        self,
        newsletter_title: str,
        newsletter_content: str,
        subscribers: list[dict],
        batch_size: int = 50
    ) -> dict[str, int]:
        """
        Send newsletter to multiple subscribers in batches.
        
        Args:
            newsletter_title: Newsletter title
            newsletter_content: Newsletter HTML content
            subscribers: List of subscriber dicts with keys: email, name, id
            batch_size: Number of emails per batch
            
        Returns:
            Statistics dict: {success: int, failed: int, total: int}
        """
        import asyncio

        stats = {"success": 0, "failed": 0, "total": len(subscribers)}

        for i in range(0, len(subscribers), batch_size):
            batch = subscribers[i:i + batch_size]

            for subscriber in batch:
                success = await self.send_newsletter(
                    to_email=subscriber['email'],
                    to_name=subscriber['name'],
                    newsletter_title=newsletter_title,
                    newsletter_content=newsletter_content,
                    subscriber_id=str(subscriber['id'])
                )

                if success:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1

            # Small delay between batches to respect rate limits
            if i + batch_size < len(subscribers):
                await asyncio.sleep(1)

        if stats["failed"] > 0:
            logger.warning(f"Bulk send completed with errors: {stats}")

        return stats

    async def send_test_email(
        self,
        to_email: str,
        newsletter_title: str,
        newsletter_content: str
    ) -> bool:
        """
        Send a test newsletter email.
        
        Args:
            to_email: Test recipient email
            newsletter_title: Newsletter title
            newsletter_content: Newsletter HTML content
            
        Returns:
            True if sent successfully
        """
        return await self.send_newsletter(
            to_email=to_email,
            to_name="Test User",
            newsletter_title=f"[TESTE] {newsletter_title}",
            newsletter_content=newsletter_content,
            subscriber_id="test-id"
        )

