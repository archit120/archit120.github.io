---
layout: default_blog
title: Archit - GSoC - The Beginning
description: Hi! I'm Archit. In this series of blog posts, I mainly plan on walking you through what it was like working for GSoC, what challenges I faced, and how I overcame those.
---

## GSoC Blog 1 - The Beginning

Until now, I've been severely behind schedule on blog posts. I hoped to have over ten posts by now, but here we are at just the second. Hopefully, this series of posts will ensure that I stay on track.

### What is this series about?

In this series of blog posts, I mainly plan on walking you through what it was like working for GSoC, what challenges I faced, and how I overcame those. It might get slightly technical at times, but for the most part, I'll try to keep away the implementation-specific details away. By the end of the series, I hope to become a better communicator and for you to experience what it feels like to participate in the program + learn about some really cool technologies and solutions through the journey.

### What is GSoC?

Feel free to skip this section if you already know about it. GSoC stands for Google Summer of Code. It's a program administered by Google every year where a large number of students from around the world are selected to work for different open source organizations. Unlike regular work, GSoC students have to propose what they will be doing for the organization. Then the organizations select which ideas they want to be implemented among the pool of competitors. Each organization can choose a fixed number of students only, which is decided by Google. Every selected student gets paid a stipend of $3000 to $6600 by Google, depending on their country of residence.

### The Process

#### Organization Selection

The first thing that you want to do is select the organization for which you'd like to contribute. In my university, Julia has a reputation for being easy to understand and for accepting a higher number of students than most organizations. So naturally, the first organization I looked at was Julia. Most organizations will have a GSoC ideas page. I found the one for Julia and started browsing through it. It had a subsection for images related projects. Because of my work with computer vision in Aerial Robotics Lab and independent projects, I felt most comfortable with computer vision. In this sub-section, I found a project that really caught my eye. It was

>Integration of OpenCV and JuliaImages
>
>OpenCV is one of the pre-eminent image-processing frameworks, and there are two existing OpenCV wrappers: https://github.com/JuliaOpenCV and https://github.com/maxruby/OpenCV.jl. This project would update one of these for more recent versions of Julia and JuliaImages, improve interoperability with pure-Julia image processing, and make further refinements to code and documentation. CxxWrap or Cxx are likely to be useful; prospective students may want to spend some time assessing the state of support for Julia 1.0.

Eventually, this becomes the project that I would work on. Interestingly, the organization that selects me, in the end, wasn't Julia.

#### Initial Contact

My next step was to get onto the Julia Slack. I went to the `image-processing` channel and declared my intention to work on this project. The members of the slack channel were accommodating and gave me some more initial pointers about what to research. I was also given an initial task to get started with Image Processing in Julia. The job was to implement the functionality of findContours from OpenCV in Julia. I started doing this research on a Sunday and had some free time, so I decided to start working on it. Luckily, through a lot of intensive googling, I discovered the original paper of findContours and even found a very straight-forward implementation. Converting the code didn't take a lot of time. I created my first pull request to JuliaImages within 12 hours of getting this task. Another oddity from most other GSoC selections that you might come across, this was also the only pull request that I had up till the day of results announcement. 

#### Investigation

Now, it was time to start figuring out what this project really entails. OpenCV is a giant library, and Julia is a relatively new language. The libraries mentioned in the idea, Cxx and CxxWrap had relatively little documentation. Without diving deep into them, it was impossible to figure out whether the features that they present will be sufficient for this project to be successful. 

The intention was for the wrapper to be as close to Python wrapper for OpenCV as possible. This will require a lot of features in addition to just essential function calling functionality. Including, but not limited to, parametric classes, multidimensional arrays, tuples, default and optional arguments, getters and setters on member variables, and much more. 

I initially began by writing small wrappers. Just load an image with imread and then displaying it through imshow. All in all, this was probably under 50 lines of code for both the libraries. CxxWrap.jl based wrapper worked flawlessly, the image loaded up and then displayed just as it would've if I had called the functions through Python or C++. Cxx.jl, on the other hand, gave me a lot more trouble then I'd hoped for. I kept running into segmentation faults or incompatible pointers or missing library links. Even though it was a tiny test, I decided to focus on CxxWrap.jl for the rest of my investigation. 

### The End of Part 1

Everything I described here happened probably within the first week of me deciding that I wanted to participate in GSoC. Over the next weeks and months, there were many times when I totally left this project but eventually got back to it after facing internship rejections (yes, multiple) or just plain boredom. I plan on writing the next post within a week or two, where I describe how I went about establishing further contact with my mentor, getting OpenCV - funnily, my project was accepted by OpenCV instead of Julia - onboard, and planning out a rough sketch of the proposal. 

