import httpx
from fasthtml.common import *
from fasthtml.fastapp import *
import requests

app, rt = fast_app()

access_token = ""


@rt('/')
async def redirect_to_splash():
    return Redirect("/splash")

# splash screen
@rt('/splash')
async def splash():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Meta(name="description", content="Clinic Registration System for students"),  # Added meta description
            Link(rel="stylesheet", href="/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
            Title('Clinic Registration System')
        ),
        Body(
            Div(
                # The main splash screen content starts here
                Div(
                    Img(src="/images/uni_logo.png"),
                    H1("Welcome here!", _class="title"),
                    H3("Clinic Registration System", _class="sub-title"),
                ),
                P("Loading...", _class="loader"),
                _class="splash-container"
            ),
            # HTMX to trigger the page change after 3 seconds (3000 milliseconds)
            Script('''setTimeout(function() { window.location.href = '/login'; }, 3000);'''),
        ),
    )

# Login Screen
@rt('/login')
async def login_page():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Meta(name="description", content="Login to access the Clinic Registration System"),
            Link(rel="stylesheet", href="/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
        ),
        Body(
            Div(
                Img(src="/images/1.png", alt="Logo", _class="logo"),
                H2("Login", _class="form-title"),
                Div(
                    Form(
                        Div(
                            Label("Matriculation number:"),
                            Input(type="text", name="username", placeholder="Enter your matric number", required=True),
                        ),
                        Div(
                            Label("Password:"),
                            Input(type="password", name="password", placeholder="Enter your password", required=True),
                        ),
                        Button("Login", type="submit"),
                        hx_post="/handle_login",  # Changed to point to the new route
                        hx_swap="outerHTML",  # Replace the entire form on response
                        _class="glass-box"
                    ),
                    P(
                        A("Create Account", href="/create-account"), "|",
                        A("Forgot Password?", href="/recover-password"),
                    ),
                    _class="form-container"
                ),
                _class="login-container"
            ),
        )
    )


@rt('/handle_login', methods=['POST'])
async def handle_login(request):
    form_data = await request.form()
    username = form_data.get('username')
    password = form_data.get('password')
    print(f"Username: {username}, Password: {password}")  # Debug line

    # Send a POST request to the authentication API
    response = requests.post("http://127.0.0.1:8008/login/student", data={
        "username": username.upper(),
        "password": password.lower()
    })

    # Check if authentication was successful
    if response.status_code == 200:
        print("Login successful")  # Debug line
        access_token = response.json().get('access_token')
        print(response.json())
        return Redirect("/dashboard")
    else:
        print("Login failed")  # Debug line
        return Html(
            Div(
                H2("Login Failed", _class="error-title"),
                P("Invalid credentials. Please try again."),
                A("Back to Login", href="/login"),
                _class="error-container"
            )
        )


# Create Account
@rt('/create-account')
async def create_account():
    faculties = [{"faculty_name": "Unknown Faculty"}]
    levels = [{"level_name": "Unknown Level"}]
    sessions = [{"academic_session": "Unknown Session"}]
    try:
        # Fetch faculties, levels, and sessions from the API
        faculties = requests.get("http://127.0.0.1:8008/faculty/read-faculties/").json()
        levels = requests.get("http://127.0.0.1:8008/level/read-levels/").json()
        sessions = requests.get("http://127.0.0.1:8008/sessions/read-sessions/").json()
    except requests.RequestException as e:
        print(f"API request failed: {e}")

    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Meta(name="description", content="Create an account for the Clinic Registration System"),
            Link(rel="stylesheet", href="/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
        ),
        Body(
            Div(
                H2("Create Account", _class="form-title"),
                Div(
                    Form(
                        Div(
                            Label("Full Name"),
                            Input(type="text", name="name", placeholder="Full Name", required=True),
                        ),
                        Div(
                            Label("Matriculation Number"),
                            Input(type="text", name="matriculation_number", placeholder="Matriculation Number", required=True),
                        ),
                        Div(
                            Label("Email"),
                            Input(type="email", name="email", placeholder="Email", required=True),
                        ),
                        Div(
                            Label("Phone"),
                            Input(type="text", name="phone", placeholder="Phone", required=True),
                        ),
                        Div(
                            Label("Date of Birth"),
                            Input(type="date", name="date_of_birth", required=True),
                        ),
                        Div(
                            Label("Gender"),
                            Div(
                                Input(type="radio", name="gender", value="Male", required=True),
                                Label("Male"),
                                Input(type="radio", name="gender", value="Female", required=True),
                                Label("Female"),
                            ),
                        ),
                        Div(
                            Label("Faculty"),
                            Select(
                                Option("Select Faculty", value=""),
                                *[Option(faculty['faculty_name'], value=faculty['faculty_name']) for faculty in faculties],
                                name="faculty",
                                id="faculty-dropdown",
                                hx_trigger="change",
                                hx_post="/fetch-departments",
                                hx_target="#department-dropdown",
                                required=True
                            ),
                        ),
                        Div(
                            Label("Department"),
                            Select(
                                Option("Select Department", value=""),
                                name="department",
                                id="department-dropdown",
                                required=True
                            ),
                        ),
                        Div(
                            Label("Academic Year"),
                            Select(
                                Option("Select Academic Year", value=""),
                                *[Option(session['academic_session'], value=session['academic_session']) for session in sessions],
                                name="academic_year",
                                required=True
                            ),
                        ),
                        Div(
                            Label("Level"),
                            Select(
                                Option("Select Level", value=""),
                                *[Option(level['level_name'], value=level['level_name']) for level in levels],
                                name="level",
                                required=True
                            ),
                        ),
                        Div(
                            Label("Password"),
                            Input(type="password", name="password", placeholder="Password", required=True),
                        ),
                        Div(
                            Label("Address"),
                            Input(type="text", name="address", placeholder="Address", required=True),
                        ),
                        Div(
                            Label("Emergency Contact"),
                            Input(type="text", name="emergency_contact", placeholder="Emergency Contact", required=True),
                        ),
                        Div(
                            Label("Profile Picture (Optional)"),
                            Input(type="file", name="profile_picture", placeholder="Profile Picture (Optional)"),
                        ),
                        Button("Signup", type="submit"),
                        hx_post="/handle-account",
                        hx_swap="outerHTML",
                        _class="glass-box"
                    ),
                    P(
                        A("Create Account", href="/create-account"), "|",
                        A("Forgot Password?", href="/recover-password"),
                    ),
                    _class="signup-container"
                ),
                _class="login-container"
            ),
        )
    )

