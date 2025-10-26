import secrets
import logging
from typing import Optional
from datetime import timedelta
from pathlib import Path
import sib_api_v3_sdk
from jinja2 import Environment, FileSystemLoader
from app.core.redis import cache_service
from app.core.security import create_access_token
from app.core.config import settings
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.email_service = EmailService()
        self.code_ttl = 900
        self.token_ttl = 604800
        
        template_dir = Path(__file__).parent.parent / 'templates' / 'emails'
        self.template_env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    def _generate_code(self) -> str:
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    def _generate_magic_token(self) -> str:
        return secrets.token_urlsafe(32)
    
    async def request_access_code(self, email: str) -> bool:
        if not await self._is_allowed_email(email):
            logger.warning(f"Access code requested for unauthorized email: {email}")
            return False
        
        code = self._generate_code()
        cache_key = f"auth:code:{email}"
        await cache_service.set(cache_key, code, ttl=self.code_ttl)
        
        logger.info(f"Access code generated for {email}: {code} (expires in {self.code_ttl}s)")
        
        success = await self._send_code_email(email, code)
        
        if not success:
            logger.error(f"Failed to send access code to {email}")
            await cache_service.delete(cache_key)
            return False
        
        return True
    
    async def verify_access_code(self, email: str, code: str) -> Optional[str]:
        cache_key = f"auth:code:{email}"
        stored_code = await cache_service.get(cache_key)
        
        if not stored_code:
            logger.warning(f"No access code found for {email}")
            return None
        
        if stored_code != code:
            logger.warning(f"Invalid access code for {email}")
            return None
        
        await cache_service.delete(cache_key)
        
        token = create_access_token(
            data={"sub": email, "type": "admin"},
            expires_delta=timedelta(seconds=self.token_ttl)
        )
        
        logger.info(f"Access granted for {email}")
        return token
    
    async def request_magic_link(self, email: str) -> bool:
        if not await self._is_allowed_email(email):
            logger.warning(f"Magic link requested for unauthorized email: {email}")
            return False
        
        token = self._generate_magic_token()
        cache_key = f"auth:magic:{token}"
        await cache_service.set(cache_key, email, ttl=self.code_ttl)
        
        logger.info(f"Magic link generated for {email} (expires in {self.code_ttl}s)")
        
        magic_url = f"{settings.FRONTEND_URL}/auth/verify?token={token}"
        success = await self._send_magic_link_email(email, magic_url)
        
        if not success:
            logger.error(f"Failed to send magic link to {email}")
            await cache_service.delete(cache_key)
            return False
        
        return True
    
    async def verify_magic_token(self, token: str) -> Optional[str]:
        cache_key = f"auth:magic:{token}"
        email = await cache_service.get(cache_key)
        
        if not email:
            logger.warning(f"Invalid or expired magic token")
            return None
        
        await cache_service.delete(cache_key)
        
        jwt_token = create_access_token(
            data={"sub": email, "type": "admin"},
            expires_delta=timedelta(seconds=self.token_ttl)
        )
        
        logger.info(f"Access granted via magic link for {email}")
        return jwt_token
    
    async def _is_allowed_email(self, email: str) -> bool:
        allowed_emails = await cache_service.get("auth:allowed_emails") or []
        default_allowed = ["admin@ofertabr.com", settings.EMAIL_FROM]
        
        all_allowed = list(set([e.lower() for e in allowed_emails] + [e.lower() for e in default_allowed]))
        return email.lower() in all_allowed
    
    async def add_allowed_email(self, email: str) -> bool:
        allowed_emails = await cache_service.get("auth:allowed_emails") or []
        
        if email.lower() not in [e.lower() for e in allowed_emails]:
            allowed_emails.append(email.lower())
            await cache_service.set("auth:allowed_emails", allowed_emails, ttl=None)
            logger.info(f"Added {email} to allowed emails")
            return True
        
        return False
    
    async def remove_allowed_email(self, email: str) -> bool:
        allowed_emails = await cache_service.get("auth:allowed_emails") or []
        
        if email.lower() in [e.lower() for e in allowed_emails]:
            allowed_emails = [e for e in allowed_emails if e.lower() != email.lower()]
            await cache_service.set("auth:allowed_emails", allowed_emails, ttl=None)
            logger.info(f"Removed {email} from allowed emails")
            return True
        
        return False
    
    async def list_allowed_emails(self) -> list[str]:
        allowed_emails = await cache_service.get("auth:allowed_emails") or []
        default_allowed = ["admin@ofertabr.com", settings.EMAIL_FROM]
        
        all_allowed = list(set([e.lower() for e in allowed_emails] + [e.lower() for e in default_allowed]))
        return sorted(all_allowed)
    
    async def _send_code_email(self, to_email: str, code: str) -> bool:
        try:
            template = self.template_env.get_template('access_code.html')
            html_content = template.render(code=code)
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email}],
                sender={"email": settings.EMAIL_FROM, "name": settings.EMAIL_FROM_NAME},
                subject="🔐 Seu código de acesso - OfertaBR",
                html_content=html_content
            )
            
            self.email_service.api_instance.send_transac_email(send_smtp_email)
            logger.info(f"Access code email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending access code email to {to_email}: {e}")
            return False
    
    async def _send_magic_link_email(self, to_email: str, magic_url: str) -> bool:
        try:
            template = self.template_env.get_template('magic_link.html')
            html_content = template.render(magic_url=magic_url)
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email}],
                sender={"email": settings.EMAIL_FROM, "name": settings.EMAIL_FROM_NAME},
                subject="✨ Seu link de acesso rápido - OfertaBR",
                html_content=html_content
            )
            
            self.email_service.api_instance.send_transac_email(send_smtp_email)
            logger.info(f"Magic link email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending magic link email to {to_email}: {e}")
            return False

