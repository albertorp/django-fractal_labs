
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


# WPs to do

## Core functionality
Add Attachments
DONE Add Comments
DONE Add Invoice models
Add Terms&Conditions model
Implement currencies and currency exchange (copy from HomeFinance)
Create an "is_employee" flag for a user and a EmployeeRequiredMixin permission so that only employees can handle all items
Add Export to Excel functionality, to save all info in the database to a well-formatted Excel file


## Additional functionality


## Frontend functionality
Make "deadline" field in BaseItemForm a DatePicker
Add Filters and pagination to the ListViews


