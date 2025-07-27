🍽️ E-Commerce website Restaurant System
A full-featured Restaurant Management System built using Django, designed to handle the core operations of a restaurant such as user registration, menu browsing, order placement, and order management. The system provides a dual login architecture for admins (via the Django admin panel) and customers (via a custom authentication system). It includes a working cart and order flow tailored for a seamless user experience.

🔧 Tech Stack
Backend: Python, Django
Frontend: HTML, CSS, JavaScript (Django templates)
Database: SQLite (default)
Authentication: Django's built-in system (Admin), Custom user model for Customer login
✨ Features
👤 Customer Side:
User Registration & Login
View Menu and Item Details
Add Items to Cart
View, Modify, and Delete Cart Items
Place Orders
🔐 Admin Side:
Manage Menu Items (Add/Edit/Delete)
View All Customer Orders
Manage Order Statuses
Access via Django's default admin panel
🗃️ Project Structure
restaurant_project/
├── hotel_web/          # Menu, Cart, Order logic
├── login/                   # Customer auth system (models, views, templates)
├── media/                 # Uploaded files if applicable
├── Project/                # Django Project folder
├── static/                   # Static files (CSS, JS, images)
├── templates/           # Global templates
├── db.sqlite3
├── manage.py
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/yourusername/restaurant-management-system.git
cd restaurant-management-system
2. Set up the Virtual Environment
env\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
Make sure to generate the requirements.txt if not present:

pip freeze > requirements.txt
4. Run Migrations
python manage.py makemigrations
python manage.py migrate
5. Create Superuser (for Admin Panel)
python manage.py createsuperuser
6. Run the Server
python manage.py runserver
Visit http://127.0.0.1:8000/ for the customer side and http://127.0.0.1:8000/admin/ for the admin panel.

📂 Admin Panel
Login as superuser to:

Add/Edit/Delete Menu Items
View and manage all Orders
Manage Customers (if extended)
🔐 Authentication
Admin: Uses Django’s built-in admin login.
Customer: Custom login system via a separate login app. User data stored in a custom UserData model.
🛠️ Future Enhancements
Add payment gateway integration (e.g., Razorpay or Stripe)
Live order status tracking
SMS/Email order confirmation
Customer feedback system
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

📃 License
This project is open-source and available under the MIT License.

👨‍💻 Author
pramod kumbhar
GitHub: @pramod-kumbhar
About
No description, website, or topics provided.
Resources
 Readme
License
 MIT license
 Activity
Stars
 0 stars
Watchers
 1 watching
Forks
 0 forks
Report repository
Releases
No releases published
Packages
No packages published
Languages
Python
38.2%
 
CSS
34.3%
 
HTML
24.4%
 
JavaScript
2.6%
 
Other
0.5%
Footer
