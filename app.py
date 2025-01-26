from jinja2 import Environment, FileSystemLoader
import os
import yaml

# Set up Jinja2 environment
env = Environment(
    loader=FileSystemLoader(".")
)  # Load templates from the current directory
template = env.get_template("template.j2")

grand_coupon = "LDINFEB2025"


def generateLink(coupon_code, referral_code, course_link, use_grand_coupon=True):
    if coupon_code:
        return course_link + "/?couponCode=" + coupon_code
    elif grand_coupon and use_grand_coupon:
        return course_link + "/?couponCode=" + grand_coupon
    else:
        return course_link + "/?referralCode=" + referral_code


# Render the template with the courses data
# Load the YAML file
with open("courses.yaml", "r") as file:
    courses_data = yaml.safe_load(file)

# Access the courses data
for course in courses_data["courses"]:
    course["link"] = generateLink(
        course["coupon_code"], course["referral_code"], course["course_link"]
    )

output = template.render(courses=courses_data["courses"])

# Save the rendered HTML to a file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print("Static HTML generated: index.html")
