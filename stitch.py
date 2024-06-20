from logger_config import setup_logger
import os
import glob

# Initialize logger
logger = setup_logger(__name__)

try:
    # Path to the directory containing the files
    cache_dir = os.path.join(os.path.dirname(__file__), 'publish')

    # Pattern to match files - 'inner_cn_*.html'
    pattern = os.path.join(cache_dir, "inner_cn_*.html")

    # Read the template file once
    with open('template.html', 'r', encoding='utf-8') as file:
        html_template = file.read()

    # Find all files matching the pattern
    for idx, filepath in enumerate(glob.glob(pattern)):
        logger.info(f"Processing file: {filepath}")

        # Read the inner HTML content
        with open(filepath, 'r', encoding='utf-8') as file:
            inner_html = file.read()

        # Replace placeholder in template with inner HTML
        final_html = html_template.replace('<!-- Deals will be inserted here -->', inner_html)

        # Write the final HTML to a new file
        output_filepath = os.path.join(cache_dir, f'index_{idx + 1}.html')
        with open(output_filepath, 'w', encoding='utf-8') as file:
            file.write(final_html)
            logger.info(f"Generated webpage written to {output_filepath}")

except Exception as e:
    logger.error(f"Error generating webpage: {e}")
    raise
