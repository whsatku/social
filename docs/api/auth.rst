auth
=================

This endpoint is handled by :py:mod:`authapi.views`

.. http:get:: /api/auth/check
   :synopsis: Validate current user session

   Check whether the current user is logged in
   and retrieve information about the user.

   This endpoint is handled by :py:func:`authapi.views.UserViewSet.get`

   **Example request**:

   .. sourcecode:: http

      GET /api/auth/check HTTP/1.1
      Host: social.whs.in.th
      Accept: application/json, text/javascript
      Cookie: sessionid=.....

   **Example response when logged in**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      X-Frame-Options: SAMEORIGIN
      Allow: GET, HEAD, OPTIONS

      "whs"

   **Example response when not logged in**:

   .. sourcecode:: http

      HTTP/1.1 403 FORBIDDEN
      Content-Type: application/json
      X-Frame-Options: SAMEORIGIN
      Allow: GET, HEAD, OPTIONS

      ""

   :>json string username: Username of current user
   :statuscode 403: User is not logged in

.. http:post:: /api/auth/login
   :synopsis: Log a user in by username/password

   Authenticate user in by username/password combination. For Youniversity,
   it is usually used to authenticate against KU database via IMAP.

   This endpoint is handled by :py:func:`authapi.views.LoginViewSet.post`

   **Example request**:

   .. sourcecode:: http

      POST /api/auth/login HTTP/1.1
      Host: social.whs.in.th
      Accept: application/json, text/plain, */*
      Content-Type:application/json;charset=UTF-8

      {username: "example", password: "example"}

   **Example of success response**:

   .. sourcecode:: http

      HTTP/1.0 200 OK
      X-Frame-Options: SAMEORIGIN
      Content-Type: application/json
      Allow: POST, OPTIONS
      Set-Cookie: csrftoken=Q0oxVmaGJUkyIV9tWuaLjl5yySa4HMcE; expires=Sun, 02-Oct-2016 09:37:27 GMT; Max-Age=31449600; Path=/
      Set-Cookie: sessionid=2cceti4ju0x6t3l8wl62awpdttl6sp2p; expires=Sun, 18-Oct-2015 09:37:27 GMT; httponly; Max-Age=1209600; Path=/

      "whs"

   **Example of failed response**:

   .. sourcecode:: http

      HTTP/1.0 403 FORBIDDEN
      X-Frame-Options: SAMEORIGIN
      Content-Type: application/json
      Allow: POST, OPTIONS

      {"detail":"Cannot log you in"}

   :<json string username: Username
   :<json string password: Password
   :>json string username: Username of current user
   :statuscode 403: Cannot log user in with given credentials. The credentials may be invalid, the server may not be able to connect to authentication database, or the user may be disabled.