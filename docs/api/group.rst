group
=================

This endpoint is handled by :py:mod:`group.views`

.. http:get:: /api/group/(int:id)
   :synopsis: View group information

   View basic information about a group

   This endpoint is handled by :py:func:`group.views.GroupViewDetail.get`

   **Example request**:

   .. sourcecode:: http

      GET /api/group/1 HTTP/1.1
      Host: social.whs.in.th
      Accept: application/json, text/javascript
      Cookie: sessionid=.....

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      X-Frame-Options: SAMEORIGIN
      Allow: GET, HEAD, OPTIONS

      {"name":"test","description":"Description text","short_description":"Requirement to join group","activities":"Group activity text","type":0,"member_status":-1}

   :>json string name: Group name
   :>json string description: What's this group about
   :>json string short_description: Requirement to join group
   :>json int type: 0 = normal, 1 = classroom
   :>json int member_status: -1 = not a member, 0 = request pending, 1 = member, 2 = administrator
   :statuscode 404: No such group