---
layout: default_blog
title: Archit - GSoC - Final Evaluation
description: Hi! I'm Archit. In this blog post, I explain the work I did during my GSoC project of creating bindings from 
---

## GSoC Final Evaluation Post

This post is going to be broadly divided in two sections. In the first part, I'll summarize the work that I've done in the GSoC project and in the second part I'll summarize the technical part of this project and how to extend.

---

OpenCV
------

OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in the commercial products. Distributed under permissive license, OpenCV makes it easy for businesses to utilize and modify the code.

The library has more than 2500 optimized algorithms, which includes a comprehensive set of both classic and state-of-the-art computer vision and machine learning algorithms. These algorithms can be used to detect and recognize faces, identify objects, classify human actions in videos, track camera movements, track moving objects, extract 3D models of objects, produce 3D point clouds from stereo cameras, stitch images together to produce a high resolution image of an entire scene, find similar images from an image database, remove red eyes from images taken using flash, follow eye movements, recognize scenery and establish markers to overlay it with augmented reality, etc. OpenCV has more than 47 thousand people of user community and estimated number of downloads exceeding 18 million. The library is used extensively in companies, research groups and by governmental bodies.

Julia
-------------
Julia is a high-performance, high-level, and dynamic programming language that specializes in tasks relateted numerical, and scientefic computing. However, It can also be used for general programming with GUI and web programming. Julia can be considered as a combination of rapid interpreter style prototyping capability of Python with the raw speed of C because of its special "just-ahead-of-time" compilation.

Inspite of all this, Julia severely lacks in a lot of traditional computer vision and image processing algorithms. This also hampers the usage of Julia in any pipeline that requires computer vision. The OpenCV bindings for Julia aims to solve this problem.

The Bindings
-----------------------
The OpenCV bindings for Julia are created automatically using Python scripts at configure time and then installed with the Julia package manager on the system. These bindings cover most of the important functionality present in the core, imgproc, imgcodecs, highgui, videio, and dnn modules. These bindings depend on CxxWrap.jl and the process for usage and compilation is explained in detail below. The Bindings have been tested on Ubuntu and Mac. Windows might work but is not officially tested and supported right now.

The generation process and the method by which the binding works are similar to the Python bindings. The only major difference is that CxxWrap.jl does not support optional arguments. As a consequence, it's necessary to define the optional arguments in Julia code which adds a lot of additional complexity.

More Information and Contributions
-------------

More information about how to compile and use the bindings can be found [here](https://docs.opencv.org/master/d8/da4/tutorial_julia.html)

The pull requests that were made during the project duration are 
 - https://github.com/opencv/opencv_contrib/pull/2547
 - https://github.com/opencv/opencv_contrib/pull/2582
 - https://github.com/opencv/opencv_contrib/pull/2622
 - https://github.com/opencv/opencv_contrib/pull/2631

All of the above pull requests have now been merged. OpenCV 4.4.0 ships with phase 1 of the project while later versions will ship with the complete functionality enabled. In total over 533 functions and 34 classes are wrapped. 

---

The Technical Details
==


As stated before, the julia bindings for OpenCV work very similar to how the python bindings work. However, because of some restrictions of the language and the wrapping library CxxWrap.jl additional challenges had to be solved. I'll list the challenges and briefly describe their solutions. The base work which is done in `gen3_cpp.py`

Mat and Vec classes
---

It was essential to expose these array like classes as native Julia arrays to improve the experience and make OpenCV feel like a native library. To do this, I had to create wrapping classes in Julia that implemented the necessary functionality. It was also necessary to make sure that these arrays can be allocated both by Julia and C++ code and that the destructors do not trigger the deletion of one side while references are still available. This is mostly done by delegating the wrapper to keep track of C++ reference, if available. Also, some minor differences had to be made for Vec compared to Mat as Vec is stack allocated while Mat class is heap allocated. This is handled in `Mat.jl` and `Vec.jl`

Default Arguments
---

CxxWrap.jl does not support default arguments. As a consequence, the C++ side of code exposes the entire function with all arguments and Julia side of code implements the default arguments by wrapping C++ exposed code. This meant that types had to be converted from C++ to corresponding Julia type. Also, the value for these types had to be converted too. I initially started work on creating an automated type and value conversion system but realized that it'll take too much time and it would be faster to do the same work manually. A future expansion of this project can try to fix this. Because of manually specifying the matching types, the automated generation is still limited to tested functions only. This is handled mostly by `gen3_julia_cxx.py`

Module Nesting
---

There isn't a proper way to nest modules in CxxWrap and have all the classes then link together. To solve this, I dump all classes, functions and constants in the same base module and then create links to the correct places that they should be in. This is handled by `gen3_julia.py`

Mapping of OpenCV Types in `types.h`
---

This was mostly figured out by Bart, the author of CxxWrap.jl. Special wrapping classes and changes to CxxWrap.jl were made to ensure that primitive OpenCV types like Size, Point, Rect etc. could be handled more easily. This special conversion ensures that these types are not copied and are easily created and moved between the two languages. This is done in `jlcv_types.hpp` and `jlcxx/array.hpp`

Additional Manual Functionality
---

Additional manual functionality is easy to add. Make sure that the module you're exposing functions from is present in `CMakeLists.txt` and then find the file `cv_core.cpp` in `gen/binding_templates_cpp`. There are examples of manually wrapped functions in the file and it should be easy to understand. You can find more details about the wrapping code by checking out the README of CxxWrap.jl. Expose the C++ side of functionality in this file. Next, find `cv_manual_wrap.jl` in `gen/jl_cxx_files` and add the Julia side of wrapping. Recompile and install; the new functionality should be usable. 

Another way to do this would be to rig the automated builder. Try adding the needed function to `gen/funclist.csv` and header to `gen/gen_all.py`. If you're lucky, there might be no errors in configure time and you can proceed as usual. If CMake complains like ".. not found" then you need to manually wrap the optional types by adding details to `typemap.txt` and `defval.txt`.


