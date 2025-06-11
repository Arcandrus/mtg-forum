# MTG FORUM - A social media/ network platform for Magic: the Gathering players.
# Code Intstitute Milstone Project 3 - Full Stack Django Development

## Table of Contents

1. [Live Demo](#demo)
2. [User Stories](#user-stories)
3. [Design](#design)
4. [Technologies](#technologies)
5. [Features](#features)
6. [Deployment](#deployment)
7. [Testing](#testing)
8. [Credits](#credits)

![](./readme-assets/responsive_ui.png)

## Demo
A live demo to the website can be found [here](https://arcandrus.github.io/milestone-2/index.html)

# User Stories
When deciding on what I wanted to add to this project I looked at several soical media and forum style websites and took the greatest amount of inspiration from Reddit. To this effect, I wrote my user stories based on what I considered the cornerstone features of such a platform and split them into two Epics, User Profile and Content Interaction, detailed below, along with the acceptance criteria I decided for each user story.

## Epics

### USER PROFILE:

As a user, I want to create an account so that I can post, comment and interact.
+ User can register an account
+ User can Login to account<br><br>

As a user I want to be able to view a profile page with my information and the ability to see my posted content
+ User can access a profile page
+ Users profile page shows listed content created by the user
+ User has their own details displayed with certain fields allowing editing (display name)<br><br>

As a user I want to be able to change certain settings to enable me to customise and enjoy my experience better
+ User can reset password
+ User can delete account<br><br>

### CONTENT INTERACTION:

As a user I want to be able to create posts so I can share my thoughts in the forum
+ User can login and create post
+ User can see a list of their created posts
+ User can select a category for the post<br><br>

As a user I want to be able to like and comment on posts so I can express my feelings about the content
+ User can click a like button that tracks the number of total likes
+ User can post a comment to reply to any post
+ User can post a comment in a nested thread to reply to other comments
+ User can tag a post as a favourite<br><br>

As a user I want to be able to edit or delete my own content as needed
+ User can edit posts/ comments as needed
+ User can delete posts/ comment as needed<br><br>

As a user I want to be able to see what posts are popular to enable me to navigate quickly to active posts
+ User can view popular posts
+ User can filter by activity in a given time frame (24 hrs / 7 days / 30 days / All Time)<br><br>

As a user I want to be able to view the website on a mobile device to enable me to access the site from any device
+ Implement responsive design to allow for multiple screen sizes<br><br>

## Design
Taking into account Strategy, Scope, Structure, Skeleton and surface, together with User Stories and desired outcomes, this is what I considered while building this project.

To keep things cohesive and intuative, I had decided on having a sidebar navigation layout, with a persistent header and footer, all loaded and controlled by the **base.html** template. A wireframe of this initial design concept can be seen [here](mtg-forum-assets/mtg_forum.pdf) (pdf format). I felt this enabled the most cohesive and consistent display of all the controls and options while giving plenty of space to display content to the user. I wanted all the controls for the user to be persitent and easy to understand, which is why I used the sidebar approach, included icon labels using FontAwesome. 

(screenshot of sidebar)

The colour scheme I chose was a very calming and simple slate grey and white combination for maximum contrast and clarity while still being easier on the eyes than a plain white background with black text.

(screenshot of color scheme here)
(color palette here)

For visual clarity, links have a colour change when hovered, however, I considered mobile device users would not have this feature, and so, as part of my responsive design practice, I made links display with the default underline on smaller screens to make it clear what is a clickable link.

(Example gif to be added here)

## Technologies
**HTML** - To create a basic site skeleton and add the content

**CSS** - To create a controlled and consistent display for each element and to give a great user experience. Using js, I applied a class based responsive design to the site.

**Javascript** - This is where most of the work for this project was done, as much of the system runs on Javascript
+ comments.js - Contains the functionality to post comments, post replies and edit/ delete both
+ favourite.js - Enables AJAX js for the favourtie button, both processing the form and updating the button
+ like.js - Enables the like button functionality in a similar vein to the favourite button
+ messages.js - Controls the display of Django messages
+ post_edit.js - Enables the inline form to allow users to edit any of thier own posts
+ screen_check.js - As part of responsive design, this js file checks for screen size changes as well as orientation changes

**Django** - This was the meat of the project, enabling full user controlled CRUD functionality. Implementing a CustomUser model as well as creating custom templates for much of the Django AllAuth library to allow for greater access and customisation across the sites features. 

<details>
<summary>CustomUser model is shown here</summary>
```python
class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds full_name, unique email, and profile picture via Cloudinary.
    """
    full_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='samples/cloudinary-icon'
    )

    @property
    def post_count(self):
        """Returns the count of posts authored by this user."""
        return self.posts.count()

    @property
    def comment_count(self):
        """Returns the count of comments authored by this user."""
        return self.comments.count()

    @property
    def user_status(self):
        """
        Returns a string representing the user's status:
        'Superuser', 'Staff', 'Active', or 'Inactive'.
        """
        if self.is_superuser:
            return "Superuser"
        elif self.is_staff:
            return "Staff"
        elif self.is_active:
            return "Active"
        else:
            return "Inactive"

    def __str__(self):
        return self.username
</details>

**Balsamiq** - To create a wireframe.

**Bootstrap** - To ensure responsive design and usability across all devices, I use a combination of Bootstrap classes and custom css.
