<h1 align="center">Simple Social Media App</h1>
This is a Django REST API project that provides functionalities for users to interact with posts and comments.

## Features

- **Public access:**
    - View all existing posts and comments.
    - Search for posts and comments by content and author username.
    - View user information by username.<br><br>
- **Authenticated user access:**
    - Create new posts and comments.
    - Like/unlike existing posts and comments.
    - Update and delete posts and comments (requires being the author).
    - Update user information (excluding username).
    - Change password (requires old password).<br><br>
- **User registration and login/logout:**
    - Users can register for new accounts.
    - Existing users can log in and logout.<br><br>
- **Follow and unfollow users:**
    - Users can follow and unfollow other users.
    - View all users followed by the authenticated user.
    - View all users following the authenticated user.<br><br>
- **Posts of followings:**
    - Users can view posts from the users they are following.<br><br>
- **User profile:**
    - Each user has a profile associated with their account
    - The profile includes a bio, birthdate, and a profile picture.
    - The profile picture is stored in the 'avatars/' directory<br><br>
- **Comments and replies:**
    - Users can create comments on posts.
    - Users can create replies to comments.
    - Users can view all replies to a specific comment.<br><br>

### Technologies

- Django (web framework)
- Django REST framework (API development toolkit)
- Django Filter (filtering library)

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

| Method |              URL Path              |                           Description                           |
|:------:|:----------------------------------:|:---------------------------------------------------------------:|
|  GET   |       `/posts/:id/comments/`       |            Retrieve all comments for a specific post            |
|  POST  |       `/posts/:id/comments/`       |      Create a comment on a post (requires authentication)       |
|  GET   |     `/posts/:id/comments/:pk/`     |                Retrieve a specific comment by ID                |
|  PUT   |     `/posts/:id/comments/:pk/`     | Update a comment (requires authentication and being the author) |
| DELETE |     `/posts/:id/comments/:pk/`     | Delete a comment (requires authentication and being the author) |
|  PUT   |  `/posts/:id/comments/:pk/like/`   |    Like/Unlike a specific comment (requires authentication)     |
|  GET   | `/posts/:id/comments/:id/replies/` |           Retrieve all replies for a specific comment           |
|  POST  | `/posts/:id/comments/:id/replies/` |              Create a reply to a specific comment               |

- **Users:**

| Method |          URL Path           |                         Description                         |
|:------:|:---------------------------:|:-----------------------------------------------------------:|
|  GET   |         `/account/`         | Retrieve information about the currently authenticated user |
|  POST  |         `/account/`         |        Update user information (excluding username)         |
|  PUT   |    `/account/register/`     |                     Register a new user                     |
|  PUT   |      `/account/login/`      |                   Login an existing user                    |
|  PUT   |     `/account/logout/`      |                Logout from existing account                 |
|  PUT   | `/account/password-change/` |        Change user password (requires old password)         |

- **Search:**
You can now search for posts and comments based on their content and the author's username.

| Method |                 URL Path                 |                                   Description                                   |
|:------:|:----------------------------------------:|:-------------------------------------------------------------------------------:|
|  GET   |        `/posts/?search=something`        |               Use the search query parameter in the URL for posts               |
|  GET   | `/posts/:id/comments/?search=something/` | Use the search query parameter within the comments endpoint for a specific post |
|  GET   |      `/users/?username=something/`       |            Use the search query parameter within the users endpoint             |

The search is case-insensitive and will return results matching the search term in the content or author's username of posts or comments.

- **Follow:**

| Method |            URL Path            |                      Description                      |
|:------:|:------------------------------:|:-----------------------------------------------------:|
|  GET   |  `/users/profile/followings/`  | Retrieve all users followed by the authenticated user |
|  GET   |  `/users/profile/followers/`   |  Retrieve all users following the authenticated user  |
|  PUT   |   `/users/:username/follow/`   |                Follow/Unfollow a user                 |
|  GET   | `/users/:username/followers/`  |     Retrieve all users following a specific user      |
|  GET   | `/users/:username/followings/` |    Retrieve all users followed by a specific user     |

## Testing

The application includes a comprehensive suite of tests to ensure all functionalities work as expected. Here are the main test cases:

#### Users:
- **User Registration:**
    - Test user registration with valid and invalid data.
    - Test user registration without a password.
    - Test user registration without a username.
    - Test user registration without a confirmation password.
    - Test user registration with mismatched passwords.
    - Test user registration without an email.
    - Test user registration without a first name.
    - Test user registration without a last name.<br><br>

- **User Login:**
    - Test user login with valid and invalid data.
    - Test user login without a username.
    - Test user login without a password.
    - Test user login with a wrong password.
    - Test user login with a wrong username.<br><br>

- **User Logout:**
    - Test user logout.
    - Test user logout when unauthenticated.<br><br>

- **User Follow System:**
    - Test following a user.
    - Test following a user when unauthenticated.
    - Test unfollowing a user.
    - Test unfollowing a user when unauthenticated.
    - Test following a user that does not exist.<br><br>

- **User Profile:**
    - Test showing a user profile.
    - Test showing a user profile when unauthenticated.
    - Test showing a user that does not exist.<br><br>

#### Posts:
- **Posts:**
    - Test retrieving all posts.
    - Test creating a new post.
    - Test updating a post.
    - Test deleting a post.
    - Test searching for posts.
    - Test creating a post when unauthenticated.
    - Test updating a post when not the author.<br><br>

- **Comments:**
    - Test retrieving all comments for a specific post.
    - Test creating a new comment on a post.
    - Test updating a comment.
    - Test deleting a comment.
    - Test searching for comments within a specific post.
    - Test creating a comment when unauthenticated.
    - Test updating a comment when not the author.<br><br>

- **Likes:**
    - Test liking a post.
    - Test unliking a post.
    - Test liking a comment.
    - Test unliking a comment.
    - Test liking a post when unauthenticated.
    - Test unliking a post when unauthenticated.
    - Test liking a comment when unauthenticated.
    - Test unliking a comment when unauthenticated.<br><br>

To run the tests, use the following command:

```bash
python manage.py test
```

**Note:**
This project is under development, and I'm working on improving the features and functionalities.