# Bhargava Opticians

A Django web application for Bhargava Opticians, an eyewear shop in Sironj, M.P. Customers can browse frames by brand, register, place pickup orders and review what they bought. The owner gets a dashboard with sales insights.

**Live site:** (add link after deployment)

## Features

- **Frame catalogue:** brands and frames with photos, managed by the owner from the Django admin.
- **Customer accounts:** register and log in with a mobile number. Age and gender are optional, and consent is required.
- - **Pickup orders:** customers choose a frame and a shop. There is no delivery. Each order needs a 50% advance, which the owner marks as received in the admin. Each order also shows a ready-by date (2 days after ordering) and a status set by the owner: Placed, Ready for pickup, Picked up or Cancelled.
- **WhatsApp messages:** the owner sends "ready" and "thank you" messages to a customer from the admin Orders list using a pre-filled WhatsApp link.
- **Reviews:** a customer can review a frame only after the order is marked Picked up. Reviews appear on the home page right away.
- **Owner dashboard:** total orders, revenue, repeat customers, average rating, orders per month, top brands and top frames (staff only).
- **REST APIs:** read-only APIs for brands, frames and approved reviews, plus a staff-only dashboard API.

## Tech stack

Python, Django, Django REST Framework, SQLite, HTML, CSS, JavaScript, Chart.js.

## API endpoints

| Endpoint | Access | Description |
|---|---|---|
| `/api/brands/` | Public | All brands |
| `/api/frames/` | Public | All frames, filter with `?brand=<id>` |
| `/api/reviews/` | Public | Approved reviews (first name only) |
| `/api/dashboard/` | Staff only | Summary numbers |

## Design decisions

- The order stores its own `price`, so changing a frame's price later does not change past orders or the revenue figures.
- Reviews are tied to a Picked up order, so only real buyers can review.
- The review API exposes only the customer's first name to protect privacy.
- Secrets and debug settings come from environment variables, not from the code.

## Run it locally

```
git clone https://github.com/sweeti-vish/Bhargava_Opticals.git
cd Bhargava_Opticals
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000`. Add brands and frames from `http://127.0.0.1:8000/admin`.

## Run the tests

```
python manage.py test
```

## Note on data

The payment QR code on the order page is a demo image and not a real payment code. The shop owner's own UPI QR must replace it before real use.

The database and uploaded photos are not stored in this repository. Customer details are private, so only code is shared.

## Author

Sweeti Vishwakarma, B.E. Electronics and Telecommunication Engineering, IET DAVV Indore.