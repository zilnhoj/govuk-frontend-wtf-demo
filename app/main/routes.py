from flask import flash, json, make_response, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException
from bokeh.plotting import figure
from bokeh.embed import components

from app.main import bp
from app.main.forms import BankDetailsForm, ConditionalRevealForm, CreateAccountForm, KitchenSinkForm

from app.main import bp
# from app.main.forms import CookiesForm




@bp.route("/", methods=["GET"])
def index():
    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot)
    print(script)
    return render_template("index.html", script=script, div=div)

@bp.route("/start", methods=["GET"])
def start():
    return render_template("start.html")

@bp.route("/date", methods=["GET", "POST"])
def date():
    form = KitchenSinkForm()
    if form.validate_on_submit():

    # if form.submit_button():
        print('in validate on submit if statement')
        flash("Form successfully submitted", "success")
        # return redirect("choose-circuit.html")
        return redirect(url_for("main.choose_circuit"))
    print('outside of validate on submit if statement')
    return render_template("date.html", form=form, date=form.validate_on_submit())


@bp.route("/choose-circuit", methods=["GET", "POST"])
def choose_circuit():
    form = KitchenSinkForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        return redirect(url_for("main.index"))
    return render_template("choose-circuit.html", form=form, circuit_choice=form.validate_on_submit())

@bp.route("/review", methods=["GET", "POST"])
def review():
    form = KitchenSinkForm()
    if form.validate_on_submit():
        flash("Form successfully submitted", "success")
        return redirect(url_for("main.index"))
    return render_template("review.html", form=form)

# @bp.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Headers'] = '*'
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Content-Security-Policy'] = "default-src 'self';"
#     return response

# @bp.route("/forms/kitchen-sink", methods=["GET", "POST"])
# def kitchen_sink():
#     form = KitchenSinkForm()
#     if form.validate_on_submit():
#         flash("Form successfully submitted", "success")
#         return redirect(url_for("main.index"))
#     return render_template("kitchen_sink.html", form=form)


# @bp.route("/forms/conditional-reveal", methods=["GET", "POST"])
# def conditional_reveal():
#     form = ConditionalRevealForm()
#     if form.validate_on_submit():
#         flash("Form successfully submitted", "success")
#         return redirect(url_for("main.index"))
#     return render_template("conditional_reveal.html", form=form)

@bp.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("accessibility.html")


@bp.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookiesForm()
    # Default cookies policy to reject all categories of cookie
    cookies_policy = {"functional": "no", "analytics": "no"}

    if form.validate_on_submit():
        # Update cookies policy consent from form data
        cookies_policy["functional"] = form.functional.data
        cookies_policy["analytics"] = form.analytics.data

        # Create flash message confirmation before rendering template
        flash("You’ve set your cookie preferences.", "success")

        # Create the response so we can set the cookie before returning
        response = make_response(render_template("cookies.html", form=form))

        # Set cookies policy for one year
        response.set_cookie("cookies_policy", json.dumps(cookies_policy), max_age=31557600)
        return response
    elif request.method == "GET":
        if request.cookies.get("cookies_policy"):
            # Set cookie consent radios to current consent
            cookies_policy = json.loads(request.cookies.get("cookies_policy"))
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
        else:
            # If conset not previously set, use default "no" policy
            form.functional.data = cookies_policy["functional"]
            form.analytics.data = cookies_policy["analytics"]
    return render_template("cookies.html", form=form)


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    if error.code == 404:
        return render_template("404.html"), error.code
    elif error.code == 500:
        return render_template("500.html"), error.code
    elif error.code == 503:
        return render_template("503.html"), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.", "info")
    return redirect(request.full_path)
