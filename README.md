# Django Store API

A RESTful backend API for an online store, built with Django and Django REST Framework.

This project focuses on developing the backend components of an e-commerce application, including product and collection management, shopping carts, customer profiles, product reviews, user authentication, permissions, and API filtering.

It is a learning and development project intended to demonstrate Django REST Framework concepts, relational data modeling, API design, and backend development practices.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Authentication and Permissions](#authentication-and-permissions)
- [Filtering, Searching, and Pagination](#filtering-searching-and-pagination)
- [Admin Dashboard](#admin-dashboard)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [Current Limitations](#current-limitations)
- [Future Improvements](#future-improvements)

## Features

### Product and Collection Management

- Create, retrieve, update, and delete products.
- Organize products into collections.
- Calculate a product price including a 10% tax estimate.
- Track product inventory and last-update timestamps.
- Display the number of products belonging to each collection.
- Prevent deletion of products associated with order items.
- Prevent deletion of collections that still contain products.

### Shopping Cart

- Create shopping carts identified by UUIDs.
- Retrieve cart details and their associated items.
- Add products to a cart.
- Increase the quantity of an existing cart item when the same product is added again.
- Update cart item quantities.
- Remove cart items and delete carts.
- Calculate individual cart item subtotals and the total cart price.
- Prevent duplicate entries for the same product within a cart through a database uniqueness constraint.

### Customer Management

- Associate customer profiles with user accounts.
- Store customer phone numbers, birth dates, and membership levels.
- Support Bronze, Silver, and Gold membership categories.
- Provide a dedicated endpoint for retrieving or updating the authenticated user's customer profile.
- Define a custom permission for accessing customer history.

### User Authentication

- Use a custom Django user model with unique email addresses.
- Integrate Djoser for user-related authentication endpoints.
- Use JSON Web Tokens (JWT) through Django REST Framework Simple JWT.
- Customize user creation and current-user serializers.

### Product Reviews

- Associate reviews with individual products.
- Store reviewer names, descriptions, and dates.
- Provide nested review endpoints under products.

### Filtering and API Responses

- Filter products by collection.
- Filter products by minimum and maximum unit price.
- Search product titles and descriptions.
- Order products by unit price or last-update time.
- Paginate product results.
- Use serializers to control the structure of API responses.

### Tagging and Generic Relationships

- Define reusable tags.
- Associate tags with objects using Django's generic relationships.
- Customize Django Admin to manage product tags inline.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework and ORM |
| Django REST Framework | REST API development |
| MySQL | Configured relational database |
| Django Filter | API filtering |
| Djoser | User management endpoints |
| Simple JWT | Token-based authentication |
| DRF Nested Routers | Nested resource routing |
| Django Debug Toolbar | Development-time debugging |
| Pipenv | Dependency and virtual environment management |
| Git and GitHub | Version control and source code hosting |

## Project Structure

```text
Django-Store-API/
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── serializers.py
├── likes/
│   ├── apps.py
│   └── models.py
├── playground/
│   └── apps.py
├── store/
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── storefront/
│   ├── settings.py
│   └── urls.py
├── tags/
│   ├── admin.py
│   ├── apps.py
│   └── models.py
├── manage.py
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── README.md
```

### Application Responsibilities

- **`core/`**: Custom user model, user serializers, and user-related admin configuration.
- **`store/`**: Main e-commerce domain, including products, collections, customers, orders, cart functionality, reviews, serializers, API views, filters, permissions, and pagination.
- **`tags/`**: Reusable tag models and generic object-tag relationships.
- **`likes/`**: A generic liked-item model associating users with different types of content.
- **`playground/`**: Development and learning-related application.
- **`storefront/`**: Main Django project configuration and URL routing.

## Data Models

The main application contains the following models:

| Model | Responsibility |
|---|---|
| `Product` | Product information, pricing, inventory, collection, and promotions |
| `Collection` | Groups products and optionally references a featured product |
| `Promotion` | Stores promotion descriptions and discount values |
| `Customer` | Stores customer profile information and membership level |
| `Order` | Stores order ownership, placement time, and payment status |
| `OrderItem` | Associates products and quantities with orders |
| `Cart` | Represents a shopping cart with a UUID primary key |
| `CartItem` | Associates products and quantities with carts |
| `Review` | Stores reviews associated with products |
| `User` | Custom Django user with a unique email address |
| `Tag` | Stores reusable tags |
| `TaggedItem` | Associates tags with objects through generic relationships |
| `LikedItem` | Associates a user with a generic content object |

The data models use foreign keys, one-to-one relationships, many-to-many relationships, validation constraints, and Django content types where appropriate.

## API Endpoints

The API is mounted under `/store/`, while authentication endpoints are mounted under `/auth/`.

### Products

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/store/products/` | List products |
| POST | `/store/products/` | Create a product |
| GET | `/store/products/{id}/` | Retrieve a product |
| PUT / PATCH | `/store/products/{id}/` | Update a product |
| DELETE | `/store/products/{id}/` | Delete a product, subject to business rules |

### Collections

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/store/collections/` | List collections |
| POST | `/store/collections/` | Create a collection |
| GET | `/store/collections/{id}/` | Retrieve a collection |
| PUT / PATCH | `/store/collections/{id}/` | Update a collection |
| DELETE | `/store/collections/{id}/` | Delete a collection, subject to business rules |

### Shopping Carts

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/store/carts/` | List carts |
| POST | `/store/carts/` | Create a cart |
| GET | `/store/carts/{cart_uuid}/` | Retrieve a cart and its items |
| DELETE | `/store/carts/{cart_uuid}/` | Delete a cart |

### Cart Items

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/store/carts/{cart_uuid}/items/` | List items in a cart |
| POST | `/store/carts/{cart_uuid}/items/` | Add a product to a cart |
| GET | `/store/carts/{cart_uuid}/items/{id}/` | Retrieve a cart item |
| PATCH | `/store/carts/{cart_uuid}/items/{id}/` | Update an item quantity |
| DELETE | `/store/carts/{cart_uuid}/items/{id}/` | Remove an item |

### Product Reviews

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/store/products/{product_id}/reviews/` | List reviews for a product |
| POST | `/store/products/{product_id}/reviews/` | Create a review |
| GET | `/store/products/{product_id}/reviews/{id}/` | Retrieve a review |
| PUT / PATCH | `/store/products/{product_id}/reviews/{id}/` | Update a review |
| DELETE | `/store/products/{product_id}/reviews/{id}/` | Delete a review |

### Customers

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/store/customers/` | List customers |
| POST | `/store/customers/` | Create a customer profile |
| GET | `/store/customers/{id}/` | Retrieve a customer |
| PUT / PATCH | `/store/customers/{id}/` | Update a customer |
| DELETE | `/store/customers/{id}/` | Delete a customer |
| GET | `/store/customers/me/` | Retrieve the authenticated user's customer profile |
| PUT | `/store/customers/me/` | Update the authenticated user's customer profile |
| GET | `/store/customers/{id}/history/` | Access the custom customer-history action |

The endpoints above are derived from the configured routers and viewsets. Actual behavior depends on authentication, permissions, validation, and the current implementation.

## Authentication and Permissions

The project configures JWT authentication using Django REST Framework Simple JWT.

Djoser routes are mounted under `/auth/`, including the standard user and JWT endpoint families.

The JWT configuration uses the `JWT` authorization header prefix and an access-token lifetime of one day.

Example request header:

```http
Authorization: JWT <access_token>
```

### Permission Rules

- Product and collection read operations are publicly accessible under the custom `IsAdminOrReadOnly` permission.
- Product and collection write operations require a staff user.
- Customer viewset operations require an administrator, except for actions with their own permission configuration.
- The customer `me` action requires authentication.
- The customer `history` action uses a custom permission checking the `store.view_history` permission.

**Important:** These permission rules describe the current configuration. Additional ownership checks and authorization tests should be added where necessary before production use.

## Filtering, Searching, and Pagination

The product API supports filtering, searching, ordering, and pagination.

### Filtering

Supported filter fields:

- `collection_id`
- `unit_price__gt`
- `unit_price__lt`

Examples:

```http
GET /store/products/?collection_id=1
GET /store/products/?unit_price__gt=10
GET /store/products/?unit_price__lt=100
```

### Search

Search product titles and descriptions:

```http
GET /store/products/?search=phone
```

### Ordering

Order products by price or last update:

```http
GET /store/products/?ordering=unit_price
GET /store/products/?ordering=-last_update
```

### Pagination

The default product pagination size is 10 items per page.

```http
GET /store/products/?page=2
```

## Admin Dashboard

Django Admin provides an interface for managing application data.

Current customizations include:

- Product search, filtering, editable prices, and inventory status.
- A low-inventory filter for products with fewer than 10 units.
- A bulk action to clear product inventory.
- Collection management with product counts and links to related products.
- Customer management with membership editing and order counts.
- Order management with inline order items.
- Product tag management through an inline interface.
- Custom user administration based on Django's `UserAdmin`.

The administration interface is available at:

```text
/admin/
```

A staff account can be created locally using:

```bash
pipenv run python manage.py createsuperuser
```

## Installation and Setup

### Prerequisites

- Python compatible with the versions required by the project dependencies.
- Pipenv.
- A running MySQL server if using the currently configured database backend.

### 1. Clone the Repository

```bash
git clone https://github.com/javad-salehi/Django-Store-API.git
cd Django-Store-API
```

### 2. Install Dependencies

```bash
pipenv install
```

Activate the virtual environment if desired:

```bash
pipenv shell
```

### 3. Configure Environment Variables

Create a local `.env` file in the project root. See the next section for the required configuration.

### 4. Configure the Database

Create a MySQL database and configure the database connection using local credentials. Do not commit passwords or other secrets to version control.

### 5. Apply Migrations

```bash
pipenv run python manage.py migrate
```

### 6. Create an Administrator

```bash
pipenv run python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
pipenv run python manage.py runserver
```

The local development server is available at:

http://127.0.0.1:8000/

## Environment Configuration

The Django secret key is loaded through `python-decouple`:

```python
SECRET_KEY = config('SECRET_KEY')
```

The `.env` file should remain local and must not be committed to GitHub.

Example structure:

```dotenv
SECRET_KEY=replace-with-a-new-local-secret
```

Generate a new secret key for your environment and keep it private.

The current settings also configure MySQL credentials. Before distributing the project, move database connection details into environment variables as well, and update `settings.py` to read them. Do not publish real database passwords.

## Current Limitations

This repository represents a project under active development.

- Order and order-item models exist, but a complete order-creation API is not included in the provided implementation.
- Payment status values are modeled, but payment processing is not implemented.
- The likes application currently defines its data model; a complete likes API is not included in the provided code.
- Promotion data is modeled, but a complete promotion-management API is not included.
- Automated test coverage and production deployment configuration remain to be developed.
- Authentication and authorization behavior should be validated with automated tests before production use.

## Future Improvements

- Add automated unit and API tests.
- Improve validation and error handling.
- Add comprehensive API documentation, for example with OpenAPI.
- Strengthen customer ownership and authorization rules.
- Complete order creation and order-item workflows.
- Implement promotion and likes endpoints.
- Add continuous integration using GitHub Actions.
- Improve production settings, logging, and deployment configuration.
- Add deployment instructions and example API requests and responses.

## License

No license has been specified for this repository yet. All rights are reserved by default unless a license is added. Please contact the repository owner for permission to reuse or redistribute the code.