
# main: basic config 2023 11 13
Basic app as per Pegasus, with 2 scheleton apps added:
customers
employees

However, in the beginning the employees app will not be used. Employees will just be users and for the moment we do not need to track additional information about them. 
We will have a separate group called "collaborators" that will have extra permssions to be able to edit items

# jobcycle01: BaseItem and main models 2023 11 13

Created the jobcycle app
Created menu links in the sidebar
Created basic templates for the home page of requirements, quotations, jobs and invoices (these just point to an empty page with a title)
The idea will be to create a single template for all items
Created the BaseItem model
Created the Requirement, Quotation and Job models, as well as the admin interface


# jobcycle01: CLUD and state machine 2023 11 14
Basic CLU (Create, List, Update) Views for requirements, quotations and jobs
Basic state machine for workflows implemented for the three models
No front-end is affected yet
Each UpdateView form will fetch the buttons that it needs from a utils module and pass them to the context
Each button will then trigger and action and be interpreted in the form_valid()method of the UpdateView to move the item to another state and perform additional actions (like create a quotation from a requirement, for example)

# jobcycle01: CLUD finished 2023 11 14
Added Detail views to each item
Basic detailview, with just showing all the fields in the item, with no links between them


# jobcycle01: Add Web Requirement 2023 11 14
Added a "contact us" page that has a form that can transform into a requirement and also create a new customer and potentially a new user

# jobcycle01: CLUd for Customers 2023 11 14
Basic CLU (Create, List, Update) Views for Customers

# jobcycle01: Model and CLUd for Invoicing 2023 11 15
Basic CLU (Create, List, Update) Views for Invoices and their invoiceitems
Using some htmx to add/edit the invoiceitems, but it's not working fully yet

# jobcycle01: minor changes 2023 11 16
Some minor changes and corrections.
Moved the invoices views to use their own templates instead of the common ones
Now also the listView templates include a table template, and the table the item rows



# 2023 11 17 09:48 Pull request to merge up to here and start playing with the frontend


# jobcycle02: Comments model 2023 11 17
Created the comments app and the Comment model (with admin code too)
Added it to the BaseItem model
No views at the moment


# jobcycle02: Comments to BaseItem and Customer 2023 11 17
Added the comments functionality to the BaseItem and the Customer model, so now all Requirements, Invoices, etc. can have comments.
In each UpdateView the comments are pulled into the context and displayed at the bottom of the page in table format


# jobcycle02: Attachment generic model 2023 11 17
Created a generic attachment model to add files to the items.
There are 2 clases, FileAttachment that is the actual file, and Attachment, that captures which file is attached to which item via a generic relation


# frontend01: initial integration of flowbite 2023 11 17
Added flowbite to the p

# frontend01: flowbite frontend 2023 11 19
Initial development of frontend with flowbite
Some initial progress with Customer forms and Customer list

# frontend01: flowbite frontend item 2023 11 21
Applying flowbite styles to the BaseItems templates
Added the help_text to the forms

# frontend01: flowbite datepicker 2023 11 21
Added Flowbite datepicker:
 cp node_modules/flowbite/dist/datepicker.js static/js 
 In the html template where we want to use it (at the end):
    {% block page_js %}
    <script src="{% static 'js/datepicker.js' %}"></script>
    {% endblock page_js %} 
To use it:
    {% render_field form.validity|attr:"datepicker"|attr:"datepicker-format:yyyy-mm-dd"|attr:"datepicker-autohide" class="...


# frontend01: invoice forms 2023 11 23
Changed the invoice forms to use flowbite
The HTMX and InvoiceItems are not working yet


# frontend01: added marketing site 2023 11 24 
Added some scheleton pages (Services, Pricing...)

# frontend01: changed the navbar and app templates 2023 11 24
Adapted the Application UI from Flowbite

# frontend01 and jobcycle02 were both merged together on 2023 11 24

# main: comments and attachments to flowbite 2023 11 24 
Changed the tables for comments and attachments to Flowbite format


# jobcycle03: export to excel 2023 11 24
Menu option to export all relevant data. This allows for a very simple backup for our users

# jobcycle03: messages framework 2023 11 25
Adapted the messages.html template to display Flowbite toasts. 
I have not been able to properly use the {{ message.tag_level }} as implementen in Pegasus, so I left it as several ifs

# jobcycle03: form validation formats 2023 11 26
Added danger formats to the form fields when there are errors, as well as an error message

# jobcycle03: changed the contactus form and thank you page 2023 11 27
That

# jobcycle03: pagination in ListViews 2023 11 27
Added pagination to ListViews
Added createt_at to ListView tables
Modified the updateCustomer template to incorporate errors
Changed the format for the errors in the form fields. Apparently, django has a default class called .errorlist, and this is defined in assets/styles/app/utilities.saas, but it uses the color variables from daisyui. So I have updated the -danger variable to be the same as the danger-700 color in tailwind.config.js and I have also added the font-size: .875rem; as suggested by ChatGPT: // This is typically what text-sm might represent


# jobcycle03: cancel/reject confirmation 2023 11 28
Added a modal confirmation when rejecting a requirement or cancelling a quotation/job
The cancel/reject button is now populated with data-modal-target and data-modal-toggle attributes in utils.py, and then several modals are included in the item_update.html.
This is not very efficient (or elegant) and alter we can change it to populate buttons and modals at the same time in utils.py

# WPs to do

## Core functionality
Rework on the Invoice Update template, to adapt HTMX to Flowbite format
DONE Check Validation errors in the item and customer forms
DONE Add Attachments
DONE Add Comments
DONE Add Invoice models
Add Terms&Conditions model
Implement currencies and currency exchange (copy from HomeFinance)
Create an "is_employee" flag for a user and a EmployeeRequiredMixin permission so that only employees can handle all items
DONE Add Export to Excel functionality, to save all info in the database to a well-formatted Excel file
Add item_type to the BaseItem model. This will reflect potential different job types or services that the SP can provide. For example, for a translator, we can use types of "normal translation", "urgent translation", "sworn tranlsation" or "interpreting"


## Additional functionality


## Frontend functionality
DONE Make "deadline" field in BaseItemForm a DatePicker
Add Filters and pagination to the ListViews
SOLVED I've set the top NavBar to be fixed, and this interferes with the notification messages
In the ListView tables, the created_at date should be shown. It currencly does not appear
