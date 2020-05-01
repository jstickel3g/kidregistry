### GET /children - list all kids, ages, names
### GET /child - given 1, 2, or 3, give the detials of the kid in JSON format
### POST /children - adds a kid - no index means add the latest.
### DELETE /child - Removes a kid, by name or index number

## Usage
All responses will have the form

```JSON
{
    "data":"Mixed type detailing the content of the response",
    "message":"Info on what actually occurred"
}
```

### List all children
**Definition**

`GET /children`

**Response**

- `200 OK` on success
```JSON
[
    {
        "index": 1,
        "name": "Miranda",
        "gender": "female",
        "dob": "02/21/2002",
        "age": 18
    },
    {
        "index": 2,
        "name": "Mayan",
        "gender": "female",
        "dob": "09/18/2003",
        "age": 16
    }
]
```

### Adding a new child
**Definition**

`POST /children`

**Arguments**
- `"name":string` name of the new child
- `"gender":string` gender of the child. "male" and "female" are only acceptable values
- `"dob":date` Child's date of birth. Must be valid date format.

If a child with the given name already exists, the existing child will be overwritten.

**Response**

- `201 Created` on successful add
```JSON
{
    "index": 1,
    "name": "Miranda",
    "gender": "female",
    "dob": "02/21/2002",
    "age": 18
}
```

### Lookup a child by name
**Definition**
`GET /child/<name>`

**Response**

_ `404 Not Found` if the child's name doesn't exist
- `200 OK` if child exists with matching name
```JSON
{
    "index": 1,
    "name": "Miranda",
    "gender": "female",
    "dob": "02/21/2002",
    "age": 18
}
```

### Lookup a child by index number
**Definition**
`GET /child/<index number>`

**Response**

_ `404 Not Found` if a child w/ the given index number doesn't exist
- `200 OK` if child exists with matching index number
```JSON
{
    "index": 1,
    "name": "Miranda",
    "gender": "female",
    "dob": "02/21/2002",
    "age": 18
}
```

### Delete a Child by name

**Definition**

`DELETE /children/<name>`

**Response**
- `404 Not Found` if no child with given name exists
- `204 No Content` Successful removal of child with given names

### Delete a child  by index number

**Definition**

`Delete /children/<index>`

**Response**
- `404 Not Found` if no child with given index number
- `204 No Content` Successful removal of child with given index number
