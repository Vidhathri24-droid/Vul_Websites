When we run the application and visit it, it shows the login page as we dont have the account we click on the register option and enter the details to register and we will be redirected to the login page enter the login credentials.

Once we enter the login credentials correctly we will be redirected to the index page or home page of the website there we will see the three options, Home, User Profile and LogOut.

When we click on home we will be on the same page. When we click on the User Profile, we will be redirected to the dashboard in which the url contains the id of the user. 

<img width="632" alt="image" src="https://github.com/user-attachments/assets/7fec0330-9d46-4c24-a3c2-31a99b69e24e" />

Sometimes there might be the update account option in the user dashboard. Now change the value of the user id in the url which is different from the current user id.

<img width="636" alt="image" src="https://github.com/user-attachments/assets/7751b464-dcb1-4898-9691-93aac796ae5f" />

When we change the value of the user id it shows the details of the another user without authentication there is an option to update their account also so an unauthorized user can view their accounts and change their details.

This vulnerability is idor vulnerability. 

To fix this vulnerabilty we have set authorization by checking the current user login ids and the user id that is passed in the url if both the value matches the user can update their account if it doesn't match then the user should be blocked from updating other user's accounts.



