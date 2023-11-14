
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





# WPs to do

Make "deadline" field in BaseItemForm a DatePicker
Add Invoice models
Add Terms&Conditions model
Implement currencies and currency exchange (copy from HomeFinance)
Add Filters and pagination to the ListViews