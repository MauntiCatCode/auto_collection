# The AUTO Collection
My personal scripts for the automation of marketing for a logistics company.

## What is this?
These three repos contain the most presentable scripts I developed during my three months of work at a logistics back-office company. These scripts contributed to automating their cold email marketing — first as simple utilities for generating mock forms and invoices, and later for the outreach itself.

Note: These scripts are for educational/demo purposes. They might not run as-is.
*Trust no one, even `requirements.txt`.*

This project is licensed under the GPLv3. You are free to use, modify, and redistribute it under the same terms.
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Dependencies used across scripts:
- pandas
- PyPDFForm
- python-safer
- docxtpl
- usaddress

---

## Auto MCS-150
It began with Auto MCS-150: I was tasked with filling out forms that would be sent alongside outreach messages, but I found manually switching between websites and spreadsheets tedious, so I gradually optimized my work using `python-safer` — a Python wrapper over the SAFER REST API — and `PyPDFForm`, a library for quickly filling out fillable PDF forms.

*I then worked on a script for filling out personalized invoices with the data from those MCS-150 forms, but it’s a mess — so you won't see it, for the same reasons you don't see my Git commits.*

## Auto Email
Fast forward a bit — I was tasked with automating cold outreach for them. I implemented message personalization using the data from the same MCS-150 forms that would be sent along with the messages (initially, before we realized that attachments were a no-go), as well as personalized invoices. I also integrated the `Easy Email API`, a tool for verifying the validity of email addresses. The sending itself was done using Google’s SMTP Relay.

## Auto IFTA
Somewhere in between setting up helpers for going through folders, looking up invoices recursively, and implementing caching for the email scripts, I was tasked with automating the **filling** of IFTA reports — which I did with much more grace than the original invoice automation tool — using `docxtpl`, a Python library that uses `Jinja2` under the hood to insert text into preformatted `.docx` templates, and `LibreOffice` for PDF conversion.


---

## Key takeaways and issues

If you ever wanted to scale any of this up, you’d run into some problems.

**Auto MCS-150** and **Auto Email** both rely on heavy OOP that eventually outgrew its purpose.  
The abstraction made sense at the time of implementation, but as the goals changed and I became more familiar with existing libraries and frameworks, it became nearly impossible to add new features effectively — mostly because of the extensive, archaic abstraction.

**Auto MCS-150** was developed when I didn’t even know what a DataFrame was and was hesitant to use external APIs. I decided to implement my own helper class, a `SimpleCompany`, that inherited attributes from the `Company` class provided by `python-safer`.  
I was right to question the bloated OOP design of `python-safer` — I could have just used the SAFER API directly — but eventually, my own script became bloated as well.  

When I wanted to add a new input (importing emails from an external spreadsheet), it required an extremely awkward injection inside a method meant for something entirely different — best summarized by the quote:  
> “There is nothing more permanent than a temporary solution.”  

There’s also no caching of data: if you interrupt the process at any stage, you lose everything and have to start over. Implementing caching would be difficult because of the aforementioned OOP mess.  
If I were to redo it, I’d use plain dictionaries — maybe `pd.DataFrame` at most.

**Auto Email**… At the time of implementation, I had three goals in mind:
1. Send one personalized email to one carrier from a list, using one email address.  
2. Attach two different files corresponding to that carrier.  
3. Follow the path of least resistance.

So I did. I implemented layer upon layer of abstraction while still relying on data parsed from MCS-150 forms and invoices, instead of designing proper inputs.  

Later, I learned more about best practices for cold outreach — that you need to send more than one message, that attachments in the first email are a bad idea, and that your email list needs heavy preprocessing before sending. I picked up some `pandas`, implemented a few nice features (like email validation), and tried to reform Auto Email.  
But ultimately, what it needs isn’t a code refactor — it needs a **full paradigm rework**.

---

## How do I use this?
I don't know — you tell me. Feel free to open an issue, and maybe we can figure out how to adapt this together for your use case.  
If you want to use the Auto MCS-150 script, read its own `README.md`.

