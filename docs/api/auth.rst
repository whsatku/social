auth
=================

This endpoint is handled by :py:mod:`authapi.views`

.. http:get:: /api/auth/check
   :synopsis: Validate current user session

   This API is used to check whether the current user is logged in
   and to retrieve information about the user.

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

   :statuscode 403: User is not logged in