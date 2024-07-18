<h1 align="center">Simple Social Media App</h1>
This is a Django REST API project that provides functionalities for users to interact with posts and comments.

## Features

- **Public access:**
    - View all existing posts and comments.
- **Authenticated user access:**
    - Create new posts and comments.
    - Like/unlike existing posts and comments.
    - Update user information (excluding username).
    - Change password (requires old password).
- **User registration and login/logout:**
    - Users can register for new accounts.
    - Existing users can log in and logout.

### Technologies

- Django (web framework)
- Django REST framework (API development toolkit)

## Installation

1. Clone this repository:

   ```bash
   git clone https://your_github_repo_url.git
   ```

2. Create a virtual environment and activate it (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a Django secret key:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. (Optional) Create a superuser account (for initial data management):

   ```bash
   python manage.py createsuperuser
   ```

## Usage

1. Run the development server:

   ```bash
   python manage.py runserver
   ```

   This will start the server at http://127.0.0.1:8000/ by default.

2. Access the API endpoints using an API client or tools like Postman.

### Endpoints

- **Posts:**

| Method |      URL Path      |                         Description                          |
|:------:|:------------------:|:------------------------------------------------------------:|
|  GET   |     `/posts/`      |                      Retrieve all posts                      |
|  POST  |     `/posts/`      |         Create a new post (requires authentication)          |
|  GET   |   `/posts/:id/`    |                Retrieve a specific post by ID                |
|  PUT   |   `/posts/:id/`    | Update a post (requires authentication and being the author) |
| DELETE |   `/posts/:id/`    | Delete a post (requires authentication and being the author) |
|  Post  | `/posts/:id/like/` |    Like/Unlike a specific post (requires authentication)     |

- **Comments:**

| Method |            URL Path             |                           Description                           |
|:------:|:-------------------------------:|:---------------------------------------------------------------:|
|  GET   |     `/posts/:id/comments/`      |            Retrieve all comments for a specific post            |
|  POST  |     `/posts/:id/comments/`      |      Create a comment on a post (requires authentication)       |
|  GET   |   `/posts/:id/comments/:pk/`    |                Retrieve a specific comment by ID                |
|  PUT   |   `/posts/:id/comments/:pk/`    | Update a comment (requires authentication and being the author) |
| DELETE |   `/posts/:id/comments/:pk/`    | Delete a comment (requires authentication and being the author) |
|  PUT   | `/posts/:id/comments/:pk/like/` |    Like/Unlike a specific comment (requires authentication)     |

- **Users:**

| Method |          URL Path           |                         Description                         |
|:------:|:---------------------------:|:-----------------------------------------------------------:|
|  GET   |         `/account/`         | Retrieve information about the currently authenticated user |
|  POST  |         `/account/`         |        Update user information (excluding username)         |
|  PUT   |    `/account/register/`     |                     Register a new user                     |
|  PUT   |      `/account/login/`      |                   Login an existing user                    |
|  PUT   |     `/account/logout/`      |                Logout from existing account                 |
|  PUT   | `/account/password-change/` |        Change user password (requires old password)         |

**Note:**
This project is under development, and I'm working on improving the features and functionalities.