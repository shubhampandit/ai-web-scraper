# AI Web Scraper

AI Web Scraper is an intelligent web scraping tool that leverages Large Language Models (LLMs) to extract structured data from websites. It automates the process of identifying and retrieving relevant information, making web data extraction more efficient and accessible.

## Features

- **Automated Data Extraction**: Utilizes LLMs to understand and extract desired data from web pages without manual intervention.
- **Dynamic Content Handling**: Capable of processing JavaScript-rendered content, ensuring accurate data retrieval from modern websites.
- **Customizable Extraction Rules**: Allows users to define specific data points for extraction, tailoring the scraping process to individual needs.
- **Scalable Architecture**: Designed to handle multiple URLs and large datasets efficiently.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/shubhampandit/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   Create a `.env` file in the project root directory with the following content:

   ```
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_googleai_api_key
   ```

   Replace `your_openai_api_key` with your actual OpenAI API key.

## Usage

1. **Configure the Scraper**:

   Edit the `config.py` file to specify the target URLs and the data points you wish to extract.

2. **Run the Scraper**:

   ```bash
   python app.py
   ```

   The extracted data will be saved in the `output` directory in JSON format.

## Dependencies

- Python 3.8 or higher
- Requests
- BeautifulSoup4
- OpenAI

All dependencies are listed in the `requirements.txt` file.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Acknowledgements

Special thanks to the developers of the following projects for their inspiration and contributions to the field of AI-powered web scraping:

- [Crawl4AI](https://github.com/unclecode/crawl4ai)

These projects have paved the way for integrating AI into web scraping, and their work has been instrumental in the development of AI Web Scraper.

