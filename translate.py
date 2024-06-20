import os
import glob
import google.generativeai as genai
from logger_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)

api_key = os.getenv('GOOGLE_API_KEY')

def translate(text, api_key, type='html'):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-pro')
        
        # Craft a prompt for translation
        if type == 'html':
            prompt = f"Translate the html file into Chinese, do not change html tags. only translate content inside html tags. For all $ signs, translated it as '澳元', not '美元'. for date like '2 Jan', translate as '1月2日':\n\n{text}"
        elif type == 'text':
            prompt = f"Translate the text file into Chinese. Keep the original format. For all $ signs, translated it as '澳元', not '美元'. for date like '2 Jan', translate as '1月2日':\n\n{text}"

        # Make the API call
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        logger.error(f"Translation error: {response.prompt_feedback}")
        logger.error(f"Translation error: {e}")
        raise

def translate_html_file(file_path, api_key):
    try:
        with open(file_path, 'r') as file:
            html_content = file.read()

        return translate(html_content, api_key)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise


if __name__ == '__main__':
    logger.info("Starting translation of HTML files ...")

    # Path to the directory containing the files
    cache_dir = "publish"

    # Pattern to match files - 'inner_en_*.html'
    pattern = os.path.join(cache_dir, "inner_en_*.html")

    # Find all files matching the pattern
    for filepath in glob.glob(pattern):
        logger.info(f"Processing file: {filepath}")

        # Translate the content of the file
        translated_content = translate_html_file(filepath, api_key)

        # Create the output file path by replacing 'en' with 'cn' in the filename
        output_filepath = filepath.replace('inner_en_', 'inner_cn_')

        # Write the translated content to the new file
        with open(output_filepath, "w") as file:
            file.write(translated_content)
            logger.info(f"Translated content written to {output_filepath}")
    
    # Translate the deals.txt
    with open("publish/deals.txt", "r") as file:
        deals_txt = file.read()
    translated_deals = translate(deals_txt, api_key)

    # Write the translated content to the new file
    with open("publish/deals_cn.txt", "w") as file:
        file.write(translated_deals)
        logger.info(f"Translated content written to publish/deals_cn.txt")