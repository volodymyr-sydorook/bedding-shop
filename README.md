# 🛏️ BeddingShop E-Commerce

> A modern, full-featured online store for bedding and home textiles, built with Django.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)

## 📖 About The Project

What started as a **pet project** to master Django development has evolved into a production-ready **MVP (Minimum Viable Product)** for an e-commerce business. 

The goal was to create a clean, responsive, and user-friendly platform that handles the entire flow of an online shop—from browsing products to processing orders with real-time manager notifications.

## ✨ Key Features

### 🛒 Customer Experience
* **Responsive Design:** Fully adaptive UI based on Bootstrap 5 (Mobile First approach).
* **Product Catalog:** Advanced filtering (price, category), search functionality, and pagination.
* **Product Variations:** Support for different sizes/colors with dynamic image switching.
* **Smart Cart:** Session-based cart (works for guests), stock validation.
* **Checkout:** Streamlined checkout process with delivery (Nova Poshta/Ukrposhta) and payment options.
* **User Profile:** Order history with detailed status tracking.

### ⚙️ Back-Office & Administration
* **Custom Admin Panel:** Optimized Django Admin with inline editing and order summaries.
* **Telegram Integration:** Real-time notifications for managers via Telegram Bot upon new orders.
* **Database:** Migrated from SQLite to **MySQL** for production stability.
* **Security:** SSL/HTTPS support, secure password handling.

## 🛠️ Tech Stack

* **Backend:** Python, Django Framework.
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript.
* **Database:** MySQL.
* **Deployment:** Nginx, Gunicorn, VPS (Ubuntu).
* **Tools:** Git, Telegram API (requests).

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites
* Python 3.10+
* MySQL Server

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/beddingshop.git](https://github.com/yourusername/beddingshop.git)
    cd beddingshop
    ```

2.  **Create and activate virtual environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Database (settings.py)**
    Update the `DATABASES` section in `core/settings.py` with your MySQL credentials or create a `.env` file.

5.  **Apply migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Run the server**
    ```bash
    python manage.py runserver
    ```

## 📸 Screenshots
*(Add screenshots of your Catalog, Cart, and Admin panel here)*

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

---
*Developed by Volodymyr Sydoruk*