AJAX Spider 
===

This is a ***prototype crawler*** which crawls **AJAX** targets and saves its snapshot.

The concepts explained below are mentioned in this [thesis paper](http://www.slideshare.net/Sampetruda/analysis-and-testing-of-ajaxbased-singlepage-web-applications). ##Thank you!

Some important steps involved:

1.**User Interface States**
<hr>

In traditional web applications, ***each URL*** was associated with a separate page. In *AJAX*, the web application is essentially a single page whose changing internal **DOM** stucture represents a state of the application.

 2.**Create a state flow graph for the application**
<hr>
A **state flow graph** can be defined as tuple of 3 elements, mainly initial state of target, multiple possible states and paths connecting them through various clickable elements.

 3.**Clickable elements**
<hr>
*Clickable elements* are those `<a>` elements, when triggered possibly change the state of the ***AJAX*** web application.

 4.**Creating DOM structure and generating a static sitemap**
<hr>
This static sitemap is generally a snapshot of the target at a particular instance. The DOM structure is converted to multi-page HTML document, which can be easily crawled.

A general algorithm representing the above steps can be found at slide ***114*** in the paper given.

An example of the DOM tree is provided below:

![image]


####Contribute

Fork & send a pull a request!


[image]: http://static.flickr.com/75/154105033_f20d6d511f_m.jpg