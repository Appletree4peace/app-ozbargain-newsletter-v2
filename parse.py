from bs4 import BeautifulSoup
from logger_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Load the HTML content from the file
with open("publish/output.html", "r") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the "Popular Deals" section
popular_deals = soup.find_all('h2', string=lambda text: "Popular Deals" in text)[0].find_next_sibling('table')

index = -1
html_outputs = []
deals_txt = ""
# Extract the requested fields for each product
for row in popular_deals.find_all('tr'):
    vote_cell = row.find('td', class_='vote-cell')
    deal_title = row.find('h2', class_='deal-title')
    deal_desc = row.find('div', class_='deal-desc')
    deal_img_cell = row.find('td', class_='deal-img-cell')

    if vote_cell and deal_title and deal_img_cell and deal_desc:
        index += 1
        vote = vote_cell.get_text(strip=True)
        link = deal_title.find('a').get('href').split('?')[0]
        title = deal_title.get_text(strip=True)
        image = deal_img_cell.find('img', alt="deal img")['src']
        posted_time = deal_desc.get_text(strip=True).split('in')[0].strip().replace('Posted on ', '')
        tag = deal_desc.find('img', alt="tag").find_next_sibling(string=True).strip() if deal_desc.find('img', alt="tag") else None
        expiry = deal_desc.find('img', alt="Expiry").find_next_sibling(text=True).strip().replace('Expires on ', '') if deal_desc.find('img', alt="Expiry") else None

        print(f"Vote Number: {vote}")
        print(f"Title: {title}")
        print(f"Image URL: {image}")
        print(f"Posted Time: {posted_time}")
        print(f"Tag: {tag}")
        print(f"Link: {link}")
        print(f"Expiry Time: {expiry}")
        print("-" * 30)

        # push in deals text file
        deals_txt += f"{title}<br />\n - Link: {link}<br />\n - Expiry: {expiry}<br /><br />\n\n"

        # Build the HTML for this product
        if expiry:
            expiry_html = f"<li>有效期: {expiry}</li>"
        else:
            expiry_html = ""
        
        group_idx = index // 5
        if group_idx >= len(html_outputs):
            html_outputs.append("")

        html_outputs[group_idx] += f'''
<div class="product">
    <h2 class="product-title">{title}</h2>
    <ul class="product-introduction">
        <li class="vote">网友投票: {vote}</li>
        {expiry_html}
    </ul>
    <img src="{image}" alt="{title}" class="product-image">
</div>
        '''

for i in range(len(html_outputs)):
    extra_html = '<style>body {border-color: #5F59F7}</style>' if i % 2 == 0 else ""
    # Save the new HTML content to a file
    with open(f"publish/inner_en_{i}.html", "w") as file:
        file.write(html_outputs[i] + extra_html)

with open("publish/deals.txt", "w") as file:
    file.write(deals_txt)
