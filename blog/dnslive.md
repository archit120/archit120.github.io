---
layout: default_blog
title: Archit - A simple python webapp for DNS resolution
description: Hi! I'm Archit. 
--- 

## Demo

Type a domain name and see DNS in action <input type="text" id="dns-input" val=""> <button id="dns-btn"> Click Me </button>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<pre><code id="dns-output">It can take some time for output to appear. Please wait!</code></pre>


<script>
$("#dns-btn").on("click", function(x) { $.get("https://dnswhy-flask.herokuapp.com/"+$("#dns-input").val(), function(x) {$("#dns-output").text(x); });} )
</script>

--- 

This widget uses the DNS resolver I developed in [this blog series](dns). The first step to get this working was to wrap it some sort of http server and get it hosted.

I had three key requirements from this project
 1. Use the latest DNSWhy program as is (with STDOUT output) and decoupled version from this project
 2. The DSNWhy program is made accessible on a web server with a simple GET request.
 3. Uses Heroku (_no reason but wanted to try it out_)


The first and third requirements made deployment an exciting challenge that I will get into more detail later.

### Program Structure
```
 |---DNSWhy/
 |---|-----*
 |---main.py
 |---heroku.yml
 |---Dockerfile
 |---requirements.py
```

## Flask

Flask is a web application framework for creating web apps using python. I had to use very little of the functionality provided because my project would have just one `GET` endpoint that returns the resolution output. For calling the other program I just used `subprocess.check_output` that runs it with domain name supplied as a path parameter and returns the STDOUT output. 

### CORS
Finally, we also need CORS header `Access-Control-Allow-Origin` set because this application will be hosted on a heroku server and my blog is hosted at `archit.me`. With all that out of the way the final code for `main.py` is just

```python
from flask import Flask
import subprocess
app = Flask(__name__)


@app.route('/<domain>')
def hello(domain):
    try:
        return subprocess.check_output(["python", "DNSWhy/main.py" ,domain]).decode('ascii')
    except Exception as e:
        return "Error. Check domain!"


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


if __name__== "__main__":
    app.run()
```

### gunicorn

Just a small footnote. While Flask does come with an http server, it actually recommends using some other server for production workloads. Keeping inline with this recommendation I decided to use gunicorn so the way to run this program is actually - 

```bash
gunicorn main:app
```
## Heroku

Heroku build process in its usual way is not really compatible with the requirement 1 that I had set. Usually for a python based program, heroku will create a slug with a python installation, dependencies as defined in `requirements.txt` and the rest of the application. Slugs are similar to docker images. Now when it's time to actually run the image, Heroku will use the command defined in `Procfile`. No where does this let you actually influence the build process of the slug which is necessary to clone the DNSWhy repository. There were three ways to get around this problem

 1. Write a custom buildpack. This can let you influence the slug build process but I didn't want to get so involved.
 2. Deploy to Heroku using a github action. The github action before deploying to Heroku would get the required dependencies. 
 3. Use a docker deployment. 

 There's a fourth way aswell that would be including the dependency fetch step in `Procfile` but this is a bad way to do achieve this. Please don't do this because you will add a significant start time.

## Docker

I wanted to use Heroku's github integration so that only left the third option of docker deployment. This was pretty easy to configure because all I  needed was a python installation and a git clone. Instead of using `Procfile` I could just specify CMD in the `Dockerfile`.


```
FROM python:3.10

COPY main.py .
COPY requirements.txt .

RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/archit120/DNSWhy.git

CMD gunicorn main:app
```

Along with the `Dockerfile` another file named `heroku.yml` is necessary which tells heroku that the web type dyno is using this `Dockerfile`.

```yaml
build:
  docker:
    web: Dockerfile
```

## Deployment 

With all that out of the way I pushed it on to my [github](https://github.com/archit120/dnswhy-flask). Set up the heroku integration and loaded up https://dnswhy-flask.herokuapp.com/archit.me hoping to see some nice DNS output but instead got greeted with an error that no server is running. Looking at the logs I realize that heroku is unable to figure out that I want a docker deployment. This was quickly fixed by running 

```
> heroku stack:set container
```

And this time it worked perfectly! The final step was to write the javascript demo for this post. With everything set in place I used a little jquery to 
hook it all up and display the output.


```
$("#dns-btn").on("click", function(x) { 
    $.get("https://dnswhy-flask.herokuapp.com/"+$("#dns-input").val(), function(x) {
        $("#dns-output").text(x); 
    });
})
```

