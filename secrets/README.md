# Project Description
Madeleine Jin, Aleksandra Tyutynik, Andrew Sun, & Elijah Sandler

The goal of this project is to create a database for Shadow and Page's inventory and finances. Shadow and Page is an evil bookstore, and this particular evil bookstore has an R&D department (for malicious purposes) and a front, which is a normal, non-evil bookstore. The database’s tables will be lower-level employees, management, books, curses, safety information, and customers. This project creates a well-organized database that gives people appropriate access to information that they have the clearance to view information necessary.


# Password secrets for MySQL

You should never store passwords in a file that will be pushed to github or any other cloud-hosted system.  You'll notice that in the .gitignore, two files from this folder are indeed ignored.  

In this folder, you'll need to create two files:

- `db_password.txt`
  - in this file, put a password that will be used for a non-root db user
- `db_root_password.txt`
  - in this file, put the password you want to use for the root user (superuser) of mysql. 