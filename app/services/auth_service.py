"""
Passwordless authentication service using email codes
"""
import secrets
import logging
from typing import Optional
from datetime import timedelta
from app.core.redis import cache_service
from app.core.security import create_access_token
from app.core.config import settings
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class AuthService:
    """Service for passwordless authentication"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.code_ttl = 900  # 15 minutes
        self.token_ttl = 604800  # 7 days
    
    def _generate_code(self) -> str:
        """
        Generate a 6-digit numeric code
        
        Returns:
            6-digit code as string
        """
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    def _generate_magic_token(self) -> str:
        """
        Generate a secure random token for magic links
        
        Returns:
            URL-safe random token
        """
        return secrets.token_urlsafe(32)
    
    async def request_access_code(self, email: str) -> bool:
        """
        Generate and send access code via email
        
        Args:
            email: Admin email address
            
        Returns:
            True if code was sent successfully
        """
        # Check if email is in allowed list
        if not await self._is_allowed_email(email):
            logger.warning(f"Access code requested for unauthorized email: {email}")
            return False
        
        # Generate code
        code = self._generate_code()
        
        # Store in Redis with TTL
        cache_key = f"auth:code:{email}"
        await cache_service.set(cache_key, code, ttl=self.code_ttl)
        
        logger.info(f"Access code generated for {email}: {code} (expires in {self.code_ttl}s)")
        
        # Send email with code
        success = await self._send_code_email(email, code)
        
        if not success:
            logger.error(f"Failed to send access code to {email}")
            # Clean up cache if email failed
            await cache_service.delete(cache_key)
            return False
        
        return True
    
    async def verify_access_code(self, email: str, code: str) -> Optional[str]:
        """
        Verify access code and return JWT token
        
        Args:
            email: Admin email address
            code: 6-digit access code
            
        Returns:
            JWT token if code is valid, None otherwise
        """
        # Get stored code from Redis
        cache_key = f"auth:code:{email}"
        stored_code = await cache_service.get(cache_key)
        
        if not stored_code:
            logger.warning(f"No access code found for {email}")
            return None
        
        # Verify code
        if stored_code != code:
            logger.warning(f"Invalid access code for {email}")
            return None
        
        # Delete code (single use)
        await cache_service.delete(cache_key)
        
        # Generate JWT token
        token = create_access_token(
            data={"sub": email, "type": "admin"},
            expires_delta=timedelta(seconds=self.token_ttl)
        )
        
        logger.info(f"Access granted for {email}")
        
        return token
    
    async def request_magic_link(self, email: str) -> bool:
        """
        Generate and send magic link via email
        
        Args:
            email: Admin email address
            
        Returns:
            True if link was sent successfully
        """
        # Check if email is in allowed list
        if not await self._is_allowed_email(email):
            logger.warning(f"Magic link requested for unauthorized email: {email}")
            return False
        
        # Generate secure token
        token = self._generate_magic_token()
        
        # Store in Redis with email
        cache_key = f"auth:magic:{token}"
        await cache_service.set(cache_key, email, ttl=self.code_ttl)
        
        logger.info(f"Magic link generated for {email} (expires in {self.code_ttl}s)")
        
        # Send email with magic link
        magic_url = f"{settings.FRONTEND_URL}/auth/verify?token={token}"
        success = await self._send_magic_link_email(email, magic_url)
        
        if not success:
            logger.error(f"Failed to send magic link to {email}")
            await cache_service.delete(cache_key)
            return False
        
        return True
    
    async def verify_magic_token(self, token: str) -> Optional[str]:
        """
        Verify magic link token and return JWT token
        
        Args:
            token: Magic link token
            
        Returns:
            JWT token if valid, None otherwise
        """
        # Get email from Redis
        cache_key = f"auth:magic:{token}"
        email = await cache_service.get(cache_key)
        
        if not email:
            logger.warning(f"Invalid or expired magic token")
            return None
        
        # Delete token (single use)
        await cache_service.delete(cache_key)
        
        # Generate JWT token
        jwt_token = create_access_token(
            data={"sub": email, "type": "admin"},
            expires_delta=timedelta(seconds=self.token_ttl)
        )
        
        logger.info(f"Access granted via magic link for {email}")
        
        return jwt_token
    
    async def _is_allowed_email(self, email: str) -> bool:
        """
        Check if email is allowed to access admin endpoints
        
        For now, checks against a whitelist in Redis or env var.
        In production, you might check against a database table.
        
        Args:
            email: Email to check
            
        Returns:
            True if email is allowed
        """
        # Check if whitelist exists in Redis
        allowed_emails = await cache_service.get("auth:allowed_emails")
        
        if allowed_emails:
            return email.lower() in [e.lower() for e in allowed_emails]
        
        # Fallback: check env var or use default admin email
        # TODO: Move this to database or proper config
        default_allowed = [
            "admin@ofertabr.com",
            settings.EMAIL_FROM,
        ]
        
        return email.lower() in [e.lower() for e in default_allowed]
    
    async def add_allowed_email(self, email: str) -> bool:
        """
        Add email to allowed list
        
        Args:
            email: Email to allow
            
        Returns:
            True if added successfully
        """
        allowed_emails = await cache_service.get("auth:allowed_emails") or []
        
        if email.lower() not in [e.lower() for e in allowed_emails]:
            allowed_emails.append(email.lower())
            await cache_service.set("auth:allowed_emails", allowed_emails, ttl=None)
            logger.info(f"Added {email} to allowed emails")
            return True
        
        return False
    
    async def remove_allowed_email(self, email: str) -> bool:
        """
        Remove email from allowed list
        
        Args:
            email: Email to remove
            
        Returns:
            True if removed successfully
        """
        allowed_emails = await cache_service.get("auth:allowed_emails") or []
        
        if email.lower() in [e.lower() for e in allowed_emails]:
            allowed_emails = [e for e in allowed_emails if e.lower() != email.lower()]
            await cache_service.set("auth:allowed_emails", allowed_emails, ttl=None)
            logger.info(f"Removed {email} from allowed emails")
            return True
        
        return False
    
    async def list_allowed_emails(self) -> list[str]:
        """
        List all allowed emails
        
        Returns:
            List of allowed email addresses
        """
        return await cache_service.get("auth:allowed_emails") or []
    
    async def _send_code_email(self, to_email: str, code: str) -> bool:
        """
        Send access code via email
        
        Args:
            to_email: Recipient email
            code: 6-digit access code
            
        Returns:
            True if sent successfully
        """
        try:
            from jinja2 import Template
            
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #667eea;
            margin: 0;
            font-size: 24px;
        }
        .code-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
        }
        .code {
            font-size: 48px;
            font-weight: bold;
            letter-spacing: 10px;
            margin: 10px 0;
        }
        .info {
            color: #666;
            line-height: 1.6;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Código de Acesso</h1>
        </div>
        
        <div class="info">
            <p>Olá!</p>
            <p>Alguém solicitou acesso ao painel administrativo do <strong>OfertaBR</strong>.</p>
            <p>Use o código abaixo para fazer login:</p>
        </div>
        
        <div class="code-box">
            <div>Seu código de acesso:</div>
            <div class="code">{{ code }}</div>
            <div style="font-size: 14px; margin-top: 10px;">Válido por 15 minutos</div>
        </div>
        
        <div class="info">
            <p><strong>⚠️ Importante:</strong></p>
            <ul>
                <li>Este código é de uso único</li>
                <li>Não compartilhe com ninguém</li>
                <li>Se você não solicitou este código, ignore este email</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>OfertaBR - Sistema de Newsletters</p>
        </div>
    </div>
</body>
</html>
            """
            
            template = Template(html_template)
            html_content = template.render(code=code)
            
            # Use email service (Brevo)
            import sib_api_v3_sdk
            from sib_api_v3_sdk.rest import ApiException
            
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
        """
        Send magic link via email
        
        Args:
            to_email: Recipient email
            magic_url: Magic link URL
            
        Returns:
            True if sent successfully
        """
        try:
            from jinja2 import Template
            
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #667eea;
            margin: 0;
            font-size: 24px;
        }
        .button-container {
            text-align: center;
            margin: 30px 0;
        }
        .magic-button {
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        }
        .info {
            color: #666;
            line-height: 1.6;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ Link de Acesso Rápido</h1>
        </div>
        
        <div class="info">
            <p>Olá!</p>
            <p>Clique no botão abaixo para acessar o painel administrativo do <strong>OfertaBR</strong>:</p>
        </div>
        
        <div class="button-container">
            <a href="{{ magic_url }}" class="magic-button">
                🚀 Acessar Painel Admin
            </a>
        </div>
        
        <div class="info">
            <p style="font-size: 12px; color: #999;">
                Este link expira em 15 minutos e só pode ser usado uma vez.
            </p>
            <p><strong>⚠️ Importante:</strong></p>
            <ul>
                <li>Não compartilhe este link com ninguém</li>
                <li>Se você não solicitou este acesso, ignore este email</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>OfertaBR - Sistema de Newsletters</p>
        </div>
    </div>
</body>
</html>
            """
            
            template = Template(html_template)
            html_content = template.render(magic_url=magic_url)
            
            # Use email service (Brevo)
            import sib_api_v3_sdk
            
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

