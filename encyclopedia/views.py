from django.shortcuts import render, redirect
from django import forms
import markdown
from . import util


def convert_md_to_html(title):
    content = util.get_entry(title)
    md = markdown.Markdown()
    if content == None:
        return None
    else:
        return md.convert(content)




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title = None):
    # Check if a title was passed as a parameter
    if not title:
        # If title is not present, return an error message
        return render(request, "encyclopedia/error.html", {
            "message" : f"We don't have a title on our website"
        })
    
    # Convert the markdown title to HTML content
    html_content = convert_md_to_html(title)
    
    # Check if the HTML content was generated successfully
    if not html_content:
        # If the HTML content is not present, return an error message
        return render(request, "encyclopedia/error.html", {
            "message" : f"We don't have '{title}' on our website"
        })
    
    # Return the HTML content for the title
    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "content" : html_content
    })  







def newEntry(request):
    # Check if the request method is GET
    if request.method == "GET":
        # If the request method is GET, return the new entry form
        return render(request, "encyclopedia/new.html")
    else:
        # If the request method is POST, get the title and content from the form
        title = request.POST['title']
        content = request.POST['content']

        # Check if the title already exists
        if util.get_entry(title) is not None:
            # If the title already exists, return an error message
            return render(request, "encyclopedia/error.html", {
                "message" : "Title already exists"
            })
        else:
            # If the title does not exist, save the entry and return the HTML content
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "content" : content
            })