"""
Flask Web Application for PassForge V7.

Provides web routes for public security tools, personal credential vault,
authentication, security health assessments, and admin user management.
"""

import base64
import os
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from passforge.analyzer import analyze_password
from passforge.auth import (
    admin_required,
    authenticate_user,
    login_required,
    register_user,
)
from passforge.generator import MIN_PASSWORD_LENGTH, generate_passphrase, generate_password
from passforge.models import (
    get_all_users,
    get_audit_events,
    get_user_by_id,
    get_user_count,
    init_db,
    log_audit_event,
    set_user_active_status,
)
from passforge.security import PBKDF2_ITERATIONS, hash_password, verify_password
from passforge.vault import (
    add_credential,
    analyze_user_vault,
    decrypt_secret,
    delete_credential,
    get_credential_by_id,
    get_user_credentials,
    update_credential,
)

# Determine root directories relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
)

# Configuration via environment variables with safe defaults
app.config["SECRET_KEY"] = os.getenv(
    "PASSFORGE_SECRET_KEY", "passforge_educational_secret_key_v7"
)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Initialize database tables on startup
init_db()


def get_client_ip():
    """Retrieve client IP address from request."""
    return request.remote_addr or "127.0.0.1"


def get_session_vault_key() -> bytes:
    """Retrieve derived session vault key from Flask session."""
    key_b64 = session.get("vault_key_b64", "")
    return base64.b64decode(key_b64) if key_b64 else b""


# ============================================================
# PUBLIC ROUTES
# ============================================================


