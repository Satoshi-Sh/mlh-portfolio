import os
from flask import Flask, render_template, render_template_string, request, abort
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
from app.utils.gravatar import get_gravatar_url
import re


load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


work_experiences = [
    {
        "position": "Frontend Developer",
        "company": "Ori.Gatou Creative Solution Inc. - Apprenticeship",
        "date": "2023 Jul - 2023 Sep",
        "detail": [
            "Created reactive data analytics dashboard with Svelte and D3.js.",
            "Integrated a backend API to fetch data with the front end.",
        ],
    },
    {
        "position": "React Teaching Assistant",
        "company": "ComIT",
        "date": "2023 Sep - 2023 Dec",
        "detail": [
            "Provide additional assistance to students in troubleshooting, understanding course materials, and completing assignments through chat and video calls.",
            "Maintain attendance records and communicate with the instructor and program coordinators to address student absences and issues related to class participation.",
        ],
    },
    {
        "position": "Web Dev Intern",
        "company": "North York Arts",
        "date": "2023 Jul - 2023 Sep",
        "detail": [
            "Contributed to the successful launch of a website rebrand by implementing design concepts, resulting in improved aesthetics and user experience.",
            "Optimized website performance by minimizing page load times, resulting in an improved user experience and increase in user engagement.",
        ],
    },
]

hobbies = [
    {
        "description": "Making Music with Guitar and Piano",
        "img_path": "./static/img/piano-man.jpg",
        "img_alt_text": "Playing the public piano",
    },
    {
        "description": "Soccer is the greatest!",
        "img_path": "./static/img/greatest-sport.jpg",
        "img_alt_text": "Soccer ball on field",
    },
    {
        "description": "Shogi - Japanese Chess",
        "img_path": "./static/img/shogi-game.jpg",
        "img_alt_text": "Shogi board game",
    },
]

education = [
    {
        "institution": "ComIT",
        "program": "Node Js Course",
        "date": "2023 Jun - 2023 Sep",
    },
    {
        "institution": "Osaka University",
        "program": "Economics, Economics and Management",
        "date": "2010 Apr - 2014 Mar",
    },
    {
        "institution": "Wilfrid Laurier University",
        "program": "Computer Science",
        "date": "2020 Sep - 2025 Apr",
    },
]

# Views


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        work_experiences=work_experiences,
        hobbies=hobbies,
        education=education,
        url=os.getenv("URL"),
    )


@app.route("/hobbies")
def hobby_page():
    return render_template(
        "hobbies.html", title="My Hobbies", hobbies=hobbies, url=os.getenv("URL")
    )


@app.route("/health")
def headl_check():
    TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template(
        "index.html",
        title="MLH Fellow",
        work_experiences=work_experiences,
        hobbies=hobbies,
        education=education,
        url=os.getenv("URL"),
    )


@app.route("/timeline")
def timeline():
    all_posts = []
    for p in TimelinePost.select().order_by(TimelinePost.created_at.desc()):
        p = model_to_dict(p)
        p["gravatar_url"] = get_gravatar_url(p["email"])
        all_posts.append(p)
    return render_template(
        "timeline.html", title="Timeline", url=os.getenv("URL"), all_posts=all_posts
    )


# API


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    messages = []
    code = None
    name = request.form.get("name", "")
    if len(name) == 0:
        messages.append("Invalid name")
        code = 400
    email = request.form.get("email", "")
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        messages.append("Invalid email")
        code = 400
    content = request.form.get("content", "")
    if len(content) == 0:
        messages.append("Invalid content")
        code = 400
    if len(messages) > 0:
        abort(code, description=", ".join(messages))
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post/<id>", methods=["DELETE"])
def delete_time_line_post(id):
    deleted_post = TimelinePost.delete_by_id(id)
    if deleted_post:
        return {"message": f"Post {id} was deleted."}
    return {"message": f"Post {id} doesn't exist"}


# errorr Handlers
@app.errorhandler(400)
def handle_400_error(e):
    custom_message = (
        e.description
        if e.description
        else "The browser (or proxy) sent a request that this server could not understand"
    )
    error_html = f"""
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>400 Bad Request</title>
    <h1>Bad Request</h1>
    <p>{custom_message}</p>
    """
    return render_template_string(error_html), 400
