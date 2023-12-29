Lego-deals

A small program for discount products on the Lego official website.

---

### User Guide

**Introduction:**
Lego-deals is a small program designed to help users find discounted products on the official Lego website. With this program, users can easily access information about discounted Lego products and filter out products of interest based on specific product IDs configured in the YAML file.

**Configuration File:**
1. Create a YAML configuration file named `config.yaml` in the program directory.

**Configuration Example:**
```yaml
# config.yaml
hosts:
  - name: lego_sales_and_deals
    url: https://www.lego.com/en-ca/categories/sales-and-deals
  - name: lego_last_chance_to_buy
    url: https://www.lego.com/en-ca/categories/last-chance-to-buy
collect:
  - 10328
  - 71426
  - 71395
  - 21342
```

- `hosts`: Contains configuration information for different Lego product pages to be searched, including page name (`name`) and URL link (`url`).
- `collect`: Contains a list of product IDs that the user wishes to purchase.

**Usage Workflow:**
1. Install Python: Ensure that Python is installed on your computer (preferably Python 3. X).
2. Install Dependencies: Open the terminal, navigate to the program directory, and execute the following command to install the required dependencies:
   ```
   pip install requests beautifulsoup4 PyYAML
   ```
3. Configure the `config.yaml` File: Edit the configuration file according to the above configuration example, specifying the desired website pages and product IDs for purchase.
4. Run the Program: Execute the following command in the terminal to run the program:
   ```
   python Lego-deals.py
   ```
5. View the Results: The program will generate two CSV files in the current directory, one containing all product information (e.g., `lego_sales_and_deals_products.csv`) and the other containing matching product information for purchase (e.g., `collect_buy.csv`).

**Notes:**
- Ensure that Python is installed on your computer and the necessary dependencies are installed.
- Before usage, modify the configuration file parameters according to your requirements.
- Avoid making frequent network requests to prevent unnecessary stress on the Lego official website.
- If any issues arise during program execution, ensure a stable internet connection and check for write permissions in the program directory.

**Disclaimer:**
This program is intended for personal learning and research purposes. Users are responsible for any risks and liabilities associated with the use of this program, including but not limited to violating the terms of use of the official website and potential IP blocking.