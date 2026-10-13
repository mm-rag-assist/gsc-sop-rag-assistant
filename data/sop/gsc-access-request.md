---
doc_id: gsc-access-request
title: "GSC - Access Request"
tool: Google Search Console
source: "DemoCorp Search Support SOP (anonymized)"
language: en
---

# GSC - Access Request

This document is intended to provide a **Standard Operating Procedure** for Google Search Console access requests.

## How to grant GSC access?

1. **In TicketDesk** assign the ticket to yourself. Click ***Assign to Me***.
2. Click ***Begin Work***.
3. Set the ***Component*** as *Access – Google Webmaster Tools/Google Search Console*, then click **Save**.
4. **Log in to Google Search Console** <https://search.google.com/search-console/about> with searchsupport@democorp.example credentials.
5. **Find the property** on the list on the left-hand side. Copy it or start typing its name.
6. Click ***Settings***, then ***Users and permissions***.
7. Click ***ADD USER***.
8. Copy the email from the ticket’s field ***Email address for which the access is required***.
9. If the email is @democorp.example, follow **step 10**. If it’s an agency email, follow **step 11**.
10. In the case of @democorp.example emails, you always have to check if the DemoCorp email has a managed account. You can check it [here](#how-to-check-if-the-democorp-user-has-a-managed-account). Once the user has a managed account, follow **step 11**.
11. In the case of agency emails, you don’t need to check if the user has a managed account.

    **IMPORTANT:** Always check if the email you’ve granted access to is the same on the list of users in GSC after the access is granted. It may happen that the e-mail will change (e.g. from test@agency-two.example into test@gmail.com) and that’s probably because it is not associated with a Google account. In such case, remove the access you’ve just granted and follow instructions [here](#what-to-do-if-users-email-changed-to-gmail-or-a-different-email).
12. In order to grant access, paste copied email address from ticket to GSC form, set ***Permission*** to ***Restricted*** and click ***ADD***.
13. If, while granting access, you see an error ***Failed to add user: email not found***, see the instructions [here](#failed-to-add-user-email-not-found).
14. Once the access is granted properly, report the access in ***DemoCorp WMT Access/Verification Requests Management*** file in *Access* tab.
15. **Fill in** (screenshots omitted in this version):
    - Status (YTS=yet to start, WIP=work in progress, CLD=completed, SUSP=suspended)
    - Search engine
    - Type
    - Requested URL/Website (we grant access mainly to domain properties, which means without http, https, www)
    - Registered for (e-mail address the access is granted for)
    - \# of requests (merge the rows according to the ticket’s needs)
    - Close Date
    - Open Date
    - Ticket (paste the number of ticket)
    - Opened By (TicketDesk=via ticket, e-mail if someone sends an urgent e-mail)
    - WMT Permission (restricted, full, admin)
    - Person Responsible (who was assigned to manage the ticket)
16. Respond to the requestor in ***Work Notes*** in *Additional comments (Customer visible)*. Use one of the reply templates below.
17. Close the ticket:
    1. In *Closure Information* write ‘GSC access granted’.
    2. Choose ‘Fulfilled’ in Closure Code.
    3. Click Complete work.
    4. The next day, if there are no comments from the requestor, click Close record.

### Reply templates – access granted

**Template 1 – several domain properties** (customer visible):

```text
GSC access has been granted for [EMAIL] to the following domain properties:
[LIST OF DOMAIN PROPERTIES].

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

**Template 2 – one domain property** (customer visible):

```text
GSC access has been granted for [EMAIL] to [DOMAIN PROPERTY].

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

**Template 3 – one domain property, alternative wording** (customer visible):

```text
I’ve just granted GSC access for [EMAIL] to [DOMAIN PROPERTY].

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

**Template 4 – one domain property, full tool name** (customer visible):

```text
I’ve just granted Google Search Console access for [EMAIL] to [DOMAIN PROPERTY].

Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

Kind regards,
```

## What to do if user’s email changed to Gmail or a different email

1. There may be a situation when you have just granted GSC access and the email changed to Gmail or different email.

   For example: I wanted to grant access to requester@agency-one.example. However, once the access was granted, this email *requester.private@gmail.com* appeared on the list of users in GSC, instead of this requester@agency-one.example. It's probably because the email is not associated with a Google account.
2. In such case remove the access in GSC. You may need to use horizontal scrollbar to see the removal button.
3. Respond to the requestor in Work Notes and attach **DemoCorp GSC User Access Policy.pdf** file in the ticket.

   **Reply to requestor** (customer visible):

   ```text
   When trying to grant access for [EMAIL in the ticket], this email EMAIL@gmail.com appears in Google Search Console.
   Please see the file attached and associate your email with a Google account.
   Provide us with feedback within 2 business days, otherwise we’ll have to reject this ticket.
   ```
4. If the requestor responds, grant the access to the right email and close the ticket.
5. Otherwise, [reject the ticket](#how-to-reject-a-ticket) and respond in Work Notes.

   **Reply to requestor** (customer visible):

   ```text
   We haven’t received any response from you, therefore we reject the ticket.

   If you still need GSC access, raise a new ticket and let us know the correct email address.
   ```

## Failed to add user: email not found

1. If this error pops up after you have added the user to GSC, respond in the ticket.

   **Reply to requestor** (customer visible):

   ```text
   I cannot grant Google Search Console access for this email [USER’S EMAIL] because there's an error in GSC saying that this email is not found.

   Please check if the email is associated with a Google account properly (see the attachment). Also, check if there's a typo in the email address.

   Let me know within 2 business days, please.
   ```
2. Attach **DemoCorp GSC User Access Policy.pdf** file in the ticket.
3. Wait for 2 days. If there’s no response from the requestor, [reject the ticket](#how-to-reject-a-ticket).

## How to reject a ticket?

1. Go to *Closure Information* tab and write the reason for ticket rejection in *Resolution Notes*. For example: No response from the requestor.
2. Choose Request Rejected in Closure Code and click *Complete work* in the top right-hand corner.
3. Then, click **Close Record**.

## How to check if the DemoCorp user has a managed account

1. Connect to the DemoCorp corporate VPN.
2. Log in to <https://access-portal.democorp.example/> using your personal DemoCorp account.
3. From the navigation column choose: ‘Menu’ → ‘Manage Access’ → ‘Manage User Access’.
4. Type user's shortname in the search field (1) and click search button (2), then check the selection icon (3) and click ‘Next’ (4).
5. Type ‘Googlecloud’ in a search field and click search icon.
6. Check the selection icon next to GoogleCloud group.
7. If “Cannot Add Access Item >> The item you are trying to select is already assigned.” message pops up, it means the user has already had a *managed account* created.
8. If you don’t see this message, it means the user doesn't have a *managed account*.
9. In such case, you have to create a managed account for the user. See instructions below.

## How to create a managed account?

1. Connect to the DemoCorp corporate VPN.
2. Log in to <https://access-portal.democorp.example/> using your personal DemoCorp account.
3. From the navigation column choose: ‘Menu’ → ‘Manage Access’ → ‘Manage User Access’.
4. Type user's short name in the search field (1) and click search button (2), then check the selection icon (3) and click ‘Next’ (4).
5. Type ‘Googlecloud’ in a search field.
6. Check the selection icon next to Google Cloud group and click ‘Next’. Review if you have similar view, if yes click ‘submit’.
7. See your request confirmation. Your request should be approved up to 24 hours (but sometimes it takes longer).
8. The next day, check if the user has been added. Go to <https://access-portal.democorp.example/> - *My work - Access requests*.
9. There can be two options – request completed or failed:
   - If **completed**, the requested managed Google account has been created.
   - If the request has failed, contact the DemoCorp access manager <access-manager@democorp.example> and describe the case.

## How to handle a request to grant full access?

1. Since we cannot verify the changes made by users, we refuse to grant full access to GSC and we are [rejecting the ticket](#how-to-reject-a-ticket).

   **Reply to requestor** (customer visible):

   ```text
   Hello,

   By default, we grant restricted access only. Changes to the GSC are handled by Search Support via tickets.

   Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

   Kind regards,
   ```
2. If a user insists on this level of access despite a negative response, we consult the DemoCorp access manager each time.
3. If a user requests full access to connect another service to the GSC, we ask him to grant us full access to that service. Then, we establish the connection.
