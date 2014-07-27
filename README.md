Spyderjax
---

This is a module being developed as a part of **Google Summer of Code 2014** project for **OWASP OWTF**.



What is OWTF?
---

**OWTF** is a project aligned to standards such as the **OWASP Testing Guide** and the **Penetration Testing Execution Standard (PTES)**.

The main focus of **OWASP OWTF** is to automate the manual, uncreative part of *penetration testing*. **OWTF** tries to unite tools and expedite pentesting through *automation*, *efficient reporting*, *efficient human analysis*, a *fast MiTM proxy*, and *multi-processing*.


ABOUT
---

**Spyderjax** is a minimalistic port of [Crawljax](http://www.github.com/crawljax/crawljax.git).

It enables "crawling" of ***AJAX*** targets to probe for further *vulnerability testing*.

Essentially, the tool is divided into 4 main parts:


1. Clickbot
---

This is the main *spider/crawler*. It fetches the base URL (uses **Selenium**), passes on the *DOM tree* to the **DOM analyzer**.
It also performs clicking, firing/triggering of events on certain candidate elements.


2. DOM Analyzer
---

This uses the HTML source to perform parsing.

  * Compares DOM trees before and after an event is triggered by the bot.

  * Calculates the difference between two states (basically the **edit distance**)

  * Parses the new DOM tree for state changes


3. Controller
---

This manages the ***clickbot*** and the ***state-flow graph engine***.

It initializes, pauses, and stops the bot. This also creates the ***state flow graph*** based on **DOM state** changes (from the *DOM analyzer*).

This also controls the browser pool (multiple instances of the browser)


4. State-flow graph
---

This interprets visually, how the state changes with trigger/firing of an *event*.

An example of a state flow graph:
<hr>
![](http://crawljax.com/images/new-overview-plugin.png)

The ***state-flow graph*** will be accessed through the **webUI**.


Milestone
---
0.11

- [ ] Basic crawler ready

- [x] Basic DOM analysis

- [x] Minimal, functional webUI

Roadmap
---

* Beyond GSoC (0.11)

- [ ] Multiple instances of the browser, and managing the browser pool

- [ ] Multiprocessing/threading* based on future considerations

- [ ] Standalone package

- [ ] REsT API

- [ ] Fully functional web interface


Contribute
---

Send a **pull request** or create an issue on the **issue tracker**.

Suggestions welcome!