@app.route("/")
def index():
    """Render public landing page."""
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Render registration form and process new user account creation."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    success, msg = register_user(
        username=username,
        email=email,
        password=password,
        ip_address=get_client_ip(),
    )

    if not success:
        return render_template(
            "register.html",
            error=msg,
            username=username,
            email=email,
        )

    flash("Account created successfully. Please log in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Render login form and process user authentication."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    identifier = request.form.get("identifier", "")
    password = request.form.get("password", "")

    success, msg, user, vault_key = authenticate_user(
        identifier=identifier,
        password=password,
        ip_address=get_client_ip(),
    )

    if not success or not user or not vault_key:
        return render_template("login.html", error=msg, identifier=identifier)

    # Establish session
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["vault_key_b64"] = base64.b64encode(vault_key).decode("utf-8")

    flash(f"Welcome back, {user['username']}!", "success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    """Clear session and log user out."""
    if "user_id" in session:
        log_audit_event(
            user_id=session.get("user_id"),
            username=session.get("username", "Unknown"),
            event_type="LOGOUT",
            ip_address=get_client_ip(),
        )
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ============================================================
# SECURITY TOOL ROUTES (Public / Reused Core Logic)
# ============================================================


@app.route("/generate", methods=["GET", "POST"])
def generate():
    """Render password generator page and handle password generation requests."""
    if request.method == "GET":
        return render_template(
            "generate.html",
            default_length=16,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=True,
            mode="password",
        )

    mode = request.form.get("mode", "password")
    length_input = request.form.get("length", "16").strip()
    num_words_input = request.form.get("num_words", "4").strip()

    # Default all character sets to True if none were explicitly sent in POST form
    if (
        "use_uppercase" not in request.form
        and "use_lowercase" not in request.form
        and "use_digits" not in request.form
        and "use_symbols" not in request.form
    ):
        use_uppercase = True
        use_lowercase = True
        use_digits = True
        use_symbols = True
    else:
        use_uppercase = request.form.get("use_uppercase") == "on"
        use_lowercase = request.form.get("use_lowercase") == "on"
        use_digits = request.form.get("use_digits") == "on"
        use_symbols = request.form.get("use_symbols") == "on"

    try:
        if mode == "passphrase":
            num_words = int(num_words_input)
            pwd = generate_passphrase(num_words=num_words)
            length = len(pwd)
            uppercase_count = sum(1 for c in pwd if c.isupper())
            lowercase_count = sum(1 for c in pwd if c.islower())
            digit_count = sum(1 for c in pwd if c.isdigit())
            special_count = sum(1 for c in pwd if not c.isalnum())
        else:
            length = int(length_input)
            if length < MIN_PASSWORD_LENGTH:
                return render_template(
                    "generate.html",
                    error=f"Password length must be at least {MIN_PASSWORD_LENGTH} characters.",
                    default_length=length_input,
                    use_uppercase=use_uppercase,
                    use_lowercase=use_lowercase,
                    use_digits=use_digits,
                    use_symbols=use_symbols,
                    mode=mode,
                )

            pwd = generate_password(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_digits=use_digits,
                use_symbols=use_symbols,
            )

            uppercase_count = sum(1 for c in pwd if c.isupper())
            lowercase_count = sum(1 for c in pwd if c.islower())
            digit_count = sum(1 for c in pwd if c.isdigit())
            special_count = sum(1 for c in pwd if not c.isalnum())

        if "user_id" in session:
            log_audit_event(
                user_id=session["user_id"],
                username=session["username"],
                event_type="PASSWORD_GENERATED",
                ip_address=get_client_ip(),
            )

        return render_template(
            "generate.html",
            generated_password=pwd,
            length=length,
            uppercase_count=uppercase_count,
            lowercase_count=lowercase_count,
            digit_count=digit_count,
            special_count=special_count,
            default_length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_digits=use_digits,
            use_symbols=use_symbols,
            mode=mode,
        )

    except ValueError as err:
        return render_template(
            "generate.html",
            error=str(err),
            default_length=16,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_digits=use_digits,
            use_symbols=use_symbols,
            mode=mode,
        )


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    """Render password analyzer page and process password analysis requests."""
    if request.method == "GET":
        return render_template("analyze.html")

    password = request.form.get("password", "")

    if not password:
        return render_template(
            "analyze.html", error="Please enter a password to analyze."
        )

    try:
        result = analyze_password(password)
        return render_template("analyze.html", result=result)
    except ValueError as err:
        return render_template("analyze.html", error=str(err))


@app.route("/hash", methods=["GET", "POST"])
def hash_view():
    """Render password hashing page and process PBKDF2 hash requests."""
    if request.method == "GET":
        return render_template("hash.html")

    password = request.form.get("password", "")

    if not password:
        return render_template(
            "hash.html", error="Please enter a password to hash."
        )

    try:
        salt, pwd_hash = hash_password(password)
        return render_template(
            "hash.html",
            algorithm="PBKDF2-HMAC-SHA256",
            iterations=PBKDF2_ITERATIONS,
            salt=salt,
            hash=pwd_hash,
        )
    except ValueError as err:
        return render_template("hash.html", error=str(err))


@app.route("/verify", methods=["GET", "POST"])
def verify():
    """Render verification page and process password verification requests."""
    if request.method == "GET":
        return render_template("verify.html")

    password = request.form.get("password", "")
    salt = request.form.get("salt", "").strip()
    pwd_hash = request.form.get("hash", "").strip()

    if not password or not salt or not pwd_hash:
        return render_template(
            "verify.html",
            error="Unable to process the supplied values. Password, salt, and hash are all required.",
            stored_salt=salt,
            stored_hash=pwd_hash,
        )

    try:
        is_valid = verify_password(password, salt, pwd_hash)
        return render_template(
            "verify.html",
            success=is_valid,
            stored_salt=salt,
            stored_hash=pwd_hash,
        )
    except Exception:
        return render_template(
            "verify.html",
            error="Unable to process the supplied values. Please check salt and hash formats.",
            stored_salt=salt,
            stored_hash=pwd_hash,
        )


# ============================================================
# AUTHENTICATED USER ROUTES
# ============================================================


@app.route("/dashboard")
@login_required
def dashboard():
    """Render authenticated user security overview dashboard."""
    user_id = session["user_id"]
    key = get_session_vault_key()

    health = analyze_user_vault(user_id, key)
    credentials = get_user_credentials(user_id)

    return render_template(
        "dashboard.html",
        health=health,
        recent_credentials=credentials[:5],
    )


@app.route("/vault")
@login_required
def vault():
    """Render user credential vault list."""
    user_id = session["user_id"]
    credentials = get_user_credentials(user_id)
    return render_template("vault.html", credentials=credentials)


@app.route("/vault/add", methods=["GET", "POST"])
@login_required
def vault_add():
    """Render form and handle adding a new credential to vault."""
    if request.method == "GET":
        preset_pwd = request.args.get("preset_pwd", "")
        return render_template(
            "vault_form.html", action="add", preset_password=preset_pwd
        )

    service_name = request.form.get("service_name", "").strip()
    username_or_email = request.form.get("username_or_email", "").strip()
    password = request.form.get("password", "")
    url = request.form.get("url", "").strip()
    notes = request.form.get("notes", "").strip()

    if not service_name or not username_or_email or not password:
        return render_template(
            "vault_form.html",
            action="add",
            error="Service Name, Username/Email, and Password are required.",
            service_name=service_name,
            username_or_email=username_or_email,
            url=url,
            notes=notes,
        )

    user_id = session["user_id"]
    key = get_session_vault_key()

    add_credential(
        user_id=user_id,
        service_name=service_name,
        username_or_email=username_or_email,
        plaintext_password=password,
        key=key,
        url=url,
        notes=notes,
    )

    log_audit_event(
        user_id=user_id,
        username=session["username"],
        event_type="CREDENTIAL_CREATED",
        ip_address=get_client_ip(),
    )

    flash(f"Credential for '{service_name}' added to vault.", "success")
    return redirect(url_for("vault"))


@app.route("/vault/edit/<int:cred_id>", methods=["GET", "POST"])
@login_required
def vault_edit(cred_id: int):
    """Render form and handle updating an existing credential."""
    user_id = session["user_id"]
    key = get_session_vault_key()

    cred = get_credential_by_id(cred_id, user_id)
    if not cred:
        flash("Credential not found.", "danger")
        return redirect(url_for("vault"))

    if request.method == "GET":
        return render_template(
            "vault_form.html",
            action="edit",
            cred_id=cred_id,
            service_name=cred["service_name"],
            username_or_email=cred["username_or_email"],
            url=cred["url"],
            notes=cred["notes"],
        )

    service_name = request.form.get("service_name", "").strip()
    username_or_email = request.form.get("username_or_email", "").strip()
    password = request.form.get("password", "")
    url = request.form.get("url", "").strip()
    notes = request.form.get("notes", "").strip()

    if not service_name or not username_or_email:
        return render_template(
            "vault_form.html",
            action="edit",
            cred_id=cred_id,
            error="Service Name and Username/Email are required.",
            service_name=service_name,
            username_or_email=username_or_email,
            url=url,
            notes=notes,
        )

    update_credential(
        cred_id=cred_id,
        user_id=user_id,
        service_name=service_name,
        username_or_email=username_or_email,
        key=key,
        plaintext_password=password if password else None,
        url=url,
        notes=notes,
    )

    log_audit_event(
        user_id=user_id,
        username=session["username"],
        event_type="CREDENTIAL_UPDATED",
        ip_address=get_client_ip(),
    )

    flash(f"Credential for '{service_name}' updated successfully.", "success")
    return redirect(url_for("vault"))


@app.route("/vault/delete/<int:cred_id>", methods=["POST"])
@login_required
def vault_delete(cred_id: int):
    """Delete a credential from vault."""
    user_id = session["user_id"]
    cred = get_credential_by_id(cred_id, user_id)

    if cred and delete_credential(cred_id, user_id):
        log_audit_event(
            user_id=user_id,
            username=session["username"],
            event_type="CREDENTIAL_DELETED",
            ip_address=get_client_ip(),
        )
        flash("Credential deleted.", "info")
    else:
        flash("Credential not found.", "danger")

    return redirect(url_for("vault"))


@app.route("/vault/reveal/<int:cred_id>", methods=["POST"])
@login_required
def vault_reveal(cred_id: int):
    """Decrypt and return plaintext password for authorized owner."""
    user_id = session["user_id"]
    key = get_session_vault_key()

    if not key:
        return jsonify({"error": "Unauthorized active session."}), 401

    cred = get_credential_by_id(cred_id, user_id)
    if not cred:
        return jsonify({"error": "Credential not found."}), 404

    try:
        decrypted_pwd = decrypt_secret(cred["encrypted_password"], key)
        return jsonify({"password": decrypted_pwd})
    except Exception:
        return jsonify({"error": "Decryption failed."}), 500


@app.route("/security")
@login_required
def security_health():
    """Render detailed password health assessment for user vault."""
    user_id = session["user_id"]
    key = get_session_vault_key()

    health = analyze_user_vault(user_id, key)
    return render_template("security.html", health=health)


@app.route("/settings")
@login_required
def settings():
    """Render account settings page."""
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    return render_template("settings.html", user=user)


# ============================================================
# ADMIN ROUTES
# ============================================================


@app.route("/admin")
@admin_required
def admin_dashboard():
    """Render administrator overview dashboard."""
    total_users, active_users = get_user_count()
    events = get_audit_events(limit=10)
    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        active_users=active_users,
        recent_events=events,
    )


@app.route("/admin/users")
@admin_required
def admin_users():
    """Render user management table."""
    users = get_all_users()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/toggle/<int:user_id>", methods=["POST"])
@admin_required
def admin_user_toggle(user_id: int):
    """Toggle user active status (activate/deactivate)."""
    user = get_user_by_id(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin_users"))

    if user["id"] == session["user_id"]:
        flash("You cannot deactivate your own admin account.", "warning")
        return redirect(url_for("admin_users"))

    new_status = not bool(user["is_active"])
    set_user_active_status(user_id, new_status)

    log_audit_event(
        user_id=session["user_id"],
        username=session["username"],
        event_type=f"USER_{'ACTIVATED' if new_status else 'DEACTIVATED'}",
        ip_address=get_client_ip(),
    )

    flash(
        f"User '{user['username']}' status changed to {'Active' if new_status else 'Deactivated'}.",
        "success",
    )
    return redirect(url_for("admin_users"))


@app.route("/admin/activity")
@admin_required
def admin_activity():
    """Render security audit event log table."""
    events = get_audit_events(limit=200)
    return render_template("admin/activity.html", events=events)


def run_web(host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
    """Run Flask web application server."""
    print(f"Starting PassForge Web Application on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_web(debug=True)
