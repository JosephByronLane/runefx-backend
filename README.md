![RuneFX Logo](assets/logo2-highres-wide.png)

# RuneFX Back-end
This repository contains the Back-end code for the RuneFX website, a (fake) VFX company.

## What is this?

This is my graduation project (or what was going to be my graduation project) for the bachelor of computer science at Universidad Modelo in Mexico. Sadly I didn't quite have enough time to finish this in time, so I ended up choosing to graduate by virtue of having good grades.

It started as an idea during our `Web Development` class that I fleshed out during the `Web Development II` class. As I had (What I thought) was a good base for a graduation project (web design, document requirements, pipeline, cloud, etc) I decided to keep working on it and make it my graduation project during my final semester. As you might of read above however, time caught up to me and I didn't manage to finish it in time, so I ended up graduating with good grades instead.

My plan was that once I was near graduating, I thought it would be fun (and for flexing rights) to have the 3 graduation options open to me (Even though you can only choose 1 to actually graduate with): By having a good GPA (90+/100, which I managed to achieve), by passing the graduation exam EGEL ISOFT (which  I passed as the top of my class), or by making a project so good that I could defend it against a board of judges (Similar to how you defend your thesis). 

## Why a VFX company?

I do 3D as a hobby (Mainly Blender and Houdini), and I wanted to make a website of what "my own vfx company" would look like. 
Coding/software keeps the tecnical and problem solving side of my brain happy, and 3D keeps the artistic, make cool looking stuff side of my brain happy.

## Tech stack

The whole project consisted of 4 main parts:
- **Front-end**: The front-end code, written in Angular, hosted on Netlify (because I didn't want to pay for hosting).
- **Back-end**: This is the back-end code, written in Python with Django, hosted on Google Cloud Platform (because I wanted to learn some Django, I didn't want to pay for hosting and GCP's Cloud Run free tier is generous enough that I'd pay pennies a month. I also could of just used their free  e3-micro instance, but eh).
- **Database**: The  database, hosted on Aiven, using PostgreSQL as the database engine (because I wanted to try out Postgres and Aiven has a free db tier).
- **Terraform  & CI/CD**: I'll admit, this isn't the most elaborate CI/CD pipeline or the biggest Terraform project I've done, but I wanted a measure so that if I somehow woke up with a 50+ USD bill I could just `terraform destroy`, send a support ticket to whoever billed me (GCP most likely) and be done with it. The CI/CD pipeline for the Front-end makes use of Netlify's automatic repository linking, and t he backend uses GitHub Actions.
If I do somehow end up with a huge bill, I'll just move all  API-side stuff into a huge json and host it on GitHub Pages or something.

## How to run this locally
Its as simple as it gets:

1. Clone the repository:
   ```bash
   git clone 
   ```

2. install Pipenv if you don't have it:
   ```bash
   pip install pipenv
   ```

3. Install the dependencies:
   ```bash
   pipenv install
   ```

4. Make the `.env` file according to whats in the `config.py` file.

5. Enter the pipenv shell:
   ```bash
   pipenv shell
   ```

Or you can just run the commands with `pipenv run` before them, but I prefer to just enter the shell.

6. Run the migrations:
   ```bash
   python manage.py migrate
   ```

7. Apply the migrations:
   ```bash
   python manage.py makemigrations
   ```

8. Run the server:
   ```bash
   python manage.py runserver
   ```

`NOTE`: The front-end is not included in this repository, you can't really run the whole thing without it, but you can still run the back-end and test the API endpoints.

## Why?

Honestly I needed a backend for the website, and rather than doing another Node.js backend I decided I wanted to try out Django. Its nice. Batteries included frameworks are nice.
I wasn't planning on making anything super big and complicated, just something small a nd simple that I could use as my first baby steps in django. 


## Stuff to do incase I ever come back to this project
- [ ] Some service to actually store user uploaded files. (Firestore? idk)
- [ ] Flesh out the whole ass forum system, its veeeery bare bones now.
- [ ] Flesh out the vfx endpoints since right now its just a GET
- [ ] Honestly idk, most of the backend features are driven by the front-end; So if front-end doesn't get anything, backend probably wont either.