# POST handler for create account
@rt('/handle-account', methods=['POST'])
async def handle_create_account(request):
    form_data = await request.form()
    # Get form data
    user_data = {
        "name": form_data.get('name'),
        "matriculation_number": form_data.get('matriculation_number'),
        "email": form_data.get('email'),
        "phone": form_data.get('phone'),
        "date_of_birth": form_data.get('date_of_birth'),
        "gender": form_data.get('gender'),
        "faculty": form_data.get('faculty'),
        "department": form_data.get('department'),
        "academic_year": form_data.get('academic_year'),
        "level": form_data.get('level'),
        "password": form_data.get('password'),
        "address": form_data.get('address'),
        "emergency_contact": form_data.get('emergency_contact'),
        # Handle file uploads if necessary
    }
    print(user_data)

    # Send a POST request to the account creation API
    response = requests.post("http://127.0.0.1:8008/students/create-students/", json=user_data)

    if response.status_code == 201:  # Assuming 201 indicates success
        return Redirect("/login")  # Redirect to login after successful account creation
    else:
        # Handle account creation failure (e.g., display an error message)
        return Html(
            Head(
                Title('Account Creation Failed'),
                Link(rel="stylesheet", href="/css/style.css"),
            ),
            Body(
                Div(
                    H2("Account Creation Failed", _class="error-title"),
                    P("An error occurred while creating your account. Please try again."),
                    A("Back to Create Account", href="/create-account"),
                    _class="error-container"
                )
            )
        )


# Recover Password
@rt('/recover-password')
async def recover_password():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Meta(name="description", content="Recover your password for the Clinic Registration System"),
            Link(rel="stylesheet", href="/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
        ),
        Body(
            Div(
                H2("Recover Password", _class="form-title"),
                Div(
                    Form(
                        Div(
                            Input(type="email", name="email", placeholder="Enter your email", required=True),
                        ),
                        Button("Submit", type="submit"),
                        action="/recover-password", method="post", _class="glass-box"
                    ),
                    _class="form-container"
                ),
                _class="login-container"
            ),
        )
    )

# POST handler for recover password
@rt('/recover-password', methods=['POST'])
async def handle_recover_password():
    # Add logic to handle password recovery (e.g., sending password recovery email)

    pass



@rt('/dashboard')
async def dashboard():
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Link(rel="stylesheet", href="/css/style.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
        ),
        Body(
            Div(
                Img(src="/images/1.png", _class="logo"),  # Logo remains at top left

                # Student dashboard home content
                Div(
                    Div("Welcome to the Dashboard", _class="dashboard-content"),
                    _class="dashboard-container",
                    id="dashboard-content",
                ),

                # Floating bottom navigation with curved edges
                Div(

                    Button("Dashboard", _class="nav-button", id="home-btn", hx_get="/dashboard/home",
                           hx_target="#dashboard-content", _active=True),
                    Button("Student ID", _class="nav-button", id="card-btn", hx_get="/dashboard/card",
                           hx_target="#dashboard-content"),
                    Button("Clearance", _class="nav-button", id="clearance-btn", hx_get="/dashboard/clearance",
                           hx_target="#dashboard-content"),
                    _class="bottom-nav-container",
                ),

                # JavaScript to handle active state
                Script('''
                    document.querySelectorAll('.nav-button').forEach(button => {
                        button.addEventListener('click', function() {
                            document.querySelectorAll('.nav-button').forEach(btn => btn.classList.remove('active'));
                            this.classList.add('active');
                        });
                    });
                '''),
            ),
        )
    )


# Route for Home content
@rt('/dashboard/home')
async def dashboard_home():
    return Div(
        H2("Dashboard Home"),
        P("This is the Home section of the dashboard.")
    )


# Route for Card content
@rt('/dashboard/card')
async def dashboard_card():
    return Div(
        H2("Student Card"),
        P("This is the Card section of the dashboard.")
    )

# Route for Clearance content
@rt('/dashboard/clearance')
async def dashboard_clearance():
    return Div(
        H2("Clearance Status"),
        P("This is the Clearance section of the dashboard.")
    )


# Serve the application
serve()
