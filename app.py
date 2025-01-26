from jinja2 import Environment, FileSystemLoader
import yaml
from datetime import datetime

# Set up Jinja2 environment
env = Environment(
    loader=FileSystemLoader(".")
)  # Load templates from the current directory
template = env.get_template("template.j2")

courses_data = None
grand_coupon = None
grand_coupon_expiry = None

# Load the YAML file
with open("courses.yaml", "r") as file:
    courses_data = yaml.safe_load(file)
    grand_coupon = courses_data["grand_coupon"]
    grand_coupon_expiry = courses_data["grand_coupon_expiry"]


def valid_coupon(expiry_date):
    # Parse the expiry date string into a datetime object
    expiry_date_obj = datetime.strptime(expiry_date, "%d-%m-%Y")
    # Compare the expiry date with the current date
    return expiry_date_obj > datetime.now()


def generate_link(
    coupon_code, referral_code, course_link, use_grand_coupon, expiry_date
):
    if not expiry_date:  # Check if expiry date is not provided
        expiry_date = grand_coupon_expiry
    if coupon_code and valid_coupon(expiry_date):
        return course_link + "/?couponCode=" + coupon_code
    elif grand_coupon and use_grand_coupon and valid_coupon(grand_coupon_expiry):
        return course_link + "/?couponCode=" + grand_coupon
    else:
        return course_link + "/?referralCode=" + referral_code


# Access the courses data
for course in courses_data["courses"]:
    course["link"] = generate_link(
        course["coupon_code"],
        course["referral_code"],
        course["course_link"],
        course["use_grand_coupon"],
        course["coupon_expiry"],
    )

output = template.render(courses=courses_data["courses"])

# Save the rendered HTML to a file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print("Static HTML generated: index.html")
