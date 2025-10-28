
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
    image_url = product.images[0].image_url if product.images else "https://via.placeholder.com/600x280"

    badges_html = ""
    if product.discount_percentage:
        badges_html += f'<span style="display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; background-color: #ff4757; color: #ffffff; margin-right: 5px;">{format_discount(product.discount_percentage)}</span>'
    if product.free_shipping:
        badges_html += '<span style="display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; background-color: #2ecc71; color: #ffffff;">Frete Grátis</span>'

    badges_section = f'<div style="display: flex; gap: 5px; margin-bottom: 10px; flex-wrap: wrap;">{badges_html}</div>' if badges_html else ""

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

    product_url = product.product_url or product.source_url

    card_html = f"""
    <div style="background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin: 0;">
      <a href="{product_url}" style="text-decoration: none; display: block;">
        <img src="{image_url}" 
             alt="{product.title}" 
             width="280"
             height="150"
             border="0"
             style="width: 100%; height: 150px; display: block; object-fit: cover; border-bottom: 1px solid #e0e0e0;" />
      </a>
      <div style="padding: 12px;">
        <h3 style="font-size: 13px; font-weight: 600; color: #222; margin: 0 0 8px 0; line-height: 1.3; min-height: 34px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
          {product.title}
        </h3>
        {badges_section if badges_section else ''}
        <div style="margin: 8px 0;">
          {old_price_html.replace('class="old-price"', 'style="font-size: 11px; color: #999; text-decoration: line-through; margin-bottom: 2px;"') if old_price_html else ''}
          {current_price_html.replace('class="current-price"', 'style="font-size: 22px; font-weight: 700; color: #667eea; margin: 2px 0; line-height: 1;"') if current_price_html else ''}
          {installments_html.replace('class="installments"', 'style="font-size: 10px; color: #666; margin-top: 4px;"') if installments_html else ''}
        </div>
        <a href="{product_url}" 
           style="display: inline-block; width: calc(100% - 4px); padding: 9px 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff !important; text-align: center; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 13px; margin-top: 8px; box-sizing: border-box;">
          Ver Oferta
        </a>
      </div>
    </div>
    """

    return card_html


def build_products_html(products: list[ScrapedContent]) -> str:
    """
    Build HTML for multiple product cards in 2-column grid layout
    Uses tables for better email client compatibility
    """
    if not products:
        return ""

    rows_html = []

    for i in range(0, len(products), 2):
        product1 = products[i]
        product2 = products[i + 1] if i + 1 < len(products) else None

        cell1 = f"""
        <td width="50%" valign="top" style="padding: 10px;">
            {build_product_card_html(product1)}
        </td>
        """

        cell2 = ""
        if product2:
            cell2 = f"""
            <td width="50%" valign="top" style="padding: 10px;">
                {build_product_card_html(product2)}
            </td>
            """
        else:
            cell2 = '<td width="50%" style="padding: 10px;"></td>'

        row = f"""
        <tr>
            {cell1}
            {cell2}
        </tr>
        """
        rows_html.append(row)

    grid_html = f"""
    <table class="product-grid" width="100%" border="0" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
        <tbody>
            {''.join(rows_html)}
        </tbody>
    </table>
    """

    return grid_html


def build_newsletter_content(products: list[ScrapedContent], intro_text: str = None) -> str:
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

