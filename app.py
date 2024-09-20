import requests

# GitLab API token (Replace with your own)
GITLAB_TOKEN = 'YOUR_GITLAB_ACCESS_TOKEN'

# GitLab project ID where the user will be added (Replace with your project ID)
PROJECT_ID = '3'

# Base GitLab API URL
GITLAB_API_BASE_URL = 'http://localhost/api/v4'

# Headers for the requests, including the private token
HEADERS = {
    'PRIVATE-TOKEN': GITLAB_TOKEN,
    'Content-Type': 'application/json'
}


def find_user_by_email(email):
    """Check if a user with the given email already exists in GitLab."""
    search_user_url = f"{GITLAB_API_BASE_URL}/users"
    response = requests.get(search_user_url, headers=HEADERS, params={'search': email})

    if response.status_code == 200:
        users = response.json()
        for user in users:
            if user['email'] == email:
                print(f"User '{user['username']}' already exists with ID: {user['id']}")
                return user['id']
        return None
    else:
        print(f"Failed to search for user: {response.status_code}, {response.text}")
        return None


def create_user(email, username, name, password):
    """Create a new GitLab user."""
    create_user_url = f"{GITLAB_API_BASE_URL}/users"
    
    user_data = {
        'email': email,
        'username': username,
        'name': name,
        'password': password,
        'skip_confirmation': True  # Skip email confirmation for faster setup
    }
    
    response = requests.post(create_user_url, headers=HEADERS, json=user_data)

    if response.status_code == 201:
        user_info = response.json()
        print(f"User '{name}' created successfully with ID: {user_info['id']}")
        return user_info['id']
    else:
        print(f"Failed to create user: {response.status_code}, {response.text}")
        return None


def add_user_to_project(user_id, project_id, access_level=30):
    """Add a user to the GitLab project."""
    add_member_url = f"{GITLAB_API_BASE_URL}/projects/{project_id}/members"
    
    member_data = {
        'user_id': user_id,
        'access_level': access_level  # Default to Developer access (30)
    }

    response = requests.post(add_member_url, headers=HEADERS, json=member_data)

    if response.status_code == 201:
        print(f"User with ID {user_id} added to project {project_id} successfully.")
    elif response.status_code == 409:
        print(f"User with ID {user_id} is already a member of the project.")
    else:
        print(f"Failed to add user to project: {response.status_code}, {response.text}")


def main():
    # Replace these values with the details of the new user
    email = 'themobinism@gmail.com'
    username = 'themobinism'
    name = 'The Mobinism'
    password = 'Hughjackman002!'  # Choose a strong password

    # Step 1: Check if the user already exists
    user_id = find_user_by_email(email)

    # Step 2: If the user does not exist, create the user
    if not user_id:
        user_id = create_user(email, username, name, password)

    # Step 3: Add the user to the GitLab project if we have a valid user ID
    if user_id:
        add_user_to_project(user_id, PROJECT_ID, access_level=30)  # Developer access


if __name__ == "__main__":
    main()
