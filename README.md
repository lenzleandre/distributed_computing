FRIENDSHIP SERVICE
==================
Three functions are handled in this service, for impacting resources of application through URLs:

>>Reading and displaying friends of a given user, this is performed by HTTP Method 'GET'.

>>Creating friendship by entering into the friend_DB database.
  in this DB, a couple of username and friend, both have to be not NULL, and a couple can only be once registered.(PRIMARY KEY)

>>Deleting a registered friendship with HTTP method 'DELETE'
  The targeted couple is removed from friend_DB by specifying (username and friend). this specification is required because one user can have many friends

