"""
Helper functions to build newsletter HTML from scraped products
"""
from typing import List
from decimal import Decimal
from app.models.scraped_content import ScrapedContent


def format_price(value: Decimal) -> str:
    """
    Format decimal price to Brazilian currency format
    Ex: 1999.99 -> "R$ 1.999,99"
    """
    if value is None:
        return ""
    return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_discount(percentage: Decimal) -> str:
    """
    Format discount percentage
    Ex: 35.5 -> "-35%"
    """
    if percentage is None:
        return ""
    return f"-{int(percentage)}%"


def build_product_card_html(product: ScrapedContent) -> str:
    """
    Build HTML for a single product card
    """
    # Get primary image
    image_url = product.images[0].image_url if product.images else "https://via.placeholder.com/600x280"
    
    # Build badges
    badges_html = ""
    if product.discount_percentage:
        badges_html += f'<span class="badge badge-discount">{format_discount(product.discount_percentage)}</span>'
    if product.free_shipping:
        badges_html += '<span class="badge badge-free-shipping">Frete Grátis</span>'
    
    badges_section = f'<div class="badges">{badges_html}</div>' if badges_html else ""
    
    # Build price section
    old_price_html = ""
    if product.original_price and product.original_price > product.current_price:
        old_price_html = f'<div class="old-price">De {format_price(product.original_price)}</div>'
    
    current_price_html = f'<div class="current-price">{format_price(product.current_price)}</div>' if product.current_price else ""
    
    installments_html = ""
    if product.installments:
        installments_html = f'<div class="installments">{product.installments}</div>'
    
    price_section = f"""
    <div class="price-section">
      {old_price_html}
      {current_price_html}
      {installments_html}
    </div>
    """
    
    # Build full card
    product_url = product.product_url or product.source_url
    
    card_html = f"""
    <div class="product-card">
      <img src="{image_url}" alt="{product.title}" class="product-image" />
      <div class="product-content">
        <h3 class="product-title">{product.title}</h3>
        {badges_section}
        {price_section}
        <a href="{product_url}" class="cta-button">Ver Oferta</a>
      </div>
    </div>
    """
    
    return card_html


def build_products_html(products: List[ScrapedContent]) -> str:
    """
    Build HTML for multiple product cards
    """
    cards_html = []
    
    for product in products:
        cards_html.append(build_product_card_html(product))
    
    return "\n".join(cards_html)


def build_newsletter_content(products: List[ScrapedContent], intro_text: str = None) -> str:
    """
    Build complete newsletter content HTML
    
    Args:
        products: List of ScrapedContent products
        intro_text: Optional intro text before products
        
    Returns:
        Complete HTML string for newsletter content
    """
    intro_html = ""
    if intro_text:
        intro_html = f'<div style="padding: 20px; text-align: center;"><p>{intro_text}</p></div>'
    
    products_html = build_products_html(products)
    
    return f"{intro_html}{products_html}"

