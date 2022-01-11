---
layout: default_blog
title: Archit - A DNS Dive
description: Hi! I'm Archit. This page attempts to chronicle my experience of creating a DNS resolver
---

## A DNS Dive - Part 1

heroku
docker
cors
jquery

Type a domain name <input type="text" id="dns-input" val=""> <button id="dns-btn"> Click Me </button>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<pre><code id="dnswhy-output">waiting</code></pre>


<script>
$("#dns-btn").on("click", function(x) { $.get("https://dnswhy-flask.herokuapp.com/"+$("#dns-input").val(), function(x) {$("#dnswhy-output").text(x); });} )
</script>


