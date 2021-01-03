---
layout: default_blog
title: Archit - Learning CS on your own
description: Hi! I'm Archit. In this blog post I tell you about the challenges I had to face in my degree plan and how I'm trying to resolve those by studying important computer science topics on my own.
---

## Teaching Myself CS

### But Why?

**Optional Section but recommended for Kharagpur MnC**

The preivous semester is when I realized why there is a difference between the MnC degree and CS degrees offered at IIT Kharagpur. Until very recently, I was under the impression that sure, MnC has less Computer Science courses, some of those courses have _less rigour_, but just how bad can it be? If you compare the list of courses, everything important is there - Algorithms, Computer Organization and Architecture, Operating System, Networks, DBMS etc etc. If my professors are bad I can just do the exercises that CS kids are doing and call it a day.

Finally, I got to take COA from the Math Dept this semester. I don't think words can explain just how bad and inadequate the course content is. Just look at these two question papers, first from the [COA offered by CS department](http://www.library.iitkgp.ac.in/pages/SemQuestionWiki/images/2/21/CS31007_Computer_Organization_and_Architecture_MA_2016.pdf), and second from the [COA course offered by the Math department](https://static.metakgp.org/peqp/2016/Mid-Autumn%20Semester/Math/MA31009_Comp.%20Org%20&%20Arch._(Autumn%20Sem%20Exam%202016).pdf).

TL;DR of the comparison? One if a pretty indepth look at MIPS assembly and the hardware level details while the other one is puzzles and a glorified IQ test. Both of these are taken at the exact same time and I simply can't understand how the admin justifies this disparity. One of these courses actually prepare people for having a good understanding of Operating Systems, Systems Programming and Computer Architecture while the other one does jack shit. 

I used to think that companies are biased against MnC and they want CS students only. I had often heard of how Tower Research or Uber or Quadeye take MnC kids for a ride until the final interview rounds only to never extend a offer. The justification I was offered: they prefer the CS tags. However, after going through COA and looking in-depth at the courses offered for MnC like OS and Networks I came to the conclusion that the content being taught was woefully inadequate and incomparable. 

The silver lining? Well, these companies do still interview MnC students. They give an opportunity where you can shine if you are actually capable. I decided to do all the necessary courses by myself using the best resources available on internet. My transcripts show that I have done said courses and my knowledge will be complete because of all the extra hours that I put in. 

Even though I haven't completed all of these, based on my interaction with seniors and some amazing people on Reddit - these courses will help you get a better job and excel at it. So even if just academic knowledge or the joy of studying CS isn't a strong enough reason to go through this, consider your future prospects as an SWE.

_PS: This post targets future SWE/SDE roles. The advice may not be very relevant if you want to go into CS research._

### List of Courses

The courses that I feel important and necessary to be redone in no particular order are -

 1. Computer Organization and Architecture
 2. Operating Systems and Systems Programming
 3. Database Management Systems
 4. Networks

In addition to these, Compilers is supposed to be an extremely important course but so far I haven't been able to decide on its importance for most SWE roles. Finally, the Missing Semester course by MIT is probably a good addition to this list but I'm not including it because the course content is freely available and not something that necessarily needs to be followed in a structured ordered. 

In subsequent sections I'll simply paraphrase from [teachyourselfcs.com](https://teachyourselfcs.com) about why you might want to do that course. In addition, and here's the real value of this post, I'll add links to lecture videos, slides and lab assignments. 

A final note, while lecture videos are obviously important, I think it is impossible to truly understand the course content without doing their assignments. The reason these courses are truly impressive is because of the effort that TAs and professors have spent in making these assignment and it would be a shame if you ignore that. 

### Computer Organization and Architecture

>> If you don’t have a solid mental model of how a computer actually works, all of your higher-level abstractions will be brittle.	

> Computer Architecture—sometimes called “computer systems” or “computer organization”—is an important first look at computing below the surface of software. In our experience, it’s the most neglected area among self-taught software engineers.

I preferred following CS61C by UC Berkeley. The lecture videos are available here - [L01 Course Introduction UC Berkeley CS 61C, Spring 2015](https://www.youtube.com/watch?v=9y_sUqHeyy8&list=PLhMnuBfGeCDM8pXLpqib90mDFJI-e1lpk&ab_channel=SatyakiranDuggina). These videos are from Spring 2015 unfortunately and are a little out of date.

A better resource for this lecture is following the book Computer Organization and Design RISC-V Edition by Patterson and Hennessy. The best way to do this book is to go through [CS 61C FA20 website](https://cs61c.org/fa20/) and follow the suggested reading. Once you're done with reading go through the slides to make sure that you understand everything covered in the class aswell. Finally, complete the assignments and projects as described on the course website. These can be found at https://github.com/61c-teach/fa20-lab-starter and https://github.com/61c-teach/fa20-proj1-starter (first project but you can figure out the rest).

### Opearting Systems

>> Most of the code you write is run by an operating system, so you should know how those interact.	

My advice for all courses is similar to COA. So to avoid unnecessary reading, and typing! I'll simply put out the necessary links. Most of the relevant information can usually be found with a little digging on the course websites.

Suggested course: [CS 162 by UC Berkeley](https://cs162.org/)

Suggested Book: Operating Systems: Principles and Practice (2nd Ed.)

Lectures: [COMPSCI 162 - 2020-01-21
](https://www.youtube.com/watch?v=itfEcA3TXq4&list=PLIMsSuI81pxq7c91oQMpmXgmGICbuDA_c&ab_channel=WebcastDepartmental) Spring 2020 so yay! But 3 lectures are missing.

Assignments: [Github](https://github.com/Berkeley-CS162/student0)

Projects: [Github](https://github.com/Berkeley-CS162/group0)

### Database Management Systems

>> Data is at the heart of most significant programs, but few understand how database systems actually work.	

Suggested course: [CS 186 by UC Berkeley](https://cs186berkeley.net/)

Suggested Book: Nothing!

Lectures: [Lecture 1 Part 1 Intro and Why
](https://www.youtube.com/watch?v=j-iq40QBJy8&list=PLYp4IGUhNFmw8USiYMJvCUjZe79fvyYge&ab_channel=CS186Berkeley) Fall 2018 but supposedly upto date.

Assignments: [CS 186](https://cs186berkeley.net/) 

Projects: [Github](https://github.com/berkeley-cs186/fa20-moocbase )

### Computer Networks

>> The Internet turned out to be a big deal: understand how it works to unlock its full potential.	

> Given that so much of software engineering is on web servers and clients, one of the most immediately valuable areas of computer science is computer networking. Our self-taught students who methodically study networking find that they finally understand terms, concepts and protocols they’d been surrounded by for years.



Suggested Course: [CS 144 by Stanford](https://cs144.github.io/)

Suggested Book: Nothing! 

Lectures: [CS144 Fall 2013 Video 1-0: The Internet and IP Introduction](https://www.youtube.com/watch?v=-nciJGUPyAM&list=PLEAYkSg4uSQ2dr0XO_Nwa5OcdEcaaELSG&index=1&ab_channel=PhilipLevis) Fall 2013 unfortunately. It's best to supplement with readings through the internet and going through slides carefully.

Projects: [Github](https://github.com/CS144/sponge)

---

And that's it. I suggest going through [teachyourselfcs.com](https://teachyourselfcs.com) aswell. I did try making some study groups but that didn't go particularly well. If anyone wants, I can post the WhatsApp group links for those. 