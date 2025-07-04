../register/ --> create user <br>
../users/ --> git all users list
../users/<int:user_id>/upgrade/ --> update user to staff or admin
../login/ --> login
../logout/ --> logout
../users/<int:user_id>/delete/ --> delete user
../users/<int:user_id/ --> view with git method update with put method delete with delete method
../api/groups/ --> create new group with post method and view all the groups with git method
../api/groups/<int:pk>/ --> view with git method update with put method delete with delete method
../api/groups/<int:pk>/add-member/ --> Add a user to a group with id pk
../api/groups/<int:pk>/join/ --> join the group with id pk
../api/tasks/ --> create new task with post method and view all the tasks with git method
../api/tasks/<int:task_id>/ --> view with git method update with put method delete with delete method
../api/tasks/<int:task_id>/assign/ --> Assign a task to the current user
../api/events/ --> create new event with post method and view all the events with git method
../api/events/<int:event_id>/ --> view with git method update with put method delete with delete method
../api/events/<int:event_id>/join/ --> Add current user to event attendees
../api/events/<int:event_id>/leave/ --> Remove current user from event attendees
../info/activities/ --> create new activitie with post method and view all the activities with git method
../info/activities/<int:pk>/ --> view with git method update with put method delete with delete method
../info/sponsors/ --> create new sponsor with post method and view all the sponsors with git method
../info/sponsors/<int:pk>/ --> view with git method update with put method delete with delete method
