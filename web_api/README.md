#API documentation
This is not documentation for current state of the API, here are listed proposed changes to standardize API REST endpoint.

All points will perpended with $DOMAIN/api.
Presumably all responses will be in JSON format.

##+/gateways
| Method        | Action           | Description  |
| ------------- | ---------------- | ------------ |
| GET    | return list of gateways      | format of each gateway will be corresponding to the data model |
| DELETE |  delete gateways with ids    |   id enumerated in array in Request-URI ids (bulk job, should be accessible only to administrator or system itself) |
| PUT    | replace the list of gateways | deletes the old list and creates new based on provided data (bulk job, should be accessible only to administrator or system itself) |
| POST   | add gateways to the list     |  add array of gateways to the list (bulk job, should be accessible only to administrator or system itself) |
##+/gateway
| Method        | Action           | Description  |
| ------------- | ---------------- | ------------ |
| GET  | return data-model      |  data-model which is required to register a new gateway, optional parameters tagged (optional) |
| POST | register a new gateways    |   returns id assigned by the system? |
##+/gateway/{id}
| Method        | Action           | Description  |
| ------------- | ---------------- | ------------ |
| GET  | return gateway info      |  provide information about the gateway which has id == {id} |
| POST | adds additional parameters     | to the gateway which has id == {id} (overrides parameters which are already set?) |
| PUT  | replace whole gateway information      |  deletes old information, creates new gateway info with same id  |
| DELETE  | deletes gateway from the system     |  -  |
##+/users
| Method        | Action           | Description  |
| ------------- | ---------------- | ------------ |
| GET    | return list of users      | format of each users will be corresponding to the data model |
| DELETE |  delete users with ids    |   id enumerated in array under Request-URI ids (bulk job, should be accessible only to administrator or system itself) |
| PUT    | replace the list of users | deletes the old list and creates new based on provided data (bulk job, should be accessible only to administrator or system itself) |
| POST   | add users to the list     |  add array of users to the list (bulk job, should be accessible only to administrator or system itself) |
##+/user
| Method        | Action           | Description  |
| ------------- | ---------------- | ------------ |
| GET  | return data-model      |  data-model which is required to register a new user, optional parameters tagged (optional) |
| POST | register a new user    |   returns id assigned by the system? |
##+/user/{id}
| Method        | Action           | Description  |
| ------------- | ---------------- | ------------ |
| GET  | return user info      |  provide information about the user which has id == {id} |
| POST | adds additional parameters     | to the user which has id == {id} (overrides parameters which are already set?) |
| PUT  | replace whole user information      |  deletes old information, creates new user info with same id  |
| DELETE  | deletes user from the system     |  -  |

# Setup

Make sure you have 

```
DB_HOST=localhost
```

defined before starting manage.py!!
