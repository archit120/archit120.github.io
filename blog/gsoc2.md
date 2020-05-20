---
layout: default_blog
title: Archit - GSoC - The Proposal
description: Hi! I'm Archit. In this series of blog posts, I mainly plan to walk you through what it was like working for GSoC, what challenges I faced, and how I overcame those challenges.
---

## GSoC Blog 2 - The Proposal

This post took longer than I wanted it to, but here it is.

This time I'll keep headlines mostly as the months so that a timeline can be established.

### January

My previous post covered the stuff I did in January. I barely spent 2 weeks or so working on GSoC since I still had hopes and dreams of getting a physical research internship. While browsing through Facebook, one day, I came across the video of China building a hospital from scratch in a week. Curious, I read about COVID but could've never imagined how it would end up affecting us. Check out [The Beginning](gsoc1) to learn about the stuff I did in this time-frame.

Apart from that, I spent some time on getting OpenCV onboard for this project. Based on the comments for the issue [Is there any plan to provide API for julia language? #16233](https://github.com/opencv/opencv/issues/16233) I wrote an Evolution Proposal that I submitted as an issue on the OpenCV Github. This was then added to evolution proposals, and the project was added to the GSoC list by OpenCV. 

### February

February was about as unproductive (from a GSoC POV at least) as it gets. Probably a consequence of the combo: Aerial Robotics Kharagpur selections, post-Spring-Fest hangover, and then to top it all up - midterms. I tried to ping someone at Julia Slack once a week to ensure that no one thought I wasn't interested in the project anymore. Apart from that, nothing much happened. By the end of February, I had realized that physical internship is starting to get unlikely because of COVID.

### March

By early-March, I started to realize that GSoC was my best hope for an internship this summer. I was confused between working on theory courses and robotics-related research work vs. GSoC, but I overall felt that the theory and research work could be done at any-time. Furthermore, that can always be my backup in-case I don't get through with my proposal.

With better determination, I began giving around 10 hours per week on research related to what my project should be and how best to do it. My first goal was to understand precisely how Python bindings for OpenCV worked. Since I was aiming to replicate it, I needed to understand the binding generation as low-level as possible. I pulled apart the python module from the OpenCV source code and started poking at various parts of it. Changing stuff to find where it breaks and then setting back everything in a different way to get it to work again. I also did a little documentation to help me with this process. 

#### Previous Attempts

While I was doing the reverse-engineering, I also went out trying to figure out what work had been done for this previously. Judging by what I could read on the net, this was a much-desired feature by the Julia community and had been a part of the ideas list for some time. Like I'd said before, most of these attempts were based on a complicated manual method of binding and were code using `Cxx.jl`. I wanted a different approach, so I didn't initially get a lot of help with my research on how to do this. Until I stumbled upon a blog post in Japanese about a guy who already did the automated binding and had released a library as well [TakekazuKATO/OpenCV.jl](https://github.com/TakekazuKATO/OpenCV.jl). For whatever reason, I couldn't find any documentation for this package apart from the Japanese blog post - [CxxWrap.jlを使ったC++のライブラリのラッパー（CxxWrap.jl版OpenCV.jlの作り方）
](https://qiita.com/TakekazuKATO/items/f577ff9320a3e8afafca). It also looked like the package had no users. According to Google Translate, the author mentioned he had tried some features, and they seemed to work, but that was about it. There was a silver lining though in the form of showing that what I was trying to do was indeed possible. I spent some time analyzing the different problems with this package (too many to list) and trying to figure out what could be done better. 

#### The Project

Usually, at this step, you'd want to focus on getting as many PR as possible. This is a way to demonstrate your ability to work on codebases and that your project proposal will not remain just a proposal. I initially tried to get PRs only and started working on an API change issue related to JuliaImages. I had more problems than I expected to and eventually gave up on it. I felt that creating a pull-request for the sake of one doesn't make sense and that instead, my focus should be on proving that I can do this project. Some-time around mid-march, I started working on my actual project itself. While this was deviating from traditional advice, I firmly believed that it was for the better. It demonstrated my ability to wrap a library for another language better than a new implementation of Canny or Hough Transformation could ever do. 

So starting from mid-March, I began working on this project. This was, in hindsight, probably the best decision. Because of working on my deliverable from beforehand, I was able to reduce the time considerably I would spend during my actual GSoC work and make my proposal much-much more robust as I had real-working code and examples to show. When you work on a problem, you come across issues that you'd never even think about. This happened far too many times during this mini-project, which helped me include a lot of technical details in my proposal. 

There is one interesting problem related to the handling of array objects that I've explained with technical details at the end. 

### The Proposal

I began by reading different accepted proposals over the years. These were usually Julia or OpenCV related but not always. I maintained a log of interesting sections that I found and a basic idea of what I should write in each of them. Doing this helps in having a well-rounded proposal IMO that covers a lot of bases. Writing a long proposal is hard. I often felt that I could never cross five pages or six pages or *insert arbitrary goal here* pages. But whenever I got stuck, I looked around and found some fresh ideas from some other proposal that I thought I could include in my own. 

My project was a gift that kept on giving. I copied over generator code, possible problems, and solutions to issues, running examples, and so much more. Luckily, OpenCV admins also thought that this idea is better supported by a project than pull-requests and asked me to create a face detector demo. I hadn't told anyone about my work on this project till then; because of the amount of overlap, I was able to complete that within three days. 

The lockdown also hugely helped me during this time since I was easily putting in around 8-10 hours per day during the last week. Most of this was split between improving my project results, writing the proposal, and interacting with people.

I strongly recommend getting your proposal out there early. Early release will ensure more number of people can look at your project and give you valuable feedback. I received lots of feedback from the Julia community that helped me improve my proposal tremendously. 

### The Mentors

A significant part of the GSoC program is your mentors. Be in regular contact and ask good questions. I always made it a habit to spend at least an hour or two research my problem and scratching my head at it before sending a message to my mentors. This shows that you're willing to make an effort to do stuff on your own and also prepares you to ask better questions. As a mentor myself at Aerial Robotics Lab, I feel the right questions help differentiate you from the rest. In this section, I want to thank Tim Holy and Bart Janssens for their help especially. There will be times when you just need someone with more experience, and it is never a bad idea to ask in those cases.

### The Problem

One of the most significant issues I faced related to the handling of the OpenCV Mat classes. While other classes just need to export standard functionality like member variables and functions, the Mat class is an n-dimensional array. Furthermore, keeping in tradition with the Python bindings, it doesn't just need to export its array-like functionality but also be a proper Julia array so that arrays from other parts of the Julia ecosystem can be freely used. One obvious solution was to copy the information. However, this is not ideal and would impact performance. The other idea was to get the raw data pointer, array dimensions, and strides from Mat data and then wrap a Julia array in the same position using this information. While this solution would work, the problem was that we'd lose the original class reference. This should automatically cause the garbage collector to call the destructor on the original Mat object, and the array would be gone. 

The Python binding approaches this problem by creating a specialized allocator that manages the memory itself. However, with inputs from Tim Holy, I was able to create a much simpler solution. This basically does the same thing as taking a pointer and wrapping array at the position. But the array is a unique new class that inherits from AbstractArray and has an additional member variable. This member variable stores a reference to the Mat object as well. Now, as long as this array object is alive, the attached reference is still alive- preventing the deallocation of memory. And the other way around, when the array object is finalized by Julia, the reference to C++ object is gone, which frees memory.

### The End of Part 2

This covers up to the submission of the proposal. If anyone wants a copy of my proposal, please comment, and I'll be glad to put a link up. The next post will probably be more technical, where I dive into how this system works on a fundamental level. 