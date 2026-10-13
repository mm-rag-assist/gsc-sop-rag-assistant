---
doc_id: gsc-mark-errors-as-fixed
title: "GSC - Mark errors as fixed"
tool: Google Search Console
source: "DemoCorp Search Support SOP (anonymized)"
language: en
---

# GSC - Mark errors as fixed

This document is intended to provide a **Standard Operating Procedure** for marking errors as fixed in Google Search Console.

## How to mark errors as fixed in GSC?

1. If the request is not assigned yet, assign it to yourself in the TicketDesk platform by clicking the ***Assign to Me*** button.
2. Start working on the request by clicking the ***Begin Work*** button.
3. Set the **Component** as **SEO / Webmaster Tools**, then click **Save**.
4. In **Case Detail** check the ticket’s **Details**, where the requestor should provide description what errors should be marked as fixed.
5. Log in to Google Search Console <https://search.google.com/search-console/about> with searchsupport@democorp.example credentials.
6. Find domain property on the list on the left-hand side. Copy/paste it or start typing its name.
7. Find relevant menu position depending on the case details. In our example **Core Web Vitals**. Then click **OPEN REPORT** on **Mobile**.
8. In the next step scroll down report to find list of errors and click relevant one to fix.
9. On the error page click **VALIDATE FIX**.
10. Repeat steps 7 – 9 for all errors listed in **Case Details**.
11. Report the indexing in *DemoCorp WMT Access/Verification Requests Management* file in **Other** tab.
12. Fill in (screenshots omitted in this version):
    - Status (YTS=yet to start, WIP=work in progress, CLD=completed, SUSP=suspended)
    - Search engine: Google
    - Type: Mark errors as fixed
    - Requested URL/Website (paste the website URL)
    - \# of requests (number of marked errors)
    - Close Date
    - Open Date
    - Ticket (paste the number of ticket)
    - Person Responsible (person that was assigned to manage the ticket)
13. Complete the request:
    1. Respond to the requestor in **Work Notes** in **Additional comments (Customer visible)**, for example:

       ```text
       Hello,
       Validation for [description of errors marked as fixed] has been started.

       Once this ticket is closed, you'll receive a brief survey about our support. We'd appreciate your feedback.

       Kind regards,
       ```
    2. In **Closure Information** write **Validation started**.
    3. Choose **Fulfilled** in **Closure Code**.
    4. Click **Complete work**.
    5. The next day, if there are no comments from the requestor, click **Close record**.
