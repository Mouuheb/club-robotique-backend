../register/ --> create user <br>
../users/ --> git all users list <br>
../users/<int:user_id>/upgrade/ --> update user to staff or admin  <br>
../login/ --> login <br>
../logout/ --> logout <br>
../users/<int:user_id>/delete/ --> delete user <br>
../users/<int:user_id/ --> view with git method update with put method delete with delete method <br>
../api/groups/ --> create new group with post method and view all the groups with git method <br>
../api/groups/<int:pk>/ --> view with git method update with put method delete with delete method <br>
../api/groups/<int:pk>/add-member/ --> Add a user to a group with id pk <br>
../api/groups/<int:pk>/join/ --> join the group with id pk <br>
../api/tasks/ --> create new task with post method and view all the tasks with git method <br>
../api/tasks/<int:task_id>/ --> view with git method update with put method delete with delete method <br>
../api/tasks/<int:task_id>/assign/ --> Assign a task to the current user <br>
../api/events/ --> create new event with post method and view all the events with git method <br>
../api/events/<int:event_id>/ --> view with git method update with put method delete with delete method <br>
../api/events/<int:event_id>/join/ --> Add current user to event attendees <br>
../api/events/<int:event_id>/leave/ --> Remove current user from event attendees <br>
../info/activities/ --> create new activitie with post method and view all the activities with git method <br>
../info/activities/<int:pk>/ --> view with git method update with put method delete with delete method <br>
../info/sponsors/ --> create new sponsor with post method and view all the sponsors with git method <br>
../info/sponsors/<int:pk>/ --> view with git method update with put method delete with delete method <br>
