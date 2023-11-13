
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